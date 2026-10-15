"""Seed a small legacy fixture before upgrading the disposable PostgreSQL CI database."""

from datetime import date, datetime

from sqlalchemy import MetaData, Table, text

from app import create_app
from app.extensions import db


def seed():
    app = create_app()
    with app.app_context():
        if db.engine.dialect.name != "postgresql" or db.engine.url.database != "vitalilab_test":
            raise RuntimeError("Refusing writes outside the disposable PostgreSQL CI database")
        assert (
            db.session.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
            == "a903b5d7e214"
        )
        metadata = MetaData()
        users, profiles, measurements = (
            Table(name, metadata, autoload_with=db.engine)
            for name in ("users", "user_profiles", "health_measurements")
        )
        now = datetime(2026, 10, 14, 12)
        user_id = db.session.execute(
            users.insert()
            .values(
                email="ci-before-migration@example.com",
                password_hash="not-a-login-fixture",
                role="user",
                status="active",
                failed_login_count=0,
                created_at=now,
                updated_at=now,
            )
            .returning(users.c.id)
        ).scalar_one()
        db.session.execute(
            profiles.insert().values(
                user_id=user_id,
                display_name="Cuenta anterior",
                usage_mode="personal",
                grade="Nota previa",
                timezone="America/Bogota",
                privacy_version="2026-10-14",
                privacy_accepted_at=now,
                reference_sex="unspecified",
                movement_goal="center",
                created_at=now,
                updated_at=now,
            )
        )
        db.session.execute(
            measurements.insert().values(
                user_id=user_id,
                weight_kg=70,
                height_cm=175,
                bmi_snapshot=22.86,
                measured_on=date(2026, 10, 14),
                created_at=now,
            )
        )
        db.session.commit()
        print("Previous-schema fixture created in disposable CI database only.")


if __name__ == "__main__":
    seed()
