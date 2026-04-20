# Tasks: Insights & Recommendations

**Input**: Design documents from `/specs/006-insights-recommendations/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/insights-recommendations-api.yaml](./contracts/insights-recommendations-api.yaml), [quickstart.md](./quickstart.md)

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Frontend runtime work MUST include focused component/hook tests plus build validation. Write tests before implementation for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create Phase 5 backend/frontend placeholders and test package scaffolding needed before implementation begins.

- [X] T001 Create Phase 5 backend service placeholders in `backend/app/modules/ai_insights/services/insight_generation_service.py`, `backend/app/modules/ai_insights/services/insight_source_service.py`, `backend/app/modules/ai_insights/services/productivity_scoring_service.py`, `backend/app/modules/ai_insights/services/consistency_scoring_service.py`, `backend/app/modules/ai_insights/services/day_ranking_service.py`, `backend/app/modules/ai_insights/services/recommendation_service.py`, `backend/app/modules/ai_insights/services/insight_validation_service.py`, and `backend/app/modules/ai_insights/services/insight_result_service.py`
- [X] T002 [P] Create Phase 5 result repository placeholder in `backend/app/modules/ai_insights/repositories/ai_insight_result_repository.py`
- [X] T003 [P] Create Phase 5 frontend feature folders and package markers in `frontend/features/ai-insights/hooks/.gitkeep` and `frontend/features/ai-insights/components/.gitkeep`
- [X] T004 [P] Create Phase 5 test package markers in `backend/tests/domain/__init__.py`, `backend/tests/services/__init__.py`, `backend/tests/repositories/__init__.py`, `backend/tests/api/__init__.py`, `backend/tests/migrations/__init__.py`, and `frontend/features/ai-insights/components/.gitkeep`
- [X] T005 [P] Add Phase 5 implementation notes and deterministic-generation guardrails to `backend/app/modules/ai_insights/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared persistence, schemas, constants, errors, repository contracts, dependency wiring, and frontend API foundations required by all insight stories.

**CRITICAL**: No user story work can begin until this phase is complete.

- [X] T006 [P] Add migration tests for `AIInsightResult` and `AIInsightResultSource` tables, indexes, JSON fields, soft delete, and current-result constraints in `backend/tests/migrations/test_insight_results_migration.py`
- [X] T007 [P] Add model tests for Phase 5 result fields, source relationships, status values, and soft-delete defaults in `backend/tests/domain/test_ai_insight_results.py`
- [X] T008 [P] Add exception mapping tests for missing analysis, invalid source analysis, result validation failure, idempotency conflict, and result not found in `backend/tests/api/test_ai_insight_results_api_errors.py`
- [X] T009 Define Phase 5 constants for period granularity, result status, score state, confidence, generation reason, validator version, pagination defaults, and rate-limit names in `backend/app/modules/ai_insights/constants.py`
- [X] T010 Define Phase 5 custom exceptions for invalid insight period, missing source analysis, invalid source analysis, insight result not found, generation conflict, and insight validation failure in `backend/app/modules/ai_insights/exceptions.py`
- [X] T011 Add Phase 5 exception mappings to unified error handling in `backend/app/core/exceptions.py`
- [X] T012 Add or verify `ai_insights:read` and `ai_insights:write` scope support for Phase 5 endpoints in `backend/app/api/dependencies.py`
- [X] T013 Extend AI insights ORM models with `AIInsightResult` and `AIInsightResultSource` in `backend/app/modules/ai_insights/models.py`
- [X] T014 Add Alembic migration for Phase 5 insight result tables, source links, JSON payload columns, indexes, current marker, and soft delete in `backend/alembic/versions/006_insights_recommendations.py`
- [X] T015 Define base Phase 5 schemas for insight period requests, result status, source snapshot, score outcome, score factor, evidence, validation outcome, and paginated result responses in `backend/app/modules/ai_insights/schemas.py`
- [X] T016 Implement base result repository methods for create, get by owner, current lookup, source links, default-generation reuse lookup, current marker updates, soft-delete exclusion, and paginated history in `backend/app/modules/ai_insights/repositories/ai_insight_result_repository.py`
- [X] T017 Extend AI insight run repository methods for completed source analysis lookup by owner, period, granularity, and optional run ID in `backend/app/modules/ai_insights/repositories/ai_insight_run_repository.py`
- [X] T018 Wire Phase 5 repository and service dependency providers in `backend/app/modules/ai_insights/dependencies.py`
- [X] T019 Register Phase 5 route placeholders under the existing `/api/v1/ai-insights` router composition in `backend/app/modules/ai_insights/router.py` and `backend/app/api/router.py`
- [X] T020 [P] Define frontend Zod schemas and TypeScript types for Phase 5 API payloads in `frontend/features/ai-insights/schemas.ts`
- [X] T021 [P] Define frontend query keys for current result, result detail, generate mutation, rerun mutation, and history list in `frontend/features/ai-insights/query-keys.ts`
- [X] T022 [P] Implement Phase 5 API client functions for generate, current, detail, rerun, and history endpoints in `frontend/features/ai-insights/api.ts`

