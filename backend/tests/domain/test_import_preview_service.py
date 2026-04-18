from uuid import uuid4

import pytest
from sqlalchemy import select

from app.modules.imports.models import ImportRun
from app.modules.imports.services.csv_parser_service import CSVParserService
from app.modules.imports.services.import_preview_service import ImportPreviewService


@pytest.mark.asyncio
async def test_preview_service_returns_normalized_payload_without_import_run_side_effects(async_session) -> None:
    _ = uuid4()
    csv_bytes = (
        "date,task,category,time_spent_minutes,tags,notes\n"
        "2026-04-15, Write Plan , Deep Work ,45,writing,useful note\n"
        ",Missing Date,Admin,10,,\n"
    ).encode()

    preview = await ImportPreviewService(CSVParserService()).preview_csv(csv_bytes, "tasks.csv")
    result = await async_session.execute(select(ImportRun))

    assert preview.total_rows == 2
    assert preview.valid_row_count == 1
    assert preview.invalid_row_count == 1
    assert preview.valid_rows[0]["date"] == "2026-04-15"
    assert result.scalars().all() == []
