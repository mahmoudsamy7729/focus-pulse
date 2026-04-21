# Tasks: Automation & Reliability

**Input**: Design documents from `/specs/007-automation-reliability/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/automation-api.yaml](./contracts/automation-api.yaml), [quickstart.md](./quickstart.md)

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Worker changes MUST include worker delegation and idempotency tests. Write tests before implementation for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create Phase 6 placeholders, worker scaffolding, and test files needed before implementation begins.

- [ ] T001 Create Phase 6 worker scaffolding placeholders in `backend/app/workers/scheduler.py`, `backend/app/workers/schedule_windows.py`, `backend/app/workers/tasks/schedule_evaluator_tasks.py`, `backend/app/workers/tasks/scheduled_import_tasks.py`, and `backend/app/workers/tasks/scheduled_ai_analysis_tasks.py`
- [ ] T002 [P] Create import schedule repository and service placeholders in `backend/app/modules/imports/repositories/import_schedule_repository.py`, `backend/app/modules/imports/services/import_schedule_service.py`, and `backend/app/modules/imports/services/scheduled_import_service.py`
- [ ] T003 [P] Create AI analysis schedule repository and service placeholders in `backend/app/modules/ai_insights/repositories/ai_analysis_schedule_repository.py`, `backend/app/modules/ai_insights/services/ai_analysis_schedule_service.py`, and `backend/app/modules/ai_insights/services/scheduled_ai_analysis_service.py`
- [ ] T004 [P] Create Phase 6 test file placeholders in `backend/tests/domain/test_schedule_window_rules.py`, `backend/tests/migrations/test_automation_reliability_migration.py`, `backend/tests/repositories/test_import_schedule_repository.py`, `backend/tests/repositories/test_ai_analysis_schedule_repository.py`, `backend/tests/services/test_import_schedule_service.py`, `backend/tests/services/test_scheduled_import_service.py`, `backend/tests/services/test_ai_analysis_schedule_service.py`, `backend/tests/services/test_scheduled_ai_analysis_service.py`, `backend/tests/api/test_import_schedules_api.py`, `backend/tests/api/test_ai_analysis_schedules_api.py`, `backend/tests/workers/test_schedule_evaluator_worker.py`, `backend/tests/workers/test_scheduled_import_worker.py`, and `backend/tests/workers/test_scheduled_ai_analysis_worker.py`
- [ ] T005 [P] Add Phase 6 scope and no-new-module scheduling ownership notes to `backend/app/workers/README.md`, `backend/app/modules/imports/README.md`, and `backend/app/modules/ai_insights/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared schedule vocabulary, persistence, migration, worker configuration, audit/logging hooks, and dependency wiring required by all user stories.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T006 [P] Add migration tests for import schedule/history tables, AI analysis schedule/history tables, indexes, idempotency constraints, soft-delete fields, and 90-day retention fields in `backend/tests/migrations/test_automation_reliability_migration.py`
- [ ] T007 [P] Add shared schedule window tests for daily windows, weekly Monday-to-Sunday windows, timezone run times, latest-missed-window catch-up, older skipped windows, and idempotency keys in `backend/tests/domain/test_schedule_window_rules.py`
- [ ] T008 [P] Add base API error envelope tests for schedule validation, schedule not found, permission failure, conflict, and rate-limit mappings in `backend/tests/api/test_automation_schedule_api_errors.py`
- [ ] T009 Define Phase 6 schedule constants for schedule state, automation type, cadence, outcome, failure classification, pagination defaults, rate-limit names, retention days, and max attempts in `backend/app/modules/imports/constants.py` and `backend/app/modules/ai_insights/constants.py`
- [ ] T010 Define Phase 6 custom exceptions for invalid schedule, schedule not found, schedule conflict, duplicate due window, unsupported source, non-retryable failure, retry exhausted, and retention violation in `backend/app/modules/imports/exceptions.py` and `backend/app/modules/ai_insights/exceptions.py`
- [ ] T011 Add Phase 6 exception mappings to unified error handling in `backend/app/core/exceptions.py`
- [ ] T012 Add or verify `imports:read`, `imports:write`, `ai_insights:read`, and `ai_insights:write` scope support for Phase 6 endpoints in `backend/app/api/dependencies.py`
- [ ] T013 Extend Celery settings with beat schedule interval, scheduler enabled flag, schedule retention days, and max scheduled run attempts in `backend/app/settings/celery.py`
- [ ] T014 Register Celery Beat schedule entries for due-window evaluation tasks in `backend/app/workers/celery_app.py`
- [ ] T015 Implement shared schedule window value objects, date calculations, local-time resolution, latest missed-window selection, and idempotency key generation in `backend/app/workers/schedule_windows.py`
- [ ] T016 Implement base scheduler orchestration helpers for correlation IDs, due-window iteration, and module service delegation in `backend/app/workers/scheduler.py`
- [ ] T017 Extend import ORM models with `ImportAutomationSchedule` and `ImportAutomationRun` including relationships to `ImportRun` in `backend/app/modules/imports/models.py`
- [ ] T018 Extend AI insights ORM models with `AIAnalysisAutomationSchedule` and `AIAnalysisAutomationRun` including relationships to `AIInsightRun` in `backend/app/modules/ai_insights/models.py`
- [ ] T019 Add Alembic migration for Phase 6 schedule/history persistence, indexes, idempotency constraints, soft delete, and retention summary fields in `backend/alembic/versions/007_automation_reliability.py`
- [ ] T020 Define shared import schedule schemas for create, update, schedule response, run response, list filters, page metadata, and delete response in `backend/app/modules/imports/schemas.py`
- [ ] T021 Define shared AI analysis schedule schemas for create, update, schedule response, run response, list filters, page metadata, and delete response in `backend/app/modules/ai_insights/schemas.py`
- [ ] T022 Implement base import schedule repository methods for create, owner-scoped get, list with page/limit, soft delete, state updates, due active lookup, and history list in `backend/app/modules/imports/repositories/import_schedule_repository.py`
- [ ] T023 Implement base AI analysis schedule repository methods for create, owner-scoped get, list with page/limit, soft delete, state updates, due active lookup, and history list in `backend/app/modules/ai_insights/repositories/ai_analysis_schedule_repository.py`
- [ ] T024 Wire import schedule repository and services in `backend/app/modules/imports/dependencies.py`
- [ ] T025 Wire AI analysis schedule repository and services in `backend/app/modules/ai_insights/dependencies.py`
- [ ] T026 Register Phase 6 route placeholders under existing routers in `backend/app/modules/imports/router.py`, `backend/app/modules/ai_insights/router.py`, and `backend/app/api/router.py`

