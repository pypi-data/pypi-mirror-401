# Data Model: Remove Config Service URL and SSE Channel Dependencies

**Feature**: 002-update-the-current
**Date**: 2025-10-04

## Overview

This document defines the data structures and validation rules for the refactored middleware initialization model.

## Entities

### 1. SigningMaterial

**Purpose**: Contains cryptographic keys and metadata for JWT verification

**Before (Current)**:
```python
@dataclass(slots=True)
class SigningMaterial:
    hs256_secret: Optional[str]
    rs256_public_keys: Dict[str, str]
    version: str
    expires_at: Optional[datetime]  # ← TO BE REMOVED
```

**After (Refactored)**:
```python
@dataclass(slots=True, frozen=True)
class SigningMaterial:
    """
    Cryptographic material for JWT verification.

    All fields are required. Material is immutable after construction.
    To update signing material, restart the middleware with new material.
    """
    hs256_secret: str  # Required: HMAC secret for HS256 tokens
    rs256_public_keys: Dict[str, str]  # Required: kid → PEM public key mapping
    version: str  # Required: Version identifier for tracking/debugging
```

**Changes**:
- Removed `expires_at` field (no expiration support)
- Changed `hs256_secret` from `Optional[str]` to `str` (required)
- Added `frozen=True` to make immutable (signals no runtime updates)
- Removed `is_expired()` method (no longer needed)

**Validation Rules**:
| Rule | Check | Error Message |
|------|-------|---------------|
| VR-1 | `hs256_secret` is non-empty string | "Signing material must include hs256_secret" |
| VR-2 | `rs256_public_keys` is non-empty dict | "Signing material must include at least one RS256 public key" |
| VR-3 | `version` is non-empty string | "Signing material must include version identifier" |
| VR-4 | All `rs256_public_keys` values are non-empty strings | "RS256 public key for kid '{kid}' must be non-empty" |

**Invariants**:
- Material is immutable after construction
- Both HS256 and RS256 algorithms are always available
- Version is always set for debugging/telemetry

---

### 2. MiddlewareSettings

**Purpose**: Runtime configuration for middleware behavior

**Before (Current)**:
```python
@dataclass
class MiddlewareSettings:
    config_service_url: str = ""  # ← TO BE REMOVED
    sse_channel: str = ""  # ← TO BE REMOVED
    clock_skew_leeway: int = 30
    deny_on_missing_material: bool = True  # ← NO LONGER NEEDED
```

**After (Refactored)**:
```python
@dataclass
class MiddlewareSettings:
    """
    Runtime configuration for authentication middleware.

    signing_material is required and must be valid.
    """
    signing_material: SigningMaterial  # Required: Direct material (no URL fetching)
    clock_skew_leeway: int = 30  # JWT exp/nbf clock tolerance in seconds
```

**Changes**:
- Removed `config_service_url` (no HTTP fetching)
- Removed `sse_channel` (no SSE subscription)
- Removed `deny_on_missing_material` (material is always present and validated)
- Added `signing_material: SigningMaterial` as required field

**Validation Rules**:
| Rule | Check | Error Message |
|------|-------|---------------|
| VS-1 | `signing_material` is not None | "MiddlewareSettings requires signing_material" |
| VS-2 | `signing_material` passes all SigningMaterial validation | (delegate to SigningMaterial validation) |
| VS-3 | `clock_skew_leeway` is non-negative integer | "clock_skew_leeway must be non-negative" |

**Invariants**:
- Material is always present and valid
- Clock skew leeway is reasonable (0-300 seconds recommended)

---

### 3. VibrantAuthMiddleware (Constructor Changes)

**Purpose**: ASGI middleware for JWT authentication

**Before (Current)**:
```python
def __init__(
    self,
    app: Callable[..., Any],
    settings: MiddlewareSettings | None = None
) -> None:
    self.app = app
    self.settings = settings or MiddlewareSettings()
    self._material: Optional[SigningMaterial] = None  # Lazy-loaded
    # ... async initialization state ...
```

**After (Refactored)**:
```python
def __init__(
    self,
    app: Callable[..., Any],
    settings: MiddlewareSettings
) -> None:
    """
    Initialize middleware with signing material.

    Args:
        app: ASGI application
        settings: Configuration including signing material (required)

    Raises:
        ValueError: If signing_material is missing or invalid
    """
    self.app = app

    # Validate settings immediately (fail-fast)
    if not isinstance(settings, MiddlewareSettings):
        raise TypeError("settings must be MiddlewareSettings instance")

    _validate_signing_material(settings.signing_material)

    self.settings = settings
    self._material: SigningMaterial = settings.signing_material  # Direct assignment

    # No async initialization state needed
```

