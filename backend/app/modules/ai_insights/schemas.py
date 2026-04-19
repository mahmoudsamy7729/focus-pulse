from __future__ import annotations

from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.modules.ai_insights.constants import AI_INSIGHT_DEFAULT_LIMIT, AI_INSIGHT_DEFAULT_PAGE

PeriodGranularity = Literal["daily", "weekly"]
OutputOutcome = Literal["analysis_generated", "no_data"]


class AIInsightRunCreate(BaseModel):
    owner_id: UUID
    target_period_type: PeriodGranularity
    period_start: date
    period_end: date
    source_daily_log_ids: list[UUID]
    idempotency_key: str | None = None
    request_id: str | None = None


class AIInsightRunCreateRequest(BaseModel):
    period_granularity: PeriodGranularity
    anchor_date: date


class NamedMinuteTotal(BaseModel):
    label: str
    total_minutes: int = Field(ge=0)


class DailyMinuteTotal(BaseModel):
    date: date
    total_minutes: int = Field(ge=0)


class AnalysisInputSummary(BaseModel):
    period_granularity: str | None = None
    period_start: date | None = None
    period_end: date | None = None
    source_daily_log_ids: list[UUID] = Field(default_factory=list)
    daily_log_count: int = Field(default=0, ge=0)
    task_count: int = Field(default=0, ge=0)
    total_minutes: int = Field(default=0, ge=0)
    category_totals: list[NamedMinuteTotal] = Field(default_factory=list)
    tag_totals: list[NamedMinuteTotal] = Field(default_factory=list)
    daily_totals: list[DailyMinuteTotal] = Field(default_factory=list)
    included_fields: list[str] = Field(default_factory=lambda: ["task_names", "durations", "categories", "tags"])
    excluded_fields: list[str] = Field(default_factory=lambda: ["note_text"])


class StructuredTaskInput(BaseModel):
    task_id: UUID
    daily_log_id: UUID
    date: date
    title: str
    minutes: int = Field(ge=1)
    category: str
    tags: list[str] = Field(default_factory=list)


class StructuredAIInput(BaseModel):
    period_granularity: PeriodGranularity
    period_start: date
    period_end: date
    tasks: list[StructuredTaskInput] = Field(default_factory=list)
    aggregates: AnalysisInputSummary
    instruction_name: str
    instruction_version: str


class PreparedAIInput(BaseModel):
    provider_input: StructuredAIInput
    source_summary: AnalysisInputSummary
    source_daily_log_ids: list[UUID] = Field(default_factory=list)


class AnalysisInstruction(BaseModel):
    instruction_name: str
    instruction_version: str
    prompt: str
    required_output_sections: list[str]


class SupportingEvidence(BaseModel):
    evidence_id: str
    evidence_type: Literal["date_total", "category_total", "tag_total", "task_count", "task_reference", "duration_outlier"]
    source_date: date | None = None
    source_task_id: UUID | None = None
    label: str | None = None
    minutes: int | None = Field(default=None, ge=0)
    count: int | None = Field(default=None, ge=0)


class AnalysisObservation(BaseModel):
    text: str
    evidence_ids: list[str] = Field(min_length=1)


class CombinedAnalysisOutput(BaseModel):
    output_outcome: OutputOutcome
    generated_at: datetime
    summary: str | None = None
    detected_patterns: list[AnalysisObservation] = Field(default_factory=list)
    behavior_insights: list[AnalysisObservation] = Field(default_factory=list)
    supporting_evidence: list[SupportingEvidence] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class RunFailureDetail(BaseModel):
    stage: str
    reason: str
    attempt_number: int = Field(ge=1, le=3)
    transient: bool
    occurred_at: datetime


class AIInsightRunRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    owner_id: UUID
    target_period_type: str
    period_start: date
    period_end: date
    status: str
    source_summary: dict[str, object]
    output_summary: dict[str, object] | None = None
    failure_reason: str | None = None
    instruction_name: str | None = None
    instruction_version: str | None = None
    output_outcome: str | None = None
    retry_count: int = 0
    max_attempts: int = 3
    idempotency_key: str | None = None
    request_id: str | None = None
    last_failure_stage: str | None = None
    failure_details: list[dict[str, object]] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None


class AIInsightRunDetail(BaseModel):
    id: UUID
    status: str
    period_granularity: str
    period_start: date
    period_end: date
    instruction_name: str | None = None
    instruction_version: str | None = None
    output_outcome: str | None = None
    source_summary: dict[str, object]
    output_summary: dict[str, object] | None = None
    failure_reason: str | None = None
    failure_details: list[dict[str, object]] = Field(default_factory=list)
    retry_count: int = 0
    max_attempts: int = 3
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime


class AIInsightRunAccepted(BaseModel):
    ai_insight_run_id: UUID
    status: str
    period_granularity: str
    period_start: date
    period_end: date
    reused_existing: bool = False


class AIInsightRunPage(BaseModel):
    page: int = Field(default=AI_INSIGHT_DEFAULT_PAGE, ge=1)
    limit: int = Field(default=AI_INSIGHT_DEFAULT_LIMIT, ge=1)
    total: int = Field(ge=0)
    items: list[AIInsightRunDetail]


class CurrentAIInsightRun(BaseModel):
    period_granularity: str
    period_start: date
    period_end: date
    current_run: AIInsightRunDetail | None
