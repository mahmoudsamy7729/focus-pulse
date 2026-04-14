# FocusPulse Foundation

Last updated: 2026-04-14

## Phase 0 Boundary

Phase 0 defines the foundation package for FocusPulse. It documents product
purpose, v1 scope, out-of-scope future work, architecture rules, naming
conventions, practical non-functional baselines, AI boundaries, and the
skeleton-only repository setup.

Phase 0 does not create runnable backend or frontend app shells. It also does
not create API endpoints, database schemas, migrations, worker tasks, import
logic, dashboard screens, AI insight execution, CI workflows, or quality gate
enforcement.

## Product Purpose

FocusPulse is a personal productivity system for turning daily work logs into
structured records, practical analytics, and later AI-assisted insights. The
system starts with CSV-first ingestion and grows through clear phases so data
quality, traceability, and module boundaries stay understandable.

The v1 target is a single primary user or small personal workspace. The project
is intentionally a modular monolith, not a microservice system.

## V1 Scope

The planned v1 build includes these later phases:

- Phase 1: core domain model and persistence for daily logs, tasks, notes,
  categories, tags, import runs, and AI insight runs.
- Phase 2: manual CSV import pipeline with validation, normalization,
  deduplication, and import traceability.
- Phase 3: usable dashboard foundation with daily logs, task views, summaries,
  breakdowns, and filters.
- Basic Phase 4: AI insight generation with stored, traceable outputs.

Phase 0 deliverables are limited to:

- `docs/FOUNDATION.md`.
- Skeleton backend target directories under `backend/app/`.
- Skeleton frontend target directories under `frontend/`.
- Skeleton Docker support directories under `docker/`.
- Root `.env.example` placeholder groups.
- `docker-compose.yml` service placeholder comments.
- README guidance pointing contributors to the foundation and stack documents.

## Out Of Scope

These items are future work and must not be implemented during Phase 0:

- UI polish beyond later approved dashboard work.
- Report exports and advanced reporting flows.
- Notion API integration or scheduled external ingestion.
- AI chat over productivity data.
- Automation such as scheduled imports or scheduled AI runs.
- Production hardening, strict uptime objectives, full monitoring, operational
  runbooks, and CI quality gate enforcement.

Any Phase 0 change that alters stack decisions, naming conventions, AI
boundaries, or v1 scope requires an explicit amendment before implementation.

## Baseline Repository Setup

| Area | Phase 0 Path | Purpose |
| --- | --- | --- |
| Backend target | `backend/app/` | Future FastAPI modular monolith layout |
| Backend legacy placeholders | `backend/src/`, `backend/main.py` | Pre-existing placeholders, not the Phase 0 target layout |
| Frontend target | `frontend/` | Future Next.js App Router dashboard layout |
| Docker support | `docker/` | Future nginx and helper script support |
| Environment example | `.env.example` | Future configuration groups only |
| Compose placeholder | `docker-compose.yml` | Future service inventory only |
| Foundation docs | `docs/FOUNDATION.md` | Phase 0 architecture and scope source |
| Product plan | `docs/Plan.md` | Phase-based product roadmap |
| Stack rules | `docs/STACK_AND_STRUCTURE.md` | Target stack and structure details |

Do not add Phase 0 feature logic under `backend/src/` or `backend/main.py`.
Future backend implementation should use `backend/app/` after a later phase
authorizes runnable behavior.

## Approved Platform Decisions

| Area | Decision | Phase 0 Action |
| --- | --- | --- |
| Backend | Python 3.12+, FastAPI, REST API, modular monolith | Reserve `backend/app/` skeleton |
| Frontend | Next.js App Router, TypeScript, Tailwind CSS, shadcn/ui | Reserve `frontend/` skeleton |
| Database | PostgreSQL with SQLAlchemy Async and Alembic | Document only |
| Jobs | Celery with Redis | Reserve `backend/app/workers/` |
| AI | Isolated AI insights module | Reserve `backend/app/modules/ai_insights/` |
| Ingestion | Manual CSV upload first | Reserve `backend/app/modules/imports/` |
| Orchestration | Local Docker Compose in later phases | Add service placeholder comments |

## Backend Architecture Rules

- API routers belong under `backend/app/api/` or module `router.py` files in a
  later runnable phase.
