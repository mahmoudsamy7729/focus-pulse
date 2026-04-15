from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.imports.repositories.import_run_repository import ImportRunRepository
from app.modules.imports.services.import_trace_service import ImportTraceService


def get_import_run_repository(session: Annotated[AsyncSession, Depends(get_db_session)]) -> ImportRunRepository:
    return ImportRunRepository(session)


def get_import_trace_service(
    repository: Annotated[ImportRunRepository, Depends(get_import_run_repository)],
) -> ImportTraceService:
    return ImportTraceService(repository)