**Checkpoint**: Persistence, contracts, errors, dependency wiring, and frontend API foundations are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Review Explainable Scores (Priority: P1) MVP

**Goal**: Generate or reuse a day/week insight result with productivity and consistency score outcomes, explanations, evidence, validation, source analysis traceability, and later review.

**Independent Test**: Generate insights for a week with completed Phase 4 output and saved records, then verify productivity and consistency scores are bounded or explicitly insufficient, explained, evidence-backed, stored, current, and reviewable.

### Tests for User Story 1

- [X] T023 [P] [US1] Add source service tests for daily/weekly period resolution, completed Phase 4 source analysis lookup, stale-source visibility, saved-fact authority, and note-text exclusion in `backend/tests/services/test_insight_source_service.py`
- [X] T024 [P] [US1] Add productivity scoring tests for valid numeric score, insufficient data, positive/limiting factors, evidence count, score bounds, and no-data output in `backend/tests/domain/test_insight_scoring_rules.py`
- [X] T025 [P] [US1] Add consistency scoring tests for weekly scored state, daily not-applicable state, fewer-than-three-days insufficient state, and evidence-backed explanation in `backend/tests/domain/test_insight_scoring_rules.py`
- [X] T026 [P] [US1] Add insight result repository tests for create, source links, current lookup, owner-scoped detail, default-generation reuse, and soft-delete exclusion in `backend/tests/repositories/test_ai_insight_result_repository.py`
- [X] T027 [P] [US1] Add generation service tests for default reuse, source snapshot creation, score validation, failed validation not current, and current marker behavior in `backend/tests/services/test_insight_generation_service.py`
- [X] T028 [P] [US1] Add privacy boundary service tests ensuring task note text is excluded from source snapshots, evidence, explanations, and stored payloads in `backend/tests/services/test_insight_privacy_boundary.py`
- [X] T029 [P] [US1] Add generate/current/detail API success envelope tests for scored, insufficient-data, no-data, and reused-existing responses in `backend/tests/api/test_ai_insight_results_api.py`
- [X] T030 [P] [US1] Add generate/current/detail API error tests for invalid period, missing analysis, failed source analysis, malformed source analysis, auth, permission, validation failure, and rate-limit envelopes in `backend/tests/api/test_ai_insight_results_api_errors.py`
- [X] T031 [P] [US1] Add frontend tests for period selection, score explanations, insufficient-data display, evidence rendering, and reused-current messaging in `frontend/features/ai-insights/components/InsightScores.test.tsx`

### Implementation for User Story 1

