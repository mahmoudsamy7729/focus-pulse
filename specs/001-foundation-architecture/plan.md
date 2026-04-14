# Implementation Plan: Foundation & Architecture

**Branch**: `001-foundation-architecture` | **Date**: 2026-04-14 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-foundation-architecture/spec.md`

**Note**: This plan covers Phase 0 only. It plans the foundation package and skeleton repository setup needed to make future architecture boundaries visible; it does not plan runnable backend/frontend app shells, domain behavior, schemas, workers, dashboards, import logic, AI logic, CI, or quality gate enforcement.

## Summary

Phase 0 creates a foundation package for FocusPulse: finalized project purpose, v1 scope boundaries, architecture rules, naming conventions, practical v1 non-functional baselines, AI source-data boundaries, and skeleton-only repository setup. The technical approach is to align documentation and placeholder repository structure with the modular monolith defined in the constitution and `docs/STACK_AND_STRUCTURE.md`, while explicitly deferring executable application behavior to later phases.

## Technical Context

**Language/Version**: Python >=3.12 is present in `backend/pyproject.toml`; TypeScript/Next.js are approved for the frontend but not bootstrapped in Phase 0.  
**Primary Dependencies**: Approved stack is FastAPI, SQLAlchemy Async, Alembic, PostgreSQL, Celery, Redis, Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Axios, and Recharts. Phase 0 does not install or require these beyond existing repository metadata.  
**Storage**: PostgreSQL is the approved future database; Redis is the approved future background job infrastructure. Phase 0 creates no schema, migrations, queues, or durable data.  
**Testing**: Phase 0 verification is document and structure inspection against this plan, quickstart, and artifact contract. Automated test/lint/type-check gates are deferred because the clarified spec limits setup to skeleton-only artifacts.  
**Target Platform**: Monorepo intended for local Docker Compose orchestration with future backend, frontend, postgres, redis, celery worker, and later celery beat services. Phase 0 may include compose placeholders only.  
**Project Type**: Monorepo web application foundation for a FastAPI REST backend, Next.js dashboard frontend, PostgreSQL persistence, Redis/Celery background work, and isolated AI insights module.  
**Performance Goals**: Reviewers can inspect the Phase 0 skeleton and identify intended module locations in under 10 minutes; reviewers can classify proposed v1 tasks as in scope, out of scope, or requiring amendment without undocumented assumptions.  
**Constraints**: Skeleton-only setup; no runnable app shells, production domain behavior, database schema, worker behavior, import logic, dashboard behavior, AI analysis behavior, CI workflows, or quality gate enforcement.  
**Scale/Scope**: Personal productivity v1 for a single primary user or small personal workspace; Phase 0 covers governance and skeleton structure only.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: PASS. Plan stays within Phase 0 and defers Phase 1+ implementation.
- Backend modules: PASS. Skeleton paths use the constitution's `backend/app/modules/<feature>/` target layout; no feature logic is added.
- Backend layering: PASS. The plan documents Router -> Service -> Repository -> Database boundaries and creates only placeholders.
- Dependency injection: PASS. No executable dependency wiring is introduced in Phase 0.
- Configuration: PASS. Skeleton setup reserves `backend/app/settings/` and `backend/app/core/config.py` as future configuration locations.
- Database: PASS. PostgreSQL/Alembic are documented as future persistence choices; no schema or migration is introduced.
- API versioning: PASS. No production API endpoints are planned.
- Response contracts: PASS. No handled JSON responses or errors are introduced.
- Pagination: PASS. No list endpoints are introduced.
- Observability: PASS. Practical v1 traceability expectations are documented; structured logging implementation is deferred.
- Security: PASS. No protected endpoints are introduced.
- Background jobs: PASS. Celery/Redis boundaries are reserved; no tasks are implemented.
- Idempotency: PASS. Future import, AI-run, report, and job idempotency expectations are documented.
- AI isolation: PASS. AI can read validated productivity data and write separate insight outputs later, but cannot mutate source logs, tasks, or imports.
- Soft delete: PASS. No deletion behavior is implemented in Phase 0.
- Audit trail: PASS. Import and AI traceability expectations are documented for future phases.
- Frontend boundaries: PASS. Skeleton paths reserve `frontend/app/`, `frontend/features/`, and `frontend/lib/api/` responsibilities.
- State/forms: PASS. TanStack Query and React Hook Form + Zod remain documented future choices; no client behavior is implemented.
- Testing: PASS. Service/API tests are not applicable because Phase 0 creates no service or endpoint behavior.

## Project Structure

### Documentation (this feature)

```text
specs/001-foundation-architecture/
|-- plan.md
|-- research.md
|-- data-model.md
|-- quickstart.md
|-- contracts/
|   `-- foundation-package.md
|-- checklists/
|   `-- requirements.md
`-- spec.md
```

