from uuid import uuid4

import pytest
from sqlalchemy import select

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.models import ImportRowOutcome
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.schemas import ConfirmedImportRequest, InvalidImportRow, NormalizedImportRow
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService
from app.shared.enums.run_status import RunStatus


def _service(async_session, enqueue_import=None) -> CSVImportService:
    trace = ImportTraceService(ImportRunRepository(async_session))
    return CSVImportService(
        CSVParserService(),
        trace,
        DailyLogService(DailyLogRepository(async_session)),
        TaskService(
            TaskRepository(async_session),
            CategoryRepository(async_session),
            NoteService(NoteRepository(async_session)),
            import_trace_service=trace,
        ),
        enqueue_import=enqueue_import,
    )


@pytest.mark.asyncio
async def test_import_pipeline_inserts_valid_rows_and_records_invalid_and_duplicate_rows(async_session) -> None:
    owner_id = uuid4()
    queued: list[tuple] = []
    service = _service(async_session, enqueue_import=lambda *args: queued.append(args))
    accepted = await service.confirm_csv_import(
        ConfirmedImportRequest(
            owner_id=owner_id,
            source_name="tasks.csv",
            csv_bytes=(
                "date,task,category,time_spent_minutes,tags,notes\n"
                "2026-04-15,Plan,Work,30,Deep,Useful\n"
                "2026-04-15, plan ,Work,30,,Duplicate\n"
                ",Missing Date,Admin,10,,\n"
            ).encode(),
        )
    )
    _, _, valid_rows, invalid_rows = queued[0]

    result = await _service(async_session).process_import_payload(
        accepted.import_run_id,
        owner_id,
        [NormalizedImportRow.model_validate(row) for row in valid_rows],
        [InvalidImportRow.model_validate(row) for row in invalid_rows],
    )
    outcomes = (await async_session.execute(select(ImportRowOutcome))).scalars().all()

    assert result.status == RunStatus.COMPLETED_WITH_ERRORS.value
    assert result.inserted_row_count == 1
    assert result.invalid_row_count == 1
    assert result.skipped_row_count == 1
    assert {outcome.outcome_type for outcome in outcomes} == {"invalid", "skipped"}
