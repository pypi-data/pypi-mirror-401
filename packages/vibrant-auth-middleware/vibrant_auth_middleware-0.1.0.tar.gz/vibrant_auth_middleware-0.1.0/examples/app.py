"""Example FastAPI app demonstrating VibrantAuthMiddleware integration."""

import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from vibrant_auth_middleware import SigningMaterial, MiddlewareSettings, VibrantAuthMiddleware

# Create FastAPI app
app = FastAPI(title="Vibrant Auth Example")

# Load signing material from environment
# In production, load from your secret manager, config service, or file
material = SigningMaterial(
    hs256_secret=os.environ.get("JWT_HS256_SECRET", "example-secret-key-min-32-chars-long"),
    rs256_public_keys={
        "key-2024": os.environ.get("JWT_RS256_PUBLIC_KEY", "-----BEGIN PUBLIC KEY-----\nMIIBIj...")
    },
    version=os.environ.get("JWT_VERSION", "1.0.0")
)

# Configure middleware settings
middleware_settings = MiddlewareSettings(
    signing_material=material,
    clock_skew_leeway=30,
)

# Add VibrantAuthMiddleware as the first middleware in the chain
app.add_middleware(VibrantAuthMiddleware, settings=middleware_settings)


@app.get("/")
async def root():
    """Public endpoint (still goes through auth middleware)."""
    return {"message": "Hello from Vibrant Auth example"}


@app.get("/profile")
async def read_profile(request: Request):
    """Protected endpoint requiring valid JWT."""
    decision = request.state.auth_decision

    if decision.status != "allow":
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Unauthorized",
                "reason": decision.reason,
                "correlation_id": getattr(request.state, "correlation_id", "unknown"),
            },
        )

    return {
        "sub": decision.principal,
        "claims": decision.claims,
        "message": "Profile accessed successfully",
    }


@app.get("/admin")
async def admin_endpoint(request: Request):
    """Admin endpoint with additional authorization checks."""
    decision = request.state.auth_decision

    if decision.status != "allow":
        return JSONResponse(
            status_code=401,
            content={
                "detail": "Unauthorized",
                "reason": decision.reason,
            },
        )

    # Additional authorization check for admin role
    claims = decision.claims
    roles = claims.get("roles", [])

    if "admin" not in roles:
        return JSONResponse(
            status_code=403,
            content={
                "detail": "Forbidden",
                "reason": "insufficient_permissions",
            },
        )

    return {
        "message": "Admin access granted",
        "principal": decision.principal,
    }


@app.get("/health")
async def health_check(request: Request):
    """Health check endpoint showing auth status."""
    decision = request.state.auth_decision

    return {
        "status": "healthy",
        "auth_status": decision.status,
        "signing_material_version": getattr(
            request.state, "signing_material_version", "unknown"
        ),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
