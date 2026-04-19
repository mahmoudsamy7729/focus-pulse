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
