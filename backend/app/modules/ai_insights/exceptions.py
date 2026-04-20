class AIInsightRunError(Exception):
    """Base exception for AI insight run rules."""


class InvalidAIInsightTargetPeriodError(AIInsightRunError):
    """Raised when a target period is unsupported or malformed."""


class InvalidAIInsightStatusTransitionError(AIInsightRunError):
    """Raised when an AI run status transition is not allowed."""


class AIInsightNotFoundError(AIInsightRunError):
    """Raised when an AI run is not visible to the current owner."""


class AIInsightConflictError(AIInsightRunError):
    """Raised when a request conflicts with an in-flight or idempotent run."""


class AIInsightEnqueueError(AIInsightRunError):
    """Raised when an AI run cannot be queued."""


class AIProviderFailureError(AIInsightRunError):
    """Raised when the configured AI provider fails."""

    def __init__(self, message: str, *, transient: bool = True) -> None:
        super().__init__(message)
        self.transient = transient


class AIOutputValidationError(AIInsightRunError):
    """Raised when provider output is malformed or unsafe to store."""


class AIInsightIdempotencyConflictError(AIInsightConflictError):
    """Raised when an idempotency key conflicts with another request."""


class InsightResultError(Exception):
    """Base exception for generated insight result rules."""


class InvalidInsightPeriodError(InsightResultError):
    """Raised when an insight result period is unsupported or malformed."""


class MissingSourceAnalysisError(InsightResultError):
    """Raised when no completed Phase 4 source analysis can be used."""


class InvalidSourceAnalysisError(InsightResultError):
    """Raised when a selected source analysis is failed, incomplete, or mismatched."""


class InsightResultNotFoundError(InsightResultError):
    """Raised when an insight result is not visible to the current owner."""


class InsightGenerationConflictError(InsightResultError):
    """Raised when generation would conflict with an existing request/result."""


class InsightValidationFailureError(InsightResultError):
    """Raised when a generated insight result fails blocking validation."""
