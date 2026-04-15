# Implementation Plan: CSV Import Pipeline

**Branch**: `003-csv-import-pipeline` | **Date**: 2026-04-15 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-csv-import-pipeline/spec.md`

**Note**: This plan covers Phase 2 only. It plans manual CSV import preview, validation, normalization, confirmed async import execution, import status/history APIs, and row-level traceability. Dashboard screens, AI analysis execution, scheduled imports, Notion API synchronization, and report export remain out of scope.

## Summary

Phase 2 converts Notion-compatible CSV exports into structured daily tracking records while preserving data quality. The technical approach is to extend the existing `imports` backend module with CSV parsing, preview, validation, import execution, API contracts, and thin worker orchestration. The pipeline reuses Phase 1 `DailyLogService`, `TaskService`, `NoteService`, and `ImportTraceService` so daily-log reuse, category reuse, task deduplication, tag normalization, note handling, run statuses, and row outcomes stay centralized.

Preview remains side-effect free: it parses and validates uploaded CSV data but does not create tracking records or ImportRun records. Confirmed imports create an ImportRun, parse and normalize the submitted CSV server-side, enqueue normalized row payloads for background processing, and avoid retaining the full raw CSV file after import history is recorded.

## Technical Context

**Language/Version**: Python >=3.12 from `backend/pyproject.toml`; frontend TypeScript/Next.js remains out of runtime scope for Phase 2 unless tasks add a minimal route shell later.  
**Primary Dependencies**: Existing backend dependencies include FastAPI, SQLAlchemy Async, Alembic, asyncpg, and pydantic-settings. Phase 2 requires adding Celery, Redis client support, and multipart upload support for CSV endpoints; CSV parsing uses Python standard library `csv`; date parsing uses standard ISO parsing plus explicit Notion-style formats.  
**Storage**: PostgreSQL target with existing Phase 1 tables for `DailyLog`, `Task`, `Category`, `Note`, `ImportRun`, and `ImportRowOutcome`; Redis is required as the Celery broker/result backend for confirmed imports. No raw CSV file storage is planned.  
**Testing**: Current backend test command is `cd backend; pytest -q`. Phase 2 tasks should add targeted tests under `backend/tests/domain`, `backend/tests/repositories`, `backend/tests/api`, and `backend/tests/workers`, then validate with `cd backend; pytest tests/domain tests/repositories tests/api tests/workers -q`.  
**Target Platform**: Backend modular monolith in the existing monorepo, intended for Docker Compose local orchestration with backend, PostgreSQL, Redis, and Celery worker services.  
**Project Type**: Backend API and worker phase inside a FastAPI REST + future Next.js dashboard product.  
**Performance Goals**: Preview returns a validation result for personal-tracker CSV files up to 5,000 rows in under 5 seconds on a local development machine; confirmed import submission returns an ImportRun identifier in under 2 seconds after server-side validation and enqueue; completed import history can be reviewed in under 2 minutes after processing completes.  
**Constraints**: Stay inside Phase 2 CSV import scope; do not add dashboard visualization, AI execution, scheduled imports, Notion API sync, or report export. Routers remain thin, services own parsing/validation/execution rules, repositories own persistence, Celery tasks delegate to services, and full raw CSV file contents are not retained.  
**Scale/Scope**: Personal v1 workspace with one owner initially. CSV contract is limited to required columns `date`, `task`, `category`, `time_spent_minutes` and optional `tags`, `notes`. Dates accept ISO dates and common Notion date text; tags are comma-separated; deduplication uses date + normalized task name + time spent.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to CSV preview, validation, normalization, confirmed import execution, status/history, and row traceability.
- Backend modules: PASS. Feature code belongs in `backend/app/modules/imports/` with reuse of existing `daily_logs`, `tasks`, and `notes` services.
- Backend layering: PASS. Routers call import services; services coordinate parsing and domain services; repositories encapsulate ImportRun and row-outcome queries.
- Dependency injection: PASS. `backend/app/modules/imports/dependencies.py` owns provider wiring for import services, repositories, and cross-module services.
- Configuration: PASS. Redis and Celery settings are planned under `backend/app/settings/` and composed in `backend/app/core/config.py`.
- Database: PASS. Existing Phase 1 persistence is reused. New migrations are required only if implementation adds import idempotency, source hash, or status index fields not already present.
- API versioning: PASS. Runtime endpoints are planned under `/api/v1/imports`.
- Response contracts: PASS. Contracts require `{ "success": true, "data": ... }` for handled JSON success responses and the unified handled error schema.
- Pagination: PASS. Import-run history and row-outcome list endpoints use `page` and `limit` with defaults and maximums documented in the API contract.
- Observability: PASS. Import logs include `request_id`, `import_run_id`, row counts, status transitions, and failure details.
- Security: PASS. Import endpoints define `imports:write` and `imports:read` scopes plus rate-limit expectations. Until the auth module is implemented, tests should override a current-owner dependency rather than accepting owner identity from user-controlled payloads.
- Background jobs: PASS. Celery tasks stay thin and delegate import processing to services.
- Idempotency: PASS. The same ImportRun retry must not create duplicate tasks; task-level deduplication by date + normalized task name + time spent is the final guard.
- AI isolation: PASS. No AI module behavior is planned.
- Soft delete: PASS. ImportRun history remains audit-sensitive and soft-delete-capable through Phase 1 models; deletion behavior is not exposed in this phase.
- Audit trail: PASS. Confirmed imports record actor/owner, source metadata, status, timing, row counts, row outcomes, and failure details without retaining raw CSV files.
- Frontend boundaries: PASS. No production frontend runtime work is required. Future UI belongs in `frontend/features/imports/` and `frontend/app/` composition only.
- State/forms: PASS. No frontend state or forms are required by this backend plan.
- Testing: PASS. Plan requires service tests, API contract tests, worker tests, idempotency tests, row-outcome tests, and response-shape tests.

## Project Structure

### Documentation (this feature)

```text
specs/003-csv-import-pipeline/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- import-api.yaml
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 2 backend ownership:

