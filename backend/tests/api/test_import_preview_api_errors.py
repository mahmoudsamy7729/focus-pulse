import pytest


@pytest.mark.asyncio
async def test_preview_api_returns_error_envelope_for_missing_required_columns(api_client) -> None:
    response = await api_client.post(
        "/api/v1/imports/csv/preview",
        files={"file": ("tasks.csv", b"date,task\n2026-04-15,Plan\n", "text/csv")},
    )

    body = response.json()
    assert response.status_code == 400
    assert body["success"] is False
    assert body["error"]["code"] == "CSV_VALIDATION_ERROR"
    assert "missing required columns" in body["error"]["message"]
