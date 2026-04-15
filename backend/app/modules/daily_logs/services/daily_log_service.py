from datetime import date
from uuid import UUID

from app.modules.daily_logs.exceptions import InvalidDailyLogRangeError
from app.modules.daily_logs.models import DailyLog
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository


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

    async def list_daily_logs_by_range(
        self,
        owner_id: UUID,
        start_date: date,
        end_date: date,
    ) -> list[DailyLog]:
        if start_date > end_date:
            raise InvalidDailyLogRangeError("start_date must be on or before end_date")
        return await self.repository.list_by_range(owner_id, start_date, end_date)
