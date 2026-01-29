# Quickstart: Direct Signing Material Initialization

**Feature**: 002-update-the-current
**Date**: 2025-10-04

## Overview

This quickstart demonstrates the new initialization pattern for the VibrantAuth middleware, where signing material is provided directly instead of being fetched from a configuration service.

## Prerequisites

- Python 3.13+
- FastAPI >=0.111
- PyJWT[crypto] >=2.9
- vibrant-auth-middleware (this refactored version)

## Quick Example

### Minimal Working Example

```python
from fastapi import FastAPI
from vibrant_auth_middleware import (
    VibrantAuthMiddleware,
    MiddlewareSettings,
    SigningMaterial
)

# 1. Create signing material
material = SigningMaterial(
    hs256_secret="your-secret-key-at-least-32-chars-long",
    rs256_public_keys={
        "key-2024": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBg...\n-----END PUBLIC KEY-----"
    },
    version="1.0.0"
)

# 2. Configure middleware
settings = MiddlewareSettings(signing_material=material)

# 3. Create FastAPI app and add middleware
app = FastAPI()
app.add_middleware(VibrantAuthMiddleware, settings=settings)

# 4. Define protected endpoints
@app.get("/protected")
def protected_route(request: Request):
    # Access authenticated claims from request state
    claims = request.state.auth_claims
    return {"user": claims.get("sub"), "data": "protected content"}
```

## Step-by-Step Guide

### Step 1: Load Signing Material

You have full control over where/how you load signing material. Common patterns:

#### Pattern A: From Environment Variables

```python
import os
import json

material = SigningMaterial(
    hs256_secret=os.environ["JWT_HS256_SECRET"],
    rs256_public_keys=json.loads(os.environ["JWT_RS256_PUBLIC_KEYS"]),
    version=os.environ.get("JWT_VERSION", "1.0.0")
)
```

#### Pattern B: From Configuration File

```python
import json
from pathlib import Path

config_file = Path("config/signing-material.json")
config = json.loads(config_file.read_text())

material = SigningMaterial(
    hs256_secret=config["hs256_secret"],
    rs256_public_keys=config["rs256_public_keys"],
    version=config["version"]
)
```

#### Pattern C: From Secret Manager

```python
import boto3
import json

# Example: AWS Secrets Manager
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='jwt-signing-material')
secret = json.loads(response['SecretString'])

material = SigningMaterial(
    hs256_secret=secret["hs256_secret"],
    rs256_public_keys=secret["rs256_public_keys"],
    version=secret["version"]
)
```

#### Pattern D: From HTTP Endpoint (Migration from Old Pattern)

```python
import httpx

# Your application now controls the HTTP call
response = httpx.get("https://config.example.com/signing-material")
response.raise_for_status()
data = response.json()

material = SigningMaterial(
    hs256_secret=data["hs256_secret"],
    rs256_public_keys=data["rs256_public_keys"],
    version=data["version"]
)
```

### Step 2: Configure Middleware Settings

```python
settings = MiddlewareSettings(
    signing_material=material,
    clock_skew_leeway=30  # Optional: JWT timestamp tolerance (default: 30 seconds)
)
```

### Step 3: Add Middleware to FastAPI

```python
from fastapi import FastAPI

app = FastAPI()

# Add middleware - initialization happens synchronously here
# Any validation errors will be raised immediately
app.add_middleware(VibrantAuthMiddleware, settings=settings)
```

### Step 4: Use Authenticated Requests

```python
from fastapi import Request

@app.get("/api/user/profile")
def get_user_profile(request: Request):
    # Middleware populates request.state on successful authentication
    auth_decision = request.state.auth_decision  # AuthDecision object
    claims = request.state.auth_claims  # JWT claims dict
    correlation_id = request.state.correlation_id  # Request tracking ID

    user_id = claims.get("sub")
    return {"user_id": user_id, "email": claims.get("email")}
```

## Handling Key Rotation

Since the middleware no longer supports automatic rotation via SSE, you must handle rotation externally:

### Rotation Strategy 1: Graceful Restart

```python
# In your application orchestration (e.g., Kubernetes, systemd)
# 1. Load new signing material
# 2. Restart application with new material
# 3. Old instances handle existing requests with old keys
# 4. New instances use new keys
```

### Rotation Strategy 2: Multiple Keys During Transition

```python
# Support both old and new RS256 keys during rotation window
material = SigningMaterial(
    hs256_secret="current-secret",
    rs256_public_keys={
        "key-2024-01": "-----BEGIN PUBLIC KEY-----\n...",  # Old key
        "key-2024-02": "-----BEGIN PUBLIC KEY-----\n..."   # New key
    },
    version="transition-2024-02"
)
```

