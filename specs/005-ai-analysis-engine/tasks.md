# Tasks: AI Analysis Engine

**Input**: Design documents from `/specs/005-ai-analysis-engine/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/ai-insights-api.yaml](./contracts/ai-insights-api.yaml)

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Worker changes MUST include worker delegation tests. Write tests before implementation for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Add AI analysis module scaffolding, provider package structure, and test package files needed before Phase 4 implementation begins.

- [ ] T001 Create AI insights provider package markers in `backend/app/modules/ai_insights/providers/__init__.py`
- [ ] T002 [P] Create Phase 4 service module placeholders in `backend/app/modules/ai_insights/services/ai_analysis_service.py`, `backend/app/modules/ai_insights/services/ai_input_service.py`, `backend/app/modules/ai_insights/services/ai_instruction_service.py`, and `backend/app/modules/ai_insights/services/ai_output_validator.py`
- [ ] T003 [P] Create Phase 4 provider module placeholders in `backend/app/modules/ai_insights/providers/base.py` and `backend/app/modules/ai_insights/providers/configured.py`
- [ ] T004 [P] Create Phase 4 worker placeholder in `backend/app/workers/tasks/ai_analysis_tasks.py`
- [ ] T005 [P] Create Phase 4 test package markers in `backend/tests/services/__init__.py`, `backend/tests/repositories/__init__.py`, `backend/tests/api/__init__.py`, `backend/tests/workers/__init__.py`, and `backend/tests/migrations/__init__.py`
- [ ] T006 [P] Add Phase 4 AI analysis test command notes to `backend/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared settings, persistence, constants, schemas, error mappings, auth scopes, and routing foundations required by all AI analysis stories.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T007 [P] Add AI settings tests for provider/model/timeouts/max attempts in `backend/tests/domain/test_ai_settings.py`
- [ ] T008 [P] Add AI run migration metadata tests in `backend/tests/migrations/test_ai_analysis_engine_migration.py`
- [ ] T009 [P] Add AI run model field tests for instruction metadata, output outcome, retry count, idempotency key, request id, and failure details in `backend/tests/domain/test_ai_insight_runs.py`
- [ ] T010 Implement AI settings in `backend/app/settings/ai.py`
- [ ] T011 Compose AI settings in `backend/app/core/config.py`
- [ ] T012 Add AI provider/model/retry environment examples in `.env.example`
- [ ] T013 Extend AI insight constants for period granularity, instruction names, output outcomes, retry limits, pagination defaults, and rate-limit names in `backend/app/modules/ai_insights/constants.py`
- [ ] T014 Extend AI insight exceptions for invalid period, not found, conflict, enqueue failure, provider failure, output validation failure, and idempotency conflict in `backend/app/modules/ai_insights/exceptions.py`
- [ ] T015 Add AI insight exception mappings to unified error handling in `backend/app/core/exceptions.py`
- [ ] T016 Add `ai_insights:read` and `ai_insights:write` scope support to current-owner dependency stubs in `backend/app/api/dependencies.py`
- [ ] T017 Extend `AIInsightRun` ORM fields and indexes for Phase 4 metadata in `backend/app/modules/ai_insights/models.py`
- [ ] T018 Add Alembic migration for Phase 4 AI run metadata in `backend/alembic/versions/005_ai_analysis_engine.py`
- [ ] T019 Extend AI insight base schemas, output outcome schemas, failure detail schemas, pagination schemas, and accepted response schemas in `backend/app/modules/ai_insights/schemas.py`
- [ ] T020 Extend AI insight run repository create/get/list/current/idempotency method signatures in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [ ] T021 Wire base AI insight repository and service dependencies in `backend/app/modules/ai_insights/dependencies.py`
- [ ] T022 Register AI insights router under `/api/v1/ai-insights` in `backend/app/api/router.py`

**Checkpoint**: AI settings, metadata persistence, auth scopes, exception mappings, common schemas, and router composition are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Generate Daily and Weekly Summaries (Priority: P1) MVP

**Goal**: Request combined daily or weekly AI analysis for saved tracking records, produce grounded summaries, handle no-data periods, store outputs, and review the completed run later.

