from pathlib import Path

from app.modules.ai_insights.models import AIInsightRun


def test_ai_analysis_engine_model_exposes_phase_4_metadata() -> None:
    columns = AIInsightRun.__table__.columns

    for name in (
        "instruction_name",
        "instruction_version",
        "output_outcome",
        "retry_count",
        "max_attempts",
        "idempotency_key",
        "request_id",
        "last_failure_stage",
        "failure_details",
    ):
        assert name in columns


def test_ai_analysis_engine_migration_documents_metadata_columns() -> None:
    migration = Path("alembic/versions/005_ai_analysis_engine.py")
    assert migration.exists()
    content = migration.read_text(encoding="utf-8")

    assert "instruction_name" in content
    assert "failure_details" in content
