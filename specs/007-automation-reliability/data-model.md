# Data Model: Automation & Reliability

Phase 6 adds schedule and schedule-run persistence around existing import and AI analysis execution records. Source tracking records, imported tasks, AI analysis outputs, and Phase 5 insight results remain authoritative in their existing modules and are not mutated by schedule evaluation.

## Shared Concepts

### Automation Type

**Purpose**: Identify the kind of scheduled work.

**Values**:

- `scheduled_import`
- `scheduled_ai_analysis`

**Validation Rules**:

- Import automation is owned by the `imports` module.
- AI analysis automation is owned by the `ai_insights` module.
- A schedule may have exactly one automation type.

### Schedule Cadence

**Purpose**: Define how often a schedule is evaluated.

**Values**:

- `daily`
- `weekly`

**Validation Rules**:

- Daily schedules resolve one local calendar-day due window.
- Weekly schedules resolve one Monday-to-Sunday week due window.
- Month and custom cadence schedules are outside Phase 6.

### Schedule State

**Purpose**: Represent whether a schedule participates in due-window evaluation.

**Values**:

- `active`
- `paused`
- `deleted`

**Validation Rules**:

- Only `active` schedules are evaluated for due windows.
- `paused` schedules preserve configuration and history but do not start future windows.
- `deleted` schedules are excluded from normal active schedule queries and evaluation while preserving history and audit records.

### Schedule Run Outcome

**Purpose**: Add schedule-specific outcome semantics while preserving shared run statuses.

**Values**:

- `started`: Downstream import or AI analysis work was started.
- `completed`: Scheduled work completed successfully.
- `completed_with_errors`: Work completed with partial row or processing issues.
- `failed`: Work reached a terminal failure.
- `skipped`: Window was skipped intentionally, such as older missed windows after downtime.
- `no_new_data`: Scheduled import found no new eligible CSV input.
- `no_data`: Scheduled AI analysis target period had no saved tracking records.

**Validation Rules**:

- The persisted status uses the shared vocabulary `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`.
- `skipped`, `no_new_data`, and `no_data` are stored as schedule-run outcomes, not new shared statuses.
- No skipped or no-data outcome may fabricate imported records, AI observations, or Phase 5 insight results.

## ImportAutomationSchedule

**Purpose**: User-owned schedule for CSV import automation.

**Planned Location**: `backend/app/modules/imports/models.py`

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference from authentication context.
- `state`: `active`, `paused`, or `deleted`.
- `cadence`: `daily` or `weekly`.
- `local_run_time`: time-of-day string or time value in the user's local timezone.
- `timezone`: IANA timezone identifier used to resolve due windows.
- `source_reference`: JSON object describing the configured CSV source reference without storing raw CSV contents.
- `source_name`: display-safe source label.
- `target_window_rule`: rule for selecting newly available CSV input for each due window.
- `next_run_at`: timestamp for the next due evaluation.
- `last_run_at`: nullable timestamp of the latest evaluated window.
- `last_run_outcome`: nullable schedule-run outcome.
- `failure_summary`: nullable latest failure summary.
- `created_by`: UUID actor that created the schedule.
- `updated_by`: nullable UUID actor for the latest user change.
- `deleted_at`: nullable soft-delete timestamp.
- `created_at`: timestamp.
- `updated_at`: timestamp.

**Relationships**:

- Has many `ImportAutomationRun` history records.
- May link created work to existing `ImportRun` records.
- Does not store full raw CSV contents.

**Validation Rules**:

- Owner is required and derived from authentication context.
- `source_reference` must identify a CSV source reference that satisfies the Phase 2 CSV contract.
- Active schedules require `cadence`, `local_run_time`, `timezone`, and `source_reference`.
- Deleted schedules are excluded from normal active queries and due evaluation.

## ImportAutomationRun

**Purpose**: Reviewable history for one scheduled import window.

