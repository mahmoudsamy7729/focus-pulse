from enum import StrEnum


class RunStatus(StrEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"


TERMINAL_RUN_STATUSES = {
    RunStatus.COMPLETED,
    RunStatus.COMPLETED_WITH_ERRORS,
    RunStatus.FAILED,
}

VALID_RUN_TRANSITIONS = {
    RunStatus.PENDING: {RunStatus.PROCESSING},
    RunStatus.PROCESSING: TERMINAL_RUN_STATUSES,
}
