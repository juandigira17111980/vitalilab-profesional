"""Tenant-scoped authorization and aggregates; no student-level teacher data."""

from collections import defaultdict
from datetime import date

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    HabitEntry,
    HealthMeasurement,
    School,
    SchoolEnrollmentRequest,
    SchoolGroup,
    SchoolMembership,
    TeacherGroupAssignment,
    User,
    UserProfile,
    utcnow,
)
from app.services.audit import record_event
from app.services.clock import local_day

MIN_COHORT = 10
SCHOOL_CATALOG = (
    ("jose-miguel-de-la-calle", "I.E. José Miguel de la Calle"),
    ("leticia-arango", "Leticia Arango"),
)


def seed_schools():
    created = 0
    for code, name in SCHOOL_CATALOG:
        if db.session.scalar(db.select(School.id).where(School.code == code)) is None:
            db.session.add(School(code=code, name=name))
            created += 1
    db.session.commit()
    return created


def membership_for(user):
    return db.session.scalar(db.select(SchoolMembership).where(SchoolMembership.user_id == user.id))


def teacher_membership(user):
    if not user.is_active or user.profile.usage_mode != "institutional":
        return None
    return db.session.scalar(
        db.select(SchoolMembership)
        .join(School, School.id == SchoolMembership.school_id)
        .where(
            SchoolMembership.user_id == user.id,
            SchoolMembership.requested_role == "teacher",
            SchoolMembership.status == "approved",
            SchoolMembership.authorization_confirmed.is_(True),
            SchoolMembership.reviewed_at.is_not(None),
            SchoolMembership.reviewed_by_user_id.is_not(None),
            School.active.is_(True),
        )
    )


def school_choices():
    schools = list(
        db.session.scalars(db.select(School).where(School.active.is_(True)).order_by(School.name))
    )
    groups = list(
        db.session.scalars(
            db.select(SchoolGroup)
            .join(School)
            .where(SchoolGroup.active.is_(True), School.active.is_(True))
            .order_by(SchoolGroup.academic_year.desc(), SchoolGroup.name)
        )
    )
    return schools, groups


def configure_join_form(form):
    schools, groups = school_choices()
    form.school_id.choices = [(school.id, school.name) for school in schools]
    form.group_id.choices = [(0, "Sin grupo asignado aún")] + [
        (group.id, f"{group.school.name} · {group.name} · {group.academic_year}")
        for group in groups
    ]
    return schools, groups


def request_membership(user, school_id, group_id, requested_role):
    db.session.scalar(db.select(User.id).where(User.id == user.id).with_for_update())
    if db.session.scalar(
        db.select(SchoolEnrollmentRequest.id).where(
            SchoolEnrollmentRequest.user_id == user.id,
            SchoolEnrollmentRequest.status == "pending",
        )
    ):
        raise ValueError("Ya tienes una solicitud en trámite. Retírala antes de enviar otra.")
    school = db.session.get(School, school_id)
    group = db.session.get(SchoolGroup, group_id) if group_id else None
    if not school or not school.active or requested_role not in {"student", "teacher"}:
        raise ValueError("Selecciona un colegio y un rol válidos.")
    if group_id and (not group or not group.active or group.school_id != school_id):
        raise ValueError("El grupo debe pertenecer al colegio seleccionado.")
    existing = db.session.scalar(
        db.select(SchoolMembership).where(SchoolMembership.user_id == user.id).with_for_update()
    )
    if existing and existing.status in {"pending", "approved"}:
        raise ValueError(
            "Ya tienes una vinculación en trámite o aprobada. Retírala antes de solicitar otra."
        )
    member = existing or SchoolMembership(user_id=user.id)
    if existing:
        db.session.execute(
            delete(TeacherGroupAssignment).where(
                TeacherGroupAssignment.membership_id == existing.id
            )
        )
    member.school_id, member.group_id = school_id, group_id or None
    member.requested_role, member.status = requested_role, "pending"
    member.allow_aggregate, member.aggregate_since = False, None
    member.authorization_confirmed, member.reviewed_at, member.reviewed_by_user_id = (
        False,
        None,
        None,
    )
    user.profile.usage_mode = "institutional"
    db.session.add(member)
    try:
        db.session.flush()
        record_event(
            "school.membership_requested",
            "school_membership",
            member.id,
            user.id,
            {"school_id": school_id, "role": requested_role},
        )
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ValueError(
            "La solicitud cambió en otra sesión. Recarga antes de intentar de nuevo."
        ) from error
    return member


