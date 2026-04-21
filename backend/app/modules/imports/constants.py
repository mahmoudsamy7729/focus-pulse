from enum import StrEnum


class ImportSourceType(StrEnum):
    CSV = "csv"


class ImportRowOutcomeType(StrEnum):
    INVALID = "invalid"
    SKIPPED = "skipped"
    FAILED = "failed"


class ImportAutomationType(StrEnum):
    SCHEDULED_IMPORT = "scheduled_import"


class ImportScheduleState(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


class ImportScheduleCadence(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


class ImportScheduleRunOutcome(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"
    SKIPPED = "skipped"
    NO_NEW_DATA = "no_new_data"


class ImportScheduleFailureClassification(StrEnum):
    RETRYABLE = "retryable"
    NON_RETRYABLE = "non_retryable"
    EXHAUSTED = "exhausted"


IMPORT_ROW_OUTCOME_TYPES = {item.value for item in ImportRowOutcomeType}
IMPORT_SCHEDULE_STATES = {item.value for item in ImportScheduleState}
IMPORT_SCHEDULE_CADENCES = {item.value for item in ImportScheduleCadence}
IMPORT_SCHEDULE_RUN_OUTCOMES = {item.value for item in ImportScheduleRunOutcome}
IMPORT_SCHEDULE_FAILURE_CLASSIFICATIONS = {item.value for item in ImportScheduleFailureClassification}

CSV_REQUIRED_COLUMNS = {"date", "task", "category", "time_spent_minutes"}
CSV_OPTIONAL_COLUMNS = {"tags", "notes"}
CSV_SOURCE_TYPE = ImportSourceType.CSV.value
CSV_MAX_ROWS = 5000
CSV_MAX_UPLOAD_BYTES = 2 * 1024 * 1024
CSV_PREVIEW_RATE_LIMIT = "imports_csv_preview"
CSV_CONFIRM_RATE_LIMIT = "imports_csv_confirm"
IMPORT_READ_RATE_LIMIT = "imports_read"
IMPORT_SCHEDULE_READ_RATE_LIMIT = "imports_schedule_read"
IMPORT_SCHEDULE_WRITE_RATE_LIMIT = "imports_schedule_write"
IMPORT_SCHEDULE_TRIGGER_RATE_LIMIT = "imports_schedule_trigger"
DEFAULT_IMPORT_PAGE = 1
DEFAULT_IMPORT_LIMIT = 20
MAX_IMPORT_LIMIT = 100
IMPORT_SCHEDULE_RETENTION_DAYS = 90
IMPORT_SCHEDULE_MAX_ATTEMPTS = 3
NOTION_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y")
