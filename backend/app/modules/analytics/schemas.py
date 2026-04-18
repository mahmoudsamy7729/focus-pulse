from datetime import date
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


PeriodType = Literal["day", "week", "month"]


class EmptyState(BaseModel):
    code: str
    message: str


class DashboardPeriod(BaseModel):
    period_type: PeriodType
    anchor_date: date
    start_date: date
    end_date: date
    label: str


class NamedTimeTotal(BaseModel):
    label: str
    total_minutes: int = Field(ge=0)
    display_total: str


class DashboardSummary(BaseModel):
    total_minutes: int = Field(ge=0)
    display_total: str
    task_count: int = Field(ge=0)
    daily_log_count: int = Field(ge=0)
    highest_time_category: NamedTimeTotal | None = None
    average_minutes_per_logged_day: int | None = Field(default=None, ge=0)


class DailyLogListItem(BaseModel):
    date: date
    total_minutes: int = Field(ge=0)
    display_total: str
    task_count: int = Field(ge=0)
    top_category: NamedTimeTotal | None = None


class PeriodTimeTimelinePoint(BaseModel):
    date: date
    total_minutes: int = Field(ge=0)
    display_total: str
    has_tasks: bool


class CategoryBreakdownItem(BaseModel):
    label: str
    total_minutes: int = Field(ge=0)
    display_total: str
    share_of_total: float = Field(ge=0, le=1)
    is_other: bool


class TagBreakdownItem(BaseModel):
    label: str
    total_minutes: int = Field(ge=0)
    display_total: str
    share_label: str
    is_untagged: bool
    is_other: bool


class DashboardOverview(BaseModel):
    period: DashboardPeriod
    summary: DashboardSummary
    daily_logs: list[DailyLogListItem] = Field(default_factory=list)
    period_timeline: list[PeriodTimeTimelinePoint] = Field(default_factory=list)
    category_breakdown: list[CategoryBreakdownItem] = Field(default_factory=list)
    tag_breakdown: list[TagBreakdownItem] = Field(default_factory=list)
    tag_total_notice: str | None = None
    empty_state: EmptyState | None = None


class DashboardTaskRow(BaseModel):
    id: UUID
    log_date: date
    title: str
    time_spent_minutes: int = Field(gt=0)
    category: str
    tags: list[str] = Field(default_factory=list)
    source: str
