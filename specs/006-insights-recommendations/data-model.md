# Data Model: Insights & Recommendations

Phase 5 adds stored deterministic insight results derived from completed Phase 4 `AIInsightRun` output and saved tracking facts. Source records remain authoritative and are never mutated by insight generation.

## Shared Concepts

### Insight Period Granularity

**Purpose**: Identify the supported shape of a Phase 5 insight period.

**Values**:

- `daily`
- `weekly`

**Validation Rules**:

- `daily` periods use identical `period_start` and `period_end`.
- `weekly` periods cover exactly seven local calendar days from Monday through Sunday.
- Month and custom date ranges are outside Phase 5.

### Insight Result Status

**Purpose**: Track whether a generated result is safe to show.

**Values**:

- `completed`: Result passed validation and may be current.
- `failed`: Generation or validation failed and the result must not be shown as successful.

**Validation Rules**:

- `completed` results require a successful validation outcome.
- `failed` results require a failure code and failure details.
- Failed results may remain in history for audit but are never current.

### Score State

**Purpose**: Represent a score outcome without fabricating unsupported numeric values.

**Values**:

- `scored`
- `insufficient_data`
- `not_applicable`

**Validation Rules**:

- `scored` requires an integer score from 0 to 100 and at least two evidence references.
- `insufficient_data` requires no numeric score and a missing-data reason.
- `not_applicable` is allowed for single-day consistency score and single-day best/worst comparisons.

## Insight Generation Request

**Purpose**: A user request to generate or reuse an insight result for one supported period.

**Fields**:

- `owner_id`: UUID actor/workspace reference from authentication context.
- `period_granularity`: `daily` or `weekly`.
- `anchor_date`: requested local calendar date used to resolve the target period.
- `source_ai_insight_run_id`: optional UUID of the completed Phase 4 run to use.
- `explicit_rerun`: boolean, false for default generation and true for rerun endpoints.
- `request_id`: optional request correlation identifier.
- `idempotency_key`: optional client duplicate-submission key.

**Validation Rules**:

- Owner is required and derived from authentication context.
- If `source_ai_insight_run_id` is omitted, the service resolves the current completed Phase 4 analysis for the period.
- The source analysis run must belong to the owner, match the resolved period, be active, and have completed output.
- Failed, processing, incomplete, malformed, or missing Phase 4 analysis blocks successful generation.
- Request payloads must not include note text or arbitrary prompt text.

## AIInsightResult

**Purpose**: Durable Phase 5 result containing scores, findings, recommendations, explanations, validation, source links, and current-result metadata.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID actor/workspace reference.
- `period_granularity`: `daily` or `weekly`.
- `period_start`: date.
- `period_end`: date.
- `source_ai_insight_run_id`: UUID reference to completed Phase 4 `AIInsightRun`.
- `status`: `completed` or `failed`.
- `is_current`: boolean current marker for successful results.
- `generation_reason`: `default_generate` or `explicit_rerun`.
- `idempotency_key`: nullable client duplicate-submission key.
- `request_id`: nullable request correlation identifier.
- `source_snapshot`: JSON source tracking summary used by scoring.
- `productivity_score`: JSON `ScoreOutcome`.
- `consistency_score`: nullable JSON `ScoreOutcome`.
- `best_day_finding`: nullable JSON `DayFinding`.
- `worst_day_finding`: nullable JSON `DayFinding`.
- `recommendations`: JSON array of `Recommendation`.
- `evidence`: JSON array of `InsightEvidence`.
- `validation_outcome`: JSON `InsightValidationOutcome`.
- `failure_code`: nullable stable error code.
- `failure_details`: nullable structured failure details.
- `generated_at`: timestamp.
- `created_at`: timestamp.
- `updated_at`: timestamp.
- `deleted_at`: nullable soft-delete timestamp.

**Relationships**:

- Belongs to one completed Phase 4 `AIInsightRun`.
- Has many `AIInsightResultSource` records referencing source `DailyLog` records.
- Does not own or mutate `DailyLog`, `Task`, `Category`, `Tag`, `Note`, `ImportRun`, or `AIInsightRun` records.

**Validation Rules**:

- Completed results require `validation_outcome.passed = true`.
- Failed results require `validation_outcome.passed = false`, `failure_code`, and `failure_details`.
- Only one active completed result may be current per owner + period granularity + period at a time.
- Default generation for owner + period + source analysis returns the existing current result when one exists.
- Explicit rerun creates a new result and marks the latest successful rerun current.
- `source_snapshot.excluded_fields` must include `note_text`.
- Normal reads exclude soft-deleted results.

## AIInsightResultSource

**Purpose**: Preserve source `DailyLog` references used by a Phase 5 result.

**Fields**:

- `id`: UUID primary key.
- `owner_id`: UUID owner/workspace reference.
- `ai_insight_result_id`: required UUID reference to `AIInsightResult`.
- `daily_log_id`: required UUID reference to `DailyLog`.
- `created_at`: timestamp.

**Validation Rules**:

- Source links are immutable after result creation.
- Source links are retained even if source `DailyLog` is soft-deleted later.
- No note text is copied into source links.

## Source Snapshot

**Purpose**: Retained audit summary of saved facts used for deterministic scoring and recommendations.

**Fields**:

- `period_granularity`: `daily` or `weekly`.
- `period_start`: date.
- `period_end`: date.
- `source_daily_log_ids`: list of DailyLog UUIDs.
- `source_task_ids`: list of Task UUIDs used as evidence.
- `daily_log_count`: non-negative integer.
- `tracked_day_count`: non-negative integer.
- `task_count`: non-negative integer.
- `total_minutes`: non-negative integer.
- `category_totals`: list of category labels with total minutes.
- `tag_totals`: list of tag labels with total minutes.
- `daily_totals`: list of dates with total minutes for weekly periods.
- `phase4_observation_ids`: list of source analysis observation identifiers when available.
- `included_fields`: list containing task names, durations, categories, and tags.
- `excluded_fields`: list containing note text.

**Validation Rules**:

- Must not contain note text.
- Must reflect saved tracking facts at generation time.
- Must identify the source analysis run used so stale source analysis is visible to the user.

## ScoreOutcome

**Purpose**: Represent productivity or consistency scoring with explanation and evidence.

**Fields**:

- `score_type`: `productivity` or `consistency`.
- `state`: `scored`, `insufficient_data`, or `not_applicable`.
- `score`: nullable integer from 0 to 100.
- `confidence`: `low`, `medium`, or `high`.
- `summary`: plain-language explanation.
- `positive_factors`: list of score factor objects.
- `limiting_factors`: list of score factor objects.
- `evidence_ids`: list of evidence identifiers.
- `insufficient_data_reason`: nullable string.

**Validation Rules**:

- Productivity `scored` requires at least one tracked day, one tracked task, completed source analysis, and two evidence references.
- Weekly consistency `scored` requires at least three tracked days.
- Daily consistency uses `not_applicable`.
- Scores must be integers between 0 and 100.
- Score factors must reference evidence from the selected period.

## Score Factor

**Purpose**: Explain why a score moved up or down.

**Fields**:

- `label`: concise factor name.
- `direction`: `positive` or `limiting`.
- `explanation`: plain-language reason.
- `evidence_ids`: list of evidence identifiers.

**Validation Rules**:

- Each factor must have at least one evidence reference.
- Factor text must avoid medical claims, character judgments, shame, and blame.

## DayFinding

**Purpose**: Identify a relative best or worst day in a weekly period.

**Fields**:

- `finding_type`: `best_day`, `worst_day`, or `no_meaningful_distinction`.
- `date`: nullable date.
- `label`: neutral display label.
- `summary`: neutral explanation.
- `confidence`: `low`, `medium`, or `high`.
- `evidence_ids`: list of evidence identifiers.
- `tie_or_close_ranking`: boolean.

