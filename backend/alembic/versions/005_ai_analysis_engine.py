"""ai analysis engine metadata

Revision ID: 005_ai_analysis_engine
Revises: 002_core_domain_data_model
Create Date: 2026-04-19
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "005_ai_analysis_engine"
down_revision: str | None = "002_core_domain_data_model"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("ai_insight_runs", sa.Column("instruction_name", sa.String(length=120), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("instruction_version", sa.String(length=64), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("output_outcome", sa.String(length=32), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"))
    op.add_column("ai_insight_runs", sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"))
    op.add_column("ai_insight_runs", sa.Column("idempotency_key", sa.String(length=128), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("request_id", sa.String(length=128), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("last_failure_stage", sa.String(length=64), nullable=True))
    op.add_column("ai_insight_runs", sa.Column("failure_details", sa.JSON(), nullable=False, server_default="[]"))
    op.create_index("ix_ai_insight_runs_output_outcome", "ai_insight_runs", ["output_outcome"])
    op.create_index("ix_ai_insight_runs_idempotency_key", "ai_insight_runs", ["idempotency_key"])
    op.create_index("ix_ai_insight_runs_owner_status_created", "ai_insight_runs", ["owner_id", "status", "created_at"])
    op.create_index(
        "ix_ai_insight_runs_owner_period_idempotency",
        "ai_insight_runs",
        ["owner_id", "target_period_type", "period_start", "period_end", "idempotency_key"],
    )
    op.create_check_constraint("ck_ai_insight_runs_retry_non_negative", "ai_insight_runs", "retry_count >= 0")
    op.create_check_constraint("ck_ai_insight_runs_max_attempts_positive", "ai_insight_runs", "max_attempts >= 1")


def downgrade() -> None:
    op.drop_constraint("ck_ai_insight_runs_max_attempts_positive", "ai_insight_runs", type_="check")
    op.drop_constraint("ck_ai_insight_runs_retry_non_negative", "ai_insight_runs", type_="check")
    op.drop_index("ix_ai_insight_runs_owner_period_idempotency", table_name="ai_insight_runs")
    op.drop_index("ix_ai_insight_runs_owner_status_created", table_name="ai_insight_runs")
    op.drop_index("ix_ai_insight_runs_idempotency_key", table_name="ai_insight_runs")
    op.drop_index("ix_ai_insight_runs_output_outcome", table_name="ai_insight_runs")
    for column in (
        "failure_details",
        "last_failure_stage",
        "request_id",
        "idempotency_key",
        "max_attempts",
        "retry_count",
        "output_outcome",
        "instruction_version",
        "instruction_name",
    ):
        op.drop_column("ai_insight_runs", column)
