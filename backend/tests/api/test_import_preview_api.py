import pytest


@pytest.mark.asyncio
async def test_preview_api_returns_success_envelope_and_normalized_payload(api_client) -> None:
    response = await api_client.post(
        "/api/v1/imports/csv/preview",
        files={
            "file": (
                "tasks.csv",
                b"date,task,category,time_spent_minutes,tags,notes\n2026-04-15,Plan,Work,30,Deep,Useful\n",
                "text/csv",
            )
        },
    )

    body = response.json()
    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["valid_row_count"] == 1
    assert body["data"]["valid_rows"][0]["date"] == "2026-04-15"
    assert body["data"]["valid_rows"][0]["tags"] == ["deep"]
