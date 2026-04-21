# Feature Specification: Automation & Reliability

**Feature Branch**: `007-automation-reliability`  
**Created**: 2026-04-21  
**Status**: Draft  
**Input**: User description: "Use the existing constitution generated from STACK_AND_STRUCTURE.md as the primary source of rules and constraints. Use Plan.md in docs folder only as a reference for scope and intended behavior. Create a feature specification for Phase 6 - Automation & Reliability."

## Clarifications

### Session 2026-04-21

- Q: What source may scheduled imports consume in Phase 6? -> A: Scheduled imports use a user-configured CSV source reference; each run consumes only newly available CSV input and retains metadata/outcomes only.
- Q: What frontend or UI scope is included in Phase 6 automation management? -> A: Backend automation APIs and run history only; no new frontend schedule-management UI in Phase 6.
- Q: Should scheduled AI analysis automatically generate Phase 5 insight results? -> A: Scheduled AI analysis only; Phase 5 insight/result generation remains explicit or future automation.
- Q: How should automation handle missed schedule windows after downtime? -> A: On restart, process only the latest missed due window per active schedule; mark older missed windows as skipped.
- Q: How long should automation run history and audit details be retained? -> A: Keep automation run history and audit details for 90 days, then allow pruning of non-current diagnostic detail while preserving final summaries.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Scheduled Imports Reliably (Priority: P1)

As the project owner, I want supported import work to run on a schedule, so my tracking data can stay current without manually starting every eligible import attempt.

**Why this priority**: Scheduled imports are the first Phase 6 automation item and directly support stable daily usage. The system must preserve the Phase 2 import quality rules while adding scheduling and recovery.

**Independent Test**: Can be tested by enabling a daily import schedule for a supported import source, reaching the scheduled time, and verifying that exactly one traceable import run is created, processed, retried if needed, and reviewable later.

**Acceptance Scenarios**:

1. **Given** an active import schedule has an eligible supported import source and reaches its next run time, **When** the scheduler evaluates due work, **Then** the system creates one traceable import run for that schedule window.
2. **Given** a scheduled import source has no new eligible input for the schedule window, **When** the schedule runs, **Then** the system records a skipped or no-new-data outcome instead of creating misleading imported records.
3. **Given** a scheduled import contains valid, invalid, duplicate, or failed rows, **When** processing completes, **Then** the import history preserves the same row-count, row-outcome, deduplication, and raw-file non-retention guarantees as manual imports.
4. **Given** an import schedule is paused or disabled before its next run time, **When** the scheduler evaluates due work, **Then** no new import run is started for that disabled schedule.

---

### User Story 2 - Run Scheduled AI Analysis (Priority: P2)

As the project owner, I want daily and weekly AI analysis to run automatically for completed tracking periods, so summaries and patterns are ready without manual request timing.

**Why this priority**: Scheduled AI runs turn the Phase 4 analysis engine into a dependable daily habit while keeping AI behavior isolated and traceable.

**Independent Test**: Can be tested by enabling scheduled daily and weekly analysis, creating saved tracking records for the target periods, and verifying that completed, no-data, failed, and retried runs are recorded without duplicate current results.

**Acceptance Scenarios**:

1. **Given** an active daily analysis schedule and saved records for the prior calendar day, **When** the scheduled time arrives, **Then** the system creates one traceable daily AI analysis run for that completed day.
2. **Given** an active weekly analysis schedule and a completed Monday-to-Sunday week, **When** the weekly schedule runs, **Then** the system creates one traceable weekly AI analysis run for that completed week.
3. **Given** the target period has no saved tracking records, **When** a scheduled analysis runs, **Then** the system records a completed no-data outcome without generating fabricated observations.
4. **Given** a current analysis run already exists or is in progress for the same owner, period, and granularity, **When** the schedule evaluates the same period, **Then** the system reuses or skips according to idempotency rules instead of creating duplicate current results.

---

### User Story 3 - Recover and Diagnose Background Work (Priority: P3)