- [X] T032 [P] [US1] Implement completed source analysis resolution, source tracking summary, source task/evidence extraction, and note-text exclusion in `backend/app/modules/ai_insights/services/insight_source_service.py`
- [X] T033 [P] [US1] Implement productivity score rules, positive/limiting factor generation, insufficient-data reasons, confidence, and evidence IDs in `backend/app/modules/ai_insights/services/productivity_scoring_service.py`
- [X] T034 [P] [US1] Implement consistency score rules for daily not-applicable, weekly scored state, fewer-than-three-days insufficient state, confidence, and evidence IDs in `backend/app/modules/ai_insights/services/consistency_scoring_service.py`
- [X] T035 [US1] Implement score, evidence, source-period, privacy-boundary, and current-result validation checks in `backend/app/modules/ai_insights/services/insight_validation_service.py`
- [X] T036 [US1] Implement default deterministic result generation, validation, source link persistence, failed-result handling, and current marker assignment in `backend/app/modules/ai_insights/services/insight_generation_service.py`
- [X] T037 [US1] Implement current result lookup, detail lookup, default-generation reuse, and owner-scoped not-found behavior in `backend/app/modules/ai_insights/services/insight_result_service.py`
- [X] T038 [US1] Extend result schemas for generate request/response, current result response, detail response, score outcomes, source snapshot, evidence, and validation outcome in `backend/app/modules/ai_insights/schemas.py`
- [X] T039 [US1] Implement `POST /api/v1/ai-insights/results/generate`, `GET /api/v1/ai-insights/results/current`, and `GET /api/v1/ai-insights/results/{insight_result_id}` with standard envelopes in `backend/app/modules/ai_insights/router.py`
- [X] T040 [US1] Add request-id, owner, period, source analysis, result ID, validation status, and reused-existing structured logs in `backend/app/modules/ai_insights/services/insight_generation_service.py`
- [X] T041 [US1] Implement frontend current result, generate mutation, and detail hooks in `frontend/features/ai-insights/hooks/use-current-insight-result.ts` and `frontend/features/ai-insights/hooks/use-generate-insight-result.ts`
- [X] T042 [P] [US1] Implement period picker for supported day/week periods only in `frontend/features/ai-insights/components/InsightPeriodPicker.tsx`
- [X] T043 [P] [US1] Implement score explanation UI for numeric, insufficient-data, and not-applicable states in `frontend/features/ai-insights/components/ScoreExplanation.tsx`
- [X] T044 [P] [US1] Implement evidence list UI that shows source facts and source analysis references without note text in `frontend/features/ai-insights/components/EvidenceList.tsx`
- [X] T045 [US1] Compose the MVP insights review page with period picker, generate action, current result, scores, evidence, empty states, and source analysis traceability in `frontend/app/dashboard/ai-insights/page.tsx`

**Checkpoint**: User Story 1 is independently testable as the MVP score-generation and review flow.

---

## Phase 4: User Story 2 - Understand Best and Worst Days (Priority: P2)

**Goal**: Identify relative best and worst days for weekly results when enough tracked days exist, explain ties or low-confidence comparisons, and keep weak-day language neutral.

**Independent Test**: Generate insights for a seeded week with varied daily totals, categories, tags, task volume, and Phase 4 observations, then verify best/worst day findings are relative, evidence-backed, neutral, and omitted or qualified when comparison is unreliable.

### Tests for User Story 2

- [X] T046 [P] [US2] Add day ranking service tests for best day, worst day, tie or close ranking, no meaningful distinction, single outlier, and fewer-than-three-days behavior in `backend/tests/domain/test_day_ranking_rules.py`
- [X] T047 [P] [US2] Add validation tests for weekly day-finding evidence references, neutral worst-day language, daily-period omission, and unsupported broad recommendation prevention in `backend/tests/domain/test_day_ranking_rules.py`
- [X] T048 [P] [US2] Add API tests for weekly best/worst day payloads, omitted findings, tie explanations, and standard response envelopes in `backend/tests/api/test_ai_insight_results_api.py`
- [X] T049 [P] [US2] Add frontend DayFindings rendering tests for best/worst labels, neutral wording, omitted states, and tie explanations in `frontend/features/ai-insights/components/DayFindings.test.tsx`

### Implementation for User Story 2

- [X] T050 [P] [US2] Implement weekly day ranking rules, tie detection, no-meaningful-distinction detection, outlier handling, and neutral summaries in `backend/app/modules/ai_insights/services/day_ranking_service.py`
- [X] T051 [US2] Extend validation checks for best/worst day evidence, daily omission, three-tracked-day minimum, neutral language, and meaningful distinction in `backend/app/modules/ai_insights/services/insight_validation_service.py`
- [X] T052 [US2] Integrate day ranking into deterministic generation after scoring and before result validation in `backend/app/modules/ai_insights/services/insight_generation_service.py`
- [X] T053 [US2] Extend schemas for best day, worst day, no-meaningful-distinction, tie flags, and day-finding confidence in `backend/app/modules/ai_insights/schemas.py`
- [X] T054 [US2] Ensure result detail, current result, and generate responses serialize day findings consistently in `backend/app/modules/ai_insights/router.py`
- [X] T055 [US2] Implement day findings UI for weekly best/worst findings, omitted states, tie explanations, and neutral weak-day copy in `frontend/features/ai-insights/components/DayFindings.tsx`
- [X] T056 [US2] Integrate day findings into the insights review page below score explanations in `frontend/app/dashboard/ai-insights/page.tsx`

