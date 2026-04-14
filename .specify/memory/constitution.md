<!--
Sync Impact Report
Version change: 1.1.0 -> 1.2.0
Modified principles:
- III. Layered Backend Boundaries: added success response and pagination standards
- V. Background Work, AI Isolation, and Data Integrity: expanded auditability to formal audit trails
- API, Security, and Observability Standards: added success envelopes, pagination, and audit trail rules
Added sections:
- None
Removed sections:
- None
Templates requiring updates:
- updated .specify/templates/plan-template.md
- updated .specify/templates/tasks-template.md
- updated .specify/templates/spec-template.md
- checked .specify/templates/checklist-template.md
- checked .specify/templates/agent-file-template.md
- n/a .specify/templates/commands/ (directory not present)
Follow-up TODOs:
- The mandatory pre-constitution Git hook script could not run because its PowerShell
  file contains mojibake that breaks parsing, but the repository is already initialized.
-->
# FocusPulse Constitution

## Core Principles

### I. Spec-Driven Phased Delivery
FocusPulse MUST be built incrementally through Spec Kit phases. Each phase MUST have
its own spec, plan, and tasks, and implementation MUST stay inside the current
phase scope. Manual CSV upload is the first ingestion path; auto import,
scheduling, notifications, and chat integrations are future extensions unless a
later approved spec explicitly brings them into scope.

Rationale: The project plan defines a phase-based delivery model, and data quality
must be established before analytics, AI, and automation layers can be trusted.

### II. Modular Monolith and Feature Isolation
The system MUST remain a monorepo modular monolith with feature-based backend and
frontend modules. Backend feature code belongs under `backend/app/modules/<feature>/`
using the documented module layout: `router.py`, `schemas.py`, `services/`,
`repositories/`, `models.py`, `dependencies.py`, and optional module-local
`utils.py`, `exceptions.py`, `constants.py`, and `shared/`. Service and repository
code inside a module MUST be organized as folders, not flattened into growing
single-file implementations.

Cross-module reusable business-support code belongs in `backend/app/shared/`.
Infrastructure and framework wiring belongs in `backend/app/core/`. Feature-specific
business behavior MUST stay inside its owning module and MUST NOT be moved into
global shared folders for convenience.

Rationale: Feature isolation keeps the modular monolith scalable without adding
microservice complexity before the product needs it.

### III. Layered Backend Boundaries
Backend code MUST follow `Router -> Service -> Repository -> Database`. Routers
MUST define endpoints, parse inputs, return HTTP responses, and call services only.
Routers MUST NOT contain business logic or direct database logic. Services MUST
own use-case rules, validations, and external coordination; services MUST NOT
return FastAPI responses and MUST NOT contain raw persistence queries. Repositories
MUST encapsulate SQLAlchemy async data access and MUST NOT know about FastAPI
requests or responses.

FastAPI dependency injection MUST be explicit with `Depends`: routers depend on
services, services depend on repositories, and repositories depend on an
`AsyncSession`. `backend/app/core/database.py` is the single source of truth for
engine, session factory, declarative base, and DB dependency setup. Async database
access is the default; sync sessions are allowed only for clearly isolated
sync-only execution paths such as worker code that cannot use async access.

All REST APIs MUST be versioned under `/api/v1/`, `/api/v2/`, and so on.
Production API routes MUST NOT be exposed without a versioned `/api/vN/` prefix.
Version changes that alter contracts MUST be documented in the feature plan and
reflected in router composition.

Handled API success responses MUST use a standard success envelope unless the
endpoint is explicitly documented as a file download, stream, redirect, or other
non-JSON response:

```json
{
  "success": true,
  "data": {}
}
```

