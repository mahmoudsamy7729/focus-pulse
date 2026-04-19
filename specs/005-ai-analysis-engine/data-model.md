# Data Model: AI Analysis Engine

Phase 4 extends the existing Phase 1 `AIInsightRun` and `AIInsightRunSource` traceability model to support executable daily and weekly AI analysis runs. Source productivity records remain authoritative and are never mutated by AI output.

## Shared Concepts

### Period Granularity

**Purpose**: Identify the target period shape for a combined analysis run.

**Values**:

- `daily`
- `weekly`

**Validation Rules**:

- `daily` runs use identical `period_start` and `period_end`.
- `weekly` runs cover exactly seven local calendar days.
- Monthly, custom range, scheduled, and chat-triggered analysis are outside Phase 4.

### RunStatus

**Purpose**: Reuse the shared lifecycle vocabulary from Phase 1.

**Values**:

- `pending`
- `processing`
- `completed`
- `completed_with_errors`
- `failed`

**State Transitions**:

- `pending` -> `processing`
- `processing` -> `completed`
- `processing` -> `completed_with_errors`
- `processing` -> `failed`
- Terminal states are not overwritten by reruns; reruns create separate `AIInsightRun` records.

### Output Outcome

**Purpose**: Classify completed outputs without changing the shared run status vocabulary.

**Values**:

- `analysis_generated`: Analysis content was generated and validated.
- `no_data`: The selected period had no saved tracking records and no analysis claims were generated.

**Validation Rules**:

- `no_data` outputs use run status `completed`.
- `analysis_generated` outputs use run status `completed` unless non-fatal source-level limitations require `completed_with_errors`.
- Failed provider calls, malformed output, and exhausted retries use status `failed`, not an output outcome.

## AI Analysis Request

**Purpose**: A user request to run combined analysis for one day or one week.

**Fields**:

- `owner_id`: UUID actor/workspace reference from authentication context.
- `period_granularity`: `daily` or `weekly`.
- `anchor_date`: requested calendar date used to resolve the target period.
- `request_id`: optional request correlation identifier.
- `idempotency_key`: optional client-provided duplicate submission key.

**Validation Rules**:

- Owner is required and derived from the authenticated user context.
- Anchor date must resolve to a valid daily or Monday-to-Sunday weekly period.
- Request does not include note text or arbitrary prompt text.
- Duplicate owner + period + period granularity + idempotency key returns the existing run.
- A second in-flight request for the same owner + period + period granularity without the same idempotency key is a conflict.

## AIInsightRun

**Purpose**: Durable trace for one combined AI analysis attempt.

**Existing Fields Reused**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference.
- `target_period_type`: `daily` or `weekly`.
- `period_start`: date.
- `period_end`: date.
- `status`: shared `RunStatus`.
- `source_summary`: retained aggregate input summary.
- `output_summary`: completed generated output or no-data output.
- `failure_reason`: final failure summary.
- `started_at`: processing start timestamp.
- `completed_at`: processing completion timestamp.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Phase 4 Planned Fields**:

- `instruction_name`: name of the combined instruction template, such as `daily_combined_analysis` or `weekly_combined_analysis`.
- `instruction_version`: version string for the prompt/instruction set used.
- `output_outcome`: nullable output outcome, `analysis_generated` or `no_data`, set for completed runs.
- `retry_count`: non-negative integer count of completed retry attempts after the first attempt.
- `max_attempts`: positive integer, default 3.
- `idempotency_key`: nullable client duplicate-submission key.
- `request_id`: nullable request correlation identifier.
- `last_failure_stage`: nullable stage label for the latest failed attempt.
- `failure_details`: nullable structured details for final failure and attempt history.

**Relationships**:

- Has many `AIInsightRunSource` records referencing source `DailyLog` records.
- Does not own or mutate `DailyLog`, `Task`, `Category`, `Tag`, `Note`, `ImportRun`, or `ImportRowOutcome` records.

**Validation Rules**:

- Status must be one of the shared `RunStatus` values.
- `retry_count` must be between 0 and `max_attempts - 1`.
- `max_attempts` is 3 for Phase 4.
- `failed` terminal runs require `failure_reason`.
- `completed` runs require `output_summary` and `output_outcome`.
- `no_data` completed runs must not include generated summary, pattern, or behavior-insight claims.
- Generated outputs must pass output validation before status becomes `completed`.
- Reruns create new `AIInsightRun` records and preserve earlier run history.
- Normal reads exclude soft-deleted AI runs; audit reads may include them.

## AIInsightRunSource

**Purpose**: Preserve source `DailyLog` references used by a run.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `ai_insight_run_id`: required UUID reference to `AIInsightRun`.
- `daily_log_id`: required UUID reference to `DailyLog`.
- `created_at`: creation timestamp.

