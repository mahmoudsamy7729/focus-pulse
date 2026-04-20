from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.models import AIInsightRun
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.consistency_scoring_service import ConsistencyScoringService
from app.modules.ai_insights.services.day_ranking_service import DayRankingService
from app.modules.ai_insights.services.insight_generation_service import InsightGenerationService
from app.modules.ai_insights.services.insight_source_service import InsightSourceService
from app.modules.ai_insights.services.insight_validation_service import InsightValidationService
from app.modules.ai_insights.services.productivity_scoring_service import ProductivityScoringService
from app.modules.ai_insights.services.recommendation_service import RecommendationService
from app.shared.enums.run_status import RunStatus


def _service(async_session) -> InsightGenerationService:
    run_repository = AIInsightRunRepository(async_session)
    return InsightGenerationService(
        AIInsightResultRepository(async_session),
        InsightSourceService(run_repository),
        ProductivityScoringService(),
        ConsistencyScoringService(),
        DayRankingService(),
        RecommendationService(),
        InsightValidationService(),
    )


@pytest.mark.asyncio
async def test_generation_creates_current_result_and_reuses_default(async_session) -> None:
    owner_id = uuid4()
    run = AIInsightRun(
        owner_id=owner_id,
        target_period_type="weekly",
        period_start=date(2026, 4, 13),
        period_end=date(2026, 4, 19),
        status=RunStatus.COMPLETED.value,
        source_summary={
            "period_granularity": "weekly",
            "period_start": "2026-04-13",
            "period_end": "2026-04-19",
            "daily_log_count": 3,
            "task_count": 5,
            "total_minutes": 300,
            "category_totals": [{"label": "Build", "total_minutes": 200}],
            "daily_totals": [
                {"date": "2026-04-13", "total_minutes": 180},
                {"date": "2026-04-14", "total_minutes": 90},
                {"date": "2026-04-15", "total_minutes": 30},
            ],
            "excluded_fields": ["note_text"],
        },
        output_summary={
            "output_outcome": "analysis_generated",
            "generated_at": "2026-04-19T00:00:00Z",
            "detected_patterns": [{"text": "Build work dominated the week.", "evidence_ids": ["category-1"]}],
            "behavior_insights": [],
            "supporting_evidence": [],
        },
        output_outcome="analysis_generated",
        failure_details=[],
    )
    async_session.add(run)
    await async_session.flush()
    service = _service(async_session)

    created = await service.generate(owner_id, "weekly", date(2026, 4, 13), date(2026, 4, 19))
    reused = await service.generate(owner_id, "weekly", date(2026, 4, 13), date(2026, 4, 19))

    assert created.reused_existing is False
    assert created.result.is_current is True
    assert created.result.productivity_score.state == "scored"
    assert reused.reused_existing is True
    assert reused.result.id == created.result.id
