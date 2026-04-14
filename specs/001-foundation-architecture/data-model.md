# Data Model: Foundation & Architecture

Phase 0 does not create database models or persistent application data. These entities describe the planning artifacts and reviewable concepts that make up the foundation package.

## Foundation Package

**Purpose**: The complete Phase 0 deliverable that future phases use as the source of architecture truth.

**Fields**:

- `feature_branch`: `001-foundation-architecture`
- `spec_path`: `specs/001-foundation-architecture/spec.md`
- `plan_path`: `specs/001-foundation-architecture/plan.md`
- `research_path`: `specs/001-foundation-architecture/research.md`
- `quickstart_path`: `specs/001-foundation-architecture/quickstart.md`
- `contract_path`: `specs/001-foundation-architecture/contracts/foundation-package.md`
- `foundation_doc_path`: planned `docs/FOUNDATION.md`
- `status`: draft, ready_for_tasks, implemented

**Relationships**:

- Contains Architecture Rules, Scope Boundaries, Platform Decisions, Naming Conventions, Non-Functional Baselines, AI Boundary, and Skeleton Artifacts.

**Validation Rules**:

- Must remain Phase 0 only.
- Must include no runnable app shell requirement.
- Must identify future module locations in under 10 minutes of review.

## Architecture Rule

**Purpose**: A governance rule that future phases must follow.

**Fields**:

- `name`: short rule name
- `statement`: required behavior or boundary
- `applies_to`: backend, frontend, jobs, imports, AI, docs, or repo
- `source`: constitution, `docs/STACK_AND_STRUCTURE.md`, `docs/Plan.md`, or clarified spec
- `enforcement_method`: review checklist, skeleton path ownership, future task validation

**Relationships**:

- May constrain one or more Skeleton Artifacts.
- May be referenced by future phase plans.

**Validation Rules**:

- Must be testable by review.
- Must not introduce implementation work outside Phase 0.

## Scope Boundary

**Purpose**: An include/exclude decision that prevents phase drift.

**Fields**:

- `name`: boundary label
- `included`: what Phase 0 permits
- `excluded`: what Phase 0 defers
- `future_phase`: phase where excluded work can be reconsidered

**Relationships**:

- Belongs to Foundation Package.
- Informs future task decomposition.

**Validation Rules**:

- Must clearly distinguish skeleton work from runnable app behavior.
- Must defer domain behavior to later phases.

## Platform Decision

**Purpose**: A locked technology or architecture choice.

**Fields**:

- `area`: backend, frontend, database, jobs, AI, ingestion, orchestration
- `decision`: selected platform choice
- `reason`: why it is locked
- `phase_0_action`: document, reserve skeleton path, or defer implementation

**Relationships**:

- Supports Skeleton Artifacts and Architecture Rules.

**Validation Rules**:

- Must map to an explicit choice from `docs/Plan.md`, the constitution, or `docs/STACK_AND_STRUCTURE.md`.
- Must not require implementation during Phase 0 unless it is a placeholder artifact.

## Naming Convention

**Purpose**: Canonical naming rules for future files, modules, specs, branches, entities, and jobs.

**Fields**:

- `backend_modules`: snake_case
- `specs_and_branches`: kebab-case with numeric prefix where applicable
- `domain_entities`: PascalCase
- `background_jobs`: descriptive names
- `frontend_routes`: product-language route segments

**Relationships**:

- Applies to Skeleton Artifacts.
- Constrains future feature specs and tasks.

**Validation Rules**:

- 100% of Phase 0 skeleton paths and placeholder names must follow the convention.

## Non-Functional Baseline

**Purpose**: Practical v1 quality expectations for future phases.

**Fields**:

- `import_traceability`: required for future imports
- `clear_failures`: required for future user-facing and operational failures
- `async_status_visibility`: required for future background work
- `local_recoverability`: required for future imports and jobs
- `data_quality`: foundational expectation for analytics and AI
- `excluded_operations`: uptime SLA, full monitoring, operational runbooks, strict recovery objectives

**Relationships**:

- Constrains future import, job, analytics, and AI plans.

**Validation Rules**:

- Must remain practical v1, not production hardening.
- Must be measurable through later phase acceptance criteria.

## AI Boundary

**Purpose**: Protect source productivity data from AI mutation.

**Fields**:

- `read_allowed`: validated productivity data
- `write_allowed`: separate AI insight outputs
- `write_forbidden`: source logs, tasks, imports
- `conflict_resolution`: source records remain authoritative

**Relationships**:

- Constrains future `ai_insights` module work.
- Relates to Scope Boundary and Non-Functional Baseline.

**Validation Rules**:

- Future AI features must be reviewable against this boundary in under 5 minutes.

## Skeleton Artifact

**Purpose**: A placeholder folder, doc, env example, compose placeholder, or architecture note that makes future ownership visible.

**Fields**:

- `path`: repository path
- `artifact_type`: folder, placeholder_doc, env_example, compose_placeholder, architecture_note
- `owner_area`: backend, frontend, docker, docs, root
- `allowed_content`: placeholder or explanatory content only
- `forbidden_content`: production logic, schemas, endpoints, workers, dashboard behavior, AI analysis, CI gates

**Relationships**:

- Belongs to Foundation Package.
- Must comply with Naming Convention and Architecture Rules.

**Validation Rules**:

- Must be inspectable without running the app.
- Must not require dependency installation.

## Compliance Review

**Purpose**: A future review action that checks whether a phase or artifact obeys Phase 0.

**Fields**:

- `review_target`: plan, task list, skeleton artifact, or future implementation
- `checked_rules`: list of Architecture Rules and Scope Boundaries
- `result`: pass, fail, amendment_required
- `notes`: concise explanation

**Relationships**:

- References Foundation Package decisions.

**Validation Rules**:

- Must classify proposed work as in scope, out of scope, or amendment required.
