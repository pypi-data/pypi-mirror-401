# Tasks: FastAPI JWT Access Middleware

**Input**: Design documents from `/specs/001-its-a-python/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
   → quickstart.md: Extract scenarios → integration tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, CLI commands
   → Integration: middleware wiring, configuration service, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have model tasks?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Phase 3.1: Setup
- [X] T001 Initialize Python project tooling (`pyproject.toml`) with FastAPI, Starlette, PyJWT, httpx, pytest, pytest-asyncio dependencies (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/pyproject.toml`).
- [X] T002 Configure repo-level linting and formatting (ruff or black) and add pre-commit hooks (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/.pre-commit-config.yaml`).
- [X] T003 Set up middleware package scaffolding with module stubs (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/__init__.py`).

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
- [X] T004 [P] Author contract test covering middleware decision table (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/contract/test_middleware_contract.py`).
- [X] T005 [P] Write unit test for cookie extraction and token_type validation (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/unit/test_cookie_extraction.py`).
- [X] T006 [P] Write unit test for Authorization header parsing and Bearer enforcement (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/unit/test_header_extraction.py`).
- [X] T007 [P] Write unit test ensuring HS256/RS256 algorithm switching and deny on unsupported alg (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/unit/test_algorithm_switch.py`).
- [X] T008 [P] Create integration test simulating configuration rotation SSE event and deny-until-refresh (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/integration/test_rotation_events.py`).
- [X] T009 [P] Create integration test covering negative paths (expired token, malformed token, missing token_type) (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/integration/test_negative_paths.py`).

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [X] T010 Implement `TokenSource` extractor handling cookies and headers (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/token_source.py`).
- [X] T011 Implement `SigningMaterial` management with configuration service bootstrap and SSE subscription (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/config.py`).
- [X] T012 Implement `AuthDecision` utilities and sanitized claims handling (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/decisions.py`).
- [X] T013 Implement core middleware request flow enforcing default-deny and attaching decisions (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/middleware.py`).
- [X] T014 Implement structured telemetry helpers for decisions (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/telemetry.py`).

## Phase 3.4: Integration
- [X] T015 Wire configuration service HTTP client with retry/backoff and SSE listener (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/config.py`).
- [X] T016 Integrate middleware into FastAPI sample app and ensure first-in-chain registration (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/examples/app.py`).
- [X] T017 Emit structured logs and metrics per decision, ensuring secrets redacted (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/telemetry.py`).
- [X] T018 Provide helper to convert `AuthDecision` into HTTP response payloads (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/src/vibrant_auth_middleware/decisions.py`).

## Phase 3.5: Polish
- [X] T019 [P] Add unit tests for telemetry formatting and secret redaction (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/unit/test_telemetry.py`).
- [X] T020 [P] Add performance regression test ensuring ≤5 ms overhead at 1k req/s (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/tests/performance/test_middleware_latency.py`).
- [X] T021 [P] Update documentation (README.md and quickstart) with usage and rotation drill instructions (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/README.md`).
- [X] T022 [P] Run agent context update script for new dependencies (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/.specify/scripts/bash/update-agent-context.sh`).
- [X] T023 Perform full test suite and finalize changelog entry (`/Users/tianhaowang/Documents/GitHub/Vibrant-auth-middleware/CHANGELOG.md`).

## Dependencies
- Setup tasks T001-T003 run sequentially.
- Tests T004-T009 must be written and failing before implementing T010-T014.
- T010 depends on T005-T006; T011 on T008; T012 on T004; T013 on T004-T009; T014 on T004 and research telemetry guidelines.
- Integration tasks T015-T018 depend on core implementations T010-T014.
- Polish tasks depend on successful integration tasks and passing core tests.

## Parallel Example
```
# Parallel test authoring once setup complete
/specify/tasks T004
/specify/tasks T005
/specify/tasks T006
/specify/tasks T007

# Parallel polish efforts after integration
/specify/tasks T019
/specify/tasks T020
/specify/tasks T021
```

## Validation Checklist
- [ ] All contract scenarios have corresponding tests (T004).
- [ ] All entities have implementation tasks (T010-T012).
- [ ] All tests precede implementation tasks.
- [ ] Parallel tasks modify distinct files.
- [ ] Security posture coverage includes negative paths, rotation denies, telemetry.
- [ ] Documentation updated for adopters and tooling.
