# Initialization Contract

**Feature**: 002-update-the-current
**Contract Type**: Middleware Constructor API
**Date**: 2025-10-04

## Overview

This contract defines the initialization interface for `VibrantAuthMiddleware` after removing config service URL and SSE channel dependencies.

## Constructor Signature

```python
class VibrantAuthMiddleware:
    def __init__(
        self,
        app: Callable[..., Any],
        settings: MiddlewareSettings
    ) -> None:
        """
        Initialize authentication middleware with signing material.

        Args:
            app: ASGI application callable
            settings: Middleware configuration with signing material

        Raises:
            TypeError: If settings is not MiddlewareSettings instance
            ValueError: If signing material is missing or invalid

        Example:
            material = SigningMaterial(
                hs256_secret="your-secret-key",
                rs256_public_keys={"key-1": "-----BEGIN PUBLIC KEY-----\\n..."},
                version="v1.0.0"
            )
            settings = MiddlewareSettings(signing_material=material)
            middleware = VibrantAuthMiddleware(app, settings)
        """
```

## SigningMaterial Contract

```python
@dataclass(slots=True, frozen=True)
class SigningMaterial:
    """
    Immutable cryptographic material for JWT verification.

    Fields:
        hs256_secret: HMAC secret for HS256 algorithm (required, non-empty)
        rs256_public_keys: Mapping of key ID to PEM-encoded public key (required, non-empty dict)
        version: Version identifier for tracking (required, non-empty)

    Validation:
        - All fields are required (no None values)
        - hs256_secret must be non-empty string
        - rs256_public_keys must have at least one entry
        - All rs256_public_keys values must be non-empty strings
        - version must be non-empty string
    """
    hs256_secret: str
    rs256_public_keys: Dict[str, str]
    version: str
```

## MiddlewareSettings Contract

```python
@dataclass
class MiddlewareSettings:
    """
    Runtime configuration for middleware.

    Fields:
        signing_material: Cryptographic material (required)
        clock_skew_leeway: JWT timestamp tolerance in seconds (default: 30)

    Validation:
        - signing_material must be valid SigningMaterial instance
        - clock_skew_leeway must be non-negative integer
    """
    signing_material: SigningMaterial
    clock_skew_leeway: int = 30
```

## Success Scenarios

### Scenario 1: Valid Initialization with Minimal Material
**Given**: Application has loaded signing material
**When**: Middleware is initialized with valid material
**Then**: Initialization succeeds without errors

```python
material = SigningMaterial(
    hs256_secret="test-secret-key-min-32-characters-long",
    rs256_public_keys={"default": "-----BEGIN PUBLIC KEY-----\nMIIBIj..."},
    version="1.0.0"
)
settings = MiddlewareSettings(signing_material=material)
middleware = VibrantAuthMiddleware(app, settings)
# Should succeed
```

### Scenario 2: Valid Initialization with Multiple RS256 Keys
**Given**: Application has multiple RS256 keys for key rotation
**When**: Middleware is initialized with multiple keys
**Then**: Initialization succeeds and all keys are available for verification

```python
material = SigningMaterial(
    hs256_secret="test-secret",
    rs256_public_keys={
        "key-2024-01": "-----BEGIN PUBLIC KEY-----\n...",
        "key-2024-02": "-----BEGIN PUBLIC KEY-----\n...",
        "key-2024-03": "-----BEGIN PUBLIC KEY-----\n..."
    },
    version="2024.1"
)
settings = MiddlewareSettings(signing_material=material)
middleware = VibrantAuthMiddleware(app, settings)
# Should succeed
```

### Scenario 3: Valid Initialization with Custom Clock Skew
**Given**: Application needs tight clock synchronization
**When**: Middleware is initialized with custom clock skew leeway
**Then**: Initialization succeeds with custom setting

```python
material = SigningMaterial(
    hs256_secret="test-secret",
    rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
    version="1.0"
)
settings = MiddlewareSettings(
    signing_material=material,
    clock_skew_leeway=10  # 10 seconds instead of default 30
)
middleware = VibrantAuthMiddleware(app, settings)
# Should succeed
```

## Error Scenarios

