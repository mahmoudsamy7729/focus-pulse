# Feature Specification: AI Analysis Engine

**Feature Branch**: `005-ai-analysis-engine`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 4 - AI Analysis Engine"

## Clarifications

### Session 2026-04-19

- Q: What privacy boundary should Phase 4 use for AI analysis inputs? -> A: Use task names, durations, categories, and tags, but exclude note text from AI inputs.
- Q: How much of the AI analysis input should Phase 4 retain after a run? -> A: Store source record references, aggregate input summary, instruction version, and output only.
- Q: How should Phase 4 package AI analysis runs and outputs? -> A: One combined analysis run per day or week, containing summary, patterns, behavior insights, evidence, and limitations.
- Q: How should Phase 4 represent a no-data analysis request within the existing shared statuses? -> A: Status `completed`, with output outcome `no_data`.
- Q: What bounded retry policy should Phase 4 use for transient AI analysis failures? -> A: Up to 3 total attempts per run, then mark `failed`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Daily and Weekly Summaries (Priority: P1)

As the project owner, I want AI-generated daily and weekly summaries from my saved tracking data, so I can understand what happened without manually reading every task, category, and tag.

**Why this priority**: Daily and weekly summaries are the core Phase 4 value. They convert already imported and visualized tracking records into understandable narrative analysis.

**Independent Test**: Can be tested by requesting analysis for a day and a week with saved tracking records, then verifying that each completed result is stored, reviewable, and grounded in the selected period's records.

**Acceptance Scenarios**:

1. **Given** a selected day has saved tracking records, **When** the user requests a daily analysis, **Then** the system creates a daily summary that reflects that day's total tracked time, task count, and category and tag themes.
2. **Given** a selected week has saved tracking records, **When** the user requests a weekly analysis, **Then** the system creates a weekly summary that reflects daily totals, category and tag distribution, recurring themes, and notable changes across the week.
3. **Given** the selected period has no saved tracking records, **When** analysis is requested, **Then** the system records a completed run with output outcome `no_data` and does not produce fabricated summary text.
4. **Given** a completed analysis exists, **When** the user reviews the result later, **Then** the stored summary is available without requiring the analysis to be regenerated.

---

### User Story 2 - Detect Patterns and Behavior Insights (Priority: P2)

As the project owner, I want the system to identify patterns and neutral behavior insights in my tracking history, so I can notice repeated work themes, time concentration, and unusual distributions before later recommendation features are added.

**Why this priority**: Pattern detection is the difference between a plain summary and an analysis engine. It prepares the ground for Phase 5 while keeping this phase limited to observations.

**Independent Test**: Can be tested with sample days and weeks containing repeated categories, tags, task themes, and uneven daily totals, then verifying that generated patterns include supporting evidence from the source data.

**Acceptance Scenarios**:

1. **Given** a selected period contains repeated categories, tags, or task themes, **When** analysis completes, **Then** the result lists the detected patterns with evidence such as dates, task counts, or tracked-time totals.
2. **Given** a selected week contains uneven tracked-time totals across days, **When** weekly analysis completes, **Then** the result identifies the distribution pattern without labeling it good or bad unless the data supports that framing.
3. **Given** task notes are present, **When** analysis completes, **Then** note text is excluded from generated observations and is not reproduced in the output.
4. **Given** the available data does not support a meaningful pattern, **When** analysis completes, **Then** the result states that no strong pattern was detected instead of inventing one.

---

### User Story 3 - Track AI Runs and Failures (Priority: P3)

As the project owner, I want every analysis attempt to have status, history, and failure details, so I can trust which results were generated and diagnose problems when an analysis fails.

**Why this priority**: AI output must be auditable. Stored outputs, reruns, retries, and traceable failures are explicit Phase 4 requirements and protect the reliability of later insight features.

**Independent Test**: Can be tested by starting successful analyses, no-data analyses, failed analyses, retried analyses, and reruns for the same period, then verifying status, timing, input references, output, and failure details.

**Acceptance Scenarios**:

1. **Given** the user requests analysis, **When** processing begins, **Then** a traceable combined analysis run exists with the selected period, period granularity, status, request time, and source data summary.
2. **Given** analysis completes successfully, **When** the user reviews run history, **Then** the output, completion time, source record counts, and analysis instruction version are visible.
3. **Given** analysis fails, **When** the user reviews the run, **Then** the failure status, retry count, failure reason, and latest known stage are visible.
4. **Given** a failed combined analysis run is retried, **When** retry processing completes, **Then** the retry outcome is linked to the original run and does not create duplicate current results.
5. **Given** the user reruns analysis for a period that already has a completed result, **When** the rerun completes, **Then** the new result is stored as a separate run while preserving earlier run history.

### Edge Cases

