# Feature Specification: Remove Config Service URL and SSE Channel Dependencies

**Feature Branch**: `002-update-the-current`
**Created**: 2025-10-04
**Status**: Draft
**Input**: User description: "Update the current features: 1. Remove config_service_url and related features, I want to separate it out from this middleware, but rather as an input when init this middleware. 2. Remove sse_channel related feature, for example subscribe_to_rotation and etc."

## Execution Flow (main)
```
1. Parse user description from Input
   → Identify: refactoring of configuration and subscription mechanisms
2. Extract key concepts from description
   → Actors: Application developers initializing the middleware
   → Actions: Provide signing material directly, remove automatic rotation subscription
   → Data: Signing material (secrets/keys) provided at initialization
   → Constraints: Must maintain security, cannot fetch config automatically
3. For each unclear aspect:
   → [RESOLVED: Rotation requires middleware restart/reinitialization]
   → [RESOLVED: Middleware accepts static signing material at initialization]
4. Fill User Scenarios & Testing section
   → User flow: Initialize middleware with signing material directly
5. Generate Functional Requirements
   → Each requirement must be testable
6. Identify Key Entities (if data involved)
7. Run Review Checklist
   → WARN "Spec has uncertainties about rotation mechanism"
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

---

## Clarifications

### Session 2025-10-04
- Q: How should the middleware provide a mechanism for updating signing material at runtime? → A: Require application to restart/reinitialize the middleware to change signing material (no runtime updates)
- Q: What should happen when the middleware is initialized without signing material? → A: Fail immediately with an error (raise exception/return error during initialization)
- Q: Should this refactoring maintain backward compatibility with existing initialization patterns? → A: No - immediate breaking change, remove old patterns entirely (users must update their code)
- Q: What validation rules determine if signing material is "invalid or malformed"? → A: Must have both HS256 secret AND at least one RS256 public key plus valid version field
- Q: What should happen when the signing material's expiration timestamp is reached (if provided)? → A: No expiration for signing material (remove expiration feature)

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As an application developer, I want to initialize the authentication middleware with signing material directly (rather than providing a URL to fetch it from) so that I have full control over where and how the configuration is loaded. I also want to remove the automatic SSE-based rotation subscription feature so that rotation can be handled separately by my application.

### Acceptance Scenarios
1. **Given** I am initializing the middleware, **When** I provide signing material directly as an initialization parameter, **Then** the middleware MUST use that material for token verification without making any external HTTP calls
2. **Given** I am initializing the middleware, **When** I do not provide signing material or provide invalid signing material, **Then** the initialization MUST fail immediately with an error
3. **Given** the middleware is running, **When** I do not provide an SSE channel URL, **Then** the middleware MUST NOT attempt to subscribe to any rotation events
4. **Given** I am upgrading from a previous version that used config_service_url, **When** I attempt to use the old initialization pattern, **Then** the system MUST fail with a clear error indicating the breaking change
5. **Given** I want to update signing material, **When** I restart or reinitialize the middleware with new signing material, **Then** the middleware MUST use the updated material for all subsequent token verifications

### Edge Cases
- Middleware initialization MUST fail immediately (raise error) when signing material is not provided
- Middleware initialization MUST fail immediately (raise error) when signing material is missing HS256 secret
- Middleware initialization MUST fail immediately (raise error) when signing material has no RS256 public keys
- Middleware initialization MUST fail immediately (raise error) when signing material is missing version field

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: System MUST remove the `config_service_url` field from middleware settings
- **FR-002**: System MUST remove the `sse_channel` field from middleware settings
- **FR-003**: System MUST accept signing material as a direct input parameter during middleware initialization
- **FR-004**: System MUST remove the automatic HTTP fetching of signing material from a configuration service
- **FR-005**: System MUST remove the SSE subscription mechanism for rotation events (including the `subscribe_to_rotation` function)
- **FR-006**: System MUST remove the background task that listens for rotation events
- **FR-007**: System MUST continue to verify JWT tokens using the signing material provided at initialization
- **FR-008**: System MUST NOT make any automatic external HTTP calls to fetch or refresh signing material
- **FR-009**: System MUST NOT provide runtime signing material updates (material changes require middleware restart/reinitialization)
- **FR-010**: System MUST fail immediately (raise error) during initialization when signing material is not provided
- **FR-011**: System MUST fail immediately (raise error) during initialization when signing material is invalid or malformed (missing HS256 secret, missing RS256 public keys, or missing version field)
- **FR-012**: System MUST validate that signing material contains both an HS256 secret AND at least one RS256 public key AND a valid version field
- **FR-013**: System MUST NOT support expiration timestamps for signing material (remove expiration checking logic)
- **FR-014**: System MUST NOT maintain backward compatibility with old initialization patterns (config_service_url and sse_channel are completely removed)

### Key Entities *(include if feature involves data)*
- **Signing Material**: Represents the cryptographic keys and secrets used to verify JWT tokens. Previously fetched from a remote service, now provided directly by the application. Must contain: (1) HS256 secret (required), (2) at least one RS256 public key (required), (3) version identifier (required). Does not support expiration timestamps.
- **Middleware Settings**: Configuration parameters for the middleware. Will no longer include config_service_url or sse_channel fields. Will include new parameter(s) for direct signing material input.

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [ ] No [NEEDS CLARIFICATION] markers remain
- [ ] Requirements are testable and unambiguous
- [ ] Success criteria are measurable
- [x] Scope is clearly bounded
- [ ] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed (has [NEEDS CLARIFICATION] markers)

---
