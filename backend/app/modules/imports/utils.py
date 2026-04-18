from datetime import date, datetime

from app.modules.imports.constants import NOTION_DATE_FORMATS
from app.modules.imports.exceptions import CSVValidationError
from app.shared.enums.source import normalize_text


def normalize_header(value: str | None) -> str:
    return normalize_text(value or "").replace(" ", "_")


def normalize_display_text(value: str | None) -> str:
    return " ".join((value or "").strip().split())


def parse_import_date(value: str | None) -> date:
    text = normalize_display_text(value)
    if not text:
        raise CSVValidationError("date is required")
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass
    for date_format in NOTION_DATE_FORMATS:
        try:
            return datetime.strptime(text, date_format).date()
        except ValueError:
            continue
    raise CSVValidationError(f"invalid date: {text}")


def parse_duration_minutes(value: str | None) -> int:
    text = normalize_display_text(value)
    if not text:
        raise CSVValidationError("time_spent_minutes is required")
    try:
        duration = int(text)
    except ValueError as exc:
        raise CSVValidationError(f"invalid time_spent_minutes: {text}") from exc
    if duration <= 0:
        raise CSVValidationError("time_spent_minutes must be positive")
    return duration


def parse_tags(value: str | None) -> list[str]:
    tags: list[str] = []
    seen: set[str] = set()
    for raw_tag in (value or "").split(","):
        tag = normalize_text(raw_tag)
        if tag and tag not in seen:
            tags.append(tag)
            seen.add(tag)
    return tags


def normalize_note(value: str | None) -> str | None:
    text = normalize_display_text(value)
    return text or None
