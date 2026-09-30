import re
from unittest.mock import patch

from app import create_app
from app.extensions import db
from app.models import User


def test_register_hashes_password_and_opens_dashboard(client, app):
    response = client.post(
        "/acceso/registro",
        data={
            "display_name": "Ana",
            "email": "ANA@Example.com ",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "privacy_accepted": "y",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Hola, Ana" in response.text
    user = db.session.scalar(db.select(User).where(User.email == "ana@example.com"))
    assert user is not None
    assert user.password_hash != "StrongPass123"
    assert user.check_password("StrongPass123")


def test_registration_rejects_duplicate_email(client, user_factory):
    user_factory()
    response = client.post(
        "/acceso/registro",
        data={
            "display_name": "Otro",
            "email": "USER@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
            "privacy_accepted": "y",
        },
    )
    assert response.status_code == 409
    assert "No fue posible crear la cuenta" in response.text


def test_login_and_logout_use_safe_session_flow(client, user_factory, login):
    user_factory()
    response = login()
    assert response.status_code == 200
    assert "Bienvenido de nuevo" in response.text
    response = client.post("/acceso/salir", follow_redirects=True)
    assert response.status_code == 200
    assert "Sesión cerrada correctamente" in response.text


def test_failed_logins_lock_account_temporarily(client, user_factory):
    user = user_factory()
    for _ in range(5):
        client.post(
            "/acceso/ingresar",
            data={"email": user.email, "password": "WrongPass123"},
        )
    db.session.refresh(user)
    assert user.is_locked
    response = client.post(
        "/acceso/ingresar",
        data={"email": user.email, "password": "SecurePass123"},
        follow_redirects=True,
    )
    assert "Correo o contraseña incorrectos" in response.text


def test_password_reset_token_expires_after_password_change(app, user_factory):
    user = user_factory()
    token = user.generate_reset_token()
    assert User.verify_reset_token(token).id == user.id
    user.set_password("AnotherPass456")
    db.session.commit()
    assert User.verify_reset_token(token) is None


def test_forgot_and_reset_password_flow_does_not_disclose_accounts(client, user_factory):
    user = user_factory()
    with patch("app.auth.routes.send_password_reset", return_value=True) as sender:
        response = client.post(
            "/acceso/recuperar",
            data={"email": f" {user.email.upper()} "},
            follow_redirects=True,
        )
    assert "Si el correo existe" in response.text
    reset_url = sender.call_args.args[1]
    token = reset_url.rsplit("/", 1)[-1]
    response = client.post(
        f"/acceso/restablecer/{token}",
        data={"password": "NewSecurePass456", "confirm_password": "NewSecurePass456"},
        follow_redirects=True,
    )
    assert "Contraseña actualizada" in response.text
    assert user.check_password("NewSecurePass456")

    response = client.post(
        "/acceso/recuperar",
        data={"email": "missing@example.com"},
        follow_redirects=True,
    )
    assert "Si el correo existe" in response.text


def test_invalid_reset_token_and_unsafe_next_are_rejected(client, user_factory):
    user = user_factory()
    response = client.get("/acceso/restablecer/invalido", follow_redirects=True)
    assert "enlace es inválido" in response.text

    response = client.post(
        "/acceso/ingresar?next=https://example.org/robo",
        data={"email": user.email, "password": "SecurePass123"},
    )
    assert response.status_code == 302
    assert response.location.endswith("/panel")


def test_password_policy_and_unknown_login_are_generic(client):
    response = client.post(
        "/acceso/registro",
        data={
            "display_name": "Ana",
            "email": "ana@example.com",
            "password": "weak",
            "confirm_password": "weak",
            "privacy_accepted": "y",
        },
    )
    assert "al menos 10 caracteres" in response.text

    response = client.post(
        "/acceso/ingresar",
        data={"email": "missing@example.com", "password": "SecurePass123"},
    )
    assert "Correo o contraseña incorrectos" in response.text


def test_registration_round_trip_with_csrf_enabled():
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "csrf-round-trip-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": True,
            "RATELIMIT_ENABLED": False,
        }
    )
    with application.app_context():
        db.create_all()
        client = application.test_client()
        page = client.get("/acceso/registro")
        match = re.search(r'name="csrf_token"[^>]+value="([^"]+)"', page.text)
        assert match is not None
        response = client.post(
            "/acceso/registro",
            data={
                "csrf_token": match.group(1),
                "display_name": "Prueba CSRF",
                "email": "csrf@example.com",
                "password": "StrongPass123",
                "confirm_password": "StrongPass123",
                "privacy_accepted": "y",
            },
        )
        assert response.status_code == 302
        assert response.location.endswith("/panel")
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
