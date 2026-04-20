from datetime import date

import pytest

from app.modules.ai_insights.constants import InsightGenerationReason
from app.modules.ai_insights.repositories.ai_insight_result_repository import AIInsightResultRepository
from app.modules.ai_insights.services.insight_result_service import InsightResultService


@pytest.mark.asyncio
async def test_result_service_period_resolution_supports_default_generation_boundary(async_session) -> None:
    service = InsightResultService(AIInsightResultRepository(async_session), None)  # type: ignore[arg-type]

    period_start, period_end = service.resolve_period("weekly", date(2026, 4, 15))

    assert period_start == date(2026, 4, 13)
    assert period_end == date(2026, 4, 19)
    assert InsightGenerationReason.DEFAULT_GENERATE.value == "default_generate"
