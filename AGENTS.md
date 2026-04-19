# FocusPulse Development Guidelines

Auto-generated from feature plans and adjusted for the current skeleton-only Phase 0 state. Last updated: 2026-04-19.

## Active Technologies
- Phase 1 backend planning target: Python >=3.12, FastAPI, SQLAlchemy Async, Alembic, PostgreSQL, UUID primary keys, JSON task tags, normalized categories, soft-delete-capable traceability records, and pytest-compatible backend tests.
- Phase 1 excludes frontend runtime work; Next.js/Tailwind/shadcn/TanStack Query/React Hook Form/Zod/Axios/Recharts remain approved future stack items.
- Phase 2 backend planning target: Python >=3.12, FastAPI, SQLAlchemy Async, Alembic, PostgreSQL, existing Phase 1 daily tracking/import traceability tables, Celery, Redis, multipart CSV upload support, standard-library CSV parsing, explicit ISO/Notion-style date parsing, and pytest-compatible backend/API/worker tests.
- Phase 2 excludes frontend runtime work unless a later task adds a minimal import route shell; full dashboard visualization remains Phase 3+.
- Phase 3 dashboard planning target: Python >=3.12 backend read APIs plus the approved Next.js App Router/TypeScript frontend stack, with Tailwind CSS, shadcn/ui, TanStack Query, Zod, Axios, and Recharts.
- Phase 3 storage target: existing PostgreSQL `DailyLog`, `Task`, `Category`, and `Note` tables; no new persistent dashboard tables by default, and Redis/Celery remain available but unused for dashboard reads.
- Phase 4 AI analysis planning target: Python >=3.12 backend APIs, Celery/Redis async execution, existing Phase 1-3 domain modules, AI provider adapter isolated in `backend/app/modules/ai_insights/`, shared run statuses, and pytest-compatible backend/API/worker tests.
- Phase 4 storage target: existing PostgreSQL `DailyLog`, `Task`, `Category`, `Note`, `AIInsightRun`, and `AIInsightRunSource` tables, with planned AI run metadata for instruction version, output outcome, retry count, idempotency key, and failure details.

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
- `005-ai-analysis-engine`: Added Phase 4 plan artifacts for combined daily/weekly AI analysis runs, privacy-bounded input summaries, stored outputs, reruns, retries, and traceable failures.
- `004-dashboard-foundation`: Added Phase 3 plan artifacts for read-only dashboard analytics APIs, day detail retrieval, period filters, chart-ready payloads, and frontend dashboard bootstrap.
- `003-csv-import-pipeline`: Added Phase 2 plan artifacts for CSV preview, validation, normalization, confirmed async import execution, status/history APIs, row outcomes, and raw CSV non-retention.
- `002-core-domain-data-model`: Added Phase 1 plan artifacts for backend domain models, persistence rules, traceability contracts, and validation expectations.
- `001-foundation-architecture`: Added Phase 0 plan artifacts for the foundation package and skeleton-only repository setup.

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