**Independent Test**: Request daily and weekly analysis for seeded saved tracking data, process with a deterministic provider, and verify stored completed outputs include summaries grounded in task names, durations, categories, and tags while excluding note text.

### Tests for User Story 1

- [ ] T023 [P] [US1] Add AI input service tests for daily/weekly period resolution, active saved records, aggregate totals, and note-text exclusion in `backend/tests/services/test_ai_input_service.py`
- [ ] T024 [P] [US1] Add AI run creation and no-data service tests in `backend/tests/services/test_ai_analysis_service.py`
- [ ] T025 [P] [US1] Add deterministic provider and instruction service tests in `backend/tests/services/test_ai_instruction_service.py`
- [ ] T026 [P] [US1] Add AI run repository tests for create, source links, owner-scoped get, and soft-delete exclusion in `backend/tests/repositories/test_ai_analysis_repository.py`
- [ ] T027 [P] [US1] Add create-run API success envelope, idempotency reuse, and no-data tests in `backend/tests/api/test_ai_insight_api.py`
- [ ] T028 [P] [US1] Add create-run API validation, permission, conflict, and enqueue error tests in `backend/tests/api/test_ai_insight_api_errors.py`
- [ ] T029 [P] [US1] Add AI analysis worker success and no-data delegation tests in `backend/tests/workers/test_ai_analysis_worker.py`

### Implementation for User Story 1

- [ ] T030 [P] [US1] Implement provider interface and deterministic test-provider contract in `backend/app/modules/ai_insights/providers/base.py`
- [ ] T031 [P] [US1] Implement configured provider factory with settings-based selection in `backend/app/modules/ai_insights/providers/configured.py`
- [ ] T032 [US1] Implement daily and weekly instruction selection with stable instruction versions in `backend/app/modules/ai_insights/services/ai_instruction_service.py`
- [ ] T033 [US1] Implement privacy-bounded daily/weekly input preparation and aggregate input summaries in `backend/app/modules/ai_insights/services/ai_input_service.py`
- [ ] T034 [US1] Extend AI run repository for source links, owner-scoped get, idempotency lookup, in-flight lookup, and current-result candidate queries in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [ ] T035 [US1] Extend AI run service for create-run validation, period bounds, source links, output outcome `no_data`, instruction metadata, and idempotency reuse in `backend/app/modules/ai_insights/services/ai_insight_run_service.py`
- [ ] T036 [US1] Implement AI analysis orchestration for generated summaries and stored outputs in `backend/app/modules/ai_insights/services/ai_analysis_service.py`
- [ ] T037 [US1] Implement thin Celery task wrapper for `ai_insights.process_analysis_run` in `backend/app/workers/tasks/ai_analysis_tasks.py`
- [ ] T038 [US1] Extend AI insight dependency wiring for input, instruction, provider, run, and analysis services in `backend/app/modules/ai_insights/dependencies.py`
- [ ] T039 [US1] Implement `POST /api/v1/ai-insights/runs` and `GET /api/v1/ai-insights/runs/{ai_insight_run_id}` with standard envelopes in `backend/app/modules/ai_insights/router.py`
- [ ] T040 [US1] Add request-id and `ai_insight_run_id` structured logging for create and worker execution in `backend/app/modules/ai_insights/services/ai_analysis_service.py`
- [ ] T041 [US1] Update AI insight module README with Phase 4 summary generation ownership and privacy boundaries in `backend/app/modules/ai_insights/README.md`

**Checkpoint**: User Story 1 is independently testable as the MVP analysis flow for daily/weekly summaries, no-data outcomes, stored outputs, and result retrieval.

---

## Phase 4: User Story 2 - Detect Patterns and Behavior Insights (Priority: P2)

**Goal**: Validate and store combined outputs containing detected patterns, neutral behavior insights, supporting evidence, and limitations without unsupported claims or note text.

**Independent Test**: Use seeded days and weeks with repeated categories, tags, task themes, uneven totals, and notes; verify generated observations include evidence references, omit unsupported claims, and never include note text.

### Tests for User Story 2

