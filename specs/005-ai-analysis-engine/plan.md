# Implementation Plan: AI Analysis Engine

**Branch**: `005-ai-analysis-engine` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/005-ai-analysis-engine/spec.md`

**Note**: This plan covers Phase 4 only. It plans basic AI analysis execution for saved daily tracking data: combined daily and weekly analysis runs, structured input preparation, privacy-bounded AI inputs, prompt/instruction versioning, stored outputs, reruns, retry support, and traceable failures. CSV import, dashboard visualization changes, productivity scores, recommendation generation, scheduled automation, AI chat, report export, and Notion API synchronization remain out of scope.

## Summary

Phase 4 turns existing saved tracking records into traceable AI analysis runs. The technical approach is to extend the existing `ai_insights` backend module with request/status/history APIs, service-layer input preparation, prompt/instruction versioning, output validation, current-result selection, and a thin Celery task that delegates execution to services. The implementation reuses Phase 1 `AIInsightRun` and `AIInsightRunSource` ownership while adding the Phase 4 metadata needed for combined outputs, retained input summaries, retry counts, idempotency, and instruction versions.

AI analysis reads valid saved task names, durations, categories, and tags only. Note text is excluded from AI inputs and generated outputs. The full structured AI input payload is not retained after source references, aggregate input summary, instruction version, output, and run metadata are recorded.

## Technical Context

**Language/Version**: Backend uses Python >=3.12 from `backend/pyproject.toml`. Frontend remains the existing Next.js 15.5.15 + TypeScript 5.7.3 app, but Phase 4 does not plan frontend runtime work.  
**Primary Dependencies**: FastAPI >=0.135.3, SQLAlchemy Async >=2.0.45, Alembic >=1.17.2, asyncpg >=0.31.0, pydantic-settings >=2.12.0, Celery >=5.6.0, Redis >=7.1.0, existing Phase 1-3 domain modules, and an AI provider adapter isolated in `backend/app/modules/ai_insights/`.  
**Storage**: PostgreSQL with existing `DailyLog`, `Task`, `Category`, `Note`, `AIInsightRun`, and `AIInsightRunSource` tables. A migration is planned to extend AI run persistence for `instruction_name`, `instruction_version`, `output_outcome`, `retry_count`, `idempotency_key`, and attempt/failure metadata while keeping outputs separate from source records. Redis remains the Celery broker/result backend.  
**Testing**: Backend command: `cd backend; pytest -q`. Phase 4 tasks should add targeted tests under `backend/tests/domain`, `backend/tests/services`, `backend/tests/repositories`, `backend/tests/api`, `backend/tests/workers`, and `backend/tests/migrations`, then validate with `cd backend; pytest tests/domain tests/services tests/repositories tests/api tests/workers tests/migrations -q`.  
**Target Platform**: Docker Compose monorepo with FastAPI backend, PostgreSQL, Redis, and Celery worker. Phase 4 exposes versioned REST APIs and runs heavy analysis through Celery.  
**Project Type**: Monorepo web application backend feature: FastAPI REST backend + Celery worker. Existing frontend may consume the APIs later, but frontend UI work is outside this phase.  
**Performance Goals**: Accepted analysis requests return a run identifier and visible `pending` status within 5 seconds. At least 95% of analyses for a week containing up to 7 days of personal tracking data complete or reach a traceable failure state within 2 minutes. Run history/status lookup for a period and granularity is reviewable in under 2 minutes.  
**Constraints**: Stay within `ai_insights` and read-only analytics/source-data boundaries; do not mutate daily logs, tasks, notes, categories, tags, imports, or import outcomes. Exclude note text from AI inputs and outputs. Do not retain the full structured AI input payload. Use shared run statuses `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`. No scheduled runs, scores, recommendations, dashboard UI changes, or chat behavior.  
**Scale/Scope**: Personal v1 workspace. Supported period granularities are `daily` and `weekly` only. A weekly run covers exactly 7 local calendar days. Each daily or weekly request creates one combined analysis output containing summary, detected patterns, behavior insights, supporting evidence, limitations, generated timestamp, and output outcome.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to basic Phase 4 AI analysis runs and explicitly excludes Phase 5 recommendations/scores and Phase 6 scheduled automation.
- Backend modules: PASS. AI orchestration, prompt preparation, run storage, output validation, and worker payload handling belong in `backend/app/modules/ai_insights/`; source record reads use existing daily log/task ownership through repositories/services.
- Backend layering: PASS. Routers expose request/status/history endpoints; services own run lifecycle, input preparation, output validation, retry rules, and current-result selection; repositories encapsulate SQLAlchemy queries.
- Dependency injection: PASS. `ai_insights/dependencies.py` provides service/repository wiring through FastAPI `Depends`.
- Configuration: PASS. AI settings are planned under `backend/app/settings/ai.py` and composed in `backend/app/core/config.py`.
- Database: PASS. Persistence changes require an Alembic migration extending existing AI run tables; source tables remain authoritative and are not mutated.
- API versioning: PASS. Contracts define `/api/v1/ai-insights/...`; no unversioned production APIs are planned.
- Response contracts: PASS. Contracts use `{ "success": true, "data": ... }` and the unified handled error schema with stable error codes.
- Pagination: PASS. Run history uses bounded `page` and `limit` pagination.
- Observability: PASS. API and worker logs include `request_id`, `ai_insight_run_id`, owner, period granularity, status transitions, retry count, instruction version, and failure details.
- Security: PASS. Endpoints require `ai_insights:read` or `ai_insights:write`; expensive write/rerun endpoints have stricter rate limits than read endpoints.
- Background jobs: PASS. Celery tasks stay thin and delegate all AI analysis behavior to services.
- Idempotency: PASS. Create-analysis requests support an optional `Idempotency-Key`; duplicate in-flight requests for the same owner/period/granularity are handled without creating conflicting current results.
- AI isolation: PASS. Agent/provider orchestration, prompt templates, output validation, and stored outputs remain inside `backend/app/modules/ai_insights/`.
- Soft delete: PASS. Generated AI outputs and run records are audit-sensitive and use soft delete; normal reads exclude soft-deleted runs.
- Audit trail: PASS. AI runs record actor/owner, request metadata, source references, aggregate input summary, instruction version, resulting status, retry count, output outcome, and failure details.
- Frontend boundaries: PASS. No frontend work is planned. Future UI consumption would belong under `frontend/features/ai-insights/`.
- State/forms: PASS. No frontend state or form work is introduced.
- Testing: PASS. Plan requires service tests for lifecycle/input/output/retry/idempotency, API integration tests for envelopes/errors/auth/pagination/rate-limit expectations, worker tests for thin delegation, repository tests, and migration tests.

## Project Structure

### Documentation (this feature)

```text
specs/005-ai-analysis-engine/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- ai-insights-api.yaml
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 4 backend ownership:

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
|   |   |   |   `-- ai_insight_run_repository.py
|   |   |   |-- services/
|   |   |   |   |-- ai_analysis_service.py
|   |   |   |   |-- ai_input_service.py
|   |   |   |   |-- ai_instruction_service.py
|   |   |   |   |-- ai_output_validator.py
|   |   |   |   `-- ai_insight_run_service.py
|   |   |   `-- providers/
|   |   |       |-- base.py
|   |   |       `-- configured.py
|   |   |-- daily_logs/
|   |   |-- tasks/
|   |   `-- analytics/
|   |-- settings/
|   |   `-- ai.py
|   |-- workers/
|   |   `-- tasks/
|   |       `-- ai_analysis_tasks.py
|   |-- api/
|   |   `-- router.py
|   `-- shared/
|       |-- enums/
|       |   `-- run_status.py
|       `-- schemas/
|           `-- responses.py
|-- alembic/
|   `-- versions/
`-- tests/
    |-- api/
    |   |-- test_ai_insight_api.py
    |   `-- test_ai_insight_api_errors.py
    |-- domain/
    |   `-- test_ai_analysis_output_validation.py
    |-- migrations/
    |   `-- test_ai_analysis_engine_migration.py
    |-- repositories/
    |   `-- test_ai_analysis_repository.py
    |-- services/
    |   |-- test_ai_analysis_service.py
    |   |-- test_ai_input_service.py
    |   `-- test_ai_run_idempotency.py
    `-- workers/
        `-- test_ai_analysis_worker.py
