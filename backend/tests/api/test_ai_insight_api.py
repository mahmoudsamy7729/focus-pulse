from datetime import date
from uuid import UUID

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.main import app
from app.modules.ai_insights.dependencies import get_ai_insight_run_service
from app.modules.ai_insights.repositories.ai_insight_run_repository import AIInsightRunRepository
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_ai_insight_api_create_get_history_current_and_rerun(api_client, async_session) -> None:
    queued: list[tuple] = []

    def override_service() -> AIInsightRunService:
        return AIInsightRunService(AIInsightRunRepository(async_session), enqueue_analysis_run=lambda *args: queued.append(args))

    app.dependency_overrides[get_ai_insight_run_service] = override_service
    response = await api_client.post(
        "/api/v1/ai-insights/runs",
        headers={"Idempotency-Key": "abc12345"},
        json={"period_granularity": "daily", "anchor_date": "2026-04-15"},
    )

    body = response.json()
    assert response.status_code == 202
    assert body["success"] is True
    run_id = body["data"]["ai_insight_run_id"]
    assert queued

    service = override_service()
    run = await AIInsightRunRepository(async_session).get_for_owner(DEFAULT_OWNER_ID, UUID(run_id))
    await service.mark_ai_run_processing(run.id)
    await service.complete_ai_run(
        run.id,
        RunStatus.COMPLETED.value,
        {
            "output_outcome": "no_data",
            "generated_at": "2026-04-15T00:00:00Z",
            "summary": None,
            "detected_patterns": [],
            "behavior_insights": [],
            "supporting_evidence": [],
            "limitations": [],
        },
        output_outcome="no_data",
    )

    detail = await api_client.get(f"/api/v1/ai-insights/runs/{run_id}")
    history = await api_client.get("/api/v1/ai-insights/runs")
    current = await api_client.get("/api/v1/ai-insights/runs/current?period_granularity=daily&anchor_date=2026-04-15")
    rerun = await api_client.post(f"/api/v1/ai-insights/runs/{run_id}/rerun")

    assert detail.status_code == 200
    assert detail.json()["data"]["output_outcome"] == "no_data"
    assert history.json()["data"]["total"] == 1
    assert current.json()["data"]["current_run"]["id"] == run_id
    assert rerun.status_code == 202


@pytest.mark.asyncio
async def test_ai_insight_api_idempotency_reuse(api_client, async_session) -> None:
    def override_service() -> AIInsightRunService:
        return AIInsightRunService(AIInsightRunRepository(async_session), enqueue_analysis_run=lambda *_: None)

    app.dependency_overrides[get_ai_insight_run_service] = override_service
    payload = {"period_granularity": "daily", "anchor_date": date(2026, 4, 15).isoformat()}
    first = await api_client.post("/api/v1/ai-insights/runs", headers={"Idempotency-Key": "abc12345"}, json=payload)
    second = await api_client.post("/api/v1/ai-insights/runs", headers={"Idempotency-Key": "abc12345"}, json=payload)

    assert first.status_code == 202
    assert second.status_code == 202
    assert second.json()["data"]["reused_existing"] is True