```text
backend/
|-- app/
|   |-- core/
|   |   |-- config.py
|   |   |-- database.py
|   |   |-- exceptions.py
|   |   `-- logging.py
|   |-- settings/
|   |   |-- redis.py
|   |   `-- celery.py
|   |-- shared/
|   |   |-- schemas/
|   |   |   `-- responses.py
|   |   `-- enums/
|   |       |-- run_status.py
|   |       `-- source.py
|   |-- modules/
|   |   |-- imports/
|   |   |   |-- router.py
|   |   |   |-- schemas.py
|   |   |   |-- constants.py
|   |   |   |-- exceptions.py
|   |   |   |-- dependencies.py
|   |   |   |-- utils.py
|   |   |   |-- services/
|   |   |   |   |-- csv_parser_service.py
|   |   |   |   |-- import_preview_service.py
|   |   |   |   |-- csv_import_service.py
|   |   |   |   `-- import_trace_service.py
|   |   |   `-- repositories/
|   |   |       `-- import_run_repository.py
|   |   |-- daily_logs/
|   |   |-- tasks/
|   |   `-- notes/
|   |-- workers/
|   |   |-- celery_app.py
|   |   `-- tasks/
|   |       `-- import_tasks.py
|   |-- api/
|   |   `-- router.py
|   `-- main.py
`-- tests/
    |-- domain/
    |   `-- test_csv_import_pipeline.py
    |-- api/
    |   `-- test_import_api.py
    |-- workers/
    |   `-- test_import_worker.py
    `-- repositories/
        `-- test_import_run_repository.py
```

Frontend files remain out of Phase 2 runtime scope. If a future task adds a minimal import page shell, it must stay under `frontend/app/imports/` for routing and `frontend/features/imports/` for feature logic.

**Structure Decision**: Implement CSV pipeline behavior in the existing `backend/app/modules/imports/` module. Add runtime API composition only through `backend/app/api/router.py` and `backend/app/main.py` if those are still placeholders. Do not add Phase 2 feature logic to root `backend/main.py` or `backend/src/main.py`.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 2 planning details:

- Preview parses and validates CSV data without creating ImportRun records or tracking records.
- Confirmed imports parse the submitted CSV again, create ImportRun records, and enqueue normalized row payloads rather than retaining raw CSV files.
- Standard library CSV parsing is sufficient for the Notion-compatible CSV contract.
- Date parsing accepts ISO dates and explicit Notion-style date text.
- Tags split on commas and normalize into unique lowercase trimmed values.
- Celery + Redis handle confirmed import execution, with thin worker tasks delegating to import services.
- API endpoints use `/api/v1/imports`, standard success/error envelopes, auth scopes, rate limits, and page/limit pagination for history.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines parsed row value objects, preview result shape, confirmed import command, ImportRun usage, row outcome details, validation rules, and status transitions.
- [contracts/import-api.yaml](./contracts/import-api.yaml): Defines versioned REST API contracts for preview, confirm import, import history, import status, and row outcomes.
- [quickstart.md](./quickstart.md): Defines manual validation steps for the planning artifacts and later implementation output.

No frontend contract is generated because Phase 2 planning focuses on backend import APIs and worker execution. Future dashboard UI work remains Phase 3+ unless a later spec explicitly authorizes a frontend import page.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts remain focused on CSV import preview, execution, status, and traceability.
- Backend modules: PASS. Artifacts assign feature behavior to the `imports` module and reuse existing cross-module services through dependency wiring.
- Backend layering: PASS. API, service, worker, repository, and model responsibilities are separated.
- Dependency injection: PASS. Service/provider wiring belongs in `imports/dependencies.py`; tests can override owner/context dependencies.
- Configuration and database: PASS. Redis/Celery settings are planned; existing database models are reused unless implementation needs narrowly scoped migration additions.
- API versioning, response contracts, pagination: PASS. Contracts use `/api/v1/imports`, success/error envelopes, and page/limit pagination.
- Observability, audit, idempotency: PASS. ImportRun IDs, status transitions, row counts, row outcomes, request IDs, and duplicate guards are specified.
- Security: PASS. Contracts define `imports:write`, `imports:read`, and rate limits.
- Background jobs: PASS. Worker tasks are thin and delegate to services.
- AI isolation: PASS. No AI behavior is introduced.
- Soft delete: PASS. No delete endpoint is introduced; import history remains traceability-sensitive.
- Frontend boundaries and state/forms: PASS. No frontend runtime work is planned.
- Testing: PASS. Service, API, worker, repository, idempotency, response shape, and error shape tests are documented.

Ready for `/speckit.tasks`.
