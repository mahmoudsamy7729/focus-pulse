import asyncio
from uuid import UUID

from app.core.database import AsyncSessionLocal
from app.modules.ai_insights.providers.configured import get_configured_ai_provider
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_analysis_service import AIAnalysisService
from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.workers.celery_app import celery_app


async def process_ai_analysis_run_payload(ai_insight_run_id: UUID, owner_id: UUID) -> dict[str, object]:
    _ = owner_id
    async with AsyncSessionLocal() as session:
        service = AIAnalysisService(
            AIInsightRunRepository(session),
            AIInputService(DailyLogRepository(session)),
            AIInstructionService(),
            get_configured_ai_provider(),
            AIOutputValidator(),
        )
        result = await service.process_analysis_run(ai_insight_run_id)
        await session.commit()
        return result


if celery_app is not None:

    @celery_app.task(name="ai_insights.process_analysis_run")
    def process_ai_analysis_run(ai_insight_run_id: str, owner_id: str) -> dict[str, object]:
        return asyncio.run(process_ai_analysis_run_payload(UUID(ai_insight_run_id), UUID(owner_id)))

else:

    class _ProcessAIAnalysisRunFallback:
        def delay(self, ai_insight_run_id: str, owner_id: str) -> dict[str, object]:
            return {
                "queued": False,
                "ai_insight_run_id": ai_insight_run_id,
                "owner_id": owner_id,
            }

    process_ai_analysis_run = _ProcessAIAnalysisRunFallback()