**Checkpoint**: Shared persistence, schedule vocabulary, due-window calculation, Celery Beat wiring, error mappings, auth scopes, and dependency providers are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Run Scheduled Imports Reliably (Priority: P1) MVP

**Goal**: Create, manage, trigger, and review scheduled CSV imports that consume newly available CSV input, preserve Phase 2 import guarantees, and avoid duplicate work.

**Independent Test**: Enable a daily import schedule for a configured CSV source, trigger or evaluate a due window, and verify exactly one traceable import run is created, processed or skipped, retried safely, and reviewable later.

### Tests for User Story 1

- [ ] T027 [P] [US1] Add import schedule service tests for create, update, pause, resume, soft delete, active-only evaluation, source reference validation, and next run time calculation in `backend/tests/services/test_import_schedule_service.py`
- [ ] T028 [P] [US1] Add scheduled import service tests for newly available CSV input, no-new-data outcome, unsupported source failure, source fingerprint idempotency, row-count summary, and raw CSV non-retention in `backend/tests/services/test_scheduled_import_service.py`
- [ ] T029 [P] [US1] Add import schedule repository tests for owner-scoped CRUD, soft-delete exclusion, due active lookup, duplicate due-window protection, and paginated run history in `backend/tests/repositories/test_import_schedule_repository.py`
- [ ] T030 [P] [US1] Add import schedule API success tests for create, list, detail, update, delete, trigger, and run history success envelopes in `backend/tests/api/test_import_schedules_api.py`
- [ ] T031 [P] [US1] Add import schedule API error tests for invalid source reference, unsupported cadence, permission failure, duplicate window conflict, deleted schedule, auth failure, and rate-limit envelope in `backend/tests/api/test_import_schedules_api.py`
- [ ] T032 [P] [US1] Add scheduled import worker tests for thin task delegation, session commit, existing run reuse, fallback behavior, and no duplicate downstream import task enqueue in `backend/tests/workers/test_scheduled_import_worker.py`