- [ ] T042 [P] [US2] Add output validator tests for required sections, evidence references, unsupported claims, and malformed output rejection in `backend/tests/domain/test_ai_analysis_output_validation.py`
- [ ] T043 [P] [US2] Add behavior insight and pattern service tests for repeated categories, tags, task themes, uneven daily totals, and no strong pattern cases in `backend/tests/services/test_ai_analysis_service.py`
- [ ] T044 [P] [US2] Add provider-output note-redaction and evidence integrity tests in `backend/tests/services/test_ai_output_validator.py`
- [ ] T045 [P] [US2] Add API run detail tests for combined output sections and supporting evidence serialization in `backend/tests/api/test_ai_insight_api.py`

### Implementation for User Story 2

- [ ] T046 [P] [US2] Add combined analysis output, observation, supporting evidence, and limitation schemas in `backend/app/modules/ai_insights/schemas.py`
- [ ] T047 [US2] Implement output validation for required sections, evidence IDs, output outcome, generated timestamp, and note-text exclusion in `backend/app/modules/ai_insights/services/ai_output_validator.py`
- [ ] T048 [US2] Extend instruction templates to require summary, detected patterns, behavior insights, supporting evidence, limitations, and generated timestamp in `backend/app/modules/ai_insights/services/ai_instruction_service.py`
- [ ] T049 [US2] Extend AI analysis orchestration to validate provider output, reject malformed output, and store only validated combined outputs in `backend/app/modules/ai_insights/services/ai_analysis_service.py`
- [ ] T050 [US2] Extend repository serialization support for output outcome and combined output summary fields in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [ ] T051 [US2] Ensure API run detail responses expose combined output sections and do not expose full structured input payloads in `backend/app/modules/ai_insights/router.py`
- [ ] T052 [US2] Update AI insight README with pattern detection, behavior insight, evidence, and limitation rules in `backend/app/modules/ai_insights/README.md`

**Checkpoint**: User Stories 1 and 2 are independently testable; combined outputs contain validated summaries, patterns, insights, evidence, and limitations without note leakage.

---

## Phase 5: User Story 3 - Track AI Runs and Failures (Priority: P3)

**Goal**: Review AI run status/history/current results, rerun analysis, preserve previous runs, retry transient failures up to 3 total attempts, and expose traceable failure details.

**Independent Test**: Start successful, no-data, failed, retried, and rerun analyses; verify status, timing, source references, current-result selection, history pagination, retry counts, and failure details.

### Tests for User Story 3

- [ ] T053 [P] [US3] Add AI run lifecycle tests for status transitions, retry count, final failed status, and failure details in `backend/tests/domain/test_ai_insight_run_lifecycle.py`
- [ ] T054 [P] [US3] Add idempotency and in-flight conflict tests in `backend/tests/services/test_ai_run_idempotency.py`
- [ ] T055 [P] [US3] Add run history, current-result, and rerun repository tests in `backend/tests/repositories/test_ai_analysis_repository.py`
- [ ] T056 [P] [US3] Add run history pagination, current-result, run detail, and rerun API success tests in `backend/tests/api/test_ai_insight_api.py`
- [ ] T057 [P] [US3] Add AI API not-found, invalid period, conflict, auth, permission, pagination, and rate-limit error tests in `backend/tests/api/test_ai_insight_api_errors.py`
- [ ] T058 [P] [US3] Add worker retry and exhausted-failure delegation tests in `backend/tests/workers/test_ai_analysis_worker.py`

### Implementation for User Story 3

- [ ] T059 [P] [US3] Add run history filter, current-result, rerun, and page response schemas in `backend/app/modules/ai_insights/schemas.py`
- [ ] T060 [US3] Extend repository methods for paginated history, current completed result, rerun source lookup, in-flight conflict lookup, and retry metadata updates in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [ ] T061 [US3] Extend AI run service for rerun creation, current-result selection, history filters, pagination validation, and owner-scoped not-found handling in `backend/app/modules/ai_insights/services/ai_insight_run_service.py`
- [ ] T062 [US3] Extend AI analysis service for transient failure classification, 3-attempt retry loop, failure detail recording, and exhausted-failure terminal state in `backend/app/modules/ai_insights/services/ai_analysis_service.py`
- [ ] T063 [US3] Extend worker task to delegate retries and failure persistence without duplicating business rules in `backend/app/workers/tasks/ai_analysis_tasks.py`
- [ ] T064 [US3] Implement `GET /api/v1/ai-insights/runs`, `GET /api/v1/ai-insights/runs/current`, and `POST /api/v1/ai-insights/runs/{ai_insight_run_id}/rerun` in `backend/app/modules/ai_insights/router.py`
- [ ] T065 [US3] Add pagination defaults, max limits, auth scopes, idempotency header handling, and conflict responses to AI insight endpoints in `backend/app/modules/ai_insights/router.py`
- [ ] T066 [US3] Add status transition, retry count, output outcome, and failure detail structured logs in `backend/app/modules/ai_insights/services/ai_analysis_service.py`

