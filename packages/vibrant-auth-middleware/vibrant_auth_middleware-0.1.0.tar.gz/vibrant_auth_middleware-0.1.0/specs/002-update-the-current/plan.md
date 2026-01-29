# Implementation Plan: Remove Config Service URL and SSE Channel Dependencies

**Branch**: `002-update-the-current` | **Date**: 2025-10-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-update-the-current/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path ✓
2. Fill Technical Context ✓
3. Fill the Constitution Check section ✓
4. Evaluate Constitution Check section ✓
5. Execute Phase 0 → research.md ✓
6. Execute Phase 1 → contracts, data-model.md, quickstart.md, CLAUDE.md ✓
7. Re-evaluate Constitution Check section ✓
8. Plan Phase 2 → Describe task generation approach ✓
9. STOP - Ready for /tasks command ✓
```

**IMPORTANT**: The /plan command STOPS at step 9. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

This feature removes external configuration dependencies from the authentication middleware by:
1. Eliminating `config_service_url` - signing material will be provided directly during initialization
2. Removing `sse_channel` and all SSE-based rotation subscription mechanisms
3. Removing signing material expiration logic
4. Implementing strict validation: signing material must contain HS256 secret, RS256 public keys, and version
5. Enforcing fail-fast initialization when signing material is missing or invalid

This is a breaking change that simplifies the middleware's dependency model and gives applications full control over configuration management and key rotation strategies.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: FastAPI >=0.111, PyJWT[crypto] >=2.9 (httpx will be removed)
**Storage**: N/A (in-memory signing material only)
**Testing**: pytest >=8.4.2, pytest-asyncio >=1.2.0
**Target Platform**: Linux/macOS server (ASGI middleware)
**Project Type**: single - Python library/middleware
**Performance Goals**: <1ms middleware overhead per request (unchanged)
**Constraints**: Breaking change - no backward compatibility, fail-fast initialization
**Scale/Scope**: Single middleware module, ~6 source files, ~8 test files

## Constitution Check
*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Status**: Constitution is template-only - proceeding with general Python best practices

**General Principles Applied**:
- [x] Test-first development: Write tests before implementation
- [x] Breaking changes properly documented
- [x] Validation at initialization (fail-fast)
- [x] Simplification: Remove unused features (SSE, expiration, HTTP fetching)
- [x] Clear error messages for migration path

## Project Structure

### Documentation (this feature)
```
specs/002-update-the-current/
├── plan.md              # This file (/plan command output)
├── research.md          # Phase 0 output (/plan command)
├── data-model.md        # Phase 1 output (/plan command)
├── quickstart.md        # Phase 1 output (/plan command)
├── contracts/           # Phase 1 output (/plan command)
└── tasks.md             # Phase 2 output (/tasks command - NOT created by /plan)
```

### Source Code (repository root)
```
src/vibrant_auth_middleware/
├── __init__.py          # Public exports
├── config.py            # REFACTOR: Remove load_initial_material, subscribe_to_rotation
├── middleware.py        # REFACTOR: Accept signing material directly, remove bootstrap
├── decisions.py         # UNCHANGED: Token verification logic
├── token_source.py      # UNCHANGED: Token extraction
└── telemetry.py         # UNCHANGED: Logging

tests/
├── contract/
│   └── test_middleware_contract.py  # UPDATE: New initialization contract tests
├── integration/
│   ├── test_rotation_events.py      # DELETE: No longer relevant
│   └── test_negative_paths.py       # UPDATE: New validation failure tests
├── unit/
│   ├── test_algorithm_switch.py     # UNCHANGED
│   ├── test_cookie_extraction.py    # UNCHANGED
│   ├── test_header_extraction.py    # UNCHANGED
│   └── test_telemetry.py            # UNCHANGED
└── performance/
    └── test_middleware_latency.py   # UNCHANGED
```

**Structure Decision**: Single project structure maintained. This is a refactoring of existing middleware, preserving the `src/vibrant_auth_middleware/` module structure. Primary changes focus on `config.py` and `middleware.py`.

## Phase 0: Outline & Research

**Research completed - no unknowns in Technical Context**

Key technical decisions already clear from codebase analysis:
- Existing `SigningMaterial` dataclass in `config.py` - will simplify (remove expiration)
- Existing `MiddlewareSettings` in `middleware.py` - will refactor (remove URLs, add material param)
- Current async initialization in `_ensure_bootstrap()` - will replace with sync validation
- Current rotation task in `_listen_for_rotations()` - will remove entirely

**Output**: research.md

## Phase 1: Design & Contracts

### Data Model Changes
See `data-model.md` for:
- Simplified `SigningMaterial` (no expiration field)
- Updated `MiddlewareSettings` (signing_material param instead of URLs)
- Validation requirements for initialization

### API Contracts
See `contracts/` for:
- Middleware initialization contract (constructor signature)
- Error contracts (validation failure messages)
- Breaking change migration guide

### Tests Generated
- Contract tests for new initialization pattern
- Validation tests for missing/invalid signing material
- Migration tests ensuring old patterns fail with clear errors

### Agent Context
Updated `CLAUDE.md` with:
- Current refactoring approach
- Breaking changes summary
- Validation rules

**Output**: data-model.md, /contracts/*, failing tests, quickstart.md, CLAUDE.md

## Phase 2: Task Planning Approach
*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:
- Load `.specify/templates/tasks-template.md` as base
- Generate tasks in strict TDD order:
  1. Write failing contract tests for new initialization
  2. Write failing validation tests
  3. Update `SigningMaterial` dataclass (remove expiration)
  4. Update `MiddlewareSettings` (add material param, remove URLs)
  5. Refactor middleware initialization (remove bootstrap, add validation)
  6. Remove `load_initial_material()` function
  7. Remove `subscribe_to_rotation()` function
  8. Remove rotation background task
  9. Delete rotation integration tests
  10. Update existing tests to use new initialization
  11. Update documentation and examples

**Ordering Strategy**:
- Tests first (TDD)
- Data model changes before behavior changes
- Deletions after new code is working
- Documentation updates last

**Estimated Output**: 15-20 ordered tasks in tasks.md

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation
*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)
**Phase 4**: Implementation (execute tasks.md following constitutional principles)
**Phase 5**: Validation (run tests, execute quickstart.md, performance validation)

## Complexity Tracking

**No constitutional violations** - this is a simplification refactoring that:
- Removes external dependencies (httpx for config fetching/SSE)
- Removes async complexity (no background tasks)
- Removes expiration logic
- Improves initialization clarity (fail-fast validation)

## Progress Tracking
*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [x] Phase 3: Tasks generated (/tasks command) - 33 tasks in 6 phases
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (simplification, no violations)
- [x] Post-Design Constitution Check: PASS
- [x] All NEEDS CLARIFICATION resolved (via /clarify)
- [x] Complexity deviations documented (none - this is simplification)

---
*Based on general Python best practices - constitution template not yet customized*