```

No Phase 4 frontend source ownership is planned.

**Structure Decision**: Extend the existing `backend/app/modules/ai_insights/` module rather than adding AI behavior to analytics, imports, daily logs, or frontend modules. Add a module-local provider abstraction so tests can use deterministic fake AI output while production settings can point to a configured provider. Register the new router through `backend/app/api/router.py` under `/api/v1/ai-insights`.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 4 planning details:

- Use one combined analysis run per day or week.
- Use a provider abstraction inside `ai_insights` with deterministic test provider support.
- Build privacy-bounded structured input from task names, durations, categories, and tags only; exclude notes.
- Retain only source references, aggregate input summary, instruction version, output, and run metadata.
- Use the shared `RunStatus` vocabulary with output outcome `no_data` for empty periods.
- Retry transient failures up to 3 total attempts and preserve attempt/failure details.
- Use optional request idempotency keys plus in-flight conflict handling to avoid duplicate current results.
- Expose backend REST APIs for create, rerun, status, current result, and paginated history.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines Phase 4 AI analysis request, run, input summary, instruction version, combined output, evidence, failure attempt, current result, state transitions, validation rules, and persistence changes.
- [contracts/ai-insights-api.yaml](./contracts/ai-insights-api.yaml): Defines versioned REST API contracts for requesting runs, reruns, current result lookup, run status, and paginated history.
- [quickstart.md](./quickstart.md): Defines planning validation and later implementation smoke checks.

Database migration is planned for Phase 4 to extend `AIInsightRun` with explicit combined-analysis metadata, retry/idempotency fields, and output outcome tracking while preserving existing source links.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts remain focused on Phase 4 basic AI analysis engine behavior.
- Backend modules: PASS. Contracts and data model assign AI execution and output storage to `ai_insights`; source records remain owned by daily logs, tasks, notes, imports, and analytics.
- Backend layering: PASS. API contracts, data model, and quickstart preserve router/service/repository/database separation.
- Dependency injection: PASS. Planned dependencies are module-local and explicit.
- Configuration: PASS. AI provider/model/timeouts/retry settings are planned in `backend/app/settings/ai.py` and composed in core settings.
- Database: PASS. Migration impact is identified and limited to AI run metadata; source records are not changed.
- API versioning, response contracts, pagination: PASS. Contract uses `/api/v1`, success/error envelopes, and `page`/`limit` history pagination.
- Observability, audit, idempotency: PASS. Run records and contract fields include request metadata, source references, status, retry counts, failure details, idempotency behavior, and current-result selection.
- Security: PASS. Contract defines `ai_insights:read` and `ai_insights:write` scopes and rate-limit expectations.
- Background jobs: PASS. Worker contract is thin and delegates to services.
- AI isolation: PASS. Provider, instructions, validation, and outputs stay in `ai_insights`.
- Soft delete: PASS. AI run records remain audit-sensitive and soft-delete-capable.
- Frontend boundaries and state/forms: PASS. No frontend work is planned.
- Testing: PASS. Backend service/API/repository/worker/migration tests are documented.

Ready for `/speckit.tasks`.
