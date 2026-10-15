"""Add personal/institutional profile preference, preserving existing groups.

Revision ID: 7ca6e014b982
Revises: 54e1c8bb7901
"""

import sqlalchemy as sa
from alembic import op

revision = "7ca6e014b982"
down_revision = "54e1c8bb7901"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user_profiles") as batch:
        batch.add_column(
            sa.Column("usage_mode", sa.String(20), nullable=False, server_default="personal")
        )
        batch.add_column(sa.Column("institution_name", sa.String(160), nullable=True))
        batch.create_check_constraint(
            op.f("ck_user_profiles_valid_usage_mode"),
            "usage_mode IN ('personal', 'institutional')",
        )
    op.execute(
        sa.text(
            "UPDATE user_profiles SET usage_mode = 'institutional' "
            "WHERE grade IS NOT NULL AND trim(grade) <> ''"
        )
    )


def downgrade():
    # Disposable databases only: live rollback retains these additive columns.
    with op.batch_alter_table("user_profiles") as batch:
        batch.drop_constraint(op.f("ck_user_profiles_valid_usage_mode"), type_="check")
        batch.drop_column("institution_name")
        batch.drop_column("usage_mode")
