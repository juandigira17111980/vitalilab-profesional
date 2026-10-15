"""Private routine CRUD. Identity, quotas and edit version are enforced server-side."""

from sqlalchemy import delete

from app.extensions import db
from app.models import PersonalRoutine, RoutineExercise, User
from app.services.audit import record_event

MAX_ROUTINES = 30


def personal_routines_for(user):
    return list(
        db.session.scalars(
            db.select(PersonalRoutine)
            .where(PersonalRoutine.user_id == user.id, PersonalRoutine.active.is_(True))
            .order_by(PersonalRoutine.updated_at.desc(), PersonalRoutine.id.desc())
            .limit(MAX_ROUTINES)
        )
    )


def owned_routine(user, routine_id, *, lock=False):
    if not isinstance(routine_id, int) or not 0 < routine_id <= 2_147_483_647:
        return None
    statement = db.select(PersonalRoutine).where(
        PersonalRoutine.id == routine_id,
        PersonalRoutine.user_id == user.id,
        PersonalRoutine.active.is_(True),
    )
    if lock:
        statement = statement.with_for_update()
    return db.session.scalar(statement.execution_options(populate_existing=True))


def save_personal_routine(user, data, routine_id=None):
    if routine_id is None:
        # Per-owner lock serializes quota checks on PostgreSQL.
        db.session.scalar(db.select(User.id).where(User.id == user.id).with_for_update())
        count = db.session.scalar(
            db.select(db.func.count(PersonalRoutine.id)).where(
                PersonalRoutine.user_id == user.id, PersonalRoutine.active.is_(True)
            )
        )
        if count >= MAX_ROUTINES:
            raise ValueError("Ya tienes 30 rutinas. Archiva una antes de crear otra.")
        routine = PersonalRoutine(user_id=user.id, revision=1)
        db.session.add(routine)
    else:
        routine = owned_routine(user, routine_id, lock=True)
        if routine is None:
            raise LookupError("Routine not found")
        if int(data["revision"]) != routine.revision:
            raise ValueError("Esta rutina cambió en otra ventana. Recarga antes de guardar.")
        routine.revision += 1
        db.session.execute(delete(RoutineExercise).where(RoutineExercise.routine_id == routine.id))
        db.session.expire(routine, ["exercises"])
    routine.name, routine.goal = data["name"], data["goal"]
    routine.description = data["description"] or ""
    db.session.flush()
    for position, item in enumerate(data["exercises"]):
        db.session.add(
            RoutineExercise(
                routine_id=routine.id,
                position=position,
                **{
                    key: item[key]
                    for key in (
                        "name",
                        "sets",
                        "repetitions",
                        "duration_seconds",
                        "rest_seconds",
                        "visual",
                    )
                },
                instructions=item["instructions"] or "",
            )
        )
    record_event(
        "personal_routine.updated" if routine_id else "personal_routine.created",
        "personal_routine",
        routine.id,
        user.id,
        {"exercise_count": len(data["exercises"])},
    )
    db.session.commit()
    return routine


def archive_personal_routine(user, routine_id):
    routine = owned_routine(user, routine_id, lock=True)
    if routine is None:
        return False
    routine.active = False
    routine.revision += 1
    record_event("personal_routine.archived", "personal_routine", routine.id, user.id)
    db.session.commit()
    return True
