import pytest

from app.modules.imports.exceptions import CSVValidationError
from app.modules.imports.services.csv_parser_service import CSVParserService


def test_csv_parser_normalizes_headers_dates_duration_tags_and_notes() -> None:
    csv_bytes = (
        " Date , Task , Category , time_spent_minutes,tags,notes\n"
        "2026-04-15, Write Plan , Deep Work ,45,\"Writing, writing, Docs\", useful note\n"
        "April 15, 2026,Review,Admin,10,,\n"
    ).encode()

    result = CSVParserService().parse(csv_bytes, "tasks.csv")

    assert result.total_rows == 2
    assert result.invalid_rows == []
    assert result.valid_rows[0].log_date.isoformat() == "2026-04-15"
    assert result.valid_rows[0].task_name == "Write Plan"
    assert result.valid_rows[0].normalized_task_name == "write plan"
    assert result.valid_rows[0].tags == ["writing", "docs"]
    assert result.valid_rows[0].note == "useful note"
    assert result.valid_rows[1].log_date.isoformat() == "2026-04-15"
    assert result.valid_rows[1].note is None


def test_csv_parser_returns_row_errors_for_invalid_dates_duration_and_required_cells() -> None:
    csv_bytes = (
        "date,task,category,time_spent_minutes,tags,notes\n"
        ",Missing Date,Admin,10,,\n"
        "2026-04-15,,Admin,0,,\n"
        "not-a-date,Task,Admin,abc,,\n"
    ).encode()

    result = CSVParserService().parse(csv_bytes, "tasks.csv")

    assert result.valid_rows == []
    assert result.invalid_rows[0].reasons == ["date is required"]
    assert "task is required" in result.invalid_rows[1].reasons
    assert "time_spent_minutes must be positive" in result.invalid_rows[1].reasons
    assert "invalid date" in result.invalid_rows[2].reasons[0]
    assert "invalid time_spent_minutes" in result.invalid_rows[2].reasons[1]


@pytest.mark.parametrize(
    ("csv_bytes", "message"),
    [
        (b"", "CSV file is empty."),
        (b"date,task\n", "missing required columns"),
        (b"date,task,category,time_spent_minutes\n", "contains no data rows"),
    ],
)
def test_csv_parser_rejects_invalid_files(csv_bytes: bytes, message: str) -> None:
    with pytest.raises(CSVValidationError, match=message):
        CSVParserService().parse(csv_bytes, "tasks.csv")
