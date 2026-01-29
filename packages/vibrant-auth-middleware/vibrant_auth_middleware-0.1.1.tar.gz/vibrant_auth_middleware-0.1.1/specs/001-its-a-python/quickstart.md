# Quickstart: FastAPI JWT Access Middleware

## Prerequisites
- Python 3.13 runtime
- FastAPI application using ASGI server (e.g., Uvicorn)
- Access to the configuration service providing signing material and SSE rotation channel

## Installation
```bash
pip install vibrant-auth-middleware
```

## Configuration
1. Obtain your configuration service endpoints:
   - `CONFIG_SERVICE_URL`: HTTPS endpoint returning the latest signing material.
   - `CONFIG_SERVICE_SSE`: SSE channel path for rotation notifications.
2. Configure the middleware (environment variables or settings object):
```bash
export VIBRANT_CONFIG_URL="https://config.internal/auth/jwt"
export VIBRANT_CONFIG_SSE="https://config.internal/auth/jwt/stream"
```

## Usage in FastAPI
```python
from fastapi import FastAPI
from vibrant_auth_middleware import VibrantAuthMiddleware, MiddlewareSettings

app = FastAPI()

app.add_middleware(
    VibrantAuthMiddleware,
    settings=MiddlewareSettings(
        config_service_url="https://config.internal/auth/jwt",
        sse_channel="https://config.internal/auth/jwt/stream",
        clock_skew_leeway=30,
    ),
)

@app.get("/profile")
async def read_profile(request):
    decision = request.state.auth_decision
    if decision.status != "allow":
        return {"detail": "Unauthorized"}, 401
    return {"sub": decision.principal, "claims": decision.claims}
```

## Verifying Behavior Locally
1. Start a mock configuration service returning HS256 material.
2. Launch your FastAPI app with the middleware.
3. Issue a request with cookies:
```bash
http --follow GET :8000/profile \
  Cookie:"access_token=...; token_type=Bearer"
```
4. Issue a request with an Authorization header:
```bash
http --follow GET :8000/profile \
  Authorization:"Bearer ..."
```
5. Observe structured logs for `decision=allow` or `decision=deny` along with reason codes.

## Rotation Drill
- Trigger a rotation event (publish to SSE channel).
- Confirm middleware denies requests until refreshed material is applied and logs `reason=rotation_pending`.
