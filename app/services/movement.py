"""Record a routine and its existing habit atomically; never duplicate daily XP."""

from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Habit, HabitEntry, RoutineCompletion
from app.services.audit import record_event
from app.services.clock import local_day
from app.wellness.catalog import ROUTINES

GOAL_ROUTINES = {
    "center": "fortalece-tu-centro",
    "energy": "despierta-tu-energia",
    "strength": "construye-tu-fuerza",
}


def suggested_routine(user):
    slug = GOAL_ROUTINES.get(user.profile.movement_goal, GOAL_ROUTINES["energy"])
    return next(item for item in ROUTINES if item["slug"] == slug)


def routine_done_today(user, slug):
    return (
        db.session.scalar(
            db.select(RoutineCompletion.id).where(
                RoutineCompletion.user_id == user.id,
                RoutineCompletion.routine_slug == slug,
                RoutineCompletion.completed_on == local_day(user),
            )
        )
        is not None
    )


def register_routine(user, slug):
    routine = next((item for item in ROUTINES if item["slug"] == slug), None)
    if routine is None:
        return None
    habit = db.session.scalar(
        db.select(Habit).where(Habit.code == routine["habit_code"], Habit.active.is_(True))
    )
    if habit is None:
        return None
    day = local_day(user)
    try:
        with db.session.begin_nested():
            db.session.add(
                RoutineCompletion(
                    user_id=user.id, routine_slug=slug, habit_id=habit.id, completed_on=day
                )
            )
            db.session.flush()
    except IntegrityError:
        db.session.rollback()
        return {"created": False, "points": 0}
    points = 0
    try:
        with db.session.begin_nested():
            db.session.add(HabitEntry(user_id=user.id, habit_id=habit.id, completed_on=day))
            db.session.flush()
        points = habit.points
    except IntegrityError:
        pass  # This habit already earned its points through another routine or quick action.
    record_event(
        "routine.completed", "routine", slug, user.id, {"date": day.isoformat(), "points": points}
    )
    db.session.commit()
    return {"created": True, "points": points}