### Implementation for User Story 1

- [ ] T033 [P] [US1] Implement import schedule create/update/pause/resume/delete, next-run calculation, active-state validation, and audit metadata in `backend/app/modules/imports/services/import_schedule_service.py`
- [ ] T034 [P] [US1] Implement import schedule persistence, due-window lookup, history creation, run updates, idempotency lookup, and paginated history queries in `backend/app/modules/imports/repositories/import_schedule_repository.py`
- [ ] T035 [US1] Implement scheduled import source-reference validation, new-input detection, no-new-data outcome, source fingerprinting, ImportRun creation, and row-count summary updates in `backend/app/modules/imports/services/scheduled_import_service.py`
- [ ] T036 [US1] Integrate scheduled import execution with existing CSV import processing without retaining raw CSV contents in `backend/app/modules/imports/services/csv_import_service.py`
- [ ] T037 [US1] Extend import schemas for schedule create/update, schedule response, trigger response, history response, source reference, outcome, and pagination metadata in `backend/app/modules/imports/schemas.py`
- [ ] T038 [US1] Implement import schedule endpoints `POST /api/v1/imports/schedules`, `GET /api/v1/imports/schedules`, `GET/PATCH/DELETE /api/v1/imports/schedules/{schedule_id}`, `POST /api/v1/imports/schedules/{schedule_id}/trigger`, and `GET /api/v1/imports/schedules/{schedule_id}/runs` in `backend/app/modules/imports/router.py`
- [ ] T039 [US1] Implement scheduled import Celery task wrapper that delegates to `ScheduledImportService` and existing import task behavior in `backend/app/workers/tasks/scheduled_import_tasks.py`
- [ ] T040 [US1] Add request-id or scheduler correlation ID, owner ID, schedule ID, due window, source fingerprint, ImportRun ID, status, outcome, retry count, and failure details structured logs in `backend/app/modules/imports/services/scheduled_import_service.py`
- [ ] T041 [US1] Add import schedule mutation and terminal outcome audit writes in `backend/app/modules/imports/services/import_schedule_service.py` and `backend/app/modules/imports/services/scheduled_import_service.py`

**Checkpoint**: User Story 1 is independently testable as the MVP scheduled import flow.

---

## Phase 4: User Story 2 - Run Scheduled AI Analysis (Priority: P2)

**Goal**: Create, manage, trigger, and review scheduled daily/weekly AI analysis runs for completed periods without automatically generating Phase 5 insight results.

**Independent Test**: Enable scheduled daily and weekly AI analysis, seed saved tracking records, trigger or evaluate due windows, and verify completed, no-data, failed, and reused/in-flight outcomes are recorded without duplicate current AI results.

### Tests for User Story 2

