# Contract: Core Domain Data

Phase 1 is a backend domain and persistence phase. This contract defines the service and repository behavior required by the model. It does not require public dashboard endpoints, CSV upload endpoints, AI execution endpoints, or scheduled jobs.

## Response Shape If Endpoints Are Added

If implementation adds any inspection endpoint in Phase 1, it must:

- Register under `/api/v1/`.
- Return handled JSON success responses as:

```json
{
  "success": true,
  "data": {}
}
```

- Return handled errors as:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {}
  }
}
```

- Define `page` and `limit` for any bounded list endpoint that exposes user-navigable results.
- Define auth scopes and rate limits if the endpoint is protected or expensive.

## DailyLog Service Contract

### `get_or_create_daily_log(owner_id, log_date, source)`

**Input**:

- `owner_id`: UUID.
- `log_date`: calendar date.
- `source`: source label.

**Output**:

- Existing active `DailyLog` for `owner_id + log_date`, or a new one when none exists.

**Rules**:

- Must not create a second active DailyLog for the same owner and date.
- Must preserve soft-deleted logs unless explicit restore behavior is introduced later.

### `get_daily_log_with_entries(owner_id, log_date)`

**Input**:

- `owner_id`: UUID.
- `log_date`: calendar date.

**Output**:

- DailyLog with active tasks, categories, tags, and optional notes.

**Rules**:

- Normal reads exclude soft-deleted records.

### `list_daily_logs_by_range(owner_id, start_date, end_date)`

**Input**:

- `owner_id`: UUID.
- `start_date`: calendar date.
- `end_date`: calendar date.

**Output**:

- Ordered daily logs in the inclusive range with related active task data.

**Rules**:

- `start_date` must be on or before `end_date`.
- This is a service/repository contract for Phase 1; public pagination is deferred until an endpoint is introduced.

## Task Service Contract

### `create_task(owner_id, daily_log_id, title, time_spent_minutes, category_name, tags, note, import_run_id)`

**Input**:

- `owner_id`: UUID.
- `daily_log_id`: UUID.
- `title`: non-empty string.
- `time_spent_minutes`: positive whole number.
- `category_name`: non-empty string.
- `tags`: optional list of strings.
- `note`: optional string.
- `import_run_id`: optional UUID.

**Output**:

- Created Task with normalized category, normalized tag JSON array, and optional Note.

**Rules**:

- Category is reused by normalized name.
- Tags are trimmed, lowercased, empty-filtered, and de-duplicated.
- Empty note input does not create a Note.
- Imported duplicate rows are not created as Tasks; the import trace service records a skipped row outcome.

### `calculate_totals(owner_id, start_date, end_date)`

**Output**:

- Totals by day, category, and tag based on active tasks.

**Rules**:

- Exclude soft-deleted tasks, notes, categories, and daily logs from normal totals.

## Import Trace Service Contract

### `create_import_run(owner_id, source_type, source_name)`

**Output**:

- ImportRun with status `pending` and zero row counts.

### `mark_import_processing(import_run_id)`

**Rules**:

- Valid transition: `pending` -> `processing`.

### `record_import_row_outcome(import_run_id, row_number, outcome_type, reason, row_summary)`

**Input**:

- `outcome_type`: invalid, skipped, or failed.
- `reason`: concise explanation.
- `row_summary`: optional normalized row details.

**Rules**:

- Must increment the matching outcome count on ImportRun.
- Must preserve row-level reason for invalid, skipped, and failed rows.

### `complete_import_run(import_run_id, status)`

**Input**:

- `status`: `completed`, `completed_with_errors`, or `failed`.

**Rules**:

- Terminal status must align with row counts and failure details.
- Failed runs require failure details.
- Existing created records remain traceable to the run.

## AI Insight Run Service Contract

### `create_ai_insight_run(owner_id, target_period_type, period_start, period_end, source_daily_log_ids)`

**Input**:

- `target_period_type`: daily or weekly.
- `period_start`: date.
- `period_end`: date.
- `source_daily_log_ids`: list of DailyLog IDs.

**Output**:

- AIInsightRun with status `pending` and immutable source links.

**Rules**:

- Daily target periods use identical start and end dates.
- Weekly target periods cover exactly seven days.
- Unsupported target period types are rejected as outside v1 scope.
- Source DailyLogs are read-only inputs; the AI run must not mutate source records.

### `mark_ai_run_processing(ai_insight_run_id)`

**Rules**:

- Valid transition: `pending` -> `processing`.

### `complete_ai_run(ai_insight_run_id, status, output_summary, failure_reason)`

**Input**:

- `status`: `completed`, `completed_with_errors`, or `failed`.

**Rules**:

- Reruns create separate AIInsightRun records.
- Failed runs require failure details.
- Completed runs may include output summary metadata, but AI generation content is finalized by later AI phases.

## Repository Contract

Repositories must:

- Accept an `AsyncSession`.
- Return ORM entities or typed domain structures, not HTTP responses.
- Encapsulate SQLAlchemy queries.
- Provide uniqueness-safe helpers for DailyLog and Category lookup/creation.
- Provide active-record query helpers that exclude soft-deleted rows by default.
- Provide traceability query helpers that can include soft-deleted rows when reviewing ImportRun or AIInsightRun history.
