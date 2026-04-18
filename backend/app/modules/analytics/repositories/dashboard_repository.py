from datetime import date
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.analytics.schemas import DashboardTaskRow
from app.modules.daily_logs.models import DailyLog
from app.modules.tasks.models import Category, Task


class DashboardRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def latest_tracked_day(self, owner_id: UUID) -> date | None:
        result = await self.session.execute(
            select(func.max(DailyLog.log_date))
            .join(Task, Task.daily_log_id == DailyLog.id)
            .join(Category, Category.id == Task.category_id)
            .where(
                DailyLog.owner_id == owner_id,
                Task.owner_id == owner_id,
                Category.owner_id == owner_id,
                DailyLog.deleted_at.is_(None),
                Task.deleted_at.is_(None),
                Category.deleted_at.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def list_task_rows(self, owner_id: UUID, start_date: date, end_date: date) -> list[DashboardTaskRow]:
        result = await self.session.execute(
            select(
                Task.id,
                DailyLog.log_date,
                Task.title,
                Task.time_spent_minutes,
                Category.name,
                Task.tags,
                Task.source,
            )
            .join(DailyLog, Task.daily_log_id == DailyLog.id)
            .join(Category, Category.id == Task.category_id)
            .where(
                DailyLog.owner_id == owner_id,
                Task.owner_id == owner_id,
                Category.owner_id == owner_id,
                DailyLog.log_date >= start_date,
                DailyLog.log_date <= end_date,
                DailyLog.deleted_at.is_(None),
                Task.deleted_at.is_(None),
                Category.deleted_at.is_(None),
            )
            .order_by(DailyLog.log_date, Task.created_at, Task.id)
        )
        return [
            DashboardTaskRow(
                id=task_id,
                log_date=log_date,
                title=title,
                time_spent_minutes=minutes,
                category=category_name,
                tags=list(tags or []),
                source=source,
            )
            for task_id, log_date, title, minutes, category_name, tags, source in result.all()
        ]
