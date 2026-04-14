---

description: "Task list template for feature implementation"
---

# Tasks: [FEATURE NAME]

**Input**: Design documents from `/specs/[###-feature-name]/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Add any extra tests requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend app**: `backend/app/` for application code, `backend/tests/` for backend tests, `backend/alembic/` for migrations
- **Backend modules**: `backend/app/modules/<feature>/router.py`, `schemas.py`, `services/`, `repositories/`, `models.py`, `dependencies.py`
- **Backend infrastructure**: `backend/app/core/`, `backend/app/shared/`, `backend/app/settings/`, `backend/app/workers/`, `backend/app/api/`
- **Frontend app**: `frontend/app/` for routes and layouts, `frontend/features/` for feature logic, `frontend/components/` for shared UI, `frontend/lib/` for API utilities
- **DevOps/docs**: `docker/`, `docker-compose.yml`, `.env.example`, `docs/`
- Paths shown below are samples; generated tasks MUST use the exact paths from plan.md.

<!-- 
  ============================================================================
  IMPORTANT: The tasks below are SAMPLE TASKS for illustration purposes only.
  
  The /speckit.tasks command MUST replace these with actual tasks based on:
  - User stories from spec.md (with their priorities P1, P2, P3...)
  - Feature requirements from plan.md
  - Entities from data-model.md
  - Endpoints from contracts/
  
  Tasks MUST be organized by user story so each story can be:
  - Implemented independently
  - Tested independently
  - Delivered as an MVP increment
  
  DO NOT keep these sample tasks in the generated tasks.md file.
  ============================================================================
-->

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize [language] project with [framework] dependencies
- [ ] T003 [P] Configure linting and formatting tools

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [ ] T004 Setup database schema and migrations framework
- [ ] T005 [P] Implement authentication/authorization framework
- [ ] T006 [P] Setup API routing in `backend/app/api/router.py`
- [ ] T007 Create shared base models/entities in `backend/app/shared/` or the owning module
- [ ] T008 Configure error handling and logging infrastructure in `backend/app/core/`
- [ ] T009 Setup domain settings in `backend/app/settings/` and compose them in `backend/app/core/config.py`
- [ ] T010 Setup database engine/session/Base in `backend/app/core/database.py`
- [ ] T011 Define standard API success/error response schemas and exception mapping in `backend/app/core/`
- [ ] T012 Define shared pagination schemas/helpers for `page` and `limit` or `cursor` pagination
- [ ] T013 Add request-id structured logging middleware in `backend/app/core/`
- [ ] T014 Add audit-trail foundation for imports, AI runs, and admin actions
- [ ] T015 Add rate limiting and auth scope/permission foundations for protected routes

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - [Title] (Priority: P1) 🎯 MVP

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 1

> **NOTE: Write service unit tests and API integration tests FIRST, ensure they FAIL before implementation**

- [ ] T016 [P] [US1] Unit test for [service behavior] in `backend/tests/unit/test_[name].py`
- [ ] T017 [P] [US1] Integration test for [endpoint] success envelope in `backend/tests/integration/test_[name].py`
- [ ] T018 [P] [US1] Integration test for unified error response and HTTP status mapping in `backend/tests/integration/test_[name]_errors.py`
- [ ] T019 [P] [US1] Integration test for pagination or audit-trail behavior if this story lists records or triggers audited actions

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create [Entity1] model in `backend/app/modules/<feature>/models.py`
- [ ] T021 [P] [US1] Create request/response schemas in `backend/app/modules/<feature>/schemas.py`
- [ ] T022 [US1] Implement custom exceptions in `backend/app/modules/<feature>/exceptions.py`
- [ ] T023 [US1] Implement repository in `backend/app/modules/<feature>/repositories/[name]_repository.py`
- [ ] T024 [US1] Implement service in `backend/app/modules/<feature>/services/[name]_service.py`
- [ ] T025 [US1] Wire dependencies in `backend/app/modules/<feature>/dependencies.py`
- [ ] T026 [US1] Implement versioned endpoint with standard success/error envelopes in `backend/app/modules/<feature>/router.py`
- [ ] T027 [US1] Register module router under `/api/v1/` in `backend/app/api/router.py`
- [ ] T028 [US1] Add pagination behavior for list endpoints if required by this story
- [ ] T029 [US1] Add audit-trail writes for imports, AI runs, or admin actions if required by this story
- [ ] T030 [US1] Add validation, error handling, request-id logging, auth scopes, and rate-limit behavior in the owning backend module
- [ ] T031 [US1] Add idempotency or soft delete behavior if required by this story

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - [Title] (Priority: P2)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 2

- [ ] T032 [P] [US2] Unit test for [service behavior] in `backend/tests/unit/test_[name].py`
- [ ] T033 [P] [US2] Integration test for [endpoint] success envelope in `backend/tests/integration/test_[name].py`
- [ ] T034 [P] [US2] Integration test for pagination, audit trail, auth, rate-limit, error, idempotency, or soft delete behavior as applicable

### Implementation for User Story 2

- [ ] T035 [P] [US2] Create or update feature model in `backend/app/modules/<feature>/models.py`
- [ ] T036 [US2] Implement repository logic in `backend/app/modules/<feature>/repositories/`
- [ ] T037 [US2] Implement service logic in `backend/app/modules/<feature>/services/`
- [ ] T038 [US2] Implement versioned endpoint with standard success/error envelopes in `backend/app/modules/<feature>/router.py`
- [ ] T039 [US2] Add pagination or audit-trail behavior if required by this story
- [ ] T040 [US2] Add frontend route or feature UI under `frontend/app/` and `frontend/features/<feature>/` if this story has UI scope
- [ ] T041 [US2] Integrate with User Story 1 components only through documented service/API boundaries

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - [Title] (Priority: P3)

**Goal**: [Brief description of what this story delivers]

**Independent Test**: [How to verify this story works on its own]

### Tests for User Story 3

- [ ] T042 [P] [US3] Unit test for [service behavior] in `backend/tests/unit/test_[name].py`
- [ ] T043 [P] [US3] Integration test for [endpoint] success envelope in `backend/tests/integration/test_[name].py`
- [ ] T044 [P] [US3] Integration test for pagination, audit trail, auth, rate-limit, error, idempotency, or soft delete behavior as applicable

### Implementation for User Story 3

- [ ] T045 [P] [US3] Create or update feature schemas in `backend/app/modules/<feature>/schemas.py`
- [ ] T046 [US3] Implement repository logic in `backend/app/modules/<feature>/repositories/`
- [ ] T047 [US3] Implement service logic in `backend/app/modules/<feature>/services/`
- [ ] T048 [US3] Implement versioned endpoint with standard success/error envelopes in `backend/app/modules/<feature>/router.py`
- [ ] T049 [US3] Add pagination or audit-trail behavior if required by this story
- [ ] T050 [US3] Add frontend feature code under `frontend/features/<feature>/` if this story has UI scope

**Checkpoint**: All user stories should now be independently functional

---

[Add more user story phases as needed, following the same pattern]

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] TXXX [P] Documentation updates in docs/
- [ ] TXXX Code cleanup and refactoring
- [ ] TXXX Performance optimization across all stories
- [ ] TXXX [P] Additional unit tests in `backend/tests/unit/`
- [ ] TXXX [P] Additional API integration tests in `backend/tests/integration/`
- [ ] TXXX Verify all API routes are versioned under `/api/v1/` or later
- [ ] TXXX Verify handled JSON responses use the standard success/error envelopes
- [ ] TXXX Verify list endpoints use consistent `page` and `limit` or `cursor` pagination
- [ ] TXXX Verify structured logs include `request_id` and audit fields for imports or AI runs
- [ ] TXXX Verify imports, AI runs, and admin actions write audit records with actor, timestamp, requested or changed data, resulting status, and failure details
- [ ] TXXX Verify idempotency and soft delete behavior for applicable features
- [ ] TXXX Security hardening
- [ ] TXXX Run quickstart.md validation

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Required service unit tests and API integration tests MUST be written and FAIL before implementation
- Models and schemas before repositories and services
- Repositories before services
- Services before endpoints
- Dependencies before router wiring
- Exception/status mappings before endpoint error handling
- Pagination contract before list endpoint implementation
- Audit-trail schema before import, AI-run, or admin-action implementation
- Idempotency and soft delete rules before worker or destructive flows
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch required tests for User Story 1 together:
Task: "Unit test for [service behavior] in backend/tests/unit/test_[name].py"
Task: "Integration test for [endpoint] success envelope in backend/tests/integration/test_[name].py"
Task: "Integration test for unified error response and status mapping in backend/tests/integration/test_[name]_errors.py"
Task: "Integration test for pagination or audit trail in backend/tests/integration/test_[name]_audit_or_pagination.py"

# Launch all models for User Story 1 together:
Task: "Create [Entity1] model in backend/app/modules/<feature>/models.py"
Task: "Create [Entity1] schemas in backend/app/modules/<feature>/schemas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify required service unit tests and API integration tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
