"""Shared schedule window value objects for Phase 6 automation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone
from enum import StrEnum
from hashlib import sha256
from uuid import UUID
from zoneinfo import ZoneInfo


class AutomationType(StrEnum):
    SCHEDULED_IMPORT = "scheduled_import"
    SCHEDULED_AI_ANALYSIS = "scheduled_ai_analysis"


class ScheduleCadence(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass(frozen=True)
class ScheduleWindow:
    schedule_id: UUID
    automation_type: AutomationType
    due_at: datetime
    window_start: date | datetime
    window_end: date | datetime
    is_latest_missed_window: bool
    missed_window_count: int
    idempotency_key: str


@dataclass(frozen=True)
class ScheduleWindowSelection:
    process_window: ScheduleWindow | None
    skipped_windows: tuple[ScheduleWindow, ...]


def parse_local_run_time(value: str | time) -> time:
    if isinstance(value, time):
        return value.replace(tzinfo=None)
    try:
        hour, minute = value.split(":", maxsplit=1)
        return time(int(hour), int(minute))
    except (TypeError, ValueError) as exc:
        raise ValueError("local_run_time must use HH:MM format") from exc


def build_schedule_idempotency_key(
    *,
    owner_id: UUID,
    schedule_id: UUID,
    automation_type: AutomationType,
    window_start: date | datetime,
    window_end: date | datetime,
    target_fingerprint: str | None = None,
) -> str:
    parts = [
        str(owner_id),
        str(schedule_id),
        automation_type.value,
        window_start.isoformat(),
        window_end.isoformat(),
        target_fingerprint or "",
    ]
    return sha256("|".join(parts).encode("utf-8")).hexdigest()


def resolve_due_windows(
    *,
    owner_id: UUID,
    schedule_id: UUID,
    automation_type: AutomationType,
    cadence: ScheduleCadence,
    local_run_time: str | time,
    timezone_name: str,
    now: datetime,
    last_evaluated_due_at: datetime | None = None,
    target_fingerprint: str | None = None,
) -> ScheduleWindowSelection:
    local_zone = ZoneInfo(timezone_name)
    local_now = _as_aware_utc(now).astimezone(local_zone)
    run_time = parse_local_run_time(local_run_time)
    last_local_due = last_evaluated_due_at.astimezone(local_zone) if last_evaluated_due_at else None
    due_dates = _daily_due_dates(local_now, run_time, last_local_due) if cadence == ScheduleCadence.DAILY else _weekly_due_dates(local_now, run_time, last_local_due)

    windows = tuple(
        _build_window(
            owner_id=owner_id,
            schedule_id=schedule_id,
            automation_type=automation_type,
            cadence=cadence,
            local_zone=local_zone,
            run_time=run_time,
            due_date=due_date,
            missed_window_count=max(0, len(due_dates) - 1),
            target_fingerprint=target_fingerprint,
        )
        for due_date in due_dates
    )
    if not windows:
        return ScheduleWindowSelection(process_window=None, skipped_windows=())
    return ScheduleWindowSelection(process_window=windows[-1], skipped_windows=windows[:-1])


def _as_aware_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _daily_due_dates(
    local_now: datetime,
    run_time: time,
    last_local_due: datetime | None,
) -> list[date]:
    latest_due_date = local_now.date()
    if datetime.combine(latest_due_date, run_time, local_now.tzinfo) > local_now:
        latest_due_date -= timedelta(days=1)
    if last_local_due is None:
        return [latest_due_date] if latest_due_date < local_now.date() or datetime.combine(latest_due_date, run_time, local_now.tzinfo) <= local_now else []
    start = last_local_due.date() + timedelta(days=1)
    return _date_range(start, latest_due_date)


def _weekly_due_dates(
    local_now: datetime,
    run_time: time,
    last_local_due: datetime | None,
) -> list[date]:
    this_monday = local_now.date() - timedelta(days=local_now.weekday())
    latest_due_date = this_monday
    if datetime.combine(latest_due_date, run_time, local_now.tzinfo) > local_now:
        latest_due_date -= timedelta(days=7)
    if last_local_due is None:
        return [latest_due_date] if latest_due_date <= local_now.date() else []
    start = last_local_due.date() + timedelta(days=7)
    due_dates: list[date] = []
    current = start
    while current <= latest_due_date:
        due_dates.append(current)
        current += timedelta(days=7)
    return due_dates


def _date_range(start: date, end: date) -> list[date]:
    if start > end:
        return []
    return [start + timedelta(days=offset) for offset in range((end - start).days + 1)]


def _build_window(
    *,
    owner_id: UUID,
    schedule_id: UUID,
    automation_type: AutomationType,
    cadence: ScheduleCadence,
    local_zone: ZoneInfo,
    run_time: time,
    due_date: date,
    missed_window_count: int,
    target_fingerprint: str | None,
) -> ScheduleWindow:
    due_at = datetime.combine(due_date, run_time, local_zone).astimezone(timezone.utc)
    if cadence == ScheduleCadence.DAILY:
        window_start = due_date - timedelta(days=1)
        window_end = window_start
    else:
        window_start = due_date - timedelta(days=7)
        window_end = due_date - timedelta(days=1)
    return ScheduleWindow(
        schedule_id=schedule_id,
        automation_type=automation_type,
        due_at=due_at,
        window_start=window_start,
        window_end=window_end,
        is_latest_missed_window=missed_window_count > 0,
        missed_window_count=missed_window_count,
        idempotency_key=build_schedule_idempotency_key(
            owner_id=owner_id,
            schedule_id=schedule_id,
            automation_type=automation_type,
            window_start=window_start,
            window_end=window_end,
            target_fingerprint=target_fingerprint,
        ),
    )
