from uuid import uuid4

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


@pytest.mark.asyncio
async def test_import_history_api_returns_paginated_success_envelope(api_client, async_session) -> None:
    service = ImportTraceService(ImportRunRepository(async_session))
    await service.create_import_run(DEFAULT_OWNER_ID, "csv", "one.csv")
    await service.create_import_run(DEFAULT_OWNER_ID, "csv", "two.csv")
    await service.create_import_run(uuid4(), "csv", "other.csv")

    response = await api_client.get("/api/v1/imports?page=1&limit=1")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["page"] == 1
    assert body["data"]["limit"] == 1
    assert body["data"]["total"] == 2
    assert len(body["data"]["items"]) == 1
