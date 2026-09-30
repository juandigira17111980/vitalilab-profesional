from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Habit, HabitEntry, User
from app.services.audit import record_event

LEVELS = (
    (500, "Leyenda vital"),
    (250, "Guardián del equilibrio"),
    (100, "Explorador saludable"),
    (0, "Semilla vital"),
)


@dataclass(frozen=True)
class ProgressSummary:
    points: int
    streak: int
    level: str
    completed_today: int
    total_habits: int
    week: list[dict[str, int | str]]


def level_for(points: int) -> str:
    return next(name for threshold, name in LEVELS if points >= threshold)


def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    return round(weight_kg / ((height_cm / 100) ** 2), 2)


def bmi_label(value: float) -> str:
    if value < 18.5:
        return "Por debajo del rango orientativo"
    if value < 25:
        return "Dentro del rango orientativo"
    if value < 30:
        return "Por encima del rango orientativo"
    return "Rango elevado: consulta a un profesional"


def complete_habit(user: User, habit: Habit, completed_on: date | None = None) -> bool:
    day = completed_on or date.today()
    existing = db.session.scalar(
        db.select(HabitEntry).where(
            HabitEntry.user_id == user.id,
            HabitEntry.habit_id == habit.id,
            HabitEntry.completed_on == day,
        )
    )
    if existing:
        return False
    db.session.add(HabitEntry(user_id=user.id, habit_id=habit.id, completed_on=day))
    record_event("habit.completed", "habit", habit.id, user.id, {"date": day.isoformat()})
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


def progress_for(user: User, today: date | None = None) -> ProgressSummary:
    day = today or date.today()
    points = db.session.scalar(
        db.select(func.coalesce(func.sum(Habit.points), 0))
        .select_from(HabitEntry)
        .join(Habit, Habit.id == HabitEntry.habit_id)
        .where(HabitEntry.user_id == user.id)
    )
    completed_today = db.session.scalar(
        db.select(func.count(HabitEntry.id)).where(
            HabitEntry.user_id == user.id, HabitEntry.completed_on == day
        )
    )
    total_habits = db.session.scalar(db.select(func.count(Habit.id)).where(Habit.active.is_(True)))
    distinct_days = list(
        db.session.scalars(
            db.select(HabitEntry.completed_on)
            .where(HabitEntry.user_id == user.id)
            .distinct()
            .order_by(HabitEntry.completed_on.desc())
        )
    )
    streak = _current_streak(distinct_days, day)
    week = _week_progress(user.id, day)
    points_int = int(points or 0)
    return ProgressSummary(
        points=points_int,
        streak=streak,
        level=level_for(points_int),
        completed_today=int(completed_today or 0),
        total_habits=int(total_habits or 0),
        week=week,
    )


def _current_streak(days: list[date], today: date) -> int:
    if not days:
        return 0
    day_set = set(days)
    cursor = today if today in day_set else today - timedelta(days=1)
    if cursor not in day_set:
        return 0
    streak = 0
    while cursor in day_set:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def _week_progress(user_id: int, today: date) -> list[dict[str, int | str]]:
    start = today - timedelta(days=6)
    rows = db.session.execute(
        db.select(HabitEntry.completed_on, func.count(HabitEntry.id))
        .where(HabitEntry.user_id == user_id, HabitEntry.completed_on >= start)
        .group_by(HabitEntry.completed_on)
    ).all()
    counts = {row[0]: int(row[1]) for row in rows}
    labels = ("Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom")
    return [
        {
            "date": (current := start + timedelta(days=offset)).isoformat(),
            "label": labels[current.weekday()],
            "count": counts.get(current, 0),
        }
        for offset in range(7)
    ]
