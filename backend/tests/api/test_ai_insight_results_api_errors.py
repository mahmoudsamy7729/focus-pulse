import pytest


@pytest.mark.asyncio
async def test_generate_result_returns_missing_source_analysis_error(api_client) -> None:
    response = await api_client.post(
        "/api/v1/ai-insights/results/generate",
        json={"period_granularity": "daily", "anchor_date": "2026-04-15"},
    )

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "SOURCE_ANALYSIS_MISSING"
