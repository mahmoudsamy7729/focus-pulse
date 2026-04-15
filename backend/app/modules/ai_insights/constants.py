from enum import StrEnum


class AIInsightTargetPeriod(StrEnum):
    DAILY = "daily"
    WEEKLY = "weekly"


AI_INSIGHT_TARGET_PERIODS = {item.value for item in AIInsightTargetPeriod}
