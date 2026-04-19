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


class AIInsightFailureStage(StrEnum):
    INPUT_PREPARATION = "input_preparation"
    PROVIDER_CALL = "provider_call"
    OUTPUT_VALIDATION = "output_validation"
    PERSISTENCE = "persistence"
    WORKER_EXECUTION = "worker_execution"


AI_INSIGHT_TARGET_PERIODS = {item.value for item in AIInsightTargetPeriod}
AI_INSIGHT_OUTPUT_OUTCOMES = {item.value for item in AIInsightOutputOutcome}
AI_INSIGHT_INSTRUCTION_VERSION = "2026-04-19.v1"
AI_INSIGHT_MAX_ATTEMPTS = 3
AI_INSIGHT_DEFAULT_PAGE = 1
AI_INSIGHT_DEFAULT_LIMIT = 20
AI_INSIGHT_MAX_LIMIT = 100
AI_INSIGHT_WRITE_RATE_LIMIT_NAME = "ai_insights_write"
AI_INSIGHT_READ_RATE_LIMIT_NAME = "ai_insights_read"
