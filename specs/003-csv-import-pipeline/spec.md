# Feature Specification: CSV Import Pipeline

**Feature Branch**: `003-csv-import-pipeline`  
**Created**: 2026-04-15  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 2 - CSV Import Pipeline"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Preview CSV Import Data (Priority: P1)

As the project owner, I want to upload a Notion CSV export and preview the parsed rows before import, so I can catch file and row problems before data is added to my tracker.

**Why this priority**: Preview and validation are the first reliability checkpoint. The user should understand whether a file is usable before any records are changed.

**Independent Test**: Can be tested by submitting a CSV file with required and optional columns, then confirming the preview shows normalized values, valid rows, invalid rows, and row-level messages without inserting data.

**Acceptance Scenarios**:

1. **Given** a CSV file contains the required columns `date`, `task`, `category`, and `time_spent_minutes`, **When** the user requests a preview, **Then** the system displays parsed rows with validation status for each row.
2. **Given** a CSV file omits one or more required columns, **When** the user requests a preview, **Then** the system rejects the file for import and explains which required columns are missing.
3. **Given** a CSV file includes optional `tags` and `notes` columns, **When** the user requests a preview, **Then** the system includes the normalized tag list and note value in the preview.
4. **Given** a CSV row has invalid required data, **When** the preview is generated, **Then** that row is marked invalid with a clear reason and no data is inserted.

---

### User Story 2 - Import Valid Daily Tracking Rows (Priority: P2)

As the project owner, I want valid CSV rows to become structured daily tracking records, so exported daily logs can be reused for dashboards and later analysis.

**Why this priority**: The feature delivers its core value only when valid rows are normalized, deduplicated, and saved as usable tracking records.

**Independent Test**: Can be tested by importing a CSV file containing valid rows, invalid rows, duplicate rows, optional tags, and optional notes, then confirming only non-duplicate valid rows are saved with the expected normalized values.

**Acceptance Scenarios**:

1. **Given** a CSV file has valid rows, **When** the user confirms import, **Then** each non-duplicate valid row is saved as structured daily tracking data.
2. **Given** a row contains uppercase text or surrounding spaces in task, category, tags, or notes, **When** the row is imported, **Then** text values used for matching and grouping are lowercased and trimmed.
3. **Given** a row contains repeated or blank tags, **When** the row is imported, **Then** tags are saved as a unique array of non-empty normalized values.
4. **Given** a row has an empty notes value, **When** the row is imported, **Then** the saved record treats the note as absent.
5. **Given** a row duplicates an existing task by date, normalized task name, and time spent, **When** the row is processed, **Then** the existing task is preserved and the duplicate row is skipped.

---

### User Story 3 - Track Import Progress and Outcomes (Priority: P3)

As the project owner, I want each import attempt to show status, counts, and row outcomes, so I can trust what happened even when a file has partial problems or processing takes time.

**Why this priority**: Import traceability is a critical project rule and is necessary for diagnosing bad files, duplicate data, and partial failures.

**Independent Test**: Can be tested by starting an import and reviewing its import run record while processing, after successful completion, after completion with row errors, and after a failed import.

**Acceptance Scenarios**:

1. **Given** the user confirms an import, **When** processing begins, **Then** the system creates an import run with a status that reflects queued or active processing.
2. **Given** an import contains valid, invalid, and duplicate rows, **When** processing completes, **Then** the import run reports processed, inserted, invalid, skipped, and failed row counts.
3. **Given** an import row is invalid, duplicate, or fails during processing, **When** the import run is reviewed, **Then** the row outcome includes the row reference, outcome type, and reason.
4. **Given** an import fails before all rows are processed, **When** the import run is reviewed later, **Then** the failure status, failure reason, timing, and any completed row outcomes remain available.
5. **Given** import processing takes longer than an immediate response, **When** the user checks the import run, **Then** the current status is available without requiring the user to resubmit the file.

### Edge Cases