def withdraw_membership(user):
    member = db.session.scalar(
        db.select(SchoolMembership).where(SchoolMembership.user_id == user.id).with_for_update()
    )
    if member:
        member.status, member.allow_aggregate, member.aggregate_since = "revoked", False, None
        member.authorization_confirmed = False
        db.session.execute(
            delete(TeacherGroupAssignment).where(TeacherGroupAssignment.membership_id == member.id)
        )
        record_event("school.membership_withdrawn", "school_membership", member.id, user.id)
        db.session.commit()


def review_membership(actor, membership_id, decision, group_id=0, verified=False):
    if not actor.is_admin:
        raise PermissionError("Administrative review required")
    member = db.session.scalar(
        db.select(SchoolMembership).where(SchoolMembership.id == membership_id).with_for_update()
    )
    if not member or decision not in {"approved", "rejected", "revoked"}:
        raise ValueError("Solicitud o decisión no válida.")
    if decision == "approved":
        school = db.session.get(School, member.school_id)
        group = db.session.get(SchoolGroup, group_id) if group_id else None
        if member.status != "pending" or not verified or not school.active:
            raise ValueError(
                "Solo se aprueban solicitudes pendientes con verificación "
                "de identidad y autorizaciones."
            )
        if member.requested_role == "student" and not group:
            raise ValueError("Asigna un grupo válido al estudiante.")
        if group and (not group.active or group.school_id != member.school_id):
            raise ValueError("El grupo no pertenece a este colegio o no está activo.")
        member.group_id = group.id if group else None
        member.authorization_confirmed = True
    else:
        member.authorization_confirmed, member.allow_aggregate, member.aggregate_since = (
            False,
            False,
            None,
        )
        db.session.execute(
            delete(TeacherGroupAssignment).where(TeacherGroupAssignment.membership_id == member.id)
        )
    member.status, member.reviewed_at, member.reviewed_by_user_id = decision, utcnow(), actor.id
    record_event(
        "school.membership_reviewed", "school_membership", member.id, actor.id, {"status": decision}
    )
    db.session.commit()
    return member


def assign_teacher(actor, membership_id, group_id):
    if not actor.is_admin:
        raise PermissionError("Administrative assignment required")
    member, group = (
        db.session.get(SchoolMembership, membership_id),
        db.session.get(SchoolGroup, group_id),
    )
    if (
        not member
        or not group
        or member.status != "approved"
        or member.requested_role != "teacher"
        or not member.authorization_confirmed
        or not group.active
        or member.school_id != group.school_id
        or not group.school.active
    ):
        raise ValueError("Asigna solo docentes aprobados a grupos activos de su propio colegio.")
    if db.session.scalar(
        db.select(TeacherGroupAssignment.id).where(
            TeacherGroupAssignment.membership_id == member.id,
            TeacherGroupAssignment.group_id == group.id,
        )
    ):
        return False
    db.session.add(
        TeacherGroupAssignment(
            membership_id=member.id, school_id=member.school_id, group_id=group.id
        )
    )
    record_event(
        "school.teacher_assigned", "school_group", group.id, actor.id, {"membership_id": member.id}
    )
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


def set_aggregate_consent(user, enabled):
    member = membership_for(user)
    if (
        not member
        or member.requested_role != "student"
        or member.status != "approved"
        or not member.authorization_confirmed
    ):
        raise ValueError(
            "La preferencia está disponible después de aprobar la vinculación estudiantil."
        )
    if enabled and not member.allow_aggregate:
        member.aggregate_since = utcnow()
    if not enabled:
        member.aggregate_since = None
    member.allow_aggregate = enabled
    record_event(
        "school.aggregate_preference", "school_membership", member.id, user.id, {"enabled": enabled}
    )
    db.session.commit()