- If the selected day or week has no saved tracking records, the system must mark the run `completed`, record output outcome `no_data`, and avoid producing AI-generated claims.
- If imported rows were invalid, skipped, or failed, they must not contribute to analysis inputs unless they became valid saved tracking records.
- If tags are absent from some tasks, the analysis must still run using available task, duration, and category data.
- If a task has multiple tags, analysis evidence must make the multi-tag interpretation clear when tag totals are discussed.
- If a category, tag, or task name is unusually long, the analysis output must remain readable and must not drop the associated tracked-time evidence.
- If saved tasks include note text, note text must be excluded from AI analysis inputs and generated outputs.
- If a selected week contains days with no tracked tasks between tracked days, the weekly analysis must represent those gaps honestly without inventing missing activity.
- If saved tracking records change after a previous analysis, a rerun must use the current saved records and preserve the earlier result as historical.
- If two combined analysis requests for the same period and granularity are made close together, the system must avoid conflicting current results and keep the run history understandable.
- If analysis processing takes longer than the initial request, the user must be able to check status without submitting the same request repeatedly.
- If an analysis retry occurs after a transient failure, the run must stop after no more than 3 total attempts, mark the run `failed` when all attempts fail, and preserve earlier failed attempt details.
- If analysis output is incomplete, malformed, or missing required sections, the run must not be marked as a successful completed analysis.
- If the AI service is unavailable or times out, the run must fail or retry with traceable failure details.
- If a generated observation is not supported by the selected period's data, it must be omitted or marked as unsupported rather than stored as a fact.
- If AI output conflicts with source productivity records, the saved daily logs, tasks, notes, categories, tags, and imports remain authoritative.
- If a user reviews older analysis history, the system must make it clear which completed result is the latest successful result for the period and period granularity.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST allow analysis to be requested for a single calendar day and for a full calendar week using saved daily tracking records.
- **FR-002**: The system MUST assemble a structured analysis input for the selected period that includes period boundaries, saved task names, tracked durations, categories, tags, and aggregate totals.
- **FR-002a**: The system MUST exclude note text from AI analysis inputs and generated outputs.
- **FR-003**: Analysis inputs MUST include only valid saved tracking records and MUST exclude invalid, skipped, or failed import rows that did not become saved records.
- **FR-004**: If a selected period has no saved tracking records, the system MUST complete the analysis run with output outcome `no_data` instead of generating summary, pattern, or insight claims.
- **FR-005**: The system MUST maintain named and versioned combined analysis instructions for daily analysis and weekly analysis so outputs can be traced to the instruction set used.
- **FR-006**: A daily summary MUST include the selected date, total tracked time, task count, dominant categories or tags when present, and concise narrative observations grounded in that day's records.
- **FR-007**: A weekly summary MUST include the selected week, daily tracked-time distribution, task count, category or tag themes, recurring task themes, and notable changes across the week when supported by data.
- **FR-008**: Pattern detection MUST identify repeated or concentrated categories, tags, task themes, tracked-time distributions, and notable outliers when the selected data supports them.
- **FR-009**: Behavior insights MUST remain observational and evidence-based in this phase; productivity scores, consistency scores, best/worst day labels, and recommendations are outside Phase 4.
- **FR-010**: Each completed daily or weekly analysis run MUST produce one combined output with structured sections for summary, detected patterns, behavior insights, supporting evidence, limitations, and generated timestamp.
- **FR-011**: Each detected pattern or behavior insight MUST include supporting evidence from the selected period, such as source dates, task counts, categories, tags, or tracked-time totals.
- **FR-012**: The system MUST avoid storing unsupported claims as completed insights when the selected data does not provide evidence for them.
- **FR-013**: The system MUST store each analysis attempt as a traceable combined analysis run with period granularity, selected period, status, request time, requester, source record references, aggregate input summary, instruction version, completion time when available, output when successful, retry count, and failure details when applicable.
- **FR-013a**: The system MUST NOT retain the full structured AI input payload after the analysis run records its source references, aggregate input summary, instruction version, output, and run metadata.
- **FR-014**: Analysis processing MUST be able to continue after the initial request returns, and users MUST be able to check run status later.
- **FR-015**: Analysis runs MUST use the shared run status vocabulary `pending`, `processing`, `completed`, `completed_with_errors`, and `failed`.
- **FR-015a**: No-data analysis requests MUST use run status `completed` with output outcome `no_data`.
- **FR-016**: The system MUST retry transient analysis failures up to 3 total attempts per run and preserve each failed attempt's traceability.
- **FR-016a**: If all retry attempts fail, the system MUST mark the analysis run `failed` with final failure details.
- **FR-017**: Retrying an analysis run MUST NOT create duplicate current outputs for the same run.
- **FR-018**: The user MUST be able to rerun combined analysis for the same period and period granularity.
- **FR-019**: Rerunning analysis MUST create a new run and preserve previous completed and failed runs for audit history.
- **FR-020**: When multiple successful runs exist for the same period and period granularity, the system MUST clearly identify the latest successful result as the current result.
- **FR-021**: The system MUST validate generated output before marking an analysis run completed.
- **FR-022**: Failed analysis runs MUST retain enough information for the user or maintainer to understand what failed without requiring access to raw temporary processing state.
- **FR-023**: Analysis history MUST remain reviewable by period, period granularity, status, and completion time.
- **FR-024**: AI analysis MUST write separate analysis outputs only and MUST NOT mutate source daily logs, tasks, notes, categories, tags, imports, or import outcomes.
- **FR-025**: Phase 4 MUST cover the AI analysis engine only; CSV import, dashboard visualization, productivity scoring, recommendation generation, scheduled automation, AI chat, report export, and Notion API synchronization are outside this phase.

