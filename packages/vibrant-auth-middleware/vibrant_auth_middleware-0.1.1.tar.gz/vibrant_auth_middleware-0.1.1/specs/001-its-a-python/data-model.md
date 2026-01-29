# Data Model: FastAPI JWT Access Middleware

## Entities

### TokenSource
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| origin | Enum[`cookie`, `authorization_header`] | Where the JWT was obtained. | Drives telemetry token_source field. |
| token | str | Raw JWT extracted from request. | Stored only in-memory during verification. |
| token_type | str | Value of `token_type` cookie or header prefix. | MUST match expected `Bearer` when header-derived. |
| correlation_id | str | Unique request identifier propagated from headers or generated. | Used for traceability. |

### SigningMaterial
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| hs256_secret | Optional[str] | Current symmetric key for HS256 verification. | Retrieved from configuration service payload. |
| rs256_public_keys | Dict[str, str] | Map of key IDs to PEM-encoded RSA public keys. | Cache for rapid lookup. |
| version | str | Monotonic version identifier from configuration service. | Drives deny-until-refresh rule. |
| expires_at | datetime | Expiration timestamp for the current material. | Middleware denies requests when expired. |

### AuthDecision
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| status | Enum[`allow`, `deny`, `error`] | Final outcome of verification. | Required by Constitution Principle I. |
| reason | str | Machine-readable reason code. | Used in telemetry and error responses. |
| principal | Optional[str] | Subject or user identifier from JWT claims. | Populated only on allow. |
| claims | Dict[str, Any] | Sanitized claims shared downstream. | Secrets (e.g., tokens) removed. |

### MiddlewareSettings
| Field | Type | Description | Notes |
|-------|------|-------------|-------|
| config_service_url | str | HTTPS endpoint for initial signing material fetch. | Provided by platform ops. |
| sse_channel | str | Path or topic for rotation pushes. | Used to subscribe for updates. |
| clock_skew_leeway | int | Allowed leeway in seconds for exp/nbf claims. | Defaults to 30s, configurable per service. |
| deny_on_missing_material | bool | If true, deny when materials unavailable. | MUST remain true per constitution. |

## Relationships and Lifecycle
- `MiddlewareSettings` determines how the middleware retrieves and refreshes `SigningMaterial` on startup and during runtime.
- `SigningMaterial` updates trigger invalidation of any cached verifiers and deny requests until the new version is loaded.
- Each request instantiates a `TokenSource`, which feeds verification logic to produce an `AuthDecision`.
- `AuthDecision` and sanitized claims are attached to the FastAPI `Request.state` for downstream handlers.

## Identity & Uniqueness Rules
- `SigningMaterial.version` MUST increase monotonically; duplicate or regressive versions trigger deny events logged as configuration errors.
- `TokenSource.correlation_id` MUST be unique per request (fallback to UUID4 when header missing).

## State Transitions
1. **Uninitialized → Bootstrapping**: Middleware starts, fetches `SigningMaterial`.
2. **Bootstrapping → Active**: Valid materials loaded; requests allowed if tokens verify.
3. **Active → Refreshing**: SSE event indicates rotation; middleware temporarily denies until new version fetched.
4. **Refreshing → Active**: New materials applied successfully.
5. **Active → Degraded**: Configuration service unreachable beyond timeout; middleware remains default-deny and emits alerts.

## Scale Considerations
- Cache compiled verifiers per `kid` to reduce RSA verification cost under high load.
- Maintain asynchronous lock to prevent thundering herds on rotation events.
