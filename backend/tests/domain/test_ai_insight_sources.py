from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService


@pytest.mark.asyncio
async def test_ai_insight_sources_do_not_mutate_daily_logs(async_session) -> None:
    owner_id = uuid4()
    daily_log_service = DailyLogService(DailyLogRepository(async_session))
    daily_log = await daily_log_service.get_or_create_daily_log(owner_id, date(2026, 4, 15))

    await AIInsightRunService(AIInsightRunRepository(async_session)).create_ai_insight_run(
        owner_id,
        "daily",
        date(2026, 4, 15),
        date(2026, 4, 15),
        [daily_log.id],
    )

    loaded = await daily_log_service.get_or_create_daily_log(owner_id, date(2026, 4, 15))
    assert loaded.id == daily_log.id
    assert loaded.deleted_at is None
