# Research: Core Domain & Data Model

## Decision: Split Models Across Owning Modules

**Decision**: Implement models in the modules that own their behavior: `DailyLog` in `daily_logs`, `Task` and `Category` in `tasks`, `Note` in `notes`, `ImportRun` and import row outcomes in `imports`, and `AIInsightRun` in `ai_insights`.

**Rationale**: The constitution requires a modular monolith with feature isolation. Splitting models by owner keeps module responsibilities reviewable while still allowing relationships across modules.

**Alternatives considered**:

- Single global domain models file: rejected because it weakens feature ownership and will grow into a shared dumping ground.
- Put all Phase 1 models under `daily_logs`: rejected because import and AI traceability have distinct lifecycle behavior and ownership.

## Decision: DailyLog Uniqueness Uses Owner and Calendar Date

**Decision**: A `DailyLog` is unique by `owner_id` plus `log_date`; when new data targets an existing date, services reuse the existing record and attach non-duplicate tasks.

**Rationale**: The clarified spec requires one unambiguous daily log per date in the v1 personal workspace while preserving a future path for authenticated ownership.

**Alternatives considered**:

- Unique by date only: rejected because future auth or multi-user support would require a disruptive migration.
- Allow multiple logs per date by import run: rejected because it contradicts the clarified one-log-per-date rule.

## Decision: Tags Are a JSON Array on Task

**Decision**: Store normalized task tags as a JSON array on `Task`, with service validation that trims, lowercases, removes empty values, and de-duplicates per task.

**Rationale**: The Phase 1 plan explicitly requires tags stored as a JSON array, while dashboard breakdowns can still aggregate tag values later by reading normalized arrays.

**Alternatives considered**:

- Separate normalized `Tag` table: rejected because it violates the explicit JSON-array requirement and adds unnecessary join complexity for v1.
- Free-form comma-delimited string: rejected because it weakens validation, uniqueness, and future analytics.

## Decision: Category Is a Normalized Table

**Decision**: Store categories as normalized records with canonical lowercase trimmed names and uniqueness by owner plus canonical name.

**Rationale**: The project plan requires normalized categories. A dedicated table prevents duplicate category meanings caused by capitalization or surrounding whitespace.

**Alternatives considered**:

- Category as task string only: rejected because it cannot enforce normalization or clean relationships.
- Global category names without owner: rejected because later multi-user support may need user-specific category vocabularies.

## Decision: Duplicate Imported Tasks Are Skipped

**Decision**: Treat imported rows as duplicates when they match an existing task by `log_date`, normalized task name, and `time_spent_minutes`; keep the existing task and record later duplicate rows as skipped import input.

**Rationale**: This matches the clarified spec and Phase 2 deduplication rule while avoiding unsafe merges of category, tag, or note differences.

**Alternatives considered**:

- Merge duplicate rows: rejected because it can silently combine conflicting note, tag, or category data.
- Replace existing task: rejected because it damages auditability and makes retries destructive.
- Allow duplicates when metadata differs: rejected because it weakens import idempotency.

## Decision: ImportRun Includes Row-Level Outcomes for Non-Inserted Rows

**Decision**: Store aggregate counts on `ImportRun` and row-level outcomes for invalid, skipped, and failed rows with row reference, outcome type, reason, and optional row snapshot.

**Rationale**: The clarified spec requires enough detail to explain invalid, skipped, and failed rows without requiring full raw-file storage in Phase 1.

**Alternatives considered**:

- Aggregate counts only: rejected because it would not explain individual invalid or skipped rows.
- Store full raw file in Phase 1: rejected because file storage is beyond the core domain model scope.

## Decision: Shared Run Status Vocabulary

**Decision**: `ImportRun` and `AIInsightRun` use the shared statuses `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`.

**Rationale**: A shared lifecycle supports future background work, partial outcomes, and consistent operational status handling.

**Alternatives considered**:

- Simpler statuses without `completed_with_errors`: rejected because partial imports and partial AI analysis issues need a non-failure terminal state.
- Separate status vocabularies: rejected because it adds complexity without current value.

## Decision: AIInsightRun Supports Daily and Weekly Target Periods

**Decision**: Limit v1 AI insight target periods to `daily` and `weekly`, with period start/end dates and source daily-log references.

**Rationale**: The project plan names daily and weekly summaries in the AI analysis phase. Monthly or custom ranges can be added later without forcing them into Phase 1.

**Alternatives considered**:

- Daily only: rejected because weekly summary is already in the v1 plan.
- Daily, weekly, monthly, and custom ranges: rejected because it expands scope beyond the clarified Phase 1 model.

## Decision: Soft Delete for Traceability-Sensitive Records

**Decision**: Include soft-delete capability for user-owned source records and traceability-sensitive operational records, with normal queries excluding soft-deleted rows by default.

**Rationale**: The constitution requires soft delete where deletion could affect traceability, restore behavior, or historical analytics.

**Alternatives considered**:

- Hard delete all records: rejected because it can break import and AI run traceability.
- No deletion fields in Phase 1: rejected because retrofitting soft delete later would affect every core table.
