class ImportTraceError(Exception):
    """Base exception for import traceability rules."""


class InvalidImportStatusTransitionError(ImportTraceError):
    """Raised when an import run status transition is not allowed."""


class InvalidImportOutcomeError(ImportTraceError):
    """Raised when an import row outcome is invalid."""


class CSVParsingError(ImportTraceError):
    """Raised when uploaded CSV bytes cannot be decoded or parsed."""


class CSVValidationError(ImportTraceError):
    """Raised when CSV shape or rows fail validation."""


class ImportPermissionError(ImportTraceError):
    """Raised when the current owner cannot access an import run."""


class ImportNotFoundError(ImportTraceError):
    """Raised when an owner-scoped import run is not found."""


class ImportEnqueueError(ImportTraceError):
    """Raised when a confirmed import cannot be delegated to the worker."""


class InvalidImportScheduleError(ImportTraceError):
    """Raised when an import schedule request is invalid."""


class ImportScheduleNotFoundError(ImportTraceError):
    """Raised when an owner-scoped import schedule is not found."""


class ImportScheduleConflictError(ImportTraceError):
    """Raised when an import schedule request conflicts with existing work."""


class DuplicateImportDueWindowError(ImportScheduleConflictError):
    """Raised when a scheduled import due window already exists."""


class UnsupportedImportSourceError(ImportTraceError):
    """Raised when a scheduled import source reference is unsupported."""


class NonRetryableImportScheduleFailureError(ImportTraceError):
    """Raised when a scheduled import failure must not be retried."""


class ImportScheduleRetryExhaustedError(ImportTraceError):
    """Raised when a scheduled import reaches its retry limit."""


class ImportScheduleRetentionError(ImportTraceError):
    """Raised when import schedule history retention rules are violated."""
