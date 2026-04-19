from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_ai_repository_finds_idempotent_in_flight_current_and_history(async_session) -> None:
    owner_id = uuid4()
    repository = AIInsightRunRepository(async_session)
    service = AIInsightRunService(repository)
    run = await service.create_ai_insight_run(
        owner_id,
        "daily",
        date(2026, 4, 15),
        date(2026, 4, 15),
        [],
        idempotency_key="abc12345",
    )

    assert await repository.find_by_idempotency_key(owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15), "abc12345")
    assert await repository.find_in_flight(owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15))

    await service.mark_ai_run_processing(run.id)
    await service.complete_ai_run(
        run.id,
        RunStatus.COMPLETED.value,
        {"output_outcome": "no_data", "generated_at": "2026-04-15T00:00:00Z"},
        output_outcome="no_data",
    )

    current = await repository.find_current_result(owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15))
    items, total = await repository.list_for_owner(owner_id, page=1, limit=20)

    assert current is not None
    assert total == 1
    assert items[0].id == run.id