As the project owner or maintainer, I want scheduled jobs, retries, failures, and logs to be traceable, so failures can be recovered or understood without corrupting tracking data or AI history.

**Why this priority**: Phase 6 is about production readiness. Automation is useful only when failures are bounded, observable, and recoverable.

**Independent Test**: Can be tested by forcing transient and permanent failures in scheduled imports and scheduled AI analysis, then verifying retry limits, terminal statuses, audit details, and correlated logs.

**Acceptance Scenarios**:

1. **Given** scheduled work fails because of a transient condition, **When** retry rules allow another attempt, **Then** the system retries the same work without creating duplicate imported records or duplicate current AI results.
2. **Given** scheduled work fails repeatedly until the retry limit is reached, **When** the final attempt fails, **Then** the run is marked failed with the final reason, attempt count, latest stage, and recovery guidance.
3. **Given** scheduled work fails because of invalid user data or unsupported input, **When** the failure is classified, **Then** the system avoids pointless automatic retries and records a user-actionable failure.
4. **Given** a maintainer investigates a failed scheduled run, **When** they review run history and logs, **Then** they can correlate schedule, run, attempt, owner, target period, status transition, and failure details.

### Edge Cases

- If a schedule is due more than once because the scheduler was offline, the system must process only the latest missed due window per active schedule and mark older missed windows as skipped.
- If two scheduler evaluations happen at nearly the same time, the same schedule window must not create duplicate import runs or duplicate AI analysis runs.
- If a scheduled import retry reprocesses rows that were partially inserted in a previous attempt, retry processing must not create duplicate tasks.
- If a scheduled import source becomes unavailable, unreadable, or unsupported, the scheduled run must fail with traceable details and avoid retaining raw CSV contents.
- If scheduled import input violates the existing CSV contract, the run must preserve row-level validation outcomes and avoid inserting invalid rows.
- If scheduled AI analysis is requested for a future or incomplete period, the schedule must skip or defer the run instead of generating partial-period analysis.
- If source tracking records change after a scheduled AI run, the older run must remain historical and a later eligible run or explicit rerun must be traceable separately.
- If a user disables a schedule while work is already processing, in-flight work may finish, but no later schedule windows should start until the schedule is re-enabled.
- If a user deletes an automation schedule, deletion must preserve prior run history needed for audit and troubleshooting.
- If logs or audit records are reviewed later, they must not expose raw CSV file contents or note text that earlier phases excluded from retained inputs.
- If recurring scheduled work repeatedly fails, the system must avoid infinite retry loops and make the latest failure visible.
- If a rate limit or permission failure occurs while managing automation, the system must return a stable error outcome without changing the schedule.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the project owner to create, view, pause, resume, and delete automation schedules for supported scheduled import work and scheduled AI analysis work.
- **FR-002**: Each automation schedule MUST define an owner, automation type, active state, cadence, user-local run time, target period rule, next run time, last run outcome, and failure summary when applicable.
- **FR-003**: The system MUST support daily and weekly schedule cadences for Phase 6 automation.
- **FR-004**: Scheduled imports MUST use a user-configured CSV source reference that satisfies the existing CSV import contract; each run MUST consume only newly available CSV input and MUST NOT introduce Notion API synchronization or arbitrary external connectors in this phase.
- **FR-005**: Scheduled imports MUST preserve existing import validation, normalization, deduplication, row-outcome, status-history, and raw CSV non-retention behavior.
- **FR-006**: If no eligible import input exists for a scheduled window, the system MUST record a skipped or no-new-data outcome with the reason.
- **FR-007**: Scheduled AI analysis MUST support the same day and Monday-to-Sunday week period boundaries already used by analysis and insight features.
- **FR-008**: Scheduled AI analysis MUST use saved tracking records as the source of truth and MUST preserve the existing AI privacy boundary by excluding note text from retained inputs and outputs.
- **FR-009**: Scheduled AI analysis MUST create traceable AI analysis runs with status, source period, source summary, instruction version, retry count, output outcome, and failure details when applicable.
- **FR-010**: Scheduled automation MUST be idempotent for the same owner, schedule, automation type, target period or source window, and due time.
- **FR-010a**: When downtime causes multiple missed due windows for an active schedule, the system MUST process only the latest missed due window and MUST record older missed windows as skipped.
- **FR-011**: Retrying scheduled import work MUST NOT create duplicate tasks, duplicate import row outcomes for the same attempt, or misleading row counts.
- **FR-012**: Retrying scheduled AI analysis work MUST NOT create duplicate current AI analysis results for the same owner, period, and granularity.
- **FR-013**: The system MUST classify scheduled-work failures as retryable or non-retryable before retrying.
- **FR-014**: Retryable scheduled-work failures MUST stop after no more than three total attempts for a run unless a later approved spec changes the bounded retry policy.
- **FR-015**: Non-retryable scheduled-work failures MUST move directly to a terminal failed outcome with user-actionable details.
- **FR-016**: Scheduled work MUST use the shared run status vocabulary `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`; skipped or no-new-data outcomes MUST be represented without fabricating successful imported data or AI observations.
- **FR-017**: The system MUST preserve a reviewable history of automation schedule evaluations, started runs, skipped windows, retries, terminal outcomes, and failure details.
- **FR-018**: The system MUST make automation history filterable by automation type, status, schedule, and time period.
- **FR-019**: Automation history list behavior MUST define consistent pagination using `page` and `limit`.
- **FR-019a**: Automation run history and audit details MUST remain reviewable for at least 90 days; after 90 days, non-current diagnostic detail may be pruned while final summaries remain available.
- **FR-020**: Protected automation operations MUST require explicit owner permission and must not allow one owner to view, change, or trigger another owner's schedules or run history.
- **FR-021**: Expensive or abuse-sensitive automation operations, including manual trigger, schedule creation, and repeated retry requests, MUST have rate-limit expectations.
- **FR-022**: Handled JSON responses for automation interfaces MUST use the standard success envelope, and handled errors MUST use the unified error shape with stable error codes.
- **FR-023**: Scheduled imports, scheduled AI runs, manual triggers, schedule changes, retry decisions, and terminal failures MUST write audit records with actor, timestamp, requested action or change, target schedule or run, resulting status, and failure details when applicable.
- **FR-024**: Application and background-work logs for scheduled automation MUST include enough correlation data to connect schedule evaluation, created run, retry attempt, status transition, and failure details.
- **FR-025**: Deleting an automation schedule MUST be a soft-delete-style operation that removes it from normal active schedule evaluation while preserving prior schedule and run history for audit.
- **FR-026**: Phase 6 MUST cover backend automation APIs, scheduled imports, scheduled AI analysis runs, retry/recovery behavior, logs, auditability, and automation status/history only; automatic Phase 5 insight generation, frontend schedule-management UI, report export, Notion API synchronization, AI chat, dashboard redesign, and new AI recommendation logic are outside this phase.

