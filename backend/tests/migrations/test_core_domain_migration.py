import importlib.util
from pathlib import Path

from app.core.database import Base


EXPECTED_TABLES = {
    "daily_logs",
    "categories",
    "tasks",
    "notes",
    "import_runs",
    "import_row_outcomes",
    "ai_insight_runs",
    "ai_insight_run_sources",
}


def test_core_domain_metadata_contains_expected_tables_columns_and_indexes() -> None:
    assert EXPECTED_TABLES.issubset(Base.metadata.tables)

    daily_logs = Base.metadata.tables["daily_logs"]
    assert {"id", "owner_id", "log_date", "source", "created_at", "updated_at", "deleted_at"}.issubset(
        daily_logs.columns.keys()
    )
    assert "ix_daily_logs_owner_log_date_active" in {index.name for index in daily_logs.indexes}

    tasks = Base.metadata.tables["tasks"]
    assert {"daily_log_id", "category_id", "normalized_title", "time_spent_minutes", "tags"}.issubset(
        tasks.columns.keys()
    )
    assert "ix_tasks_import_dedup" in {index.name for index in tasks.indexes}

    notes = Base.metadata.tables["notes"]
    assert "ix_notes_one_active_per_task" in {index.name for index in notes.indexes}


def test_import_and_ai_traceability_metadata() -> None:
    import_runs = Base.metadata.tables["import_runs"]
    assert {
        "status",
        "processed_row_count",
        "inserted_row_count",
        "invalid_row_count",
        "skipped_row_count",
        "failed_row_count",
        "failure_reason",
    }.issubset(import_runs.columns.keys())

    row_outcomes = Base.metadata.tables["import_row_outcomes"]
    assert {"outcome_type", "reason", "row_snapshot", "normalized_task_name"}.issubset(row_outcomes.columns.keys())

    ai_runs = Base.metadata.tables["ai_insight_runs"]
    assert {"target_period_type", "period_start", "period_end", "source_summary", "output_summary"}.issubset(
        ai_runs.columns.keys()
    )

    ai_sources = Base.metadata.tables["ai_insight_run_sources"]
    assert {"ai_insight_run_id", "daily_log_id"}.issubset(ai_sources.columns.keys())


def test_alembic_revision_creates_phase_1_tables(monkeypatch) -> None:
    revision_path = Path(__file__).parents[2] / "alembic" / "versions" / "002_core_domain_data_model.py"
    spec = importlib.util.spec_from_file_location("core_domain_data_model_revision", revision_path)
    assert spec is not None
    revision = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(revision)

    recorder = MigrationOpRecorder()
    monkeypatch.setattr(revision, "op", recorder)

    revision.upgrade()

    assert EXPECTED_TABLES.issubset(set(recorder.created_tables))
    assert "ix_daily_logs_owner_log_date_active" in recorder.created_indexes
    assert "ix_import_row_outcomes_run_type" in recorder.created_indexes
    assert "ix_ai_insight_run_sources_unique_source" in recorder.created_indexes


class MigrationOpRecorder:
    def __init__(self) -> None:
        self.created_tables: list[str] = []
        self.created_indexes: list[str] = []

    def create_table(self, name: str, *args, **kwargs) -> None:
        self.created_tables.append(name)

    def create_index(self, name: str, table_name: str, columns: list[str], **kwargs) -> None:
        self.created_indexes.append(name)

    def drop_table(self, name: str) -> None:
        pass
