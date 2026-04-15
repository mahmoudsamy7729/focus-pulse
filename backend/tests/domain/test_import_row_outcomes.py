from uuid import uuid4

import pytest

from app.modules.imports.exceptions import InvalidImportOutcomeError
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


@pytest.mark.asyncio
async def test_import_row_outcome_validation(async_session) -> None:
    service = ImportTraceService(ImportRunRepository(async_session))
    import_run = await service.create_import_run(uuid4(), "csv", "tasks.csv")

    with pytest.raises(InvalidImportOutcomeError):
        await service.record_import_row_outcome(import_run.id, 1, "inserted", "Not a row outcome")

    with pytest.raises(InvalidImportOutcomeError):
        await service.record_import_row_outcome(import_run.id, 1, "failed", " ")
