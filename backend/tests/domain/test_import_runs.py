from uuid import uuid4

import pytest

from app.modules.imports.exceptions import InvalidImportStatusTransitionError
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_import_run_status_transitions_and_counts(async_session) -> None:
    service = ImportTraceService(ImportRunRepository(async_session))
    import_run = await service.create_import_run(uuid4(), "csv", "tasks.csv")

    await service.mark_import_processing(import_run.id)
    await service.record_inserted_row(import_run.id)
    await service.record_import_row_outcome(import_run.id, 2, "invalid", "Missing title")
    await service.complete_import_run(import_run.id, RunStatus.COMPLETED_WITH_ERRORS.value)

    assert import_run.status == RunStatus.COMPLETED_WITH_ERRORS.value
    assert import_run.processed_row_count == 2
    assert import_run.inserted_row_count == 1
    assert import_run.invalid_row_count == 1


@pytest.mark.asyncio
async def test_failed_import_requires_failure_reason(async_session) -> None:
    service = ImportTraceService(ImportRunRepository(async_session))
    import_run = await service.create_import_run(uuid4(), "csv", "tasks.csv")
    await service.mark_import_processing(import_run.id)

    with pytest.raises(InvalidImportStatusTransitionError):
        await service.complete_import_run(import_run.id, RunStatus.FAILED.value)
