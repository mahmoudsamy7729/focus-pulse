from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService


@pytest.mark.asyncio
async def test_ai_insight_repository_loads_sources_for_traceability(async_session) -> None:
    repository = AIInsightRunRepository(async_session)
    service = AIInsightRunService(repository)
    source_id = uuid4()
    ai_run = await service.create_ai_insight_run(
        uuid4(),
        "daily",
        date(2026, 4, 15),
        date(2026, 4, 15),
        [source_id],
    )
    await async_session.commit()

    loaded = await repository.get(ai_run.id)

    assert loaded is not None
    assert loaded.sources[0].daily_log_id == source_id
