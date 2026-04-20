from app.core.database import Base


def test_insight_result_tables_are_registered_in_metadata() -> None:
    result_table = Base.metadata.tables["ai_insight_results"]
    source_table = Base.metadata.tables["ai_insight_result_sources"]

    assert "source_snapshot" in result_table.c
    assert "productivity_score" in result_table.c
    assert "validation_outcome" in result_table.c
    assert "deleted_at" in result_table.c
    assert source_table.c.ai_insight_result_id.foreign_keys
