# Implementation Plan: Dashboard Foundation

**Branch**: `004-dashboard-foundation` | **Date**: 2026-04-18 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/004-dashboard-foundation/spec.md`

**Note**: This plan covers Phase 3 only. It plans read-only dashboard analytics, daily log detail retrieval, period filters, chart-ready payloads, and the first usable dashboard frontend. CSV import processing, data editing, AI-generated insights, scheduled automation, report export, and Notion API synchronization remain out of scope.

## Summary

Phase 3 turns the Phase 1/2 stored tracking records into a usable dashboard. The technical approach is to add a read-only `analytics` backend module for dashboard aggregates and chart-ready payloads, add a small `daily_logs` read endpoint for day detail, and bootstrap the frontend dashboard route using the approved Next.js App Router stack. The backend remains the source of truth for date-range selection, totals, top-10-plus-Other grouping, untagged time, and multi-tag counting notices; the frontend focuses on navigation, rendering, filters, and accessible visualization.

The dashboard defaults to the latest tracked day when available. Week and month filters use Monday-to-Sunday weeks and full calendar months. All user-facing durations are displayed as hours and minutes while preserving minute-level values in API payloads.

## Technical Context

**Language/Version**: Backend uses Python >=3.12 from `backend/pyproject.toml`. Frontend uses the approved Next.js App Router + TypeScript stack; package versions will be pinned when the Phase 3 frontend package is bootstrapped because the current `frontend/` directory is still a skeleton without `package.json`.  
**Primary Dependencies**: Backend uses FastAPI, SQLAlchemy Async, Alembic, asyncpg, pydantic-settings, and existing Phase 1/2 modules. Frontend uses Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, Zod, Axios, and Recharts.  
**Storage**: PostgreSQL with existing `DailyLog`, `Task`, `Category`, and `Note` tables. No new persistent tables are planned for Phase 3; analytics payloads are derived from active saved tracking records. Redis/Celery remain available from Phase 2 but are not used for dashboard reads.  
**Testing**: Backend command: `cd backend; pytest -q`. Phase 3 tasks should add targeted backend tests under `backend/tests/api`, `backend/tests/services`, and `backend/tests/repositories`, then validate with `cd backend; pytest tests/api tests/services tests/repositories -q`. Frontend tasks must add package scripts during bootstrap and validate with `cd frontend; npm run lint` and `cd frontend; npm run build`; component or hook tests should be added if the chosen scaffold includes a test runner.  
**Target Platform**: Docker Compose monorepo with FastAPI backend, Next.js frontend, PostgreSQL, Redis, and the existing worker service. Dashboard pages are browser-based and consume versioned backend REST APIs.  
**Project Type**: Monorepo web application: FastAPI REST backend + Next.js dashboard frontend.  
**Performance Goals**: Dashboard overview and day detail payloads for one year of personal tracking data return quickly enough for visible filter changes to complete within 2 seconds. Primary dashboard information is understandable within 30 seconds of opening the page.  
**Constraints**: Stay read-only; no import processing, editing, AI analysis, scheduled jobs, report export, or Notion API synchronization. Routers remain thin, services own period/date and aggregation rules, repositories own SQLAlchemy queries, and frontend server state uses TanStack Query rather than duplicated global state.  
**Scale/Scope**: Personal v1 workspace. Dashboard filters cover `day`, `week`, and `month`. Month daily-log lists are naturally bounded by calendar days and do not require pagination. Category and tag charts show top 10 contributors plus `Other`.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to dashboard read APIs, analytics payloads, frontend dashboard rendering, filters, and charts.
- Backend modules: PASS. Aggregate behavior belongs in `backend/app/modules/analytics/`; day detail read behavior belongs in `backend/app/modules/daily_logs/`; task/category/note data remains owned by existing modules.
- Backend layering: PASS. Routers expose versioned read endpoints; services calculate period bounds and payloads; repositories encapsulate read queries.
- Dependency injection: PASS. `analytics/dependencies.py` and `daily_logs/dependencies.py` provide service/repository wiring through FastAPI `Depends`.
- Configuration: PASS. No new settings domain is required unless frontend API base URL configuration is added during scaffold.
- Database: PASS. Existing Phase 1 tables are reused; no migration is required. Day detail can use saved order as the stable fallback when source/import order is unavailable.
- API versioning: PASS. Contracts define `/api/v1/analytics/dashboard` and `/api/v1/daily-logs/{log_date}`.
- Response contracts: PASS. Contracts use `{ "success": true, "data": ... }` and the unified handled error schema.
- Pagination: PASS. Dashboard daily-log lists are date-bounded and do not need page/cursor pagination; this is documented in the contract.
- Observability: PASS. Read endpoints log `request_id`, owner, period type, date range, and error codes without audit-trail writes because no user-owned data is changed.
- Security: PASS. Read endpoints require `analytics:read` or `daily_logs:read`; rate-limit expectations are documented.
- Background jobs: PASS. No Celery work is introduced.
- Idempotency: PASS. Dashboard reads are safe and idempotent by HTTP semantics; no idempotency key is needed.
- AI isolation: PASS. No AI behavior is introduced.
- Soft delete: PASS. User-facing dashboard reads exclude soft-deleted daily logs, tasks, categories, and notes by default.
- Audit trail: PASS. No import, AI-run, admin action, or mutation audit trail is introduced in Phase 3.
- Frontend boundaries: PASS. Route composition belongs in `frontend/app/`; dashboard feature logic belongs in `frontend/features/analytics/` and reusable chart components in `frontend/components/`.
- State/forms: PASS. TanStack Query handles dashboard server state. No user-facing form validation is needed beyond filter schema parsing.
- Testing: PASS. Plan requires service aggregation tests, API integration tests for envelopes/errors/auth/rate-limit metadata, and frontend build/lint plus dashboard rendering checks.

## Project Structure

### Documentation (this feature)

```text
specs/004-dashboard-foundation/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- dashboard-api.yaml
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 3 backend ownership:

