from pathlib import Path

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from flask_migrate import upgrade
from sqlalchemy import MetaData, Table
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.extensions import db
from app.models import AuditEvent, User, UserProfile, utcnow


def test_new_profile_defaults_to_personal(client, user_factory, login):
    user = user_factory()
    login()
    assert user.profile.usage_mode == "personal"
    response = client.get("/perfil/")
    assert response.status_code == 200
    assert "Uso personal" in response.text
    assert "Uso institucional" in response.text
    assert "data-institution-fields" in response.text
    assert "personal o institucional" in client.get("/panel").text


def test_institutional_profile_is_saved_and_can_clear_optional_fields(client, user_factory, login):
    user = user_factory()
    login()
    response = client.post(
        "/perfil/",
        data={
            "display_name": "Estudiante de ejemplo",
            "usage_mode": "institutional",
            "institution_name": "  Instituto de práctica  ",
            "grade": "  10° A  ",
        },
    )
    assert response.status_code == 302
    assert user.profile.usage_mode == "institutional"
    assert user.profile.institution_name == "Instituto de práctica"
    assert user.profile.grade == "10° A"
    assert user.role == "user"
    assert "Tu perfil institucional" in client.get("/panel").text
    event = db.session.scalar(db.select(AuditEvent).where(AuditEvent.action == "profile.updated"))
    assert event.metadata_redacted == {"usage_mode": "institutional"}
    client.post(
        "/perfil/",
        data={
            "display_name": "Estudiante de ejemplo",
            "usage_mode": "institutional",
            "institution_name": " ",
            "grade": " ",
        },
    )
    assert user.profile.institution_name is None
    assert user.profile.grade is None


def test_personal_switch_keeps_previous_context_without_accepting_spoofed_fields(
    client, user_factory, login
):
    user = user_factory()
    other = user_factory(email="other@example.com")
    user.profile.usage_mode = "institutional"
    user.profile.institution_name = "Instituto de práctica"
    user.profile.grade = "Grupo A"
    db.session.commit()
    login()
    response = client.post(
        "/perfil/",
        data={
            "display_name": "Usuario de prueba",
            "usage_mode": "personal",
            "institution_name": "No guardar",
            "grade": "No guardar",
            "user_id": other.id,
            "role": "admin",
        },
        follow_redirects=True,
    )
    assert "Perfil actualizado" in response.text
    assert user.profile.usage_mode == "personal"
    assert user.profile.institution_name == "Instituto de práctica"
    assert user.profile.grade == "Grupo A"
    assert user.role == "user"
    assert other.profile.usage_mode == "personal"
    assert other.profile.institution_name is None
    assert "Tu espacio personal" in client.get("/panel").text


@pytest.mark.parametrize("mode", ["admin", "", "institution", "<script>"])
def test_invalid_usage_mode_does_not_update_profile(client, user_factory, login, mode):
    user = user_factory()
    login()
    response = client.post("/perfil/", data={"display_name": "No cambiar", "usage_mode": mode})
    assert "Revisa los campos marcados" in response.text
    assert user.profile.usage_mode == "personal"
    assert user.profile.display_name == "Usuario de prueba"


@pytest.mark.parametrize("field,limit", [("institution_name", 160), ("grade", 80)])
def test_institutional_field_length_is_validated(client, user_factory, login, field, limit):
    user = user_factory()
    login()
    response = client.post(
        "/perfil/",
        data={"display_name": "Usuario", "usage_mode": "institutional", field: "x" * (limit + 1)},
    )
    assert "Revisa los campos marcados" in response.text
    assert user.profile.usage_mode == "personal"


def test_usage_preference_requires_login_and_csrf(client, app, user_factory, login):
    assert client.post("/perfil/", data={"usage_mode": "institutional"}).status_code == 302
    user = user_factory()
    login()
    app.config["WTF_CSRF_ENABLED"] = True
    assert (
        client.post(
            "/perfil/", data={"display_name": "Usuario", "usage_mode": "institutional"}
        ).status_code
        == 400
    )
    assert user.profile.usage_mode == "personal"


def test_usage_mode_database_constraint(app, user_factory):
    user = user_factory()
    user.profile.usage_mode = "admin"
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
    assert user.profile.usage_mode == "personal"


def test_profile_migration_preserves_legacy_groups_and_has_no_schema_drift(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "APP_ENV": "development",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{(tmp_path / 'migration.db').as_posix()}",
            "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
            "RATELIMIT_ENABLED": False,
        }
    )
    migrations = str(Path(__file__).resolve().parents[1] / "migrations")
    with application.app_context():
        upgrade(directory=migrations, revision="54e1c8bb7901")
        legacy = Table("user_profiles", MetaData(), autoload_with=db.engine)
        for index, grade in enumerate(("10° A", None, " ")):
            user = User(email=f"migration-{index}@example.com")
            user.set_password("DisposableOnly2026!")
            db.session.add(user)
            db.session.flush()
            db.session.execute(
                legacy.insert().values(
                    user_id=user.id,
                    display_name=f"Ejemplo {index}",
                    grade=grade,
                    timezone="America/Bogota",
                    privacy_version="2026-09",
                    privacy_accepted_at=utcnow(),
                    created_at=utcnow(),
                    updated_at=utcnow(),
                )
            )
        db.session.commit()
        upgrade(directory=migrations)
        profiles = db.session.scalars(db.select(UserProfile).order_by(UserProfile.user_id)).all()
        assert [profile.usage_mode for profile in profiles] == [
            "institutional",
            "personal",
            "personal",
        ]
        assert [profile.grade for profile in profiles] == ["10° A", None, " "]
        assert all(profile.institution_name is None for profile in profiles)
        with db.engine.connect() as connection:
            assert compare_metadata(MigrationContext.configure(connection), db.metadata) == []
        db.session.remove()
        db.engine.dispose()
