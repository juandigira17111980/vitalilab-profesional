import pytest

from app import create_app
from app.commands import seed_habits
from app.extensions import db
from app.models import User, UserProfile


@pytest.fixture()
def app():
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "SQLALCHEMY_ENGINE_OPTIONS": {"pool_pre_ping": True},
            "WTF_CSRF_ENABLED": False,
            "RATELIMIT_ENABLED": False,
            "SERVER_NAME": "localhost",
        }
    )
    with application.app_context():
        db.create_all()
        seed_habits()
        yield application
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user_factory(app):
    def factory(email="user@example.com", password="SecurePass123", role="user"):
        user = User(email=email, role=role)
        user.set_password(password)
        user.profile = UserProfile(display_name="Usuario de prueba")
        db.session.add(user)
        db.session.commit()
        return user

    return factory


@pytest.fixture()
def login(client):
    def perform(email="user@example.com", password="SecurePass123"):
        return client.post(
            "/acceso/ingresar",
            data={"email": email, "password": password},
            follow_redirects=True,
        )

    return perform
