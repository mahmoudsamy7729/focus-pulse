from datetime import UTC, date, datetime
from uuid import uuid4

import pytest

from app.modules.ai_insights.models import AIInsightResult, AIInsightRun
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_result_repository_current_lookup_and_history_exclude_soft_deleted(async_session) -> None:
    owner_id = uuid4()
    run = AIInsightRun(
        owner_id=owner_id,
        target_period_type="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        status=RunStatus.COMPLETED.value,
        source_summary={},
        output_summary={"output_outcome": "no_data", "generated_at": "2026-04-15T00:00:00Z"},
        output_outcome="no_data",
        failure_details=[],
    )
    async_session.add(run)
    await async_session.flush()
    repository = AIInsightResultRepository(async_session)
    result = await repository.add(
        AIInsightResult(
            owner_id=owner_id,
            period_granularity="daily",
            period_start=date(2026, 4, 15),
            period_end=date(2026, 4, 15),
            source_ai_insight_run_id=run.id,
            status="completed",
            is_current=True,
            generation_reason="default_generate",
            source_snapshot={
                "period_granularity": "daily",
                "period_start": "2026-04-15",
                "period_end": "2026-04-15",
                "source_ai_insight_run_id": str(run.id),
                "daily_log_count": 0,
                "tracked_day_count": 0,
                "task_count": 0,
                "total_minutes": 0,
                "included_fields": [],
                "excluded_fields": ["note_text"],
            },
            productivity_score={
                "score_type": "productivity",
                "state": "insufficient_data",
                "score": None,
                "confidence": "low",
                "summary": "No data",
                "positive_factors": [],
                "limiting_factors": [],
                "evidence_ids": [],
                "insufficient_data_reason": "No data",
            },
            recommendations=[],
            evidence=[],
            validation_outcome={"passed": True, "checked_at": "2026-04-15T00:00:00Z", "validator_version": "test", "checks": [], "failure_codes": []},
            generated_at=datetime.now(UTC),
        )
    )

    current = await repository.find_current(owner_id, "daily", date(2026, 4, 15), date(2026, 4, 15))
    items, total = await repository.list_for_owner(owner_id, page=1, limit=20)

    assert current is not None and current.id == result.id
    assert total == 1
    assert items[0].id == result.id
