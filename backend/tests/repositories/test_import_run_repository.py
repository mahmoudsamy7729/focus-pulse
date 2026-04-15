from uuid import uuid4

import pytest

from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


@pytest.mark.asyncio
async def test_import_repository_loads_row_outcomes_for_traceability(async_session) -> None:
    repository = ImportRunRepository(async_session)
    service = ImportTraceService(repository)
    import_run = await service.create_import_run(uuid4(), "csv", "tasks.csv")
    await service.record_import_row_outcome(
        import_run.id,
        4,
        "skipped",
        "Duplicate",
        {"normalized_task_name": "plan", "time_spent_minutes": 30},
    )
    await async_session.commit()

    loaded = await repository.get(import_run.id)

    assert loaded is not None
    assert loaded.row_outcomes[0].outcome_type == "skipped"
    assert loaded.row_outcomes[0].normalized_task_name == "plan"
