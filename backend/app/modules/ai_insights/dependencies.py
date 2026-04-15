from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService


def get_ai_insight_run_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AIInsightRunRepository:
    return AIInsightRunRepository(session)


def get_ai_insight_run_service(
    repository: Annotated[AIInsightRunRepository, Depends(get_ai_insight_run_repository)],
) -> AIInsightRunService:
    return AIInsightRunService(repository)
