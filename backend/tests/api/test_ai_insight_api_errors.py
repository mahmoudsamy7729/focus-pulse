import pytest

from app.api.dependencies import CurrentOwner, get_current_owner
from app.main import app
from app.modules.ai_insights.dependencies import get_ai_insight_run_service
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService


@pytest.mark.asyncio
async def test_ai_insight_api_validation_conflict_and_not_found(api_client, async_session) -> None:
    def override_service() -> AIInsightRunService:
        return AIInsightRunService(AIInsightRunRepository(async_session), enqueue_analysis_run=lambda *_: None)

    app.dependency_overrides[get_ai_insight_run_service] = override_service
    invalid = await api_client.post(
        "/api/v1/ai-insights/runs",
        json={"period_granularity": "monthly", "anchor_date": "2026-04-15"},
    )
    first = await api_client.post(
        "/api/v1/ai-insights/runs",
        json={"period_granularity": "daily", "anchor_date": "2026-04-15"},
    )
    conflict = await api_client.post(
        "/api/v1/ai-insights/runs",
        json={"period_granularity": "daily", "anchor_date": "2026-04-15"},
    )
    not_found = await api_client.get("/api/v1/ai-insights/runs/00000000-0000-4000-8000-000000000999")

    assert invalid.status_code == 400
    assert first.status_code == 202
    assert conflict.status_code == 409
    assert not_found.status_code == 404


@pytest.mark.asyncio
async def test_ai_insight_api_permission_error(api_client) -> None:
    async def limited_owner():
        return CurrentOwner(
            owner_id=__import__("uuid").UUID("00000000-0000-4000-8000-000000000001"),
            scopes=frozenset(),
        )

    app.dependency_overrides[get_current_owner] = limited_owner
    response = await api_client.get("/api/v1/ai-insights/runs")

    assert response.status_code == 403
