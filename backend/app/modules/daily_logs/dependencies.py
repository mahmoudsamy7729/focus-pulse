from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService


def get_daily_log_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DailyLogRepository:
    return DailyLogRepository(session)


def get_daily_log_service(
    repository: Annotated[DailyLogRepository, Depends(get_daily_log_repository)],
) -> DailyLogService:
    return DailyLogService(repository)
