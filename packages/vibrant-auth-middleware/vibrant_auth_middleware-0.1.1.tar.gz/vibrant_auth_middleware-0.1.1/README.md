# Vibrant Auth Middleware

A production-ready FastAPI middleware for JWT authentication with default-deny security posture and comprehensive telemetry.

## Features

- **Default-Deny Security**: All requests are denied unless a valid JWT is provided
- **Multi-Source Token Extraction**: Supports both cookie-based and Authorization header authentication
- **Algorithm Support**: HS256 (HMAC) and RS256 (RSA) JWT verification
- **Immediate Initialization**: No async bootstrap delay - middleware is ready on startup
- **Comprehensive Telemetry**: Structured JSON logging with secret redaction
- **High Performance**: <1ms overhead per request
- **Clock Skew Tolerance**: Configurable leeway for exp/nbf claims
- **Immutable Material**: Signing material is frozen after initialization for safety

## Installation

```bash
pip install vibrant-auth-middleware
```

Or with uv:

```bash
uv add vibrant-auth-middleware
```

## Quick Start

```python
import os
from fastapi import FastAPI, Request
from vibrant_auth_middleware import SigningMaterial, MiddlewareSettings, VibrantAuthMiddleware

app = FastAPI()

# Create signing material directly
material = SigningMaterial(
    hs256_secret=os.environ["JWT_HS256_SECRET"],
    rs256_public_keys={
        "key-2024": os.environ["JWT_RS256_PUBLIC_KEY"]
    },
    version="1.0.0"
)

# Configure middleware
settings = MiddlewareSettings(
    signing_material=material,
    clock_skew_leeway=30,
)

# Add middleware (must be first in chain)
app.add_middleware(VibrantAuthMiddleware, settings=settings)

@app.get("/profile")
async def read_profile(request: Request):
    decision = request.state.auth_decision

    if decision.status != "allow":
        return {"detail": "Unauthorized"}, 401

    return {
        "sub": decision.principal,
        "claims": decision.claims
    }
```

## Migration from 1.x

**Version 2.0 is a breaking change.** The middleware no longer fetches configuration from external URLs or subscribes to SSE rotation events.

### Before (1.x):

```python
settings = MiddlewareSettings(
    config_service_url="https://config.internal/auth/jwt",
    sse_channel="https://config.internal/auth/jwt/stream",
)
app.add_middleware(VibrantAuthMiddleware, settings=settings)
```

### After (2.0):

```python
# Your application now controls where/how to load signing material
import httpx

response = httpx.get("https://config.internal/auth/jwt")
data = response.json()

material = SigningMaterial(
    hs256_secret=data["hs256_secret"],
    rs256_public_keys=data["rs256_public_keys"],
    version=data["version"]
)

settings = MiddlewareSettings(signing_material=material)
app.add_middleware(VibrantAuthMiddleware, settings=settings)
```

### Breaking Changes in 2.0:

- **Removed**: `config_service_url` parameter
- **Removed**: `sse_channel` parameter
- **Removed**: `deny_on_missing_material` parameter (material is always required)
- **Removed**: `expires_at` field from `SigningMaterial`
- **Removed**: `load_initial_material()` function
- **Removed**: `subscribe_to_rotation()` function
- **Removed**: `httpx` dependency
- **Added**: `signing_material` required parameter in `MiddlewareSettings`
- **Changed**: `SigningMaterial` is now immutable (frozen dataclass)
- **Changed**: Initialization is now synchronous (no async bootstrap)

### Key Rotation Strategy:

Since automatic rotation is removed, you have several options:

1. **Graceful Restart**: Fetch new material and restart your application
2. **Multiple Keys**: Include both old and new RS256 keys during rotation window
3. **External Rotation Manager**: Poll for changes and trigger restart

```python
# Strategy 2: Multiple keys during transition
material = SigningMaterial(
    hs256_secret="current-secret",
    rs256_public_keys={
        "key-2024-01": "-----BEGIN PUBLIC KEY-----\n...",  # Old key
        "key-2024-02": "-----BEGIN PUBLIC KEY-----\n..."   # New key
    },
    version="transition-2024-02"
)
```

## Configuration

### SigningMaterial

All fields are required and validated at initialization:

| Field | Type | Description |
|-------|------|-------------|
| `hs256_secret` | str | HMAC secret for HS256 tokens (non-empty) |
| `rs256_public_keys` | dict | Mapping of key ID to PEM public key (≥1 entry) |
| `version` | str | Version identifier for tracking (non-empty) |

### MiddlewareSettings

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `signing_material` | SigningMaterial | **required** | Cryptographic material for verification |
| `clock_skew_leeway` | int | 30 | Leeway in seconds for exp/nbf claims |

## Loading Signing Material

You control where and how to load signing material. Common patterns:

### From Environment Variables