def teacher_groups(user):
    member = teacher_membership(user)
    if not member:
        return []
    return list(
        db.session.scalars(
            db.select(SchoolGroup)
            .join(TeacherGroupAssignment, TeacherGroupAssignment.group_id == SchoolGroup.id)
            .where(
                TeacherGroupAssignment.membership_id == member.id,
                TeacherGroupAssignment.school_id == member.school_id,
                SchoolGroup.school_id == member.school_id,
                SchoolGroup.active.is_(True),
            )
            .order_by(SchoolGroup.academic_year.desc(), SchoolGroup.name)
        )
    )


def report_for_group(user, group_id):
    group = next((item for item in teacher_groups(user) if item.id == group_id), None)
    if group is None:
        raise PermissionError("Group is outside this teacher's assignment")
    eligible = list(
        db.session.scalars(
            db.select(SchoolMembership)
            .join(User, User.id == SchoolMembership.user_id)
            .join(UserProfile, UserProfile.user_id == User.id)
            .where(
                SchoolMembership.school_id == group.school_id,
                SchoolMembership.group_id == group.id,
                SchoolMembership.status == "approved",
                SchoolMembership.requested_role == "student",
                SchoolMembership.authorization_confirmed.is_(True),
                SchoolMembership.reviewed_at.is_not(None),
                SchoolMembership.reviewed_by_user_id.is_not(None),
                SchoolMembership.allow_aggregate.is_(True),
                SchoolMembership.aggregate_since.is_not(None),
                User.status == "active",
                UserProfile.usage_mode == "institutional",
            )
        )
    )
    months = [
        {"month": month, "label": label, "activity": None, "growth": None, "percentile": None}
        for month, label in enumerate(
            ("Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"), 1
        )
    ]
    output = {
        "group": group,
        "sufficient": len(eligible) >= MIN_COHORT,
        "months": months,
        "minimum": MIN_COHORT,
    }
    if not output["sufficient"]:
        return output
    start, end = date(group.academic_year, 1, 1), date(group.academic_year + 1, 1, 1)
    eligible_by_id = {member.user_id: member for member in eligible}
    since = {
        member.user_id: max(member.aggregate_since, member.reviewed_at or member.aggregate_since)
        for member in eligible
    }
    # Only rows created after both verified approval and opt-in; no historical data grab.
    latest = {}
    rows = db.session.scalars(
        db.select(HealthMeasurement)
        .where(
            HealthMeasurement.user_id.in_(eligible_by_id),
            HealthMeasurement.measured_on >= start,
            HealthMeasurement.measured_on < end,
            HealthMeasurement.reference_source == "WHO-2007-LMS",
        )
        .order_by(HealthMeasurement.measured_on, HealthMeasurement.id)
    )
    for row in rows:
        if (
            row.created_at >= since[row.user_id]
            and row.measured_on >= since[row.user_id].date()
            and row.measured_on <= local_day(user)
            and row.growth_percentile is not None
        ):
            latest[(row.user_id, row.measured_on.month)] = float(row.growth_percentile)
    growth = defaultdict(list)
    for (_, month), percentile in latest.items():
        growth[month].append(percentile)
    active = defaultdict(set)
    entries = db.session.scalars(
        db.select(HabitEntry).where(
            HabitEntry.user_id.in_(eligible_by_id),
            HabitEntry.completed_on >= start,
            HabitEntry.completed_on < end,
        )
    )
    for entry in entries:
        if (
            entry.created_at >= since[entry.user_id]
            and entry.completed_on >= since[entry.user_id].date()
            and entry.completed_on <= local_day(user)
        ):
            active[entry.completed_on.month].add(entry.user_id)
    for month in months:
        number = month["month"]
        if len(active[number]) >= MIN_COHORT:
            month["activity"] = len(active[number]) // 5 * 5
        if len(growth[number]) >= MIN_COHORT:
            month["growth"] = len(growth[number]) // 5 * 5
            month["percentile"] = round(sum(growth[number]) / len(growth[number]) / 5) * 5
    return output