```text
backend/
|-- app/
|   |-- modules/
|   |   |-- analytics/
|   |   |   |-- router.py
|   |   |   |-- schemas.py
|   |   |   |-- constants.py
|   |   |   |-- exceptions.py
|   |   |   |-- dependencies.py
|   |   |   |-- services/
|   |   |   |   `-- dashboard_service.py
|   |   |   `-- repositories/
|   |   |       `-- dashboard_repository.py
|   |   |-- daily_logs/
|   |   |   |-- router.py
|   |   |   |-- schemas.py
|   |   |   |-- dependencies.py
|   |   |   |-- services/
|   |   |   |   `-- daily_log_service.py
|   |   |   `-- repositories/
|   |   |       `-- daily_log_repository.py
|   |   |-- tasks/
|   |   `-- notes/
|   |-- api/
|   |   `-- router.py
|   `-- shared/
|       `-- schemas/
|           `-- responses.py
`-- tests/
    |-- api/
    |   |-- test_dashboard_api.py
    |   `-- test_daily_log_detail_api.py
    |-- services/
    |   `-- test_dashboard_service.py
    `-- repositories/
        `-- test_dashboard_repository.py
```

Planned Phase 3 frontend ownership:

```text
frontend/
|-- package.json
|-- app/
|   |-- layout.tsx
|   |-- page.tsx
|   `-- dashboard/
|       `-- page.tsx
|-- components/
|   |-- charts/
|   |   |-- CategoryBreakdownChart.tsx
|   |   |-- TagBreakdownChart.tsx
|   |   `-- PeriodTimeTimeline.tsx
|   `-- layout/
|       `-- DashboardShell.tsx
|-- features/
|   `-- analytics/
|       |-- api.ts
|       |-- hooks.ts
|       |-- schemas.ts
|       |-- types.ts
|       |-- utils.ts
|       `-- components/
|           |-- DashboardOverview.tsx
|           |-- DashboardFilters.tsx
|           |-- SummaryCards.tsx
|           |-- DailyLogsList.tsx
|           |-- DayDetailView.tsx
|           `-- EmptyState.tsx
|-- lib/
|   `-- api/
|       `-- client.ts
|-- types/
`-- public/
```

**Structure Decision**: Implement dashboard aggregation in `backend/app/modules/analytics/` and day detail reads in `backend/app/modules/daily_logs/`. Register both routers through `backend/app/api/router.py` under `/api/v1`. Bootstrap the frontend package in the existing `frontend/` skeleton rather than creating a second app directory. Keep dashboard-specific frontend behavior in `frontend/features/analytics/`; reusable chart primitives may live under `frontend/components/charts/`.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 3 planning details:

- Use a backend-composed dashboard payload so totals, grouping, period bounds, and edge cases have one source of truth.
- Expose two read endpoints: dashboard overview and day detail.
- Use `period_type` plus `anchor_date` for day/week/month filters.
- Use top 10 plus `Other` grouping server-side for category and tag chart payloads.
- Include `untagged` time in tag breakdowns and include a multi-tag counting notice when applicable.
- Bootstrap the frontend runtime during Phase 3 because the current frontend folder is a skeleton.
- Keep all dashboard behavior read-only and exclude soft-deleted records.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines dashboard query value objects, aggregate response models, chart item rules, day detail shape, and validation rules.
- [contracts/dashboard-api.yaml](./contracts/dashboard-api.yaml): Defines versioned REST API contracts for dashboard overview and day detail.
- [quickstart.md](./quickstart.md): Defines manual validation steps for the planning artifacts and later implementation output.

No database migration is planned for Phase 3. Existing saved task order is the stable fallback when source/import order is unavailable.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts remain focused on read-only dashboard foundation behavior.
- Backend modules: PASS. Aggregation is assigned to `analytics`; day detail reads remain in `daily_logs`; source record ownership remains unchanged.
- Backend layering: PASS. Contracts, data model, and plan separate router, service, repository, and model responsibilities.
- Dependency injection: PASS. Provider files are planned for analytics and daily logs.
- Configuration and database: PASS. No new settings or tables are required by default.
- API versioning, response contracts, pagination: PASS. Contracts use `/api/v1`, success/error envelopes, and document why pagination is not used for date-bounded dashboard lists.
- Observability, audit, idempotency: PASS. Read endpoints are request-id logged, require no mutation audit trail, and are idempotent reads.
- Security: PASS. Contracts define `analytics:read`, `daily_logs:read`, and rate limits.
- Background jobs: PASS. No worker tasks are introduced.
- AI isolation: PASS. No AI behavior is introduced.
- Soft delete: PASS. Dashboard reads exclude soft-deleted source records.
- Frontend boundaries and state/forms: PASS. App routes compose pages; `features/analytics` owns dashboard logic; TanStack Query owns server state.
- Testing: PASS. Backend service/API/repository tests and frontend lint/build/render checks are documented.

Ready for `/speckit.tasks`.
