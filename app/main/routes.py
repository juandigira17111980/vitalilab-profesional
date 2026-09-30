from datetime import date

from flask import Blueprint, current_app, jsonify, render_template
from flask_login import current_user, login_required
from sqlalchemy import text

from app.extensions import db
from app.models import Announcement, Habit, HabitEntry
from app.services.progress import progress_for

bp = Blueprint("main", __name__)

CONTENT = {
    "imc": {
        "eyebrow": "Conoce tus indicadores",
        "title": "El IMC es una referencia, no un diagnóstico",
        "lead": (
            "Relaciona peso y altura para ofrecer una orientación general. "
            "La edad, el desarrollo, la composición corporal y el contexto "
            "individual también importan."
        ),
        "sections": (
            (
                "Cómo se calcula",
                "Se divide el peso en kilogramos por la altura en metros elevada al cuadrado.",
            ),
            (
                "Cómo interpretarlo",
                "Úsalo como una señal para conversar con un profesional, "
                "nunca como una etiqueta personal.",
            ),
            (
                "Cuándo pedir orientación",
                "Si te preocupa un cambio de peso, energía o alimentación, "
                "consulta a personal de salud calificado.",
            ),
        ),
    },
    "bienestar": {
        "eyebrow": "Bienestar cotidiano",
        "title": "Pequeñas decisiones, constancia real",
        "lead": (
            "Moverte, descansar, hidratarte y pausar también son herramientas de aprendizaje. "
            "La meta no es la perfección: es construir una rutina sostenible."
        ),
        "sections": (
            ("Movimiento", "Interrumpe periodos largos sentado con pausas breves y frecuentes."),
            ("Descanso", "Una rutina estable de sueño favorece atención, memoria y recuperación."),
            ("Autocuidado", "Reconoce señales de cansancio y busca apoyo cuando lo necesites."),
        ),
    },
    "fundamentos": {
        "eyebrow": "Cómo funciona VitaliLab",
        "title": "Tecnología al servicio de hábitos comprensibles",
        "lead": (
            "VitaliLab convierte metas cotidianas en acciones visibles, protege la información "
            "y permite aprender del progreso sin reemplazar asesoría profesional."
        ),
        "sections": (
            ("Privacidad", "Recopilamos únicamente los datos necesarios para el funcionamiento."),
            (
                "Evidencia",
                "Cada hábito se registra una vez por día y el progreso se calcula en el servidor.",
            ),
            (
                "Aprendizaje",
                "El proyecto documenta arquitectura, datos, seguridad, pruebas y despliegue.",
            ),
        ),
    },
}


@bp.get("/")
def home():
    announcements = list(
        db.session.scalars(
            db.select(Announcement)
            .where(Announcement.status == "published")
            .order_by(Announcement.published_at.desc())
            .limit(3)
        )
    )
    return render_template("main/home.html", announcements=announcements)


@bp.get("/contenido/<slug>")
def content(slug: str):
    article = CONTENT.get(slug)
    if article is None:
        return render_template("errors/404.html"), 404
    return render_template("main/content.html", article=article)


@bp.get("/privacidad")
def privacy():
    return render_template("main/privacy.html")


@bp.get("/panel")
@login_required
def dashboard():
    summary = progress_for(current_user)
    habits = list(
        db.session.scalars(
            db.select(Habit).where(Habit.active.is_(True)).order_by(Habit.sort_order)
        )
    )
    completed_ids = set(
        db.session.scalars(
            db.select(HabitEntry.habit_id).where(
                HabitEntry.user_id == current_user.id,
                HabitEntry.completed_on == date.today(),
            )
        )
    )
    announcement = db.session.scalar(
        db.select(Announcement)
        .where(Announcement.status == "published")
        .order_by(Announcement.published_at.desc())
        .limit(1)
    )
    return render_template(
        "main/dashboard.html",
        summary=summary,
        habits=habits,
        completed_ids=completed_ids,
        announcement=announcement,
    )


@bp.get("/health")
def health():
    return jsonify(status="ok", service="vitalilab", version=current_app.config["APP_VERSION"])


@bp.get("/ready")
def ready():
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        current_app.logger.exception("Readiness database check failed")
        return jsonify(status="unavailable"), 503
    return jsonify(status="ready")


@bp.app_context_processor
def global_template_values():
    return {"current_year": date.today().year}
