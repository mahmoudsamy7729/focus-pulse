import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.dependencies import get_csv_import_service
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService
from app.main import app


@pytest.mark.asyncio
async def test_confirm_api_returns_accepted_envelope_and_honors_idempotency_header(api_client, async_session) -> None:
    queued: list[tuple] = []

    def override_service() -> CSVImportService:
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
            enqueue_import=lambda *args: queued.append(args),
        )

    app.dependency_overrides[get_csv_import_service] = override_service
    response = await api_client.post(
        "/api/v1/imports/csv",
        headers={"Idempotency-Key": "abc12345"},
        files={"file": ("tasks.csv", b"date,task,category,time_spent_minutes\n2026-04-15,Plan,Work,30\n", "text/csv")},
    )

    body = response.json()
    assert response.status_code == 202
    assert body["success"] is True
    assert body["data"]["status"] == "pending"
    assert body["data"]["import_run_id"]
    assert queued
