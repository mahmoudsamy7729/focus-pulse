"""core domain data model

Revision ID: 002_core_domain_data_model
Revises:
Create Date: 2026-04-14
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "002_core_domain_data_model"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def uuid_pk() -> sa.Column:
    return sa.Column("id", sa.Uuid(), primary_key=True, nullable=False)


def owner_id() -> sa.Column:
    return sa.Column("owner_id", sa.Uuid(), nullable=False)


def timestamps(include_deleted: bool = True) -> list[sa.Column]:
    columns = [
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    ]
    if include_deleted:
        columns.append(sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    return columns


def upgrade() -> None:
    op.create_table(
        "daily_logs",
        uuid_pk(),
        owner_id(),
        sa.Column("log_date", sa.Date(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        *timestamps(),
    )
    op.create_index("ix_daily_logs_owner_id", "daily_logs", ["owner_id"])
    op.create_index(
        "ix_daily_logs_owner_log_date_active",
        "daily_logs",
        ["owner_id", "log_date"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
        sqlite_where=sa.text("deleted_at IS NULL"),
    )

    op.create_table(
        "categories",
        uuid_pk(),
        owner_id(),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("normalized_name", sa.String(length=120), nullable=False),
        *timestamps(),
    )
    op.create_index("ix_categories_owner_id", "categories", ["owner_id"])
    op.create_index(
        "ix_categories_owner_normalized_name_active",
        "categories",
        ["owner_id", "normalized_name"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
        sqlite_where=sa.text("deleted_at IS NULL"),
    )

    op.create_table(
        "import_runs",
        uuid_pk(),
        owner_id(),
        sa.Column("source_type", sa.String(length=32), nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("processed_row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("inserted_row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("invalid_row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("skipped_row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_row_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        *timestamps(),
        sa.CheckConstraint("processed_row_count >= 0", name="ck_import_runs_processed_non_negative"),
        sa.CheckConstraint("inserted_row_count >= 0", name="ck_import_runs_inserted_non_negative"),
        sa.CheckConstraint("invalid_row_count >= 0", name="ck_import_runs_invalid_non_negative"),
        sa.CheckConstraint("skipped_row_count >= 0", name="ck_import_runs_skipped_non_negative"),
        sa.CheckConstraint("failed_row_count >= 0", name="ck_import_runs_failed_non_negative"),
    )
    op.create_index("ix_import_runs_owner_id", "import_runs", ["owner_id"])
    op.create_index("ix_import_runs_status", "import_runs", ["status"])
    op.create_index("ix_import_runs_owner_status_created", "import_runs", ["owner_id", "status", "created_at"])

    op.create_table(
        "tasks",
        uuid_pk(),
        owner_id(),
        sa.Column("daily_log_id", sa.Uuid(), sa.ForeignKey("daily_logs.id"), nullable=False),
        sa.Column("category_id", sa.Uuid(), sa.ForeignKey("categories.id"), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("normalized_title", sa.String(length=255), nullable=False),
        sa.Column("time_spent_minutes", sa.Integer(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("source", sa.String(length=32), nullable=False),
        sa.Column("import_run_id", sa.Uuid(), sa.ForeignKey("import_runs.id"), nullable=True),
        *timestamps(),
        sa.CheckConstraint("time_spent_minutes > 0", name="ck_tasks_time_spent_positive"),
    )
    op.create_index("ix_tasks_owner_id", "tasks", ["owner_id"])
    op.create_index("ix_tasks_daily_log_id", "tasks", ["daily_log_id"])
    op.create_index("ix_tasks_category_id", "tasks", ["category_id"])
    op.create_index("ix_tasks_normalized_title", "tasks", ["normalized_title"])
    op.create_index("ix_tasks_import_run_id", "tasks", ["import_run_id"])
    op.create_index("ix_tasks_owner_daily_log", "tasks", ["owner_id", "daily_log_id"])
    op.create_index("ix_tasks_import_dedup", "tasks", ["owner_id", "normalized_title", "time_spent_minutes"])

    op.create_table(
        "notes",
        uuid_pk(),
        owner_id(),
        sa.Column("task_id", sa.Uuid(), sa.ForeignKey("tasks.id"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("import_run_id", sa.Uuid(), sa.ForeignKey("import_runs.id"), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_notes_owner_id", "notes", ["owner_id"])
    op.create_index("ix_notes_task_id", "notes", ["task_id"])
    op.create_index("ix_notes_import_run_id", "notes", ["import_run_id"])
    op.create_index(
        "ix_notes_one_active_per_task",
        "notes",
        ["task_id"],
        unique=True,
        postgresql_where=sa.text("deleted_at IS NULL"),
        sqlite_where=sa.text("deleted_at IS NULL"),
    )

    op.create_table(
        "import_row_outcomes",
        uuid_pk(),
        owner_id(),
        sa.Column("import_run_id", sa.Uuid(), sa.ForeignKey("import_runs.id"), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=True),
        sa.Column("outcome_type", sa.String(length=32), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("normalized_task_name", sa.String(length=255), nullable=True),
        sa.Column("log_date", sa.Date(), nullable=True),
        sa.Column("time_spent_minutes", sa.Integer(), nullable=True),
        sa.Column("row_snapshot", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_import_row_outcomes_owner_id", "import_row_outcomes", ["owner_id"])
    op.create_index("ix_import_row_outcomes_import_run_id", "import_row_outcomes", ["import_run_id"])
    op.create_index("ix_import_row_outcomes_run_type", "import_row_outcomes", ["import_run_id", "outcome_type"])

    op.create_table(
        "ai_insight_runs",
        uuid_pk(),
        owner_id(),
        sa.Column("target_period_type", sa.String(length=32), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("source_summary", sa.JSON(), nullable=False),
        sa.Column("output_summary", sa.JSON(), nullable=True),
        sa.Column("failure_reason", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        *timestamps(),
    )
    op.create_index("ix_ai_insight_runs_owner_id", "ai_insight_runs", ["owner_id"])
    op.create_index("ix_ai_insight_runs_status", "ai_insight_runs", ["status"])
    op.create_index(
        "ix_ai_insight_runs_owner_period",
        "ai_insight_runs",
        ["owner_id", "target_period_type", "period_start", "period_end"],
    )

    op.create_table(
        "ai_insight_run_sources",
        uuid_pk(),
        owner_id(),
        sa.Column("ai_insight_run_id", sa.Uuid(), sa.ForeignKey("ai_insight_runs.id"), nullable=False),
        sa.Column("daily_log_id", sa.Uuid(), sa.ForeignKey("daily_logs.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_insight_run_sources_owner_id", "ai_insight_run_sources", ["owner_id"])
    op.create_index("ix_ai_insight_run_sources_ai_insight_run_id", "ai_insight_run_sources", ["ai_insight_run_id"])
    op.create_index("ix_ai_insight_run_sources_daily_log_id", "ai_insight_run_sources", ["daily_log_id"])
    op.create_index(
        "ix_ai_insight_run_sources_unique_source",
        "ai_insight_run_sources",
        ["ai_insight_run_id", "daily_log_id"],
        unique=True,
    )


def downgrade() -> None:
    for table_name in (
        "ai_insight_run_sources",
        "ai_insight_runs",
        "import_row_outcomes",
        "notes",
        "tasks",
        "import_runs",
        "categories",
        "daily_logs",
    ):
        op.drop_table(table_name)
