from enum import StrEnum


class ImportSourceType(StrEnum):
    CSV = "csv"


class ImportRowOutcomeType(StrEnum):
    INVALID = "invalid"
    SKIPPED = "skipped"
    FAILED = "failed"


IMPORT_ROW_OUTCOME_TYPES = {item.value for item in ImportRowOutcomeType}
