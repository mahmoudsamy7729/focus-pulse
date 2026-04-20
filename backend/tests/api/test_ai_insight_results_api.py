from datetime import date
from uuid import UUID

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.ai_insights.models import AIInsightRun
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_ai_insight_results_api_generate_current_history_detail_and_rerun(api_client, async_session) -> None:
    run = AIInsightRun(
        owner_id=DEFAULT_OWNER_ID,
        target_period_type="daily",
        period_start=date(2026, 4, 15),
        period_end=date(2026, 4, 15),
        status=RunStatus.COMPLETED.value,
        source_summary={
            "period_granularity": "daily",
            "period_start": "2026-04-15",
            "period_end": "2026-04-15",
            "daily_log_count": 1,
            "task_count": 2,
            "total_minutes": 120,
            "category_totals": [{"label": "Build", "total_minutes": 120}],
            "daily_totals": [{"date": "2026-04-15", "total_minutes": 120}],
            "excluded_fields": ["note_text"],
        },
        output_summary={
            "output_outcome": "analysis_generated",
            "generated_at": "2026-04-15T00:00:00Z",
            "detected_patterns": [{"text": "Build work was the strongest category.", "evidence_ids": ["category-1"]}],
            "behavior_insights": [],
            "supporting_evidence": [],
        },
        output_outcome="analysis_generated",
        failure_details=[],
    )
    async_session.add(run)
    await async_session.flush()

    generated = await api_client.post(
        "/api/v1/ai-insights/results/generate",
        json={"period_granularity": "daily", "anchor_date": "2026-04-15"},
    )

    assert generated.status_code == 201
    body = generated.json()
    assert body["success"] is True
    result_id = UUID(body["data"]["result"]["id"])
    assert body["data"]["result"]["source_snapshot"]["excluded_fields"] == ["note_text"]

    current = await api_client.get("/api/v1/ai-insights/results/current?period_granularity=daily&anchor_date=2026-04-15")
    detail = await api_client.get(f"/api/v1/ai-insights/results/{result_id}")
    history = await api_client.get("/api/v1/ai-insights/results?period_granularity=daily")
    rerun = await api_client.post(f"/api/v1/ai-insights/results/{result_id}/rerun")

    assert current.json()["data"]["current_result"]["id"] == str(result_id)
    assert detail.json()["data"]["id"] == str(result_id)
    assert history.json()["data"]["total"] >= 1
    assert rerun.status_code == 201
