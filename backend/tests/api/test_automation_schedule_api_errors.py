from fastapi import status
import pytest

from app.core.exceptions import EXCEPTION_MAP
from app.api.dependencies import CurrentOwner, require_scope
from app.modules.ai_insights.exceptions import (
    AIAnalysisScheduleConflictError,
    AIAnalysisScheduleNotFoundError,
    InvalidAIAnalysisScheduleError,
)
from app.modules.ai_insights.constants import (
    AI_ANALYSIS_SCHEDULE_READ_RATE_LIMIT,
    AI_ANALYSIS_SCHEDULE_TRIGGER_RATE_LIMIT,
    AI_ANALYSIS_SCHEDULE_WRITE_RATE_LIMIT,
)
from app.modules.imports.constants import (
    IMPORT_SCHEDULE_READ_RATE_LIMIT,
    IMPORT_SCHEDULE_TRIGGER_RATE_LIMIT,
    IMPORT_SCHEDULE_WRITE_RATE_LIMIT,
)
from app.modules.imports.exceptions import (
    ImportScheduleConflictError,
    ImportScheduleNotFoundError,
    InvalidImportScheduleError,
)


def test_import_schedule_error_mappings_use_standard_codes() -> None:
    assert EXCEPTION_MAP[InvalidImportScheduleError][0:2] == (
        status.HTTP_400_BAD_REQUEST,
        "IMPORT_SCHEDULE_INVALID",
    )
    assert EXCEPTION_MAP[ImportScheduleNotFoundError][0:2] == (
        status.HTTP_404_NOT_FOUND,
        "IMPORT_SCHEDULE_NOT_FOUND",
    )
    assert EXCEPTION_MAP[ImportScheduleConflictError][0:2] == (
        status.HTTP_409_CONFLICT,
        "IMPORT_SCHEDULE_CONFLICT",
    )


def test_ai_analysis_schedule_error_mappings_use_standard_codes() -> None:
    assert EXCEPTION_MAP[InvalidAIAnalysisScheduleError][0:2] == (
        status.HTTP_400_BAD_REQUEST,
        "AI_ANALYSIS_SCHEDULE_INVALID",
    )
    assert EXCEPTION_MAP[AIAnalysisScheduleNotFoundError][0:2] == (
        status.HTTP_404_NOT_FOUND,
        "AI_ANALYSIS_SCHEDULE_NOT_FOUND",
    )
    assert EXCEPTION_MAP[AIAnalysisScheduleConflictError][0:2] == (
        status.HTTP_409_CONFLICT,
        "AI_ANALYSIS_SCHEDULE_CONFLICT",
    )


@pytest.mark.asyncio
async def test_schedule_permission_failure_uses_domain_error_prefix() -> None:
    dependency = require_scope("imports:write")
    owner = CurrentOwner(owner_id="00000000-0000-4000-8000-000000000001", scopes=frozenset({"imports:read"}))

    with pytest.raises(Exception) as exc_info:
        await dependency(owner)

    assert getattr(exc_info.value, "code") == "IMPORT_PERMISSION_DENIED"
    assert getattr(exc_info.value, "status_code") == status.HTTP_403_FORBIDDEN
    assert getattr(exc_info.value, "details") == {"required_scope": "imports:write"}


def test_schedule_rate_limit_names_are_defined_per_module() -> None:
    assert IMPORT_SCHEDULE_READ_RATE_LIMIT == "imports_schedule_read"
    assert IMPORT_SCHEDULE_WRITE_RATE_LIMIT == "imports_schedule_write"
    assert IMPORT_SCHEDULE_TRIGGER_RATE_LIMIT == "imports_schedule_trigger"
    assert AI_ANALYSIS_SCHEDULE_READ_RATE_LIMIT == "ai_analysis_schedule_read"
    assert AI_ANALYSIS_SCHEDULE_WRITE_RATE_LIMIT == "ai_analysis_schedule_write"
    assert AI_ANALYSIS_SCHEDULE_TRIGGER_RATE_LIMIT == "ai_analysis_schedule_trigger"
