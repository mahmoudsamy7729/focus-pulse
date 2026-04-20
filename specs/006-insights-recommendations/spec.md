# Feature Specification: Insights & Recommendations

**Feature Branch**: `006-insights-recommendations`  
**Created**: 2026-04-20  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 5 - Insights & Recommendations"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Review Explainable Scores (Priority: P1)

As the project owner, I want each completed insight period to show a productivity score and a consistency score with plain-language explanations, so I can understand how the scores were derived and whether they are meaningful for my data.

**Why this priority**: Scores are the primary Phase 5 output. They must be understandable and evidence-backed before recommendations can be trusted.

**Independent Test**: Can be tested by generating insights for a week with completed analysis output and saved tracking records, then verifying that both scores are present, bounded, explained, and traceable to source facts.

**Acceptance Scenarios**:

1. **Given** a selected week has completed analysis output and enough saved tracking data, **When** the user requests insights, **Then** the system returns a productivity score from 0 to 100 with the main evidence that increased or decreased the score.
2. **Given** a selected week has completed analysis output and enough saved tracking data, **When** the user requests insights, **Then** the system returns a consistency score from 0 to 100 with the main evidence that increased or decreased the score.
3. **Given** the selected period lacks enough data for a meaningful score, **When** insights are generated, **Then** the system marks the affected score as insufficient data and explains what is missing instead of fabricating a score.
4. **Given** a user reviews a saved insight result later, **When** the score is displayed, **Then** the score explanation, supporting evidence, generated timestamp, and source analysis reference remain available.

---

### User Story 2 - Understand Best and Worst Days (Priority: P2)

As the project owner, I want the system to identify the strongest and weakest days in a selected week, so I can see which behaviors or contexts were associated with better or worse productivity outcomes.

**Why this priority**: Best and worst day identification turns scores into a useful comparison, while still keeping the feature grounded in observable data rather than generic advice.

**Independent Test**: Can be tested with a sample week containing varied daily activity, categories, tags, and AI observations, then verifying that the selected best and worst days are relative to that week and include supporting reasons.

**Acceptance Scenarios**:

1. **Given** a selected week contains at least three tracked days, **When** insights are generated, **Then** the system identifies the best day and worst day relative to that week with the evidence used for each label.
2. **Given** multiple days have similar evidence, **When** the system identifies best or worst days, **Then** it explains the tie or close ranking instead of overstating a difference.
3. **Given** a selected week has fewer than three tracked days, **When** insights are generated, **Then** the system avoids best/worst labels and explains that the comparison would not be reliable.
4. **Given** a day is labeled worst, **When** the result is shown, **Then** the language stays neutral and focuses on tracked patterns, not judgment or blame.

---

### User Story 3 - Receive Low-Noise Recommendations (Priority: P3)

As the project owner, I want a short set of actionable recommendations based on my scores and AI analysis, so I can decide what to change next without sorting through generic or repetitive advice.

**Why this priority**: Recommendations are the final Phase 5 value, but they are useful only when they are specific, evidence-backed, limited in number, and clearly tied to the user's own tracking history.

**Independent Test**: Can be tested by generating recommendations for periods with clear patterns, weak patterns, repeated prior recommendations, and insufficient data, then verifying that the output is concise, useful, and not noisy.

**Acceptance Scenarios**:

1. **Given** the selected period contains evidence-backed patterns, **When** recommendations are generated, **Then** the system returns no more than three prioritized recommendations with action, rationale, supporting evidence, confidence, and expected benefit.
2. **Given** the selected period does not support a useful recommendation, **When** recommendations are generated, **Then** the system returns no recommendation for that unsupported theme and explains that more data is needed when helpful.
3. **Given** a recommendation is similar to one already produced for the same source pattern, **When** recommendations are generated again, **Then** the system avoids duplicate wording and keeps the latest recommendation history understandable.
4. **Given** a user reviews recommendations later, **When** the result is displayed, **Then** each recommendation remains linked to the score factors, best/worst day evidence, or AI observations that supported it.

### Edge Cases

