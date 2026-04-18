from enum import StrEnum


class ImportSourceType(StrEnum):
    CSV = "csv"


class ImportRowOutcomeType(StrEnum):
    INVALID = "invalid"
    SKIPPED = "skipped"
    FAILED = "failed"


IMPORT_ROW_OUTCOME_TYPES = {item.value for item in ImportRowOutcomeType}

CSV_REQUIRED_COLUMNS = {"date", "task", "category", "time_spent_minutes"}
CSV_OPTIONAL_COLUMNS = {"tags", "notes"}
CSV_SOURCE_TYPE = ImportSourceType.CSV.value
CSV_MAX_ROWS = 5000
CSV_MAX_UPLOAD_BYTES = 2 * 1024 * 1024
CSV_PREVIEW_RATE_LIMIT = "imports_csv_preview"
CSV_CONFIRM_RATE_LIMIT = "imports_csv_confirm"
IMPORT_READ_RATE_LIMIT = "imports_read"
DEFAULT_IMPORT_PAGE = 1
DEFAULT_IMPORT_LIMIT = 20
MAX_IMPORT_LIMIT = 100
NOTION_DATE_FORMATS = ("%B %d, %Y", "%b %d, %Y")
