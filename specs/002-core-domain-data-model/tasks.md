# Tasks: Core Domain & Data Model

**Input**: Design documents from `/specs/002-core-domain-data-model/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/domain-data-contract.md](./contracts/domain-data-contract.md)

**Tests**: Service changes MUST include unit tests. Repository and migration behavior MUST be validated because Phase 1 is a persistence-focused phase. No API integration tests are required unless implementation adds endpoints, which this task list avoids.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish backend package, dependency, and test foundations needed before persistence work begins.

- [X] T001 Add SQLAlchemy Async, Alembic, async PostgreSQL driver, pydantic-settings, pytest, pytest-asyncio, and any test database helper dependencies to `backend/pyproject.toml`
- [X] T002 Create backend package markers for the target app layout in `backend/app/__init__.py`, `backend/app/core/__init__.py`, `backend/app/settings/__init__.py`, and `backend/app/shared/__init__.py`
- [X] T003 [P] Create backend test package markers in `backend/tests/__init__.py`, `backend/tests/domain/__init__.py`, `backend/tests/repositories/__init__.py`, and `backend/tests/migrations/__init__.py`
- [X] T004 [P] Add Phase 1 test command documentation to `backend/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database, model, enum, and migration scaffolding that all user stories depend on.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Implement database settings in `backend/app/settings/database.py`
- [X] T006 Implement settings aggregation in `backend/app/core/config.py`
- [X] T007 Implement async engine, async session factory, declarative Base, and DB dependency in `backend/app/core/database.py`
- [X] T008 [P] Implement shared timestamp and soft-delete mixins in `backend/app/shared/models/base.py`
- [X] T009 [P] Implement shared `RunStatus` enum in `backend/app/shared/enums/run_status.py`
- [X] T010 [P] Implement shared source and normalization constants in `backend/app/shared/enums/source.py`
- [X] T011 Configure Alembic metadata imports for `backend/app/core/database.py` and planned module models in `backend/alembic/env.py`
- [X] T012 Create initial Phase 1 Alembic revision skeleton in `backend/alembic/versions/002_core_domain_data_model.py`
- [X] T013 [P] Add async database test fixtures in `backend/tests/conftest.py`
- [X] T014 [P] Add shared model import smoke test in `backend/tests/migrations/test_model_metadata.py`

**Checkpoint**: Database and test foundations are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Model Daily Tracking Records (Priority: P1) MVP

**Goal**: Represent daily logs, tasks, categories, tags, and notes with clean relationships and normalization rules.

**Independent Test**: Create a sample day with multiple tasks and verify every task has one day, one normalized category, normalized unique JSON tags, and optional note behavior without relying on import or dashboard behavior.

### Tests for User Story 1

- [X] T015 [P] [US1] Add DailyLog uniqueness and date reuse service tests in `backend/tests/domain/test_daily_logs.py`
- [X] T016 [P] [US1] Add task duration, tag normalization, and category normalization service tests in `backend/tests/domain/test_tasks.py`
- [X] T017 [P] [US1] Add empty note and one-active-note service tests in `backend/tests/domain/test_notes.py`
- [X] T018 [P] [US1] Add daily log, task, category, and note repository tests in `backend/tests/repositories/test_daily_tracking_repositories.py`
- [X] T019 [P] [US1] Add migration assertions for daily log, task, category, and note tables in `backend/tests/migrations/test_core_domain_migration.py`

### Implementation for User Story 1