**Validation Rules**:

- Day findings are omitted or marked not applicable for daily periods.
- Weekly best/worst labels require at least three tracked days and a meaningful distinction.
- Worst-day language must be neutral and pattern-focused.
- Ties or close rankings must be explained without overstating differences.

## Recommendation

**Purpose**: Concise, evidence-backed suggested action.

**Fields**:

- `recommendation_id`: stable identifier within the result.
- `priority`: integer 1 through 3.
- `action`: user-controlled concrete action.
- `rationale`: reason for the action.
- `expected_benefit`: expected benefit stated without guarantees.
- `confidence`: `low`, `medium`, or `high`.
- `evidence_ids`: list of evidence identifiers.
- `source_links`: list of score, day-finding, or Phase 4 observation references.
- `dedupe_key`: stable key for similar recommendations from the same source pattern.

**Validation Rules**:

- A result may include 0-3 recommendations.
- Each recommendation requires action, rationale, evidence, expected benefit, confidence, and priority.
- Actions must be user-controlled and concrete.
- Recommendations must not be generic, unsupported, duplicative, unactionable, medical, or character-judgment claims.
- Similar recommendations for the same source pattern should reuse or evolve the `dedupe_key` to keep history understandable.

## InsightEvidence

**Purpose**: Tie scores, findings, and recommendations to source facts or supported Phase 4 observations.

**Fields**:

- `evidence_id`: stable local identifier within the result.
- `evidence_type`: `date_total`, `category_total`, `tag_total`, `task_count`, `task_reference`, `duration_outlier`, `phase4_pattern`, or `phase4_behavior_insight`.
- `source_date`: nullable date.
- `source_task_id`: nullable Task UUID.
- `source_ai_insight_run_id`: nullable Phase 4 run UUID.
- `source_observation_id`: nullable Phase 4 observation identifier.
- `label`: nullable category, tag, task, or observation label.
- `minutes`: nullable tracked duration.
- `count`: nullable count.
- `summary`: short evidence summary.

**Validation Rules**:

- Evidence must belong to the selected period and owner.
- Evidence may reference task IDs and task names but not note text.
- Phase 4 observations must not override conflicting saved tracking facts.

## InsightValidationOutcome

**Purpose**: Persist validation checks that decide whether a result is successful.

**Fields**:

- `passed`: boolean.
- `checked_at`: timestamp.
- `validator_version`: version string.
- `checks`: list of validation check results.
- `failure_codes`: list of stable failure codes.

**Validation Rules**:

- Successful results require all blocking checks to pass.
- Blocking checks cover score bounds, required explanations, evidence references, recommendation count, actionability, unsupported claims, duplicate recommendations, source period match, current-result consistency, and privacy boundary.

## Current Insight Result

**Purpose**: The latest successful Phase 5 result for an owner, period, and period granularity.

**Selection Rules**:

- Include only active results where `status = completed`, `validation_outcome.passed = true`, and `is_current = true`.
- A successful explicit rerun clears the previous current marker for that owner + period and marks the new result current.
- Default generation returns the existing current result for the same owner + period + source analysis.
- Failed and soft-deleted results are never current.

## State Transitions

- Default generate with existing current result for same source analysis: return existing `completed` result with `reused_existing = true`.
- Default generate with no current result for source analysis: create result, validate, then mark `completed` and current or mark `failed`.
- Explicit rerun: create new result, validate, then mark latest successful result current and preserve prior results.
- Soft delete: set `deleted_at`; normal current/detail/history reads exclude deleted results.

## Query Requirements

- Get current insight result by owner, period granularity, and anchor date.
- Find completed Phase 4 source analysis by owner, period granularity, and period.
- Find an existing current result by owner + period + source analysis.
- List insight result history by owner with page/limit, period granularity, status, and date filters.
- Get one insight result by owner and result ID.
- Fetch saved source records for daily or weekly generation without note text.
- Mark previous current results not current when an explicit rerun succeeds.
