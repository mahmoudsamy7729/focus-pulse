from datetime import datetime, timezone
from uuid import UUID

from app.workers.schedule_windows import (
    AutomationType,
    ScheduleCadence,
    build_schedule_idempotency_key,
    resolve_due_windows,
)


OWNER_ID = UUID("00000000-0000-4000-8000-000000000001")
SCHEDULE_ID = UUID("00000000-0000-4000-8000-000000000101")


def test_daily_window_uses_previous_local_day_at_run_time() -> None:
    selection = resolve_due_windows(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_IMPORT,
        cadence=ScheduleCadence.DAILY,
        local_run_time="06:00",
        timezone_name="Africa/Cairo",
        now=datetime(2026, 4, 21, 4, 30, tzinfo=timezone.utc),
    )

    assert selection.skipped_windows == ()
    assert selection.process_window is not None
    assert selection.process_window.window_start.isoformat() == "2026-04-20"
    assert selection.process_window.window_end.isoformat() == "2026-04-20"
    assert selection.process_window.due_at.isoformat() == "2026-04-21T04:00:00+00:00"


def test_weekly_window_uses_previous_monday_to_sunday() -> None:
    selection = resolve_due_windows(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_AI_ANALYSIS,
        cadence=ScheduleCadence.WEEKLY,
        local_run_time="07:00",
        timezone_name="Africa/Cairo",
        now=datetime(2026, 4, 27, 5, 30, tzinfo=timezone.utc),
    )

    assert selection.process_window is not None
    assert selection.process_window.window_start.isoformat() == "2026-04-20"
    assert selection.process_window.window_end.isoformat() == "2026-04-26"
    assert selection.process_window.due_at.isoformat() == "2026-04-27T04:00:00+00:00"


def test_latest_missed_window_is_processed_and_older_windows_are_skipped() -> None:
    selection = resolve_due_windows(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_IMPORT,
        cadence=ScheduleCadence.DAILY,
        local_run_time="06:00",
        timezone_name="Africa/Cairo",
        now=datetime(2026, 4, 21, 4, 30, tzinfo=timezone.utc),
        last_evaluated_due_at=datetime(2026, 4, 18, 3, 0, tzinfo=timezone.utc),
    )

    assert len(selection.skipped_windows) == 2
    assert [window.window_start.isoformat() for window in selection.skipped_windows] == [
        "2026-04-18",
        "2026-04-19",
    ]
    assert selection.process_window is not None
    assert selection.process_window.window_start.isoformat() == "2026-04-20"
    assert selection.process_window.is_latest_missed_window is True
    assert selection.process_window.missed_window_count == 2


def test_schedule_idempotency_key_is_stable_and_source_sensitive() -> None:
    base_key = build_schedule_idempotency_key(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_IMPORT,
        window_start=datetime(2026, 4, 20, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 21, tzinfo=timezone.utc),
        target_fingerprint="source-a",
    )
    same_key = build_schedule_idempotency_key(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_IMPORT,
        window_start=datetime(2026, 4, 20, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 21, tzinfo=timezone.utc),
        target_fingerprint="source-a",
    )
    other_key = build_schedule_idempotency_key(
        owner_id=OWNER_ID,
        schedule_id=SCHEDULE_ID,
        automation_type=AutomationType.SCHEDULED_IMPORT,
        window_start=datetime(2026, 4, 20, tzinfo=timezone.utc),
        window_end=datetime(2026, 4, 21, tzinfo=timezone.utc),
        target_fingerprint="source-b",
    )

    assert base_key == same_key
    assert base_key != other_key
