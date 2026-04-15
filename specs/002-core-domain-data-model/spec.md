# Feature Specification: Core Domain & Data Model

**Feature Branch**: `002-core-domain-data-model`  
**Created**: 2026-04-14  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 1 - Core Domain & Data Model"

## Clarifications

### Session 2026-04-14

- Q: When new data targets a date that already has a DailyLog, how should the model handle it? -> A: Reuse the existing DailyLog for the same date and add only non-duplicate tasks.
- Q: How should duplicate task rows be handled when they match an existing task by date, normalized task name, and time spent? -> A: Keep the existing task and record later duplicate rows as skipped import rows.
- Q: What status vocabulary should ImportRun and AIInsightRun use? -> A: Shared statuses: pending, processing, completed, completed_with_errors, failed.
- Q: What import traceability detail should Phase 1 require? -> A: Aggregate run counts plus row-level outcomes for invalid, skipped, and failed rows.
- Q: Which AI insight target periods should the Phase 1 model support for v1? -> A: Daily and weekly AI insight target periods.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Model Daily Tracking Records (Priority: P1)

As the project owner, I want a clear domain model for daily logs, tasks, categories, tags, and notes, so daily tracking data can be captured consistently before import, dashboard, or AI features are added.

**Why this priority**: The rest of the product depends on reliable daily tracking records with clean relationships and predictable meanings.

**Independent Test**: Can be tested by reviewing a sample day with multiple tasks and verifying every task has a single day, a normalized category, a structured tag list, and any related note without relying on later import or dashboard behavior.

**Acceptance Scenarios**:

1. **Given** a day contains several tracked tasks, **When** the records are represented by the model, **Then** every task is linked to exactly one daily log for that calendar date.
2. **Given** two tasks use the same category text with different capitalization or surrounding spaces, **When** the records are represented by the model, **Then** both tasks resolve to one canonical category.
3. **Given** a task has no tags and no note, **When** the record is represented by the model, **Then** its tags are represented as an empty structured list and no note is attached.
4. **Given** a DailyLog already exists for a calendar date, **When** new non-duplicate tasks are added for that date, **Then** those tasks attach to the existing DailyLog rather than creating a second DailyLog.

---

### User Story 2 - Preserve Import Traceability (Priority: P2)

As an implementer of the later import phase, I want imported daily tracking records to retain their import-run context, so every inserted, skipped, invalid, or failed row can be traced back to the import attempt that produced it.

**Why this priority**: CSV import reliability is a critical project rule, and traceability must be part of the model before import behavior is implemented.

**Independent Test**: Can be tested by reviewing a hypothetical import run and verifying the model can identify the run status, row counts, failure summary, and records created from that run.

**Acceptance Scenarios**:

1. **Given** an import run creates valid task records, **When** a reviewer inspects those records, **Then** each imported record can be traced to the import run that created it.
2. **Given** an import run includes invalid or skipped rows, **When** the run is inspected, **Then** the run can report totals for processed, inserted, invalid, skipped, and failed rows.
3. **Given** an import run fails before completion, **When** the run is inspected later, **Then** the failure status, failure reason, and timing information remain available.
4. **Given** an import row duplicates an existing task by date, normalized task name, and time spent, **When** the import run is represented by the model, **Then** the existing task is preserved and the duplicate row is recorded as skipped.
5. **Given** an import run is waiting, active, finished cleanly, finished with row-level problems, or failed, **When** the run is inspected, **Then** its status uses one of the shared run statuses.
6. **Given** an import run includes invalid, skipped, or failed rows, **When** the run is inspected, **Then** each non-inserted row outcome can be reviewed with its row reference, outcome type, and reason.

---

### User Story 3 - Support Future AI Insight Runs (Priority: P3)

As an implementer of the later AI analysis phase, I want AI insight runs to be represented separately from source tracking records, so analysis can be rerun, audited, and failed without mutating daily logs or tasks.

**Why this priority**: The Phase 0 AI boundary states that source logs, tasks, and imports remain authoritative while AI outputs are separate traceable results.

**Independent Test**: Can be tested by reviewing a hypothetical daily or weekly AI analysis run and verifying the model can record what period was analyzed, what source records were used, the run status, and any failure details without changing source records.

**Acceptance Scenarios**:

1. **Given** an AI insight run analyzes a day or week of daily logs, **When** the run is recorded, **Then** it identifies its target period and the source daily records used for analysis.
2. **Given** an AI insight run fails, **When** the run is inspected, **Then** the failure status and failure reason are available without altering daily logs, tasks, categories, tags, notes, or import runs.
3. **Given** an AI insight is regenerated for the same period, **When** previous runs are inspected, **Then** each run remains distinguishable by status, timing, and source context.
4. **Given** an AI insight run is waiting, active, finished cleanly, finished with partial analysis issues, or failed, **When** the run is inspected, **Then** its status uses one of the shared run statuses.

### Edge Cases

- If two daily logs are submitted for the same calendar date in the v1 personal workspace, the model must prevent ambiguous duplicate daily logs.
- If new data targets an existing DailyLog date, the model must reuse the existing DailyLog and attach only non-duplicate tasks.
- If a task has zero, negative, missing, or non-whole-number time spent, the model must treat the task duration as invalid for complete tracked data.
- If category text differs only by capitalization or surrounding spaces, the model must resolve it to the same canonical category.
- If a task has repeated tags after normalization, the model must keep only one occurrence of each tag value.
- If a task has no tags, the model must represent tags as an empty structured list rather than missing or null tag data.
- If a task has an empty note, the model must treat it as no note.
- If imported records are partially created before an import failure, the model must still allow reviewers to identify which records belong to the failed or partial import run.
- If a later import row duplicates an existing task by date, normalized task name, and time spent, the model must preserve the existing task and count the later row as skipped import input.
- If an import row is invalid, skipped, or fails during processing, the model must keep row-level outcome details sufficient to explain what happened without requiring full raw-file storage.
- If an ImportRun or AIInsightRun completes with recoverable row-level or source-level problems, the model must distinguish that outcome from both a clean completion and a full failure.
- If an AIInsightRun is requested for a period other than daily or weekly in v1, the model must treat that target period as outside Phase 1 scope.
- If source daily records change after an AI insight run, the historical AI insight run must remain distinguishable from later analysis runs.
- If future deletion behavior is introduced, source tracking changes must not erase historical import-run or AI-run traceability.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The Phase 1 domain model MUST define all core entities named in the project plan: DailyLog, Task, Category, Tag, Note, ImportRun, and AIInsightRun.
- **FR-002**: The model MUST represent one DailyLog as the tracking record for one calendar date in the v1 personal workspace.
- **FR-003**: The model MUST prevent ambiguous duplicate DailyLog records for the same calendar date in the v1 personal workspace.
- **FR-003a**: When new data targets a date with an existing DailyLog, the model MUST reuse that DailyLog and attach only non-duplicate Tasks to it.
- **FR-004**: The model MUST represent each Task as work performed on exactly one DailyLog.
- **FR-005**: The model MUST require each complete Task to have a task name, a positive whole-number time-spent value in minutes, and one Category.
- **FR-006**: The model MUST allow multiple Tasks to be associated with the same DailyLog.
- **FR-007**: The model MUST represent Category as a normalized reusable entity with one canonical name.
- **FR-008**: The model MUST treat category names as duplicates when they differ only by capitalization or surrounding spaces.
- **FR-009**: The model MUST represent Tag as a task-level label value stored in a JSON array on the Task rather than as a separately normalized category-like record.
- **FR-010**: The model MUST normalize tag values by trimming surrounding spaces, lowercasing text, removing empty values, and keeping unique values per Task.
- **FR-011**: The model MUST represent tasks with no tags as an empty structured tag array.
- **FR-012**: The model MUST represent Note as optional task-level note content.
- **FR-013**: The model MUST treat empty note content as no note.
- **FR-014**: The model MUST define the relationship between imported source data and created DailyLog, Task, Category, Tag, and Note records.
- **FR-015**: The model MUST define ImportRun as a traceable import attempt with source identification, processing status, start time, completion time when available, processed-row count, inserted-row count, invalid-row count, skipped-row count, and failure details when applicable.
- **FR-015a**: ImportRun status MUST use the shared run status vocabulary: pending, processing, completed, completed_with_errors, and failed.
- **FR-015b**: ImportRun traceability MUST include row-level outcomes for invalid, skipped, and failed rows with row reference, outcome type, and reason.
- **FR-016**: The model MUST allow every imported record created by an import attempt to be traced back to its ImportRun.
- **FR-017**: The model MUST support later import deduplication based on date, normalized task name, and time spent without requiring duplicate source records to be stored as separate completed tasks.
- **FR-017a**: When an imported row duplicates an existing Task by date, normalized task name, and time spent, the model MUST preserve the existing Task and record the later row as skipped import input.
- **FR-018**: The model MUST define AIInsightRun as a traceable analysis attempt with daily or weekly target period, source daily records, processing status, start time, completion time when available, and failure details when applicable.
- **FR-018a**: AIInsightRun status MUST use the shared run status vocabulary: pending, processing, completed, completed_with_errors, and failed.
- **FR-018b**: AIInsightRun target period MUST be limited to daily and weekly periods for v1.
- **FR-019**: The model MUST keep AIInsightRun records separate from DailyLog, Task, Category, Tag, Note, and ImportRun source records.
- **FR-020**: The model MUST ensure AIInsightRun records can be rerun for the same period while preserving previous run history.
- **FR-021**: The model MUST support reading daily logs by date and date range with their tasks, categories, tags, and notes.
- **FR-022**: The model MUST support calculating total tracked time by day, by category, and by tag from the represented records.
- **FR-023**: The model MUST preserve historical ImportRun and AIInsightRun traceability even if source tracking records are corrected later.
- **FR-024**: Phase 1 MUST define the domain and data model only; CSV upload flows, dashboard screens, AI analysis execution, scheduled automation, and production reliability workflows are outside this phase.