**Validation Rules**:

- Source links are immutable after the run reaches a terminal status.
- Source links are retained even if the source `DailyLog` is soft-deleted later.
- No note text is copied into source links.

## Analysis Input Summary

**Purpose**: Retained audit summary of what was analyzed without retaining the full structured AI input payload.

**Fields**:

- `period_granularity`: `daily` or `weekly`.
- `period_start`: date.
- `period_end`: date.
- `source_daily_log_ids`: list of source DailyLog UUIDs.
- `daily_log_count`: non-negative integer.
- `task_count`: non-negative integer.
- `total_minutes`: non-negative integer.
- `category_totals`: list of category labels with total minutes.
- `tag_totals`: list of tag labels with total minutes.
- `daily_totals`: list of dates with total minutes for weekly runs.
- `included_fields`: list containing task names, durations, categories, and tags.
- `excluded_fields`: list containing note text.

**Validation Rules**:

- Must not contain note text.
- Must not retain the full structured AI input payload sent to the provider.
- Must include enough aggregate evidence to audit why a completed output was produced.

## Structured AI Input

**Purpose**: Ephemeral provider input used during execution.

**Fields**:

- `period`: resolved daily or weekly period.
- `tasks`: task name, duration, category, and tags for active saved records.
- `aggregates`: total minutes, task count, category totals, tag totals, and daily totals for weekly runs.
- `instruction_name`: selected instruction name.
- `instruction_version`: selected instruction version.

**Lifecycle Rules**:

- Created during processing only.
- Excludes note text.
- Not retained after the run records source references and aggregate input summary.

## Analysis Instruction Version

**Purpose**: Identify the prompt/instruction set used for a run.

**Fields**:

- `instruction_name`: `daily_combined_analysis` or `weekly_combined_analysis`.
- `instruction_version`: stable version string.
- `required_output_sections`: summary, detected patterns, behavior insights, supporting evidence, limitations, generated timestamp, and output outcome.

**Validation Rules**:

- Every run records instruction name and version before processing starts.
- Output validation uses the required section list for the recorded instruction version.

## Combined Analysis Output

**Purpose**: Stored result for a completed daily or weekly run.

**Fields**:

- `output_outcome`: `analysis_generated` or `no_data`.
- `summary`: nullable narrative summary. Required for `analysis_generated`, absent for `no_data`.
- `detected_patterns`: list of detected pattern objects.
- `behavior_insights`: list of behavior insight objects.
- `supporting_evidence`: list of evidence references.
- `limitations`: list of limitations or caveats.
- `generated_at`: timestamp when output was generated.

**Validation Rules**:

- `analysis_generated` output must include summary, generated timestamp, and the required section keys even when a list is empty.
- Each detected pattern or behavior insight must reference supporting evidence from the selected period.
- Unsupported claims are omitted or represented as limitations.
- Output must not include note text.
- Malformed or incomplete output cannot complete a run successfully.

## Supporting Evidence

**Purpose**: Tie generated observations to source facts without copying note text.

**Fields**:

- `evidence_id`: stable local identifier within the output.
- `evidence_type`: date total, category total, tag total, task count, task reference, or duration outlier.
- `source_date`: nullable date.
- `source_task_id`: nullable Task UUID.
- `label`: category, tag, or task label when applicable.
- `minutes`: nullable tracked duration.
- `count`: nullable count.

**Validation Rules**:

- Evidence may reference task IDs and task names but not note text.
- Evidence must belong to the run period.

## Run Failure Detail

**Purpose**: Explain failed attempts and final failure states.

**Fields**:

- `stage`: input preparation, provider_call, output_validation, persistence, or worker_execution.
- `reason`: concise failure reason.
- `attempt_number`: integer from 1 to 3.
- `transient`: boolean.
- `occurred_at`: timestamp.

**Validation Rules**:

- Final failed runs require a failure reason and at least one failure detail.
- Attempt numbers must not exceed 3.
- Retryable transient failures may be retried until the max attempt count is reached.

## Current Analysis Result

**Purpose**: The latest successful completed result for an owner, period, and period granularity.

**Selection Rules**:

- Include only active runs where status is `completed` and output outcome is `analysis_generated` or `no_data`.
- Select the most recent by completion time, with created time as a stable fallback.
- Exclude soft-deleted runs.
- Failed and processing runs are available in history but are not current results.

## Query Requirements

- List AI runs by owner with optional period granularity, status, date range, page, and limit filters.
- Get one AI run by owner and run ID, including output summary and failure details.
- Get current result by owner, period granularity, and anchor date.
- Find duplicate idempotency key for owner + period granularity + period.
- Find in-flight run for owner + period granularity + period.
- Fetch active saved source records for daily or weekly input preparation without note text.
