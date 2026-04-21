# Research: Automation & Reliability

## Decision: Keep Schedule Ownership in Existing Approved Modules

**Decision**: Do not create a new `automation` backend module. Scheduled import behavior belongs in `backend/app/modules/imports/`; scheduled AI analysis behavior belongs in `backend/app/modules/ai_insights/`; shared due-window calculations and Celery Beat wiring belong under `backend/app/workers/`.

**Rationale**: The constitution lists approved backend modules and does not include `automation`. The Phase 6 scope maps to `workers`, `imports`, and `ai_insights`, so the plan preserves module ownership while still sharing infrastructure where it is operational rather than feature-specific.

**Alternatives considered**:

- Create `backend/app/modules/automation/`: rejected because it would add an unapproved module and blur import/AI ownership.
- Put all schedule behavior in `backend/app/workers/`: rejected because schedule validation, persistence, and user-facing APIs are feature business behavior, not worker infrastructure.
- Duplicate all scheduling logic in `imports` and `ai_insights`: rejected because due-window calculation and Celery Beat integration are shared operational concerns.

## Decision: Use User-Configured CSV Source References for Scheduled Imports

**Decision**: Scheduled imports store a user-configured CSV source reference and consume only newly available CSV input. They retain source metadata, run status, row counts, and row outcomes only, never full raw CSV contents.

**Rationale**: This directly follows the clarified spec and preserves the Phase 2 raw CSV non-retention guarantee. It also keeps Notion API synchronization and arbitrary external connectors out of Phase 6.

**Alternatives considered**:

- Reuse the most recent uploaded CSV file: rejected because it conflicts with raw file non-retention and risks repeated stale imports.
- Implement Notion API synchronization: rejected as Phase 7 scope.
- Add arbitrary connector support: rejected because it expands the import contract beyond CSV and would require connector-specific security and failure rules.

## Decision: Use Celery Beat as the Periodic Scheduler

**Decision**: Add Celery Beat service wiring and a thin scheduled evaluator task. The evaluator locates due schedule windows and delegates import or AI analysis work to module services and existing worker tasks.

**Rationale**: Celery and Redis are already approved and present in the backend stack. The constitution explicitly expects `celery_beat` only when scheduled jobs are introduced by a later phase, and Phase 6 introduces scheduled jobs.

**Alternatives considered**:

- Run schedule evaluation inside API requests: rejected because automation should not depend on user traffic and would blur request handling with background work.
- Add a separate scheduler service outside Celery: rejected because it adds infrastructure outside the approved stack.
- Use database triggers: rejected because schedule behavior needs service-layer validation, ownership checks, idempotency, and audit details.

## Decision: Deduplicate Scheduled Work by Schedule Window

**Decision**: Scheduled work idempotency uses owner, schedule ID, automation type, due window, and target source/period. Retries reuse the same scheduled run history record and link to the same import run or AI analysis run when applicable.

**Rationale**: The constitution requires idempotency for background jobs. The schedule-window key prevents duplicate work when Celery Beat fires twice, workers retry, or two evaluator instances overlap.

**Alternatives considered**:

- Rely only on Celery task IDs: rejected because task IDs do not express domain uniqueness and do not protect against duplicate scheduler evaluation.
- Rely only on import task deduplication or AI in-flight conflict handling: rejected because Phase 6 needs schedule-level history and skipped-window semantics before downstream work starts.
- Require client idempotency keys: rejected because scheduled work is system-triggered and cannot depend on a client-provided key.

## Decision: Represent Skipped Windows as Completed History Outcomes

**Decision**: Schedule windows that are intentionally skipped, missed, or have no new data use shared run status `completed` with an explicit schedule-run outcome such as `skipped`, `missed`, or `no_new_data`.

**Rationale**: The spec requires shared statuses and says skipped/no-new-data outcomes must not fabricate successful import data or AI observations. A separate outcome field preserves status vocabulary while making skipped windows reportable.

**Alternatives considered**:

- Add `skipped` to the shared run status enum: rejected because it changes a shared vocabulary used by prior phases.
- Mark skipped windows as `failed`: rejected because skipped/no-new-data windows are expected outcomes, not failures.
- Do not record skipped windows: rejected because downtime and no-new-data behavior must be auditable.

## Decision: Process Only the Latest Missed Window After Downtime

**Decision**: When downtime causes multiple missed due windows, process only the latest missed window for each active schedule and record older missed windows as skipped.

**Rationale**: This follows the clarified spec and bounds catch-up work. It avoids sudden large backfills while preserving audit visibility for missed windows.

**Alternatives considered**:

- Backfill every missed window: rejected because it can create heavy delayed work and complicates idempotency and user expectations.
- Skip all missed windows: rejected because it loses the chance to recover the latest daily/weekly state after downtime.

## Decision: Retain Detailed Automation History for 90 Days

**Decision**: Automation run history and audit details remain reviewable for at least 90 days. After 90 days, non-current diagnostic detail may be pruned while final outcome summaries remain available.

**Rationale**: This follows the clarified spec and provides enough operational history for troubleshooting without turning schedule diagnostics into indefinite analytics storage.

**Alternatives considered**:

- Retain all details indefinitely: rejected because it increases long-term storage and privacy exposure without clear v1 value.
- Retain only 30 days: rejected because monthly usage/debug cycles may need more lookback.
- Keep only latest run per schedule: rejected because it would not support failure trend investigation or downtime review.

## Decision: Split API Contracts Under Existing Feature Prefixes

**Decision**: Import schedule APIs live under `/api/v1/imports/schedules`; AI analysis schedule APIs live under `/api/v1/ai-insights/analysis-schedules`.

**Rationale**: This keeps owner permissions, rate limits, and module ownership aligned with existing imports and AI insight endpoints while avoiding an unapproved automation module or `/automation` prefix.

**Alternatives considered**:

- Add `/api/v1/automation`: rejected because it implies a new backend module and generic ownership.
- Hide schedule APIs and rely only on worker configuration: rejected because the spec requires backend automation APIs and run history.
- Use a single mixed schedule endpoint under imports or AI insights: rejected because it would give one module ownership over the other module's business behavior.
