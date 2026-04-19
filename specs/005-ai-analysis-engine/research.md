# Research: AI Analysis Engine

## Decision: Combined Daily or Weekly Analysis Run

**Decision**: Phase 4 uses one combined AI analysis run per selected day or week. Each completed run produces one output containing summary, detected patterns, behavior insights, supporting evidence, limitations, generated timestamp, and output outcome.

**Rationale**: The clarified spec selects one combined run. This keeps Basic Phase 4 smaller, easier to trace, and simpler to retry than separate summary, pattern, and behavior-insight jobs. It still leaves room to split specialized analysis types in a later phase if the combined output becomes too large or costly.

**Alternatives considered**:

- Separate run types for summary, pattern detection, and behavior insights: rejected because it adds orchestration, status, and current-result complexity before there is evidence that Basic Phase 4 needs it.
- Summary-only Phase 4 with patterns deferred: rejected because Plan.md explicitly includes pattern detection and behavior insights in Phase 4.

## Decision: AI Provider Boundary and Testability

**Decision**: Add a module-local provider abstraction under `backend/app/modules/ai_insights/providers/`. Production configuration selects the provider/model through AI settings, while tests use a deterministic fake provider.

**Rationale**: The constitution requires AI behavior to stay isolated in `ai_insights`. A provider boundary keeps prompt preparation, provider calls, and output parsing out of routers and unrelated modules. Deterministic provider tests avoid network dependency and make output validation, retry behavior, and failure paths testable.

**Alternatives considered**:

- Call a provider SDK directly from the service: rejected because it couples use-case logic to one vendor and makes retries/failure tests brittle.
- Put provider code in shared infrastructure: rejected because AI orchestration is feature-specific and belongs in `ai_insights`.
- Hard-code fake generated output without a provider boundary: rejected because it would not exercise the planned production orchestration shape.

## Decision: Privacy-Bounded Structured Input

**Decision**: Build structured AI inputs from period boundaries, saved task names, tracked durations, categories, tags, and aggregate totals. Exclude note text from AI inputs and generated outputs.

**Rationale**: The clarified spec chose the note-exclusion privacy boundary. Task names, durations, categories, and tags provide enough signal for basic summaries and patterns while reducing exposure of potentially sensitive free-form notes.

**Alternatives considered**:

- Include notes: rejected because the clarification selected note exclusion.
- Use aggregates only: rejected because task themes are required for Phase 4 pattern detection and behavior insights.
- Local-only AI processing as a hard requirement: rejected for this plan because the spec does not mandate local-only execution and provider choice is an implementation/configuration concern inside the `ai_insights` boundary.

## Decision: Retained Input Summary Instead of Full Input Payload

**Decision**: Retain source DailyLog references, source record counts, aggregate input summary, instruction name/version, output, and run metadata. Do not retain the full structured AI input payload after the run records the retained summary.

**Rationale**: This matches the clarification answer and balances auditability with data minimization. Source references allow reviewers to reconstruct why an output was produced, while aggregate summary and instruction version explain run context without keeping the full prompt/input payload.

**Alternatives considered**:

- Store full structured input: rejected because it retains more potentially sensitive task detail than needed.
- Store only output and run metadata: rejected because it weakens traceability and makes source-data drift harder to investigate.

## Decision: Shared Status Vocabulary with Output Outcome

**Decision**: Use existing shared statuses `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`. No-data requests finish with status `completed` and output outcome `no_data`. Successful generated outputs use output outcome `analysis_generated`.

**Rationale**: Phase 1 already defines the shared run status vocabulary for `AIInsightRun`. Treating no-data as a completed run avoids classifying an empty period as an error while preserving a traceable audit record.

**Alternatives considered**:

- Add a new `completed_no_data` status: rejected because it conflicts with the shared vocabulary.
- Use `completed_with_errors`: rejected because an empty period is not an error.
- Reject before creating a run: rejected because the user needs traceability that the request was made and why no analysis was generated.

## Decision: Retry Policy

**Decision**: Retry transient AI analysis failures up to 3 total attempts per run. If all attempts fail, mark the run `failed` with final failure details and preserve attempt history in run metadata.

**Rationale**: Three total attempts gives reasonable recovery from temporary provider, timeout, or worker errors without creating open-ended work. It is easy to test through `retry_count` and attempt metadata.

**Alternatives considered**:

- Two total attempts: rejected because it gives less resilience for temporary provider issues.
- No automatic retries: rejected because Plan.md requires retry support.
- Retry until timeout budget is exhausted: rejected because it is harder to reason about, test, and audit.

## Decision: Request Idempotency and In-Flight Conflict Handling

**Decision**: Create-analysis requests accept an optional `Idempotency-Key`. If the same owner submits the same key for the same period granularity and period, return the existing run. If a matching run is already `pending` or `processing` without the same idempotency key, return a conflict instead of creating another in-flight current result. Explicit rerun requests always create a separate run after validating the source run belongs to the owner.

**Rationale**: The constitution requires idempotency for AI runs and background jobs. Optional idempotency keys protect clients from duplicate submissions, while in-flight conflict handling keeps run history understandable when users click twice without a key.

**Alternatives considered**:

- Always create a new run: rejected because duplicate submissions could create conflicting current results.
- Require idempotency keys for all create requests: rejected because the current API style treats idempotency keys as optional and still handles conflicts safely.
- Coalesce all same-period requests forever: rejected because reruns are an explicit feature and must create new history.

## Decision: API Surface

**Decision**: Expose backend APIs for create run, rerun, get run status/output, get latest current result, and list run history. Use `/api/v1/ai-insights/...`, success/error envelopes, `ai_insights:read`/`ai_insights:write` scopes, and `page`/`limit` pagination for history.

**Rationale**: Phase 4 must let users request analysis, check asynchronous status, view stored results, rerun, and inspect failures. This API surface covers those flows without adding frontend UI or scheduled automation.

**Alternatives considered**:

- Worker-only/internal service with no API: rejected because user scenarios require request/status/history review.
- Add dashboard UI in Phase 4: rejected because dashboard visualization changes are out of scope.
- Add scheduled endpoints: rejected because scheduled AI runs belong to Phase 6.
