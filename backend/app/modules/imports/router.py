from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Header, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import CurrentOwner, require_scope
from app.core.database import commit_session, get_db_session
from app.core.exceptions import AppError
from app.modules.imports.constants import DEFAULT_IMPORT_LIMIT, DEFAULT_IMPORT_PAGE, MAX_IMPORT_LIMIT
from app.modules.imports.exceptions import CSVValidationError, ImportNotFoundError
from app.modules.imports.schemas import ConfirmedImportRequest
from app.modules.imports.services.csv_import_service import CSVImportService
from app.modules.imports.services.import_preview_service import ImportPreviewService
from app.modules.imports.services.import_trace_service import ImportTraceService
from app.modules.imports.dependencies import (
    get_csv_import_service,
    get_import_preview_service,
    get_import_trace_service,
)
from app.shared.schemas.responses import success_response


router = APIRouter()


async def _read_csv_upload(file: UploadFile) -> bytes:
    if not file.filename:
        raise CSVValidationError("CSV upload must include a filename.")
    return await file.read()


@router.post("/csv/preview")
async def preview_csv_import(
    owner: Annotated[CurrentOwner, Depends(require_scope("imports:write"))],
    service: Annotated[ImportPreviewService, Depends(get_import_preview_service)],
    file: Annotated[UploadFile, File()],
) -> dict[str, object]:
    _ = owner
    payload = await _read_csv_upload(file)
    preview = await service.preview_csv(payload, file.filename or "upload.csv")
    return success_response(preview.model_dump(mode="json"))


@router.post("/csv", status_code=status.HTTP_202_ACCEPTED)
async def create_csv_import(
    owner: Annotated[CurrentOwner, Depends(require_scope("imports:write"))],
    session: Annotated[AsyncSession, Depends(get_db_session)],
    service: Annotated[CSVImportService, Depends(get_csv_import_service)],
    file: Annotated[UploadFile, File()],
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    x_request_id: Annotated[str | None, Header(alias="X-Request-Id")] = None,
) -> dict[str, object]:
    payload = await _read_csv_upload(file)
    accepted = await service.confirm_csv_import(
        ConfirmedImportRequest(
            owner_id=owner.owner_id,
            source_name=file.filename or "upload.csv",
            csv_bytes=payload,
            request_id=x_request_id,
            idempotency_key=idempotency_key,
        )
    )
    await commit_session(session)
    return success_response(accepted.model_dump(mode="json"))


def _pagination(page: int, limit: int) -> tuple[int, int]:
    if page < 1:
        raise AppError("PAGINATION_INVALID", "page must be greater than or equal to 1.")
    if limit < 1 or limit > MAX_IMPORT_LIMIT:
        raise AppError("PAGINATION_INVALID", f"limit must be between 1 and {MAX_IMPORT_LIMIT}.")
    return page, limit


@router.get("")
async def list_import_runs(
    owner: Annotated[CurrentOwner, Depends(require_scope("imports:read"))],
    service: Annotated[ImportTraceService, Depends(get_import_trace_service)],
    page: Annotated[int, Query(ge=1)] = DEFAULT_IMPORT_PAGE,
    limit: Annotated[int, Query(ge=1, le=MAX_IMPORT_LIMIT)] = DEFAULT_IMPORT_LIMIT,
) -> dict[str, object]:
    page, limit = _pagination(page, limit)
    result = await service.list_import_runs(owner.owner_id, page, limit)
    return success_response(result.model_dump(mode="json"))


@router.get("/{import_run_id}")
async def get_import_run(
    owner: Annotated[CurrentOwner, Depends(require_scope("imports:read"))],
    service: Annotated[ImportTraceService, Depends(get_import_trace_service)],
    import_run_id: UUID,
) -> dict[str, object]:
    result = await service.get_import_run_for_owner(owner.owner_id, import_run_id)
    if result is None:
        raise ImportNotFoundError("Import run was not found for the current owner.")
    return success_response(result.model_dump(mode="json"))


@router.get("/{import_run_id}/row-outcomes")
async def list_import_row_outcomes(
    owner: Annotated[CurrentOwner, Depends(require_scope("imports:read"))],
    service: Annotated[ImportTraceService, Depends(get_import_trace_service)],
    import_run_id: UUID,
    page: Annotated[int, Query(ge=1)] = DEFAULT_IMPORT_PAGE,
    limit: Annotated[int, Query(ge=1, le=MAX_IMPORT_LIMIT)] = DEFAULT_IMPORT_LIMIT,
) -> dict[str, object]:
    page, limit = _pagination(page, limit)
    result = await service.list_row_outcomes(owner.owner_id, import_run_id, page, limit)
    if result is None:
        raise ImportNotFoundError("Import run was not found for the current owner.")
    return success_response(result.model_dump(mode="json"))
