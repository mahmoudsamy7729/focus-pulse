# Research: Insights & Recommendations

## Decision: Generate Phase 5 Outputs with Deterministic Rules Only

**Rationale**: The clarified spec requires no new AI provider call during Phase 5. Deterministic rules make productivity scores, consistency scores, best/worst day findings, and recommendation validation explainable, repeatable, and testable. Completed Phase 4 analysis output remains an input, but saved tracking facts stay authoritative when generated observations conflict with source data.

**Alternatives considered**:

- New AI call for recommendations: rejected because it adds provider failure modes and violates the clarification.
- Hybrid deterministic scores plus AI wording: rejected because wording could still introduce unsupported claims and privacy risks.

## Decision: Store Phase 5 Results Separately from Phase 4 Runs

**Rationale**: Phase 4 `AIInsightRun` records represent analysis execution attempts. Phase 5 `AIInsightResult` records represent deterministic derived outputs with separate validation, current-result, rerun, recommendation, and evidence semantics. Separate persistence keeps audit trails clear and avoids mutating completed Phase 4 runs.

**Alternatives considered**:

- Add Phase 5 payloads directly to `AIInsightRun`: rejected because it mixes source analysis lifecycle with derived recommendation lifecycle.
- Store only computed JSON without a result entity: rejected because current-result selection, soft delete, history, validation status, and audit metadata need first-class persistence.

## Decision: Use Synchronous API Generation

**Rationale**: Phase 5 generation is deterministic, bounded to one day or one seven-day week, and does not perform provider calls or long-running imports. A request/response service path simplifies user feedback and avoids unnecessary Celery complexity.

**Alternatives considered**:

- Celery job for every generation request: rejected as unnecessary for bounded deterministic work and because it would add status polling without a Phase 5 need.
- Frontend-only scoring: rejected because persistence, audit, privacy validation, and source authority must be enforced server-side.

## Decision: Resolve Source Analysis from Current Phase 4 Run by Default

**Rationale**: Users generally expect insights for the latest completed analysis for the selected period. The API may accept a specific `source_ai_insight_run_id` for traceability and reproducible review. Generation fails with a handled error if no completed source analysis exists or if the source analysis does not match the requested owner and period.

**Alternatives considered**:

- Always require the source analysis run ID: rejected because it makes the main user flow harder.
- Use failed or incomplete analysis with warnings: rejected because the spec requires missing, failed, incomplete, or malformed Phase 4 output to block successful insight generation.

## Decision: Use Owner + Period + Source Analysis as the Default Idempotency Boundary

**Rationale**: The clarified spec says default generation for the same period and source analysis returns the existing current result. This deduplicates repeated clicks and retry submissions while preserving explicit reruns as a history-creating action.

**Alternatives considered**:

- Always create a new result: rejected because it creates duplicate current results from identical evidence.
- Overwrite existing result: rejected because prior generated results must remain reviewable.
- Only use client idempotency keys: rejected because duplicate default generations should dedupe even without a client-provided key.

## Decision: Represent Scores, Evidence, Day Findings, and Recommendations as Structured JSON Payloads

**Rationale**: Score explanations, evidence links, recommendation validation outcomes, and best/worst findings are nested, versioned output structures. JSON payloads keep them flexible while the result table stores stable metadata for querying and current-result selection.

**Alternatives considered**:

- Fully normalized tables for every score factor and recommendation field: rejected for Phase 5 because the payload is read-mostly and likely to evolve.
- Single free-text output blob: rejected because validation, UI rendering, and traceability require structured fields.

## Decision: Validation Happens Before a Result Becomes Successful and Current

**Rationale**: The spec requires invalid scores or recommendations not to be marked successful. Service-level validation checks score bounds, insufficient-data states, evidence counts, recommendation count, actionability, duplicate/generic recommendations, unsupported claims, source period consistency, and privacy boundaries.

**Alternatives considered**:

- Validate only in tests: rejected because production must not persist invalid current results.
- Validate in the frontend: rejected because API clients must receive reliable, persisted results regardless of UI behavior.

## Decision: Add a Minimal Frontend Review Flow

**Rationale**: Phase 5 includes user review of scores, evidence, best/worst days, recommendations, and history. A small dashboard route and feature components can satisfy this without broad dashboard redesign. TanStack Query handles current result, generate/rerun mutations, and history fetching.

**Alternatives considered**:

- Backend-only Phase 5: rejected because result review is part of the feature value.
- Full dashboard redesign: rejected because the spec excludes dashboard redesign from Phase 5.

## Decision: Keep Note Text Outside All Phase 5 Inputs and Outputs

**Rationale**: Phase 4 established the privacy boundary and Phase 5 must preserve it. Task names, durations, categories, and tags may support evidence; note text must not be read into input summaries, copied into result payloads, rendered in the UI, or used for recommendation text.

**Alternatives considered**:

- Use notes internally but hide them in UI: rejected because the spec excludes note text from Phase 5 inputs, explanations, and recommendations.
- Allow note snippets as evidence: rejected for the same privacy-boundary reason.