**Checkpoint**: All Phase 4 user stories are independently functional and AI runs are requestable, reviewable, rerunnable, retryable, and traceable through versioned APIs.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, contracts, and out-of-scope boundaries across the completed Phase 4 AI analysis engine.

- [ ] T067 [P] Update AI insights API contract examples after implementation in `specs/005-ai-analysis-engine/contracts/ai-insights-api.yaml`
- [ ] T068 [P] Update Phase 4 implementation notes in `docs/FOUNDATION.md`
- [ ] T069 [P] Update worker documentation for AI analysis task behavior in `backend/app/workers/README.md`
- [ ] T070 [P] Update AI settings documentation in `backend/app/settings/README.md`
- [ ] T071 Run backend Phase 4 tests documented in `specs/005-ai-analysis-engine/quickstart.md`
- [ ] T072 Run the manual smoke flow from `specs/005-ai-analysis-engine/quickstart.md`
- [ ] T073 Review `backend/app/modules/ai_insights/router.py`, `backend/app/modules/ai_insights/services/ai_analysis_service.py`, `backend/app/modules/ai_insights/services/ai_input_service.py`, `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`, and `backend/app/workers/tasks/ai_analysis_tasks.py` for Router -> Service -> Repository -> Database and thin-worker boundary compliance
- [ ] T074 Verify all handled AI insight API responses use standard success/error envelopes across `backend/app/modules/ai_insights/router.py` and `backend/app/core/exceptions.py`
- [ ] T075 Verify AI inputs and outputs exclude note text by reviewing `backend/app/modules/ai_insights/services/ai_input_service.py`, `backend/app/modules/ai_insights/services/ai_output_validator.py`, and `backend/app/modules/ai_insights/services/ai_analysis_service.py`
- [ ] T076 Verify full structured AI input payloads are not persisted by reviewing `backend/app/modules/ai_insights/models.py`, `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`, and `backend/alembic/versions/005_ai_analysis_engine.py`
- [ ] T077 Verify Phase 4 does not add dashboard visualization changes, productivity scores, recommendations, scheduled automation, AI chat, report export, or Notion API synchronization by scanning `backend/app/modules/ai_insights/`, `backend/app/modules/analytics/`, `frontend/features/`, and `backend/app/workers/tasks/`
- [ ] T078 Run focused static validation for `backend/app/modules/ai_insights/router.py`, `backend/app/modules/ai_insights/services/ai_analysis_service.py`, `backend/app/modules/ai_insights/services/ai_input_service.py`, `backend/app/modules/ai_insights/services/ai_instruction_service.py`, `backend/app/modules/ai_insights/services/ai_output_validator.py`, and `backend/app/workers/tasks/ai_analysis_tasks.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and can validate combined output behavior using seeded runs and fake provider output.
- **User Story 3 (Phase 5)**: Depends on Foundational and AI run persistence; it can be tested with seeded AI runs and fake provider failures.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Generate Daily and Weekly Summaries**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Detect Patterns and Behavior Insights**: Starts after Foundational; builds on the combined output shape from US1 but can be validated independently with direct validator/service tests.
- **US3 - Track AI Runs and Failures**: Starts after Foundational; uses shared run lifecycle and can be validated independently with seeded runs and fake provider failures.

### Within Each User Story

- Tests are written before implementation.
- Schemas/constants/exceptions before repositories and services.
- Models and migrations before repository persistence changes.
- Repositories before services.
- Services before endpoints and worker tasks.
- Dependency providers before router wiring.
- Exception/status mappings before endpoint error handling.
- Pagination contract before list endpoint implementation.
- Idempotency and retry rules before worker execution behavior.
- Worker tasks stay thin and delegate to services.

---

## Parallel Opportunities

- T002, T003, T004, T005, and T006 can run in parallel after T001 is understood.
- T007, T008, and T009 can run in parallel before their implementation tasks.
- T010, T013, T014, T017, T019, and T020 touch different files and can be split after foundational test expectations are known.
- US1 tests T023-T029 can run in parallel.
- US1 provider tasks T030-T031 can run in parallel with instruction/input service tasks T032-T033 after constants are available.
- US2 tests T042-T045 can run in parallel.
- US2 schema task T046 can run in parallel with instruction update task T048 after output contract is understood.
- US3 tests T053-T058 can run in parallel.
- US3 schema task T059 can run in parallel with repository task T060 after the history contract is understood.
- Polish documentation tasks T067-T070 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "T023 Add AI input service tests in backend/tests/services/test_ai_input_service.py"
Task: "T024 Add AI run creation and no-data service tests in backend/tests/services/test_ai_analysis_service.py"
Task: "T025 Add deterministic provider and instruction service tests in backend/tests/services/test_ai_instruction_service.py"
Task: "T026 Add AI run repository tests in backend/tests/repositories/test_ai_analysis_repository.py"
Task: "T027 Add create-run API success tests in backend/tests/api/test_ai_insight_api.py"
Task: "T029 Add AI analysis worker tests in backend/tests/workers/test_ai_analysis_worker.py"
```

