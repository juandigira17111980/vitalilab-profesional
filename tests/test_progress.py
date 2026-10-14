from datetime import timedelta

from app.extensions import db
from app.models import Habit, HabitEntry
from app.services.clock import local_day
from app.services.progress import calculate_bmi, complete_habit, level_for, progress_for


def test_bmi_and_levels_follow_documented_rules():
    assert calculate_bmi(70, 175) == 22.86
    assert level_for(0) == "Semilla vital"
    assert level_for(100) == "Explorador saludable"
    assert level_for(250) == "Guardián del equilibrio"
    assert level_for(500) == "Leyenda vital"


def test_habit_completion_is_idempotent(user_factory):
    user = user_factory()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    assert complete_habit(user, habit) is True
    assert complete_habit(user, habit) is False
    summary = progress_for(user)
    assert summary.points == habit.points
    assert summary.completed_today == 1


def test_streak_counts_consecutive_days(user_factory):
    user = user_factory()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    today = local_day(user)
    for offset in (0, 1, 2):
        db.session.add(
            HabitEntry(
                user_id=user.id, habit_id=habit.id, completed_on=today - timedelta(days=offset)
            )
        )
    db.session.commit()
    assert progress_for(user).streak == 3


def test_complete_habit_route_does_not_duplicate_points(client, user_factory, login):
    user_factory()
    login()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    first = client.post(f"/habitos/{habit.id}/completar", follow_redirects=True)
    second = client.post(f"/habitos/{habit.id}/completar", follow_redirects=True)
    assert "Sumaste" in first.text
    assert "no se duplicaron" in second.text
