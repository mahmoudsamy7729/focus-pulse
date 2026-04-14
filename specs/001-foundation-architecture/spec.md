# Feature Specification: Foundation & Architecture

**Feature Branch**: `001-foundation-architecture`  
**Created**: 2026-04-14  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 0 - Foundation & Architecture only"

## Clarifications

### Session 2026-04-14

- Q: Should Phase 0 be documentation-only, or include repo setup? -> A: Documentation plus repo setup: add baseline folders/configs needed to enforce the architecture.
- Q: What baseline repo setup should Phase 0 include? -> A: Skeleton only: folders, placeholder docs, env examples, compose placeholders, and architecture notes.
- Q: What naming convention should Phase 0 lock? -> A: Snake case modules, kebab-case specs/branches, PascalCase domain entities, descriptive job names.
- Q: What level of non-functional baseline should Phase 0 lock? -> A: Practical v1 baselines: import traceability, clear failures, async status, local recoverability, no uptime SLA.
- Q: What AI boundary should Phase 0 lock? -> A: AI can read validated productivity data and write separate AI insight outputs, but never mutate source logs, tasks, or imports.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Define Project Purpose and Scope (Priority: P1)

As the project owner, I want a foundation package that explains what FocusPulse is, what v1 includes, what v1 excludes, and what baseline repo setup supports those boundaries, so future phase work does not drift beyond the intended product architecture.

**Why this priority**: Phase 0 must establish the product purpose and scope before domain modeling, import workflows, dashboards, or AI work begin.

**Independent Test**: Can be tested by giving the foundation package to a new contributor and verifying they can identify the product purpose, v1 boundaries, out-of-scope items, and baseline repo setup without reading any later phase plans.

**Acceptance Scenarios**:

1. **Given** a contributor has only the Phase 0 specification, **When** they review the project purpose, **Then** they can state that FocusPulse is a personal productivity system for Notion CSV daily logs, structured analysis, and actionable dashboard insights.
2. **Given** a contributor is planning future work, **When** they review v1 scope boundaries, **Then** they can distinguish included v1 work from future integrations and polish work.
3. **Given** a contributor reviews the repository after Phase 0, **When** they inspect skeleton folders, placeholder docs, environment examples, compose placeholders, and architecture notes, **Then** they can see where future backend, frontend, job, import, and AI work belongs.

---

### User Story 2 - Lock Architecture and Conventions (Priority: P2)

As an implementer, I want explicit architecture rules, naming conventions, platform decisions, and baseline repository structure, so later phases use consistent boundaries and avoid conflicting project structure.

**Why this priority**: Later phases depend on consistent module boundaries, data ownership rules, and agreed platform choices.

**Independent Test**: Can be tested by reviewing a proposed Phase 1 or Phase 2 implementation plan and checking whether it follows the locked architecture rules and conventions.

**Acceptance Scenarios**:

1. **Given** a later phase proposes business logic in request handlers, **When** the proposal is compared against Phase 0 rules, **Then** it is rejected as out of compliance.
2. **Given** a later phase proposes database access outside the repository layer, **When** the proposal is compared against Phase 0 rules, **Then** it is rejected as out of compliance.
3. **Given** a later phase introduces import, job, or AI behavior, **When** the proposal is reviewed, **Then** it must follow the locked module boundaries and naming conventions.
4. **Given** a later phase adds files to the repository, **When** their locations are reviewed, **Then** they must align with the skeleton repo structure established in Phase 0.

---

### User Story 3 - Establish Non-Functional Baselines (Priority: P3)

As a reviewer, I want practical v1 reliability, traceability, recoverability, and AI-boundary expectations, so future phase specs can be judged against the same quality bar without requiring production hardening.

**Why this priority**: The project relies on import quality, repeatable background work, and explainable AI outputs; these expectations need to be defined before implementation tasks begin, while uptime SLAs and production operations remain outside Phase 0.

**Independent Test**: Can be tested by checking whether each later phase spec references the baseline expectations for data quality, traceability, async work, and AI isolation where relevant.

