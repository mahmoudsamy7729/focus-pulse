from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.analytics.repositories.dashboard_repository import DashboardRepository
from app.modules.analytics.services.dashboard_service import DashboardService


def get_dashboard_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> DashboardRepository:
    return DashboardRepository(session)


def get_dashboard_service(
    repository: Annotated[DashboardRepository, Depends(get_dashboard_repository)],
) -> DashboardService:
    return DashboardService(repository)
