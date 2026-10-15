"""School membership, protected teaching workspace and descriptive growth snapshots.

Revision ID: a903b5d7e214
Revises: 7ca6e014b982
"""

import sqlalchemy as sa
from alembic import op

revision = "a903b5d7e214"
down_revision = "7ca6e014b982"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "schools",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=60), nullable=False),
        sa.Column("name", sa.String(length=160), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_schools")),
        sa.UniqueConstraint("code", name=op.f("uq_schools_code")),
    )
    op.create_table(
        "routine_completions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("routine_slug", sa.String(length=60), nullable=False),
        sa.Column("habit_id", sa.Integer(), nullable=False),
        sa.Column("completed_on", sa.Date(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["habit_id"],
            ["habits.id"],
            name=op.f("fk_routine_completions_habit_id_habits"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_routine_completions_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_routine_completions")),
        sa.UniqueConstraint("user_id", "routine_slug", "completed_on", name="uq_routine_daily"),
    )
    with op.batch_alter_table("routine_completions", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_routine_completions_habit_id"), ["habit_id"], unique=False
        )
        batch_op.create_index(
            batch_op.f("ix_routine_completions_user_id"), ["user_id"], unique=False
        )

    op.create_table(
        "school_groups",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("academic_year", sa.Integer(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "academic_year BETWEEN 2020 AND 2100", name=op.f("ck_school_groups_valid_academic_year")
        ),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["schools.id"],
            name=op.f("fk_school_groups_school_id_schools"),
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_school_groups")),
        sa.UniqueConstraint("id", "school_id", name="uq_school_group_id_school"),
        sa.UniqueConstraint("school_id", "academic_year", "name", name="uq_school_group_year_name"),
    )
    with op.batch_alter_table("school_groups", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_school_groups_school_id"), ["school_id"], unique=False)

    op.create_table(
        "school_memberships",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("requested_role", sa.String(length=12), nullable=False),
        sa.Column("status", sa.String(length=12), nullable=False),
        sa.Column("allow_aggregate", sa.Boolean(), nullable=False),
        sa.Column("aggregate_since", sa.DateTime(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=True),
        sa.Column("reviewed_by_user_id", sa.Integer(), nullable=True),
        sa.Column("authorization_confirmed", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.CheckConstraint(
            "requested_role IN ('student', 'teacher')",
            name=op.f("ck_school_memberships_valid_school_role"),
        ),
        sa.CheckConstraint(
            "status IN ('pending', 'approved', 'rejected', 'revoked')",
            name=op.f("ck_school_memberships_valid_membership_status"),
        ),
        sa.ForeignKeyConstraint(
            ["group_id", "school_id"],
            ["school_groups.id", "school_groups.school_id"],
            name="fk_school_membership_group_school",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["reviewed_by_user_id"],
            ["users.id"],
            name=op.f("fk_school_memberships_reviewed_by_user_id_users"),
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["school_id"],
            ["schools.id"],
            name=op.f("fk_school_memberships_school_id_schools"),
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_school_memberships_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_school_memberships")),
        sa.UniqueConstraint("id", "school_id", name="uq_school_membership_id_school"),
        sa.UniqueConstraint("user_id", name=op.f("uq_school_memberships_user_id")),
    )
    with op.batch_alter_table("school_memberships", schema=None) as batch_op:
        batch_op.create_index("ix_membership_group_status", ["group_id", "status"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_school_memberships_reviewed_by_user_id"),
            ["reviewed_by_user_id"],
            unique=False,
        )
        batch_op.create_index(
            batch_op.f("ix_school_memberships_school_id"), ["school_id"], unique=False
        )

    op.create_table(
        "teacher_group_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("membership_id", sa.Integer(), nullable=False),
        sa.Column("school_id", sa.Integer(), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["group_id", "school_id"],
            ["school_groups.id", "school_groups.school_id"],
            name="fk_assignment_group_school",
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["membership_id", "school_id"],
            ["school_memberships.id", "school_memberships.school_id"],
            name="fk_assignment_membership_school",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_teacher_group_assignments")),
        sa.UniqueConstraint("membership_id", "group_id", name="uq_teacher_group"),
    )
    with op.batch_alter_table("teacher_group_assignments", schema=None) as batch_op:
        batch_op.create_index("ix_assignment_group", ["group_id"], unique=False)

    with op.batch_alter_table("health_measurements", schema=None) as batch_op:
        batch_op.drop_constraint(op.f("ck_health_measurements_valid_weight"), type_="check")
        batch_op.drop_constraint(op.f("ck_health_measurements_valid_height"), type_="check")
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_weight"), "weight_kg BETWEEN 10 AND 500"
        )
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_height"), "height_cm BETWEEN 50 AND 250"
        )
        batch_op.add_column(sa.Column("age_months", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("reference_sex", sa.String(length=12), nullable=True))
        batch_op.add_column(sa.Column("reference_source", sa.String(length=32), nullable=True))
        batch_op.add_column(
            sa.Column("growth_percentile", sa.Numeric(precision=5, scale=2), nullable=True)
        )
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_growth_percentile"),
            "growth_percentile IS NULL OR growth_percentile BETWEEN 0 AND 100",
        )
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_measurement_reference_sex"),
            "reference_sex IS NULL OR reference_sex IN ('male', 'female')",
        )

    with op.batch_alter_table("user_profiles", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "reference_sex", sa.String(length=12), server_default="unspecified", nullable=False
            )
        )
        batch_op.add_column(
            sa.Column(
                "movement_goal", sa.String(length=12), server_default="energy", nullable=False
            )
        )
        batch_op.create_check_constraint(
            op.f("ck_user_profiles_valid_reference_sex"),
            "reference_sex IN ('unspecified', 'female', 'male')",
        )
        batch_op.create_check_constraint(
            op.f("ck_user_profiles_valid_movement_goal"),
            "movement_goal IN ('center', 'energy', 'strength')",
        )


def downgrade():
    # Disposable databases only. Live rollback keeps additive schema and all data.
    with op.batch_alter_table("user_profiles", schema=None) as batch_op:
        batch_op.drop_constraint(op.f("ck_user_profiles_valid_reference_sex"), type_="check")
        batch_op.drop_constraint(op.f("ck_user_profiles_valid_movement_goal"), type_="check")
        batch_op.drop_column("movement_goal")
        batch_op.drop_column("reference_sex")

    with op.batch_alter_table("health_measurements", schema=None) as batch_op:
        batch_op.drop_constraint(
            op.f("ck_health_measurements_valid_growth_percentile"), type_="check"
        )
        batch_op.drop_constraint(
            op.f("ck_health_measurements_valid_measurement_reference_sex"), type_="check"
        )
        batch_op.drop_constraint(op.f("ck_health_measurements_valid_weight"), type_="check")
        batch_op.drop_constraint(op.f("ck_health_measurements_valid_height"), type_="check")
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_weight"), "weight_kg BETWEEN 20 AND 500"
        )
        batch_op.create_check_constraint(
            op.f("ck_health_measurements_valid_height"), "height_cm BETWEEN 80 AND 250"
        )
        batch_op.drop_column("growth_percentile")
        batch_op.drop_column("reference_source")
        batch_op.drop_column("reference_sex")
        batch_op.drop_column("age_months")

    with op.batch_alter_table("teacher_group_assignments", schema=None) as batch_op:
        batch_op.drop_index("ix_assignment_group")

    op.drop_table("teacher_group_assignments")
    with op.batch_alter_table("school_memberships", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_school_memberships_school_id"))
        batch_op.drop_index(batch_op.f("ix_school_memberships_reviewed_by_user_id"))
        batch_op.drop_index("ix_membership_group_status")

    op.drop_table("school_memberships")
    with op.batch_alter_table("school_groups", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_school_groups_school_id"))

    op.drop_table("school_groups")
    with op.batch_alter_table("routine_completions", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_routine_completions_user_id"))
        batch_op.drop_index(batch_op.f("ix_routine_completions_habit_id"))

    op.drop_table("routine_completions")
    op.drop_table("schools")
