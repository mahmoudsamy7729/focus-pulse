# Tasks: Dashboard Foundation

**Input**: Design documents from `/specs/004-dashboard-foundation/`  
**Prerequisites**: [plan.md](./plan.md), [spec.md](./spec.md), [research.md](./research.md), [data-model.md](./data-model.md), [contracts/dashboard-api.yaml](./contracts/dashboard-api.yaml)

**Tests**: Service changes MUST include unit tests. API endpoint changes MUST include integration tests. Frontend runtime work MUST include lint/build validation and focused UI behavior tests where a test runner is available.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with other marked tasks in the same phase because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: Maps task to a specific user story: `[US1]`, `[US2]`, or `[US3]`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create dashboard module/package scaffolding and bootstrap the frontend runtime required by Phase 3.

- [ ] T001 Create analytics backend package markers in `backend/app/modules/analytics/__init__.py`, `backend/app/modules/analytics/services/__init__.py`, and `backend/app/modules/analytics/repositories/__init__.py`
- [ ] T002 [P] Create dashboard backend test package markers in `backend/tests/services/__init__.py` and verify existing `backend/tests/api/__init__.py` and `backend/tests/repositories/__init__.py`
- [ ] T003 Create frontend package manifest with scripts and dependencies in `frontend/package.json`
- [ ] T004 [P] Create TypeScript configuration in `frontend/tsconfig.json`
- [ ] T005 [P] Create Next.js configuration in `frontend/next.config.ts`
- [ ] T006 [P] Create Tailwind and PostCSS configuration in `frontend/tailwind.config.ts` and `frontend/postcss.config.mjs`
- [ ] T007 [P] Create base frontend route and style files in `frontend/app/layout.tsx`, `frontend/app/page.tsx`, `frontend/app/globals.css`, and `frontend/app/dashboard/page.tsx`
- [ ] T008 [P] Create dashboard frontend folders in `frontend/features/analytics/components/`, `frontend/components/charts/`, and `frontend/components/layout/`
- [ ] T009 Update frontend skeleton documentation for Phase 3 runtime expectations in `frontend/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared backend and frontend foundations that all dashboard user stories depend on.

**CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T010 Add `analytics:read` and `daily_logs:read` scope support to current-owner dependency stubs in `backend/app/api/dependencies.py`
- [ ] T011 [P] Define analytics constants for period types, chart limits, empty-state codes, and rate-limit names in `backend/app/modules/analytics/constants.py`
- [ ] T012 [P] Define analytics custom exceptions for invalid period and dashboard data quality errors in `backend/app/modules/analytics/exceptions.py`
- [ ] T013 Add analytics and daily-log read exception mappings to unified error handling in `backend/app/core/exceptions.py`
- [ ] T014 [P] Add shared dashboard response and period schemas in `backend/app/modules/analytics/schemas.py`
- [ ] T015 [P] Add frontend API success/error envelope schemas and shared response types in `frontend/lib/api/types.ts`
- [ ] T016 Implement Axios API client with base URL and error-code preservation in `frontend/lib/api/client.ts`
- [ ] T017 Implement TanStack Query provider in `frontend/app/providers.tsx` and wire it from `frontend/app/layout.tsx`
- [ ] T018 [P] Implement dashboard frontend Zod schemas and TypeScript types from `dashboard-api.yaml` in `frontend/features/analytics/schemas.ts` and `frontend/features/analytics/types.ts`
- [ ] T019 [P] Implement shared hours-and-minutes formatting utility in `frontend/features/analytics/utils.ts`
- [ ] T020 Register placeholder analytics and daily-log routers in `backend/app/api/router.py` with no business logic in the API composition layer

**Checkpoint**: Backend response/error/auth foundations and frontend runtime foundations are ready. User story implementation can begin.

---

## Phase 3: User Story 1 - Review Productivity Overview (Priority: P1) MVP

**Goal**: Open a dashboard overview that defaults to the latest tracked day, supports day/week/month filters, shows summary cards, daily logs list, period timeline data, and clear empty states.

**Independent Test**: Open `/dashboard` with seeded tracking records, change day/week/month filters, and verify summary cards, daily log list, period timeline, and empty states match the selected period.

### Tests for User Story 1

- [ ] T021 [P] [US1] Add dashboard period resolution and latest tracked day service tests in `backend/tests/services/test_dashboard_service.py`
- [ ] T022 [P] [US1] Add dashboard repository tests for latest tracked day, daily totals, task counts, and soft-delete exclusion in `backend/tests/repositories/test_dashboard_repository.py`
- [ ] T023 [P] [US1] Add dashboard overview API success envelope and default latest tracked day tests in `backend/tests/api/test_dashboard_api.py`
- [ ] T024 [P] [US1] Add dashboard overview API invalid period, auth, permission, and rate-limit error envelope tests in `backend/tests/api/test_dashboard_api_errors.py`
- [ ] T025 [P] [US1] Add dashboard frontend filter, empty-state, and summary rendering tests in `frontend/features/analytics/components/DashboardOverview.test.tsx`

### Implementation for User Story 1

- [ ] T026 [P] [US1] Implement dashboard overview response schemas, summary schemas, daily log list item schemas, period timeline schemas, and empty-state schemas in `backend/app/modules/analytics/schemas.py`
- [ ] T027 [US1] Implement dashboard repository queries for latest tracked day, date-bounded daily totals, task counts, and active-record filtering in `backend/app/modules/analytics/repositories/dashboard_repository.py`
- [ ] T028 [US1] Implement dashboard service period resolution for day, Monday-to-Sunday week, full month, latest tracked day fallback, and no-data empty state in `backend/app/modules/analytics/services/dashboard_service.py`
- [ ] T029 [US1] Implement dashboard service summary cards, average per logged day, daily log list, and week/month daily timeline composition in `backend/app/modules/analytics/services/dashboard_service.py`
- [ ] T030 [US1] Wire analytics repository and service providers in `backend/app/modules/analytics/dependencies.py`
- [ ] T031 [US1] Implement `GET /api/v1/analytics/dashboard` with `period_type` and `anchor_date` filters in `backend/app/modules/analytics/router.py`
- [ ] T032 [US1] Register analytics router under `/api/v1/analytics` in `backend/app/api/router.py`
- [ ] T033 [US1] Implement dashboard API client functions and TanStack Query keys in `frontend/features/analytics/api.ts` and `frontend/features/analytics/hooks.ts`
- [ ] T034 [US1] Implement dashboard filter controls for day/week/month and anchor date in `frontend/features/analytics/components/DashboardFilters.tsx`
- [ ] T035 [US1] Implement summary card rendering in `frontend/features/analytics/components/SummaryCards.tsx`
- [ ] T036 [US1] Implement daily logs list rendering and selection callback shell in `frontend/features/analytics/components/DailyLogsList.tsx`
- [ ] T037 [US1] Implement period time timeline chart for week/month filters in `frontend/components/charts/PeriodTimeTimeline.tsx`
- [ ] T038 [US1] Implement reusable dashboard empty state in `frontend/features/analytics/components/EmptyState.tsx`
- [ ] T039 [US1] Compose the dashboard overview page in `frontend/features/analytics/components/DashboardOverview.tsx` and `frontend/app/dashboard/page.tsx`

**Checkpoint**: User Story 1 is independently testable as the MVP dashboard overview with period filtering and empty states.

---

## Phase 4: User Story 2 - Inspect a Single Day (Priority: P2)

**Goal**: Select a daily log and inspect that day's tasks in a read-only detail view with stable timeline order, hours-and-minutes durations, categories, tags, and optional notes.

**Independent Test**: Select a daily log from the dashboard and verify the day detail view shows the selected date, day total, task count, ordered tasks, categories, tags, notes, and a day-focused task timeline.

### Tests for User Story 2

- [ ] T040 [P] [US2] Add daily log detail service tests for empty day, active task filtering, note exclusion, and stable saved-order fallback in `backend/tests/services/test_daily_log_detail_service.py`
- [ ] T041 [P] [US2] Add daily log repository tests for day detail loading with tasks, categories, notes, and soft-delete exclusion in `backend/tests/repositories/test_daily_log_detail_repository.py`
- [ ] T042 [P] [US2] Add day detail API success envelope and empty day tests in `backend/tests/api/test_daily_log_detail_api.py`
- [ ] T043 [P] [US2] Add day detail API auth, permission, invalid date, and error envelope tests in `backend/tests/api/test_daily_log_detail_api_errors.py`
- [ ] T044 [P] [US2] Add day detail frontend rendering and task timeline order tests in `frontend/features/analytics/components/DayDetailView.test.tsx`

### Implementation for User Story 2

- [ ] T045 [P] [US2] Add day detail and task timeline response schemas in `backend/app/modules/daily_logs/schemas.py`
- [ ] T046 [US2] Extend daily log repository to load one day with active tasks, categories, active notes, and stable saved-order fallback in `backend/app/modules/daily_logs/repositories/daily_log_repository.py`
- [ ] T047 [US2] Extend daily log service to build day detail payloads and empty-state responses in `backend/app/modules/daily_logs/services/daily_log_service.py`
- [ ] T048 [US2] Wire daily log service provider for read endpoints in `backend/app/modules/daily_logs/dependencies.py`
- [ ] T049 [US2] Implement `GET /api/v1/daily-logs/{log_date}` with standard success envelope in `backend/app/modules/daily_logs/router.py`
- [ ] T050 [US2] Register daily logs router under `/api/v1/daily-logs` in `backend/app/api/router.py`
- [ ] T051 [US2] Add day detail API client and TanStack Query hook in `frontend/features/analytics/api.ts` and `frontend/features/analytics/hooks.ts`
- [ ] T052 [US2] Implement day detail view with task timeline, notes, tags, and clean absent-state rendering in `frontend/features/analytics/components/DayDetailView.tsx`
- [ ] T053 [US2] Connect daily log selection from `DailyLogsList` to `DayDetailView` while preserving period filter state in `frontend/features/analytics/components/DashboardOverview.tsx`
- [ ] T054 [US2] Add day-focused task timeline styling and accessibility labels in `frontend/features/analytics/components/DayDetailView.tsx`

**Checkpoint**: User Stories 1 and 2 are independently testable; users can navigate from overview to day detail and back without losing period context.

---

## Phase 5: User Story 3 - Compare Categories and Tags (Priority: P3)

**Goal**: Show visual category and tag breakdowns for the selected period, including top 10 plus `Other`, untagged time, multi-tag counting notice, readable labels, and totals that reconcile correctly.

**Independent Test**: Use sample records with many categories, many tags, untagged tasks, and multi-tag tasks; verify category totals reconcile, tag behavior is explained, and charts remain readable.

### Tests for User Story 3

- [ ] T055 [P] [US3] Add dashboard service tests for category totals, top 10 plus Other grouping, and share-of-total values in `backend/tests/services/test_dashboard_breakdowns.py`
- [ ] T056 [P] [US3] Add dashboard service tests for tag totals, untagged bucket, multi-tag counting notice, and Other grouping in `backend/tests/services/test_dashboard_tag_breakdown.py`
- [ ] T057 [P] [US3] Add dashboard API category and tag breakdown contract tests in `backend/tests/api/test_dashboard_breakdown_api.py`
- [ ] T058 [P] [US3] Add category and tag chart rendering tests for long labels, Other bucket, and text labels in `frontend/components/charts/BreakdownCharts.test.tsx`

### Implementation for User Story 3

- [ ] T059 [P] [US3] Add category breakdown, tag breakdown, named time total, and Other group schemas in `backend/app/modules/analytics/schemas.py`
- [ ] T060 [US3] Extend dashboard repository to return category totals and task tag rows for selected date ranges in `backend/app/modules/analytics/repositories/dashboard_repository.py`
- [ ] T061 [US3] Implement top 10 plus Other grouping, category share calculation, and total reconciliation in `backend/app/modules/analytics/services/dashboard_service.py`
- [ ] T062 [US3] Implement untagged bucket, multi-tag full-duration counting, tag share labels, and tag total notice in `backend/app/modules/analytics/services/dashboard_service.py`
- [ ] T063 [US3] Include category and tag breakdown payloads in `GET /api/v1/analytics/dashboard` responses in `backend/app/modules/analytics/router.py`
- [ ] T064 [US3] Implement category breakdown chart with text labels and accessible values in `frontend/components/charts/CategoryBreakdownChart.tsx`
- [ ] T065 [US3] Implement tag breakdown chart with untagged, Other, and multi-tag notice display in `frontend/components/charts/TagBreakdownChart.tsx`
- [ ] T066 [US3] Integrate category and tag charts into `frontend/features/analytics/components/DashboardOverview.tsx`
- [ ] T067 [US3] Add long-label handling and chart legend utilities in `frontend/features/analytics/utils.ts`

**Checkpoint**: All Phase 3 user stories are independently functional and the dashboard provides usable visual breakdowns.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Verify consistency, documentation, contracts, and out-of-scope boundaries across the completed Phase 3 dashboard foundation.

- [ ] T068 [P] Update dashboard API contract examples after implementation in `specs/004-dashboard-foundation/contracts/dashboard-api.yaml`
- [ ] T069 [P] Update dashboard implementation notes in `frontend/README.md`
- [ ] T070 [P] Update backend module notes for analytics ownership in `backend/app/modules/analytics/README.md`
- [ ] T071 Run backend Phase 3 tests documented in `specs/004-dashboard-foundation/quickstart.md`
- [ ] T072 Run frontend lint and production build documented in `specs/004-dashboard-foundation/quickstart.md`
- [ ] T073 Run the manual end-to-end smoke check from `specs/004-dashboard-foundation/quickstart.md`
- [ ] T074 Review `backend/app/modules/analytics/router.py`, `backend/app/modules/analytics/services/dashboard_service.py`, `backend/app/modules/analytics/repositories/dashboard_repository.py`, `backend/app/modules/daily_logs/router.py`, `backend/app/modules/daily_logs/services/daily_log_service.py`, and `backend/app/modules/daily_logs/repositories/daily_log_repository.py` for Router -> Service -> Repository -> Database boundary compliance
- [ ] T075 Verify all handled dashboard API responses use standard success/error envelopes across `backend/app/modules/analytics/router.py`, `backend/app/modules/daily_logs/router.py`, and `backend/app/core/exceptions.py`
- [ ] T076 Verify dashboard remains read-only and does not add CSV import processing, data editing, AI insight generation, scheduled automation, report export, or Notion API synchronization in `backend/app/modules/analytics/`, `backend/app/modules/daily_logs/`, and `frontend/features/analytics/`
- [ ] T077 Verify frontend server state is fetched through TanStack Query and not duplicated into global stores in `frontend/features/analytics/hooks.ts`, `frontend/features/analytics/components/DashboardOverview.tsx`, and `frontend/stores/`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies.
- **Foundational (Phase 2)**: Depends on Setup completion and blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion; this is the MVP.
- **User Story 2 (Phase 4)**: Depends on Foundational and can be tested independently with seeded daily log records.
- **User Story 3 (Phase 5)**: Depends on Foundational and dashboard overview response shape; can be tested independently with seeded category/tag records.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 - Review Productivity Overview**: Starts after Foundational; no dependency on US2 or US3.
- **US2 - Inspect a Single Day**: Starts after Foundational; integrates with US1 navigation but day detail endpoint and component can be tested directly.
- **US3 - Compare Categories and Tags**: Starts after Foundational; extends the dashboard overview payload and can be validated with direct API/component tests.

### Within Each User Story

- Tests are written before implementation.
- Schemas and exceptions before repositories and services.
- Repositories before services.
- Services before endpoints.
- Dependency providers before router wiring.
- API client functions before consuming frontend components.
- Core components before route/page composition.
- Story complete before moving to next priority.

---

## Parallel Opportunities

- T004, T005, T006, T007, T008, and T009 can run in parallel after T003 is defined.
- T011, T012, T014, T015, T018, and T019 can run in parallel during Foundational work.
- US1 tests T021-T025 can run in parallel.
- US1 frontend component tasks T034-T038 can run in parallel after T033.
- US2 tests T040-T044 can run in parallel.
- US2 backend schema task T045 can run in parallel with frontend API hook task T051 after the contract is understood.
- US3 tests T055-T058 can run in parallel.
- US3 chart tasks T064-T065 can run in parallel after T058 test expectations are drafted.
- Polish documentation tasks T068-T070 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "T021 Add dashboard period resolution and latest tracked day service tests in backend/tests/services/test_dashboard_service.py"
Task: "T022 Add dashboard repository tests in backend/tests/repositories/test_dashboard_repository.py"
Task: "T023 Add dashboard overview API success envelope tests in backend/tests/api/test_dashboard_api.py"
Task: "T024 Add dashboard overview API error envelope tests in backend/tests/api/test_dashboard_api_errors.py"
Task: "T025 Add dashboard frontend rendering tests in frontend/features/analytics/components/DashboardOverview.test.tsx"
Task: "T034 Implement dashboard filter controls in frontend/features/analytics/components/DashboardFilters.tsx"
Task: "T035 Implement summary cards in frontend/features/analytics/components/SummaryCards.tsx"
```

