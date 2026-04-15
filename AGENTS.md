# FocusPulse Development Guidelines

Auto-generated from feature plans and adjusted for the current skeleton-only Phase 0 state. Last updated: 2026-04-14.

## Active Technologies
- Phase 1 backend planning target: Python >=3.12, FastAPI, SQLAlchemy Async, Alembic, PostgreSQL, UUID primary keys, JSON task tags, normalized categories, soft-delete-capable traceability records, and pytest-compatible backend tests.
- Phase 1 excludes frontend runtime work; Next.js/Tailwind/shadcn/TanStack Query/React Hook Form/Zod/Axios/Recharts remain approved future stack items.

- Backend target: Python >=3.12, FastAPI, SQLAlchemy Async, Alembic, PostgreSQL, Celery, Redis.
- Frontend target: Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Axios, Recharts.
- Phase 0 constraint: dependencies and runnable app shells are not required by the foundation plan.

## Project Structure

```text
backend/
frontend/
docker/
docs/
specs/
```

## Commands

- Phase 0 has no required test, lint, type-check, or dev-server command.
- Validate Phase 0 by reviewing `specs/001-foundation-architecture/quickstart.md`.

## Code Style

- Backend modules use snake_case.
- Spec and branch names use kebab-case with the numeric feature prefix.
- Domain entities use PascalCase.
- Background job names are descriptive.

## Recent Changes
- `002-core-domain-data-model`: Added Phase 1 plan artifacts for backend domain models, persistence rules, traceability contracts, and validation expectations.

- `001-foundation-architecture`: Added Phase 0 plan artifacts for the foundation package and skeleton-only repository setup.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