**Acceptance Scenarios**:

1. **Given** a later phase handles CSV imports, **When** its requirements are reviewed, **Then** it must include validation, traceability, clear failure visibility, and local recovery expectations.
2. **Given** a later phase handles AI analysis, **When** its requirements are reviewed, **Then** AI behavior must remain isolated from core data ownership, read only validated productivity data, and produce separate traceable insight outputs.
3. **Given** a later phase includes heavy or long-running work, **When** its requirements are reviewed, **Then** async execution and status tracking expectations must be defined.

### Edge Cases

- If a future phase conflicts with a Phase 0 architecture decision, Phase 0 remains the source of truth until the foundation spec is explicitly revised.
- If a feature appears useful but belongs to a later phase, it must be recorded as out of scope for the current phase instead of being implemented early.
- If AI analysis requirements conflict with deterministic import or reporting behavior, deterministic data quality and traceability take priority.
- If CSV ingestion and future Notion API ingestion conflict, CSV-first ingestion remains the v1 boundary.
- If a technology or naming convention is missing from Phase 0, later phases must document a proposed amendment before relying on it.
- If skeleton setup would require runnable app shells, quality gates, or production behavior, that work must be deferred to the appropriate later phase unless explicitly added through a Phase 0 amendment.
- If proposed names conflict with Phase 0 conventions, later phases must rename them before implementation planning is accepted.
- If a later phase proposes production uptime targets, full monitoring, operational runbooks, or strict recovery objectives, those requirements must be deferred unless a later phase explicitly expands the product maturity target.
- If AI output conflicts with source productivity records, source logs, tasks, and imports remain authoritative and AI output must be corrected or regenerated separately.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The foundation specification MUST define the product purpose as a personal productivity system that uses daily logs exported from Notion CSV files, normalizes structured records, analyzes behavior, and presents actionable dashboard insights.
- **FR-002**: The foundation specification MUST define v1 scope boundaries as Phase 1, Phase 2, Phase 3, and Basic Phase 4 only.
- **FR-003**: The foundation specification MUST identify future work that is outside v1, including UI polish, performance improvements beyond baseline needs, report exports, Notion API integration, and AI chat.
- **FR-004**: The foundation specification MUST lock the approved platform decisions from the project plan: FastAPI for backend, Next.js for frontend, PostgreSQL for database storage, Celery plus Redis for background jobs, isolated AI boundaries, and CSV-first ingestion.
- **FR-005**: The foundation specification MUST define module boundary rules for daily logs, tasks, notes, imports, analytics, AI insights, and workers.
- **FR-006**: The foundation specification MUST state that business logic belongs outside request routing layers.
- **FR-007**: The foundation specification MUST state that database access belongs inside repository boundaries.
- **FR-008**: The foundation specification MUST state that import pipeline work must prioritize validation, normalization, deduplication, failure visibility, and traceability.
- **FR-009**: The foundation specification MUST state that AI logic must remain isolated in the AI insights area, may read validated productivity data, may write separate AI insight outputs, and must never mutate source logs, tasks, or imports.
- **FR-010**: The foundation specification MUST state that heavy, retryable, or long-running operations use background job behavior with status tracking.
- **FR-011**: The foundation specification MUST define naming conventions for feature phases, modules, background jobs, import runs, AI insight runs, and user-facing dashboard concepts.
- **FR-012**: The foundation specification MUST define practical v1 non-functional baselines for import traceability, clear failures, async status visibility, local recoverability, data quality, and incremental phase delivery.
- **FR-013**: The foundation specification MUST require each future phase to be represented by one Spec Kit spec, one branch, and one bounded implementation cycle.
- **FR-014**: The foundation specification MUST define how later phase plans are checked for compliance against Phase 0 before implementation begins.
- **FR-015**: Phase 0 MUST include skeleton-only repository setup artifacts that define where future backend, frontend, background job, import, AI insight, documentation, and configuration work belongs.
- **FR-016**: Phase 0 repo setup MUST avoid implementing production domain behavior for later phases while still making future architecture boundaries visible and reviewable.
- **FR-017**: Phase 0 skeleton setup MUST be limited to folders, placeholder documentation, environment examples, compose placeholders, and architecture notes.
- **FR-018**: Phase 0 skeleton setup MUST NOT require runnable backend or frontend app shells, lint/test/type-check gates, CI workflows, database schemas, workers, import logic, dashboard behavior, or AI analysis behavior.
- **FR-019**: Phase 0 naming conventions MUST use snake_case for modules, kebab-case for specs and branches, PascalCase for domain entities, and descriptive names for background jobs.
- **FR-020**: Phase 0 skeleton paths and placeholder names MUST follow the locked naming conventions.
- **FR-021**: Phase 0 MUST state that production uptime SLAs, full monitoring, operational runbooks, and strict recovery objectives are outside the Phase 0 baseline.
- **FR-022**: Phase 0 MUST state that source logs, tasks, and imports remain authoritative when AI insight outputs conflict with source productivity data.

