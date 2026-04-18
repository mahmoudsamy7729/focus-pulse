import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


@pytest.mark.asyncio
async def test_import_row_outcomes_api_returns_paginated_ordered_rows(api_client, async_session) -> None:
    service = ImportTraceService(ImportRunRepository(async_session))
    import_run = await service.create_import_run(DEFAULT_OWNER_ID, "csv", "tasks.csv")
    await service.record_import_row_outcome(import_run.id, 2, "invalid", "Missing task")
    await service.record_import_row_outcome(import_run.id, 1, "skipped", "Duplicate")

    response = await api_client.get(f"/api/v1/imports/{import_run.id}/row-outcomes?page=1&limit=20")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["total"] == 2
    assert [item["row_number"] for item in body["data"]["items"]] == [1, 2]
