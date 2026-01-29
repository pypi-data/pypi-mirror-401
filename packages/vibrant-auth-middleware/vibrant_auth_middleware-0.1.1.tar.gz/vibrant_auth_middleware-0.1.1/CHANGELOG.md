# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-04

### BREAKING CHANGES

This is a major version with significant breaking changes. The middleware no longer handles configuration fetching or rotation automatically. Applications now have full control over signing material management.

#### Removed Features

- **Removed** `config_service_url` from `MiddlewareSettings`
- **Removed** `sse_channel` from `MiddlewareSettings`
- **Removed** `deny_on_missing_material` from `MiddlewareSettings` (material is always required and validated)
- **Removed** `expires_at` field from `SigningMaterial` dataclass
- **Removed** `is_expired()` method from `SigningMaterial`
- **Removed** `load_initial_material()` async function
- **Removed** `subscribe_to_rotation()` async function
- **Removed** `_ensure_bootstrap()` async method from middleware
- **Removed** `_listen_for_rotations()` async method from middleware
- **Removed** `_handle_rotation_event()` async method from middleware
- **Removed** httpx dependency (no longer needed for config fetching)
- **Removed** `rotation_pending` denial reason (rotation no longer handled by middleware)

#### Changed Features

- **Changed** `SigningMaterial` is now immutable (frozen dataclass)
- **Changed** `SigningMaterial.hs256_secret` is now required (str instead of Optional[str])
- **Changed** `MiddlewareSettings.signing_material` is now a required parameter
- **Changed** `VibrantAuthMiddleware.__init__` now requires `settings` parameter (no longer optional)
- **Changed** Initialization is now synchronous with immediate validation (fail-fast)
- **Changed** Version bumped to 2.0.0 to reflect breaking changes

#### Added Features

- **Added** `_validate_signing_material()` function with strict validation rules
- **Added** Type checking for `MiddlewareSettings` in middleware initialization
- **Added** Immediate readiness - no async bootstrap delay
- **Added** Contract tests for new initialization patterns
- **Added** Integration tests for validation and immutability

### Migration Guide

#### Before (1.x):
```python
settings = MiddlewareSettings(
    config_service_url="https://config.internal/auth/jwt",
    sse_channel="https://config.internal/auth/jwt/stream",
)
app.add_middleware(VibrantAuthMiddleware, settings=settings)
```

#### After (2.0):
```python
# Load signing material from your preferred source
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

### Validation Rules

SigningMaterial validation now enforces:
- `hs256_secret` must be non-empty string
- `rs256_public_keys` must have at least one entry
- All RS256 key values must be non-empty strings
- `version` must be non-empty string

### Key Rotation Strategies

Since automatic rotation is removed, consider these strategies:

1. **Graceful Restart**: Fetch new material and restart application
2. **Multiple Keys**: Include both old and new RS256 keys during rotation window
3. **External Rotation Manager**: Poll for changes and trigger application restart

### Performance Improvements

- No async bootstrap overhead on first request
- No background SSE subscription task
- Reduced dependency footprint (httpx removed)
- Immediate material availability after initialization

### Rationale

This refactoring:
- Simplifies the middleware by removing external dependencies
- Gives applications full control over configuration management
- Reduces attack surface (no HTTP calls from middleware)
- Improves startup clarity with synchronous validation
- Aligns with separation of concerns principle

---

## [1.0.0] - 2025-01-15

### Added

- Initial release of Vibrant Auth Middleware for FastAPI
- **Core Features**:
  - JWT authentication middleware with default-deny security posture
  - Support for HS256 (HMAC) and RS256 (RSA) token verification
  - Multi-source token extraction (cookies and Authorization headers)
  - Live configuration rotation via Server-Sent Events (SSE)
  - Comprehensive structured JSON telemetry with secret redaction
  - Request state attachment for downstream handlers

- **Security**:
  - Default-deny policy: all requests denied unless valid JWT provided
  - Automatic secret redaction from claims and logs
  - Clock skew tolerance with configurable leeway
  - Deny-on-rotation protection during material updates
  - HTTPS-only configuration service integration

- **Token Sources**:
  - Cookie-based authentication (`access_token` + `token_type` cookies)
  - Authorization header with Bearer scheme
  - Automatic correlation ID propagation from headers or generation

- **Decision Outcomes**:
  - `allow`: Valid JWT successfully verified
  - `deny`: Authentication failed (expired, missing, invalid)
  - `error`: System error during verification

- **Telemetry**:
  - Structured JSON logs with `decision`, `reason`, `correlation_id`, `principal`
  - Token source tracking (cookie vs header)
  - Signing material version tracking
  - Sanitized claims output (sensitive keys removed)

- **Configuration**:
  - `MiddlewareSettings` for flexible configuration
  - Environment variable support
  - SSE subscription for live rotation
  - HTTP client with automatic retry/backoff

- **Testing**:
  - Contract tests covering all decision scenarios
  - Unit tests for token extraction, algorithm switching, telemetry
  - Integration tests for rotation events and negative paths
  - Performance regression tests (≤5ms overhead target at 1k req/s)

- **Documentation**:
  - Comprehensive README with quickstart guide
  - Rotation drill instructions
  - Example FastAPI application
  - API reference for all public interfaces
  - Security considerations and best practices

- **Performance**:
  - Async-first design for non-blocking operations
  - Public key caching per `kid`
  - Target: ≤5ms overhead at 1000 req/s
  - Efficient SSE subscription with automatic reconnection

### Technical Details

- **Dependencies**:
  - FastAPI / Starlette for ASGI middleware
  - PyJWT for JWT verification
  - httpx for async HTTP and SSE
  - Python 3.13+ required

- **Architecture**:
  - Starlette `BaseHTTPMiddleware` for request interception
  - Async locks for thread-safe material updates
  - Event-driven rotation handling
  - Graceful degradation on configuration service unavailability

- **Compatibility**:
  - Works with any ASGI application (FastAPI, Starlette)
  - Compatible with existing FastAPI middleware chains
  - Supports both HS256 and RS256 algorithm switching

### Development

- Project scaffolding with uv package manager
- Pre-commit hooks for code quality (ruff, black)
- Comprehensive test coverage across all layers
- Type hints throughout codebase
- Async/await patterns for all I/O operations