### Key Entities *(include if feature involves data)*

- **DailyLog**: The record for one tracked calendar date. It groups all tasks performed on that date and is the anchor for day-level review, summaries, and later analysis.
- **Task**: A unit of tracked work within a DailyLog. Key attributes include task name, time spent in minutes, category, tag list, optional note, and optional import trace.
- **Category**: A normalized reusable classification for tasks. It has a canonical name and is shared by tasks that belong to the same category.
- **Tag**: A task-level label value used for flexible grouping. Tags are normalized string values stored as a unique JSON array on each Task.
- **Note**: Optional task-level free-text context. Empty note content is treated as absent.
- **ImportRun**: A traceable import attempt that records source identification, status, timing, row counts, created records, skipped or invalid rows, and failure details.
- **AIInsightRun**: A traceable AI analysis attempt that records daily or weekly target period, source daily records, status, timing, rerun history, and failure details without mutating source tracking records.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of Phase 1 core entities listed in docs/Plan.md are represented in the specification with clear meanings and relationships.
- **SC-002**: A reviewer can trace any complete task to its day, category, tag list, optional note, and import context in under 5 minutes using the specification.
- **SC-003**: A reviewer can determine whether a proposed daily log, category, tag list, note, import run, or AI insight run is valid or invalid using only the Phase 1 rules.
- **SC-004**: Category normalization rules prevent 100% of duplicate category meanings caused only by capitalization or surrounding spaces.
- **SC-005**: Tag normalization rules produce an empty list for missing tags and unique normalized tag values for 100% of task records.
- **SC-006**: Import traceability rules allow 100% of imported records to be connected to the import attempt that produced them.
- **SC-007**: AI run traceability rules allow 100% of AI insight runs to be reviewed by target period, source records, status, timing, and failure details when present.
- **SC-008**: A reviewer can verify in under 10 minutes that Phase 1 does not include CSV upload flows, dashboard UI behavior, AI execution behavior, scheduling behavior, or production operations work.

## Assumptions

- The v1 workspace is personal and single-owner unless a later phase explicitly adds multi-user ownership.
- DailyLog uniqueness is based on calendar date within the v1 personal workspace.
- Task duration is tracked in minutes because the project plan's CSV contract uses `time_spent_minutes`.
- Category names and tag values use lowercase trimmed canonical text for consistency with the later CSV normalization phase.
- Notes from imported CSV rows are task-level context unless a later phase introduces day-level notes.
- ImportRun and AIInsightRun in Phase 1 define traceability needs only; actual import processing and AI execution are handled in later phases.
- The existing docs/Plan.md Phase 1 section is the authoritative input for this specification.
