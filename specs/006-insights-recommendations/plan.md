# Implementation Plan: Insights & Recommendations

**Branch**: `006-insights-recommendations` | **Date**: 2026-04-20 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/006-insights-recommendations/spec.md`

**Note**: This plan covers Phase 5 only. It converts completed Phase 4 AI analysis output plus saved tracking facts into deterministic, explainable scores, best/worst day findings, and low-noise recommendations. It does not introduce a new AI provider call, scheduled automation, CSV import behavior, dashboard redesign, report export, Notion synchronization, AI chat, or custom/month insight periods.

## Summary

Phase 5 adds stored, reviewable insight results for calendar-day and Monday-to-Sunday calendar-week periods. The technical approach is to extend `backend/app/modules/ai_insights/` with deterministic scoring, day-ranking, recommendation, validation, persistence, and API services that read completed Phase 4 `AIInsightRun` output and source tracking facts without mutating source records. A small frontend feature under `frontend/features/ai-insights/` will consume the APIs to let the user generate, review, rerun, and inspect evidence for current and historical insight results inside the existing dashboard shell.

## Technical Context

**Language/Version**: Backend uses Python >=3.12 from `backend/pyproject.toml`. Frontend uses Next.js 15.5.15, React 18.3.1, and TypeScript 5.7.3 from `frontend/package.json`.  
**Primary Dependencies**: FastAPI >=0.135.3, SQLAlchemy Async >=2.0.45, Alembic >=1.17.2, asyncpg >=0.31.0, pydantic-settings >=2.12.0, existing Phase 1-4 domain modules, Next.js App Router, Tailwind CSS, TanStack Query 5.64.2, Zod 3.24.1, Axios 1.15.0, Recharts 2.15.0. Celery/Redis remain available from the stack but are not required for deterministic Phase 5 generation.  
**Storage**: PostgreSQL with existing `DailyLog`, `Task`, `Category`, `Note`, `AIInsightRun`, and `AIInsightRunSource` tables as read-only sources. Phase 5 adds persisted `AIInsightResult` and `AIInsightResultSource` records with UUID primary keys, JSON score/evidence/recommendation payloads, current-result selection metadata, validation outcome, source analysis reference, audit metadata, and soft delete. Redis is not used by Phase 5 generation.  
**Testing**: Backend command: `cd backend; pytest -q`. Targeted backend validation: `cd backend; pytest tests/domain tests/services tests/repositories tests/api tests/migrations -q`. Frontend commands: `cd frontend; npm run test` and `cd frontend; npm run build` for the minimal insights review UI.  
**Target Platform**: Docker Compose monorepo with FastAPI backend, PostgreSQL, Redis, Celery worker, and Next.js frontend. Phase 5 exposes versioned REST APIs and frontend dashboard views; generation is request/response because it is deterministic and bounded to personal day/week data.  
**Project Type**: Monorepo web application feature: FastAPI REST backend + Next.js dashboard frontend.  
**Performance Goals**: Generate or return the current insight result for a personal day/week within 5 seconds p95. Current result/detail/history API lookups return within 500 ms p95 for a personal workspace with up to 1,000 stored insight results. The user can understand each score and recommendation in under 2 minutes from displayed explanations and evidence.  
**Constraints**: Support only `daily` and `weekly` periods; weekly periods resolve to Monday-to-Sunday local dates. Use deterministic application rules only; do not call the AI provider. Exclude task note text from inputs, outputs, explanations, and recommendation evidence. Do not mutate daily logs, tasks, notes, categories, tags, imports, or Phase 4 AI analysis runs. Default generation for the same owner, period, and source analysis returns the existing current result; explicit rerun creates a new historical result and marks the latest successful rerun current.  
**Scale/Scope**: Personal single-owner v1. A weekly insight covers exactly 7 local calendar days. Recommendation sets contain 0-3 recommendations. A numeric productivity score requires at least one tracked day, one tracked task, completed source analysis, and at least two evidence points. Weekly consistency and best/worst findings require at least three tracked days.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to Phase 5 scores, best/worst day findings, recommendations, result review, and traceability; future automation/import/export/chat work is excluded.
- Backend modules: PASS. Insight generation, validation, persistence, and recommendation storage belong in `backend/app/modules/ai_insights/`; analytics and source modules are read-only inputs.
- Backend layering: PASS. Routers expose versioned endpoints; services own deterministic scoring/recommendation rules and validation; repositories encapsulate SQLAlchemy async persistence.
- Dependency injection: PASS. `ai_insights/dependencies.py` will wire repositories and services through FastAPI `Depends`.
- Configuration: PASS. No new external provider settings are needed. Any deterministic threshold constants stay module-local in `ai_insights/constants.py`.
- Database: PASS. Persistence changes require Alembic migrations for Phase 5 result tables; source records and Phase 4 runs are not mutated.
- API versioning: PASS. Contracts define `/api/v1/ai-insights/results...`; no unversioned production APIs are planned.
- Response contracts: PASS. Contracts use `{ "success": true, "data": ... }` and the unified handled error schema with stable error codes.
- Pagination: PASS. Result history uses bounded `page` and `limit` pagination.
- Observability: PASS. API logs include `request_id`, `owner_id`, `ai_insight_result_id`, source analysis run ID, period granularity, validation status, and current-result/reuse decisions.
- Security: PASS. Endpoints require `ai_insights:read` or `ai_insights:write`; generate/rerun endpoints have stricter rate limits than read endpoints.
- Background jobs: PASS. No Phase 5 worker is planned because generation is deterministic and bounded; Celery remains reserved for Phase 4 AI execution and future automation.
- Idempotency: PASS. Default generation is idempotent for owner + period + source analysis; explicit reruns create new history. Optional `Idempotency-Key` protects duplicate write submissions.
- AI isolation: PASS. Phase 5 uses completed Phase 4 output as input and keeps stored insight outputs inside `ai_insights`; it does not add prompts, tools, or provider calls.
- Soft delete: PASS. Generated insight results are audit-sensitive and soft-delete-capable; normal reads exclude soft-deleted results.
- Audit trail: PASS. Result records include actor/owner, request metadata, source period, source analysis run, generated timestamp, validation outcome, current marker, and failure details.
- Frontend boundaries: PASS. `frontend/app/` handles route composition; feature UI, hooks, schemas, and API calls stay under `frontend/features/ai-insights/` and `frontend/lib/api/`.
- State/forms: PASS. TanStack Query handles insight server state. Zod validates API payloads where client schemas are added. No React Hook Form work is required.
- Testing: PASS. Backend service/API/repository/migration tests and frontend component/hook tests are planned for success/error envelopes, auth, pagination, idempotency/current-result behavior, validation, privacy, and result review.

## Project Structure

### Documentation (this feature)

```text
specs/006-insights-recommendations/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- insights-recommendations-api.yaml
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 5 backend ownership:

```text
backend/
|-- app/
|   |-- modules/
|   |   |-- ai_insights/
|   |   |   |-- router.py
|   |   |   |-- schemas.py
|   |   |   |-- constants.py
|   |   |   |-- exceptions.py
|   |   |   |-- dependencies.py
|   |   |   |-- models.py
|   |   |   |-- repositories/
|   |   |   |   |-- ai_insight_run_repository.py
|   |   |   |   `-- ai_insight_result_repository.py
|   |   |   `-- services/
|   |   |       |-- insight_generation_service.py
|   |   |       |-- insight_source_service.py
|   |   |       |-- productivity_scoring_service.py
|   |   |       |-- consistency_scoring_service.py
|   |   |       |-- day_ranking_service.py
|   |   |       |-- recommendation_service.py
|   |   |       |-- insight_validation_service.py
|   |   |       `-- insight_result_service.py
|   |   |-- analytics/
|   |   |-- daily_logs/
|   |   `-- tasks/
|   |-- api/
|   |   `-- router.py
|   `-- shared/
|       |-- schemas/
|       |   `-- responses.py
|       `-- enums/
|           `-- run_status.py
|-- alembic/
|   `-- versions/
`-- tests/
    |-- api/
    |   |-- test_ai_insight_results_api.py
    |   `-- test_ai_insight_results_api_errors.py
    |-- domain/
    |   |-- test_insight_scoring_rules.py
    |   |-- test_day_ranking_rules.py
    |   `-- test_recommendation_validation.py
    |-- migrations/
    |   `-- test_insight_results_migration.py
    |-- repositories/
    |   `-- test_ai_insight_result_repository.py
    `-- services/
        |-- test_insight_generation_service.py
        |-- test_insight_result_idempotency.py
        `-- test_insight_privacy_boundary.py
