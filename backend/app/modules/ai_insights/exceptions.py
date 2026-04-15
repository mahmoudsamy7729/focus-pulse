class AIInsightRunError(Exception):
    """Base exception for AI insight run rules."""


class InvalidAIInsightTargetPeriodError(AIInsightRunError):
    """Raised when a target period is unsupported or malformed."""


class InvalidAIInsightStatusTransitionError(AIInsightRunError):
    """Raised when an AI run status transition is not allowed."""
