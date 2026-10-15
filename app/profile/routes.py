from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db, limiter
from app.forms import ProfileForm
from app.models import utcnow
from app.services.audit import record_event
from app.services.clock import local_day
from app.services.measurements import measurement_history, reference_note
from app.services.movement import routine_done_today, suggested_routine
from app.services.personalization import (
    is_school_student,
    latest_measurement,
    measurement_permission,
    save_measurement,
    student_setup_required,
)
from app.services.school import membership_for
from app.wellness.forms import MeasurementSetupForm, MovementGoalForm

bp = Blueprint("profile", __name__, url_prefix="/perfil")


@bp.route("/", methods=["GET", "POST"])
@login_required
def edit():
    profile = current_user.profile
    latest = latest_measurement(current_user)
    form = ProfileForm(obj=profile)
    valid = form.validate_on_submit()
    if (
        valid
        and form.weight_kg.data
        and is_school_student(current_user)
        and not form.birth_date.data
    ):
        form.birth_date.errors.append(
            "Completa tu fecha de nacimiento para contextualizar la medición."
        )
        valid = False
    if (
        valid
        and form.weight_kg.data
        and not measurement_permission(current_user, form.birth_date.data)
    ):
        form.weight_kg.errors.append(
            "Necesitas una vinculación verificada y autorizada antes de guardar mediciones."
        )
        valid = False
    if (
        valid
        and form.weight_kg.data
        and not (profile.measurement_consent_at or form.measurement_consent.data)
    ):
        form.measurement_consent.errors.append("Confirma que quieres guardar estas mediciones.")
        valid = False
    if valid:
        profile.display_name = form.display_name.data.strip()
        profile.birth_date = form.birth_date.data
        profile.reference_sex = form.reference_sex.data
        profile.movement_goal = form.movement_goal.data
        profile.usage_mode = form.usage_mode.data
        if profile.usage_mode == "institutional":
            # Retained for compatibility; these legacy notes never confer membership.
            if "institution_name" in request.form:
                profile.institution_name = form.institution_name.data or None
            if "grade" in request.form:
                profile.grade = form.grade.data or None
        if form.weight_kg.data and form.height_cm.data:
            profile.measurement_consent_at = profile.measurement_consent_at or utcnow()
            latest = save_measurement(current_user, form.weight_kg.data, form.height_cm.data)
        record_event(
            "profile.updated",
            "user_profile",
            current_user.id,
            current_user.id,
            metadata={"usage_mode": profile.usage_mode},
        )
        db.session.commit()
        flash("Perfil actualizado.", "success")
        return redirect(url_for("profile.edit"))
    elif form.is_submitted():
        flash("Revisa los campos marcados.", "error")
    elif latest:
        form.weight_kg.data = latest.weight_kg
        form.height_cm.data = latest.height_cm
    routine = suggested_routine(current_user)
    return render_template(
        "profile/edit.html",
        form=form,
        latest=latest,
        bmi_status=reference_note(latest) if latest else None,
        member=membership_for(current_user),
        suggested=routine,
        routine_completed=routine_done_today(current_user, routine["slug"]),
        can_measure=measurement_permission(current_user),
        needs_setup=student_setup_required(current_user),
    )


@bp.get("/seguimiento")
@login_required
def tracking():
    try:
        year = int(request.args.get("year", local_day(current_user).year))
    except (TypeError, ValueError):
        year = local_day(current_user).year
    if not 2020 <= year <= 2100:
        year = local_day(current_user).year
    return render_template("profile/tracking.html", history=measurement_history(current_user, year))


@bp.route("/inicio/medicion", methods=["GET", "POST"])
@login_required
@limiter.limit("20 per hour", methods=["POST"])
def setup_measurement():
    latest = latest_measurement(current_user)
    form = MeasurementSetupForm(obj=current_user.profile)
    allowed = measurement_permission(current_user)
    valid = form.validate_on_submit()
    if valid and is_school_student(current_user) and not form.birth_date.data:
        form.birth_date.errors.append(
            "Completa tu fecha de nacimiento para contextualizar la medición."
        )
        valid = False
    if valid:
        if not measurement_permission(current_user, form.birth_date.data):
            form.weight_kg.errors.append(
                "Tu institución debe verificar el vínculo y las autorizaciones "
                "antes de guardar mediciones."
            )
        else:
            profile = current_user.profile
            profile.birth_date = form.birth_date.data
            profile.reference_sex = form.reference_sex.data
            profile.measurement_consent_at = profile.measurement_consent_at or utcnow()
            save_measurement(current_user, form.weight_kg.data, form.height_cm.data)
            record_event(
                "personalization.measurement_saved",
                "user_profile",
                profile.user_id,
                current_user.id,
            )
            db.session.commit()
            return redirect(url_for("profile.setup_goal"))
    elif not form.is_submitted() and latest:
        form.weight_kg.data, form.height_cm.data = latest.weight_kg, latest.height_cm
    return render_template(
        "profile/setup_measurement.html", form=form, allowed=allowed, latest=latest
    )


@bp.route("/inicio/objetivo", methods=["GET", "POST"])
@login_required
@limiter.limit("20 per hour", methods=["POST"])
def setup_goal():
    latest = latest_measurement(current_user)
    if not latest or not current_user.profile.measurement_consent_at:
        return redirect(url_for("profile.setup_measurement"))
    if not measurement_permission(current_user):
        return redirect(url_for("profile.setup_measurement"))
    form = MovementGoalForm(obj=current_user.profile)
    if form.validate_on_submit():
        current_user.profile.movement_goal = form.movement_goal.data
        current_user.profile.movement_preference = form.movement_preference.data
        current_user.profile.personalization_completed_at = utcnow()
        record_event("personalization.completed", "user_profile", current_user.id, current_user.id)
        db.session.commit()
        flash("Tu espacio está listo. Elige una rutina o crea la tuya.", "success")
        return redirect(url_for("wellness.library", para="mi"))
    return render_template(
        "profile/setup_goal.html", form=form, latest=latest, bmi_status=reference_note(latest)
    )
