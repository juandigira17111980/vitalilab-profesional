"""Explicit, one-time setup. BMI is descriptive and never chooses exercise loads."""

from dataclasses import dataclass
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
    return bool(is_student and not personalization_ready(user))


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


def personalization_ready(user):
    """Personal goals do not require health data; school setup keeps its controls."""
    if not user.profile.personalization_completed_at:
        return False
    if user.profile.usage_mode == "personal":
        return True
    return bool(
        user.profile.measurement_consent_at
        and latest_measurement(user)
        and measurement_permission(user)
    )


@dataclass(frozen=True)
class MeasurementAccess:
    allowed: bool
    code: str = "allowed"
    title: str = ""
    message: str = ""
    action: str = "school"


def measurement_access(user, birth_date=None):
    """Explain the existing permission decision; never grant or fabricate approval."""
    if measurement_permission(user, birth_date):
        return MeasurementAccess(allowed=True)
    member = membership_for(user)
    if not member:
        if user.profile.usage_mode == "personal":
            return MeasurementAccess(
                False,
                "minor-authorization",
                "Antes de guardar, necesitamos una autorización",
                "La fecha de nacimiento indica que eres menor de edad. "
                "El guardado de mediciones para menores en uso personal aún no está "
                "habilitado: marcar la casilla no activa esa autorización. "
                "Si la fecha está equivocada, puedes corregirla. "
                "Si es correcta, puedes seguir usando hábitos y rutinas generales. "
                "No necesitas vincularte a un colegio si tu uso es personal.",
                "birth-date",
            )
        return MeasurementAccess(
            False,
            "school-verification",
            "Tu espacio escolar necesita una verificación",
            "Consulta tu vinculación: la administración debe verificar el colegio, "
            "el grupo y las autorizaciones antes de habilitar el guardado. "
            "Escribir el nombre del colegio no activa esta autorización.",
        )
    if member.status != "approved":
        status = {
            "pending": "Tu solicitud está pendiente de revisión.",
            "rejected": "Tu vinculación no está aprobada.",
            "revoked": "Tu vinculación está retirada.",
        }.get(member.status, "Tu vinculación necesita una revisión.")
        return MeasurementAccess(
            False,
            "membership-review",
            "Tu espacio escolar necesita una verificación",
            status + " La administración debe comprobar la pertenencia y las autorizaciones. "
            "Abre tu vinculación para consultar el estado; no hace falta repetir las medidas.",
        )
    if not member.school.active:
        return MeasurementAccess(
            False,
            "school-inactive",
            "Tu colegio está temporalmente inactivo",
            "La administración debe revisar el estado del colegio antes de habilitar "
            "el guardado de nuevas mediciones. Tu historial se conserva.",
        )
    if not (member.authorization_confirmed and member.reviewed_at and member.reviewed_by_user_id):
        return MeasurementAccess(
            False,
            "authorization-review",
            "Falta confirmar la revisión de tus autorizaciones",
            "La vinculación figura aprobada, pero falta registrar una revisión completa "
            "de las autorizaciones. Contacta con la administración para que revise "
            "el registro; no se soluciona cambiando tu peso ni tu altura.",
        )
    return MeasurementAccess(
        False,
        "group-unavailable",
        "Falta un grupo activo en tu vinculación",
        "La administración debe asignarte un grupo activo de tu colegio "
        "antes de habilitar el guardado de mediciones. Tu historial se conserva.",
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
