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


@pytest.mark.asyncio
async def test_import_repository_lists_owner_runs_and_row_outcomes_with_pagination(async_session) -> None:
    owner_id = uuid4()
    other_owner_id = uuid4()
    repository = ImportRunRepository(async_session)
    service = ImportTraceService(repository)
    first = await service.create_import_run(owner_id, "csv", "one.csv")
    second = await service.create_import_run(owner_id, "csv", "two.csv")
    await service.create_import_run(other_owner_id, "csv", "other.csv")
    await service.record_import_row_outcome(first.id, 2, "invalid", "Missing date")
    await service.record_import_row_outcome(first.id, 1, "skipped", "Duplicate")

    runs, total_runs = await repository.list_by_owner(owner_id, page=1, limit=10)
    outcomes, total_outcomes = await repository.list_row_outcomes(owner_id, first.id, page=1, limit=10)
    loaded = await repository.get_by_owner(owner_id, second.id)

    assert total_runs == 2
    assert {run.owner_id for run in runs} == {owner_id}
    assert loaded is not None
    assert total_outcomes == 2
    assert [outcome.row_number for outcome in outcomes] == [1, 2]
