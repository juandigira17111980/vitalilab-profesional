from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ProfileForm
from app.models import HealthMeasurement
from app.services.audit import record_event
from app.services.clock import local_day
from app.services.measurements import growth_snapshot, measurement_history, reference_note
from app.services.movement import routine_done_today, suggested_routine
from app.services.progress import calculate_bmi
from app.services.school import membership_for

bp = Blueprint("profile", __name__, url_prefix="/perfil")


@bp.route("/", methods=["GET", "POST"])
@login_required
def edit():
    profile = current_user.profile
    latest = db.session.scalar(
        db.select(HealthMeasurement)
        .where(HealthMeasurement.user_id == current_user.id)
        .order_by(HealthMeasurement.measured_on.desc(), HealthMeasurement.id.desc())
        .limit(1)
    )
    form = ProfileForm(obj=profile)
    if form.validate_on_submit():
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
            weight = Decimal(form.weight_kg.data)
            height = Decimal(form.height_cm.data)
            bmi = calculate_bmi(float(weight), float(height))
            snapshot = growth_snapshot(
                bmi, profile.birth_date, profile.reference_sex, local_day(current_user)
            )
            if (
                latest is None
                or latest.weight_kg != weight
                or latest.height_cm != height
                or latest.measured_on != local_day(current_user)
                or latest.age_months != snapshot["age_months"]
                or latest.reference_sex != snapshot["reference_sex"]
            ):
                latest = HealthMeasurement(
                    user_id=current_user.id,
                    weight_kg=weight,
                    height_cm=height,
                    bmi_snapshot=Decimal(str(bmi)),
                    measured_on=local_day(current_user),
                    **snapshot,
                )
                db.session.add(latest)
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
