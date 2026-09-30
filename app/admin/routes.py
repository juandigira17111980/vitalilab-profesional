from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import AnnouncementForm, EmptyForm
from app.models import Announcement, AuditEvent, User, utcnow
from app.services.audit import record_event

bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


@bp.get("/")
@admin_required
def dashboard():
    announcements = list(
        db.session.scalars(db.select(Announcement).order_by(Announcement.created_at.desc()))
    )
    recent_events = list(
        db.session.scalars(db.select(AuditEvent).order_by(AuditEvent.created_at.desc()).limit(10))
    )
    user_count = db.session.scalar(db.select(db.func.count(User.id)))
    return render_template(
        "admin/dashboard.html",
        announcements=announcements,
        recent_events=recent_events,
        user_count=user_count,
        form=AnnouncementForm(),
        action_form=EmptyForm(),
    )


@bp.post("/anuncios")
@admin_required
def create_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            author_user_id=current_user.id,
            title=form.title.data.strip(),
            body=form.body.data.strip(),
        )
        db.session.add(announcement)
        db.session.flush()
        record_event("announcement.created", "announcement", announcement.id, current_user.id)
        db.session.commit()
        flash("Borrador guardado.", "success")
    else:
        flash("Revisa el título y el contenido del anuncio.", "error")
    return redirect(url_for("admin.dashboard"))


@bp.post("/anuncios/<int:announcement_id>/publicar")
@admin_required
def publish_announcement(announcement_id: int):
    form = EmptyForm()
    if not form.validate_on_submit():
        abort(400)
    announcement = db.get_or_404(Announcement, announcement_id)
    announcement.status = "published"
    announcement.published_at = utcnow()
    record_event("announcement.published", "announcement", announcement.id, current_user.id)
    db.session.commit()
    flash("Anuncio publicado.", "success")
    return redirect(url_for("admin.dashboard"))


@bp.post("/anuncios/<int:announcement_id>/archivar")
@admin_required
def archive_announcement(announcement_id: int):
    form = EmptyForm()
    if not form.validate_on_submit():
        abort(400)
    announcement = db.get_or_404(Announcement, announcement_id)
    announcement.status = "archived"
    record_event("announcement.archived", "announcement", announcement.id, current_user.id)
    db.session.commit()
    flash("Anuncio archivado.", "info")
    return redirect(url_for("admin.dashboard"))
