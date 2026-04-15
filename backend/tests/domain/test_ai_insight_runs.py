from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.exceptions import InvalidAIInsightTargetPeriodError
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService


@pytest.mark.asyncio
async def test_ai_insight_target_period_validation(async_session) -> None:
    service = AIInsightRunService(AIInsightRunRepository(async_session))

    await service.create_ai_insight_run(uuid4(), "daily", date(2026, 4, 15), date(2026, 4, 15), [])
    await service.create_ai_insight_run(uuid4(), "weekly", date(2026, 4, 13), date(2026, 4, 19), [])

    with pytest.raises(InvalidAIInsightTargetPeriodError):
        await service.create_ai_insight_run(uuid4(), "monthly", date(2026, 4, 1), date(2026, 4, 30), [])

    with pytest.raises(InvalidAIInsightTargetPeriodError):
        await service.create_ai_insight_run(uuid4(), "weekly", date(2026, 4, 13), date(2026, 4, 20), [])