- If the selected period has no saved tracking records, the system must produce a no-data insight result with no scores, best/worst day labels, or recommendations.
- If Phase 4 analysis output is missing for the selected period, the system must explain that insights cannot be generated until analysis exists.
- If Phase 4 analysis output is incomplete, malformed, or marked as failed, the system must not generate successful insights from it.
- If saved tracking records changed after the source analysis was generated, the system must identify the source analysis used and avoid implying that insights reflect newer records.
- If a selected week has only one or two tracked days, consistency scoring and best/worst day comparisons must be marked as insufficient or low confidence.
- If every tracked day in a week has similar totals and patterns, the system must explain that no meaningful best/worst distinction was found.
- If a single outlier day dominates the week, the system must identify the outlier and avoid letting it create unsupported broad recommendations.
- If categories or tags are missing from some tasks, the system must still use available duration and task evidence without inventing missing labels.
- If AI observations conflict with saved tracking facts, saved tracking facts remain authoritative and unsupported AI observations must not drive scores or recommendations.
- If a recommendation would be generic, unsupported, repetitive, or unactionable, it must be omitted.
- If note text exists on source tasks, Phase 5 must preserve the Phase 4 privacy boundary and avoid using or reproducing note text.
- If multiple insight generations are requested for the same period and source analysis, the system must keep the current result clear and preserve prior result history.
- If generated scores or recommendations fail validation, the result must not be marked as successfully completed.
- If the user reviews an older result, the system must make clear which source period and source analysis produced it.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST generate an insight result for a selected calendar week using completed AI analysis output and saved tracking facts for that week.
- **FR-002**: The system MUST allow a selected calendar day to show day-level productivity scoring and recommendations when enough source analysis and saved tracking facts exist, while omitting best/worst day comparisons for single-day views.
- **FR-003**: The system MUST produce a productivity score on a 0 to 100 scale when the selected period has enough evidence to support the score.
- **FR-004**: The productivity score MUST include a plain-language explanation of the score factors, including the strongest positive factors and the strongest limiting factors.
- **FR-005**: The system MUST produce a consistency score on a 0 to 100 scale for multi-day periods when at least three tracked days are available.
- **FR-006**: The consistency score MUST explain the observed day-to-day pattern using tracked-time distribution, recurring categories or tags, task volume, and AI analysis observations when supported by data.
- **FR-007**: When data is insufficient for either score, the system MUST mark that score as insufficient data instead of producing a numeric score.
- **FR-008**: The system MUST identify the best day and worst day within a selected week only when at least three tracked days provide a meaningful comparison.
- **FR-009**: Best and worst day labels MUST be relative to the selected week and MUST include supporting reasons such as tracked time, task mix, category concentration, tag patterns, and relevant AI observations.
- **FR-010**: The system MUST use neutral language for weak days and recommendations, avoiding shame, blame, medical claims, or claims about the user's character.
- **FR-011**: The system MUST generate no more than three recommendations for a selected period.
- **FR-012**: Each recommendation MUST include a concrete action, the reason for the action, the supporting evidence, an expected benefit, and a confidence level.
- **FR-013**: Recommendations MUST be based on the selected period's saved tracking facts, completed AI analysis output, generated scores, or best/worst day evidence.
- **FR-014**: The system MUST omit recommendations that are generic, unsupported, duplicative, or not actionable.
- **FR-015**: The system MUST state when no useful recommendation can be made from the available data.
- **FR-016**: The system MUST preserve traceability from each insight result to the source period, source analysis result, source tracking summary, generated timestamp, score explanations, best/worst day evidence, and recommendations.
- **FR-017**: The system MUST validate generated insight results before marking them successful, including score bounds, required explanations, evidence references, recommendation count, and unsupported-claim checks.
- **FR-018**: The system MUST store insight results for later review and MUST preserve prior results when insights are regenerated.
- **FR-019**: When multiple successful insight results exist for the same period, the system MUST clearly identify the latest successful result as the current result.
- **FR-020**: Regenerating insights for the same period and same source analysis MUST avoid duplicate current results and keep history understandable.
- **FR-021**: The system MUST not mutate source daily logs, tasks, notes, categories, tags, imports, or Phase 4 analysis results when generating Phase 5 insights.
- **FR-022**: The system MUST preserve the existing privacy boundary by excluding task note text from Phase 5 inputs, explanations, and recommendations.
- **FR-023**: Phase 5 MUST cover scores, best/worst day identification, recommendations, explanations, result review, and traceability only; scheduled automation, CSV import, dashboard redesign, report export, Notion synchronization, and AI chat are outside this phase.

