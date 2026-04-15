from enum import StrEnum


class SourceLabel(StrEnum):
    MANUAL = "manual"
    CSV_IMPORT = "csv_import"
    SYSTEM = "system"


DEFAULT_SOURCE = SourceLabel.MANUAL


def normalize_text(value: str) -> str:
    return " ".join(value.strip().lower().split())
