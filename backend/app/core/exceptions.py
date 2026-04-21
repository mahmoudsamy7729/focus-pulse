from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.modules.imports.exceptions import (
    CSVParsingError,
    CSVValidationError,
    DuplicateImportDueWindowError,
    ImportEnqueueError,
    ImportNotFoundError,
    ImportPermissionError,
    ImportScheduleConflictError,
    ImportScheduleNotFoundError,
    ImportScheduleRetentionError,
    ImportScheduleRetryExhaustedError,
    InvalidImportOutcomeError,
    InvalidImportScheduleError,
    InvalidImportStatusTransitionError,
    NonRetryableImportScheduleFailureError,
    UnsupportedImportSourceError,
)
from app.modules.analytics.exceptions import DashboardDataQualityError, InvalidDashboardPeriodError
from app.modules.ai_insights.exceptions import (
    AIAnalysisScheduleConflictError,
    AIAnalysisScheduleNotFoundError,
    AIAnalysisScheduleRetentionError,
    AIAnalysisScheduleRetryExhaustedError,
    AIInsightConflictError,
    AIInsightEnqueueError,
    AIInsightIdempotencyConflictError,
    AIInsightNotFoundError,
    AIOutputValidationError,
    AIProviderFailureError,
    InsightGenerationConflictError,
    InsightResultNotFoundError,
    InsightValidationFailureError,
    DuplicateAIAnalysisDueWindowError,
    InvalidInsightPeriodError,
    InvalidSourceAnalysisError,
    InvalidAIInsightStatusTransitionError,
    InvalidAIInsightTargetPeriodError,
    InvalidAIAnalysisScheduleError,
    MissingSourceAnalysisError,
    NonRetryableAIAnalysisScheduleFailureError,
    UnsupportedAIAnalysisSourceError,
)
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
    InvalidImportScheduleError: (
        status.HTTP_400_BAD_REQUEST,
        "IMPORT_SCHEDULE_INVALID",
        "Import schedule is invalid.",
    ),
    ImportScheduleNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "IMPORT_SCHEDULE_NOT_FOUND",
        "Import schedule not found.",
    ),
    ImportScheduleConflictError: (
        status.HTTP_409_CONFLICT,
        "IMPORT_SCHEDULE_CONFLICT",
        "Import schedule request conflicts with existing work.",
    ),
    DuplicateImportDueWindowError: (
        status.HTTP_409_CONFLICT,
        "IMPORT_SCHEDULE_DUPLICATE_WINDOW",
        "Import schedule due window already exists.",
    ),
    UnsupportedImportSourceError: (
        status.HTTP_400_BAD_REQUEST,
        "IMPORT_SCHEDULE_SOURCE_UNSUPPORTED",
        "Import schedule source is unsupported.",
    ),
    NonRetryableImportScheduleFailureError: (
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "IMPORT_SCHEDULE_NON_RETRYABLE_FAILURE",
        "Import schedule failure is not retryable.",
    ),
    ImportScheduleRetryExhaustedError: (
        status.HTTP_409_CONFLICT,
        "IMPORT_SCHEDULE_RETRY_EXHAUSTED",
        "Import schedule retry attempts are exhausted.",
    ),
    ImportScheduleRetentionError: (
        status.HTTP_409_CONFLICT,
        "IMPORT_SCHEDULE_RETENTION_VIOLATION",
        "Import schedule retention rule was violated.",
    ),
    InvalidAIInsightTargetPeriodError: (
        status.HTTP_400_BAD_REQUEST,
        "AI_INSIGHT_INVALID_PERIOD",
        "AI insight period is invalid.",
    ),
    AIInsightNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "AI_INSIGHT_NOT_FOUND",
        "AI insight run not found.",
    ),
    AIInsightConflictError: (
        status.HTTP_409_CONFLICT,
        "AI_INSIGHT_CONFLICT",
        "AI insight request conflicts with an existing run.",
    ),
    AIInsightIdempotencyConflictError: (
        status.HTTP_409_CONFLICT,
        "AI_INSIGHT_IDEMPOTENCY_CONFLICT",
        "AI insight idempotency key conflicts with an existing run.",
    ),
    AIInsightEnqueueError: (
        status.HTTP_409_CONFLICT,
        "AI_INSIGHT_ENQUEUE_FAILED",
        "AI insight run could not be enqueued.",
    ),
    AIProviderFailureError: (
        status.HTTP_502_BAD_GATEWAY,
        "AI_PROVIDER_FAILURE",
        "AI provider failed.",
    ),
    AIOutputValidationError: (
        status.HTTP_400_BAD_REQUEST,
        "AI_OUTPUT_VALIDATION_FAILED",
        "AI provider output failed validation.",
    ),
    InvalidAIInsightStatusTransitionError: (
        status.HTTP_400_BAD_REQUEST,
        "AI_INSIGHT_STATUS_INVALID",
        "AI insight status transition is invalid.",
    ),
    InvalidInsightPeriodError: (
        status.HTTP_400_BAD_REQUEST,
        "INSIGHT_PERIOD_INVALID",
        "Insight result period is invalid.",
    ),
    MissingSourceAnalysisError: (
        status.HTTP_404_NOT_FOUND,
        "SOURCE_ANALYSIS_MISSING",
        "No completed source analysis was found.",
    ),
    InvalidSourceAnalysisError: (
        status.HTTP_400_BAD_REQUEST,
        "SOURCE_ANALYSIS_INVALID",
        "Source analysis cannot be used for insight generation.",
    ),
    InsightResultNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "INSIGHT_RESULT_NOT_FOUND",
        "Insight result not found.",
    ),
    InsightGenerationConflictError: (
        status.HTTP_409_CONFLICT,
        "INSIGHT_GENERATION_CONFLICT",
        "Insight generation conflicts with an existing result.",
    ),
    InsightValidationFailureError: (
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "INSIGHT_VALIDATION_FAILED",
        "Generated insight result failed validation.",
    ),
    InvalidAIAnalysisScheduleError: (
        status.HTTP_400_BAD_REQUEST,
        "AI_ANALYSIS_SCHEDULE_INVALID",
        "AI analysis schedule is invalid.",
    ),
    AIAnalysisScheduleNotFoundError: (
        status.HTTP_404_NOT_FOUND,
        "AI_ANALYSIS_SCHEDULE_NOT_FOUND",
        "AI analysis schedule not found.",
    ),
    AIAnalysisScheduleConflictError: (
        status.HTTP_409_CONFLICT,
        "AI_ANALYSIS_SCHEDULE_CONFLICT",
        "AI analysis schedule request conflicts with existing work.",
    ),
    DuplicateAIAnalysisDueWindowError: (
        status.HTTP_409_CONFLICT,
        "AI_ANALYSIS_SCHEDULE_DUPLICATE_WINDOW",
        "AI analysis schedule due window already exists.",
    ),
    UnsupportedAIAnalysisSourceError: (
        status.HTTP_400_BAD_REQUEST,
        "AI_ANALYSIS_SCHEDULE_SOURCE_UNSUPPORTED",
        "AI analysis schedule source is unsupported.",
    ),
    NonRetryableAIAnalysisScheduleFailureError: (
        status.HTTP_422_UNPROCESSABLE_ENTITY,
        "AI_ANALYSIS_SCHEDULE_NON_RETRYABLE_FAILURE",
        "AI analysis schedule failure is not retryable.",
    ),
    AIAnalysisScheduleRetryExhaustedError: (
        status.HTTP_409_CONFLICT,
        "AI_ANALYSIS_SCHEDULE_RETRY_EXHAUSTED",
        "AI analysis schedule retry attempts are exhausted.",
    ),
    AIAnalysisScheduleRetentionError: (
        status.HTTP_409_CONFLICT,
        "AI_ANALYSIS_SCHEDULE_RETENTION_VIOLATION",
        "AI analysis schedule retention rule was violated.",
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