### Key Entities *(include if feature involves data)*

- **Automation Schedule**: A user-owned rule that defines what automation should run, when it should run, whether it is active, and how its latest outcome is summarized.
- **Schedule Window**: The specific due interval for a schedule, such as a daily import window or a completed calendar week targeted by weekly AI analysis.
- **Scheduled Import Run**: A traceable import run started by an automation schedule rather than by an immediate manual confirmation, using newly available CSV input from the schedule's configured source reference.
- **Scheduled AI Analysis Run**: A traceable AI analysis run started by an automation schedule for a completed day or week.
- **Automation Run History**: The reviewable record of schedule evaluations, created runs, skipped windows, retries, completions, partial completions, and failures, with detailed diagnostics retained for at least 90 days.
- **Retry Attempt**: A bounded attempt to recover the same scheduled work after a retryable failure, linked to the original scheduled run.
- **Failure Classification**: The decision that identifies whether a failure is retryable, non-retryable, user-actionable, or exhausted after retries.
- **Automation Audit Event**: A durable trace of schedule changes, scheduled execution, manual triggers, retry decisions, and terminal outcomes.
- **Operational Log Event**: A structured diagnostic event that correlates schedule evaluation, run execution, attempt count, status transition, and failure details.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of due active automation schedules produce exactly one started, skipped, or failed history entry for each evaluated schedule window, including older missed windows that are skipped after downtime.
- **SC-002**: Duplicate scheduler evaluations for the same schedule window create zero duplicate import runs and zero duplicate current AI analysis runs.
- **SC-003**: 100% of scheduled imports preserve Phase 2 validation, deduplication, row-outcome, and raw CSV non-retention guarantees.
- **SC-004**: 100% of scheduled AI analysis runs preserve Phase 4 source-data, no-data, retry, output validation, and note-text exclusion guarantees.
- **SC-005**: 100% of retryable scheduled-work failures stop after no more than three total attempts and preserve attempt history.
- **SC-006**: 100% of non-retryable scheduled-work failures reach a terminal failed outcome without repeated automatic retries.
- **SC-007**: A user can identify whether scheduled imports and scheduled AI analysis are active, paused, completed, skipped, or failed in under 2 minutes.
- **SC-008**: A maintainer can correlate a failed scheduled run from schedule to run to retry attempts to final failure details in under 10 minutes using retained history and logs.
- **SC-009**: At least 95% of scheduled daily automation over a 30-day test period completes or reaches a traceable skipped/failed terminal state within 10 minutes of its due time.
- **SC-010**: 100% of schedule changes and terminal scheduled-run outcomes include an audit event with actor, timestamp, target, requested action or change, resulting status, and failure details when applicable.
- **SC-010a**: 100% of automation run history and audit detail remains reviewable for 90 days, and 100% of pruned older records preserve final outcome summaries.
- **SC-011**: A reviewer can verify in under 10 minutes that Phase 6 does not add automatic Phase 5 insight generation, frontend schedule-management UI, report export, Notion API synchronization, AI chat, dashboard redesign, arbitrary external import connectors, raw CSV retention, or new AI recommendation logic.

