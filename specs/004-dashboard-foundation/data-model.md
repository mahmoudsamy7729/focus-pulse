# Data Model: Dashboard Foundation

Phase 3 does not introduce new persistent tables by default. It defines read models and aggregate value objects derived from active `DailyLog`, `Task`, `Category`, and `Note` records created in previous phases.

## Shared Rules

- All dashboard calculations include only active records where `deleted_at` is absent.
- The source of truth for durations remains `Task.time_spent_minutes`.
- User-facing durations are displayed in hours-and-minutes format while minute values remain available for sorting, totals, and tests.
- Week periods use Monday-to-Sunday ranges.
- Month periods use full calendar months.
- Initial dashboard load uses the latest tracked day for the current owner when any active tracked data exists.

## DashboardPeriod

**Purpose**: Describes the active day, week, or month shown by the dashboard.

**Fields**:

- `period_type`: `day`, `week`, or `month`.
- `anchor_date`: date supplied by the user or resolved from the latest tracked day.
- `start_date`: first date included in the period.
- `end_date`: last date included in the period.
- `label`: user-readable period label.

**Validation Rules**:

- `period_type` must be one of `day`, `week`, or `month`.
- Day periods have the same `start_date` and `end_date`.
- Week periods cover exactly seven calendar days.
- Month periods cover the full calendar month containing `anchor_date`.

## DashboardSummary

**Purpose**: Summary metrics for the selected period.

**Fields**:

- `total_minutes`: total active task duration in the period.
- `display_total`: hours-and-minutes display value.
- `task_count`: active task count.
- `daily_log_count`: count of daily logs with at least one active task in the period.
- `highest_time_category`: nullable category summary with name and minutes.
- `average_minutes_per_logged_day`: nullable average for week and month views.

**Validation Rules**:

- Totals must include only valid saved tracking records.
- `average_minutes_per_logged_day` is calculated over logged days only, not empty calendar dates.
- `highest_time_category` is null when the period has no tracked tasks.

## DailyLogListItem

**Purpose**: A row in the dashboard period list.

**Fields**:

- `date`: calendar date.
- `total_minutes`: total active task duration for the date.
- `display_total`: hours-and-minutes display value.
- `task_count`: active task count for the date.
- `top_category`: nullable highest-time category for the date.

**Validation Rules**:

- One list item exists per active daily log with active tasks in the selected period.
- Rows are ordered by date ascending for week and month period context.
- Duplicate active daily logs for one date are treated as a data quality error and must not appear as separate real days.

## PeriodTimeTimelinePoint

**Purpose**: Chart-ready daily total for week and month filters.

**Fields**:

- `date`: calendar date.
- `total_minutes`: tracked minutes for that date.
- `display_total`: hours-and-minutes display value.
- `has_tasks`: boolean.

**Validation Rules**:

- Week and month timelines include each calendar date in the selected period.
- Dates with no tracked tasks use `total_minutes: 0` and `has_tasks: false`.
- Zero-value timeline points must not create fake task records.

## CategoryBreakdownItem

**Purpose**: Chart/list item showing tracked time by category.

**Fields**:

- `label`: category display name, or `Other` for grouped chart data.
- `total_minutes`: tracked minutes.
- `display_total`: hours-and-minutes display value.
- `share_of_total`: decimal share of selected period tracked time.
- `is_other`: boolean.

**Validation Rules**:

- Category breakdown totals reconcile to the selected period total.
- Items are ordered by tracked time descending before top-10 grouping.
- Charts show the top 10 contributors and one `Other` item when more contributors exist.
- Categories with no tracked time in the selected period are excluded.

## TagBreakdownItem

**Purpose**: Chart/list item showing tracked time by tag.

**Fields**:

- `label`: tag value, `untagged`, or `Other`.
- `total_minutes`: tracked minutes credited to the tag bucket.
- `display_total`: hours-and-minutes display value.
- `share_label`: readable comparison text.
- `is_untagged`: boolean.
- `is_other`: boolean.

**Validation Rules**:

- Tasks with an empty tag list contribute to `untagged`.
- Multi-tag tasks contribute their full duration once to each tag.
- Because multi-tag tasks can make tag totals exceed period total, tag responses must include a notice when this occurs.
- Tag charts show the top 10 contributors and one `Other` item when more contributors exist.

## DashboardOverview

**Purpose**: Complete payload for the dashboard overview route.

**Fields**:

- `period`: `DashboardPeriod`.
- `summary`: `DashboardSummary`.
- `daily_logs`: list of `DailyLogListItem`.
- `period_timeline`: list of `PeriodTimeTimelinePoint`.
- `category_breakdown`: list of `CategoryBreakdownItem`.
- `tag_breakdown`: list of `TagBreakdownItem`.
- `tag_total_notice`: nullable message explaining multi-tag counting.
- `empty_state`: nullable empty-state code/message.

**Validation Rules**:

- All child collections reflect the same `period`.
- Empty selected periods return empty lists and an empty-state message rather than misleading charts.
- No invalid, skipped, or failed import rows contribute unless they created valid saved tracking records.

## DayDetail

**Purpose**: Read-only day detail payload used by the dashboard.

**Fields**:

- `date`: selected date.
- `total_minutes`: total active task duration for the day.
- `display_total`: hours-and-minutes display value.
- `task_count`: active task count.
- `tasks`: list of `TaskTimelineItem`.
- `empty_state`: nullable empty-state code/message.

**Validation Rules**:

- If the day has no active daily log or active tasks, return a valid empty day detail payload.
- Tasks are ordered by source/import order when available and saved order as fallback.
- Soft-deleted tasks and notes are excluded.

## TaskTimelineItem

**Purpose**: A task displayed in the day detail timeline.

**Fields**:

- `id`: task UUID.
- `title`: display task name.
- `time_spent_minutes`: exact duration.
- `display_time`: hours-and-minutes display value.
- `category`: category display name.
- `tags`: normalized tag values.
- `note`: nullable task note content.
- `source`: source label.
- `timeline_position`: stable zero-based or one-based position used for rendering order.

**Validation Rules**:

- `time_spent_minutes` must be positive.
- Empty tag lists render as no tags without placeholder noise.
- Empty notes render as absent.
- Timeline ordering must be stable across repeated reads of unchanged data.

## Frontend Query State

**Purpose**: Client-side state used to request dashboard data.

**Fields**:

- `period_type`: `day`, `week`, or `month`.
- `anchor_date`: selected date.
- `selected_day`: nullable date for day detail.

**Validation Rules**:

- Server state is fetched through TanStack Query using keys that include `period_type` and `anchor_date`.
- Client state stores only lightweight UI selections; API response data is not duplicated in a global store.