- [X] T020 [P] [US1] Implement `DailyLog` ORM model in `backend/app/modules/daily_logs/models.py`
- [X] T021 [P] [US1] Implement `Category` and `Task` ORM models in `backend/app/modules/tasks/models.py`
- [X] T022 [P] [US1] Implement `Note` ORM model in `backend/app/modules/notes/models.py`
- [X] T023 [P] [US1] Implement daily log schemas in `backend/app/modules/daily_logs/schemas.py`
- [X] T024 [P] [US1] Implement task and category schemas in `backend/app/modules/tasks/schemas.py`
- [X] T025 [P] [US1] Implement note schemas in `backend/app/modules/notes/schemas.py`
- [X] T026 [P] [US1] Implement daily log domain exceptions in `backend/app/modules/daily_logs/exceptions.py`
- [X] T027 [P] [US1] Implement task domain exceptions in `backend/app/modules/tasks/exceptions.py`
- [X] T028 [P] [US1] Implement note domain exceptions in `backend/app/modules/notes/exceptions.py`
- [X] T029 [US1] Implement `DailyLogRepository` in `backend/app/modules/daily_logs/repositories/daily_log_repository.py`
- [X] T030 [US1] Implement `TaskRepository` and `CategoryRepository` in `backend/app/modules/tasks/repositories/task_repository.py`
- [X] T031 [US1] Implement `NoteRepository` in `backend/app/modules/notes/repositories/note_repository.py`
- [X] T032 [US1] Implement `DailyLogService.get_or_create_daily_log` and date-range reads in `backend/app/modules/daily_logs/services/daily_log_service.py`
- [X] T033 [US1] Implement `TaskService.create_task`, category reuse, tag normalization, and total calculations in `backend/app/modules/tasks/services/task_service.py`
- [X] T034 [US1] Implement `NoteService` empty-note handling and one-active-note rule in `backend/app/modules/notes/services/note_service.py`
- [X] T035 [US1] Wire daily log service and repository providers in `backend/app/modules/daily_logs/dependencies.py`
- [X] T036 [US1] Wire task service and repository providers in `backend/app/modules/tasks/dependencies.py`
- [X] T037 [US1] Wire note service and repository providers in `backend/app/modules/notes/dependencies.py`
- [X] T038 [US1] Add DailyLog, Category, Task, and Note table definitions, relationships, indexes, and constraints to `backend/alembic/versions/002_core_domain_data_model.py`

**Checkpoint**: User Story 1 is independently testable as the MVP domain model for daily tracking data.

---

## Phase 4: User Story 2 - Preserve Import Traceability (Priority: P2)

**Goal**: Represent import attempts, aggregate row counts, row-level outcomes, created-record links, duplicate skips, and run statuses for later CSV processing.

**Independent Test**: Create a hypothetical import run and verify status transitions, row counts, invalid/skipped/failed row outcomes, duplicate skip behavior, and traceability from created tasks and notes back to the run.

### Tests for User Story 2

- [X] T039 [P] [US2] Add import run status transition and count tests in `backend/tests/domain/test_import_runs.py`
- [X] T040 [P] [US2] Add import row outcome validation tests in `backend/tests/domain/test_import_row_outcomes.py`
- [X] T041 [P] [US2] Add duplicate imported task skip tests in `backend/tests/domain/test_import_deduplication.py`
- [X] T042 [P] [US2] Add import repository traceability tests in `backend/tests/repositories/test_import_run_repository.py`
- [X] T043 [P] [US2] Extend migration assertions for import run and row outcome tables in `backend/tests/migrations/test_core_domain_migration.py`

### Implementation for User Story 2

- [X] T044 [P] [US2] Implement `ImportRun` and `ImportRowOutcome` ORM models in `backend/app/modules/imports/models.py`
- [X] T045 [P] [US2] Implement import run and row outcome schemas in `backend/app/modules/imports/schemas.py`
- [X] T046 [P] [US2] Implement import constants for row outcome types in `backend/app/modules/imports/constants.py`
- [X] T047 [P] [US2] Implement import domain exceptions in `backend/app/modules/imports/exceptions.py`
- [X] T048 [US2] Implement `ImportRunRepository` and row outcome persistence in `backend/app/modules/imports/repositories/import_run_repository.py`
- [X] T049 [US2] Implement `ImportTraceService` run creation, processing transition, row outcome recording, and terminal status rules in `backend/app/modules/imports/services/import_trace_service.py`
- [X] T050 [US2] Integrate imported duplicate detection with `TaskService.create_task` in `backend/app/modules/tasks/services/task_service.py`
- [X] T051 [US2] Wire import trace service and repository providers in `backend/app/modules/imports/dependencies.py`
- [X] T052 [US2] Add ImportRun and ImportRowOutcome table definitions, relationships, indexes, and constraints to `backend/alembic/versions/002_core_domain_data_model.py`

