# Feature Specification: Dashboard Foundation

**Feature Branch**: `004-dashboard-foundation`  
**Created**: 2026-04-18  
**Status**: Draft  
**Input**: User description: "Read Plan.md inside docs folder and create specification for Phase 3 - Dashboard Foundation"

## Clarifications

### Session 2026-04-18

- Q: Which period should the dashboard open by default? -> A: Latest tracked day.
- Q: How should tasks be ordered in the day detail timeline? -> A: Source/import order, then saved order fallback.
- Q: How should tracked time be displayed in dashboard UI? -> A: Hours and minutes, e.g. `2h 15m`.
- Q: Which time chart should the dashboard use for selected periods? -> A: Daily totals timeline for week/month; hourly-style task timeline for day.
- Q: How should charts handle many categories or tags? -> A: Show top 10, group the rest as Other.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Review Productivity Overview (Priority: P1)

As the project owner, I want a dashboard overview of my tracked time for a selected day, week, or month, so I can quickly understand how my work time is distributed without reading every task individually.

**Why this priority**: The dashboard's core value is fast comprehension of daily tracking data. Summary totals and period filtering make the imported records usable.

**Independent Test**: Can be tested by opening the dashboard with existing daily tracking records, selecting day, week, and month periods, and verifying that the visible summaries, daily log list, and breakdowns match the selected period.

**Acceptance Scenarios**:

1. **Given** tracked tasks exist, **When** the user opens the dashboard without a previously selected period, **Then** the dashboard defaults to the latest tracked day and displays total tracked time in hours and minutes, task count, and the highest-time category for that day.
2. **Given** the dashboard is showing a day, **When** the user changes the filter to week or month, **Then** all visible summaries, daily log rows, category breakdowns, tag breakdowns, and charts update to the selected period.
3. **Given** a selected period contains multiple daily logs, **When** the overview is shown, **Then** the daily logs are listed with each date's total tracked time and task count.
4. **Given** the selected period contains a week or month of tracked tasks, **When** the dashboard is shown, **Then** the period visualization shows daily tracked-time totals across the selected period.
5. **Given** the selected period contains no tracked tasks, **When** the dashboard is shown, **Then** the user sees a clear empty state instead of zero-value charts that imply missing data is a system error.

---

### User Story 2 - Inspect a Single Day (Priority: P2)

As the project owner, I want to open a day from the dashboard and review its tasks in detail, so I can understand what happened on that specific date.

**Why this priority**: Day-level detail connects high-level summaries back to the actual source records that explain them.

**Independent Test**: Can be tested by selecting a daily log from the dashboard and verifying that the day detail view shows that day's tasks, durations, categories, tags, optional notes, and day total.

**Acceptance Scenarios**:

1. **Given** a daily log appears in the dashboard list, **When** the user selects it, **Then** the system displays a day detail view for that date.
2. **Given** the selected day has tracked tasks, **When** the day detail view is shown, **Then** every task for that day is visible in source or import order with task name, time spent in hours and minutes, category, tags when present, and note content when present.
3. **Given** the selected day has tracked tasks, **When** the day detail visualization is shown, **Then** the task timeline represents that day's tracked tasks in a day-focused timeline view.
4. **Given** a task has no tags or no note, **When** it is shown in day detail, **Then** the absence is represented cleanly without placeholder noise.
5. **Given** the user returns from day detail to the dashboard overview, **When** the overview is shown again, **Then** the previously selected period remains active.

---

### User Story 3 - Compare Categories and Tags (Priority: P3)

As the project owner, I want visual category and tag breakdowns for the selected period, so I can identify where my time is going and which labels dominate my work.

**Why this priority**: Category and tag analysis turns raw task records into actionable patterns while staying within the non-AI dashboard phase.

**Independent Test**: Can be tested by using sample records with multiple categories, tags, untagged tasks, and multiple selected periods, then verifying the breakdown totals, ordering, labels, and visual proportions.

**Acceptance Scenarios**:

1. **Given** the selected period includes tasks across multiple categories, **When** the dashboard is shown, **Then** the category breakdown displays each category's tracked time and share of period time.
2. **Given** the selected period includes tagged tasks, **When** the tag breakdown is shown, **Then** the dashboard displays tracked time by tag and clearly explains how multi-tag tasks are counted.
3. **Given** the selected period includes tasks without tags, **When** the tag breakdown is shown, **Then** untagged task time is still visible as untagged time.
4. **Given** the selected period contains more than 10 categories or tags, **When** category or tag charts are shown, **Then** the charts show the top 10 contributors and group the remaining contributors as Other.
5. **Given** categories or tags have long names, **When** they appear in breakdowns or charts, **Then** the labels remain readable and do not prevent the user from understanding totals.

### Edge Cases

- If there are no daily logs at all, the dashboard must show an initial empty state that directs the user toward importing data instead of trying to default to a tracked day.
- If the selected day, week, or month has no tracked tasks but other periods do, the dashboard must show an empty state for only the selected period and preserve navigation to other periods.
- If a selected week or month includes dates with no logs, those dates must not inflate task counts or tracked time.
- If a task has an empty tag list, its time must appear in the untagged portion of tag breakdowns.
- If a task has multiple tags, each tag receives the task's full duration in tag breakdowns, and the dashboard must label that tag totals may exceed total tracked time.
- If a category or tag has no tracked time in the selected period, it must not appear as an active breakdown item for that period.
- If more than 10 categories or tags exist in a selected period, the categories or tags outside the top 10 by tracked time must be grouped as Other in charts without losing their contribution to totals.
- If task, category, tag, or note text is long, the dashboard must keep the content readable without hiding the associated time values.
- If a tracked duration is less than one hour, it must still be displayed clearly in minutes using the dashboard's hours-and-minutes format.
- If two daily logs would represent the same calendar date, the dashboard must treat that as a data quality problem from earlier phases and avoid showing duplicate day rows as separate real days.
- If imported rows were invalid, skipped, or failed, they must not contribute to dashboard tracked-time totals unless they resulted in valid saved tracking records.
- If task source or import order is unavailable for a day, the day detail timeline must use saved order as a stable fallback.
- If a week or month contains dates with no tracked tasks between dates that do have tracked tasks, the daily totals timeline must make the zero-tracked dates understandable without adding fake task data.
- If new tracking records become available after an import completes, the dashboard must be able to reflect the updated records the next time the user views or refreshes the dashboard.
- If the user changes filters repeatedly, the dashboard must keep the final selected filter as the source of truth for visible summaries and details.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a dashboard where the user can review saved daily tracking records.
- **FR-002**: The dashboard MUST support day, week, and month period filters.
- **FR-003**: The dashboard MUST default to the latest tracked day when first opened, while still allowing the user to navigate to other days, weeks, and months.
- **FR-004**: Changing the selected period MUST update all visible dashboard summaries, daily log lists, breakdowns, and charts to the same selected period.
- **FR-005**: The dashboard MUST show period summary cards for total tracked time, total task count, and highest-time category when data exists.
- **FR-005a**: All user-facing tracked-time values in the dashboard MUST be displayed in hours-and-minutes format, while preserving minute-level accuracy.
- **FR-006**: For week and month views, the dashboard MUST include average tracked time per logged day.
- **FR-007**: The dashboard MUST show a daily logs list for the selected period, including date, total tracked time, task count, and the most significant category by time for each day.
- **FR-008**: The user MUST be able to select a day from the daily logs list and open a day detail view.
- **FR-009**: The day detail view MUST show the selected date, total tracked time, task count, and every task saved for that day.
- **FR-010**: Each day detail task MUST show task name, time spent, category, tags when present, and note content when present.
- **FR-011**: The day detail view MUST present tasks in source or import order when available, and MUST use saved order as a stable fallback when source or import order is unavailable.
- **FR-012**: The dashboard MUST show a category breakdown for the selected period with category name, tracked time, and share of total period time.
- **FR-013**: Category breakdown totals MUST reconcile to the selected period's total tracked time.
- **FR-014**: The dashboard MUST show a tag breakdown for the selected period with tag label, tracked time, and readable share or comparison information.
- **FR-015**: The tag breakdown MUST include untagged time for tasks with no tags.
- **FR-016**: The tag breakdown MUST clearly communicate that tasks with multiple tags are counted once for each tag.
- **FR-017**: Category and tag breakdowns MUST be ordered so the largest time contributors are easiest to identify.
- **FR-017a**: Category and tag charts MUST show the top 10 contributors by tracked time and group all remaining contributors as Other.
- **FR-017b**: The Other group MUST preserve the tracked-time contribution of grouped categories or tags in chart totals.
- **FR-018**: The dashboard MUST include visualizations for period time summary, category breakdown, and tag breakdown.
- **FR-018a**: For week and month filters, the period time visualization MUST show daily tracked-time totals across the selected period.
- **FR-018b**: For day filters and day detail, the time visualization MUST use a day-focused task timeline.
- **FR-019**: Visualizations MUST have text values or labels sufficient for the user to understand the data without relying only on color.
- **FR-020**: Empty states MUST be shown for no data, no tasks in selected period, no categories, and no tags.
- **FR-021**: Dashboard totals MUST include only valid saved tracking records and MUST exclude invalid, skipped, or failed import rows that did not become saved tracking records.
- **FR-022**: Dashboard navigation MUST allow the user to move between overview and day detail without losing the selected day, week, or month context.
- **FR-023**: Long task names, categories, tags, and notes MUST remain readable enough that time values and key labels are not obscured.
- **FR-024**: Phase 3 MUST cover dashboard read-only review and visualization only; CSV import flows, data editing, AI-generated insights, scheduled automation, report export, and Notion API synchronization are outside this phase.