Backend error handling MUST use a unified response contract for all handled
application errors:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {}
  }
}
```

Feature modules MUST define custom exception classes for domain failures.
Application-level exception handling MUST map those exceptions to explicit HTTP
status codes and stable error codes. Validation failures, authentication failures,
authorization failures, missing resources, conflicts, rate-limit failures, and
unexpected server errors MUST each have a clear status-code mapping.

List endpoints MUST use one consistent pagination style per endpoint. `page` and
`limit` MUST be used for bounded, user-navigable lists where users need explicit
page numbers or totals. `cursor` pagination MUST be used for large, append-only,
high-churn, or infinite-scroll lists where stable traversal matters more than
page numbers. Pagination parameters, default limits, maximum limits, sort order,
and response metadata MUST be documented in the feature contract and implemented
consistently across APIs.

Rationale: These boundaries make data access, validation, and HTTP behavior
reviewable and prevent framework concerns from leaking across layers.

### IV. Frontend Structure and API Discipline
The frontend MUST use the documented Next.js App Router structure with TypeScript,
Tailwind CSS, shadcn/ui, TanStack Query, React Hook Form, Zod, Axios, and Recharts.
`frontend/app/` MUST be limited to routing, layouts, page composition, and
server/client boundaries. Feature-specific UI, hooks, schemas, and utilities belong
under `frontend/features/<feature>/`. Cross-feature UI belongs under
`frontend/components/`. Shared API client setup, interceptors, token handling,
validators, constants, and utilities belong under `frontend/lib/`.

Server state MUST use TanStack Query by default. Global client state MUST be added
only when there is a clear cross-feature UI-state need; lightweight UI state may
use a store, but server data MUST NOT be duplicated into global client stores.
Form validation MUST pair React Hook Form with Zod for user-facing forms.

Rationale: The dashboard is API-heavy, so clear route, feature, API, and state
boundaries prevent duplicated fetching logic and keep UI behavior predictable.

### V. Background Work, AI Isolation, and Data Integrity
Celery with Redis MUST handle long-running work such as CSV import processing,
AI analysis runs, and report generation. Celery tasks MUST stay thin and delegate
use-case behavior to application services; they MUST NOT duplicate import,
analytics, AI, or report business rules.

AI behavior MUST stay organized inside the `ai_insights` module. Agent
orchestration, prompt preparation, tools, run history, recommendation generation,
and stored insight outputs MUST NOT be scattered through unrelated modules.

PostgreSQL is the database, SQLAlchemy Async ORM is the data access layer, Alembic
is the migration system, and UUID primary keys are required for main entities.
Persistence changes MUST include the corresponding model and migration work.
Core entities SHOULD use shared base fields such as `id`, `created_at`, and
`updated_at` unless a feature spec justifies a narrower shape.

Imports and background jobs MUST be idempotent. Import execution, AI runs, report
generation, and other worker tasks MUST use a stable idempotency key or equivalent
deduplication rule so retries and duplicate submissions do not create duplicate
processing results. The idempotency strategy MUST be documented in the plan for
features that enqueue jobs or ingest external data.

Soft delete MUST be used for user-owned records, imported records, generated AI
outputs, and audit-sensitive operational records when deletion could affect
traceability, restore behavior, or historical analytics. Soft-deleted records MUST
be excluded from normal user-facing queries by default, retain enough metadata for
auditability, and support restore when restoring does not violate data integrity.
Hard delete is allowed only for ephemeral data, failed transient staging records,
or data whose removal is explicitly required by a later approved policy.

Imports, AI runs, and admin actions MUST write an audit trail. The audit trail MUST
make it possible to trace who triggered the action, when it happened, what was
requested or changed, the resulting status, and relevant error details when the
action fails. Audit records MUST be durable enough to investigate import quality,
AI output generation, permission-sensitive changes, and operational incidents.

Rationale: Imports, analytics, reports, and AI runs need traceability and
recoverability, and they must not block normal API requests.

## Technology and Architecture Constraints

The approved backend stack is FastAPI, SQLAlchemy Async, PostgreSQL, Alembic,
Celery, Redis, JWT authentication, REST APIs, UUID primary keys, and
environment-based configuration with `pydantic-settings`.

Backend application code MUST follow the documented global structure:
`backend/app/core/`, `backend/app/shared/`, `backend/app/settings/`,
`backend/app/modules/`, `backend/app/workers/`, `backend/app/api/`, and
`backend/app/main.py`. `backend/app/core/config.py` MUST compose focused settings
classes from `backend/app/settings/`. Each settings file MUST represent one
configuration concern, such as app, auth, database, AI, Redis, or Celery settings.

The approved backend modules are `auth`, `daily_logs`, `tasks`, `notes`,
`imports`, `analytics`, `ai_insights`, and `reports`. Global API composition MUST
flow through `backend/app/api/router.py`, which aggregates module routers with
feature prefixes and tags.

The approved frontend stack is Next.js App Router, TypeScript, Tailwind CSS,
shadcn/ui, TanStack Query, Zod, React Hook Form, Axios, and Recharts. Frontend
application code MUST follow the documented structure: `frontend/app/`,
`frontend/components/`, `frontend/features/`, `frontend/lib/`, `frontend/hooks/`,
`frontend/stores/`, `frontend/types/`, and `frontend/public/`.

Docker and Docker Compose are the approved local orchestration tools. The expected
service set is `frontend`, `backend`, `postgres`, `redis`, `celery_worker`, and
`celery_beat` only when scheduled jobs are introduced by a later phase.

## API, Security, and Observability Standards

Structured logging MUST be used for backend application logs, worker logs, import
runs, and AI runs. Request handling MUST attach or propagate a `request_id` so API
logs, service logs, repository errors, and worker handoffs can be correlated.
Import runs and AI insight runs MUST remain trackable through persisted status,
input summary, output summary or error details, timestamps, and user ownership
where applicable.

Security controls MUST include rate limiting for authentication, import, AI-run,
and other expensive or abuse-sensitive endpoints. JWT authentication MUST be
paired with explicit scopes or permission checks for protected operations. Feature
plans MUST state required auth scopes, permission boundaries, and rate-limit
expectations for any new protected endpoint.

API endpoints MUST use the unified error response schema from this constitution.
Frontend API handling MUST preserve stable error codes so UI flows can distinguish
validation errors, auth failures, permission failures, missing resources,
conflicts, rate limits, and server failures without string-matching messages.

API endpoints MUST use the standard success response schema for handled JSON
responses. List endpoints MUST expose a consistent pagination contract. Page-based
pagination MUST use `page` and `limit`; cursor-based pagination MUST use `cursor`
and a documented limit. Frontend API handling MUST preserve pagination metadata
without inventing endpoint-specific list behavior.

## Development Workflow

Every feature plan MUST pass a Constitution Check before design work proceeds and
again after design artifacts are drafted. The check MUST verify phase scope,
backend layering, module ownership, settings/database single-source rules,
frontend route/feature boundaries, background-job delegation, AI isolation, and
database migration impact. The check MUST also verify API versioning, unified
success responses, unified error responses, custom exceptions, HTTP status
mappings, pagination contracts, request-id logging, audit trails, security scopes,
rate limits, idempotency, soft delete impact, and test coverage.

Specs MUST describe user journeys and measurable outcomes without introducing
technologies outside this constitution. Plans MUST name real paths from the
documented monorepo structure. Tasks MUST be dependency ordered, grouped by user
story, and written with exact file paths so reviewers can detect boundary
violations before implementation starts.

Service changes MUST include unit tests for service-layer behavior. API endpoint
changes MUST include integration tests that verify success paths, success and
error response shapes, relevant HTTP status mappings, pagination behavior, auth
or permission behavior, audit-trail writes, and idempotency or soft delete behavior
when the feature uses those concerns.

Work MUST follow the initial build order from the project docs: bootstrap and
shared foundations first; daily logs, tasks, notes, and manual imports next;
analytics and dashboard metrics after usable data exists; AI insights after the
data and analytics foundations are stable; hardening, scheduling, and automation
only in later phases.

## Governance

This constitution governs specs, plans, tasks, and implementation decisions for
FocusPulse. `docs/STACK_AND_STRUCTURE.md` is the detailed architecture reference
for the approved stack and structure; if that document and this constitution
conflict, work MUST stop until they are reconciled in the same change.

Amendments MUST include the reason for the change, affected principles or
sections, migration impact for existing specs or code, and updates to dependent
templates when the change affects planning or task generation. Versioning follows
semantic versioning: MAJOR for incompatible governance or architecture changes,
MINOR for new principles or materially expanded guidance, and PATCH for wording
or clarification changes.

Compliance review is required during `/speckit.plan`, `/speckit.tasks`, and code
review. Any accepted deviation from API versioning, success response handling,
error handling, pagination, observability, audit trails, security, testing,
idempotency, or soft delete rules MUST be recorded in the feature plan's
Complexity Tracking section with the reason and the simpler alternative that was
rejected.

**Version**: 1.2.0 | **Ratified**: 2026-04-14 | **Last Amended**: 2026-04-14