### Key Entities *(include if feature involves data)*

- **Foundation Specification**: The Phase 0 source of truth that captures purpose, scope, architecture decisions, naming conventions, and quality baselines.
- **Foundation Package**: The combined Phase 0 deliverable containing the foundation specification and skeleton-only repo setup artifacts.
- **Architecture Rule**: A project constraint that future phases must follow, such as business logic placement, repository ownership, module isolation, or async job usage.
- **Scope Boundary**: A clear include-or-exclude decision that prevents later phases from implementing future work during v1.
- **Platform Decision**: A locked technology choice or integration boundary that future implementation plans must respect.
- **Naming Convention**: A documented naming rule using snake_case modules, kebab-case specs and branches, PascalCase domain entities, and descriptive background job names.
- **Non-Functional Baseline**: A practical v1 quality expectation for import traceability, clear failures, async status visibility, local recoverability, data quality, or delivery discipline.
- **AI Boundary**: A rule that allows AI to read validated productivity data and write separate AI insight outputs while preventing AI from mutating source logs, tasks, or imports.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A new contributor can identify the product purpose, v1 scope, and out-of-scope future work in under 10 minutes using only the Phase 0 specification.
- **SC-002**: 100% of later phase plans can be checked against explicit Phase 0 architecture rules before implementation begins.
- **SC-003**: 100% of locked platform decisions listed in the Phase 0 section of Plan.md are represented in the foundation specification.
- **SC-004**: 100% of future phase specs can reference a defined rule for module boundaries, import reliability, AI isolation, or async job handling when those concerns apply.
- **SC-005**: Reviewers can classify any proposed v1 task as in scope, out of scope, or requiring a Phase 0 amendment without relying on undocumented assumptions.
- **SC-006**: A reviewer can inspect the Phase 0 skeleton setup and identify the intended location for each future module area in under 10 minutes.
- **SC-007**: A reviewer can confirm Phase 0 contains no runnable app shells, production domain behavior, or quality gate enforcement in under 10 minutes.
- **SC-008**: 100% of Phase 0 skeleton paths and placeholder names follow the locked naming conventions.
- **SC-009**: A reviewer can identify the required practical v1 reliability expectations and the excluded production hardening expectations in under 10 minutes.
- **SC-010**: A reviewer can determine whether any future AI feature violates the read-only source data boundary in under 5 minutes.

## Assumptions

- FocusPulse is a personal productivity product for a single primary user or small personal workspace during v1.
- Phase 0 includes planning, governance, and skeleton-only repository setup; it does not include production domain behavior, runnable app shells, quality gate enforcement, uptime SLAs, full monitoring, operational runbooks, or strict recovery objectives for later phases.
- The existing docs/Plan.md Phase 0 section is the authoritative input for this specification.
- Later phases will create separate Spec Kit specs and must not combine multiple phases into one implementation cycle.
- Named platform decisions are intentionally part of Phase 0 because the project plan explicitly requires them to be locked before implementation.
