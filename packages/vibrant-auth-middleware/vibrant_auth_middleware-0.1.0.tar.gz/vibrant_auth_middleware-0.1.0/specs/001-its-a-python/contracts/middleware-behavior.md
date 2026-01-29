# Contract: Vibrant Auth Middleware Behavior

## Overview
This contract defines observable behavior for the middleware when attached to a FastAPI application. Tests MUST exercise these cases before implementation changes merge.

## Decision Outcomes
| Scenario | Input | Expected Decision | Notes |
|----------|-------|-------------------|-------|
| Cookie HS256 success | Cookies: `access_token=<valid>`, `token_type=JWT` | `allow` | JWT verified with HS256 secret from configuration service. |
| Cookie token missing type | Cookie without `token_type` | `deny` | Reason `missing_token_type`; middleware logs decision with correlation ID. |
| Authorization RS256 success | Header `Authorization: Bearer <valid>` | `allow` | RS256 verification uses matching `kid` from cached public keys. |
| Authorization missing Bearer | Header `Authorization: <token>` | `deny` | Reason `invalid_prefix`; middleware does not attempt decode. |
| Expired token | Either source with `exp` in past | `deny` | Reason `token_expired`; telemetry includes token source. |
| Rotation pending | Configuration service emits newer version; middleware awaiting refresh | `deny` | Reason `rotation_pending`; lasts until new material applied. |
| Malformed JWT | Token fails base64 decode | `error` | Reason `malformed_token`; middleware continues to deny request. |

## Attached Request State
- `request.state.auth_decision`: instance of `AuthDecision` dataclass populated per contract.
- `request.state.auth_claims`: sanitized dict of claims (alias for compatibility).

## Telemetry Fields
Every decision MUST emit a structured log with fields:
- `decision`: one of `allow`, `deny`, `error`
- `reason`: reason code from table above
- `token_source`: `cookie` or `authorization_header`
- `correlation_id`: request identifier
- `principal`: subject claim when allowed, else null

## Error Responses
Applications MAY choose how to surface the decision. Middleware MUST provide helper utilities to convert an `AuthDecision` into a 401/403 response body:
```json
{
  "detail": "Access denied",
  "reason": "token_expired",
  "correlation_id": "..."
}
```