```

Planned Phase 5 frontend ownership:

```text
frontend/
|-- app/
|   `-- dashboard/
|       `-- ai-insights/
|           `-- page.tsx
|-- features/
|   `-- ai-insights/
|       |-- api.ts
|       |-- schemas.ts
|       |-- query-keys.ts
|       |-- hooks/
|       |   |-- use-current-insight-result.ts
|       |   |-- use-generate-insight-result.ts
|       |   `-- use-insight-result-history.ts
|       `-- components/
|           |-- InsightPeriodPicker.tsx
|           |-- ScoreExplanation.tsx
|           |-- DayFindings.tsx
|           |-- RecommendationList.tsx
|           |-- EvidenceList.tsx
|           `-- InsightHistoryList.tsx
|-- lib/
|   `-- api/
|       `-- client.ts
`-- types/
    `-- api.ts
```

**Structure Decision**: Extend `backend/app/modules/ai_insights/` because Phase 5 consumes completed AI analysis output and stores generated insight outputs. Keep source-data aggregation reads behind module services/repositories and do not move deterministic scoring into `analytics`, because the generated result lifecycle, recommendations, current-result history, privacy validation, and audit trail are AI-insight domain behavior. Add a minimal frontend dashboard route for review and generation controls without redesigning the broader dashboard.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 5 planning details:

- Use deterministic rules over saved facts and completed Phase 4 output; no new AI provider call.
- Add dedicated `AIInsightResult` persistence rather than overloading Phase 4 `AIInsightRun`.
- Use synchronous request/response generation because deterministic day/week generation is bounded.
- Resolve source analysis by current completed Phase 4 run unless a specific source analysis run ID is provided.
- Use default idempotent generation by owner + period + source analysis, with explicit rerun for history.
- Store evidence-backed score, day-finding, recommendation, and validation payloads as structured JSON with source links.
- Exclude note text from Phase 5 source summaries, explanations, evidence, and recommendations.
- Expose backend REST APIs for generate, explicit rerun, current result lookup, detail, and paginated history.
- Add a minimal frontend result-review experience under the existing dashboard shell.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines Phase 5 insight period, result, source links, score outcomes, day findings, recommendations, evidence, validation outcome, current-result selection, state transitions, and migration impact.
- [contracts/insights-recommendations-api.yaml](./contracts/insights-recommendations-api.yaml): Defines versioned REST API contracts for generating/reusing results, explicit reruns, current result lookup, result detail, and paginated history.
- [quickstart.md](./quickstart.md): Defines planning validation and later implementation smoke checks for backend and frontend work.

Database migration is planned for Phase 5 to add `AIInsightResult` and `AIInsightResultSource` persistence with soft delete, source analysis references, current-result metadata, validation status, and structured output payloads. Existing Phase 4 `AIInsightRun` records remain immutable source analysis inputs.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts stay focused on Phase 5 insights and recommendations and exclude scheduled automation, imports, report export, Notion sync, dashboard redesign, and AI chat.
- Backend modules: PASS. Contracts and data model assign result generation, validation, and storage to `ai_insights`; source modules remain authoritative and read-only.
- Backend layering: PASS. Contracts, data model, and quickstart preserve router/service/repository/database separation.
- Dependency injection: PASS. Planned dependencies are module-local and explicit.
- Configuration: PASS. No new settings files are required; rule thresholds belong in module constants.
- Database: PASS. Migration impact is identified and limited to generated insight result tables.
- API versioning, response contracts, pagination: PASS. Contract uses `/api/v1`, success/error envelopes, and `page`/`limit` history pagination.
- Observability, audit, idempotency: PASS. Result records and contract fields include request metadata, source analysis, status/validation details, current-result reuse, explicit rerun behavior, and traceability.
- Security: PASS. Contract defines `ai_insights:read` and `ai_insights:write` scopes and rate-limit expectations.
- Background jobs: PASS. No worker is introduced; deterministic generation remains in services.
- AI isolation: PASS. Phase 5 uses Phase 4 output as data and does not add AI provider calls.
- Soft delete: PASS. Insight results and source links remain audit-sensitive and soft-delete-capable.
- Frontend boundaries and state/forms: PASS. UI work is isolated to `frontend/features/ai-insights/` and a route composition file under `frontend/app/dashboard/ai-insights/`.
- Testing: PASS. Backend service/API/repository/migration tests and frontend query/component tests are documented.

Ready for `/speckit.tasks`.