- [ ] T042 [P] [US2] Add AI analysis schedule service tests for create, update, pause, resume, soft delete, target period rule, daily previous-day resolution, weekly last-completed-week resolution, and future-period skip in `backend/tests/services/test_ai_analysis_schedule_service.py`
- [ ] T043 [P] [US2] Add scheduled AI analysis service tests for AIInsightRun creation, no-data outcome, in-flight reuse/skip, completed run reuse/skip, note-text exclusion delegation, and no Phase 5 result generation in `backend/tests/services/test_scheduled_ai_analysis_service.py`
- [ ] T044 [P] [US2] Add AI analysis schedule repository tests for owner-scoped CRUD, soft-delete exclusion, due active lookup, duplicate target-period protection, and paginated run history in `backend/tests/repositories/test_ai_analysis_schedule_repository.py`
- [ ] T045 [P] [US2] Add AI analysis schedule API success tests for create, list, detail, update, delete, trigger, and run history success envelopes in `backend/tests/api/test_ai_analysis_schedules_api.py`
- [ ] T046 [P] [US2] Add AI analysis schedule API error tests for invalid target period, incomplete future period, permission failure, duplicate window conflict, deleted schedule, auth failure, and rate-limit envelope in `backend/tests/api/test_ai_analysis_schedules_api.py`
- [ ] T047 [P] [US2] Add scheduled AI analysis worker tests for thin task delegation, existing run reuse, session commit, fallback behavior, and no Phase 5 result enqueue in `backend/tests/workers/test_scheduled_ai_analysis_worker.py`

### Implementation for User Story 2

- [ ] T048 [P] [US2] Implement AI analysis schedule create/update/pause/resume/delete, period rule validation, next-run calculation, active-state validation, and audit metadata in `backend/app/modules/ai_insights/services/ai_analysis_schedule_service.py`
- [ ] T049 [P] [US2] Implement AI analysis schedule persistence, due-window lookup, history creation, run updates, idempotency lookup, and paginated history queries in `backend/app/modules/ai_insights/repositories/ai_analysis_schedule_repository.py`
- [ ] T050 [US2] Implement scheduled AI analysis target-period resolution, completed-period validation, no-data handling, in-flight/current run reuse, AIInsightRun creation, and schedule-run summary updates in `backend/app/modules/ai_insights/services/scheduled_ai_analysis_service.py`
- [ ] T051 [US2] Integrate scheduled AI analysis with existing AI run creation and processing services without creating `AIInsightResult` records in `backend/app/modules/ai_insights/services/ai_insight_run_service.py`
- [ ] T052 [US2] Extend AI insights schemas for analysis schedule create/update, schedule response, trigger response, history response, target period rule, outcome, and pagination metadata in `backend/app/modules/ai_insights/schemas.py`
- [ ] T053 [US2] Implement AI analysis schedule endpoints `POST /api/v1/ai-insights/analysis-schedules`, `GET /api/v1/ai-insights/analysis-schedules`, `GET/PATCH/DELETE /api/v1/ai-insights/analysis-schedules/{schedule_id}`, `POST /api/v1/ai-insights/analysis-schedules/{schedule_id}/trigger`, and `GET /api/v1/ai-insights/analysis-schedules/{schedule_id}/runs` in `backend/app/modules/ai_insights/router.py`
- [ ] T054 [US2] Implement scheduled AI analysis Celery task wrapper that delegates to `ScheduledAIAnalysisService` and existing AI analysis task behavior in `backend/app/workers/tasks/scheduled_ai_analysis_tasks.py`
- [ ] T055 [US2] Add scheduler correlation ID, owner ID, schedule ID, target period, AIInsightRun ID, status, outcome, retry count, instruction metadata, and failure details structured logs in `backend/app/modules/ai_insights/services/scheduled_ai_analysis_service.py`
- [ ] T056 [US2] Add AI analysis schedule mutation and terminal outcome audit writes in `backend/app/modules/ai_insights/services/ai_analysis_schedule_service.py` and `backend/app/modules/ai_insights/services/scheduled_ai_analysis_service.py`

**Checkpoint**: User Stories 1 and 2 are independently testable; scheduled AI analysis can run without creating Phase 5 results.

---

