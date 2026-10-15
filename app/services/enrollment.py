"""Manual school names remain untrusted until an administrator maps and verifies them."""

from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    School,
    SchoolEnrollmentRequest,
    SchoolGroup,
    SchoolMembership,
    TeacherGroupAssignment,
    User,
    utcnow,
)
from app.services.audit import record_event
from app.services.school import membership_for


def enrollment_for(user, *, lock=False):
    query = db.select(SchoolEnrollmentRequest).where(SchoolEnrollmentRequest.user_id == user.id)
    return db.session.scalar(query.with_for_update() if lock else query)


def request_manual_enrollment(user, school_name, group_name, role):
    db.session.scalar(db.select(User.id).where(User.id == user.id).with_for_update())
    member = membership_for(user)
    existing = enrollment_for(user, lock=True)
    if (member and member.status in {"pending", "approved"}) or (
        existing and existing.status == "pending"
    ):
        raise ValueError(
            "Ya tienes una vinculación en trámite o aprobada. Retírala antes de solicitar otra."
        )
    item = existing or SchoolEnrollmentRequest(user_id=user.id)
    item.school_name, item.group_name, item.requested_role = school_name, group_name, role
    item.status, item.reviewed_at, item.reviewed_by_user_id = "pending", None, None
    user.profile.usage_mode = "institutional"
    user.profile.institution_name, user.profile.grade = school_name, group_name
    db.session.add(item)
    try:
        db.session.flush()
        record_event("school.manual_request_created", "school_enrollment_request", item.id, user.id)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ValueError(
            "La solicitud cambió en otra ventana. Recarga antes de continuar."
        ) from error
    return item


def cancel_manual_enrollment(user):
    item = enrollment_for(user, lock=True)
    if item and item.status == "pending":
        item.status = "cancelled"
        record_event(
            "school.manual_request_cancelled", "school_enrollment_request", item.id, user.id
        )
        db.session.commit()


def review_manual_enrollment(actor, request_id, school_id, group_id, decision, verified):
    if not actor.is_admin:
        raise PermissionError("Administrative review required")
    item = db.session.scalar(
        db.select(SchoolEnrollmentRequest)
        .where(SchoolEnrollmentRequest.id == request_id)
        .with_for_update()
    )
    if not item or item.status != "pending" or decision not in {"approved", "rejected"}:
        raise ValueError("Esta solicitud ya se revisó o no está disponible.")
    if decision == "approved":
        school = db.session.get(School, school_id)
        group = db.session.get(SchoolGroup, group_id) if group_id else None
        if not verified or not school or not school.active:
            raise ValueError(
                "Verifica identidad, pertenencia y autorizaciones y elige un colegio activo."
            )
        if (item.requested_role == "student" and not group) or (
            group and (not group.active or group.school_id != school.id)
        ):
            raise ValueError("Selecciona un grupo activo del mismo colegio para el estudiante.")
        member = db.session.scalar(
            db.select(SchoolMembership)
            .where(SchoolMembership.user_id == item.user_id)
            .with_for_update()
        )
        if member and member.status in {"approved", "pending"}:
            raise ValueError("La persona ya tiene una vinculación activa. Revísala primero.")
        member = member or SchoolMembership(user_id=item.user_id)
        if member.id:
            db.session.execute(
                delete(TeacherGroupAssignment).where(
                    TeacherGroupAssignment.membership_id == member.id
                )
            )
        member.school_id, member.group_id = school.id, group.id if group else None
        member.requested_role, member.status = item.requested_role, "approved"
        member.authorization_confirmed = True
        member.reviewed_at, member.reviewed_by_user_id = utcnow(), actor.id
        member.allow_aggregate, member.aggregate_since = False, None
        db.session.add(member)
        item.status = "resolved"
    else:
        item.status = "rejected"
    item.reviewed_at, item.reviewed_by_user_id = utcnow(), actor.id
    record_event(
        "school.manual_request_reviewed",
        "school_enrollment_request",
        item.id,
        actor.id,
        {"decision": decision},
    )
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise ValueError(
            "La vinculación cambió en otra ventana. Recarga antes de revisar."
        ) from error
    return item
