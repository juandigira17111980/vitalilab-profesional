"""One-time personalization, manual enrollment requests and private routines.

Revision ID: c842d6e190ab
Revises: a903b5d7e214
"""

import sqlalchemy as sa
from alembic import op

revision = "c842d6e190ab"
down_revision = "a903b5d7e214"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user_profiles") as batch:
        batch.add_column(
            sa.Column(
                "movement_preference", sa.String(12), nullable=False, server_default="adaptable"
            )
        )
        batch.add_column(sa.Column("personalization_completed_at", sa.DateTime(), nullable=True))
        batch.add_column(sa.Column("measurement_consent_at", sa.DateTime(), nullable=True))
        batch.create_check_constraint(
            op.f("ck_user_profiles_valid_movement_preference"),
            "movement_preference IN ('adaptable', 'seated', 'supported', 'standing')",
        )
    op.create_table(
        "school_enrollment_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("school_name", sa.String(160), nullable=False),
        sa.Column("group_name", sa.String(80), nullable=False),
        sa.Column("requested_role", sa.String(12), nullable=False),
        sa.Column("status", sa.String(12), nullable=False),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "requested_role IN ('student', 'teacher')",
            name=op.f("ck_school_enrollment_requests_valid_requested_role"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'resolved', 'rejected', 'cancelled')",
            name=op.f("ck_school_enrollment_requests_valid_enrollment_status"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
            name=op.f("fk_school_enrollment_requests_user_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["reviewed_by_user_id"],
            ["users.id"],
            ondelete="SET NULL",
            name=op.f("fk_school_enrollment_requests_reviewed_by_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_school_enrollment_requests")),
        sa.UniqueConstraint("user_id", name=op.f("uq_school_enrollment_requests_user_id")),
    )
    op.create_index(
        "ix_enrollment_status_created", "school_enrollment_requests", ["status", "created_at"]
    )
    op.create_index(
        op.f("ix_school_enrollment_requests_reviewed_by_user_id"),
        "school_enrollment_requests",
        ["reviewed_by_user_id"],
    )
    op.create_table(
        "personal_routines",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("description", sa.String(500), nullable=False),
        sa.Column("goal", sa.String(12), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "goal IN ('center', 'energy', 'strength')",
            name=op.f("ck_personal_routines_valid_routine_goal"),
        ),
        sa.CheckConstraint(
            "revision >= 1", name=op.f("ck_personal_routines_valid_routine_revision")
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
            name=op.f("fk_personal_routines_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_personal_routines")),
    )
    op.create_index("ix_personal_routines_user_active", "personal_routines", ["user_id", "active"])
    op.create_table(
        "routine_exercises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("routine_id", sa.Integer(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("sets", sa.Integer(), nullable=False),
        sa.Column("repetitions", sa.Integer(), nullable=True),
        sa.Column("duration_seconds", sa.Integer(), nullable=True),
        sa.Column("rest_seconds", sa.Integer(), nullable=False),
        sa.Column("instructions", sa.String(280), nullable=False),
        sa.Column("visual", sa.String(12), nullable=False),
        sa.CheckConstraint(
            "position BETWEEN 0 AND 11", name=op.f("ck_routine_exercises_valid_exercise_position")
        ),
        sa.CheckConstraint(
            "sets BETWEEN 1 AND 20", name=op.f("ck_routine_exercises_valid_exercise_sets")
        ),
        sa.CheckConstraint(
            "repetitions IS NULL OR repetitions BETWEEN 1 AND 200",
            name=op.f("ck_routine_exercises_valid_exercise_reps"),
        ),
        sa.CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds BETWEEN 5 AND 3600",
            name=op.f("ck_routine_exercises_valid_exercise_duration"),
        ),
        sa.CheckConstraint(
            "repetitions IS NOT NULL OR duration_seconds IS NOT NULL",
            name=op.f("ck_routine_exercises_exercise_has_dose"),
        ),
        sa.CheckConstraint(
            "rest_seconds BETWEEN 0 AND 600", name=op.f("ck_routine_exercises_valid_exercise_rest")
        ),
        sa.CheckConstraint(
            "visual IN ('posture', 'march', 'palms', 'shoulders', "
            "'wall', 'walk', 'breathing', 'custom')",
            name=op.f("ck_routine_exercises_valid_exercise_visual"),
        ),
        sa.ForeignKeyConstraint(
            ["routine_id"],
            ["personal_routines.id"],
            ondelete="CASCADE",
            name=op.f("fk_routine_exercises_routine_id_personal_routines"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_routine_exercises")),
        sa.UniqueConstraint("routine_id", "position", name="uq_routine_exercise_position"),
    )


def downgrade():
    # Destructive: disposable databases only. A live code rollback keeps this additive schema.
    op.drop_table("routine_exercises")
    op.drop_table("personal_routines")
    op.drop_table("school_enrollment_requests")
    with op.batch_alter_table("user_profiles") as batch:
        batch.drop_constraint(op.f("ck_user_profiles_valid_movement_preference"), type_="check")
        batch.drop_column("measurement_consent_at")
        batch.drop_column("personalization_completed_at")
        batch.drop_column("movement_preference")