**Checkpoint**: User Story 2 is independently testable for import traceability without implementing CSV upload or parsing.

---

## Phase 5: User Story 3 - Support Future AI Insight Runs (Priority: P3)

**Goal**: Represent daily and weekly AI insight run attempts separately from source data, with immutable source links, shared statuses, rerun history, and failure details.

**Independent Test**: Create hypothetical daily and weekly AI runs and verify target-period validation, source daily-log links, status transitions, rerun history, and failure details without mutating source records.

### Tests for User Story 3

- [X] T053 [P] [US3] Add AI insight target-period validation tests in `backend/tests/domain/test_ai_insight_runs.py`
- [X] T054 [P] [US3] Add AI insight status transition and rerun history tests in `backend/tests/domain/test_ai_insight_run_lifecycle.py`
- [X] T055 [P] [US3] Add AI insight source immutability tests in `backend/tests/domain/test_ai_insight_sources.py`
- [X] T056 [P] [US3] Add AI insight repository traceability tests in `backend/tests/repositories/test_ai_insight_run_repository.py`
- [X] T057 [P] [US3] Extend migration assertions for AI insight run and source tables in `backend/tests/migrations/test_core_domain_migration.py`

### Implementation for User Story 3

- [X] T058 [P] [US3] Implement `AIInsightRun` and `AIInsightRunSource` ORM models in `backend/app/modules/ai_insights/models.py`
- [X] T059 [P] [US3] Implement AI insight run schemas in `backend/app/modules/ai_insights/schemas.py`
- [X] T060 [P] [US3] Implement AI insight constants for daily and weekly target periods in `backend/app/modules/ai_insights/constants.py`
- [X] T061 [P] [US3] Implement AI insight domain exceptions in `backend/app/modules/ai_insights/exceptions.py`
- [X] T062 [US3] Implement `AIInsightRunRepository` and source-link persistence in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [X] T063 [US3] Implement `AIInsightRunService` target-period validation, source linking, status transitions, and rerun creation in `backend/app/modules/ai_insights/services/ai_insight_run_service.py`
- [X] T064 [US3] Wire AI insight run service and repository providers in `backend/app/modules/ai_insights/dependencies.py`
- [X] T065 [US3] Add AIInsightRun and AIInsightRunSource table definitions, relationships, indexes, and constraints to `backend/alembic/versions/002_core_domain_data_model.py`

**Checkpoint**: All Phase 1 user stories are independently testable without executing AI analysis.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, and out-of-scope boundaries across the completed Phase 1 model.

- [X] T066 [P] Update module README ownership notes in `backend/app/modules/daily_logs/README.md`, `backend/app/modules/tasks/README.md`, `backend/app/modules/notes/README.md`, `backend/app/modules/imports/README.md`, and `backend/app/modules/ai_insights/README.md`
- [X] T067 [P] Update Phase 1 implementation notes in `docs/FOUNDATION.md`
- [X] T068 Run backend service, repository, and migration tests documented in `specs/002-core-domain-data-model/quickstart.md`
- [X] T069 Run the out-of-scope surface scan from `specs/002-core-domain-data-model/quickstart.md`
- [X] T070 Review `backend/alembic/versions/002_core_domain_data_model.py` against `specs/002-core-domain-data-model/data-model.md` for all fields, constraints, indexes, and relationships
- [X] T071 Review `backend/app/modules/daily_logs/services/daily_log_service.py`, `backend/app/modules/tasks/services/task_service.py`, `backend/app/modules/notes/services/note_service.py`, `backend/app/modules/imports/services/import_trace_service.py`, `backend/app/modules/ai_insights/services/ai_insight_run_service.py`, `backend/app/modules/daily_logs/repositories/daily_log_repository.py`, `backend/app/modules/tasks/repositories/task_repository.py`, `backend/app/modules/notes/repositories/note_repository.py`, `backend/app/modules/imports/repositories/import_run_repository.py`, and `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py` for Router -> Service -> Repository -> Database boundary compliance

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and benefits from US1 `Task`/`Note` models and services.
- **User Story 3 (Phase 5)**: Depends on Foundational and benefits from US1 `DailyLog` model and repository.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Model Daily Tracking Records**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Preserve Import Traceability**: Starts after Foundational; integrates with US1 task/note traceability for full value.
- **US3 - Support Future AI Insight Runs**: Starts after Foundational; integrates with US1 daily-log source records for full value.

