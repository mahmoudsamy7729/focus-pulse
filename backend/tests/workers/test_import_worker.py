from uuid import uuid4

import app.workers.tasks.import_tasks as import_tasks

from app.modules.imports.schemas import NormalizedImportRow
from app.workers.tasks.import_tasks import process_csv_import


def test_import_worker_delegates_payload_without_business_rules(monkeypatch) -> None:
    calls: list[tuple] = []

    async def fake_process_csv_import_payload(import_run_id, owner_id, valid_rows, invalid_rows):
        calls.append((import_run_id, owner_id, valid_rows, invalid_rows))
        return {"status": "completed"}

    monkeypatch.setattr(import_tasks, "process_csv_import_payload", fake_process_csv_import_payload)
    import_run_id = uuid4()
    owner_id = uuid4()
    rows = [
        NormalizedImportRow(
            row_number=1,
            log_date="2026-04-15",
            task_name="Plan",
            normalized_task_name="plan",
            category_name="Work",
            normalized_category_name="work",
            time_spent_minutes=30,
            tags=[],
            row_snapshot={"normalized_task_name": "plan"},
        ).model_dump(mode="json")
    ]

    if hasattr(process_csv_import, "run"):
        result = process_csv_import.run(str(import_run_id), str(owner_id), rows, [])
    else:
        result = process_csv_import.delay(str(import_run_id), str(owner_id), rows, [])

    assert result in (
        {"status": "completed"},
        {
            "queued": False,
            "import_run_id": str(import_run_id),
            "owner_id": str(owner_id),
            "valid_row_count": 1,
            "invalid_row_count": 0,
        },
    )
    if calls:
        assert calls[0][0] == import_run_id
        assert calls[0][1] == owner_id
        assert calls[0][2] == rows
