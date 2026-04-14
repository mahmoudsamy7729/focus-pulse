# Contract: Phase 0 Foundation Package

This contract defines what a completed Phase 0 foundation package must provide. It is an artifact contract, not a runtime API contract.

## Required Inputs

- `docs/Plan.md`, specifically Phase 0 - Foundation & Architecture.
- `.specify/memory/constitution.md`.
- `docs/STACK_AND_STRUCTURE.md`.
- `specs/001-foundation-architecture/spec.md`.

## Required Outputs

The completed Phase 0 implementation must provide:

- `docs/FOUNDATION.md` summarizing product purpose, v1 scope boundaries, architecture rules, naming conventions, practical v1 baselines, and AI boundary.
- Skeleton backend target directories under `backend/app/`.
- Skeleton frontend target directories under `frontend/`.
- Skeleton Docker support directories under `docker/`.
- Root `.env.example` entries or comments for future backend, frontend, database, Redis, Celery, and AI settings.
- `docker-compose.yml` placeholders or comments for future `frontend`, `backend`, `postgres`, `redis`, `celery_worker`, and later `celery_beat` services.
- README guidance pointing future contributors to the foundation and stack documents.

## Required Backend Skeleton Areas

- `backend/app/api/`
- `backend/app/core/`
- `backend/app/modules/auth/`
- `backend/app/modules/daily_logs/`
- `backend/app/modules/tasks/`
- `backend/app/modules/notes/`
- `backend/app/modules/imports/`
- `backend/app/modules/analytics/`
- `backend/app/modules/ai_insights/`
- `backend/app/modules/reports/`
- `backend/app/settings/`
- `backend/app/shared/`
- `backend/app/workers/`

Placeholder files are allowed when needed to preserve directories. They must not contain production domain logic.

## Required Frontend Skeleton Areas

- `frontend/app/`
- `frontend/components/`
- `frontend/features/auth/`
- `frontend/features/daily-logs/`
- `frontend/features/tasks/`
- `frontend/features/notes/`
- `frontend/features/imports/`
- `frontend/features/analytics/`
- `frontend/features/ai-insights/`
- `frontend/features/reports/`
- `frontend/hooks/`
- `frontend/lib/api/`
- `frontend/public/`
- `frontend/stores/`
- `frontend/types/`

Placeholder files are allowed when needed to preserve directories. They must not contain runnable UI screens or API behavior.

## Forbidden Phase 0 Outputs

Phase 0 must not introduce:

- Runnable backend app shell.
- Runnable frontend app shell.
- Production API endpoints.
- Database schemas or migrations.
- Celery task behavior.
- CSV import parsing or validation logic.
- Dashboard screens, charts, filters, or data fetching.
- AI prompts, agents, tool calls, or generated insight behavior.
- CI workflows, lint gates, test gates, or type-check enforcement.
- Production uptime SLA, monitoring implementation, operational runbooks, or strict recovery objectives.

## Review Rules

A reviewer must be able to confirm:

- Phase 0 skeleton paths follow snake_case backend modules and kebab-case specs/branches.
- Backend module ownership is visible.
- Frontend feature ownership is visible.
- AI output is separated from source logs, tasks, and imports.
- Future task proposals can be classified as in scope, out of scope, or amendment required.
- The foundation package can be reviewed without installing dependencies or running services.

## Acceptance Criteria

- All required outputs exist or are intentionally documented as deferred with a reason.
- No forbidden Phase 0 output exists.
- The foundation package points future phases to the target architecture without implementing later phase behavior.