**Changes**:
- `settings` parameter is now required (no default)
- Validation happens synchronously in `__init__`
- Removed: `_material_ready`, `_bootstrap_lock`, `_refresh_lock`, `_rotation_pending`, `_rotation_task`
- `_material` is directly assigned from settings (not lazy-loaded)

**Validation Rules**:
| Rule | Check | Error Message |
|------|-------|---------------|
| VM-1 | `settings` is provided | "settings parameter is required" |
| VM-2 | `settings` is MiddlewareSettings instance | "settings must be MiddlewareSettings instance" |
| VM-3 | `settings.signing_material` is valid | (delegate to SigningMaterial validation) |

---

## Data Flow

### Initialization Flow

```
Application Startup
    ↓
1. Application loads signing material from its config source
   (file, environment, secret manager, HTTP endpoint, etc.)
    ↓
2. Application constructs SigningMaterial(hs256_secret=..., rs256_public_keys=..., version=...)
    ↓
3. Validation runs automatically on SigningMaterial construction
   - If invalid → ValueError raised immediately
    ↓
4. Application constructs MiddlewareSettings(signing_material=material, ...)
    ↓
5. Application instantiates VibrantAuthMiddleware(app, settings)
    ↓
6. Middleware validates in __init__():
   - Type checks
   - Signing material validation
   - If invalid → ValueError raised immediately
    ↓
7. Middleware is ready - material is immutable
    ↓
Request Processing (material never changes)
```

### Request Verification Flow (Unchanged)

```
HTTP Request
    ↓
Extract token from headers/cookies
    ↓
Verify using self._material (always available)
    ↓
Allow or Deny
```

## Validation Implementation

### Validation Function

```python
def _validate_signing_material(material: SigningMaterial) -> None:
    """
    Validate signing material structure and content.

    Raises:
        ValueError: If material is invalid with specific error message
    """
    if not material:
        raise ValueError("Signing material is required")

    if not material.hs256_secret:
        raise ValueError("Signing material must include hs256_secret")

    if not isinstance(material.rs256_public_keys, dict):
        raise ValueError("rs256_public_keys must be a dictionary")

    if not material.rs256_public_keys:
        raise ValueError("Signing material must include at least one RS256 public key")

    for kid, pem_key in material.rs256_public_keys.items():
        if not pem_key:
            raise ValueError(f"RS256 public key for kid '{kid}' must be non-empty")

    if not material.version:
        raise ValueError("Signing material must include version identifier")
```

### Migration Validation

For backward compatibility detection:

```python
# In MiddlewareSettings or __init__
if hasattr(settings, 'config_service_url') and settings.config_service_url:
    raise ValueError(
        "config_service_url is no longer supported. "
        "Pass signing material directly via signing_material parameter. "
        "See migration guide: [URL]"
    )

if hasattr(settings, 'sse_channel') and settings.sse_channel:
    raise ValueError(
        "sse_channel is no longer supported. "
        "Handle key rotation externally and restart the middleware. "
        "See migration guide: [URL]"
    )
```

## State Transitions

**Before**:
```
Middleware Created → Bootstrap Pending → Material Loaded → Rotation Listening
                                ↓
                         Rotation Event → Material Updating → Material Updated
```

**After**:
```
Middleware Created (with validated material) → Ready
                                               ↓
                                      (immutable - no state changes)
```

## Testing Scenarios

### Valid Construction
1. Material with all required fields → Success
2. Multiple RS256 keys → Success
3. Version as UUID string → Success
4. Version as semantic version → Success

### Invalid Construction (Should Raise ValueError)
1. Missing hs256_secret → "Signing material must include hs256_secret"
2. Empty hs256_secret → "Signing material must include hs256_secret"
3. Empty rs256_public_keys dict → "Signing material must include at least one RS256 public key"
4. rs256_public_keys with empty value → "RS256 public key for kid 'key-id' must be non-empty"
5. Missing version → "Signing material must include version identifier"
6. Empty version → "Signing material must include version identifier"

### Migration Detection
1. Settings with config_service_url set → Error mentioning migration
2. Settings with sse_channel set → Error mentioning migration

---
*Data model design complete - ready for contract generation*