## Phase 5: User Story 3 - Recover and Diagnose Background Work (Priority: P3)

**Goal**: Provide bounded retries, missed-window recovery, diagnostic history, audit retention, and correlated logs across scheduled imports and scheduled AI analysis.

**Independent Test**: Force transient and permanent failures in scheduled import and AI analysis flows, then verify retry limits, non-retryable terminal failures, skipped missed windows, 90-day retention behavior, audit details, and correlated logs.

### Tests for User Story 3

- [ ] T057 [P] [US3] Add schedule evaluator worker tests for due schedule discovery, duplicate evaluator calls, latest missed-window processing, older skipped windows, inactive schedule exclusion, and mixed import/AI schedule delegation in `backend/tests/workers/test_schedule_evaluator_worker.py`
- [ ] T058 [P] [US3] Add scheduled retry tests for retryable import failures, retryable AI failures, three-attempt exhaustion, non-retryable direct failure, and attempt history preservation in `backend/tests/services/test_scheduled_work_recovery.py`
- [ ] T059 [P] [US3] Add retention and pruning service tests for 90-day detail availability, diagnostic pruning, final summary preservation, soft-deleted schedule history access, and raw CSV/note-text exclusion in `backend/tests/services/test_automation_history_retention.py`
- [ ] T060 [P] [US3] Add audit and structured logging tests for schedule mutation, manual trigger, due evaluation, retry decision, skipped window, terminal outcome, correlation IDs, and failure details in `backend/tests/services/test_automation_audit_and_logging.py`
- [ ] T061 [P] [US3] Add cross-module API history tests for status/outcome filters, page/limit metadata, pruned diagnostic summaries, soft-deleted schedule access rules, and owner isolation in `backend/tests/api/test_automation_history_api.py`

### Implementation for User Story 3

- [ ] T062 [US3] Implement due schedule evaluator orchestration for import schedules, AI analysis schedules, duplicate evaluation protection, latest missed-window processing, and older skipped-window history in `backend/app/workers/tasks/schedule_evaluator_tasks.py`
- [ ] T063 [US3] Implement retry classification, attempt incrementing, exhausted failure handling, non-retryable direct failure handling, and terminal outcome updates for scheduled imports in `backend/app/modules/imports/services/scheduled_import_service.py`
- [ ] T064 [US3] Implement retry classification, attempt incrementing, exhausted failure handling, non-retryable direct failure handling, and terminal outcome updates for scheduled AI analysis in `backend/app/modules/ai_insights/services/scheduled_ai_analysis_service.py`
- [ ] T065 [US3] Implement reusable retention/pruning helpers for 90-day diagnostic detail pruning and final summary preservation in `backend/app/workers/scheduler.py`
- [ ] T066 [US3] Add import history pruning repository methods and final-summary preservation in `backend/app/modules/imports/repositories/import_schedule_repository.py`
- [ ] T067 [US3] Add AI analysis history pruning repository methods and final-summary preservation in `backend/app/modules/ai_insights/repositories/ai_analysis_schedule_repository.py`
- [ ] T068 [US3] Add history retention and pruned-summary serialization to import schedule history schemas and endpoints in `backend/app/modules/imports/schemas.py` and `backend/app/modules/imports/router.py`
- [ ] T069 [US3] Add history retention and pruned-summary serialization to AI analysis schedule history schemas and endpoints in `backend/app/modules/ai_insights/schemas.py` and `backend/app/modules/ai_insights/router.py`
- [ ] T070 [US3] Add cross-module scheduler audit events for due evaluation, skipped missed windows, retry decisions, exhausted retries, non-retryable failures, and pruning outcomes in `backend/app/workers/scheduler.py`
- [ ] T071 [US3] Add correlation fields and terminal outcome logs across import and AI scheduler paths in `backend/app/workers/tasks/schedule_evaluator_tasks.py`, `backend/app/workers/tasks/scheduled_import_tasks.py`, and `backend/app/workers/tasks/scheduled_ai_analysis_tasks.py`

