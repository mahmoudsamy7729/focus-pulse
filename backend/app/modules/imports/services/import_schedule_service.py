"""Import schedule management placeholder for Phase 6 automation."""

from __future__ import annotations

from app.modules.imports.repositories.import_schedule_repository import ImportScheduleRepository


class ImportScheduleService:
    def __init__(self, repository: ImportScheduleRepository) -> None:
        self.repository = repository
