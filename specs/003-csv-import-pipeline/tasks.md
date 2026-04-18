# Tasks: CSV Import Pipeline

**Input**: Design documents from `/specs/003-csv-import-pipeline/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/import-api.yaml](./contracts/import-api.yaml)

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Worker changes MUST include worker delegation tests. Write tests before implementation for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add backend dependencies, test package folders, and documentation needed before CSV import work begins.

- [X] T001 Add Celery, Redis client, python-multipart, and HTTPX test dependency entries to `backend/pyproject.toml`
- [X] T002 [P] Create backend API and worker package markers in `backend/app/api/__init__.py`, `backend/app/workers/__init__.py`, and `backend/app/workers/tasks/__init__.py`
- [X] T003 [P] Create Phase 2 test package markers in `backend/tests/api/__init__.py` and `backend/tests/workers/__init__.py`
- [X] T004 [P] Add Phase 2 import pipeline test command documentation to `backend/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core settings, response, routing, auth-context, and worker scaffolding that all user stories depend on.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T005 Implement Redis settings in `backend/app/settings/redis.py`
- [X] T006 Implement Celery settings in `backend/app/settings/celery.py`
- [X] T007 Compose Redis and Celery settings in `backend/app/core/config.py`
- [X] T008 [P] Implement standard success/error response schema helpers in `backend/app/shared/schemas/responses.py`
- [X] T009 [P] Implement application error mapping helpers for stable error codes in `backend/app/core/exceptions.py`
- [X] T010 [P] Implement request context and current-owner dependency stubs for import APIs in `backend/app/api/dependencies.py`
- [X] T011 [P] Implement request-id logging helper for import services and workers in `backend/app/core/logging.py`
- [X] T012 Implement Celery app configuration in `backend/app/workers/celery_app.py`
- [X] T013 Extend import constants for CSV source, pagination defaults, upload limits, date formats, and rate-limit names in `backend/app/modules/imports/constants.py`
- [X] T014 Extend import exceptions for CSV parsing, validation, permission, not-found, and enqueue failures in `backend/app/modules/imports/exceptions.py`
- [X] T015 Register versioned API router composition in `backend/app/api/router.py`
- [X] T016 Wire FastAPI application startup and `/api/v1` router inclusion in `backend/app/main.py`
- [X] T017 Update root backend entrypoint to delegate to `backend/app/main.py` without feature logic in `backend/main.py`

**Checkpoint**: Settings, response helpers, API composition, and worker scaffolding are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Preview CSV Import Data (Priority: P1) MVP

**Goal**: Upload a Notion-compatible CSV and preview parsed rows with validation status and normalized values without creating tracking records or ImportRun records.

**Independent Test**: Submit a CSV file with required and optional columns, valid rows, invalid rows, tags, notes, ISO dates, and Notion-style dates; verify preview results and confirm no persistent records are created.

### Tests for User Story 1

- [X] T018 [P] [US1] Add CSV parser unit tests for headers, empty files, unreadable CSV, ISO dates, Notion-style dates, invalid dates, durations, tags, and notes in `backend/tests/domain/test_csv_parser_service.py`
- [X] T019 [P] [US1] Add preview service no-side-effects tests for ImportRun and tracking records in `backend/tests/domain/test_import_preview_service.py`
- [X] T020 [P] [US1] Add preview API success envelope and normalized payload tests in `backend/tests/api/test_import_preview_api.py`
- [X] T021 [P] [US1] Add preview API validation error envelope tests for missing columns and invalid files in `backend/tests/api/test_import_preview_api_errors.py`

### Implementation for User Story 1

