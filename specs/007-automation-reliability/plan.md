# Implementation Plan: Automation & Reliability

**Branch**: `007-automation-reliability` | **Date**: 2026-04-21 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/007-automation-reliability/spec.md`

**Note**: This plan covers Phase 6 only. It plans backend automation APIs, scheduled CSV imports from user-configured CSV source references, scheduled daily/weekly AI analysis runs, bounded retries, missed-window handling, auditability, logs, and run history. Frontend schedule-management UI, automatic Phase 5 insight generation, report export, Notion API synchronization, AI chat, dashboard redesign, arbitrary external connectors, raw CSV retention, and new AI recommendation logic remain out of scope.

## Summary

Phase 6 makes the existing import and AI analysis workflows production-ready for scheduled operation. The technical approach is to extend the existing `imports` and `ai_insights` backend modules with schedule models, schedule APIs, schedule-owned services, repositories, audit metadata, and paginated history while adding shared due-window evaluation and Celery Beat orchestration under `backend/app/workers/`. Worker tasks stay thin: the scheduler finds due schedule windows, delegates scheduled imports to the existing import services, and delegates scheduled AI analysis to the existing Phase 4 AI run services.

No new `automation` backend module is planned because it is not an approved constitution module. Common scheduling value objects and Celery Beat wiring belong in worker infrastructure; feature-specific schedule behavior remains in `imports` and `ai_insights`.

## Technical Context

**Language/Version**: Backend uses Python >=3.12 from `backend/pyproject.toml`. Frontend remains the existing Next.js 15.5.15 + TypeScript 5.7.3 app, but Phase 6 does not plan frontend runtime work.  
**Primary Dependencies**: FastAPI >=0.135.3, SQLAlchemy Async >=2.0.45, Alembic >=1.17.2, asyncpg >=0.31.0, pydantic-settings >=2.12.0, Celery >=5.6.0, Redis >=7.1.0, existing `imports` and `ai_insights` modules, existing Celery task infrastructure, and Celery Beat service wiring through the approved worker stack.  
**Storage**: PostgreSQL with existing `ImportRun`, `ImportRowOutcome`, `AIInsightRun`, and AI insight source/result tables. New migrations are planned for import schedule/history tables and AI analysis schedule/history fields or tables. Redis remains the Celery broker/result backend. Raw CSV contents are not retained.  
**Testing**: Backend command: `cd backend; pytest -q`. Phase 6 tasks should add targeted tests under `backend/tests/domain`, `backend/tests/services`, `backend/tests/repositories`, `backend/tests/api`, `backend/tests/workers`, and `backend/tests/migrations`, then validate with `cd backend; pytest tests/domain tests/services tests/repositories tests/api tests/workers tests/migrations -q`.  
**Target Platform**: Docker Compose monorepo with FastAPI backend, PostgreSQL, Redis, Celery worker, and Celery Beat for scheduled evaluation.  
**Project Type**: Backend API and worker phase inside a FastAPI REST + Next.js dashboard product. Frontend UI work is intentionally excluded.  
**Performance Goals**: Due schedule evaluation creates exactly one started/skipped/failed history entry for each evaluated window. At least 95% of scheduled daily automation over a 30-day test period completes or reaches a traceable skipped/failed terminal state within 10 minutes of due time. Users can identify automation schedule state and run outcomes from backend responses in under 2 minutes; maintainers can correlate failed scheduled work in under 10 minutes from retained history/logs.  
**Constraints**: Stay within Phase 6 automation/reliability scope; do not add frontend schedule-management UI, automatic Phase 5 insight generation, Notion API sync, arbitrary external connectors, raw CSV retention, report export, AI chat, or dashboard redesign. Preserve router/service/repository layering, success/error envelopes, page/limit pagination, owner permissions, rate limits, soft-delete schedule removal, 90-day detailed history retention, and three-attempt retry limits.  
**Scale/Scope**: Personal v1 workspace. Supported schedule cadences are `daily` and `weekly`. Scheduled imports consume only newly available CSV input from a user-configured source reference. Scheduled AI analysis supports completed calendar days and Monday-to-Sunday weeks. After downtime, only the latest missed due window per active schedule is processed; older missed windows are recorded as skipped.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to backend scheduled imports, scheduled AI analysis, retries, logs, auditability, and run history; frontend UI, Phase 5 auto-generation, export, Notion sync, chat, and dashboard redesign are excluded.
- Backend modules: PASS. Import schedule behavior belongs in `backend/app/modules/imports/`; AI analysis schedule behavior belongs in `backend/app/modules/ai_insights/`; shared due-window evaluation and Celery Beat wiring belong in `backend/app/workers/`. No unapproved `automation` module is added.
- Backend layering: PASS. Routers expose schedule and history endpoints; services own schedule validation, due-window resolution, retry classification, and delegation; repositories encapsulate persistence.
- Dependency injection: PASS. `imports/dependencies.py` and `ai_insights/dependencies.py` provide module-local service/repository wiring through FastAPI `Depends`.
- Configuration: PASS. Celery Beat scheduler settings are planned under `backend/app/settings/celery.py` or a focused worker settings file composed in `backend/app/core/config.py`.
- Database: PASS. Migrations are planned for schedule/history persistence. Existing source records remain authoritative and are not mutated except through existing import/AI processing services.
- API versioning: PASS. Contracts define `/api/v1/imports/schedules...` and `/api/v1/ai-insights/analysis-schedules...`; no unversioned production APIs are planned.
- Response contracts: PASS. Contracts use `{ "success": true, "data": ... }` and the unified handled error schema with stable error codes.
- Pagination: PASS. Schedule lists and run-history lists use bounded `page` and `limit` pagination with documented defaults and maximums.
- Observability: PASS. Scheduler, API, service, and worker logs include `request_id` or scheduler correlation IDs, schedule IDs, run IDs, owner IDs, due windows, retry counts, status transitions, and failure details.
- Security: PASS. Import schedule endpoints require `imports:read`/`imports:write`; AI analysis schedule endpoints require `ai_insights:read`/`ai_insights:write`; manual trigger and write operations have stricter rate limits than read endpoints.
- Background jobs: PASS. Celery Beat triggers thin scheduler tasks; import and AI worker tasks delegate business behavior to module services.
- Idempotency: PASS. Scheduled work deduplicates by owner + schedule + automation type + due window + target source/period; retries reuse the same scheduled run and never create duplicate imported tasks or duplicate current AI results.
- AI isolation: PASS. Scheduled AI analysis creates Phase 4 AI insight runs through `ai_insights`; no AI orchestration, prompts, or generated insight behavior is moved elsewhere.
- Soft delete: PASS. Schedule deletion is soft-delete-style removal from active evaluation while preserving run history and audit metadata.
- Audit trail: PASS. Schedule changes, scheduled executions, manual triggers, retry decisions, skipped windows, and terminal outcomes record actor or scheduler identity, timestamp, target, requested change/action, result, and failure details.
- Frontend boundaries: PASS. No frontend runtime work is planned. Future UI would belong under `frontend/features/automation/` or feature-specific frontend areas after a later approved spec.
- State/forms: PASS. No frontend state or form work is introduced.
- Testing: PASS. Plan requires service tests, API integration tests, repository tests, migration tests, worker tests, idempotency tests, missed-window tests, retry tests, response-shape tests, auth/rate-limit tests, and audit/logging checks.

## Project Structure

### Documentation (this feature)

```text
specs/007-automation-reliability/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- automation-api.yaml
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 6 backend ownership:

```text
backend/
|-- app/
|   |-- modules/
|   |   |-- imports/
|   |   |   |-- router.py
|   |   |   |-- schemas.py
|   |   |   |-- constants.py
|   |   |   |-- exceptions.py
|   |   |   |-- dependencies.py
|   |   |   |-- models.py
|   |   |   |-- repositories/
|   |   |   |   |-- import_run_repository.py
|   |   |   |   `-- import_schedule_repository.py
|   |   |   `-- services/
|   |   |       |-- csv_import_service.py
|   |   |       |-- import_schedule_service.py
|   |   |       `-- scheduled_import_service.py
|   |   `-- ai_insights/
|   |       |-- router.py
|   |       |-- schemas.py
|   |       |-- constants.py
|   |       |-- exceptions.py
|   |       |-- dependencies.py
|   |       |-- models.py
|   |       |-- repositories/
|   |       |   |-- ai_insight_run_repository.py
|   |       |   `-- ai_analysis_schedule_repository.py
|   |       `-- services/
|   |           |-- ai_insight_run_service.py
|   |           |-- ai_analysis_service.py
|   |           |-- ai_analysis_schedule_service.py
|   |           `-- scheduled_ai_analysis_service.py
|   |-- workers/
|   |   |-- celery_app.py
|   |   |-- scheduler.py
|   |   |-- schedule_windows.py
|   |   `-- tasks/
|   |       |-- scheduled_import_tasks.py
|   |       |-- scheduled_ai_analysis_tasks.py
|   |       `-- schedule_evaluator_tasks.py
|   |-- settings/
|   |   `-- celery.py
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
    |   |-- test_import_schedules_api.py
    |   `-- test_ai_analysis_schedules_api.py
    |-- domain/
    |   `-- test_schedule_window_rules.py
    |-- migrations/
    |   `-- test_automation_reliability_migration.py
    |-- repositories/
    |   |-- test_import_schedule_repository.py
    |   `-- test_ai_analysis_schedule_repository.py
    |-- services/
    |   |-- test_import_schedule_service.py
    |   |-- test_scheduled_import_service.py
    |   |-- test_ai_analysis_schedule_service.py
    |   `-- test_scheduled_ai_analysis_service.py
    `-- workers/
        |-- test_schedule_evaluator_worker.py
        |-- test_scheduled_import_worker.py
        `-- test_scheduled_ai_analysis_worker.py
