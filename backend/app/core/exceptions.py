from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.modules.imports.exceptions import (
    CSVParsingError,
    CSVValidationError,
    ImportEnqueueError,
    ImportNotFoundError,
    ImportPermissionError,
    InvalidImportOutcomeError,
    InvalidImportStatusTransitionError,
)
from app.modules.analytics.exceptions import DashboardDataQualityError, InvalidDashboardPeriodError
from app.modules.daily_logs.exceptions import InvalidDailyLogRangeError
from app.shared.schemas.responses import error_response


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}


EXCEPTION_MAP: dict[type[Exception], tuple[int, str, str]] = {
    InvalidDashboardPeriodError: (
        status.HTTP_400_BAD_REQUEST,
        "DASHBOARD_INVALID_PERIOD",
        "Dashboard period filter is invalid.",
    ),
    DashboardDataQualityError: (
        status.HTTP_409_CONFLICT,
        "DASHBOARD_DATA_QUALITY_ERROR",
        "Dashboard data cannot be summarized safely.",
    ),
    InvalidDailyLogRangeError: (
        status.HTTP_400_BAD_REQUEST,
        "DAILY_LOG_RANGE_INVALID",
        "Daily log date range is invalid.",
    ),
    CSVParsingError: (status.HTTP_400_BAD_REQUEST, "CSV_PARSING_ERROR", "CSV file could not be parsed."),
    CSVValidationError: (status.HTTP_400_BAD_REQUEST, "CSV_VALIDATION_ERROR", "CSV file failed validation."),
    ImportPermissionError: (status.HTTP_403_FORBIDDEN, "IMPORT_PERMISSION_DENIED", "Import permission denied."),
    ImportNotFoundError: (status.HTTP_404_NOT_FOUND, "IMPORT_NOT_FOUND", "Import run not found."),
    ImportEnqueueError: (status.HTTP_409_CONFLICT, "IMPORT_ENQUEUE_FAILED", "Import could not be enqueued."),
    InvalidImportOutcomeError: (status.HTTP_400_BAD_REQUEST, "IMPORT_OUTCOME_INVALID", "Import row outcome is invalid."),
    InvalidImportStatusTransitionError: (
        status.HTTP_400_BAD_REQUEST,
        "IMPORT_STATUS_INVALID",
        "Import status transition is invalid.",
    ),
}


async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.code, exc.message, exc.details),
    )


async def mapped_error_handler(_: Request, exc: Exception) -> JSONResponse:
    status_code, code, default_message = EXCEPTION_MAP[type(exc)]
    return JSONResponse(
        status_code=status_code,
        content=error_response(code, str(exc) or default_message),
    )


async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response("REQUEST_VALIDATION_ERROR", "Request validation failed.", {"errors": exc.errors()}),
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    for exception_type in EXCEPTION_MAP:
        app.add_exception_handler(exception_type, mapped_error_handler)
