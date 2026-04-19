from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.exceptions import AIProviderFailureError
from app.modules.ai_insights.providers.base import AIProviderRequest, AIProviderResponse, DeterministicAIAnalysisProvider
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_analysis_service import AIAnalysisService
from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.ai_insights.services.ai_instruction_service import AIInstructionService
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.modules.ai_insights.services.ai_output_validator import AIOutputValidator
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


class FlakyProvider:
    def __init__(self) -> None:
        self.calls = 0
        self.delegate = DeterministicAIAnalysisProvider()

    async def generate_analysis(self, request: AIProviderRequest) -> AIProviderResponse:
        self.calls += 1
        if self.calls == 1:
            raise AIProviderFailureError("temporary outage", transient=True)
        return await self.delegate.generate_analysis(request)


async def _seed_task(async_session, owner_id):
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(owner_id, date(2026, 4, 15))
    await TaskService(TaskRepository(async_session), CategoryRepository(async_session)).create_task(
        owner_id,
        daily_log,
        "Plan roadmap",
        30,
        "Work",
        ["planning"],
    )


@pytest.mark.asyncio
async def test_ai_analysis_service_completes_generated_and_no_data_runs(async_session) -> None:
    owner_id = uuid4()
    await _seed_task(async_session, owner_id)
    repository = AIInsightRunRepository(async_session)
    run_service = AIInsightRunService(repository)
    run = await run_service.create_ai_insight_run(owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15), [])
    empty = await run_service.create_ai_insight_run(owner_id, "daily", date(2026, 4, 16), date(2026, 4, 16), [])
    service = AIAnalysisService(
        repository,
        AIInputService(DailyLogRepository(async_session)),
        AIInstructionService(),
        DeterministicAIAnalysisProvider(),
        AIOutputValidator(),
    )

    await service.process_analysis_run(run.id)
    await service.process_analysis_run(empty.id)

    loaded = await repository.get(run.id)
    empty_loaded = await repository.get(empty.id)
    assert loaded.output_outcome == "analysis_generated"
    assert empty_loaded.output_outcome == "no_data"
    assert "Plan roadmap" not in str(loaded.source_summary)


@pytest.mark.asyncio
async def test_ai_analysis_service_retries_transient_provider_failure(async_session) -> None:
    owner_id = uuid4()
    await _seed_task(async_session, owner_id)
    repository = AIInsightRunRepository(async_session)
    run = await AIInsightRunService(repository).create_ai_insight_run(
        owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15), []
    )
    provider = FlakyProvider()
    service = AIAnalysisService(
        repository,
        AIInputService(DailyLogRepository(async_session)),
        AIInstructionService(),
        provider,
        AIOutputValidator(),
    )

    await service.process_analysis_run(run.id)
    loaded = await repository.get(run.id)

    assert provider.calls == 2
    assert loaded.retry_count == 1
    assert loaded.status == "completed"