- If the uploaded file is empty, the system must reject the import and explain that no rows were available.
- If the uploaded file is not a readable CSV, the system must reject the import and explain that the file format cannot be parsed.
- If required column names differ only by capitalization or surrounding spaces, the system should recognize them as the required columns.
- If a row has a missing or invalid date, missing task, missing category, missing time spent, zero time spent, negative time spent, or non-whole-number time spent, the row must be invalid.
- If optional `tags` is missing, blank, or contains only blank values, the row must use an empty tag array.
- If optional `notes` is missing or blank, the row must treat notes as absent.
- If tags contain repeated values after trimming and lowercasing, only one instance of each tag value is retained for that row.
- If multiple rows in the same CSV duplicate one another by date, normalized task name, and time spent, the first valid occurrence is eligible for insertion and later duplicates are skipped.
- If an imported row duplicates an existing task by date, normalized task name, and time spent, the existing task is preserved and the imported row is recorded as skipped.
- If a file contains both valid and invalid rows, valid non-duplicate rows must still be importable while invalid rows are logged.
- If processing is retried for the same import run, the retry must not insert duplicate tasks that were already inserted by the earlier attempt.
- If a user requests preview only, no tracking records are inserted.
- If processing is interrupted, the import run must remain traceable with the latest known status and row outcomes available at the time of interruption.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow the user to submit a CSV file for import preview.
- **FR-002**: The CSV contract MUST require the columns `date`, `task`, `category`, and `time_spent_minutes`.
- **FR-003**: The CSV contract MUST allow optional `tags` and `notes` columns.
- **FR-004**: The system MUST validate the CSV file before insertion and identify missing required columns.
- **FR-005**: The system MUST validate each row independently and identify row-specific validation failures.
- **FR-006**: The system MUST provide a preview that separates valid rows, invalid rows, and row-level validation reasons before records are inserted.
- **FR-007**: Preview behavior MUST NOT insert or modify daily tracking records.
- **FR-008**: The system MUST normalize imported text by trimming surrounding spaces and lowercasing task names, category names, tag values, and note text.
- **FR-009**: The system MUST convert imported tags into an array of unique, non-empty normalized values.
- **FR-010**: The system MUST represent missing or empty tags as an empty array.
- **FR-011**: The system MUST represent missing or empty notes as absent note content.
- **FR-012**: The system MUST treat a row as invalid when required values are missing or when time spent is not a positive whole number of minutes.
- **FR-013**: The system MUST allow the user to confirm import of valid previewed data.
- **FR-014**: The system MUST process confirmed imports without requiring the user to wait on the submission action until all rows are completed.
- **FR-015**: The system MUST make import status available after confirmation, including queued, processing, completed, completed with row issues, and failed outcomes.
- **FR-016**: The system MUST insert valid non-duplicate rows as structured daily tracking records linked to their calendar date, task, category, tags, optional note, and import run.
- **FR-017**: The system MUST reuse the existing daily log for a row's date when that daily log already exists.
- **FR-018**: The system MUST reuse the existing category when an imported category matches an existing category after normalization.
- **FR-019**: The system MUST deduplicate imported tasks based on date, normalized task name, and time spent in minutes.
- **FR-020**: The system MUST skip duplicate rows without changing the existing task record.
- **FR-021**: The system MUST track each confirmed import as an import run with source identification, status, start time, completion time when available, processed-row count, inserted-row count, invalid-row count, skipped-row count, failed-row count, and failure details when applicable.
- **FR-022**: The system MUST keep row-level outcomes for invalid, skipped, and failed rows, including row reference, outcome type, and reason.
- **FR-023**: The system MUST preserve import run history after completion or failure so the user can review what happened later.
- **FR-024**: The system MUST make confirmed import processing idempotent for the same import attempt so retries do not create duplicate tracking records.
- **FR-025**: Phase 2 MUST cover CSV import only; dashboard visualization, AI analysis, scheduled imports, Notion API synchronization, and report export are outside this phase.

### Key Entities *(include if feature involves data)*

- **CSV Import File**: A user-submitted CSV export containing required daily tracking columns and optional tag or note data.
- **Parsed Import Row**: One CSV row after parsing, validation, normalization, and duplicate checking. It includes the original row reference, normalized values, validation state, and outcome reason when applicable.
- **Import Preview**: A reviewable result produced before insertion that lists valid rows, invalid rows, normalized values, and validation messages.
- **ImportRun**: A traceable import attempt with source identification, status, timing, row counts, failure details, and links to created or skipped outcomes.
- **Import Row Outcome**: A row-level trace for invalid, skipped, or failed rows with row reference, outcome type, and reason.
- **DailyLog**: The structured record for one calendar date that receives imported tasks.
- **Task**: A structured work item imported from a valid CSV row with task name, time spent, category, tag array, optional note, and import trace.
- **Category**: A normalized reusable grouping for imported tasks.
- **Tag List**: A task-level array of unique normalized tag values created from the optional CSV tags column.
- **Note**: Optional task-level text created from the optional CSV notes column when present after normalization.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of CSV files missing any required column are rejected before insertion with a message identifying the missing columns.
- **SC-002**: 100% of preview requests leave existing daily tracking records unchanged.
- **SC-003**: 100% of valid non-duplicate rows in a confirmed import are inserted as structured tracking records.
- **SC-004**: 100% of invalid rows are excluded from insertion and recorded with row-specific reasons.
- **SC-005**: 100% of duplicate rows are skipped based on date, normalized task name, and time spent while preserving existing task records.
- **SC-006**: 100% of inserted rows apply the Phase 2 normalization rules for lowercase text, trimmed spaces, unique tags, empty tags, and empty notes.
- **SC-007**: A user can review an import run's status, row counts, and row-level problems in under 2 minutes after processing completes.
- **SC-008**: Retrying the same confirmed import attempt creates zero duplicate task records.
- **SC-009**: A mixed-quality CSV containing valid, invalid, and duplicate rows completes with accurate inserted, invalid, skipped, and failed counts.
- **SC-010**: A reviewer can verify in under 10 minutes that Phase 2 does not include dashboard screens, AI analysis execution, scheduled automation, Notion API synchronization, or report export.

## Assumptions

- Phase 1 domain entities and traceability rules are available as the data foundation for this import phase.
- The v1 product is a personal single-owner tracker unless a later phase introduces multi-user ownership.
- CSV files come from Notion exports or compatible files using the same column contract.
- Column matching is case-insensitive and ignores surrounding spaces because exported CSV headers may vary slightly.
- Tags in the CSV are provided as a delimiter-separated text value; the exact accepted delimiter rules can be finalized during planning without changing the user-facing contract.
- Import preview may be generated separately from confirmed import processing.
- Confirmed import processing may continue after the initial user action returns, and users rely on import status to check completion.
- The existing docs/Plan.md Phase 2 section is the authoritative input for this specification.
