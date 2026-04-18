# Data Model: CSV Import Pipeline

Phase 2 primarily adds import pipeline value objects and service contracts around the persistent Phase 1 entities. Existing tables for `DailyLog`, `Task`, `Category`, `Note`, `ImportRun`, and `ImportRowOutcome` remain the authoritative persistence model unless implementation needs a narrowly scoped migration for idempotency or indexing.

## CSV Import File

**Purpose**: User-submitted CSV content for preview or confirmed import.

**Fields**:

- `filename`: user-visible file name or upload label.
- `content_type`: uploaded file content type when available.
- `size_bytes`: uploaded file size when available.
- `raw_bytes`: transient request data used only during parsing and not retained after the request or worker handoff.

**Validation Rules**:

- Must be readable as CSV text.
- Must contain headers.
- Must include required columns after header normalization.
- Empty files are rejected.
- Full raw CSV contents are not retained in import history.

## CSV Header Contract

**Required Columns**:

- `date`
- `task`
- `category`
- `time_spent_minutes`

**Optional Columns**:

- `tags`
- `notes`

**Validation Rules**:

- Header matching is case-insensitive and ignores surrounding spaces.
- Missing required columns reject the file before row insertion.
- Extra columns are ignored unless included in an error row snapshot as non-sensitive context.

## ParsedImportRow

**Purpose**: One parsed CSV row before validation is complete.

**Fields**:

- `row_number`: source row number, with the header excluded from data-row counting.
- `raw_date`: original date cell.
- `raw_task`: original task cell.
- `raw_category`: original category cell.
- `raw_time_spent_minutes`: original duration cell.
- `raw_tags`: optional tags cell.
- `raw_notes`: optional notes cell.

**Relationships**:

- May become one `NormalizedImportRow`.
- May become one invalid `ImportRowOutcome` after confirmed import processing.

**Validation Rules**:

- Required cells must be present and non-empty.
- Duration must parse as a positive whole number.
- Date must parse as ISO date or common Notion date text.

## NormalizedImportRow

**Purpose**: Valid row payload used for preview display and confirmed import processing.

**Fields**:

- `row_number`: source row number.
- `log_date`: parsed calendar date.
- `task_name`: display task name after whitespace normalization.
- `normalized_task_name`: lowercase trimmed task name used for deduplication.
- `category_name`: display category name after whitespace normalization.
- `normalized_category_name`: lowercase trimmed category name used for category lookup.
- `time_spent_minutes`: positive whole-number duration.
- `tags`: unique lowercase trimmed tag array.
- `note`: nullable normalized note text.
- `row_snapshot`: structured summary sufficient for audit and row outcome review.

**Relationships**:

- Uses `DailyLogService` to reuse or create a daily log for `log_date`.
- Uses `TaskService` to create a task, reuse category, create optional note, and skip duplicates.
- References `ImportRun` only after the user confirms import.

**Validation Rules**:

- Tags split on commas, trim surrounding spaces, lowercase text, remove empty values, and keep unique values.
- Empty tags become `[]`.
- Empty notes become `null`.
- Text used for matching and grouping is lowercase and trimmed.

## ImportPreview

**Purpose**: Side-effect-free validation response for a CSV file.

**Fields**:

- `source_name`: filename or upload label.
- `total_rows`: number of data rows parsed.
- `valid_row_count`: count of rows valid for confirmed import.
- `invalid_row_count`: count of invalid rows.
- `valid_rows`: list of `NormalizedImportRow` values for user review.
- `invalid_rows`: row number plus reasons for rows that cannot import.
- `warnings`: optional non-blocking notices.

**Validation Rules**:

- Must not create `ImportRun`, `DailyLog`, `Task`, `Category`, `Note`, or `ImportRowOutcome` records.
- Must include row-specific invalid reasons.
- Must apply the same parsing and normalization rules used by confirmed import processing.

## ConfirmedImportCommand

**Purpose**: User-confirmed request to import a CSV file.

**Fields**:

- `owner_id`: resolved from authenticated context.
- `source_name`: filename or upload label.
- `csv_bytes`: transient uploaded CSV bytes.
- `request_id`: request correlation identifier when available.
- `idempotency_key`: optional request idempotency value when supplied by the client.

**Relationships**:

- Creates one `ImportRun`.
- Enqueues one background import task with the `ImportRun` ID and normalized row payloads.

**Validation Rules**:

- The server validates and normalizes the submitted CSV again at confirmation time.
- Missing required columns or a fully invalid file must return a handled validation error before enqueue.
- A mixed valid/invalid file may enqueue valid rows and record invalid rows during processing.
- The full raw CSV file is not retained after import history is recorded.

## ImportRun

**Purpose**: Persistent trace of a confirmed import attempt.

**Existing Fields Used**:

- `id`
- `owner_id`
- `source_type`
- `source_name`
- `status`
- `started_at`
- `completed_at`
- `processed_row_count`
- `inserted_row_count`
- `invalid_row_count`
- `skipped_row_count`
- `failed_row_count`
- `failure_reason`
- `created_at`
- `updated_at`
- `deleted_at`

**State Transitions**:

- `pending` -> `processing`
- `processing` -> `completed`
- `processing` -> `completed_with_errors`
- `processing` -> `failed`

**Validation Rules**:

- Created only after the user confirms import.
- Uses the shared status values: `pending`, `processing`, `completed`, `completed_with_errors`, `failed`.
- Terminal row counts must reflect inserted, invalid, skipped, and failed outcomes.
- Failed runs require failure details.
- Retains metadata and row outcomes only, not full raw CSV file contents.

## ImportRowOutcome

**Purpose**: Persistent row-level trace for rows not inserted as completed task data.

**Existing Fields Used**:

- `id`
- `owner_id`
- `import_run_id`
- `row_number`
- `outcome_type`
- `reason`
- `normalized_task_name`
- `log_date`
- `time_spent_minutes`
- `row_snapshot`
- `created_at`

**Validation Rules**:

- `outcome_type` is `invalid`, `skipped`, or `failed`.
- Invalid rows include row-specific validation reasons.
- Duplicate rows are recorded as skipped.
- Failed rows include processing failure reasons.
- `row_snapshot` stores a structured summary sufficient for audit review without full raw-file retention.

## ImportProcessingResult

**Purpose**: Service-level summary of a completed worker run.

**Fields**:

- `import_run_id`: associated ImportRun ID.
- `status`: terminal shared run status.
- `processed_row_count`
- `inserted_row_count`
- `invalid_row_count`
- `skipped_row_count`
- `failed_row_count`
- `failure_reason`: nullable full-run failure summary.

**Validation Rules**:

- If all processed rows insert cleanly, status is `completed`.
- If at least one row is invalid, skipped, or failed and at least one row is processed without full-run failure, status is `completed_with_errors`.
- If processing cannot continue due to a full-run failure, status is `failed`.

## API Pagination Shapes

**Purpose**: Bounded import history and row outcome review.

**Fields**:

- `page`: 1-based page number.
- `limit`: requested page size.
- `total`: total available records when inexpensive to calculate.
- `items`: page items.

**Validation Rules**:

- Default `page` is 1.
- Default `limit` is 20.
- Maximum `limit` is 100.
- Sort import runs by newest first.
- Sort row outcomes by row number and creation order.