- [X] T022 [P] [US1] Add parsed row, normalized row, invalid row, and preview response schemas in `backend/app/modules/imports/schemas.py`
- [X] T023 [P] [US1] Implement CSV date, duration, text, header, and tag parsing helpers in `backend/app/modules/imports/utils.py`
- [X] T024 [US1] Implement CSV parsing and row validation service in `backend/app/modules/imports/services/csv_parser_service.py`
- [X] T025 [US1] Implement side-effect-free preview orchestration in `backend/app/modules/imports/services/import_preview_service.py`
- [X] T026 [US1] Wire parser and preview service providers in `backend/app/modules/imports/dependencies.py`
- [X] T027 [US1] Implement `POST /api/v1/imports/csv/preview` in `backend/app/modules/imports/router.py`
- [X] T028 [US1] Register the imports router under `/api/v1/imports` in `backend/app/api/router.py`
- [X] T029 [US1] Map CSV parsing and validation exceptions to unified error responses in `backend/app/core/exceptions.py`
- [X] T030 [US1] Update import module ownership notes for preview behavior in `backend/app/modules/imports/README.md`

**Checkpoint**: User Story 1 is independently testable as the MVP preview flow with no persisted import side effects.

---

## Phase 4: User Story 2 - Import Valid Daily Tracking Rows (Priority: P2)

**Goal**: Confirm a CSV import, create an ImportRun, process valid non-duplicate rows asynchronously, normalize values, reuse daily logs/categories, create optional notes, and record invalid or duplicate rows.

**Independent Test**: Confirm a mixed CSV containing valid, invalid, duplicate, optional tag, and optional note rows; verify only non-duplicate valid rows are saved with expected normalized values and invalid/duplicate rows are recorded.

### Tests for User Story 2

- [X] T031 [P] [US2] Add confirmed import command tests for ImportRun creation, server-side revalidation, and enqueue behavior in `backend/tests/domain/test_csv_import_confirmation.py`
- [X] T032 [P] [US2] Add import execution tests for daily log reuse, category reuse, task insertion, notes, tags, invalid rows, duplicate skips, and raw CSV non-retention in `backend/tests/domain/test_csv_import_pipeline.py`
- [X] T033 [P] [US2] Add confirmed import API `202` success envelope and idempotency header tests in `backend/tests/api/test_import_confirm_api.py`
- [X] T034 [P] [US2] Add confirmed import API validation, conflict, auth, permission, and rate-limit error envelope tests in `backend/tests/api/test_import_confirm_api_errors.py`
- [X] T035 [P] [US2] Add import worker delegation tests in `backend/tests/workers/test_import_worker.py`

### Implementation for User Story 2

- [X] T036 [P] [US2] Add confirmed import request, accepted response, and import processing result schemas in `backend/app/modules/imports/schemas.py`
- [X] T037 [US2] Implement confirmed import orchestration and enqueue behavior in `backend/app/modules/imports/services/csv_import_service.py`
- [X] T038 [US2] Implement row processing service logic that delegates to `DailyLogService`, `TaskService`, `NoteService`, and `ImportTraceService` in `backend/app/modules/imports/services/csv_import_service.py`
- [X] T039 [US2] Extend import trace service terminal status handling for completed, completed_with_errors, and failed confirmed imports in `backend/app/modules/imports/services/import_trace_service.py`
- [X] T040 [US2] Wire confirmed import service dependencies to daily log, task, note, and trace services in `backend/app/modules/imports/dependencies.py`
- [X] T041 [US2] Implement thin Celery import task delegation in `backend/app/workers/tasks/import_tasks.py`
- [X] T042 [US2] Implement `POST /api/v1/imports/csv` with multipart upload, current-owner context, idempotency header handling, and standard envelope in `backend/app/modules/imports/router.py`
- [X] T043 [US2] Add import submission request-id logging and `import_run_id` correlation logs in `backend/app/modules/imports/services/csv_import_service.py`
- [X] T044 [US2] Add raw CSV non-retention safeguards and row snapshot minimization in `backend/app/modules/imports/services/csv_import_service.py`
- [X] T045 [US2] Add Redis and Celery environment examples for confirmed imports in `.env.example`

**Checkpoint**: User Stories 1 and 2 are independently testable; preview remains side-effect free and confirmed imports create structured daily tracking records.

---

