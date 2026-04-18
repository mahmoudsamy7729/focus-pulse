from datetime import date
from uuid import UUID

from app.modules.daily_logs.exceptions import InvalidDailyLogRangeError
from app.modules.daily_logs.models import DailyLog
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.schemas import DayDetail, TaskTimelineItem
from app.modules.analytics.constants import NO_DAY_DETAIL_DATA
from app.modules.analytics.schemas import EmptyState
from app.modules.analytics.services.dashboard_service import format_minutes


class DailyLogService:
    def __init__(self, repository: DailyLogRepository) -> None:
        self.repository = repository

    async def get_or_create_daily_log(self, owner_id: UUID, log_date: date, source: str = "manual") -> DailyLog:
        existing = await self.repository.get_by_owner_and_date(owner_id, log_date)
        if existing is not None:
            return existing
        return await self.repository.add(DailyLog(owner_id=owner_id, log_date=log_date, source=source))

    async def get_daily_log_with_entries(self, owner_id: UUID, log_date: date) -> DailyLog | None:
        return await self.repository.get_with_entries(owner_id, log_date)

    async def get_day_detail(self, owner_id: UUID, log_date: date) -> DayDetail:
        daily_log = await self.repository.get_with_entries(owner_id, log_date)
        if daily_log is None:
            return self._empty_day_detail(log_date)

        active_tasks = [
            task
            for task in daily_log.tasks
            if task.deleted_at is None and task.category is not None and task.category.deleted_at is None
        ]
        active_tasks.sort(key=lambda task: (task.created_at, str(task.id)))
        if not active_tasks:
            return self._empty_day_detail(log_date)

        items = [
            TaskTimelineItem(
                id=task.id,
                title=task.title,
                time_spent_minutes=task.time_spent_minutes,
                display_time=format_minutes(task.time_spent_minutes),
                category=task.category.name,
                tags=list(task.tags or []),
                note=task.note.content if task.note is not None and task.note.deleted_at is None else None,
                source=task.source,
                timeline_position=index,
            )
            for index, task in enumerate(active_tasks)
        ]
        total_minutes = sum(item.time_spent_minutes for item in items)
        return DayDetail(
            date=log_date,
            total_minutes=total_minutes,
            display_total=format_minutes(total_minutes),
            task_count=len(items),
            tasks=items,
        )

    async def list_daily_logs_by_range(
        self,
        owner_id: UUID,
        start_date: date,
        end_date: date,
    ) -> list[DailyLog]:
        if start_date > end_date:
            raise InvalidDailyLogRangeError("start_date must be on or before end_date")
        return await self.repository.list_by_range(owner_id, start_date, end_date)

    @staticmethod
    def _empty_day_detail(log_date: date) -> DayDetail:
        return DayDetail(
            date=log_date,
            total_minutes=0,
            display_total="0m",
            task_count=0,
            tasks=[],
            empty_state=EmptyState(code=NO_DAY_DETAIL_DATA, message="No tracked tasks were found for this day."),
        )