### Key Entities *(include if feature involves data)*

- **Insight Result**: A generated Phase 5 result for a selected period, containing score outcomes, best/worst day findings when applicable, recommendations, explanations, traceability, and generation metadata.
- **Source Analysis Result**: The completed Phase 4 analysis output used to generate scores and recommendations for the selected period.
- **Productivity Score**: A 0 to 100 outcome that summarizes productivity signals for a selected period, along with positive factors, limiting factors, evidence, and confidence.
- **Consistency Score**: A 0 to 100 outcome that summarizes how steady the user's tracked activity and work themes were across a multi-day period, with evidence and confidence.
- **Best Day Finding**: The strongest day within a selected week, relative to that week only, with reasons and supporting evidence.
- **Worst Day Finding**: The weakest day within a selected week, relative to that week only, with neutral explanation and supporting evidence.
- **Recommendation**: A concise suggested action with rationale, supporting evidence, confidence, expected benefit, priority, and source insight links.
- **Recommendation Set**: The complete prioritized list of recommendations for an insight result, capped to prevent noise.
- **Insight Evidence**: Source facts or AI observations used to justify scores, day findings, or recommendations.
- **Insight Validation Outcome**: The result of checking that generated scores and recommendations are complete, bounded, evidence-backed, non-duplicative, and safe to show.
- **Current Insight Result**: The latest successful insight result for a period, while earlier generated results remain available as history.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of successful weekly insight results include either a valid productivity score from 0 to 100 or an explicit insufficient-data reason.
- **SC-002**: 100% of successful multi-day insight results include either a valid consistency score from 0 to 100 or an explicit insufficient-data reason.
- **SC-003**: 100% of successful scores include at least two supporting evidence points when enough source data exists.
- **SC-004**: 100% of best/worst day labels include supporting reasons and are omitted when fewer than three tracked days are available.
- **SC-005**: 100% of successful recommendation sets contain between zero and three recommendations.
- **SC-006**: 100% of recommendations include a concrete action, rationale, supporting evidence, expected benefit, confidence level, and priority.
- **SC-007**: 0 unsupported, generic, or duplicate recommendations are included in successful insight results during validation testing.
- **SC-008**: A user can understand why each score and recommendation was generated in under 2 minutes by reading its explanation and evidence.
- **SC-009**: 100% of no-data or missing-analysis periods avoid fabricated scores, best/worst day labels, and recommendations.
- **SC-010**: 100% of regenerated insight results preserve previous result history and identify the latest successful result as current.
- **SC-011**: At least 90% of test users reviewing seeded sample insight results rate the recommendations as understandable and actionable.
- **SC-012**: A reviewer can verify in under 10 minutes that Phase 5 does not include scheduled automation, CSV import, dashboard redesign, report export, Notion synchronization, or AI chat.

## Assumptions

- Phase 1 saved tracking records, Phase 2 import traceability, Phase 3 dashboard views, and Phase 4 completed AI analysis outputs exist before Phase 5 implementation begins.
- The v1 product remains a personal single-owner productivity tracker.
- Calendar days use the user's local tracked dates from source records.
- Weekly insights use Monday-to-Sunday calendar weeks, consistent with earlier dashboard and analysis assumptions.
- Productivity and consistency scores are personal, evidence-based summaries for reflection; they are not absolute benchmarks, medical assessments, or judgments of personal worth.
- Best and worst days are relative labels within the selected week only.
- At least three tracked days are required for reliable weekly consistency scoring and best/worst day comparison.
- Recommendations should be limited to the highest-value actions supported by evidence, with no more than three recommendations per result.
- Saved tracking records remain authoritative if they conflict with generated AI analysis or generated insight text.
- Regenerating insights creates a new result and preserves previous insight history.
- The latest successful insight result is the default current result for a period.
- Phase 5 continues the Phase 4 privacy boundary: task names, durations, categories, and tags may be used, but note text is excluded.
- The existing docs/Plan.md Phase 5 section is the authoritative input for this specification.