### Source Code (repository root)

Target skeleton layout to plan for Phase 0:

```text
backend/
|-- app/
|   |-- api/
|   |-- core/
|   |-- modules/
|   |   |-- auth/
|   |   |-- daily_logs/
|   |   |-- tasks/
|   |   |-- notes/
|   |   |-- imports/
|   |   |-- analytics/
|   |   |-- ai_insights/
|   |   `-- reports/
|   |-- settings/
|   |-- shared/
|   |-- workers/
|   `-- main.py
|-- alembic/
|-- tests/
`-- README.md

frontend/
|-- app/
|-- components/
|-- features/
|   |-- auth/
|   |-- daily-logs/
|   |-- tasks/
|   |-- notes/
|   |-- imports/
|   |-- analytics/
|   |-- ai-insights/
|   `-- reports/
|-- hooks/
|-- lib/
|   `-- api/
|-- public/
|-- stores/
`-- types/

docker/
|-- nginx/
`-- scripts/

docs/
|-- Plan.md
|-- STACK_AND_STRUCTURE.md
`-- FOUNDATION.md

.env.example
docker-compose.yml
README.md
```

**Structure Decision**: Phase 0 tasks should create or align skeleton-only directories and placeholder documentation around `backend/app/`, `frontend/`, `docker/`, and `docs/FOUNDATION.md`. The current repository has `backend/src/` and root `backend/main.py`, which are not the target constitution layout. Phase 0 should not add feature logic to those paths; it should either leave them as pre-existing placeholders and document the target alignment, or move placeholder-only files during implementation if no user work would be overwritten.

## Complexity Tracking

No constitution violations are required. Phase 0 intentionally avoids runnable app shells, API endpoints, database schemas, domain services, worker tasks, and frontend screens.

## Phase 0: Outline & Research

Research completed in [research.md](./research.md). Decisions resolve the only planning ambiguities relevant to this feature:

- Phase 0 is a foundation package, not a feature implementation.
- Repo setup is skeleton-only.
- Naming conventions are locked.
- Practical v1 quality baselines are documented.
- AI source-data mutation is prohibited.
- Current repo layout needs alignment to the constitution target.

## Phase 1: Design & Contracts

Design artifacts:

- [data-model.md](./data-model.md): Defines planning entities such as Foundation Package, Architecture Rule, Scope Boundary, Platform Decision, Naming Convention, Non-Functional Baseline, AI Boundary, and Skeleton Artifact.
- [contracts/foundation-package.md](./contracts/foundation-package.md): Defines the artifact contract reviewers will use to validate the Phase 0 foundation package.
- [quickstart.md](./quickstart.md): Defines manual validation steps for the generated Phase 0 artifacts and future implementation output.

No OpenAPI or runtime API contract is generated because Phase 0 exposes no application endpoints.

## Post-Design Constitution Check

- Phase scope: PASS. Design artifacts remain planning/skeleton-only.
- Backend modules: PASS. Planned module names match snake_case backend conventions and approved module list.
- Backend layering: PASS. No executable layers are introduced; boundaries are documented.
- Dependency injection: PASS. No DI implementation is introduced.
- Configuration: PASS. Settings/core placeholders are planned without executable config behavior.
- Database: PASS. No models, migrations, or storage are introduced.
- API versioning, response contracts, pagination: PASS. No endpoints are introduced.
- Observability, audit, idempotency: PASS. Practical v1 expectations are documented for later phases.
- Security: PASS. No auth surfaces are introduced.
- Background jobs: PASS. Worker boundaries are reserved without Celery task behavior.
- AI isolation: PASS. Contract states AI reads validated data and writes separate outputs only.
- Frontend boundaries: PASS. Skeleton directories reserve app, feature, API, and shared UI ownership.
- Testing: PASS. Verification is document/structure inspection; automated gates are deferred by clarified scope.

Ready for `/speckit.tasks`.
