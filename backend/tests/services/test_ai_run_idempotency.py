from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.exceptions import AIInsightConflictError
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService


@pytest.mark.asyncio
async def test_ai_run_idempotency_reuses_existing_and_conflicts_without_key(async_session) -> None:
    owner_id = uuid4()
    queued: list[tuple] = []
    service = AIInsightRunService(AIInsightRunRepository(async_session), enqueue_analysis_run=lambda *args: queued.append(args))

    first = await service.request_analysis_run(owner_id, "daily", date(2026, 4, 15), idempotency_key="abc12345")
    second = await service.request_analysis_run(owner_id, "daily", date(2026, 4, 15), idempotency_key="abc12345")

    assert second.ai_insight_run_id == first.ai_insight_run_id
    assert second.reused_existing is True
    with pytest.raises(AIInsightConflictError):
        await service.request_analysis_run(owner_id, "daily", date(2026, 4, 15))
    assert len(queued) == 1
