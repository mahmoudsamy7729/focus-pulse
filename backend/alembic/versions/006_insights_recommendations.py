"""insights recommendations results

Revision ID: 006_insights_recommendations
Revises: 005_ai_analysis_engine
Create Date: 2026-04-20
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "006_insights_recommendations"
down_revision: str | None = "005_ai_analysis_engine"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ai_insight_results",
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("period_granularity", sa.String(length=32), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("source_ai_insight_run_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("is_current", sa.Boolean(), nullable=False),
        sa.Column("generation_reason", sa.String(length=32), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.Column("source_snapshot", sa.JSON(), nullable=False),
        sa.Column("productivity_score", sa.JSON(), nullable=False),
        sa.Column("consistency_score", sa.JSON(), nullable=True),
        sa.Column("best_day_finding", sa.JSON(), nullable=True),
        sa.Column("worst_day_finding", sa.JSON(), nullable=True),
        sa.Column("recommendations", sa.JSON(), nullable=False),
        sa.Column("evidence", sa.JSON(), nullable=False),
        sa.Column("validation_outcome", sa.JSON(), nullable=False),
        sa.Column("failure_code", sa.String(length=120), nullable=True),
        sa.Column("failure_details", sa.JSON(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("period_end >= period_start", name="ck_ai_insight_results_period_order"),
        sa.ForeignKeyConstraint(["source_ai_insight_run_id"], ["ai_insight_runs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_insight_results_owner_id", "ai_insight_results", ["owner_id"])
    op.create_index("ix_ai_insight_results_status", "ai_insight_results", ["status"])
    op.create_index("ix_ai_insight_results_source_ai_insight_run_id", "ai_insight_results", ["source_ai_insight_run_id"])
    op.create_index("ix_ai_insight_results_idempotency_key", "ai_insight_results", ["idempotency_key"])
    op.create_index("ix_ai_insight_results_idempotency", "ai_insight_results", ["owner_id", "idempotency_key"])
    op.create_index("ix_ai_insight_results_owner_generated", "ai_insight_results", ["owner_id", "generated_at"])
    op.create_index(
        "ix_ai_insight_results_owner_period_current",
        "ai_insight_results",
        ["owner_id", "period_granularity", "period_start", "period_end", "is_current"],
    )
    op.create_index(
        "ix_ai_insight_results_default_reuse",
        "ai_insight_results",
        ["owner_id", "period_granularity", "period_start", "period_end", "source_ai_insight_run_id", "status"],
    )

    op.create_table(
        "ai_insight_result_sources",
        sa.Column("owner_id", sa.Uuid(), nullable=False),
        sa.Column("ai_insight_result_id", sa.Uuid(), nullable=False),
        sa.Column("daily_log_id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["ai_insight_result_id"], ["ai_insight_results.id"]),
        sa.ForeignKeyConstraint(["daily_log_id"], ["daily_logs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_ai_insight_result_sources_owner_id", "ai_insight_result_sources", ["owner_id"])
    op.create_index("ix_ai_insight_result_sources_ai_insight_result_id", "ai_insight_result_sources", ["ai_insight_result_id"])
    op.create_index("ix_ai_insight_result_sources_daily_log_id", "ai_insight_result_sources", ["daily_log_id"])
    op.create_index(
        "ix_ai_insight_result_sources_unique_source",
        "ai_insight_result_sources",
        ["ai_insight_result_id", "daily_log_id"],
        unique=True,
    )
    op.create_index(
        "ix_ai_insight_result_sources_owner_result",
        "ai_insight_result_sources",
        ["owner_id", "ai_insight_result_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_ai_insight_result_sources_owner_result", table_name="ai_insight_result_sources")
    op.drop_index("ix_ai_insight_result_sources_unique_source", table_name="ai_insight_result_sources")
    op.drop_index("ix_ai_insight_result_sources_daily_log_id", table_name="ai_insight_result_sources")
    op.drop_index("ix_ai_insight_result_sources_ai_insight_result_id", table_name="ai_insight_result_sources")
    op.drop_index("ix_ai_insight_result_sources_owner_id", table_name="ai_insight_result_sources")
    op.drop_table("ai_insight_result_sources")
    op.drop_index("ix_ai_insight_results_default_reuse", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_owner_period_current", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_owner_generated", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_idempotency", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_idempotency_key", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_source_ai_insight_run_id", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_status", table_name="ai_insight_results")
    op.drop_index("ix_ai_insight_results_owner_id", table_name="ai_insight_results")
    op.drop_table("ai_insight_results")
