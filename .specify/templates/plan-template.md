# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python backend + TypeScript frontend, exact versions from repo files or NEEDS CLARIFICATION
**Primary Dependencies**: FastAPI, SQLAlchemy Async, Alembic, Celery, Redis, Next.js App Router, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Axios, Recharts
**Storage**: PostgreSQL with UUID primary keys; Redis for background job infrastructure
**Testing**: [Use repo-defined commands if present, otherwise NEEDS CLARIFICATION]
**Target Platform**: Docker Compose monorepo with backend, frontend, postgres, redis, and celery worker services
**Project Type**: Monorepo web application: FastAPI REST backend + Next.js dashboard frontend
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- Phase scope: Plan stays within the current Spec Kit phase and does not pull in future extensions.
- Backend modules: Feature code is placed under `backend/app/modules/<feature>/` and uses the documented module layout.
- Backend layering: Router -> Service -> Repository -> Database is preserved; routers have no business or DB logic.
- Dependency injection: FastAPI `Depends` wiring is explicit from routers to services to repositories to `AsyncSession`.
- Configuration: Domain settings live in `backend/app/settings/` and are composed in `backend/app/core/config.py`.
- Database: Engine/session/Base setup stays centralized in `backend/app/core/database.py`; migrations are planned for persistence changes.
- API versioning: New or changed REST endpoints are registered under `/api/v1/`, `/api/v2/`, etc.; no unversioned production APIs.
- Response contracts: Handled JSON success responses use `{ "success": true, "data": ... }`; handled errors use the unified error schema with stable error codes and explicit HTTP status mappings.
- Pagination: List endpoints define `page` and `limit` for bounded page navigation or `cursor` for large, high-churn, append-only, or infinite-scroll lists.
- Observability: Structured logs include `request_id`; imports, AI runs, and admin actions remain traceable through audit records and persisted status/error details.
- Security: Protected endpoints define JWT auth scopes or permissions and rate-limit expectations.
- Background jobs: Celery tasks are thin and delegate use-case behavior to services.
- Idempotency: Imports, AI runs, reports, and background jobs define a deduplication or idempotency-key strategy.
- AI isolation: Agent orchestration, prompts, tools, and run storage remain inside `backend/app/modules/ai_insights/`.
- Soft delete: User-owned, imported, generated AI, and audit-sensitive records define soft delete, restore, and audit behavior when deletion is in scope.
- Audit trail: Imports, AI runs, and admin actions record actor, timestamp, requested or changed data, resulting status, and relevant failure details.
- Frontend boundaries: `frontend/app/` handles routing and composition; feature logic stays in `frontend/features/`; API client code stays in `frontend/lib/api/`.
- State/forms: TanStack Query handles server state; React Hook Form + Zod handle form validation.
- Testing: Service changes include unit tests; API endpoint changes include integration tests covering success/error shape, pagination, status codes, auth, audit trails, and relevant idempotency or soft delete behavior.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
|-- app/
|   |-- core/
|   |-- shared/
|   |-- settings/
|   |-- modules/
|   |   `-- <feature>/
|   |       |-- router.py
|   |       |-- schemas.py
|   |       |-- services/
|   |       |-- repositories/
|   |       |-- models.py
|   |       |-- dependencies.py
|   |       |-- utils.py
|   |       |-- exceptions.py
|   |       |-- constants.py
|   |       `-- shared/
|   |-- workers/
|   |-- api/
|   `-- main.py
|-- alembic/
`-- tests/

frontend/
|-- app/
|-- components/
|-- features/
|-- lib/
|-- hooks/
|-- stores/
|-- types/
`-- public/

docker/
docs/
```

**Structure Decision**: [Document the backend modules, frontend feature areas,
and exact files touched for this feature. If current folders are not yet aligned
with the documented `backend/app` and `frontend/` structure, include alignment
tasks instead of adding feature logic to the wrong layout.]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