**Checkpoint**: User Stories 1 and 2 are independently testable; weekly insights can explain relative day comparisons without overstating differences.

---

## Phase 5: User Story 3 - Receive Low-Noise Recommendations (Priority: P3)

**Goal**: Produce 0-3 prioritized, actionable, non-duplicative recommendations tied to scores, day findings, Phase 4 observations, and evidence, with explicit rerun/history behavior for later review.

**Independent Test**: Generate recommendations for seeded periods with clear patterns, weak patterns, repeated prior recommendations, and insufficient data, then verify concise recommendations are evidence-backed, actionable, non-generic, non-duplicative, stored, current, and reviewable in history.

### Tests for User Story 3

- [X] T057 [P] [US3] Add recommendation service tests for actionability, evidence requirements, priority ordering, confidence, expected benefit, omitted unsupported themes, and max-three cap in `backend/tests/domain/test_recommendation_validation.py`
- [X] T058 [P] [US3] Add duplicate/generic/medical/character-claim validation tests in `backend/tests/domain/test_recommendation_validation.py`
- [X] T059 [P] [US3] Add recommendation generation service tests for links to score factors, day findings, Phase 4 observations, dedupe keys, and no useful recommendation states in `backend/tests/services/test_insight_generation_service.py`
- [X] T060 [P] [US3] Add result idempotency and rerun tests for default reuse, explicit rerun new history, latest successful current marker, and prior result preservation in `backend/tests/services/test_insight_result_idempotency.py`
- [X] T061 [P] [US3] Add paginated history repository tests for newest-first ordering, filters, current marker, failed result exclusion from current, and soft-delete exclusion in `backend/tests/repositories/test_ai_insight_result_repository.py`
- [X] T062 [P] [US3] Add API tests for rerun, history pagination, recommendation payloads, duplicate prevention, and result detail review in `backend/tests/api/test_ai_insight_results_api.py`
- [X] T063 [P] [US3] Add frontend tests for recommendations, no-recommendation state, rerun action, result history, source period, and source analysis reference in `frontend/features/ai-insights/components/RecommendationAndHistory.test.tsx`

### Implementation for User Story 3

- [X] T064 [P] [US3] Implement recommendation generation rules, priority ordering, confidence assignment, expected benefit text, source links, and dedupe keys in `backend/app/modules/ai_insights/services/recommendation_service.py`
- [X] T065 [US3] Extend validation checks for recommendation count, actionability, user-controlled actions, evidence, duplicate/generic wording, medical claims, character claims, and unsupported claims in `backend/app/modules/ai_insights/services/insight_validation_service.py`
- [X] T066 [US3] Integrate recommendation generation into deterministic generation after scoring and day findings in `backend/app/modules/ai_insights/services/insight_generation_service.py`
- [X] T067 [US3] Extend result service for explicit rerun creation, previous-current clearing, latest-successful current marker, history filters, and pagination validation in `backend/app/modules/ai_insights/services/insight_result_service.py`
- [X] T068 [US3] Extend result repository methods for explicit rerun persistence, paginated history filters, dedupe-key history lookup, previous-current clearing, and failed-result history records in `backend/app/modules/ai_insights/repositories/ai_insight_result_repository.py`
- [X] T069 [US3] Extend schemas for recommendation, recommendation source links, rerun response, history filters, and paginated result page in `backend/app/modules/ai_insights/schemas.py`
- [X] T070 [US3] Implement `POST /api/v1/ai-insights/results/{insight_result_id}/rerun` and `GET /api/v1/ai-insights/results` with page/limit pagination and standard envelopes in `backend/app/modules/ai_insights/router.py`
- [X] T071 [US3] Add explicit rerun, history pagination, recommendation validation, dedupe decision, and current marker structured logs in `backend/app/modules/ai_insights/services/insight_result_service.py`
- [X] T072 [US3] Implement frontend result history and rerun hooks in `frontend/features/ai-insights/hooks/use-insight-result-history.ts` and `frontend/features/ai-insights/hooks/use-rerun-insight-result.ts`
- [X] T073 [P] [US3] Implement recommendation list UI with action, rationale, expected benefit, confidence, priority, source links, and no-recommendation state in `frontend/features/ai-insights/components/RecommendationList.tsx`
- [X] T074 [P] [US3] Implement insight history list UI with current marker, generated timestamp, source period, source analysis reference, and rerun action in `frontend/features/ai-insights/components/InsightHistoryList.tsx`
- [X] T075 [US3] Integrate recommendations, history, and explicit rerun behavior into the insights review page in `frontend/app/dashboard/ai-insights/page.tsx`

