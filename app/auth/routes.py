import smtplib
from urllib.parse import urljoin, urlsplit

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, limiter
from app.forms import ForgotPasswordForm, LoginForm, RegisterForm, ResetPasswordForm
from app.models import User, UserProfile
from app.services.audit import record_event
from app.services.email import send_password_reset

bp = Blueprint("auth", __name__, url_prefix="/acceso")
DUMMY_HASH = generate_password_hash("not-a-real-account-password", method="scrypt")


def _normalize_email(value: str) -> str:
    return value.strip().lower()


def _safe_next(target: str | None) -> bool:
    if not target:
        return False
    host = urlsplit(request.host_url)
    destination = urlsplit(urljoin(request.host_url, target))
    return destination.scheme in {"http", "https"} and host.netloc == destination.netloc


@bp.route("/registro", methods=["GET", "POST"])
@limiter.limit("8 per hour")
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = RegisterForm()
    if form.validate_on_submit():
        email = _normalize_email(form.email.data)
        exists = db.session.scalar(db.select(User.id).where(User.email == email))
        if exists:
            flash("No fue posible crear la cuenta con esos datos.", "error")
            return render_template("auth/register.html", form=form), 409
        user = User(email=email)
        user.set_password(form.password.data)
        user.profile = UserProfile(
            display_name=form.display_name.data.strip(), usage_mode=form.usage_mode.data
        )
        db.session.add(user)
        db.session.flush()
        record_event("account.registered", "user", user.id, user.id)
        db.session.commit()
        login_user(user)
        flash("Tu cuenta está lista. Empecemos con un hábito pequeño.", "success")
        return redirect(
            url_for(
                "school.account" if user.profile.usage_mode == "institutional" else "main.dashboard"
            )
        )
    return render_template("auth/register.html", form=form)


@bp.route("/ingresar", methods=["GET", "POST"])
@limiter.limit("5 per minute; 20 per hour")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    form = LoginForm()
    if form.validate_on_submit():
        email = _normalize_email(form.email.data)
        user = db.session.scalar(db.select(User).where(User.email == email))
        password_matches = (
            user.check_password(form.password.data)
            if user is not None
            else check_password_hash(DUMMY_HASH, form.password.data)
        )
        if user and user.is_active and not user.is_locked and password_matches:
            user.register_successful_login()
            record_event("session.login", "user", user.id, user.id)
            db.session.commit()
            login_user(user, remember=form.remember.data)
            next_url = request.args.get("next")
            flash("Bienvenido de nuevo.", "success")
            return redirect(next_url if _safe_next(next_url) else url_for("main.dashboard"))
        if user and not user.is_locked:
            user.register_failed_login()
            db.session.commit()
        flash("Correo o contraseña incorrectos. Intenta de nuevo más tarde.", "error")
    return render_template("auth/login.html", form=form)


@bp.post("/salir")
def logout():
    if current_user.is_authenticated:
        user_id = current_user.id
        record_event("session.logout", "user", user_id, user_id)
        db.session.commit()
        logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("main.home"))


@bp.route("/recuperar", methods=["GET", "POST"])
@limiter.limit("5 per hour")
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = _normalize_email(form.email.data)
        user = db.session.scalar(db.select(User).where(User.email == email))
        if user and user.is_active:
            reset_url = url_for(
                "auth.reset_password", token=user.generate_reset_token(), _external=True
            )
            try:
                send_password_reset(user.email, reset_url)
            except (OSError, smtplib.SMTPException):
                current_app.logger.exception("Unable to send password reset email")
        flash(
            "Si el correo existe y el servicio está configurado, recibirás instrucciones.",
            "info",
        )
        return redirect(url_for("auth.login"))
    return render_template("auth/forgot_password.html", form=form)


@bp.route("/restablecer/<token>", methods=["GET", "POST"])
@limiter.limit("10 per hour")
def reset_password(token: str):
    user = User.verify_reset_token(token)
    if user is None or not user.is_active:
        flash("El enlace es inválido o ya venció.", "error")
        return redirect(url_for("auth.forgot_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        user.failed_login_count = 0
        user.locked_until = None
        record_event("account.password_reset", "user", user.id, user.id)
        db.session.commit()
        flash("Contraseña actualizada. Ya puedes ingresar.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
