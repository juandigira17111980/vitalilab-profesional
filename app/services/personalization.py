"""Explicit, one-time setup. BMI is descriptive and never chooses exercise loads."""

from decimal import Decimal

from app.extensions import db
from app.models import HealthMeasurement, SchoolEnrollmentRequest
from app.services.clock import local_day
from app.services.measurements import growth_snapshot
from app.services.progress import calculate_bmi
from app.services.school import membership_for


def latest_measurement(user):
    return db.session.scalar(
        db.select(HealthMeasurement)
        .where(HealthMeasurement.user_id == user.id)
        .order_by(HealthMeasurement.measured_on.desc(), HealthMeasurement.id.desc())
        .limit(1)
    )


def student_setup_required(user):
    if user.profile.usage_mode != "institutional":
        return False
    member = membership_for(user)
    requested = db.session.scalar(
        db.select(SchoolEnrollmentRequest).where(SchoolEnrollmentRequest.user_id == user.id)
    )
    is_student = (
        member and member.requested_role == "student" and member.status in {"pending", "approved"}
    ) or (requested and requested.requested_role == "student" and requested.status == "pending")
    return bool(is_student and not user.profile.personalization_completed_at)


def is_school_student(user):
    member = membership_for(user)
    requested = db.session.scalar(
        db.select(SchoolEnrollmentRequest).where(SchoolEnrollmentRequest.user_id == user.id)
    )
    return bool(
        user.profile.usage_mode == "institutional"
        and (
            (member and member.requested_role == "student")
            or (
                requested
                and requested.requested_role == "student"
                and requested.status == "pending"
            )
        )
    )


def measurement_permission(user, birth_date=None):
    """Fail closed for school students and known minors; no consent is fabricated."""
    member = membership_for(user)
    school_student = is_school_student(user)
    birth = birth_date or user.profile.birth_date
    today = local_day(user)
    minor = bool(
        birth
        and (today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))) < 18
    )
    if not school_student and not minor:
        return True
    return bool(
        member
        and member.status == "approved"
        and member.authorization_confirmed
        and member.reviewed_at
        and member.reviewed_by_user_id
        and member.school.active
        and (member.requested_role != "student" or (member.group and member.group.active))
    )


def save_measurement(user, weight, height):
    """Caller validates input and permission. Preserve previous snapshots, dedupe same day."""
    profile = user.profile
    weight, height = Decimal(weight), Decimal(height)
    bmi = calculate_bmi(float(weight), float(height))
    day = local_day(user)
    snapshot = growth_snapshot(bmi, profile.birth_date, profile.reference_sex, day)
    latest = latest_measurement(user)
    if latest and (
        latest.weight_kg == weight
        and latest.height_cm == height
        and latest.measured_on == day
        and latest.age_months == snapshot["age_months"]
        and latest.reference_sex == snapshot["reference_sex"]
    ):
        return latest
    row = HealthMeasurement(
        user_id=user.id,
        weight_kg=weight,
        height_cm=height,
        bmi_snapshot=Decimal(str(bmi)),
        measured_on=day,
        **snapshot,
    )
    db.session.add(row)
    return row
