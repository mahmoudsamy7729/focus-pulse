import pytest
from uuid import UUID

from app.api.dependencies import CurrentOwner, get_current_owner
from app.main import app


@pytest.mark.asyncio
async def test_confirm_api_returns_validation_error_for_fully_invalid_file(api_client) -> None:
    response = await api_client.post(
        "/api/v1/imports/csv",
        files={"file": ("tasks.csv", b"date,task,category,time_spent_minutes\n,No Date,Work,30\n", "text/csv")},
    )

    body = response.json()
    assert response.status_code == 400
    assert body["success"] is False
    assert body["error"]["code"] == "CSV_VALIDATION_ERROR"


@pytest.mark.asyncio
async def test_confirm_api_returns_permission_error_when_scope_missing(api_client) -> None:
    async def owner_without_write_scope() -> CurrentOwner:
        return CurrentOwner(owner_id=UUID("00000000-0000-4000-8000-000000000001"), scopes=frozenset())

    app.dependency_overrides[get_current_owner] = owner_without_write_scope
    response = await api_client.post(
        "/api/v1/imports/csv",
        files={"file": ("tasks.csv", b"date,task,category,time_spent_minutes\n2026-04-15,Plan,Work,30\n", "text/csv")},
    )

    assert response.status_code == 403
    assert response.json()["error"]["code"] == "IMPORT_PERMISSION_DENIED"
