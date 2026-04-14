# Tasks: Foundation & Architecture

**Input**: Design documents from `/specs/001-foundation-architecture/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/foundation-package.md, quickstart.md

**Tests**: No automated service, API, or UI tests are required for Phase 0 because this feature creates documentation and skeleton-only repository setup. Validation is manual inspection via `quickstart.md`.

**Organization**: Tasks are grouped by user story to enable independent implementation and review.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend skeleton**: `backend/app/` for target backend application structure; do not add feature logic under existing `backend/src/`
- **Backend modules**: `backend/app/modules/<feature>/` with snake_case module names
- **Frontend skeleton**: `frontend/` with product-facing feature folders in kebab-case
- **DevOps/docs**: `docker/`, `docker-compose.yml`, `.env.example`, `docs/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare shared placeholder conventions and protect the skeleton-only boundary before user-story work.

- [X] T001 Create a skeleton placeholder convention note in `docs/FOUNDATION.md`
- [X] T002 [P] Create backend skeleton preservation note in `backend/app/README.md`
- [X] T003 [P] Create frontend skeleton preservation note in `frontend/README.md`
- [X] T004 [P] Create Docker skeleton preservation note in `docker/README.md`
- [X] T005 Add Phase 0 validation command references to `README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish the shared skeleton directories and placeholder files that all user stories depend on.

**CRITICAL**: No user story work should begin until this phase is complete.

- [X] T006 [P] Create backend target root placeholders in `backend/app/.gitkeep`, `backend/app/api/.gitkeep`, `backend/app/core/.gitkeep`, `backend/app/settings/.gitkeep`, `backend/app/shared/.gitkeep`, and `backend/app/workers/.gitkeep`
- [X] T007 [P] Create backend module placeholders in `backend/app/modules/auth/.gitkeep`, `backend/app/modules/daily_logs/.gitkeep`, `backend/app/modules/tasks/.gitkeep`, `backend/app/modules/notes/.gitkeep`, `backend/app/modules/imports/.gitkeep`, `backend/app/modules/analytics/.gitkeep`, `backend/app/modules/ai_insights/.gitkeep`, and `backend/app/modules/reports/.gitkeep`
- [X] T008 [P] Create frontend root placeholders in `frontend/app/.gitkeep`, `frontend/components/.gitkeep`, `frontend/hooks/.gitkeep`, `frontend/lib/api/.gitkeep`, `frontend/public/.gitkeep`, `frontend/stores/.gitkeep`, and `frontend/types/.gitkeep`
- [X] T009 [P] Create frontend feature placeholders in `frontend/features/auth/.gitkeep`, `frontend/features/daily-logs/.gitkeep`, `frontend/features/tasks/.gitkeep`, `frontend/features/notes/.gitkeep`, `frontend/features/imports/.gitkeep`, `frontend/features/analytics/.gitkeep`, `frontend/features/ai-insights/.gitkeep`, and `frontend/features/reports/.gitkeep`
- [X] T010 [P] Create Docker support placeholders in `docker/nginx/.gitkeep` and `docker/scripts/.gitkeep`
- [X] T011 Document that existing `backend/src/` and `backend/main.py` are pre-existing placeholders and not the Phase 0 target layout in `docs/FOUNDATION.md`

**Checkpoint**: Shared skeleton paths exist and can be inspected before story-specific documentation is finalized.

---

## Phase 3: User Story 1 - Define Project Purpose and Scope (Priority: P1) MVP

**Goal**: Deliver the foundation package content that explains FocusPulse purpose, v1 scope, out-of-scope future work, and baseline repo setup.

**Independent Test**: A new contributor can read the Phase 0 foundation package and identify product purpose, v1 boundaries, out-of-scope items, and baseline repo setup without reading later phase plans.

### Implementation for User Story 1

- [X] T012 [US1] Add product purpose and project overview section to `docs/FOUNDATION.md`
- [X] T013 [US1] Add v1 in-scope phases and deliverables section to `docs/FOUNDATION.md`
- [X] T014 [US1] Add out-of-scope future work section covering UI polish, report exports, Notion API, AI chat, automation, and production hardening in `docs/FOUNDATION.md`
- [X] T015 [US1] Add skeleton-only Phase 0 deliverable definition to `docs/FOUNDATION.md`
- [X] T016 [US1] Add baseline repository setup inventory linking backend, frontend, docker, env, compose, and docs paths to `docs/FOUNDATION.md`
- [X] T017 [US1] Update root project guidance with links to `docs/FOUNDATION.md`, `docs/Plan.md`, and `docs/STACK_AND_STRUCTURE.md` in `README.md`
- [X] T018 [US1] Add future environment variable placeholder groups for app, auth, database, Redis, Celery, AI, and frontend settings in `.env.example`
- [X] T019 [US1] Add non-runnable service placeholder comments for future frontend, backend, postgres, redis, celery_worker, and later celery_beat services in `docker-compose.yml`

**Checkpoint**: User Story 1 is reviewable independently using `docs/FOUNDATION.md`, `README.md`, `.env.example`, and `docker-compose.yml`.

---

## Phase 4: User Story 2 - Lock Architecture and Conventions (Priority: P2)

**Goal**: Make architecture rules, naming conventions, platform decisions, and skeleton path ownership explicit for future phases.

**Independent Test**: A reviewer can compare a proposed Phase 1 or Phase 2 plan against the foundation package and determine whether it follows architecture rules and naming conventions.

### Implementation for User Story 2

- [X] T020 [US2] Add approved platform decisions table for backend, frontend, database, jobs, AI, and ingestion to `docs/FOUNDATION.md`
- [X] T021 [US2] Add backend architecture rules for router, service, repository, database, settings, shared, and workers ownership to `docs/FOUNDATION.md`
- [X] T022 [US2] Add frontend architecture rules for app routing, feature logic, components, API client, hooks, stores, and types ownership to `docs/FOUNDATION.md`
- [X] T023 [US2] Add naming convention section for snake_case modules, kebab-case specs and branches, PascalCase domain entities, and descriptive job names to `docs/FOUNDATION.md`
- [X] T024 [P] [US2] Add backend module ownership notes to `backend/app/modules/auth/README.md`, `backend/app/modules/daily_logs/README.md`, `backend/app/modules/tasks/README.md`, `backend/app/modules/notes/README.md`, `backend/app/modules/imports/README.md`, `backend/app/modules/analytics/README.md`, `backend/app/modules/ai_insights/README.md`, and `backend/app/modules/reports/README.md`
- [X] T025 [P] [US2] Add backend infrastructure ownership notes to `backend/app/api/README.md`, `backend/app/core/README.md`, `backend/app/settings/README.md`, `backend/app/shared/README.md`, and `backend/app/workers/README.md`
- [X] T026 [P] [US2] Add frontend ownership notes to `frontend/app/README.md`, `frontend/components/README.md`, `frontend/features/README.md`, `frontend/hooks/README.md`, `frontend/lib/api/README.md`, `frontend/stores/README.md`, and `frontend/types/README.md`
- [X] T027 [P] [US2] Add frontend feature ownership notes to `frontend/features/auth/README.md`, `frontend/features/daily-logs/README.md`, `frontend/features/tasks/README.md`, `frontend/features/notes/README.md`, `frontend/features/imports/README.md`, `frontend/features/analytics/README.md`, `frontend/features/ai-insights/README.md`, and `frontend/features/reports/README.md`
- [X] T028 [US2] Add future phase compliance review checklist for scope, naming, module boundaries, and skeleton path ownership to `docs/FOUNDATION.md`

**Checkpoint**: User Story 2 is reviewable independently by checking that path ownership and naming decisions are documented in `docs/FOUNDATION.md` and skeleton README files.

---

## Phase 5: User Story 3 - Establish Non-Functional Baselines (Priority: P3)

**Goal**: Document practical v1 reliability, traceability, local recoverability, async status, and AI boundary expectations without introducing production hardening.

**Independent Test**: A reviewer can check any future import, job, analytics, or AI phase spec against the documented practical v1 baselines and AI source-data boundary.

### Implementation for User Story 3

- [X] T029 [US3] Add practical v1 non-functional baseline section for import traceability, clear failures, async status visibility, local recoverability, and data quality to `docs/FOUNDATION.md`
- [X] T030 [US3] Add excluded production hardening section for uptime SLAs, full monitoring, operational runbooks, and strict recovery objectives to `docs/FOUNDATION.md`
- [X] T031 [US3] Add AI boundary section stating AI may read validated productivity data and write separate insight outputs but must never mutate source logs, tasks, or imports to `docs/FOUNDATION.md`
- [X] T032 [US3] Add source-data authority and conflict-resolution rule for AI outputs to `docs/FOUNDATION.md`
- [X] T033 [US3] Add import, job, and AI traceability expectations to `backend/app/modules/imports/README.md`, `backend/app/modules/ai_insights/README.md`, and `backend/app/workers/README.md`
- [X] T034 [US3] Add quickstart validation reference for non-functional baselines and AI boundary to `docs/FOUNDATION.md`

**Checkpoint**: User Story 3 is reviewable independently by checking non-functional and AI-boundary sections in `docs/FOUNDATION.md` and related skeleton README files.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate the Phase 0 foundation package and ensure no out-of-scope implementation slipped in.

- [X] T035 [P] Run the feature context validation commands from `specs/001-foundation-architecture/quickstart.md`
- [X] T036 [P] Run the planning artifact review from `specs/001-foundation-architecture/quickstart.md`
- [X] T037 [P] Run skeleton path inspection for `backend/app/`, `frontend/`, and `docker/` using `specs/001-foundation-architecture/quickstart.md`
- [X] T038 Run forbidden output search from `specs/001-foundation-architecture/quickstart.md` and document any acceptable documentation-only matches in `docs/FOUNDATION.md`
- [X] T039 [P] Verify every Phase 0 skeleton README and placeholder under `backend/app/`, `frontend/`, and `docker/` contains explanatory content only and no runnable app behavior
- [X] T040 [P] Verify `docs/FOUNDATION.md` satisfies `specs/001-foundation-architecture/contracts/foundation-package.md`
- [X] T041 [P] Verify all Phase 0 paths follow naming conventions in `docs/FOUNDATION.md`
- [X] T042 Update `specs/001-foundation-architecture/quickstart.md` only if implementation changed validation commands or expected skeleton paths

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion; MVP scope.
- **User Story 2 (Phase 4)**: Depends on Foundational completion and benefits from US1 foundation doc sections.
- **User Story 3 (Phase 5)**: Depends on Foundational completion and can proceed after US1 establishes the foundation doc.
- **Polish (Phase 6)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational; no dependency on US2 or US3.
- **User Story 2 (P2)**: Can start after Foundational; should update the same `docs/FOUNDATION.md` after or coordinated with US1 to avoid file conflicts.
- **User Story 3 (P3)**: Can start after Foundational; should update the same `docs/FOUNDATION.md` after or coordinated with US1 to avoid file conflicts.

### Within Each User Story

- Update `docs/FOUNDATION.md` sections before adding references from README files.
- Add skeleton README ownership notes before final quickstart validation.
- Keep all placeholder files explanatory; do not add executable code.
- Complete each user story checkpoint before moving to the next priority if working sequentially.

### Parallel Opportunities

- T002, T003, and T004 can run in parallel because they touch different files.
- Foundational directory creation tasks T006 through T010 can run in parallel if implemented by separate workers because they create disjoint directory groups.
- US2 backend ownership notes T024 and T025 can run in parallel with frontend ownership notes T026 and T027.
- US3 module-specific traceability notes T033 can run after T031 and may be split by target README file.
- Polish validation tasks T035 through T041 can be run in parallel after all story work is complete.

---

## Parallel Example: User Story 2

```text
Task: "T024 Add backend module ownership notes to backend/app/modules/*/README.md"
Task: "T025 Add backend infrastructure ownership notes to backend/app/api/README.md, backend/app/core/README.md, backend/app/settings/README.md, backend/app/shared/README.md, and backend/app/workers/README.md"
Task: "T026 Add frontend ownership notes to frontend/app/README.md, frontend/components/README.md, frontend/features/README.md, frontend/hooks/README.md, frontend/lib/api/README.md, frontend/stores/README.md, and frontend/types/README.md"
Task: "T027 Add frontend feature ownership notes to frontend/features/*/README.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup.
2. Complete Phase 2 foundational skeleton directories.
3. Complete Phase 3 User Story 1.
4. Stop and validate that a new contributor can identify product purpose, v1 scope, out-of-scope items, and skeleton setup.

### Incremental Delivery

1. Setup plus Foundational: skeleton paths exist.
2. US1: foundation purpose and scope are documented.
3. US2: architecture and naming rules are locked in docs and skeleton ownership notes.
4. US3: practical v1 baselines and AI boundaries are documented.
5. Polish: quickstart and artifact contract validation pass.

### Parallel Team Strategy

With multiple contributors:

1. One contributor handles shared setup and foundational skeleton creation.
2. One contributor drafts `docs/FOUNDATION.md` scope sections for US1.
3. One contributor adds backend/frontend ownership README files for US2 after skeleton paths exist.
4. One contributor adds non-functional and AI-boundary notes for US3 after `docs/FOUNDATION.md` exists.

---

## Notes

- [P] tasks use different files or disjoint path groups.
- User story labels map to the three user stories in `spec.md`.
- This task list intentionally avoids service tests, API integration tests, database migrations, app shells, and quality gates because Phase 0 is skeleton-only.
- Stop if a task would require implementing runnable backend, frontend, database, worker, import, dashboard, or AI behavior.
