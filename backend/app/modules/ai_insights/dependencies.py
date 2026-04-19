from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.modules.ai_insights.services.ai_analysis_service import AIAnalysisService
from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator
from app.modules.ai_insights.providers.base import AIAnalysisProvider
from app.modules.ai_insights.providers.configured import get_configured_ai_provider


def get_ai_insight_run_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AIInsightRunRepository:
    return AIInsightRunRepository(session)


def _enqueue_analysis_run(ai_insight_run_id, owner_id) -> object:
    from app.workers.tasks.ai_analysis_tasks import process_ai_analysis_run

    return process_ai_analysis_run.delay(str(ai_insight_run_id), str(owner_id))


def get_ai_insight_run_service(
    repository: Annotated[AIInsightRunRepository, Depends(get_ai_insight_run_repository)],
) -> AIInsightRunService:
    return AIInsightRunService(repository, enqueue_analysis_run=_enqueue_analysis_run)


def get_ai_input_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> AIInputService:
    return AIInputService(DailyLogRepository(session))


def get_ai_instruction_service() -> AIInstructionService:
    return AIInstructionService()


def get_ai_output_validator() -> AIOutputValidator:
    return AIOutputValidator()


def get_ai_provider() -> AIAnalysisProvider:
    return get_configured_ai_provider()


def get_ai_analysis_service(
    repository: Annotated[AIInsightRunRepository, Depends(get_ai_insight_run_repository)],
    input_service: Annotated[AIInputService, Depends(get_ai_input_service)],
    instruction_service: Annotated[AIInstructionService, Depends(get_ai_instruction_service)],
    provider: Annotated[AIAnalysisProvider, Depends(get_ai_provider)],
    output_validator: Annotated[AIOutputValidator, Depends(get_ai_output_validator)],
) -> AIAnalysisService:
    return AIAnalysisService(repository, input_service, instruction_service, provider, output_validator)