### Key Entities *(include if feature involves data)*

- **Dashboard Period**: The active day, week, or month selected by the user. It determines which daily logs and tasks contribute to summaries and visualizations.
- **Dashboard Summary**: The aggregate view for a selected period, including total tracked time, task count, highest-time category, and average tracked time per logged day when applicable.
- **Daily Log List Item**: A dashboard row representing one calendar date with its total tracked time, task count, and most significant category.
- **Day Detail**: The read-only view for one calendar date, including day totals and the tasks saved for that date.
- **Task Timeline Item**: A task shown within a day detail view, including task name, time spent, category, tag list, optional note, and its stable position in source/import order or saved fallback order.
- **Category Breakdown**: A period-level grouping that shows how total tracked time is distributed across normalized categories.
- **Tag Breakdown**: A period-level grouping that shows how task time maps to tag labels, including untagged time and multi-tag counting behavior.
- **Other Group**: A chart bucket that combines categories or tags outside the top 10 contributors while preserving their tracked-time contribution.
- **Period Time Timeline**: A visualization that shows daily tracked-time totals for week and month filters.
- **Day Task Timeline**: A visualization that shows tasks for a selected day using the clarified timeline ordering rule.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can identify total tracked time, total task count, and highest-time category for the selected period within 30 seconds of opening the dashboard.
- **SC-002**: 100% of day, week, and month filter changes update summaries, daily log list, category breakdown, tag breakdown, and charts to the same selected period.
- **SC-003**: A user can open any visible daily log's detail view from the dashboard in no more than two interactions.
- **SC-004**: 100% of week and month time visualizations show daily tracked-time totals for the selected period.
- **SC-005**: 100% of day detail time visualizations show a day-focused task timeline.
- **SC-006**: 100% of category breakdowns reconcile to the selected period's total tracked time.
- **SC-007**: 100% of tag breakdowns show untagged time when untagged tasks exist and explain multi-tag counting when multi-tag tasks exist.
- **SC-008**: 100% of category and tag charts with more than 10 contributors show the top 10 contributors and an Other group without dropping tracked time from chart totals.
- **SC-009**: For one year of personal tracking data, visible dashboard results update within 2 seconds after a period filter change.
- **SC-010**: In usability review, at least 90% of primary dashboard tasks are completed without assistance: changing period, finding a day, opening day detail, and identifying the largest category.
- **SC-011**: A reviewer can verify in under 10 minutes that Phase 3 does not include CSV import processing, data editing, AI analysis, scheduled automation, report export, or Notion API synchronization.

## Assumptions

- Phase 1 domain records and Phase 2 imported tracking records are available before this dashboard phase is implemented.
- The v1 product remains a personal single-owner tracker.
- Calendar days use the user's local tracked dates from the source records.
- If no previous user selection exists, the initial dashboard period is the latest tracked day.
- Week filters use Monday-to-Sunday calendar weeks.
- Month filters use full calendar months.
- Dashboard data is read-only in this phase.
- The dashboard uses saved valid tracking records as its source of truth; import traceability records remain available to import history but are not part of dashboard time totals.
- The existing docs/Plan.md Phase 3 section is the authoritative input for this specification.
