from calendar import monthrange
from collections import defaultdict
from datetime import date, timedelta
from uuid import UUID

from app.modules.analytics.constants import (
    CHART_BUCKET_LIMIT,
    NO_PERIOD_DATA,
    NO_TRACKED_DATA,
    PERIOD_DAY,
    PERIOD_MONTH,
    PERIOD_TYPES,
    PERIOD_WEEK,
)
from app.modules.analytics.exceptions import InvalidDashboardPeriodError
from app.modules.analytics.repositories.dashboard_repository import DashboardRepository
from app.modules.analytics.schemas import (
    CategoryBreakdownItem,
    DailyLogListItem,
    DashboardOverview,
    DashboardPeriod,
    DashboardSummary,
    EmptyState,
    NamedTimeTotal,
    PeriodTimeTimelinePoint,
    TagBreakdownItem,
)


def format_minutes(total_minutes: int) -> str:
    minutes = max(0, int(total_minutes))
    hours, remainder = divmod(minutes, 60)
    if hours == 0:
        return f"{remainder}m"
    if remainder == 0:
        return f"{hours}h"
    return f"{hours}h {remainder}m"


class DashboardService:
    def __init__(self, repository: DashboardRepository) -> None:
        self.repository = repository

    async def get_dashboard_overview(
        self,
        owner_id: UUID,
        period_type: str = PERIOD_DAY,
        anchor_date: date | None = None,
    ) -> DashboardOverview:
        if period_type not in PERIOD_TYPES:
            raise InvalidDashboardPeriodError(f"Unsupported period_type: {period_type}")

        latest_tracked_day = await self.repository.latest_tracked_day(owner_id)
        resolved_anchor = anchor_date or latest_tracked_day or date.today()
        period = self._resolve_period(period_type, resolved_anchor)
        rows = await self.repository.list_task_rows(owner_id, period.start_date, period.end_date)

        empty_state = None
        if not rows:
            empty_state = EmptyState(
                code=NO_TRACKED_DATA if latest_tracked_day is None else NO_PERIOD_DATA,
                message=(
                    "No tracked data is available yet."
                    if latest_tracked_day is None
                    else "No tracked tasks were found for this period."
                ),
            )

        return DashboardOverview(
            period=period,
            summary=self._summary(rows, period.period_type),
            daily_logs=self._daily_logs(rows),
            period_timeline=self._timeline(rows, period.start_date, period.end_date),
            category_breakdown=self._category_breakdown(rows),
            tag_breakdown=self._tag_breakdown(rows),
            tag_total_notice=self._tag_total_notice(rows),
            empty_state=empty_state,
        )

    def _resolve_period(self, period_type: str, anchor_date: date) -> DashboardPeriod:
        if period_type == PERIOD_DAY:
            start_date = end_date = anchor_date
            label = f"{anchor_date:%b} {anchor_date.day}, {anchor_date.year}"
        elif period_type == PERIOD_WEEK:
            start_date = anchor_date - timedelta(days=anchor_date.weekday())
            end_date = start_date + timedelta(days=6)
            label = f"{start_date.isoformat()} to {end_date.isoformat()}"
        else:
            start_date = anchor_date.replace(day=1)
            end_date = anchor_date.replace(day=monthrange(anchor_date.year, anchor_date.month)[1])
            label = anchor_date.strftime("%B %Y")

        return DashboardPeriod(
            period_type=period_type,  # type: ignore[arg-type]
            anchor_date=anchor_date,
            start_date=start_date,
            end_date=end_date,
            label=label,
        )

    def _summary(self, rows, period_type: str) -> DashboardSummary:
        total_minutes = sum(row.time_spent_minutes for row in rows)
        task_count = len(rows)
        logged_days = {row.log_date for row in rows}
        category_totals = self._category_totals(rows)
        highest = self._named_total(max(category_totals.items(), key=lambda item: (item[1], item[0])), allow_none=True)
        average = None
        if period_type in {PERIOD_WEEK, PERIOD_MONTH} and logged_days:
            average = round(total_minutes / len(logged_days))
        return DashboardSummary(
            total_minutes=total_minutes,
            display_total=format_minutes(total_minutes),
            task_count=task_count,
            daily_log_count=len(logged_days),
            highest_time_category=highest,
            average_minutes_per_logged_day=average,
        )

    def _daily_logs(self, rows) -> list[DailyLogListItem]:
        by_day: dict[date, list] = defaultdict(list)
        for row in rows:
            by_day[row.log_date].append(row)

        items: list[DailyLogListItem] = []
        for log_date in sorted(by_day):
            day_rows = by_day[log_date]
            category_totals = self._category_totals(day_rows)
            top_category = self._named_total(
                max(category_totals.items(), key=lambda item: (item[1], item[0])),
                allow_none=True,
            )
            total_minutes = sum(row.time_spent_minutes for row in day_rows)
            items.append(
                DailyLogListItem(
                    date=log_date,
                    total_minutes=total_minutes,
                    display_total=format_minutes(total_minutes),
                    task_count=len(day_rows),
                    top_category=top_category,
                )
            )
        return items

    def _timeline(self, rows, start_date: date, end_date: date) -> list[PeriodTimeTimelinePoint]:
        totals: dict[date, int] = defaultdict(int)
        for row in rows:
            totals[row.log_date] += row.time_spent_minutes

        points = []
        current = start_date
        while current <= end_date:
            total_minutes = totals[current]
            points.append(
                PeriodTimeTimelinePoint(
                    date=current,
                    total_minutes=total_minutes,
                    display_total=format_minutes(total_minutes),
                    has_tasks=total_minutes > 0,
                )
            )
            current += timedelta(days=1)
        return points

    def _category_breakdown(self, rows) -> list[CategoryBreakdownItem]:
        total_minutes = sum(row.time_spent_minutes for row in rows)
        totals = self._category_totals(rows)
        grouped = self._top_with_other(totals)
        return [
            CategoryBreakdownItem(
                label=label,
                total_minutes=minutes,
                display_total=format_minutes(minutes),
                share_of_total=round(minutes / total_minutes, 4) if total_minutes else 0,
                is_other=label == "Other",
            )
            for label, minutes in grouped
        ]

    def _tag_breakdown(self, rows) -> list[TagBreakdownItem]:
        total_minutes = sum(row.time_spent_minutes for row in rows)
        totals: dict[str, int] = defaultdict(int)
        for row in rows:
            tags = row.tags or ["untagged"]
            for tag in tags:
                totals[tag or "untagged"] += row.time_spent_minutes

        grouped = self._top_with_other(totals)
        return [
            TagBreakdownItem(
                label=label,
                total_minutes=minutes,
                display_total=format_minutes(minutes),
                share_label=f"{round((minutes / total_minutes) * 100)}% of tracked time" if total_minutes else "0%",
                is_untagged=label == "untagged",
                is_other=label == "Other",
            )
            for label, minutes in grouped
        ]

    def _tag_total_notice(self, rows) -> str | None:
        total_minutes = sum(row.time_spent_minutes for row in rows)
        tagged_total = sum(row.time_spent_minutes * max(1, len(row.tags or [])) for row in rows)
        if tagged_total > total_minutes:
            return "Tag totals may exceed total tracked time because multi-tag tasks count once for each tag."
        return None

    @staticmethod
    def _category_totals(rows) -> dict[str, int]:
        totals: dict[str, int] = defaultdict(int)
        for row in rows:
            totals[row.category] += row.time_spent_minutes
        return totals

    @staticmethod
    def _top_with_other(totals: dict[str, int]) -> list[tuple[str, int]]:
        ordered = sorted(totals.items(), key=lambda item: (-item[1], item[0].lower()))
        if len(ordered) <= CHART_BUCKET_LIMIT:
            return ordered
        visible = ordered[:CHART_BUCKET_LIMIT]
        other_total = sum(minutes for _, minutes in ordered[CHART_BUCKET_LIMIT:])
        return [*visible, ("Other", other_total)]

    @staticmethod
    def _named_total(item: tuple[str, int] | None, *, allow_none: bool = False) -> NamedTimeTotal | None:
        if item is None:
            return None if allow_none else NamedTimeTotal(label="", total_minutes=0, display_total="0m")
        label, minutes = item
        return NamedTimeTotal(label=label, total_minutes=minutes, display_total=format_minutes(minutes))