### Key Entities *(include if feature involves data)*

- **AI Analysis Request**: A user-initiated request to run combined analysis for a specific day or week.
- **AIInsightRun**: A traceable combined analysis attempt with status, selected period, period granularity, request and completion timing, source record references, aggregate input summary, instruction version, output, retry count, and failure details.
- **Analysis Input Summary**: The retained audit summary for a run, including source record references, source record counts, aggregate totals, category and tag summaries, and instruction version while excluding note text and the full structured AI input payload.
- **Analysis Instruction Version**: The named version of the analysis guidance used to produce the result, allowing future runs to be compared against older outputs.
- **Daily Summary**: A completed analysis output for one calendar date, grounded in that day's saved tasks and totals.
- **Weekly Summary**: A completed analysis output for one calendar week, grounded in the week's saved daily logs and task records.
- **Output Outcome**: The result classification inside a completed output, including `analysis_generated` when analysis content is produced and `no_data` when the selected period has no saved tracking records.
- **Detected Pattern**: An evidence-backed observation about repeated or concentrated categories, tags, task themes, tracked-time distribution, or notable outliers.
- **Behavior Insight**: A neutral interpretation of detected patterns that explains observed behavior without turning it into a recommendation or score.
- **Supporting Evidence**: Source facts used to justify a summary, pattern, or insight, such as dates, durations, task counts, categories, or tags.
- **Run Failure Detail**: Traceable information about a failed run or failed attempt, including stage, reason, retry count, and final status.
- **Current Analysis Result**: The latest successful completed run for a period and period granularity, while older runs remain available as history.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of requested analyses for periods with saved records create a traceable analysis run with status visible within 5 seconds of the request.
- **SC-002**: 100% of completed daily analyses include total tracked time, task count, and at least one grounded observation when the selected day contains enough data to support one.
- **SC-003**: 100% of completed weekly analyses include daily tracked-time distribution, category or tag themes, and recurring patterns when the selected week contains enough data to support them.
- **SC-004**: 100% of no-data periods produce a no-data outcome and zero fabricated summary, pattern, or insight claims.
- **SC-005**: 100% of stored patterns and behavior insights include supporting evidence from the selected period.
- **SC-006**: 100% of malformed or incomplete AI outputs are rejected from successful completion and recorded as failed or retryable outcomes.
- **SC-007**: 100% of transient analysis failures stop after no more than 3 total attempts and preserve the failed attempt history.
- **SC-008**: Rerunning analysis for a period with an existing successful result creates a separate run and preserves 100% of previous run history.
- **SC-009**: A user can identify the latest successful result, prior runs, run status, and failure details for a period and granularity in under 2 minutes.
- **SC-010**: At least 95% of analyses for a week containing up to 7 days of personal tracking data complete or reach a traceable failure state within 2 minutes.
- **SC-011**: A reviewer can verify in under 10 minutes that Phase 4 does not include CSV import, dashboard visualization changes, productivity scores, recommendations, scheduled automation, AI chat, report export, or Notion API synchronization.

## Assumptions

- Phase 1 domain records, Phase 2 import traceability, and Phase 3 dashboard read models exist before Phase 4 implementation begins.
- The v1 product remains a personal single-owner tracker.
- Calendar days use the user's local tracked dates from source records.
- Weekly analysis uses Monday-to-Sunday calendar weeks, consistent with the Phase 3 dashboard assumptions.
- Saved tracking records are the source of truth for analysis; import history is used only for traceability and exclusion of unsaved rows.
- AI analysis inputs include task names, durations, categories, and tags, but exclude note text as a privacy boundary.
- After a run records source references and aggregate input summary, the full structured AI input payload is not retained.
- Source productivity records remain authoritative if they conflict with generated AI output.
- Reruns create new analysis runs instead of overwriting prior run history.
- The latest successful run is the default current result for a period and period granularity.
- Phase 4 insights are observational; prescriptive recommendations and scoring belong to Phase 5.
- Scheduled analysis belongs to Phase 6 and is not included in this phase.
- The existing docs/Plan.md Phase 4 section is the authoritative input for this specification.
