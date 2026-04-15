class TaskError(Exception):
    """Base exception for task domain rules."""


class InvalidTaskError(TaskError):
    """Raised when task input violates domain rules."""
