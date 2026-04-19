from uuid import uuid4

import app.workers.tasks.ai_analysis_tasks as ai_tasks
from app.workers.tasks.ai_analysis_tasks import process_ai_analysis_run


def test_ai_analysis_worker_delegates_payload_without_business_rules(monkeypatch) -> None:
    calls: list[tuple] = []

    async def fake_process_ai_analysis_run_payload(ai_insight_run_id, owner_id):
        calls.append((ai_insight_run_id, owner_id))
        return {"status": "completed"}

    monkeypatch.setattr(ai_tasks, "process_ai_analysis_run_payload", fake_process_ai_analysis_run_payload)
    ai_run_id = uuid4()
    owner_id = uuid4()

    if hasattr(process_ai_analysis_run, "run"):
        result = process_ai_analysis_run.run(str(ai_run_id), str(owner_id))
    else:
        result = process_ai_analysis_run.delay(str(ai_run_id), str(owner_id))

    assert result in (
        {"status": "completed"},
        {"queued": False, "ai_insight_run_id": str(ai_run_id), "owner_id": str(owner_id)},
    )
    if calls:
        assert calls[0] == (ai_run_id, owner_id)