**Planned Location**: `backend/app/modules/imports/models.py`

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `schedule_id`: UUID reference to `ImportAutomationSchedule`.
- `due_window_start`: timestamp or local date boundary.
- `due_window_end`: timestamp or local date boundary.
- `due_at`: timestamp that triggered evaluation.
- `status`: shared run status.
- `outcome`: schedule-run outcome.
- `import_run_id`: nullable UUID reference to the `ImportRun` created for actual import processing.
- `source_fingerprint`: nullable stable source-window identifier for newly available CSV input.
- `idempotency_key`: stable deduplication key derived from owner, schedule, automation type, due window, and source fingerprint.
- `attempt_count`: integer from 0 to 3.
- `max_attempts`: integer, default 3.
- `failure_classification`: nullable `retryable`, `non_retryable`, or `exhausted`.
- `failure_reason`: nullable user-actionable failure summary.
- `failure_details`: nullable structured failure detail.
- `processed_row_count`: non-negative integer summary copied from linked `ImportRun` when available.
- `inserted_row_count`: non-negative integer summary copied from linked `ImportRun` when available.
- `invalid_row_count`: non-negative integer summary copied from linked `ImportRun` when available.
- `skipped_row_count`: non-negative integer summary copied from linked `ImportRun` when available.
- `failed_row_count`: non-negative integer summary copied from linked `ImportRun` when available.
- `request_id`: nullable request or scheduler correlation identifier.
- `started_at`: nullable timestamp.
- `completed_at`: nullable timestamp.
- `diagnostic_prunable_after`: timestamp at least 90 days after creation.
- `diagnostic_pruned_at`: nullable timestamp.
- `final_summary`: JSON summary retained after diagnostic pruning.
- `created_at`: timestamp.
- `updated_at`: timestamp.

**Relationships**:

- Belongs to one `ImportAutomationSchedule`.
- Optionally links to one `ImportRun`.
- Does not replace `ImportRun` or `ImportRowOutcome`; it summarizes schedule-level execution.

**Validation Rules**:

- Unique active run per owner + schedule + due window + source fingerprint.
- Retry attempts for the same due window reuse the same `ImportAutomationRun`.
- Linked import processing must remain idempotent and must not insert duplicate tasks.
- Diagnostic details remain reviewable for at least 90 days.

## AIAnalysisAutomationSchedule

**Purpose**: User-owned schedule for daily or weekly Phase 4 AI analysis automation.

**Planned Location**: `backend/app/modules/ai_insights/models.py`

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference from authentication context.
- `state`: `active`, `paused`, or `deleted`.
- `target_period_type`: `daily` or `weekly`.
- `cadence`: `daily` or `weekly`.
- `local_run_time`: time-of-day string or time value in the user's local timezone.
- `timezone`: IANA timezone identifier used to resolve completed periods.
- `period_rule`: `previous_day` for daily schedules or `last_completed_week` for weekly schedules.
- `next_run_at`: timestamp for the next due evaluation.
- `last_run_at`: nullable timestamp of latest evaluated window.
- `last_run_outcome`: nullable schedule-run outcome.
- `failure_summary`: nullable latest failure summary.
- `created_by`: UUID actor that created the schedule.
- `updated_by`: nullable UUID actor for latest user change.
- `deleted_at`: nullable soft-delete timestamp.
- `created_at`: timestamp.
- `updated_at`: timestamp.

**Relationships**:

- Has many `AIAnalysisAutomationRun` history records.
- May link created work to existing `AIInsightRun` records.

**Validation Rules**:

- `target_period_type` must be `daily` or `weekly`.
- Daily schedules target completed prior local calendar days.
- Weekly schedules target completed Monday-to-Sunday weeks.
- Future or incomplete periods must be skipped or deferred, not partially analyzed.
- Deleted schedules are excluded from normal active queries and due evaluation.

## AIAnalysisAutomationRun

**Purpose**: Reviewable history for one scheduled AI analysis window.