### Error 1: Missing signing_material
**Given**: Settings created without signing material
**When**: Middleware initialization is attempted
**Then**: Raises TypeError or ValueError with clear message

```python
# This should fail at MiddlewareSettings construction
settings = MiddlewareSettings()  # Missing required parameter
# Expected: TypeError: missing 1 required positional argument: 'signing_material'
```

### Error 2: Missing hs256_secret
**Given**: Signing material created without HS256 secret
**When**: Middleware initialization is attempted
**Then**: Raises ValueError with specific message

```python
material = SigningMaterial(
    hs256_secret="",  # Empty
    rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
    version="1.0"
)
# Expected: ValueError: Signing material must include hs256_secret
```

### Error 3: Empty rs256_public_keys
**Given**: Signing material created without any RS256 keys
**When**: Middleware initialization is attempted
**Then**: Raises ValueError with specific message

```python
material = SigningMaterial(
    hs256_secret="test-secret",
    rs256_public_keys={},  # Empty dict
    version="1.0"
)
# Expected: ValueError: Signing material must include at least one RS256 public key
```

### Error 4: Missing version
**Given**: Signing material created without version
**When**: Middleware initialization is attempted
**Then**: Raises ValueError with specific message

```python
material = SigningMaterial(
    hs256_secret="test-secret",
    rs256_public_keys={"key": "-----BEGIN PUBLIC KEY-----\n..."},
    version=""  # Empty
)
# Expected: ValueError: Signing material must include version identifier
```

### Error 5: Invalid RS256 key value
**Given**: Signing material with empty RS256 key value
**When**: Middleware initialization is attempted
**Then**: Raises ValueError mentioning the specific key ID

```python
material = SigningMaterial(
    hs256_secret="test-secret",
    rs256_public_keys={"key-1": "-----BEGIN PUBLIC KEY-----\n...", "key-2": ""},
    version="1.0"
)
# Expected: ValueError: RS256 public key for kid 'key-2' must be non-empty
```

### Error 6: Wrong settings type
**Given**: Non-MiddlewareSettings object passed as settings
**When**: Middleware initialization is attempted
**Then**: Raises TypeError with clear message

```python
middleware = VibrantAuthMiddleware(app, {"signing_material": material})
# Expected: TypeError: settings must be MiddlewareSettings instance
```

## Migration Error Scenarios

### Migration Error 1: Old config_service_url pattern
**Given**: Application attempts to use old config_service_url pattern
**When**: Middleware initialization is attempted
**Then**: Raises ValueError with migration guidance

```python
# If we detect this pattern (through temporary compatibility check)
# Expected: ValueError: config_service_url is no longer supported.
#           Pass signing material directly via signing_material parameter.
#           See migration guide: [URL]
```

### Migration Error 2: Old sse_channel pattern
**Given**: Application attempts to use old sse_channel pattern
**When**: Middleware initialization is attempted
**Then**: Raises ValueError with migration guidance

```python
# If we detect this pattern
# Expected: ValueError: sse_channel is no longer supported.
#           Handle key rotation externally and restart the middleware.
#           See migration guide: [URL]
```

## Backward Compatibility

**Breaking Change**: This contract represents a breaking change from previous versions.

**Previous Pattern**:
```python
settings = MiddlewareSettings(
    config_service_url="https://config.example.com/signing-material",
    sse_channel="https://events.example.com/rotation"
)
middleware = VibrantAuthMiddleware(app, settings)
```

**New Pattern**:
```python
# Application fetches material itself
response = httpx.get("https://config.example.com/signing-material")
data = response.json()

material = SigningMaterial(
    hs256_secret=data["hs256_secret"],
    rs256_public_keys=data["rs256_public_keys"],
    version=data["version"]
)
settings = MiddlewareSettings(signing_material=material)
middleware = VibrantAuthMiddleware(app, settings)
```

## Contract Tests

Contract tests must verify:
1. Valid initialization succeeds
2. Each validation error scenario raises appropriate exception
3. Error messages are clear and actionable
4. Material is immutable after initialization
5. Middleware is immediately ready (no async bootstrap)

See `tests/contract/test_middleware_contract.py` for implementation.

---
*Contract ready for test implementation*
