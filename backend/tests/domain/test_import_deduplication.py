from datetime import date
from uuid import uuid4

import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_imported_duplicate_task_is_skipped_and_recorded(async_session) -> None:
    owner_id = uuid4()
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        owner_id,
        date(2026, 4, 15),
    )
    import_trace = ImportTraceService(ImportRunRepository(async_session))
    import_run = await import_trace.create_import_run(owner_id, "csv", "tasks.csv")
    service = TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        import_trace_service=import_trace,
    )

    first = await service.create_task(owner_id, daily_log, "Plan", 30, "Planning", import_run_id=import_run.id)
    duplicate = await service.create_task(
        owner_id,
        daily_log,
        " plan ",
        30,
        "Planning",
        import_run_id=import_run.id,
        row_number=2,
    )

    assert duplicate.id == first.id
    assert import_run.skipped_row_count == 1
    assert import_run.processed_row_count == 1