**Checkpoint**: All Phase 5 user stories are independently functional and insights are scoreable, comparable, recommendable, rerunnable, traceable, and reviewable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, contracts, tests, and out-of-scope boundaries across Phase 5.

- [X] T076 [P] Update API contract examples after implementation in `specs/006-insights-recommendations/contracts/insights-recommendations-api.yaml`
- [X] T077 [P] Update quickstart implementation checks after final endpoint/component names settle in `specs/006-insights-recommendations/quickstart.md`
- [X] T078 [P] Update AI insights module documentation for Phase 5 scoring, day findings, recommendations, history, privacy, and deterministic-generation ownership in `backend/app/modules/ai_insights/README.md`
- [X] T079 [P] Update frontend AI insights feature documentation for review flow and supported day/week periods in `frontend/features/ai-insights/README.md`
- [X] T080 Run targeted backend Phase 5 tests from `specs/006-insights-recommendations/quickstart.md`
- [X] T081 Run full backend test suite with `pytest -q` from `backend/`
- [X] T082 Run frontend tests with `npm run test` from `frontend/`
- [X] T083 Run frontend production build with `npm run build` from `frontend/`
- [ ] T084 Run the manual API and frontend smoke checks from `specs/006-insights-recommendations/quickstart.md`
- [X] T085 Review `backend/app/modules/ai_insights/router.py`, `backend/app/modules/ai_insights/services/insight_generation_service.py`, `backend/app/modules/ai_insights/services/insight_result_service.py`, and `backend/app/modules/ai_insights/repositories/ai_insight_result_repository.py` for Router -> Service -> Repository -> Database boundary compliance
- [X] T086 Verify all handled Phase 5 API responses use standard success/error envelopes across `backend/app/modules/ai_insights/router.py` and `backend/app/core/exceptions.py`
- [X] T087 Verify Phase 5 excludes note text from source snapshots, evidence, score explanations, day findings, recommendations, and frontend rendering across `backend/app/modules/ai_insights/services/`, `backend/app/modules/ai_insights/schemas.py`, and `frontend/features/ai-insights/`
- [X] T088 Verify Phase 5 does not add new AI provider calls, scheduled automation, CSV import behavior, dashboard redesign, report export, Notion synchronization, AI chat, month insight periods, or custom date ranges across `backend/app/modules/ai_insights/`, `backend/app/workers/tasks/`, and `frontend/features/ai-insights/`
- [X] T089 Verify current-result idempotency, explicit rerun history, soft-delete exclusion, pagination, auth scopes, rate limits, and structured logging by reviewing `backend/app/modules/ai_insights/services/insight_result_service.py`, `backend/app/modules/ai_insights/repositories/ai_insight_result_repository.py`, and `backend/app/modules/ai_insights/router.py`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and can be tested independently with seeded weekly source snapshots.
- **User Story 3 (Phase 5)**: Depends on Foundational and can be tested independently with seeded score/day-finding/evidence payloads.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Review Explainable Scores**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Understand Best and Worst Days**: Starts after Foundational; uses shared evidence/source snapshot shape from US1 but day-ranking rules can be tested directly.
- **US3 - Receive Low-Noise Recommendations**: Starts after Foundational; integrates with scores/day findings when available but recommendation validation can be tested directly with seeded evidence and source links.

### Within Each User Story

