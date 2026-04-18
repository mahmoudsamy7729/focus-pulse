from uuid import uuid4

import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.schemas import ConfirmedImportRequest
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService
from app.shared.enums.run_status import RunStatus


@pytest.mark.asyncio
async def test_confirmed_import_creates_import_run_and_enqueues_normalized_rows(async_session) -> None:
    owner_id = uuid4()
    enqueued: list[object] = []
    trace = ImportTraceService(ImportRunRepository(async_session))
    service = CSVImportService(
        CSVParserService(),
        trace,
        DailyLogService(DailyLogRepository(async_session)),
        TaskService(TaskRepository(async_session), CategoryRepository(async_session), NoteService(NoteRepository(async_session))),
        enqueue_import=lambda *args: enqueued.append(args),
    )

    accepted = await service.confirm_csv_import(
        ConfirmedImportRequest(
            owner_id=owner_id,
            source_name="tasks.csv",
            csv_bytes=b"date,task,category,time_spent_minutes\n2026-04-15,Plan,Work,30\n",
        )
    )

    assert accepted.status == RunStatus.PENDING.value
    assert enqueued
    import_run_id, queued_owner_id, valid_rows, invalid_rows = enqueued[0]
    assert import_run_id == accepted.import_run_id
    assert queued_owner_id == owner_id
    assert valid_rows[0]["normalized_task_name"] == "plan"
    assert invalid_rows == []
