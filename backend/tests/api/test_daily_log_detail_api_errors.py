from uuid import UUID

import pytest

from app.api.dependencies import CurrentOwner, get_current_owner
from app.main import app


@pytest.mark.asyncio
async def test_day_detail_api_returns_validation_error_for_invalid_date(api_client) -> None:
    response = await api_client.get("/api/v1/daily-logs/not-a-date")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "REQUEST_VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_day_detail_api_returns_permission_error_when_scope_missing(api_client) -> None:
    async def owner_without_daily_log_scope() -> CurrentOwner:
        return CurrentOwner(owner_id=UUID("00000000-0000-4000-8000-000000000001"), scopes=frozenset())

    app.dependency_overrides[get_current_owner] = owner_without_daily_log_scope
    response = await api_client.get("/api/v1/daily-logs/2026-04-15")

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "DAILY_LOGS_PERMISSION_DENIED"
