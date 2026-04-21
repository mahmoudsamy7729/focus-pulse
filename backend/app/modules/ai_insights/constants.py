from enum import StrEnum


class AIInsightTargetPeriod(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


class AIInsightInstructionName(StrEnum):
    DAILY_COMBINED_ANALYSIS = "daily_combined_analysis"
    WEEKLY_COMBINED_ANALYSIS = "weekly_combined_analysis"


class AIInsightOutputOutcome(StrEnum):
    ANALYSIS_GENERATED = "analysis_generated"
    NO_DATA = "no_data"


class AIAnalysisAutomationType(StrEnum):
    SCHEDULED_AI_ANALYSIS = "scheduled_ai_analysis"


class AIAnalysisScheduleState(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    DELETED = "deleted"


class AIAnalysisScheduleCadence(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


class AIAnalysisScheduleRunOutcome(StrEnum):
    STARTED = "started"
    COMPLETED = "completed"
    COMPLETED_WITH_ERRORS = "completed_with_errors"
    FAILED = "failed"
    SKIPPED = "skipped"
    NO_DATA = "no_data"


class AIAnalysisScheduleFailureClassification(StrEnum):
    RETRYABLE = "retryable"
    NON_RETRYABLE = "non_retryable"
    EXHAUSTED = "exhausted"


class InsightResultStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"


class InsightScoreState(StrEnum):
    SCORED = "scored"
    INSUFFICIENT_DATA = "insufficient_data"
    NOT_APPLICABLE = "not_applicable"


class InsightConfidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class InsightGenerationReason(StrEnum):
    DEFAULT_GENERATE = "default_generate"
    EXPLICIT_RERUN = "explicit_rerun"


class InsightEvidenceType(StrEnum):
    DATE_TOTAL = "date_total"
    CATEGORY_TOTAL = "category_total"
    TAG_TOTAL = "tag_total"
    TASK_COUNT = "task_count"
    TASK_REFERENCE = "task_reference"
    DURATION_OUTLIER = "duration_outlier"
    PHASE4_PATTERN = "phase4_pattern"
    PHASE4_BEHAVIOR_INSIGHT = "phase4_behavior_insight"


class InsightValidationCode(StrEnum):
    SOURCE_PERIOD_MATCH = "source_period_match"
    PRIVACY_BOUNDARY = "privacy_boundary"
    SCORE_BOUNDS = "score_bounds"
    SCORE_EVIDENCE = "score_evidence"
    DAY_FINDING_EVIDENCE = "day_finding_evidence"
    RECOMMENDATION_COUNT = "recommendation_count"
    RECOMMENDATION_QUALITY = "recommendation_quality"
    CURRENT_RESULT = "current_result"


class AIInsightFailureStage(StrEnum):
    INPUT_PREPARATION = "input_preparation"
    PROVIDER_CALL = "provider_call"
    OUTPUT_VALIDATION = "output_validation"
    PERSISTENCE = "persistence"
    WORKER_EXECUTION = "worker_execution"


AI_INSIGHT_TARGET_PERIODS = {item.value for item in AIInsightTargetPeriod}
AI_INSIGHT_OUTPUT_OUTCOMES = {item.value for item in AIInsightOutputOutcome}
AI_ANALYSIS_SCHEDULE_STATES = {item.value for item in AIAnalysisScheduleState}
AI_ANALYSIS_SCHEDULE_CADENCES = {item.value for item in AIAnalysisScheduleCadence}
AI_ANALYSIS_SCHEDULE_RUN_OUTCOMES = {item.value for item in AIAnalysisScheduleRunOutcome}
AI_ANALYSIS_SCHEDULE_FAILURE_CLASSIFICATIONS = {item.value for item in AIAnalysisScheduleFailureClassification}
INSIGHT_RESULT_STATUSES = {item.value for item in InsightResultStatus}
INSIGHT_SCORE_STATES = {item.value for item in InsightScoreState}
INSIGHT_CONFIDENCE_LEVELS = {item.value for item in InsightConfidence}
INSIGHT_GENERATION_REASONS = {item.value for item in InsightGenerationReason}
INSIGHT_VALIDATOR_VERSION = "2026-04-20.v1"
AI_INSIGHT_INSTRUCTION_VERSION = "2026-04-19.v1"
AI_INSIGHT_MAX_ATTEMPTS = 3
AI_INSIGHT_DEFAULT_PAGE = 1
AI_INSIGHT_DEFAULT_LIMIT = 20
AI_INSIGHT_MAX_LIMIT = 100
AI_INSIGHT_WRITE_RATE_LIMIT_NAME = "ai_insights_write"
AI_INSIGHT_READ_RATE_LIMIT_NAME = "ai_insights_read"
AI_ANALYSIS_SCHEDULE_READ_RATE_LIMIT = "ai_analysis_schedule_read"
AI_ANALYSIS_SCHEDULE_WRITE_RATE_LIMIT = "ai_analysis_schedule_write"
AI_ANALYSIS_SCHEDULE_TRIGGER_RATE_LIMIT = "ai_analysis_schedule_trigger"
AI_ANALYSIS_SCHEDULE_RETENTION_DAYS = 90
AI_ANALYSIS_SCHEDULE_MAX_ATTEMPTS = 3
