"""Add personal goals and daily check-ins without changing existing data.

Revision ID: 54e1c8bb7901
Revises: 208469fd48ef
"""

import sqlalchemy as sa
from alembic import op

revision = "54e1c8bb7901"
down_revision = "208469fd48ef"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user_goals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("target_days", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "target_days BETWEEN 1 AND 7", name=op.f("ck_user_goals_valid_target_days")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name=op.f("fk_user_goals_user_id_users"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["habit_id"],
            ["habits.id"],
            name=op.f("fk_user_goals_habit_id_habits"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user_goals")),
        sa.UniqueConstraint("user_id", "habit_id", name="uq_user_goal_habit"),
    )
    op.create_table(
        "daily_checkins",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("checked_on", sa.Date(), nullable=False),
        sa.Column("energy", sa.Integer(), nullable=False),
        sa.Column("focus", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint("energy BETWEEN 1 AND 5", name=op.f("ck_daily_checkins_valid_energy")),
        sa.CheckConstraint("focus BETWEEN 1 AND 5", name=op.f("ck_daily_checkins_valid_focus")),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_daily_checkins_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_daily_checkins")),
        sa.UniqueConstraint("user_id", "checked_on", name="uq_user_daily_checkin"),
    )


def downgrade():
    # Only for disposable environments: this removes goals and reflections.
    op.drop_table("daily_checkins")
    op.drop_table("user_goals")
