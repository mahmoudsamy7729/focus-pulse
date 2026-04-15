class ImportTraceError(Exception):
    """Base exception for import traceability rules."""


class InvalidImportStatusTransitionError(ImportTraceError):
    """Raised when an import run status transition is not allowed."""


class InvalidImportOutcomeError(ImportTraceError):
    """Raised when an import row outcome is invalid."""