**Planned Location**: `backend/app/modules/ai_insights/models.py`

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `schedule_id`: UUID reference to `AIAnalysisAutomationSchedule`.
- `target_period_type`: `daily` or `weekly`.
- `period_start`: date.
- `period_end`: date.
- `due_at`: timestamp that triggered evaluation.
- `status`: shared run status.
- `outcome`: schedule-run outcome.
- `ai_insight_run_id`: nullable UUID reference to the Phase 4 `AIInsightRun`.
- `idempotency_key`: stable deduplication key derived from owner, schedule, automation type, target period, and due time.
- `attempt_count`: integer from 0 to 3.
- `max_attempts`: integer, default 3.
- `failure_classification`: nullable `retryable`, `non_retryable`, or `exhausted`.
- `failure_reason`: nullable user-actionable failure summary.
- `failure_details`: nullable structured failure detail.
- `output_outcome`: nullable output outcome copied from linked `AIInsightRun`, such as `analysis_generated` or `no_data`.
- `request_id`: nullable request or scheduler correlation identifier.
- `started_at`: nullable timestamp.
- `completed_at`: nullable timestamp.
- `diagnostic_prunable_after`: timestamp at least 90 days after creation.
- `diagnostic_pruned_at`: nullable timestamp.
- `final_summary`: JSON summary retained after diagnostic pruning.
- `created_at`: timestamp.
- `updated_at`: timestamp.

**Relationships**:

- Belongs to one `AIAnalysisAutomationSchedule`.
- Optionally links to one `AIInsightRun`.
- Does not create or mutate `AIInsightResult` records.

**Validation Rules**:

- Unique active run per owner + schedule + target period + due time.
- Retry attempts for the same target period reuse the same `AIAnalysisAutomationRun`.
- If a current or in-flight `AIInsightRun` already exists for the owner + period + granularity, the automation run reuses or skips according to existing AI idempotency rules.
- Scheduled AI analysis excludes note text and does not automatically generate Phase 5 insight results.
- Diagnostic details remain reviewable for at least 90 days.

## Schedule Window

**Purpose**: Derived value object used by workers and services to decide due work.

**Fields**:

- `schedule_id`: UUID.
- `automation_type`: `scheduled_import` or `scheduled_ai_analysis`.
- `due_at`: timestamp.
- `window_start`: date or timestamp.
- `window_end`: date or timestamp.
- `is_latest_missed_window`: boolean.
- `missed_window_count`: non-negative integer.
- `idempotency_key`: stable deduplication key.

**Validation Rules**:

- Due windows are resolved from schedule timezone and local run time.
- After downtime, only the latest missed due window is processed.
- Older missed windows are written as skipped history entries.

## Retry Attempt

**Purpose**: Bounded recovery attempt for scheduled work.

**Fields**:

- `attempt_number`: integer from 1 to 3.
- `started_at`: timestamp.
- `completed_at`: nullable timestamp.
- `status`: shared run status.
- `failure_classification`: nullable classification.
- `failure_reason`: nullable summary.
- `failure_details`: nullable structured details.

**Validation Rules**:

- Retryable failures stop after no more than three total attempts.
- Non-retryable failures move directly to terminal failed outcome.
- Attempts must not create duplicate import tasks, imported tasks, or duplicate current AI results.

## Automation Audit Event

**Purpose**: Durable trace for schedule changes and scheduled execution outcomes.

**Fields**:

- `actor_type`: `user` or `scheduler`.
- `actor_id`: nullable UUID for user actors.
- `owner_id`: UUID owner/workspace reference.
- `automation_type`: schedule type.
- `schedule_id`: UUID.
- `run_id`: nullable UUID of schedule-run history.
- `action`: create, update, pause, resume, delete, trigger, evaluate, retry, complete, fail, skip, or prune.
- `requested_change`: nullable structured change details.
- `resulting_status`: nullable shared run status or schedule state.
- `failure_details`: nullable structured failure details.
- `request_id`: nullable request or scheduler correlation identifier.
- `created_at`: timestamp.

**Validation Rules**:

- Schedule mutations and terminal run outcomes require audit events.
- Audit events must not contain raw CSV contents or note text.
- Audit details remain reviewable for 90 days; final summaries remain after diagnostic pruning.

## State Transitions

### Schedule

```text
active -> paused
paused -> active
active -> deleted
paused -> deleted
deleted -> active is not supported in Phase 6
```

### Schedule Run

```text
pending -> processing -> completed
pending -> processing -> completed_with_errors
pending -> processing -> failed
pending -> completed       # skipped, missed, no_new_data, or no_data outcome
failed -> processing        # retry while attempts remain
```

## Retention and Pruning

- Detailed automation run history and audit details must remain reviewable for 90 days.
- After 90 days, non-current diagnostic detail may be pruned.
- `final_summary` must remain available after pruning.
- Soft-deleted schedules keep schedule identity and history links for audit.
