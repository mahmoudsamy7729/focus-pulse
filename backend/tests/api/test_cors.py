import pytest


@pytest.mark.asyncio
async def test_cors_preflight_allows_local_frontend_origin(api_client) -> None:
    response = await api_client.options(
        "/api/v1/analytics/dashboard",
        headers={
            "Origin": "http://127.0.0.1:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://127.0.0.1:3000"