```python
import os
import json

material = SigningMaterial(
    hs256_secret=os.environ["JWT_HS256_SECRET"],
    rs256_public_keys=json.loads(os.environ["JWT_RS256_PUBLIC_KEYS"]),
    version=os.environ.get("JWT_VERSION", "1.0.0")
)
```

### From Configuration File

```python
import json
from pathlib import Path

config = json.loads(Path("config/signing-material.json").read_text())
material = SigningMaterial(**config)
```

### From Secret Manager (AWS)

```python
import boto3
import json

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='jwt-signing-material')
secret = json.loads(response['SecretString'])

material = SigningMaterial(**secret)
```

### From HTTP Endpoint

```python
import httpx

response = httpx.get("https://config.example.com/signing-material")
response.raise_for_status()
data = response.json()

material = SigningMaterial(**data)
```

## Token Sources

### Cookie-Based Authentication

```bash
curl http://localhost:8000/profile \
  -H "Cookie: access_token=<JWT>; token_type=Bearer"
```

Requirements:
- `access_token` cookie contains the JWT
- `token_type` cookie must be present

### Authorization Header

```bash
curl http://localhost:8000/profile \
  -H "Authorization: Bearer <JWT>"
```

Requirements:
- Must use `Bearer` scheme
- Token follows the scheme

## Request State

The middleware attaches the following to `request.state`:

| Attribute | Type | Description |
|-----------|------|-------------|
| `auth_decision` | AuthDecision | Complete decision object |
| `auth_claims` | dict | Sanitized JWT claims (alias) |
| `correlation_id` | str | Request correlation ID |
| `token_source` | str | "cookie" or "authorization_header" |
| `signing_material_version` | str | Current material version |

## Decision Outcomes

| Status | Reason Code | Description |
|--------|-------------|-------------|
| `allow` | `authenticated` | Valid JWT verified |
| `deny` | `missing_token` | No token found |
| `deny` | `missing_token_type` | Cookie missing token_type |
| `deny` | `invalid_prefix` | Authorization header missing "Bearer" |
| `deny` | `token_expired` | JWT exp claim in past |
| `error` | `malformed_token` | Token failed base64 decode |
| `error` | `verification_error` | Unexpected error during verification |

## Telemetry

Every request emits a structured JSON log:

```json
{
  "event": "auth_decision",
  "decision": "allow",
  "reason": "authenticated",
  "correlation_id": "abc123",
  "principal": "user@example.com",
  "token_source": "cookie",
  "signing_material_version": "v1.2.3",
  "claims": {
    "sub": "user@example.com",
    "email": "user@example.com",
    "roles": ["user"]
  }
}
```

**Secret Redaction**: Claims containing `token`, `secret`, `password`, or `key` are automatically removed.

## Error Handling

Convert `AuthDecision` to HTTP responses:

```python
from vibrant_auth_middleware.decisions import decision_to_response_body

@app.get("/api/resource")
async def protected_resource(request: Request):
    decision = request.state.auth_decision

    if decision.status != "allow":
        body = decision_to_response_body(
            decision,
            correlation_id=request.state.correlation_id
        )
        status_code = 403 if decision.status == "deny" else 500
        return JSONResponse(status_code=status_code, content=body)

    return {"data": "sensitive information"}
```

## Performance

- **Target**: <1ms overhead per request
- **Caching**: Public keys are cached per `kid`
- **Immediate Ready**: No async bootstrap delay

Run performance tests:
```bash
pytest tests/performance/test_middleware_latency.py -v
```

## Development

### Setup

```bash
# Clone and install dependencies
git clone https://github.com/your-org/vibrant-auth-middleware
cd vibrant-auth-middleware
uv sync

# Run tests
uv run pytest

# Run specific test suites
uv run pytest tests/contract/
uv run pytest tests/unit/
uv run pytest tests/integration/
uv run pytest tests/performance/
```

### Running the Example App

```bash
cd examples
uvicorn app:app --reload
```

Test with curl:
```bash
# Generate a test token (requires PyJWT)
python -c "import jwt; print(jwt.encode({'sub': 'test@example.com', 'exp': 9999999999}, 'example-secret-key-min-32-chars-long', algorithm='HS256'))"

# Use the token
curl http://localhost:8000/profile \
  -H "Cookie: access_token=<TOKEN>; token_type=Bearer"
```

## Security Considerations

1. **Validate signing material at startup** - Fail fast if invalid
2. **Rotate signing material regularly** via application restart or reload
3. **Monitor telemetry** for unusual denial patterns
4. **Set appropriate `clock_skew_leeway`** (default 30s is recommended)
5. **Keep signing material secure** - Use secret managers, not plain files

## License

MIT

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- **Issues**: https://github.com/your-org/vibrant-auth-middleware/issues
- **Docs**: https://docs.example.com/vibrant-auth-middleware