- Tests are written before implementation.
- Constants, exceptions, models, migrations, and schemas before repositories and services.
- Repositories before services.
- Services before endpoints.
- Dependency providers before router wiring.
- Backend API schemas before frontend schemas and API hooks.
- Frontend API hooks before consuming components.
- Components before route/page composition.
- Story complete before moving to next priority.

---

## Parallel Opportunities

- T002, T003, T004, and T005 can run in parallel after T001 is understood.
- T006, T007, and T008 can run in parallel before foundational implementation.
- T009, T010, T013, T015, T020, T021, and T022 touch different files and can be split after foundational test expectations are known.
- US1 tests T023-T031 can run in parallel.
- US1 scoring/source service tasks T032-T034 can run in parallel after foundational schemas/constants exist.
- US1 frontend component tasks T042-T044 can run in parallel after API hooks are available.
- US2 tests T046-T049 can run in parallel.
- US2 backend day-ranking task T050 can run in parallel with frontend test task T049 after the payload contract is understood.
- US3 tests T057-T063 can run in parallel.
- US3 frontend component tasks T073-T074 can run in parallel after hooks are available.
- Polish documentation tasks T076-T079 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "T023 Add source service tests in backend/tests/services/test_insight_source_service.py"
Task: "T024 Add productivity scoring tests in backend/tests/domain/test_insight_scoring_rules.py"
Task: "T025 Add consistency scoring tests in backend/tests/domain/test_insight_scoring_rules.py"
Task: "T026 Add result repository tests in backend/tests/repositories/test_ai_insight_result_repository.py"
Task: "T029 Add generate/current/detail API success tests in backend/tests/api/test_ai_insight_results_api.py"
Task: "T031 Add frontend score rendering tests in frontend/features/ai-insights/components/InsightScores.test.tsx"
```

## Parallel Example: User Story 2

```text
Task: "T046 Add day ranking service tests in backend/tests/domain/test_day_ranking_rules.py"
Task: "T047 Add day finding validation tests in backend/tests/domain/test_day_ranking_rules.py"
Task: "T048 Add day finding API tests in backend/tests/api/test_ai_insight_results_api.py"
Task: "T049 Add DayFindings rendering tests in frontend/features/ai-insights/components/DayFindings.test.tsx"
Task: "T050 Implement day ranking rules in backend/app/modules/ai_insights/services/day_ranking_service.py"
```

## Parallel Example: User Story 3

```text
Task: "T057 Add recommendation service tests in backend/tests/domain/test_recommendation_validation.py"
Task: "T060 Add result idempotency and rerun tests in backend/tests/services/test_insight_result_idempotency.py"
Task: "T061 Add paginated history repository tests in backend/tests/repositories/test_ai_insight_result_repository.py"
Task: "T062 Add rerun and history API tests in backend/tests/api/test_ai_insight_results_api.py"
Task: "T063 Add frontend recommendations and history tests in frontend/features/ai-insights/components/RecommendationAndHistory.test.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup tasks T001-T005.
2. Complete Phase 2 foundational tasks T006-T022.
3. Complete US1 tasks T023-T045.
4. Stop and validate score generation/review independently with backend tests, frontend component tests, and the quickstart API checks.

### Incremental Delivery

1. Setup + Foundational create result persistence, source analysis lookup, schemas, exceptions, dependency wiring, API contract foundations, and frontend API foundations.
2. US1 delivers deterministic productivity/consistency scores, evidence, source traceability, default idempotent generation, and current/detail review.
3. US2 adds weekly best/worst day findings, tie/low-confidence behavior, and neutral language safeguards.
4. US3 adds low-noise recommendations, explicit rerun history, paginated history review, dedupe behavior, and current-result preservation.
5. Polish verifies contracts, response shapes, privacy boundaries, deterministic-only behavior, frontend build, and out-of-scope exclusions.

### Scope Guardrails

- Do not add new AI provider calls for Phase 5 generation.
- Do not add month or custom date range insight periods.
- Do not add scheduled generation, CSV import behavior, dashboard redesign, report export, Notion synchronization, or AI chat.
- Do not mutate daily logs, tasks, notes, categories, tags, imports, or Phase 4 AI analysis runs.
- Keep business rules in services and persistence logic in repositories.
- Keep frontend route files limited to composition and server/client boundaries.
- Use TanStack Query for server state and avoid copying API data into global stores.
