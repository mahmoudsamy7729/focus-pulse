# STACK_AND_STRUCTURE.md

## Project Stack

### Backend
- FastAPI
- SQLAlchemy Async
- PostgreSQL
- Alembic
- Celery
- Redis
- JWT Authentication
- REST API
- UUID primary keys

### Frontend
- Next.js (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Query
- Zod
- React Hook Form
- Axios

### DevOps
- Docker
- Docker Compose
- Monorepo

---

## Architecture Style

The project will follow a **Modular Monolith + Layered Architecture** approach.

### Core Decisions
- Feature-based modules
- Layered structure inside each module
- Composition Root in `main.py`
- Dependency Injection using `FastAPI Depends`
- Repository pattern using SQLAlchemy async
- Manual CSV upload first
- Auto import can be added later as a separate phase
- AI layer built as an **agent system**
- Background processing handled by **Celery + Redis**

### Configuration and Settings
The backend should also include a dedicated **`settings/` folder** for environment-based configuration domains.

Each settings file should represent one concern, for example:
- `app.py`
- `auth.py`
- `database.py`
- `ai.py`
- `redis.py`
- `celery.py`

These settings classes should be composed together in a central `config.py` file.

This keeps:
- env variables organized by domain
- defaults and validators close to the related feature
- configuration scalable as integrations grow

Recommended pattern:
- each settings file contains a `BaseSettings` class
- use `pydantic-settings`
- use aliases for env variables where needed
- normalize values through validators
- aggregate all settings classes into a single `Settings` object in `config.py`

---

## Backend Module Structure

Each backend feature module should follow this structure:

```text
backend/app/modules/<feature>/
├── router.py
├── schemas.py
├── services/
├── repositories/
├── models.py
├── dependencies.py
├── utils.py
├── exceptions.py
├── constants.py
└── shared/
```

### Layer Responsibilities

#### `router.py`
API layer only.
- Define endpoints
- Parse request inputs
- Return HTTP responses
- Call service layer
- No business logic
- No direct database logic

#### `schemas.py`
DTOs and validation.
- Request schemas
- Response schemas
- Filter schemas
- Internal typed payloads when needed

#### `services/`
Business logic layer.
- Organizes service classes by use case or domain responsibility
- Calls repositories
- Applies rules and validations
- Coordinates external systems
- No raw SQL and no HTTP response formatting

Typical examples:
- `create_task.py`
- `update_task.py`
- `list_tasks.py`
- `task_service.py`

#### `repositories/`
Data access layer.
- Organizes repository classes and query helpers
- Query database through SQLAlchemy async
- Encapsulate persistence logic
- Return entities or structured data to services
- No HTTP awareness

Typical examples:
- `task_repository.py`
- `task_query_repository.py`
- `filters.py`

#### `models.py`
ORM entities.
- SQLAlchemy models
- Table definitions
- Relationships
- UUID keys
- Shared model mixins when needed

#### `dependencies.py`
Dependency injection wiring.
- Service providers
- Repository providers
- Shared module dependencies
- Auth/context helpers specific to that module

#### `utils.py`
Module-local helper functions.
- formatting helpers
- mapping helpers
- small reusable calculations inside the module

#### `exceptions.py`
Module-local custom exceptions.
- use-case errors
- domain-specific validation failures
- not-found exceptions specific to the feature

#### `constants.py`
Static values for the module.
- statuses
- fixed labels
- default limits
- internal enums/constants when a full enum file is unnecessary

#### `shared/`
Reusable internals for the same module.
Use this only when logic is shared across multiple files inside the same feature but is still too feature-specific to move to global shared code.

---

## Backend Global Structure

```text
backend/
├── app/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── exceptions.py
│   │   └── utils/
│   ├── shared/
│   │   ├── enums/
│   │   ├── validators/
│   │   ├── helpers/
│   │   ├── types/
│   │   └── schemas/
│   ├── settings/
│   │   ├── app.py
│   │   ├── auth.py
│   │   ├── database.py
│   │   ├── ai.py
│   │   ├── redis.py
│   │   ├── celery.py
│   │   └── ...
│   ├── modules/
│   │   ├── auth/
│   │   ├── daily_logs/
│   │   ├── tasks/
│   │   ├── notes/
│   │   ├── imports/
│   │   ├── analytics/
│   │   ├── ai_insights/
│   │   └── reports/
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks/
│   ├── api/
│   │   ├── router.py
│   │   └── dependencies.py
│   └── main.py
├── alembic/
├── tests/
├── Dockerfile
└── requirements/
```

---

## Recommended Backend Modules

### 1. `auth`
Responsible for:
- login
- token issuance
- token refresh later if needed
- current user resolution
- auth guards

### 2. `daily_logs`
Responsible for:
- daily log records
- date-based grouping
- daily summaries
- linking imported day data

### 3. `tasks`
Responsible for:
- task storage
- task status
- task duration
- category relation
- daily task listing

### 4. `notes`
Responsible for:
- daily notes
- note history
- note search and filtering later

### 5. `imports`
Responsible for:
- CSV upload
- CSV parsing
- data normalization
- import validation
- import execution
- import history

### 6. `analytics`
Responsible for:
- productivity calculations
- consistency metrics
- time spent reports
- dashboard aggregations

### 7. `ai_insights`
Responsible for:
- AI agent orchestration
- prompt preparation
- insights generation
- recommendation storage
- AI run history

### 8. `reports`
Responsible for:
- weekly reports
- monthly reports
- export-ready report payloads

---

## API Composition

### Global API Entry
The main API router should aggregate module routers from:
- `app/api/router.py`

### Example
```python
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(daily_logs_router, prefix="/daily-logs", tags=["Daily Logs"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])
api_router.include_router(notes_router, prefix="/notes", tags=["Notes"])
api_router.include_router(imports_router, prefix="/imports", tags=["Imports"])
api_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(ai_insights_router, prefix="/ai-insights", tags=["AI Insights"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
```

---

## Database Connection Layer

The backend must include a dedicated database connection file:

- `backend/app/core/database.py`

This file is responsible for:
- creating the async SQLAlchemy engine
- creating the async session factory
- exposing `Base` for ORM models
- providing the FastAPI DB dependency
- optionally exposing a sync session factory for sync-only tasks such as some Celery jobs

### Recommended responsibilities for `core/database.py`
- define `create_async_engine(...)`
- define async `sessionmaker(...)`
- define `Base = declarative_base()`
- define `get_db()` dependency for `AsyncSession`
- expose a typed dependency alias if useful
- define sync engine/session access only when required for sync workers

### Rule
- API routes and repositories use `AsyncSession`
- sync DB access is allowed only in explicitly sync execution paths
- do not mix async and sync sessions randomly
- any sync session support must be clearly isolated and documented

### Example direction
- `get_db()` is used by FastAPI dependencies
- repositories receive `AsyncSession`
- sync Celery or utility tasks can use a separate sync session provider when truly needed

## Dependency Injection Pattern

Use `FastAPI Depends` consistently.

### Rule
- Routers depend on services
- Services depend on repositories
- Repositories depend on async DB session

### Flow
```text
Router -> Service -> Repository -> Database
```

### Example direction
- `router.py` gets `service: TaskService = Depends(get_task_service)`
- `get_task_service()` resolves repository dependencies
- repository uses `AsyncSession`

---

## Core and Shared Infrastructure

The backend should standardize two foundational areas:

- `app/core/` for application infrastructure
- `app/shared/` for reusable cross-module code

### Recommended `core/` files
```text
backend/app/core/
├── config.py
├── database.py
├── security.py
├── logging.py
├── exceptions.py
└── utils/
```

### Recommended `shared/` structure
```text
backend/app/shared/
├── enums/
├── validators/
├── helpers/
├── types/
└── schemas/
```

### `core/`
Use `core/` for framework and infrastructure wiring:
- config aggregation
- database setup
- auth/security primitives
- logging
- app-level exception handling

### `shared/`
Use `shared/` for reusable business-support code that is used across multiple modules:
- generic validators
- common enums
- shared helper functions
- reusable schema fragments
- common types

### Rule
- if code is infrastructure-related, it belongs in `core/`
- if code is reusable across modules, it belongs in `shared/`
- if code is only used inside one module, keep it inside that module
- do not move feature-specific business logic into global shared folders

### `database.py`
This file is the single source of truth for database connection setup.

It should contain:
- async engine
- async session factory
- declarative base
- FastAPI DB dependency
- optional sync engine/session for sync-only jobs

This gives the project one clear place for DB wiring and avoids scattered session setup across modules.

## Settings and Configuration Structure

Environment configuration should not be dumped into one large file.

Use a dedicated `settings/` package for domain-based settings classes, then compose them in `core/config.py`.

### Recommended structure

```text
backend/app/
├── core/
│   └── config.py
└── settings/
    ├── app.py
    ├── auth.py
    ├── database.py
    ├── ai.py
    ├── redis.py
    ├── celery.py
    └── ...
```

### Rule
- `settings/` contains small focused settings classes
- `config.py` aggregates them into one `Settings` class
- app code imports the shared `settings` object from `config.py`
- validation and normalization should happen inside the related settings class

### Example responsibility split
- `app.py`: app name, debug, API prefix, CORS
- `auth.py`: JWT secret, token expiry, algorithm
- `database.py`: DB URL, pool settings
- `ai.py`: model, API key, base URL
- `redis.py`: Redis host, port, URL
- `celery.py`: broker URL, result backend, queue names

### Why this matters
This pattern avoids:
- huge unreadable config files
- unrelated env variables mixed together
- weak validation of env inputs

It also makes the project easier to scale when new external integrations are added.

## Database Standards

### Database
- PostgreSQL

### ORM
- SQLAlchemy Async ORM

### Migrations
- Alembic

### Primary Keys
- UUID for all main entities

### Recommended shared base fields
For most tables:
- `id`
- `created_at`
- `updated_at`

Optional where useful:
- `deleted_at`
- `created_by`

---

## Suggested Core Entities

### Users
- id
- email
- password_hash
- full_name
- is_active
- created_at
- updated_at

### DailyLogs
- id
- user_id
- log_date
- source
- raw_import_reference (optional)
- created_at
- updated_at

### Tasks
- id
- daily_log_id
- user_id
- title
- status
- category
- started_at
- ended_at
- duration_minutes
- source
- created_at
- updated_at

### Notes
- id
- daily_log_id
- user_id
- content
- created_at
- updated_at

### ImportRuns
- id
- user_id
- filename
- status
- imported_at
- summary
- created_at
- updated_at

### AIInsightRuns
- id
- user_id
- daily_log_id nullable
- period_type
- period_start
- period_end
- status
- model_name
- output_json
- created_at
- updated_at

---

## Background Jobs Structure

Use Celery for:
- CSV import processing
- AI analysis runs
- report generation later

### Suggested structure
```text
backend/app/workers/
├── celery_app.py
└── tasks/
    ├── import_tasks.py
    ├── ai_tasks.py
    └── report_tasks.py
```

### Rule
Celery tasks should:
- call application services
- stay thin
- not duplicate business logic

---

## AI Layer Structure

The AI layer should be implemented as an **agent system**, but still inside the modular monolith.

### Suggested internal structure
```text
backend/app/modules/ai_insights/
├── router.py
├── schemas.py
├── services.py
├── repositories.py
├── models.py
├── dependencies.py
├── agents/
├── prompts/
└── tools/
```

### Responsibilities
- run insight generation
- analyze daily and range-based productivity
- detect patterns
- generate recommendations
- store results in DB
- expose insights to dashboard

### Rule
Keep the agent orchestration inside the AI module.
Do not spread prompt logic randomly across the codebase.

---

## Frontend Decision

The best frontend setup for this project is:

- **Next.js App Router**
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui**
- **TanStack Query**
- **React Hook Form + Zod**
- **Axios client wrapper**
- **Recharts** for dashboard charts

### Why this setup
- App Router works well for modern dashboard apps
- TypeScript improves maintainability
- Tailwind + shadcn speeds up UI development
- TanStack Query is ideal for API-heavy dashboards
- Zod keeps forms and validation clean
- Recharts is enough for analytics dashboards without overcomplication

---

## Frontend Structure

```text
frontend/
├── app/
│   ├── (auth)/
│   ├── (dashboard)/
│   │   ├── dashboard/
│   │   ├── daily-logs/
│   │   ├── tasks/
│   │   ├── notes/
│   │   ├── imports/
│   │   ├── analytics/
│   │   ├── ai-insights/
│   │   └── reports/
│   ├── api/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── ui/
│   ├── layout/
│   ├── charts/
│   └── shared/
├── features/
│   ├── auth/
│   ├── daily-logs/
│   ├── tasks/
│   ├── notes/
│   ├── imports/
│   ├── analytics/
│   ├── ai-insights/
│   └── reports/
├── lib/
│   ├── api/
│   ├── utils/
│   ├── validators/
│   └── constants/
├── hooks/
├── stores/
├── types/
├── public/
├── Dockerfile
└── package.json
```

---

## Frontend Structure Rules

### `app/`
Routing only.
- layouts
- route groups
- page composition
- server/client boundaries

### `features/`
Feature-specific frontend logic.
- API hooks
- feature components
- local schemas
- view-specific utilities

### `components/`
Reusable cross-feature UI components.
- layout components
- shared cards
- tables
- dialogs
- charts
- form wrappers

### `lib/api/`
API client setup.
- axios instance
- interceptors
- token handling
- shared request helpers

### `stores/`
Only for global client state when truly needed.
Use TanStack Query for server state first.
Use Zustand only for lightweight UI state if necessary.

---

## Monorepo Structure

```text
project-root/
├── backend/
├── frontend/
├── docker/
│   ├── nginx/
│   └── scripts/
├── .env.example
├── docker-compose.yml
├── README.md
└── docs/
```

---

## Docker Setup

### Services
- `frontend`
- `backend`
- `postgres`
- `redis`
- `celery_worker`
- `celery_beat` later if scheduled jobs are added

### Notes
- keep backend and worker images aligned
- mount code in development
- use separate production Dockerfiles if needed later

---

## Service and Repository Folder Rule

Inside each module:
- `services/` should be a folder, not a single file
- `repositories/` should be a folder, not a single file

### Why
This keeps modules scalable when:
- the number of use cases grows
- queries become more complex
- multiple repository helpers or specialized service classes are needed

### Rule
- simple projects may start with one main service/repository file inside the folder
- do not flatten growing logic back into one giant file
- keep service files organized by use case when the module expands

## Module vs Global Shared Rule

### Keep code inside the module when:
- it is used by one feature only
- it contains feature-specific business behavior
- it is tightly coupled to that module's models or workflows

### Move code to `app/shared/` when:
- it is reused across multiple modules
- it is generic enough to stay independent from one feature
- it improves consistency across the project

### Keep code in `app/core/` when:
- it is infrastructure or framework setup
- it is app bootstrapping related
- it affects the whole application runtime

## Naming Conventions

### Backend
- modules use plural or domain-friendly names consistently
- routers: `router.py`
- services: class-based, ex: `TaskService`
- repositories: class-based, ex: `TaskRepository`
- dependencies: `get_task_service`, `get_task_repository`
- schemas:
  - `TaskCreateRequest`
  - `TaskUpdateRequest`
  - `TaskResponse`

### Frontend
- components: `PascalCase`
- hooks: `useXxx`
- folders: kebab-case or feature name consistency
- query keys centralized by feature
- route segments follow product language, not internal implementation names

---

## Non-Negotiable Architecture Rules

1. No business logic inside routers
2. No direct DB logic inside routers
3. Services must not return HTTP responses
4. Repositories must not know anything about FastAPI request/response
5. Keep modules isolated by feature as much as possible
6. Shared utilities go into `core` only when truly shared
7. Prefer explicit dependencies over hidden imports
8. Async DB access should be consistent across the backend
9. Celery tasks should delegate to services, not embed use-case logic
10. AI logic must stay organized inside the AI module
11. Environment configuration must be organized into dedicated files under `settings/`
12. `core/config.py` is the single aggregation point for app settings
13. `core/database.py` is the single source of truth for DB engine and session setup
14. Async repositories must use `AsyncSession` by default
15. Sync DB sessions are allowed only for explicit sync-only execution paths
16. Every module may define `utils.py`, `exceptions.py`, `constants.py`, and a local `shared/` when needed
17. `services` and `repositories` inside modules should be folders to support internal separation
18. Cross-module reusable code belongs in `app/shared/`, not inside a feature module
19. `app/shared/` must not become a dumping ground for feature-specific business logic

---

## Initial Build Order

### Phase 1
- project bootstrap
- Docker setup
- PostgreSQL + Redis
- FastAPI base app
- Next.js base app
- auth module
- shared backend core
- frontend dashboard shell

### Phase 2
- daily_logs module
- tasks module
- notes module
- CSV manual upload flow
- basic list/detail pages

### Phase 3
- analytics module
- dashboard metrics
- charts
- filters
- report payloads

### Phase 4
- ai_insights module
- agent orchestration
- AI runs
- insights pages
- recommendation cards

### Phase 5
- hardening
- audit and logs
- testing improvements
- auto import later
- scheduling later

---

## Future Extensions

Planned later:
- auto import from Notion or external source
- scheduled imports
- scheduled AI runs
- advanced reporting
- notifications
- chat with productivity data
- multi-source ingestion

---

## Final Recommendation

This project should be built as a **feature-based modular monolith** with:
- strict layering inside each module
- async SQLAlchemy repositories
- service-driven business logic
- Celery for long-running work
- Next.js App Router for the dashboard
- TanStack Query as the default server-state layer

This keeps the system scalable without making it unnecessarily microservice-heavy in the first version.
