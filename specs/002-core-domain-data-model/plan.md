# Implementation Plan: Core Domain & Data Model

**Branch**: `002-core-domain-data-model` | **Date**: 2026-04-14 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-core-domain-data-model/spec.md`

**Note**: This plan covers Phase 1 only. It plans the backend domain model, persistence rules, repository/service contracts, migrations, and validation tests for daily tracking data. It does not plan CSV upload flows, dashboard screens, AI execution, scheduled automation, or production reliability workflows.

## Summary

Phase 1 defines and implements the core data model for FocusPulse daily tracking: `DailyLog`, `Task`, `Category`, task-level JSON tags, optional task notes, traceable `ImportRun` history, row-level import outcomes, and traceable `AIInsightRun` history for daily and weekly analysis runs. The technical approach is to implement SQLAlchemy Async ORM models and Alembic migrations under the approved `backend/app` modular monolith layout, keep business rules in services, keep persistence in repositories, and expose no production REST endpoints beyond any minimal internal contract needed by implementation tests.

## Technical Context

**Language/Version**: Python >=3.12 from `backend/pyproject.toml`; frontend TypeScript/Next.js remains out of scope for Phase 1 implementation.  
**Primary Dependencies**: Existing backend dependency is FastAPI. Phase 1 implementation requires adding SQLAlchemy Async, Alembic, async PostgreSQL driver, pydantic-settings if core config is introduced, and pytest-compatible test tooling for service/repository/migration validation. Celery, Redis, Next.js, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Axios, and Recharts remain approved stack items but are not required for this phase's runtime behavior.  
**Storage**: PostgreSQL target with UUID primary keys, JSON array storage for task tags, normalized `Category` records, soft-delete-capable user-owned and audit-sensitive records, and Alembic migrations.  
**Testing**: Current repo has no required Phase 1 test command yet. Phase 1 tasks should add backend test dependencies and define a command such as `cd backend; pytest tests/domain tests/repositories -q` once tests exist. Until then, planning verification is document inspection plus migration/model review.  
**Target Platform**: Monorepo intended for Docker Compose local orchestration. Current `docker-compose.yml` is a Phase 0 placeholder; Phase 1 may add PostgreSQL service configuration only if needed to validate migrations locally.  
**Project Type**: Backend-focused modular monolith phase inside a FastAPI REST + Next.js dashboard product.  
**Performance Goals**: Reviewers can validate the domain relationships and traceability rules in under 10 minutes; date-range daily-log reads and day/category/tag total calculations are modeled so later dashboard queries can be implemented without schema redesign.  
**Constraints**: Stay inside Phase 1 domain/data-model scope; no CSV upload UI, parsing pipeline, background job execution, dashboard pages, AI prompt execution, scheduled imports, scheduled AI runs, or production monitoring. Preserve `backend/app` target layout and do not add new feature logic to pre-existing placeholder `backend/src/` or root `backend/main.py`.  
**Scale/Scope**: Personal v1 workspace with one owner initially, but records include owner/audit fields where needed so future auth and multi-user work does not require a destructive schema redesign.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan is limited to core domain entities, persistence, repositories/services, migrations, and tests.
- Backend modules: PASS. Planned work stays in `backend/app/modules/daily_logs/`, `backend/app/modules/tasks/`, `backend/app/modules/notes/`, `backend/app/modules/imports/`, and `backend/app/modules/ai_insights/`.
- Backend layering: PASS. Domain rules are planned for services; persistence is planned for repositories and models.
- Dependency injection: PASS. Any service/repository providers belong in module `dependencies.py`; no router dependency wiring is required unless implementation adds internal endpoints.
- Configuration: PASS. Database settings are planned under `backend/app/settings/` and composed through `backend/app/core/config.py` if missing.
- Database: PASS. Persistence changes require SQLAlchemy models and Alembic migrations; `backend/app/core/database.py` remains the single database wiring source.
- API versioning: PASS. No production REST endpoint is required by Phase 1. If implementation adds minimal inspection endpoints, they must be under `/api/v1/`.
- Response contracts: PASS. No handled JSON response contract is required unless endpoints are added; any added handled JSON endpoint must use the standard success/error envelope.
- Pagination: PASS. No list endpoint is required. Repository/service date-range reads should be designed so later bounded page/list endpoints can document pagination in Phase 3.
- Observability: PASS. Import and AI run models include persisted status, timing, row/source summaries, and failure details; structured logging implementation is deferred.
- Security: PASS. No protected endpoints are introduced. Models include owner/audit fields where applicable for later JWT/auth integration.
- Background jobs: PASS. ImportRun and AIInsightRun records are modeled for future async work, but no Celery tasks are implemented in this phase.
- Idempotency: PASS. DailyLog uniqueness and task deduplication by date + normalized task name + time spent are planned as model/service constraints for future import retries.
- AI isolation: PASS. AIInsightRun storage remains in `backend/app/modules/ai_insights/` and never mutates source logs, tasks, notes, categories, or imports.
- Soft delete: PASS. User-owned and audit-sensitive records define `deleted_at` behavior where deletion can affect traceability; hard deletion is out of scope.
- Audit trail: PASS. ImportRun, ImportRowOutcome, and AIInsightRun include actor/owner, timing, requested/source context, status, and failure details.
- Frontend boundaries: PASS. No frontend application code is planned for Phase 1.
- State/forms: PASS. No frontend state or forms are planned.
- Testing: PASS. Plan requires service/repository/model tests and migration verification; endpoint integration tests are only required if implementation adds endpoints.

## Project Structure

### Documentation (this feature)

```text
specs/002-core-domain-data-model/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- domain-data-contract.md
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Planned Phase 1 backend ownership:

```text
backend/
|-- app/
|   |-- core/
|   |   |-- config.py
|   |   `-- database.py
|   |-- settings/
|   |   `-- database.py
|   |-- shared/
|   |   |-- models/
|   |   |   `-- base.py
|   |   |-- enums/
|   |   |   `-- run_status.py
|   |   `-- schemas/
|   |       `-- responses.py
|   |-- modules/
|   |   |-- daily_logs/
|   |   |   |-- models.py
|   |   |   |-- schemas.py
|   |   |   |-- services/
|   |   |   |   `-- daily_log_service.py
|   |   |   |-- repositories/
|   |   |   |   `-- daily_log_repository.py
|   |   |   `-- dependencies.py
|   |   |-- tasks/
|   |   |   |-- models.py
|   |   |   |-- schemas.py
|   |   |   |-- services/
|   |   |   |   `-- task_service.py
|   |   |   |-- repositories/
|   |   |   |   `-- task_repository.py
|   |   |   `-- dependencies.py
|   |   |-- notes/
|   |   |   |-- models.py
|   |   |   |-- services/
|   |   |   |   `-- note_service.py
|   |   |   `-- repositories/
|   |   |       `-- note_repository.py
|   |   |-- imports/
|   |   |   |-- models.py
|   |   |   |-- schemas.py
|   |   |   |-- services/
|   |   |   |   `-- import_trace_service.py
|   |   |   |-- repositories/
|   |   |   |   `-- import_run_repository.py
|   |   |   `-- dependencies.py
|   |   `-- ai_insights/
|   |       |-- models.py
|   |       |-- schemas.py
|   |       |-- services/
|   |       |   `-- ai_insight_run_service.py
|   |       |-- repositories/
|   |       |   `-- ai_insight_run_repository.py
|   |       `-- dependencies.py
|   `-- api/
|       `-- router.py
|-- alembic/
|   |-- env.py
|   `-- versions/
|       `-- <revision>_core_domain_data_model.py
`-- tests/
    |-- domain/
    |-- repositories/
    `-- migrations/
```

No frontend files are planned for this phase.

**Structure Decision**: Phase 1 implementation should use the existing `backend/app` skeleton created by Phase 0. Pre-existing `backend/src/main.py` and root `backend/main.py` remain placeholders and must not receive Phase 1 feature logic. If implementation discovers missing core files such as `backend/app/core/database.py`, tasks should create them before adding module models and repositories.

## Complexity Tracking

No constitution violations are required.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolved Phase 1 planning details:

- Model ownership is split across domain modules while preserving cross-module relationships.
- Tags are stored as a normalized JSON array on `Task`.
- Categories are normalized in a dedicated table.
- DailyLog uniqueness uses owner + calendar date.
- Duplicate imported tasks are skipped based on date + normalized task name + time spent.
- Import row outcomes are stored for invalid, skipped, and failed rows.
- ImportRun and AIInsightRun share a run status vocabulary.
- AIInsightRun supports daily and weekly target periods only for v1.
- Soft delete and audit fields are included for traceable records.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines database entities, fields, relationships, validation rules, uniqueness rules, state transitions, and soft-delete behavior.
- [contracts/domain-data-contract.md](./contracts/domain-data-contract.md): Defines repository/service contracts and optional REST response constraints if inspection endpoints are later added in this phase.
- [quickstart.md](./quickstart.md): Defines manual validation steps for plan artifacts and future implementation output.

No frontend contract is generated because Phase 1 does not introduce dashboard screens or frontend state. No OpenAPI contract is required unless implementation adds versioned inspection endpoints; in that case, the contract in `contracts/domain-data-contract.md` governs response shape and error behavior.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts remain focused on persistence and domain behavior.
- Backend modules: PASS. Artifacts assign models/services/repositories to approved modules.
- Backend layering: PASS. Contracts separate services from repositories and keep routing optional.
- Dependency injection: PASS. Dependencies are only planned at module boundaries.
- Configuration and database: PASS. Core database wiring and Alembic migration impact are planned.
- API versioning, response contracts, pagination: PASS. No mandatory runtime endpoints are introduced; optional endpoints must follow constitution rules.
- Observability, audit, idempotency: PASS. Run records, row outcomes, status fields, timing, actor/owner fields, and dedupe rules are specified.
- Security: PASS. No auth surface is introduced; owner fields support later auth.
- Background jobs: PASS. Run records are modeled, but job execution remains out of scope.
- AI isolation: PASS. AIInsightRun remains in the AI module and source data is authoritative.
- Soft delete: PASS. Deletion behavior is specified for traceability-sensitive records.
- Frontend boundaries and state/forms: PASS. No frontend changes are planned.
- Testing: PASS. Service, repository, and migration test expectations are documented.

Ready for `/speckit.tasks`.
