# Feature Specification: FastAPI JWT Access Middleware

**Feature Branch**: `001-its-a-python`  
**Created**: 2025-10-04  
**Status**: Draft  
**Input**: User description: "Its a Python FastAPI compatible middleware library to be shared for the whole organization. It needs to do two things, first, get access_token from cookies if there anything and use it as the jwt token, remember, it doesnt have Bearer, the token_type is defined in a separate field, if no access_token present, check Authorization header for jwt token, but now it should come with Bearer prefix before the actual token. Second, it needs to check jwt token alg for HS256 or RS256 and decode and verify accodingly with secret or public key respectively."

## Execution Flow (main)
```
1. Organization onboarding teams enable the middleware on their FastAPI apps.
2. Incoming requests first evaluate cookies for an `access_token` plus `token_type` pair.
3. If no cookie token is found, the middleware inspects the `Authorization` header for
   a `Bearer` JWT.
4. Middleware validates the JWT algorithm (HS256 or RS256) and verifies the signature
   with the corresponding secret or public key source.
5. Middleware attaches verified identity context to the request and records the
   authentication decision for downstream services.
```

---

## ⚡ Quick Guidelines
- Ensure every inbound request is evaluated by the middleware before any application logic.
- Capture structured audit telemetry for every allow, deny, or error outcome with correlation IDs.
- Maintain a default-deny posture whenever signing keys, secrets, or tokens are missing.
- Document how shared teams load secrets from managed stores and coordinate key rotation.

## Clarifications
### Session 2025-10-04
- Q: How will teams supply and rotate the HS256 secret and RS256 public key used by the middleware? → A: Middleware fetches both secret and public keys from a dedicated configuration service on each start-up, which pushes updates when keys rotate.

## User Scenarios & Testing *(mandatory)*

### Primary User Story
An internal FastAPI service owner enables the shared middleware so that every request is
authenticated automatically, regardless of whether partner teams send JWTs via cookies or
Authorization headers.

### Acceptance Scenarios
1. **Given** a request containing `access_token` and `token_type` cookies with a valid HS256
   JWT, **When** the request reaches the middleware, **Then** the middleware validates the
   token using the shared secret and marks the request as authenticated.
2. **Given** a request without cookies but with an `Authorization: Bearer <jwt>` header using
   RS256, **When** the middleware processes it, **Then** it verifies the signature with the
   configured public key and exposes the decoded claims to downstream handlers.

### Edge Cases
- How does the middleware respond when cookies are present but `token_type` does not match
  the encoded token?
- What happens when neither cookies nor Authorization header provide a JWT?
- How are expired or tampered JWTs surfaced to clients and logged for compliance review?
- Middleware treats key rotation events from the configuration service as deny-until-refresh,
  ensuring stale materials never authenticate requests.

## Requirements *(mandatory)*

### Functional Requirements
- **FR-001**: Middleware MUST prioritize extracting a JWT from `access_token` and
  `token_type` cookies when present.
- **FR-002**: Middleware MUST fall back to parsing the `Authorization` header for a
  `Bearer` JWT when cookies do not provide a token.
- **FR-003**: Middleware MUST reject tokens lacking an accompanying `token_type` field or
  using an unsupported algorithm.
- **FR-004**: Middleware MUST validate HS256 tokens with the shared secret and RS256 tokens
  with the configured public key, surfacing a deny decision if validation fails.
- **FR-005**: Middleware MUST capture each authentication decision (allow, deny, error) with
  correlation ID, token origin (cookie vs header), and reason code in the observability
  pipeline.
- **FR-006**: Middleware configuration MUST default to deny when signing materials,
  supported algorithm settings, or required environment configuration are missing.
- **FR-007**: Middleware MUST expose decoded claims to downstream services only after
  successful verification and MUST redact sensitive fields from logs and telemetry.
- **FR-008**: Middleware MUST retrieve the HS256 secret and RS256 public key bundle from the
  dedicated configuration service at start-up and accept rotation pushes; failure to
  obtain current materials MUST produce a deny decision.

### Key Entities *(include if feature involves data)*
- **JWT Token Context**: Represents the decoded JWT claims, algorithm, token source, and
  verification timestamp shared with downstream handlers.
- **Signing Material Configuration**: Describes secret keys for HS256 and public key bundle
  for RS256, including rotation metadata and retrieval location references.

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
- [x] Requirements are testable and unambiguous  
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [ ] Review checklist passed

---
