from datetime import date
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.daily_logs.models import DailyLog
from app.modules.notes.models import Note
from app.modules.tasks.models import Task


class DailyLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _active_query() -> Select[tuple[DailyLog]]:
        return select(DailyLog).where(DailyLog.deleted_at.is_(None))

    async def get_by_owner_and_date(self, owner_id: UUID, log_date: date) -> DailyLog | None:
        result = await self.session.execute(
            self._active_query().where(DailyLog.owner_id == owner_id, DailyLog.log_date == log_date)
        )
        return result.scalar_one_or_none()

    async def add(self, daily_log: DailyLog) -> DailyLog:
        self.session.add(daily_log)
        await self.session.flush()
        return daily_log

    async def get_with_entries(self, owner_id: UUID, log_date: date) -> DailyLog | None:
        result = await self.session.execute(
            self._active_query()
            .where(DailyLog.owner_id == owner_id, DailyLog.log_date == log_date)
            .options(
                selectinload(DailyLog.tasks.and_(Task.deleted_at.is_(None))).selectinload(Task.category),
                selectinload(DailyLog.tasks.and_(Task.deleted_at.is_(None))).selectinload(
                    Task.note.and_(Note.deleted_at.is_(None))
                ),
            )
        )
        return result.scalar_one_or_none()

    async def list_by_range(self, owner_id: UUID, start_date: date, end_date: date) -> list[DailyLog]:
        result = await self.session.execute(
            self._active_query()
            .where(
                DailyLog.owner_id == owner_id,
                DailyLog.log_date >= start_date,
                DailyLog.log_date <= end_date,
            )
            .order_by(DailyLog.log_date)
            .options(selectinload(DailyLog.tasks.and_(Task.deleted_at.is_(None))).selectinload(Task.category))
        )
        return list(result.scalars().unique())