**Checkpoint**: All Phase 6 user stories are independently functional and scheduled work is manageable, executable, recoverable, traceable, and bounded.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, contracts, tests, and out-of-scope boundaries across Phase 6.

- [ ] T072 [P] Update API contract examples after implementation details settle in `specs/007-automation-reliability/contracts/automation-api.yaml`
- [ ] T073 [P] Update quickstart implementation checks after final endpoint/service names settle in `specs/007-automation-reliability/quickstart.md`
- [ ] T074 [P] Update import module documentation for scheduled CSV source references, no raw CSV retention, idempotency, and history behavior in `backend/app/modules/imports/README.md`
- [ ] T075 [P] Update AI insights module documentation for scheduled AI analysis, no Phase 5 auto-generation, no note-text exposure, and history behavior in `backend/app/modules/ai_insights/README.md`
- [ ] T076 [P] Update worker documentation for Celery Beat, due-window evaluation, missed-window catch-up, retry limits, and retention pruning in `backend/app/workers/README.md`
- [ ] T077 [P] Update environment examples for Celery Beat and scheduler retention settings in `.env.example`
- [ ] T078 Run targeted backend Phase 6 tests from `specs/007-automation-reliability/quickstart.md`
- [ ] T079 Run full backend test suite with `pytest -q` from `backend/`
- [ ] T080 Run Alembic upgrade validation for Phase 6 migration from `backend/`
- [ ] T081 Run manual API smoke checks for import schedules from `specs/007-automation-reliability/quickstart.md`
- [ ] T082 Run manual API smoke checks for AI analysis schedules from `specs/007-automation-reliability/quickstart.md`
- [ ] T083 Verify Router -> Service -> Repository -> Database boundaries across `backend/app/modules/imports/router.py`, `backend/app/modules/imports/services/`, `backend/app/modules/imports/repositories/`, `backend/app/modules/ai_insights/router.py`, `backend/app/modules/ai_insights/services/`, and `backend/app/modules/ai_insights/repositories/`
- [ ] T084 Verify Celery Beat and worker tasks stay thin and delegate business behavior to services across `backend/app/workers/tasks/schedule_evaluator_tasks.py`, `backend/app/workers/tasks/scheduled_import_tasks.py`, and `backend/app/workers/tasks/scheduled_ai_analysis_tasks.py`
- [ ] T085 Verify all handled Phase 6 API responses use standard success/error envelopes across `backend/app/modules/imports/router.py`, `backend/app/modules/ai_insights/router.py`, and `backend/app/core/exceptions.py`
- [ ] T086 Verify page/limit pagination, owner isolation, auth scopes, rate limits, soft-delete exclusion, idempotency, audit trails, and structured logs across `backend/app/modules/imports/`, `backend/app/modules/ai_insights/`, and `backend/app/workers/`
- [ ] T087 Verify Phase 6 does not add frontend schedule-management UI, automatic Phase 5 insight generation, report export, Notion API synchronization, AI chat, dashboard redesign, arbitrary external import connectors, or raw CSV retention across `backend/app/`, `frontend/`, and `specs/007-automation-reliability/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion and can be implemented in parallel with US1 if staffed.
- **User Story 3 (Phase 5)**: Depends on Foundational plus at least one scheduled work path from US1 or US2 for end-to-end verification.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Run Scheduled Imports Reliably**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Run Scheduled AI Analysis**: Starts after Foundational; no dependency on US1, but shares worker due-window infrastructure.
- **US3 - Recover and Diagnose Background Work**: Starts after Foundational; integrates with US1 and US2 scheduled-run services for full cross-module validation.

### Within Each User Story

- Tests are written before implementation.
- Constants, exceptions, models, migrations, and schemas before repositories and services.
- Repositories before services.
- Services before endpoints.
- Dependency providers before router wiring.
- Worker task wrappers after service behavior exists.
- Exception/status mappings before endpoint error handling.
- Pagination contract before list endpoint implementation.
- Audit and idempotency behavior before worker execution paths.
- Story complete before moving to next priority.

---

## Parallel Opportunities

- T002, T003, T004, and T005 can run in parallel after T001 is understood.
- T006, T007, and T008 can run in parallel before foundational implementation.
- T017 and T018 can run in parallel because they touch different module model files.
- T020 and T021 can run in parallel because they touch different module schema files.
- T022 and T023 can run in parallel because they touch different module repository files.
- T024 and T025 can run in parallel because they touch different module dependency files.
- US1 tests T027-T032 can run in parallel.
- US2 tests T042-T047 can run in parallel.
- US3 tests T057-T061 can run in parallel.
- US1 repository/service tasks T033-T035 can be split after models/schemas are ready.
- US2 repository/service tasks T048-T050 can be split after models/schemas are ready.
- Polish documentation tasks T072-T077 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "T027 Add import schedule service tests in backend/tests/services/test_import_schedule_service.py"
Task: "T028 Add scheduled import service tests in backend/tests/services/test_scheduled_import_service.py"
Task: "T029 Add import schedule repository tests in backend/tests/repositories/test_import_schedule_repository.py"
Task: "T030 Add import schedule API success tests in backend/tests/api/test_import_schedules_api.py"
Task: "T032 Add scheduled import worker tests in backend/tests/workers/test_scheduled_import_worker.py"
```

