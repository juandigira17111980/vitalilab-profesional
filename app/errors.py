import uuid

from flask import current_app, render_template, request
from flask_wtf.csrf import CSRFError


def register_error_handlers(app) -> None:
    @app.errorhandler(CSRFError)
    def handle_csrf(error):
        return render_template("errors/400.html", message=error.description), 400

    @app.errorhandler(400)
    def bad_request(_error):
        return render_template("errors/400.html", message="La solicitud no es válida."), 400

    @app.errorhandler(403)
    def forbidden(_error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(429)
    def too_many_requests(_error):
        return render_template("errors/429.html"), 429

    @app.errorhandler(500)
    def internal_error(error):
        incident_id = uuid.uuid4().hex[:12]
        current_app.logger.error(
            "Unhandled error incident=%s path=%s",
            incident_id,
            request.path,
            exc_info=(type(error), error, error.__traceback__),
        )
        return render_template("errors/500.html", incident_id=incident_id), 500
