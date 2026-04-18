class AnalyticsError(Exception):
    """Base exception for dashboard analytics read rules."""


class InvalidDashboardPeriodError(AnalyticsError):
    """Raised when a dashboard period filter is unsupported."""


class DashboardDataQualityError(AnalyticsError):
    """Raised when source records cannot produce a reliable dashboard payload."""
