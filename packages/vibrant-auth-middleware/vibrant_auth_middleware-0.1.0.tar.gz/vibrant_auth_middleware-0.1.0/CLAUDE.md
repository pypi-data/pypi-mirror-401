# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Vibrant Auth Middleware** is a production-ready FastAPI middleware for JWT authentication with default-deny security posture. The middleware validates JWT tokens (HS256/RS256) and attaches authentication decisions to requests.

## Commands

### Development & Testing
```bash
# Install dependencies (using uv)
uv sync

# Run all tests
uv run pytest

# Run specific test suites
uv run pytest tests/unit/               # Unit tests for individual components
uv run pytest tests/contract/           # Contract validation tests
uv run pytest tests/integration/        # Integration tests
uv run pytest tests/performance/        # Performance benchmarks (<1ms target)

# Run a single test file
uv run pytest tests/contract/test_middleware_contract.py -v

# Run tests matching a pattern
uv run pytest -k "test_missing_signing_material"

# Linting and formatting
ruff check .                            # Check for linting issues
ruff format .                           # Format code
black src/ tests/                      # Alternative formatter
```

### Development Workflow
```bash
# Watch tests during development
uv run pytest --watch

# Run with coverage
uv run pytest --cov=src/vibrant_auth_middleware --cov-report=term-missing

# Install in editable mode for local development
uv pip install -e .
```

## Architecture

### Core Flow
1. **Middleware Initialization** (`middleware.py:43-68`): Synchronously validates and stores signing material at startup
2. **Request Interception** (`middleware.py:70-85`): Processes each request through the authentication pipeline
3. **Token Extraction** (`token_source.py`): Attempts extraction from cookies first, then Authorization header
4. **JWT Verification** (`middleware.py:87-155`): Validates token using appropriate algorithm (HS256/RS256)
5. **Decision Attachment** (`middleware.py:157-174`): Attaches `AuthDecision` to `request.state`
6. **Telemetry Emission** (`telemetry.py`): Logs structured JSON with secret redaction

### Key Components

**SigningMaterial** (`config.py:10-30`)
- Immutable dataclass holding cryptographic material
- Validated at initialization: HS256 secret, RS256 public keys, version all required
- No expiration tracking (removed in v2.0)

**AuthDecision** (`decisions.py:15-35`)
- Tri-state decision model: `allow`, `deny`, `error`
- Includes reason codes for detailed failure diagnostics
- Sanitizes claims to redact sensitive fields

**TokenSource** (`token_source.py:20-90`)
- Cookie extraction: Requires both `access_token` and `token_type` cookies
- Header extraction: Expects `Bearer <token>` format
- Returns `TokenOrigin` enum for telemetry

### Version 2.0 Breaking Changes

The middleware was refactored to remove external dependencies:
- **Removed**: Async config fetching from URLs
- **Removed**: SSE-based key rotation subscriptions
- **Removed**: httpx dependency
- **Added**: Direct signing material injection at initialization
- **Impact**: Applications now control configuration lifecycle

## Testing Strategy

### Test Organization
- `tests/unit/`: Component isolation tests
- `tests/contract/`: API contract validation
- `tests/integration/`: End-to-end flows with negative paths
- `tests/performance/`: Latency benchmarks

### Key Test Patterns
```python
# Create test signing material
material = SigningMaterial(
    hs256_secret="test-secret-32-chars-minimum",
    rs256_public_keys={"key-1": "-----BEGIN PUBLIC KEY-----\\n..."},
    version="test-1.0"
)

# Test middleware initialization failures
with pytest.raises(ValueError, match="hs256_secret must be"):
    SigningMaterial(hs256_secret="", ...)
```

## Current Feature Work

### Feature 002: Config Service Removal (Active)
**Branch**: `002-update-the-current`
**Status**: Implementation ready

Key tasks:
1. Remove async config loading from `config.py`
2. Refactor `middleware.py` initialization to be synchronous
3. Update contract tests for new validation rules
4. Delete obsolete SSE rotation tests

See `specs/002-update-the-current/` for detailed design docs.

## Performance Targets

- Middleware overhead: <1ms per request
- Token verification: <0.5ms for HS256, <1ms for RS256
- No async initialization delays
- Immediate readiness on startup

## Security Considerations

- Default-deny posture: All requests blocked without valid JWT
- Secret redaction in telemetry (fields containing: token, secret, password, key)
- Clock skew tolerance: 30 seconds default
- Immutable signing material after initialization