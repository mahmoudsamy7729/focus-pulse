import csv
from io import StringIO

from app.modules.imports.constants import CSV_MAX_ROWS, CSV_REQUIRED_COLUMNS
from app.modules.imports.exceptions import CSVParsingError, CSVValidationError
from app.modules.imports.schemas import CSVParseResult, InvalidImportRow, NormalizedImportRow
from app.modules.imports.utils import (
    normalize_display_text,
    normalize_header,
    normalize_note,
    parse_duration_minutes,
    parse_import_date,
    parse_tags,
)
from app.shared.enums.source import normalize_text


class CSVParserService:
    def parse(self, csv_bytes: bytes, source_name: str) -> CSVParseResult:
        try:
            text = csv_bytes.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise CSVParsingError("CSV file must be UTF-8 encoded.") from exc
        if not text.strip():
            raise CSVValidationError("CSV file is empty.")

        try:
            reader = csv.DictReader(StringIO(text))
        except csv.Error as exc:
            raise CSVParsingError("CSV file could not be read.") from exc

        if not reader.fieldnames:
            raise CSVValidationError("CSV file must contain headers.")

        normalized_headers = [normalize_header(header) for header in reader.fieldnames]
        missing = sorted(CSV_REQUIRED_COLUMNS.difference(normalized_headers))
        if missing:
            raise CSVValidationError(f"CSV file is missing required columns: {', '.join(missing)}")

        header_lookup = dict(zip(reader.fieldnames, normalized_headers, strict=False))
        valid_rows: list[NormalizedImportRow] = []
        invalid_rows: list[InvalidImportRow] = []
        total_rows = 0

        try:
            for total_rows, row in enumerate(reader, start=1):
                if total_rows > CSV_MAX_ROWS:
                    raise CSVValidationError(f"CSV files are limited to {CSV_MAX_ROWS} data rows.")
                normalized_row = self._normalize_raw_row(row, header_lookup)
                parsed = self._parse_row(total_rows, normalized_row)
                if isinstance(parsed, NormalizedImportRow):
                    valid_rows.append(parsed)
                else:
                    invalid_rows.append(parsed)
        except csv.Error as exc:
            raise CSVParsingError("CSV file could not be read.") from exc

        if total_rows == 0:
            raise CSVValidationError("CSV file contains no data rows.")

        return CSVParseResult(
            source_name=source_name,
            total_rows=total_rows,
            valid_rows=valid_rows,
            invalid_rows=invalid_rows,
        )

    @staticmethod
    def _normalize_raw_row(row: dict[str | None, object], header_lookup: dict[str, str]) -> dict[str, str | None]:
        unwrapped_row = CSVParserService._unwrap_single_field_row(row, header_lookup)
        if unwrapped_row is not None:
            return unwrapped_row

        normalized_row = {header_lookup[key]: value for key, value in row.items() if key in header_lookup}
        extra_cells = row.get(None)
        if not isinstance(extra_cells, list) or not extra_cells:
            return normalized_row

        # Some Notion exports contain month-name dates with commas. If the date
        # cell was not quoted, DictReader shifts the year into the task column.
        date_part = normalize_display_text(normalized_row.get("date"))
        year_part = normalize_display_text(normalized_row.get("task"))
        if date_part and year_part.isdigit() and len(year_part) == 4:
            shifted = [
                f"{date_part}, {year_part}",
                normalized_row.get("category"),
                normalized_row.get("time_spent_minutes"),
                normalized_row.get("tags"),
                normalized_row.get("notes"),
                *extra_cells,
            ]
            for key, value in zip(
                ["date", "task", "category", "time_spent_minutes", "tags", "notes"],
                shifted,
                strict=False,
            ):
                normalized_row[key] = value
        return normalized_row

    @staticmethod
    def _unwrap_single_field_row(
        row: dict[str | None, object], header_lookup: dict[str, str]
    ) -> dict[str, str | None] | None:
        header_keys = list(header_lookup)
        extra_cells = row.get(None)
        if extra_cells:
            return None

        non_empty_values = [
            (key, normalize_display_text(str(value)))
            for key in header_keys
            if (value := row.get(key)) is not None and normalize_display_text(str(value))
        ]
        if len(non_empty_values) != 1:
            return None

        only_key, wrapped_value = non_empty_values[0]
        if only_key != header_keys[0]:
            return None

        try:
            inner_cells = next(csv.reader([wrapped_value]))
        except csv.Error:
            return None

        if len(inner_cells) != len(header_keys):
            return None

        return {
            header_lookup[header_key]: value
            for header_key, value in zip(header_keys, inner_cells, strict=False)
        }

    def _parse_row(self, row_number: int, row: dict[str, str | None]) -> NormalizedImportRow | InvalidImportRow:
        reasons: list[str] = []
        log_date = None
        duration = None
        task_name = normalize_display_text(row.get("task"))
        category_name = normalize_display_text(row.get("category"))

        if not task_name:
            reasons.append("task is required")
        if not category_name:
            reasons.append("category is required")

        try:
            log_date = parse_import_date(row.get("date"))
        except CSVValidationError as exc:
            reasons.append(str(exc))

        try:
            duration = parse_duration_minutes(row.get("time_spent_minutes"))
        except CSVValidationError as exc:
            reasons.append(str(exc))

        row_snapshot = {
            "date": normalize_display_text(row.get("date")),
            "task": task_name,
            "category": category_name,
            "time_spent_minutes": normalize_display_text(row.get("time_spent_minutes")),
        }

        if reasons:
            return InvalidImportRow(row_number=row_number, reasons=reasons, row_snapshot=row_snapshot)

        assert log_date is not None
        assert duration is not None
        normalized_task_name = normalize_text(task_name)
        normalized_category_name = normalize_text(category_name)
        tags = parse_tags(row.get("tags"))
        note = normalize_note(row.get("notes"))
        normalized_snapshot = {
            "row_number": row_number,
            "log_date": log_date.isoformat(),
            "task_name": task_name,
            "normalized_task_name": normalized_task_name,
            "category_name": category_name,
            "normalized_category_name": normalized_category_name,
            "time_spent_minutes": duration,
            "tags": tags,
            "note": note,
        }
        return NormalizedImportRow(
            row_number=row_number,
            log_date=log_date,
            task_name=task_name,
            normalized_task_name=normalized_task_name,
            category_name=category_name,
            normalized_category_name=normalized_category_name,
            time_spent_minutes=duration,
            tags=tags,
            note=note,
            row_snapshot=normalized_snapshot,
        )