## Parallel Example: User Story 2

```text
Task: "T042 Add AI analysis schedule service tests in backend/tests/services/test_ai_analysis_schedule_service.py"
Task: "T043 Add scheduled AI analysis service tests in backend/tests/services/test_scheduled_ai_analysis_service.py"
Task: "T044 Add AI analysis schedule repository tests in backend/tests/repositories/test_ai_analysis_schedule_repository.py"
Task: "T045 Add AI analysis schedule API success tests in backend/tests/api/test_ai_analysis_schedules_api.py"
Task: "T047 Add scheduled AI analysis worker tests in backend/tests/workers/test_scheduled_ai_analysis_worker.py"
```

## Parallel Example: User Story 3

```text
Task: "T057 Add schedule evaluator worker tests in backend/tests/workers/test_schedule_evaluator_worker.py"
Task: "T058 Add scheduled retry tests in backend/tests/services/test_scheduled_work_recovery.py"
Task: "T059 Add retention and pruning service tests in backend/tests/services/test_automation_history_retention.py"
Task: "T060 Add audit and structured logging tests in backend/tests/services/test_automation_audit_and_logging.py"
Task: "T061 Add cross-module API history tests in backend/tests/api/test_automation_history_api.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Stop and validate scheduled import create/list/detail/update/delete/trigger/history plus raw CSV non-retention and duplicate-window behavior.
5. Demo or review the MVP scheduled import backend flow.

### Incremental Delivery

1. Complete Setup and Foundational phases.
2. Add User Story 1 for scheduled imports and validate independently.
3. Add User Story 2 for scheduled AI analysis and validate independently.
4. Add User Story 3 for recovery, retry, audit, logging, retention, and cross-module diagnostics.
5. Complete Polish checks and quickstart validation.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup and Foundational together.
2. After Foundational:
   - Developer A: User Story 1 import scheduling.
   - Developer B: User Story 2 AI analysis scheduling.
   - Developer C: User Story 3 recovery/diagnostics tests and shared worker behavior.
3. Integrate through the shared worker due-window service and module-owned schedule services.

---

## Notes

- [P] tasks touch different files and can run in parallel.
- [Story] labels map each task to one user story for traceability.
- Each user story is independently completable and testable.
- Tests should fail before implementation.
- Do not add `backend/app/modules/automation/`.
- Do not add frontend schedule-management UI.
- Do not add automatic Phase 5 insight generation.
- Do not retain full raw CSV contents.