## Assumptions

- Phase 1 domain records, Phase 2 manual CSV import behavior, Phase 4 AI analysis runs, and Phase 5 stored insight results exist before Phase 6 implementation begins.
- The v1 product remains a personal single-owner tracker unless a later phase introduces multi-user collaboration.
- Calendar days use the user's local tracked dates from source records.
- Weekly automation uses Monday-to-Sunday calendar weeks, consistent with prior dashboard, analysis, and insight phases.
- Scheduled imports automate only newly available CSV input from a user-configured source reference that already satisfies the approved CSV import contract; connector-specific synchronization, including Notion API synchronization, remains a future Phase 7 concern.
- Scheduled imports may record source metadata, run status, counts, and row outcomes, but they do not retain full raw CSV file contents.
- Scheduled AI analysis automates Phase 4 analysis execution for completed day and week periods; it does not automatically generate Phase 5 insight results and does not create AI chat behavior or new recommendation-generation logic.
- Phase 6 provides backend automation APIs and run history only; frontend schedule-management screens are deferred unless a later phase brings them into scope.
- Existing saved tracking records remain authoritative if they conflict with generated AI output, scheduled metadata, or operational logs.
- A bounded retry limit of three total attempts is used for scheduled work to match the existing AI run retry expectation and avoid infinite recovery loops.
- After scheduler downtime, only the latest missed due window for each active schedule is processed; older missed windows are recorded as skipped rather than backfilled.
- In-flight work may finish after a schedule is paused or deleted, but no future windows should start from an inactive schedule.
- Automation history and audit details are retained for at least 90 days for troubleshooting; after 90 days, non-current diagnostic detail may be pruned while final summaries remain available.
- Automation history and audit records are retained for troubleshooting even when a schedule is deleted from normal active use.
