from unittest.mock import patch

from app.commands import seed_habits
from app.extensions import db
from app.models import Habit
from app.services.email import send_password_reset


def test_seed_habits_is_idempotent(app):
    assert seed_habits() == 0
    assert db.session.scalar(db.select(db.func.count(Habit.id))) == 8


def test_email_service_without_configuration_returns_false(app):
    assert send_password_reset("user@example.com", "https://example.test/reset") is False


def test_email_service_uses_tls_and_auth_when_configured(app):
    app.config.update(
        MAIL_HOST="smtp.example.test",
        MAIL_USERNAME="smtp-user",
        MAIL_PASSWORD="smtp-secret",
        MAIL_FROM="noreply@example.test",
    )
    with patch("app.services.email.smtplib.SMTP") as smtp:
        assert send_password_reset("user@example.com", "https://example.test/reset") is True
    server = smtp.return_value.__enter__.return_value
    server.starttls.assert_called_once()
    server.login.assert_called_once_with("smtp-user", "smtp-secret")
    server.send_message.assert_called_once()


def test_readiness_reports_database_failure(client):
    with patch("app.main.routes.db.session.execute", side_effect=RuntimeError("db offline")):
        response = client.get("/ready")
    assert response.status_code == 503
    assert response.json == {"status": "unavailable"}


def test_create_admin_command_enforces_identity_security(app):
    runner = app.test_cli_runner()
    invalid_email = runner.invoke(
        args=[
            "create-admin",
            "--email",
            "admin@invalid.local",
            "--name",
            "Admin",
            "--password",
            "StrongPass123",
        ]
    )
    assert invalid_email.exit_code != 0
    assert "formato válido" in invalid_email.output

    weak_password = runner.invoke(
        args=[
            "create-admin",
            "--email",
            "admin@example.com",
            "--name",
            "Admin",
            "--password",
            "weak",
        ]
    )
    assert weak_password.exit_code != 0
    assert "10 caracteres" in weak_password.output

    created = runner.invoke(
        args=[
            "create-admin",
            "--email",
            "ADMIN@example.com",
            "--name",
            "Administrador",
            "--password",
            "StrongPass123",
        ]
    )
    assert created.exit_code == 0
    assert "Administrador creado" in created.output
