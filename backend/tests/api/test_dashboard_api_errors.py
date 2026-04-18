from uuid import UUID

import pytest
from fastapi import status

from app.api.dependencies import CurrentOwner, get_current_owner
from app.core.exceptions import AppError
from app.main import app
from app.modules.analytics.dependencies import get_dashboard_service


@pytest.mark.asyncio
async def test_dashboard_api_returns_invalid_period_error(api_client) -> None:
    response = await api_client.get("/api/v1/analytics/dashboard?period_type=year")

    assert response.status_code == 400
    assert response.json()["error"]["code"] == "DASHBOARD_INVALID_PERIOD"


@pytest.mark.asyncio
async def test_dashboard_api_returns_permission_error_when_scope_missing(api_client) -> None:
    async def owner_without_dashboard_scope() -> CurrentOwner:
        return CurrentOwner(owner_id=UUID("00000000-0000-4000-8000-000000000001"), scopes=frozenset())

    app.dependency_overrides[get_current_owner] = owner_without_dashboard_scope
    response = await api_client.get("/api/v1/analytics/dashboard")

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "ANALYTICS_PERMISSION_DENIED"


@pytest.mark.asyncio
async def test_dashboard_api_preserves_rate_limit_error_envelope(api_client) -> None:
    class RateLimitedDashboardService:
        async def get_dashboard_overview(self, *args, **kwargs):
            raise AppError(
                "DASHBOARD_RATE_LIMITED",
                "Too many dashboard requests.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                details={"limit": 60, "window": "1 minute"},
            )

    app.dependency_overrides[get_dashboard_service] = lambda: RateLimitedDashboardService()
    response = await api_client.get("/api/v1/analytics/dashboard")
    body = response.json()

    assert response.status_code == 429
    assert body["success"] is False
    assert body["error"]["code"] == "DASHBOARD_RATE_LIMITED"
    assert body["error"]["details"]["limit"] == 60
