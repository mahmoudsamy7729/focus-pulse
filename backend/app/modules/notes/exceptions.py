class NoteError(Exception):
    """Base exception for note domain rules."""


class ActiveNoteExistsError(NoteError):
    """Raised when a second active note would be created for a task."""
