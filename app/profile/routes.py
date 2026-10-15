from decimal import Decimal

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ProfileForm
from app.models import HealthMeasurement
from app.services.audit import record_event
from app.services.clock import local_day
from app.services.progress import bmi_label, calculate_bmi

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
        profile.usage_mode = form.usage_mode.data
        if profile.usage_mode == "institutional":
            profile.institution_name = form.institution_name.data or None
            profile.grade = form.grade.data or None
        if form.weight_kg.data and form.height_cm.data:
            weight = Decimal(form.weight_kg.data)
            height = Decimal(form.height_cm.data)
            if latest is None or latest.weight_kg != weight or latest.height_cm != height:
                bmi = calculate_bmi(float(weight), float(height))
                latest = HealthMeasurement(
                    user_id=current_user.id,
                    weight_kg=weight,
                    height_cm=height,
                    bmi_snapshot=Decimal(str(bmi)),
                    measured_on=local_day(current_user),
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
    return render_template(
        "profile/edit.html",
        form=form,
        latest=latest,
        bmi_status=bmi_label(float(latest.bmi_snapshot)) if latest else None,
    )
