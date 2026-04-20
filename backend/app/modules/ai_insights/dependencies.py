from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.modules.ai_insights.services.ai_analysis_service import AIAnalysisService
from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator
from app.modules.ai_insights.services.consistency_scoring_service import ConsistencyScoringService
from app.modules.ai_insights.services.day_ranking_service import DayRankingService
from app.modules.ai_insights.services.insight_generation_service import InsightGenerationService
from app.modules.ai_insights.services.insight_result_service import InsightResultService
from app.modules.ai_insights.services.insight_source_service import InsightSourceService
from app.modules.ai_insights.services.insight_validation_service import InsightValidationService
from app.modules.ai_insights.services.productivity_scoring_service import ProductivityScoringService
from app.modules.ai_insights.services.recommendation_service import RecommendationService
from app.modules.ai_insights.providers.base import AIAnalysisProvider
from app.modules.ai_insights.providers.configured import get_configured_ai_provider


def _enqueue_analysis_run_after_commit(session: AsyncSession, ai_insight_run_id, owner_id) -> object:
    def enqueue() -> object:
        from app.workers.tasks.ai_analysis_tasks import process_ai_analysis_run

        return process_ai_analysis_run.delay(str(ai_insight_run_id), str(owner_id))

    session.info.setdefault("after_commit_callbacks", []).append(enqueue)
    return {"queued_after_commit": True}


def get_ai_insight_run_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AIInsightRunRepository:
    return AIInsightRunRepository(session)


def get_ai_insight_result_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AIInsightResultRepository:
    return AIInsightResultRepository(session)


def get_ai_insight_run_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    repository: Annotated[AIInsightRunRepository, Depends(get_ai_insight_run_repository)],
) -> AIInsightRunService:
    return AIInsightRunService(
        repository,
        enqueue_analysis_run=lambda ai_insight_run_id, owner_id: _enqueue_analysis_run_after_commit(
            session,
            ai_insight_run_id,
            owner_id,
        ),
    )


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


def get_insight_source_service(
    run_repository: Annotated[AIInsightRunRepository, Depends(get_ai_insight_run_repository)],
) -> InsightSourceService:
    return InsightSourceService(run_repository)


def get_productivity_scoring_service() -> ProductivityScoringService:
    return ProductivityScoringService()


def get_consistency_scoring_service() -> ConsistencyScoringService:
    return ConsistencyScoringService()


def get_day_ranking_service() -> DayRankingService:
    return DayRankingService()


def get_recommendation_service() -> RecommendationService:
    return RecommendationService()


def get_insight_validation_service() -> InsightValidationService:
    return InsightValidationService()


def get_insight_generation_service(
    result_repository: Annotated[AIInsightResultRepository, Depends(get_ai_insight_result_repository)],
    source_service: Annotated[InsightSourceService, Depends(get_insight_source_service)],
    productivity_scoring_service: Annotated[ProductivityScoringService, Depends(get_productivity_scoring_service)],
    consistency_scoring_service: Annotated[ConsistencyScoringService, Depends(get_consistency_scoring_service)],
    day_ranking_service: Annotated[DayRankingService, Depends(get_day_ranking_service)],
    recommendation_service: Annotated[RecommendationService, Depends(get_recommendation_service)],
    validation_service: Annotated[InsightValidationService, Depends(get_insight_validation_service)],
) -> InsightGenerationService:
    return InsightGenerationService(
        result_repository,
        source_service,
        productivity_scoring_service,
        consistency_scoring_service,
        day_ranking_service,
        recommendation_service,
        validation_service,
    )


def get_insight_result_service(
    result_repository: Annotated[AIInsightResultRepository, Depends(get_ai_insight_result_repository)],
    generation_service: Annotated[InsightGenerationService, Depends(get_insight_generation_service)],
) -> InsightResultService:
    return InsightResultService(result_repository, generation_service)
