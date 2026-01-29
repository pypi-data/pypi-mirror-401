# Research: Remove Config Service URL and SSE Channel Dependencies

**Feature**: 002-update-the-current
**Date**: 2025-10-04

## Overview

This document captures the research findings for refactoring the middleware to accept signing material directly at initialization, removing external configuration fetching and SSE-based rotation subscription mechanisms.

## Current Implementation Analysis

### 1. Signing Material Management (`config.py`)

**Current Approach**:
- `SigningMaterial` dataclass with fields: `hs256_secret`, `rs256_public_keys`, `version`, `expires_at`
- `load_initial_material()` async function that fetches config via HTTP GET from `config_service_url`
- `subscribe_to_rotation()` async function that listens to SSE events from `sse_channel`
- Expiration checking via `is_expired()` method

**Decision**: Simplify to direct initialization
- Remove HTTP fetching logic entirely
- Remove SSE subscription logic entirely
- Remove `expires_at` field and expiration checking
- Keep core dataclass with: `hs256_secret`, `rs256_public_keys`, `version`

**Rationale**:
- Removes external dependency on httpx for config management
- Gives applications full control over where/how they load signing material
- Simplifies async initialization complexity
- Rotation can be handled externally by restarting the middleware

**Alternatives Considered**:
- Keep expiration field but make it optional → Rejected: Adds complexity with no clear use case when rotation requires restart
- Support both URL-based and direct initialization → Rejected: Violates clarification decision for breaking change

### 2. Middleware Initialization (`middleware.py`)

**Current Approach**:
- `MiddlewareSettings` with `config_service_url` and `sse_channel` fields
- `_ensure_bootstrap()` async method that lazily fetches initial material
- `_listen_for_rotations()` background task for SSE subscription
- `_handle_rotation_event()` for atomic material updates
- Complex locking: `_bootstrap_lock`, `_refresh_lock`, `_rotation_pending` event

**Decision**: Synchronous validation at initialization
- Accept `SigningMaterial` directly in `MiddlewareSettings` or as constructor param
- Validate material synchronously in `__init__()`
- Remove all bootstrap/rotation async logic
- Remove all locking mechanisms related to material rotation
- Fail immediately with clear error if material is invalid

**Rationale**:
- Fail-fast principle: errors caught at startup, not during first request
- Eliminates race conditions and complex locking
- Simpler mental model: material is immutable after initialization
- Performance: no async overhead on first request

**Alternatives Considered**:
- Keep async validation → Rejected: No benefit when material is provided directly
- Allow runtime material updates via method call → Rejected: Clarification decision requires restart

### 3. Validation Rules

**Decision**: Strict validation requirements
- MUST have non-empty `hs256_secret` (string)
- MUST have at least one entry in `rs256_public_keys` (dict with ≥1 key-value pair)
- MUST have non-empty `version` (string)
- All fields are required (no optional/nullable)

**Rationale**:
- Matches clarification requirement for both HS256 AND RS256 support
- Version tracking is critical for debugging multi-instance deployments
- Fail-fast prevents runtime errors during token verification

**Implementation Approach**:
```python
def _validate_signing_material(material: SigningMaterial) -> None:
    """Validate signing material at initialization. Raises ValueError if invalid."""
    if not material.hs256_secret:
        raise ValueError("Signing material must include hs256_secret")
    if not material.rs256_public_keys:
        raise ValueError("Signing material must include at least one RS256 public key")
    if not material.version:
        raise ValueError("Signing material must include version identifier")
```

### 4. Dependency Changes

**Current Dependencies**:
- `httpx[sse]>=0.27,<0.28` - Used for config fetching and SSE subscription

**Decision**: Remove httpx dependency
- No longer needed after removing `load_initial_material()` and `subscribe_to_rotation()`
- Remove from `pyproject.toml` dependencies

**Rationale**:
- Reduces attack surface (fewer external network calls)
- Smaller dependency footprint
- Faster installation

**Migration Note**: Applications that were relying on the middleware to fetch config will need to:
1. Fetch signing material themselves (using httpx or other HTTP client)
2. Parse the response into `SigningMaterial` dataclass
3. Pass it to middleware initialization

### 5. Breaking Change Migration Path

**Decision**: Clear error messages for old patterns

When users attempt to use old initialization patterns, provide actionable errors:
- If `config_service_url` is set → Error: "config_service_url is no longer supported. Pass signing material directly via signing_material parameter."
- If `sse_channel` is set → Error: "sse_channel is no longer supported. Handle key rotation externally and restart the middleware."

**Rationale**:
- Makes migration path obvious
- Prevents silent failures or confusing behavior

## Technical Decisions Summary

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Material Source | Direct initialization param | Full application control, no external calls |
| Expiration Support | Removed entirely | No use case when rotation requires restart |
| Validation Timing | Synchronous at `__init__` | Fail-fast, simpler error handling |
| Required Fields | hs256_secret + rs256_public_keys + version | Both algorithms required per clarification |
| Runtime Updates | Not supported | Requires middleware restart per clarification |
| Backward Compatibility | None (breaking change) | Clean break per clarification |
| httpx Dependency | Removed | No longer needed |

## Testing Strategy

### Contract Tests
- Test new initialization signature accepts `SigningMaterial`
- Test validation errors for missing/invalid material
- Test that old patterns (config_service_url) are rejected

### Integration Tests
- Delete `test_rotation_events.py` (no longer applicable)
- Update `test_negative_paths.py` with new validation scenarios
- Verify middleware works with directly-provided material

### Unit Tests
- Test `SigningMaterial` validation logic
- Test error messages for migration guidance
- Existing algorithm/extraction tests should work unchanged

## Risk Assessment

**Low Risk**:
- Well-defined breaking change with clear migration path
- Simplification (removing code) rather than adding complexity
- All requirements clarified via /clarify session

**Medium Risk**:
- Applications must update their initialization code
- Applications must implement their own config fetching/rotation logic

**Mitigation**:
- Comprehensive documentation in quickstart.md
- Clear error messages for migration
- Example code showing new initialization pattern

## Open Questions

**None** - All clarifications resolved:
- ✓ Runtime updates: Not supported (requires restart)
- ✓ Missing material: Fail immediately at init
- ✓ Backward compatibility: None (breaking change)
- ✓ Validation rules: Both HS256 and RS256 required
- ✓ Expiration: Not supported (removed)

---
*Research complete - ready for Phase 1 design*
