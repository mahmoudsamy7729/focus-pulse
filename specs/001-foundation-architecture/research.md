# Research: Foundation & Architecture

## Decision: Phase 0 Deliverable Shape

**Decision**: Phase 0 produces a foundation package made of documentation plus skeleton-only repository setup.

**Rationale**: The clarified specification states that Phase 0 must define project rules, scope, architecture, naming, non-functional baselines, v1 boundaries, and baseline repo setup. It must not implement production domain behavior or runnable app shells.

**Alternatives considered**:

- Documentation only: rejected because the clarified spec requires baseline repo setup artifacts.
- Runnable backend/frontend shells: rejected because this would pull app bootstrapping into Phase 0 and risk bleeding into Phase 1.
- Full platform baseline: rejected because database, Redis, worker, and quality gate enforcement are later implementation concerns.

## Decision: Repository Skeleton Scope

**Decision**: Phase 0 skeleton setup is limited to folders, placeholder documentation, environment examples, compose placeholders, and architecture notes.

**Rationale**: This gives future phases visible ownership boundaries without creating runnable code, schemas, workers, dashboards, imports, or AI behavior early.

**Alternatives considered**:

- Skeleton plus app shells: rejected as too much implementation for Phase 0.
- Skeleton plus CI/lint/test gates: rejected because clarified Phase 0 excludes quality gate enforcement.
- No skeleton: rejected because future phase planning needs concrete target paths.

## Decision: Target Architecture Layout

**Decision**: Use the constitution and `docs/STACK_AND_STRUCTURE.md` as the target layout: `backend/app/` for backend application structure, `frontend/` for Next.js dashboard structure, `docker/` for local orchestration placeholders, and `docs/FOUNDATION.md` for the Phase 0 foundation summary.

**Rationale**: The constitution is the current governance source, and the stack document provides detailed path ownership. The current repo contains `backend/src/`, but the accepted target layout is `backend/app/`; Phase 0 should plan alignment rather than add new work to the wrong layout.

**Alternatives considered**:

- Keep `backend/src/` as the target: rejected because it conflicts with the constitution and planning template.
- Create feature logic under target directories now: rejected because Phase 0 is skeleton-only.

## Decision: Naming Conventions

**Decision**: Use snake_case for backend modules, kebab-case for specs and branches, PascalCase for domain entities, and descriptive background job names.

**Rationale**: This matches the clarified spec and the existing plan terms such as `daily_logs`, `ai_insights`, and `001-foundation-architecture`.

**Alternatives considered**:

- Kebab-case everywhere: rejected because Python module folders should use snake_case.
- CamelCase/PascalCase folders: rejected because it conflicts with backend module conventions and route/product naming conventions.

## Decision: Practical v1 Non-Functional Baseline

**Decision**: Lock practical v1 baselines: import traceability, clear failures, async status visibility, local recoverability, data quality, and incremental phase delivery. Exclude uptime SLAs, full monitoring, operational runbooks, and strict recovery objectives from Phase 0.

**Rationale**: FocusPulse is a personal productivity v1; the foundation must protect data quality and traceability without turning Phase 0 into production hardening.

**Alternatives considered**:

- Production-grade operations baseline: rejected as premature for Phase 0 and v1 scope.
- Minimal data-quality-only baseline: rejected because future imports, jobs, and AI runs need traceability and recoverability expectations.

## Decision: AI Boundary

**Decision**: AI may read validated productivity data and write separate AI insight outputs later, but must never mutate source logs, tasks, or imports.

**Rationale**: Source productivity data must remain deterministic and authoritative. AI output can be regenerated, corrected, and audited separately.

**Alternatives considered**:

- AI annotates source records: rejected because it blurs generated output with source-of-truth data.
- Fully defer AI boundaries: rejected because Phase 0 explicitly locks AI boundaries.

## Decision: Contracts for Phase 0

**Decision**: Generate an artifact contract rather than an OpenAPI/runtime contract.

**Rationale**: Phase 0 exposes no API endpoints. The useful contract is the required shape of the foundation package that reviewers and future phases consume.

**Alternatives considered**:

- OpenAPI contract: rejected because no runtime API is in scope.
- No contract: rejected because Phase 0 outputs need reviewable acceptance criteria.