## Parallel Example: User Story 2

```text
Task: "T042 Add output validator tests in backend/tests/domain/test_ai_analysis_output_validation.py"
Task: "T043 Add behavior insight and pattern service tests in backend/tests/services/test_ai_analysis_service.py"
Task: "T044 Add provider-output note-redaction tests in backend/tests/services/test_ai_output_validator.py"
Task: "T045 Add API run detail tests in backend/tests/api/test_ai_insight_api.py"
Task: "T046 Add combined analysis output schemas in backend/app/modules/ai_insights/schemas.py"
```

## Parallel Example: User Story 3

```text
Task: "T053 Add AI run lifecycle tests in backend/tests/domain/test_ai_insight_run_lifecycle.py"
Task: "T054 Add idempotency and in-flight conflict tests in backend/tests/services/test_ai_run_idempotency.py"
Task: "T055 Add run history and current-result repository tests in backend/tests/repositories/test_ai_analysis_repository.py"
Task: "T056 Add history/current/rerun API success tests in backend/tests/api/test_ai_insight_api.py"
Task: "T058 Add worker retry tests in backend/tests/workers/test_ai_analysis_worker.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup tasks T001-T006.
2. Complete Phase 2 foundational tasks T007-T022.
3. Complete US1 tasks T023-T041.
4. Stop and validate daily/weekly summary generation independently with US1 tests and the quickstart smoke checks.

### Incremental Delivery

1. Setup + Foundational create settings, persistence metadata, constants, errors, schemas, auth scopes, and API composition.
2. US1 delivers requestable daily/weekly analysis, no-data outcomes, stored summary output, worker execution, and run retrieval.
3. US2 adds validated pattern detection, behavior insights, supporting evidence, limitations, and note-text exclusion checks.
4. US3 adds history, current result, rerun, retry, idempotency, and failure traceability APIs.
5. Polish verifies contracts, response shapes, AI isolation, privacy boundaries, input non-retention, and out-of-scope exclusions.

### Scope Guardrails

- Do not add CSV import behavior.
- Do not add dashboard visualization changes or frontend AI insight UI.
- Do not add productivity scores, consistency scores, best/worst day labels, or recommendations.
- Do not add scheduled AI runs, AI chat, report export, or Notion API synchronization.
- Keep AI provider orchestration, instructions, validation, and outputs inside `backend/app/modules/ai_insights/`.
- Keep source daily logs, tasks, notes, categories, tags, imports, and import outcomes authoritative and unmutated by AI output.