### Within Each User Story

- Tests are written before implementation.
- Models and schemas before repositories and services.
- Repositories before services.
- Services before dependency providers.
- Migration table definitions after model shape is known, then migration tests must pass.
- No router or frontend work unless a later approved task changes Phase 1 scope.

---

## Parallel Opportunities

- T003 and T004 can run in parallel after T001.
- T008, T009, T010, T013, and T014 can run in parallel after T005-T007 are understood.
- US1 test tasks T015-T019 can run in parallel.
- US1 model/schema/exception tasks T020-T028 can run in parallel before repository/service integration.
- US2 test tasks T039-T043 can run in parallel.
- US2 model/schema/constants/exception tasks T044-T047 can run in parallel before repository/service integration.
- US3 test tasks T053-T057 can run in parallel.
- US3 model/schema/constants/exception tasks T058-T061 can run in parallel before repository/service integration.

---

## Parallel Example: User Story 1

```text
Task: "T015 Add DailyLog uniqueness and date reuse service tests in backend/tests/domain/test_daily_logs.py"
Task: "T016 Add task duration, tag normalization, and category normalization service tests in backend/tests/domain/test_tasks.py"
Task: "T017 Add empty note and one-active-note service tests in backend/tests/domain/test_notes.py"
Task: "T020 Implement DailyLog ORM model in backend/app/modules/daily_logs/models.py"
Task: "T021 Implement Category and Task ORM models in backend/app/modules/tasks/models.py"
Task: "T022 Implement Note ORM model in backend/app/modules/notes/models.py"
```

## Parallel Example: User Story 2

```text
Task: "T039 Add import run status transition and count tests in backend/tests/domain/test_import_runs.py"
Task: "T040 Add import row outcome validation tests in backend/tests/domain/test_import_row_outcomes.py"
Task: "T044 Implement ImportRun and ImportRowOutcome ORM models in backend/app/modules/imports/models.py"
Task: "T045 Implement import run and row outcome schemas in backend/app/modules/imports/schemas.py"
```

## Parallel Example: User Story 3

```text
Task: "T053 Add AI insight target-period validation tests in backend/tests/domain/test_ai_insight_runs.py"
Task: "T054 Add AI insight status transition and rerun history tests in backend/tests/domain/test_ai_insight_run_lifecycle.py"
Task: "T058 Implement AIInsightRun and AIInsightRunSource ORM models in backend/app/modules/ai_insights/models.py"
Task: "T059 Implement AI insight run schemas in backend/app/modules/ai_insights/schemas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup tasks T001-T004.
2. Complete Phase 2 foundational tasks T005-T014.
3. Complete US1 tasks T015-T038.
4. Stop and validate daily tracking records independently with the US1 tests and quickstart checks.

### Incremental Delivery

1. Setup + Foundational create the backend database and test base.
2. US1 delivers the core daily tracking model.
3. US2 adds import traceability without implementing CSV upload/parsing.
4. US3 adds AI run traceability without implementing AI execution.
5. Polish verifies boundaries and documentation.

### Scope Guardrails

- Do not add CSV upload, CSV parsing, Celery jobs, dashboard screens, frontend data fetching, AI prompt execution, scheduled imports, or scheduled AI runs.
- Do not add Phase 1 feature logic to `backend/src/main.py` or root `backend/main.py`.
- Keep business rules in services and persistence logic in repositories.
- Keep import traceability in `backend/app/modules/imports/`.
- Keep AI run traceability in `backend/app/modules/ai_insights/`.
