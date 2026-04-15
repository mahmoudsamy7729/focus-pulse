from datetime import date
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.daily_logs.models import DailyLog
from app.modules.tasks.models import Category, Task


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _active_query() -> Select[tuple[Category]]:
        return select(Category).where(Category.deleted_at.is_(None))

    async def get_by_normalized_name(self, owner_id: UUID, normalized_name: str) -> Category | None:
        result = await self.session.execute(
            self._active_query().where(
                Category.owner_id == owner_id,
                Category.normalized_name == normalized_name,
            )
        )
        return result.scalar_one_or_none()

    async def add(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        return category


class TaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _active_query() -> Select[tuple[Task]]:
        return select(Task).where(Task.deleted_at.is_(None))

    async def add(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.flush()
        return task

    async def get_import_duplicate(
        self,
        owner_id: UUID,
        log_date: date,
        normalized_title: str,
        time_spent_minutes: int,
    ) -> Task | None:
        result = await self.session.execute(
            self._active_query()
            .join(DailyLog, Task.daily_log_id == DailyLog.id)
            .where(
                Task.owner_id == owner_id,
                DailyLog.owner_id == owner_id,
                DailyLog.log_date == log_date,
                DailyLog.deleted_at.is_(None),
                Task.normalized_title == normalized_title,
                Task.time_spent_minutes == time_spent_minutes,
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def calculate_totals(self, owner_id: UUID, start_date: date, end_date: date) -> dict[str, object]:
        result = await self.session.execute(
            select(DailyLog.log_date, Category.name, Task.tags, Task.time_spent_minutes)
            .join(Task, Task.daily_log_id == DailyLog.id)
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
        )

        by_day: dict[str, int] = {}
        by_category: dict[str, int] = {}
        by_tag: dict[str, int] = {}
        total_minutes = 0
        for log_date, category_name, tags, minutes in result.all():
            day_key = log_date.isoformat()
            by_day[day_key] = by_day.get(day_key, 0) + minutes
            by_category[category_name] = by_category.get(category_name, 0) + minutes
            for tag in tags or []:
                by_tag[tag] = by_tag.get(tag, 0) + minutes
            total_minutes += minutes

        return {
            "total_minutes": total_minutes,
            "by_day": by_day,
            "by_category": by_category,
            "by_tag": by_tag,
        }

    async def count_for_category(self, category_id: UUID) -> int:
        result = await self.session.execute(
            select(func.count(Task.id)).where(Task.category_id == category_id, Task.deleted_at.is_(None))
        )
        return int(result.scalar_one())