### Rotation Strategy 3: External Rotation Manager

```python
# Application polls for material changes and restarts when detected
import schedule
import sys

def check_for_rotation():
    new_version = fetch_current_version()
    if new_version != material.version:
        print(f"New version detected: {new_version}")
        sys.exit(0)  # Orchestrator will restart with new material

schedule.every(5).minutes.do(check_for_rotation)
```

## Validation and Error Handling

### Fail-Fast Validation

```python
try:
    material = SigningMaterial(
        hs256_secret="",  # Invalid: empty secret
        rs256_public_keys={"key": "..."},
        version="1.0"
    )
except ValueError as e:
    print(f"Validation error: {e}")
    # Output: Validation error: Signing material must include hs256_secret
```

### Initialization Error Handling

```python
try:
    settings = MiddlewareSettings(signing_material=material)
    app.add_middleware(VibrantAuthMiddleware, settings=settings)
except ValueError as e:
    print(f"Middleware initialization failed: {e}")
    # Log error and exit - don't start server with invalid material
    sys.exit(1)
```

## Testing Your Integration

### Test 1: Valid Initialization

```python
def test_middleware_initialization():
    material = SigningMaterial(
        hs256_secret="test-secret-key",
        rs256_public_keys={"test-key": "-----BEGIN PUBLIC KEY-----\n..."},
        version="test-1.0"
    )
    settings = MiddlewareSettings(signing_material=material)
    middleware = VibrantAuthMiddleware(app, settings)
    assert middleware._material == material
```

### Test 2: Missing Material

```python
def test_missing_material_fails():
    with pytest.raises(ValueError, match="Signing material must include hs256_secret"):
        material = SigningMaterial(
            hs256_secret="",
            rs256_public_keys={"key": "..."},
            version="1.0"
        )
```

### Test 3: Request Authentication

```python
from fastapi.testclient import TestClient
import jwt

def test_authenticated_request():
    client = TestClient(app)

    # Generate test JWT
    token = jwt.encode(
        {"sub": "user-123", "exp": int(time.time()) + 3600},
        material.hs256_secret,
        algorithm="HS256"
    )

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["user"] == "user-123"
```

## Migration from Old Pattern

### Before (Old Pattern)

```python
# Application relied on middleware to fetch config
settings = MiddlewareSettings(
    config_service_url="https://config.example.com/signing-material",
    sse_channel="https://events.example.com/rotation"
)
middleware = VibrantAuthMiddleware(app, settings)
# Material loaded asynchronously on first request
```

### After (New Pattern)

```python
# Application manages config fetching
import httpx

# Fetch material synchronously at startup
response = httpx.get("https://config.example.com/signing-material")
data = response.json()

material = SigningMaterial(
    hs256_secret=data["hs256_secret"],
    rs256_public_keys=data["rs256_public_keys"],
    version=data["version"]
)

settings = MiddlewareSettings(signing_material=material)
middleware = VibrantAuthMiddleware(app, settings)
# Material validated immediately, ready for requests
```

## Common Pitfalls

### Pitfall 1: Empty Secrets

```python
# ❌ Wrong: Empty secret
material = SigningMaterial(hs256_secret="", ...)

# ✅ Correct: Non-empty secret
material = SigningMaterial(hs256_secret="my-secure-secret-key", ...)
```

### Pitfall 2: Missing RS256 Keys

```python
# ❌ Wrong: Empty keys dict
material = SigningMaterial(rs256_public_keys={}, ...)

# ✅ Correct: At least one key
material = SigningMaterial(
    rs256_public_keys={"key-1": "-----BEGIN PUBLIC KEY-----\n..."},
    ...
)
```

### Pitfall 3: Forgetting Validation

```python
# ❌ Wrong: Starting server despite validation error
try:
    middleware = VibrantAuthMiddleware(app, settings)
except ValueError:
    pass  # Silently ignoring error

# ✅ Correct: Fail fast on validation error
try:
    middleware = VibrantAuthMiddleware(app, settings)
except ValueError as e:
    logger.error(f"Invalid signing material: {e}")
    sys.exit(1)  # Don't start server
```

## Next Steps

- Review [contracts/initialization-contract.md](./contracts/initialization-contract.md) for detailed API contract
- See [data-model.md](./data-model.md) for validation rules
- Check existing tests in `tests/contract/test_middleware_contract.py`

---
*Quickstart ready for user testing*
