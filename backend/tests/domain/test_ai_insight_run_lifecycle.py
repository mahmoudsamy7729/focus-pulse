from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.exceptions import InvalidAIInsightStatusTransitionError
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_ai_insight_status_transition_and_rerun_history(async_session) -> None:
    service = AIInsightRunService(AIInsightRunRepository(async_session))
    daily_log_id = uuid4()
    ai_run = await service.create_ai_insight_run(
        uuid4(),
        "daily",
        date(2026, 4, 15),
        date(2026, 4, 15),
        [daily_log_id],
    )

    await service.mark_ai_run_processing(ai_run.id)
    await service.complete_ai_run(ai_run.id, RunStatus.COMPLETED.value, {"summary": "ok"})
    rerun = await service.create_rerun(ai_run.id)

    assert ai_run.status == RunStatus.COMPLETED.value
    assert rerun.id != ai_run.id
    assert rerun.sources[0].daily_log_id == daily_log_id


@pytest.mark.asyncio
async def test_failed_ai_run_requires_failure_reason(async_session) -> None:
    service = AIInsightRunService(AIInsightRunRepository(async_session))
    ai_run = await service.create_ai_insight_run(uuid4(), "daily", date(2026, 4, 15), date(2026, 4, 15), [])
    await service.mark_ai_run_processing(ai_run.id)

    with pytest.raises(InvalidAIInsightStatusTransitionError):
        await service.complete_ai_run(ai_run.id, RunStatus.FAILED.value)
