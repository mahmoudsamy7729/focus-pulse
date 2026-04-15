# Data Model: Core Domain & Data Model

Phase 1 creates persistent backend domain models for daily tracking data and traceability. Main entities use UUID primary keys, `created_at`, `updated_at`, and `deleted_at` where traceability or user ownership makes soft delete relevant.

## Shared Concepts

### Owner and Audit Fields

**Purpose**: Keep v1 personal data future-safe for auth and multi-user ownership without implementing auth in Phase 1.

**Fields**:

- `owner_id`: UUID identifying the user/workspace owner. Required on user-owned and operational records.
- `created_at`: timestamp when the record was created.
- `updated_at`: timestamp when the record was last updated.
- `deleted_at`: nullable timestamp for soft-deleted records where deletion could affect traceability.

**Validation Rules**:

- Normal user-facing reads exclude records where `deleted_at` is set.
- Traceability reads may include soft-deleted records when needed for import or AI audit review.
- Hard deletion is out of scope except for transient implementation artifacts not modeled here.

### RunStatus

**Purpose**: Shared lifecycle vocabulary for import and AI analysis attempts.

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
- Terminal states may be superseded by a new separate rerun record; existing run records are not overwritten into a new attempt.

## DailyLog

**Purpose**: The record for one tracked calendar date. It groups all tasks performed on that date and anchors day-level summaries and future analysis.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `log_date`: calendar date.
- `source`: source label such as manual, csv_import, or system.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Has many `Task` records.
- May be referenced by many `AIInsightRunSource` records.
- May be created or updated through an `ImportRun`.

**Validation Rules**:

- Unique active DailyLog per `owner_id` plus `log_date`.
- New data targeting an existing active `DailyLog` date reuses that `DailyLog`.
- Soft-deleted logs are excluded from normal reads and calculations.

## Task

**Purpose**: A unit of tracked work within one DailyLog.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `daily_log_id`: required UUID reference to `DailyLog`.
- `category_id`: required UUID reference to `Category`.
- `title`: original task name for display and audit review.
- `normalized_title`: lowercase trimmed task name used for deduplication.
- `time_spent_minutes`: positive whole-number duration.
- `tags`: JSON array of normalized unique strings.
- `source`: source label such as manual or csv_import.
- `import_run_id`: nullable UUID reference to the `ImportRun` that created the task.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Belongs to one `DailyLog`.
- Belongs to one `Category`.
- May have one `Note`.
- May reference the `ImportRun` that created it.

**Validation Rules**:

- Must have a non-empty title and normalized title.
- `time_spent_minutes` must be a positive whole number.
- `tags` must be a JSON array; missing tags become `[]`.
- Tag normalization trims whitespace, lowercases text, removes empty values, and removes duplicates.
- Imported duplicate identity is `daily_log.log_date` + `normalized_title` + `time_spent_minutes`.
- Duplicate imported rows do not create a new task; they are recorded as skipped row outcomes.

## Category

**Purpose**: A normalized reusable classification for tasks.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `name`: canonical display name.
- `normalized_name`: lowercase trimmed category name used for uniqueness.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Has many `Task` records.

**Validation Rules**:

- Unique active category per `owner_id` plus `normalized_name`.
- Category names differing only by capitalization or surrounding spaces resolve to the same active category.
- A category referenced by active tasks cannot be hard-deleted.

## Tag

**Purpose**: A task-level label value used for flexible grouping.

**Representation**:

- Tags are not stored as normalized rows in Phase 1.
- Tags are normalized string values stored in `Task.tags` as a JSON array.

**Validation Rules**:

- Empty or missing tag input becomes `[]`.
- Repeated normalized values appear only once per task.
- Tags are lowercased and trimmed before storage.

## Note

**Purpose**: Optional task-level free-text context.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `task_id`: required UUID reference to `Task`.
- `content`: non-empty note text.
- `import_run_id`: nullable UUID reference to the `ImportRun` that created the note.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Belongs to one `Task`.
- May reference the `ImportRun` that created it.

**Validation Rules**:

- Empty note input is treated as no note and does not create a Note record.
- At most one active Note belongs to one Task in Phase 1.
- Notes remain task-level; day-level notes are out of scope unless a later phase adds them.

## ImportRun

**Purpose**: A traceable import attempt used by later CSV processing and retry behavior.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference.
- `source_type`: import source type, initially csv.
- `source_name`: source identifier such as filename or upload label.
- `status`: `RunStatus`.
- `started_at`: nullable processing start timestamp.
- `completed_at`: nullable processing completion timestamp.
- `processed_row_count`: whole-number count.
- `inserted_row_count`: whole-number count.
- `invalid_row_count`: whole-number count.
- `skipped_row_count`: whole-number count.
- `failed_row_count`: whole-number count.
- `failure_reason`: nullable summary for full-run failure.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Has many created `Task` records.
- Has many created `Note` records.
- Has many `ImportRowOutcome` records for invalid, skipped, and failed rows.

**Validation Rules**:

- Status must be one of the shared `RunStatus` values.
- Row counts must be non-negative whole numbers.
- `processed_row_count` should equal inserted + invalid + skipped + failed counts after a terminal status.
- A failed run must include failure details.
- ImportRun records are audit-sensitive and use soft delete only.

## ImportRowOutcome

**Purpose**: Row-level traceability for import rows that were not inserted as completed task data.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference.
- `import_run_id`: required UUID reference to `ImportRun`.
- `row_number`: source row reference when available.
- `outcome_type`: invalid, skipped, or failed.
- `reason`: concise explanation for the outcome.
- `normalized_task_name`: nullable normalized task name when available.
- `log_date`: nullable date when available.
- `time_spent_minutes`: nullable duration when available.
- `row_snapshot`: nullable structured row summary sufficient for audit review without requiring full raw-file storage.
- `created_at`: creation timestamp.

**Relationships**:

- Belongs to one `ImportRun`.

**Validation Rules**:

- Outcome type must be invalid, skipped, or failed.
- Skipped duplicate rows should include enough normalized identity data to connect the skip to the deduplication rule.
- Row outcomes are immutable audit details after the import run reaches a terminal status.

## AIInsightRun

**Purpose**: A traceable AI analysis attempt for daily or weekly productivity insights.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference.
- `target_period_type`: daily or weekly.
- `period_start`: date.
- `period_end`: date.
- `status`: `RunStatus`.
- `source_summary`: structured summary of source data used for the run.
- `output_summary`: nullable structured summary of generated insight output.
- `failure_reason`: nullable failure explanation.
- `started_at`: nullable processing start timestamp.
- `completed_at`: nullable processing completion timestamp.
- `created_at`: creation timestamp.
- `updated_at`: update timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Has many `AIInsightRunSource` records that reference source `DailyLog` records.
- Does not own or mutate DailyLog, Task, Category, Tag, Note, or ImportRun records.

**Validation Rules**:

- Target period type must be `daily` or `weekly` for v1.
- Daily runs have the same `period_start` and `period_end`.
- Weekly runs cover a seven-day date range.
- Status must be one of the shared `RunStatus` values.
- Reruns create new AIInsightRun records rather than overwriting previous runs.

## AIInsightRunSource

**Purpose**: Join record that preserves which DailyLogs were used by an AIInsightRun.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `ai_insight_run_id`: required UUID reference to `AIInsightRun`.
- `daily_log_id`: required UUID reference to `DailyLog`.
- `created_at`: creation timestamp.

**Relationships**:

- Belongs to one `AIInsightRun`.
- References one `DailyLog`.

**Validation Rules**:

- Source links are immutable after a run reaches a terminal status.
- Soft-deleting a DailyLog must not erase historical AIInsightRunSource traceability.

## Query and Calculation Requirements

- Daily logs can be read by exact date and date range with active tasks, categories, tags, and notes.
- Time totals can be calculated by day, category, and tag from active tasks.
- Normal user-facing reads exclude soft-deleted source records.
- Traceability reads can include soft-deleted records when reviewing ImportRun or AIInsightRun history.
