from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_preview_service import ImportPreviewService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


def _enqueue_csv_import_after_commit(
    session: AsyncSession,
    import_run_id,
    owner_id,
    valid_rows: list[dict[str, object]],
    invalid_rows: list[dict[str, object]],
) -> object:
    def enqueue() -> object:
        from app.workers.tasks.import_tasks import process_csv_import

        return process_csv_import.delay(str(import_run_id), str(owner_id), valid_rows, invalid_rows)

    session.info.setdefault("after_commit_callbacks", []).append(enqueue)
    return {"queued_after_commit": True}


def get_import_run_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> ImportRunRepository:
    return ImportRunRepository(session)


def get_import_trace_service(
    repository: Annotated[ImportRunRepository, Depends(get_import_run_repository)],
) -> ImportTraceService:
    return ImportTraceService(repository)


def get_csv_parser_service() -> CSVParserService:
    return CSVParserService()


def get_import_preview_service(
    parser: Annotated[CSVParserService, Depends(get_csv_parser_service)],
) -> ImportPreviewService:
    return ImportPreviewService(parser)


def get_daily_log_service(session: Annotated[AsyncSession, Depends(get_db_session)]) -> DailyLogService:
    return DailyLogService(DailyLogRepository(session))


def get_task_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    import_trace_service: Annotated[ImportTraceService, Depends(get_import_trace_service)],
) -> TaskService:
    return TaskService(
        TaskRepository(session),
        CategoryRepository(session),
        NoteService(NoteRepository(session)),
        import_trace_service=import_trace_service,
    )


def get_csv_import_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
    parser: Annotated[CSVParserService, Depends(get_csv_parser_service)],
    import_trace_service: Annotated[ImportTraceService, Depends(get_import_trace_service)],
    daily_log_service: Annotated[DailyLogService, Depends(get_daily_log_service)],
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> CSVImportService:
    return CSVImportService(
        parser,
        import_trace_service,
        daily_log_service,
        task_service,
        enqueue_import=lambda import_run_id, owner_id, valid_rows, invalid_rows: _enqueue_csv_import_after_commit(
            session,
            import_run_id,
            owner_id,
            valid_rows,
            invalid_rows,
        ),
    )
