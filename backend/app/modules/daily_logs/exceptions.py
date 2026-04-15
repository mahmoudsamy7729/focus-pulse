class DailyLogError(Exception):
    """Base exception for daily log domain rules."""


class InvalidDailyLogRangeError(DailyLogError):
    """Raised when a date range is inverted."""
