# Research: FastAPI JWT Access Middleware

## JWT verification library
- **Decision**: Use [PyJWT](https://pyjwt.readthedocs.io/) for decoding and verifying HS256 and RS256 tokens.
- **Rationale**: PyJWT supports both HMAC and RSA algorithms, integrates with Python 3.13, and allows custom leeway handling for clock skew.
- **Alternatives considered**:
  - `python-jose`: wider algorithm coverage but brings heavier dependencies and slower verification in benchmarks.
  - `Authlib`: powerful but oriented toward full OAuth/OIDC servers rather than lightweight middleware.

## FastAPI middleware insertion point
- **Decision**: Implement the middleware using Starlette's `BaseHTTPMiddleware` and mount it as the first middleware in the FastAPI stack.
- **Rationale**: Guarantees every request passes through the JWT checks before reaching application routes, satisfying Authenticated Entry Only.
- **Alternatives considered**:
  - Dependency-based approach (`Depends`): would require every route to opt-in, risking bypasses.
  - Custom APIRouter subclass: more complex and still leaves room for manual bypass.

## Configuration service integration
- **Decision**: Fetch signing material from the configuration service via HTTPS on startup and subscribe to its server-sent events (SSE) channel for live rotation pushes.
- **Rationale**: Meets the clarification requirement, keeps secrets out of the repo, and allows near-real-time rotation with minimal downtime.
- **Alternatives considered**:
  - Periodic polling: simpler but risks short windows using stale keys.
  - Static environment variables: conflicts with organization-wide rotation policies.

## Telemetry and observability
- **Decision**: Emit structured JSON logs through the standard logging framework with fields: `correlation_id`, `token_source`, `decision`, `reason`, `principal`, and redact sensitive claims.
- **Rationale**: Fulfills Traceable Access Decisions while remaining agent-agnostic; easily ships to the organization's log pipeline.
- **Alternatives considered**:
  - Custom metrics-only approach: insufficient for forensic detail.
  - Verbose claim logging: rejected to avoid leaking PII/secrets.

## Performance guard rails
- **Decision**: Target ≤5 ms additional latency per request at 1,000 req/s on a single application instance by caching parsed public keys and reusing compiled regex for header parsing.
- **Rationale**: Maintains responsiveness for shared services and aligns with zero-trust guidance.
- **Alternatives considered**:
  - No explicit target: unacceptable for production adoption.
  - Aggressive caching of entire JWTs: rejected due to risk of replaying revoked tokens.