- Service code owns business rules and coordinates repositories or external
  systems.
- Repository code owns database access and must not know about HTTP request or
  response objects.
- Database engine, sessions, and base model wiring belong in
  `backend/app/core/database.py` when a later phase authorizes persistence.
- App-level configuration aggregation belongs in `backend/app/core/config.py`.
- Domain-specific settings classes belong under `backend/app/settings/`.
- Reusable cross-module support belongs under `backend/app/shared/`.
- Background job setup and thin task entry points belong under
  `backend/app/workers/`.
- Feature-specific behavior stays inside `backend/app/modules/<feature>/`.
- Phase 0 files in these paths must remain explanatory placeholders only.

The intended flow for later implementation is:

```text
Router -> Service -> Repository -> Database
```

## Frontend Architecture Rules

- `frontend/app/` owns routing, layouts, page composition, and server/client
  boundaries.
- `frontend/features/` owns feature-specific UI logic, API hooks, schemas, and
  view utilities.
- `frontend/components/` owns reusable cross-feature UI.
- `frontend/lib/api/` owns the shared API client wrapper and request helpers.
- `frontend/hooks/` owns reusable hooks that are not tied to one feature.
- `frontend/stores/` owns global client state only when server state is not the
  right fit.
- `frontend/types/` owns shared TypeScript types.
- Phase 0 frontend files must remain explanatory placeholders only.

## Naming Conventions

- Backend modules use `snake_case`, for example `daily_logs` and
  `ai_insights`.
- Specs and branches use kebab-case with the numeric feature prefix, for
  example `001-foundation-architecture`.
- Domain entities use PascalCase, for example `DailyLog` and `AIInsightRun`.
- Background job names must be descriptive and use the owning domain, for
  example `imports.process_csv_upload` in a future phase.
- Frontend product feature folders use kebab-case where product-facing, for
  example `daily-logs` and `ai-insights`.

## Practical V1 Non-Functional Baselines

Future v1 phases must preserve:

- Import traceability: every import should be attributable to a run, file, user,
  status, and summary.
- Clear failures: validation, import, job, and AI failures should be visible and
  explainable enough for local recovery.
- Async status visibility: long-running imports, AI runs, and reports should
  expose status and failure reasons.
- Local recoverability: failed imports or jobs should be retryable or safely
  repeatable without corrupting source records.
- Data quality: normalized records should remain deterministic and auditable so
  analytics and AI outputs are based on trusted source data.

## Excluded Production Hardening

Phase 0 and practical v1 baselines do not require:

- Uptime SLAs.
- Full monitoring implementation.
- Operational runbooks.
- Strict recovery point or recovery time objectives.
- Production deployment hardening.

These may be considered in later hardening phases.

## AI Boundary

Future AI features may read validated productivity data and write separate AI
insight outputs. AI output must never mutate source daily logs, tasks, notes, or
imports.

Source productivity records remain authoritative. If an AI output conflicts with
source records, the source record wins and the AI output must be corrected,
regenerated, or marked stale in a separate insight record.

AI runs must be traceable by input period, model, status, output, and failure
reason when implemented in a later phase.

## Import, Job, And AI Traceability

Future import, background job, and AI work must make status, ownership, and
failure context reviewable. Traceability belongs in the relevant domain module
and should not be hidden inside one-off scripts or untracked generated files.

## Future Phase Compliance Checklist

Use this checklist before approving future phase plans or task lists:

- Scope: the work belongs to the named phase and does not smuggle in later
  phase behavior.
- Naming: backend modules use snake_case, frontend product folders use
  kebab-case, entities use PascalCase, and job names are descriptive.
- Module boundaries: routers, services, repositories, settings, workers, and
  shared code keep their documented ownership.
- Skeleton ownership: new files are added under the documented target paths.
- AI boundary: AI reads source data and writes separate insight outputs only.
- Data authority: source logs, tasks, notes, and imports remain authoritative.

## Validation Notes

Use `specs/001-foundation-architecture/quickstart.md` for Phase 0 validation.
The forbidden-output search may return matches in `docs/` and `specs/` because
those files describe future architecture and prohibited Phase 0 behavior. Such
documentation-only matches are acceptable. Matches in Phase 0 skeleton source
files are not acceptable unless they are explanatory placeholders and do not
implement behavior.