## Phase 5: User Story 3 - Track Import Progress and Outcomes (Priority: P3)

**Goal**: Let the user review each confirmed import attempt by status, counts, timing, failure details, and row-level invalid/skipped/failed outcomes.

**Independent Test**: Start an import and review its ImportRun while processing, after clean completion, after completion with row errors, and after failure; verify page/limit pagination for history and row outcomes.

### Tests for User Story 3

- [X] T046 [P] [US3] Add import repository pagination and owner-scoped lookup tests in `backend/tests/repositories/test_import_run_repository.py`
- [X] T047 [P] [US3] Add import history API pagination and success envelope tests in `backend/tests/api/test_import_history_api.py`
- [X] T048 [P] [US3] Add import status API success, not-found, auth, and permission error envelope tests in `backend/tests/api/test_import_status_api.py`
- [X] T049 [P] [US3] Add import row outcome API pagination and ordering tests in `backend/tests/api/test_import_row_outcomes_api.py`

### Implementation for User Story 3

- [X] T050 [P] [US3] Add import run page, row outcome page, and status response schemas in `backend/app/modules/imports/schemas.py`
- [X] T051 [US3] Implement owner-scoped import run list, import run get, and row outcome list repository methods in `backend/app/modules/imports/repositories/import_run_repository.py`
- [X] T052 [US3] Implement import history and row outcome query service methods in `backend/app/modules/imports/services/import_trace_service.py`
- [X] T053 [US3] Implement `GET /api/v1/imports` with `page` and `limit` pagination in `backend/app/modules/imports/router.py`
- [X] T054 [US3] Implement `GET /api/v1/imports/{import_run_id}` with owner-scoped status response in `backend/app/modules/imports/router.py`
- [X] T055 [US3] Implement `GET /api/v1/imports/{import_run_id}/row-outcomes` with `page` and `limit` pagination in `backend/app/modules/imports/router.py`
- [X] T056 [US3] Map import not-found and pagination validation errors to unified error responses in `backend/app/core/exceptions.py`
- [X] T057 [US3] Add status transition and row-count consistency logging in `backend/app/modules/imports/services/import_trace_service.py`

**Checkpoint**: All Phase 2 user stories are independently functional and traceable through versioned APIs.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, contracts, and out-of-scope boundaries across the completed Phase 2 import pipeline.