```

No Phase 6 frontend source ownership is planned.

**Structure Decision**: Do not introduce `backend/app/modules/automation/`. Import scheduling is owned by `imports`; AI analysis scheduling is owned by `ai_insights`; reusable due-window calculations and Celery Beat task wiring are worker infrastructure. API composition continues through `backend/app/api/router.py` under existing `/api/v1/imports` and `/api/v1/ai-insights` prefixes.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 6 planning details:

- Keep schedule behavior in existing approved modules instead of adding an `automation` module.
- Use user-configured CSV source references for scheduled imports, while retaining metadata/outcomes only.
- Use Celery Beat to run thin due-window evaluator tasks that delegate to module services.
- Deduplicate scheduled work by owner, schedule, automation type, due window, and target source/period.
- Represent skipped/no-new-data windows as completed schedule-run history with an explicit outcome instead of fabricating import or AI results.
- Process only the latest missed due window after downtime and mark older windows skipped.
- Retain detailed automation run/audit information for 90 days, then allow pruning of non-current diagnostics while preserving final summaries.
- Split versioned APIs under existing imports and AI insight prefixes.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines import schedules, AI analysis schedules, schedule windows, schedule-run history, retry attempts, failure classification, audit/log events, validation rules, state transitions, idempotency, missed-window handling, soft delete, and retention.
- [contracts/automation-api.yaml](./contracts/automation-api.yaml): Defines versioned REST API contracts for import schedules, AI analysis schedules, manual trigger, schedule detail/update/delete, and paginated run history.
- [quickstart.md](./quickstart.md): Defines planning validation and later implementation smoke checks.

Database migrations are planned for import and AI analysis schedule persistence plus history/audit metadata. Existing `ImportRun` and `AIInsightRun` records remain the execution records for actual import/analysis work; schedule-run records link to them when a run is started.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts stay focused on Phase 6 automation and reliability and exclude frontend UI, automatic Phase 5 insight generation, export, Notion sync, chat, dashboard redesign, raw CSV retention, and arbitrary connectors.
- Backend modules: PASS. Data model and contracts assign import schedule behavior to `imports`, AI analysis schedule behavior to `ai_insights`, and common scheduler mechanics to `backend/app/workers/`.
- Backend layering: PASS. Contracts, data model, and quickstart preserve router/service/repository/database separation and thin worker delegation.
- Dependency injection: PASS. Planned dependencies are module-local and explicit.
- Configuration: PASS. Celery Beat settings are planned in backend settings and composed through core config.
- Database: PASS. Migration impact is identified for schedule/history records; source tracking records and generated AI result records are not mutated by schedule evaluation.
- API versioning, response contracts, pagination: PASS. Contract uses `/api/v1`, success/error envelopes, and `page`/`limit` pagination.
- Observability, audit, idempotency: PASS. Schedule/history records and contracts include owner, actor, schedule ID, run ID, due window, outcome, retry count, request/correlation ID, failure details, retention, and duplicate-window handling.
- Security: PASS. Contract defines `imports:read`, `imports:write`, `ai_insights:read`, and `ai_insights:write` scopes plus rate-limit expectations.
- Background jobs: PASS. Celery Beat and worker tasks remain thin and delegate to services.
- AI isolation: PASS. Scheduled AI behavior remains in `ai_insights`; no AI prompt/provider/result behavior is moved to workers or imports.
- Soft delete: PASS. Schedule deletion removes schedules from active evaluation while preserving history.
- Frontend boundaries and state/forms: PASS. No frontend work is planned.
- Testing: PASS. Backend service/API/repository/worker/migration tests are documented.

Ready for `/speckit.tasks`.
