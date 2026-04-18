from uuid import uuid4

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


@pytest.mark.asyncio
async def test_import_status_api_returns_owner_scoped_import_run(api_client, async_session) -> None:
    import_run = await ImportTraceService(ImportRunRepository(async_session)).create_import_run(
        DEFAULT_OWNER_ID,
        "csv",
        "tasks.csv",
    )

    response = await api_client.get(f"/api/v1/imports/{import_run.id}")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["id"] == str(import_run.id)
    assert body["data"]["status"] == "pending"


@pytest.mark.asyncio
async def test_import_status_api_returns_not_found_for_wrong_owner_or_missing_run(api_client) -> None:
    response = await api_client.get(f"/api/v1/imports/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "IMPORT_NOT_FOUND"