- [X] T058 [P] Update Phase 2 implementation notes in `docs/FOUNDATION.md`
- [X] T059 [P] Update import API contract examples after implementation in `specs/003-csv-import-pipeline/contracts/import-api.yaml`
- [X] T060 Run backend Phase 2 tests documented in `specs/003-csv-import-pipeline/quickstart.md`
- [X] T061 Run the out-of-scope surface scan from `specs/003-csv-import-pipeline/quickstart.md`
- [X] T062 Review `backend/app/modules/imports/router.py`, `backend/app/modules/imports/services/csv_parser_service.py`, `backend/app/modules/imports/services/import_preview_service.py`, `backend/app/modules/imports/services/csv_import_service.py`, `backend/app/modules/imports/services/import_trace_service.py`, `backend/app/modules/imports/repositories/import_run_repository.py`, and `backend/app/workers/tasks/import_tasks.py` for Router -> Service -> Repository -> Database and thin-worker boundary compliance
- [X] T063 Verify all handled import API responses use standard success/error envelopes across `backend/app/modules/imports/router.py` and `backend/app/core/exceptions.py`
- [X] T064 Verify import run history and row outcome list pagination defaults and maximum limits in `backend/app/modules/imports/router.py`
- [X] T065 Verify raw CSV contents are not retained by reviewing `backend/app/modules/imports/services/import_preview_service.py`, `backend/app/modules/imports/services/csv_import_service.py`, and `backend/app/modules/imports/models.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and can reuse US1 parser behavior; confirmed import remains independently testable by exercising the service/API directly.
- **User Story 3 (Phase 5)**: Depends on Foundational and ImportRun traceability; it can be tested with seeded ImportRun data even if worker execution is stubbed.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Preview CSV Import Data**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Import Valid Daily Tracking Rows**: Starts after Foundational; reuses parsing rules from US1 but must revalidate confirmed uploads server-side.
- **US3 - Track Import Progress and Outcomes**: Starts after Foundational; reads existing ImportRun and ImportRowOutcome data and can be validated with seeded records.

### Within Each User Story

- Tests are written before implementation.
- Schemas and exceptions before services.
- Parser/utility logic before preview or confirmed import services.
- Repositories before query services.
- Services before endpoints and worker tasks.
- Dependency providers before router wiring.
- Exception/status mappings before endpoint error handling.
- Pagination contracts before list endpoint implementation.
- Worker tasks stay thin and delegate to services.

---

## Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001 is understood.
- T008, T009, T010, T011, T013, and T014 can run in parallel after settings decisions are clear.
- US1 tests T018-T021 can run in parallel.
- US1 schema/helper tasks T022-T023 can run in parallel before service integration.
- US2 tests T031-T035 can run in parallel.
- US2 schema, worker, and environment tasks T036, T041, and T045 can run in parallel after foundational setup.
- US3 tests T046-T049 can run in parallel.
- US3 schema task T050 can run in parallel with repository task T051 after the pagination contract is understood.
- Polish documentation tasks T058-T059 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "T018 Add CSV parser unit tests in backend/tests/domain/test_csv_parser_service.py"
Task: "T019 Add preview service no-side-effects tests in backend/tests/domain/test_import_preview_service.py"
Task: "T020 Add preview API success envelope tests in backend/tests/api/test_import_preview_api.py"
Task: "T021 Add preview API validation error envelope tests in backend/tests/api/test_import_preview_api_errors.py"
Task: "T022 Add preview schemas in backend/app/modules/imports/schemas.py"
Task: "T023 Implement CSV parsing helpers in backend/app/modules/imports/utils.py"
```

## Parallel Example: User Story 2

```text
Task: "T031 Add confirmed import command tests in backend/tests/domain/test_csv_import_confirmation.py"
Task: "T032 Add import execution tests in backend/tests/domain/test_csv_import_pipeline.py"
Task: "T033 Add confirmed import API success tests in backend/tests/api/test_import_confirm_api.py"
Task: "T035 Add import worker delegation tests in backend/tests/workers/test_import_worker.py"
Task: "T041 Implement thin Celery import task in backend/app/workers/tasks/import_tasks.py"
```

## Parallel Example: User Story 3

```text
Task: "T046 Add import repository pagination tests in backend/tests/repositories/test_import_run_repository.py"
Task: "T047 Add import history API pagination tests in backend/tests/api/test_import_history_api.py"
Task: "T048 Add import status API tests in backend/tests/api/test_import_status_api.py"
Task: "T049 Add import row outcome API tests in backend/tests/api/test_import_row_outcomes_api.py"
Task: "T050 Add import run page and row outcome page schemas in backend/app/modules/imports/schemas.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup tasks T001-T004.
2. Complete Phase 2 foundational tasks T005-T017.
3. Complete US1 tasks T018-T030.
4. Stop and validate preview independently with US1 tests and quickstart preview checks.

### Incremental Delivery

1. Setup + Foundational create API, response, settings, and worker scaffolding.
2. US1 delivers CSV preview without side effects.
3. US2 adds confirmed async import execution and structured record creation.
4. US3 adds status/history and row outcome review APIs.
5. Polish verifies contracts, response shapes, raw CSV non-retention, and boundaries.

### Scope Guardrails

- Do not add dashboard visualization, AI execution, scheduled imports, Notion API synchronization, or report export.
- Do not add Phase 2 feature logic to `backend/src/main.py` or root `backend/main.py`.
- Keep business rules in services and persistence logic in repositories.
- Keep worker tasks thin and delegate to services.
- Keep full raw CSV file contents out of persistence.