## Parallel Example: User Story 2

```text
Task: "T040 Add daily log detail service tests in backend/tests/services/test_daily_log_detail_service.py"
Task: "T041 Add daily log repository tests in backend/tests/repositories/test_daily_log_detail_repository.py"
Task: "T042 Add day detail API success tests in backend/tests/api/test_daily_log_detail_api.py"
Task: "T044 Add day detail frontend tests in frontend/features/analytics/components/DayDetailView.test.tsx"
Task: "T052 Implement day detail view in frontend/features/analytics/components/DayDetailView.tsx"
```

## Parallel Example: User Story 3

```text
Task: "T055 Add category breakdown service tests in backend/tests/services/test_dashboard_breakdowns.py"
Task: "T056 Add tag breakdown service tests in backend/tests/services/test_dashboard_tag_breakdown.py"
Task: "T057 Add dashboard breakdown API tests in backend/tests/api/test_dashboard_breakdown_api.py"
Task: "T058 Add chart rendering tests in frontend/components/charts/BreakdownCharts.test.tsx"
Task: "T064 Implement category breakdown chart in frontend/components/charts/CategoryBreakdownChart.tsx"
Task: "T065 Implement tag breakdown chart in frontend/components/charts/TagBreakdownChart.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup tasks T001-T009.
2. Complete Phase 2 foundational tasks T010-T020.
3. Complete US1 tasks T021-T039.
4. Stop and validate the overview independently with backend tests, frontend rendering checks, and the quickstart dashboard overview checks.

### Incremental Delivery

1. Setup + Foundational create backend analytics scaffolding, frontend runtime, API client, and shared dashboard types.
2. US1 delivers dashboard overview, filters, summary cards, daily logs list, period timeline, and empty states.
3. US2 adds day detail navigation and timeline inspection.
4. US3 adds category and tag comparison charts.
5. Polish verifies contracts, response shapes, read-only scope, frontend build, and boundary compliance.

### Scope Guardrails

- Do not add CSV import processing, data editing, AI insight generation, scheduled automation, report export, or Notion API synchronization.
- Do not add new persistent dashboard tables unless a later approved spec changes Phase 3 scope.
- Keep business rules in services and persistence logic in repositories.
- Keep frontend route files limited to composition and server/client boundaries.
- Use TanStack Query for server state and avoid copying API data into global stores.
