import os
from logging.config import dictConfig

from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix

from app.config import Config, TestingConfig, validate_runtime_config
from app.extensions import csrf, db, limiter, login_manager, migrate


def create_app(test_config: dict | None = None) -> Flask:
    _configure_logging()
    app = Flask(__name__)
    app.config.from_object(TestingConfig if test_config is not None else Config)
    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    if not app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"].update({"pool_size": 5, "max_overflow": 2})
    validate_runtime_config(app)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
    _init_extensions(app)
    _register_blueprints(app)
    _register_errors(app)
    _register_commands(app)
    _register_security_headers(app)
    return app


def _configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s %(levelname)s %(name)s %(message)s",
                }
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                }
            },
            "root": {
                "level": os.getenv("LOG_LEVEL", "INFO").upper(),
                "handlers": ["console"],
            },
        }
    )


def _init_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)


def _register_blueprints(app: Flask) -> None:
    from app.admin.routes import bp as admin_bp
    from app.auth.routes import bp as auth_bp
    from app.habits.routes import bp as habits_bp
    from app.main.routes import bp as main_bp
    from app.profile.routes import bp as profile_bp
    from app.school.routes import bp as school_bp
    from app.wellness.routes import bp as wellness_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(habits_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(wellness_bp)
    app.register_blueprint(school_bp)


def _register_errors(app: Flask) -> None:
    from app.errors import register_error_handlers

    register_error_handlers(app)


def _register_commands(app: Flask) -> None:
    from app.commands import register_commands

    register_commands(app)


def _register_security_headers(app: Flask) -> None:
    @app.after_request
    def add_security_headers(response):
        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
        response.headers.setdefault(
            "Permissions-Policy", "camera=(), microphone=(), geolocation=()"
        )
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "base-uri 'self'; object-src 'none'; frame-ancestors 'none'; "
            "form-action 'self'; img-src 'self' data:; "
            "style-src 'self'; script-src 'self'; connect-src 'self'",
        )
        if app.config["SESSION_COOKIE_SECURE"]:
            response.headers.setdefault(
                "Strict-Transport-Security", "max-age=31536000; includeSubDomains"
            )
        if request.path.startswith(
            (
                "/panel",
                "/perfil",
                "/habitos",
                "/admin",
                "/metas",
                "/bitacora",
                "/progreso",
                "/acceso",
                "/colegios",
                "/docentes",
                "/mis-rutinas",
            )
        ):
            response.headers.setdefault("Cache-Control", "no-store")
        if request.path.startswith("/rutinas"):
            # The library now contains owner-specific routines and preferences.
            response.headers.setdefault("Cache-Control", "no-store")
        return response
