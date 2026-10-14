from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models import DailyCheckIn, Habit, HabitEntry, User, UserGoal
from app.services.audit import record_event
from app.services.clock import local_day


def save_goal(user: User, habit: Habit, target_days: int) -> bool:
    if not habit.active or not 1 <= target_days <= 7:
        raise ValueError("Invalid goal")
    goal = db.session.scalar(
        db.select(UserGoal).where(UserGoal.user_id == user.id, UserGoal.habit_id == habit.id)
    )
    if goal is None:
        goal = UserGoal(user_id=user.id, habit_id=habit.id, target_days=target_days)
        db.session.add(goal)
    else:
        goal.target_days = target_days
    record_event("goal.saved", "habit", habit.id, user.id, {"target_days": target_days})
    return _commit()


def remove_goal(goal: UserGoal, user: User) -> None:
    if goal.user_id != user.id:
        raise PermissionError("Goal belongs to another user")
    record_event("goal.removed", "goal", goal.id, user.id)
    db.session.delete(goal)
    db.session.commit()


def goals_for(user: User) -> list[dict]:
    day = local_day(user)
    counts = dict(
        db.session.execute(
            db.select(HabitEntry.habit_id, func.count(HabitEntry.id))
            .where(
                HabitEntry.user_id == user.id,
                HabitEntry.completed_on.between(day - timedelta(days=6), day),
            )
            .group_by(HabitEntry.habit_id)
        ).all()
    )
    goals = db.session.scalars(
        db.select(UserGoal)
        .options(joinedload(UserGoal.habit))
        .where(UserGoal.user_id == user.id)
        .order_by(UserGoal.id)
    )
    return [
        {
            "goal": goal,
            "days_done": counts.get(goal.habit_id, 0),
            "percent": min(100, round(counts.get(goal.habit_id, 0) / goal.target_days * 100)),
        }
        for goal in goals
    ]


def save_checkin(user: User, energy: int, focus: int) -> bool:
    if not 1 <= energy <= 5 or not 1 <= focus <= 5:
        raise ValueError("Invalid check-in")
    day = local_day(user)
    checkin = db.session.scalar(
        db.select(DailyCheckIn).where(
            DailyCheckIn.user_id == user.id, DailyCheckIn.checked_on == day
        )
    )
    if checkin is None:
        db.session.add(DailyCheckIn(user_id=user.id, checked_on=day, energy=energy, focus=focus))
    else:
        checkin.energy, checkin.focus = energy, focus
    # Personal self-reported values do not belong in the operational audit log.
    record_event("checkin.saved", "checkin", None, user.id)
    return _commit()


def history_for(user: User) -> dict:
    day = local_day(user)
    start = day - timedelta(days=27)
    counts = dict(
        db.session.execute(
            db.select(HabitEntry.completed_on, func.count(HabitEntry.id))
            .where(HabitEntry.user_id == user.id, HabitEntry.completed_on.between(start, day))
            .group_by(HabitEntry.completed_on)
        ).all()
    )
    checkins = list(
        db.session.scalars(
            db.select(DailyCheckIn)
            .where(DailyCheckIn.user_id == user.id, DailyCheckIn.checked_on.between(start, day))
            .order_by(DailyCheckIn.checked_on.desc())
            .limit(28)
        )
    )
    return {
        "days": [
            {"date": (current := start + timedelta(days=offset)), "count": counts.get(current, 0)}
            for offset in range(28)
        ],
        "entries": sum(counts.values()),
        "active_days": len(counts),
        "checkins": checkins,
    }


def _commit() -> bool:
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True
