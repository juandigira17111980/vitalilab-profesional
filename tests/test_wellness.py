from datetime import UTC, datetime, timedelta
from unittest.mock import patch

import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import AuditEvent, DailyCheckIn, Habit, HabitEntry, UserGoal
from app.services.clock import local_day
from app.services.wellness import goals_for, history_for, remove_goal, save_checkin, save_goal


@pytest.mark.parametrize("path", ["/metas/", "/bitacora/", "/progreso/"])
def test_new_private_pages_require_login(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Cache-Control"] == "no-store"


def test_library_is_public_searchable_and_escapes_queries(client):
    assert "15 rutinas disponibles" in client.get("/rutinas/").text
    assert "1 rutina disponible" in client.get("/rutinas/?categoria=Descanso").text
    assert "2 rutinas disponibles" in client.get("/rutinas/?q=pantalla").text
    assert "No encontramos" in client.get("/rutinas/?q=noexiste").text
    assert (
        "<script>alert(1)</script>" not in client.get("/rutinas/?q=<script>alert(1)</script>").text
    )
    assert client.get("/rutinas/pausa-consciente/").status_code == 200
    assert client.get("/rutinas/desconocida/").status_code == 404


def test_goal_create_update_and_delete_preserve_entries(client, user_factory, login):
    user = user_factory()
    login()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    response = client.post(
        "/metas/", data={"habit_id": habit.id, "target_days": 3}, follow_redirects=True
    )
    assert "Meta guardada" in response.text
    goal = db.session.scalar(db.select(UserGoal).where(UserGoal.user_id == user.id))
    client.post("/metas/", data={"habit_id": habit.id, "target_days": 5})
    assert goal.target_days == 5
    assert db.session.scalar(db.select(db.func.count(UserGoal.id))) == 1
    db.session.add(HabitEntry(user_id=user.id, habit_id=habit.id, completed_on=local_day(user)))
    db.session.commit()
    response = client.post(f"/metas/{goal.id}/eliminar", follow_redirects=True)
    assert "Tus hábitos registrados se conservan" in response.text
    assert db.session.scalar(db.select(db.func.count(UserGoal.id))) == 0
    assert db.session.scalar(db.select(db.func.count(HabitEntry.id))) == 1


def test_goal_isolation_and_form_validation(client, user_factory, login):
    owner = user_factory(email="owner@example.com")
    other = user_factory()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    save_goal(owner, habit, 3)
    goal = db.session.scalar(db.select(UserGoal))
    login()
    assert client.post(f"/metas/{goal.id}/eliminar").status_code == 404
    assert goals_for(other) == []
    for payload in ({"habit_id": 999, "target_days": 3}, {"habit_id": habit.id, "target_days": 8}):
        assert "Revisa los campos" in client.post("/metas/", data=payload).text
    with pytest.raises(PermissionError):
        remove_goal(goal, other)
    habit.active = False
    db.session.commit()
    assert (
        "Revisa los campos"
        in client.post("/metas/", data={"habit_id": habit.id, "target_days": 2}).text
    )
    with pytest.raises(ValueError):
        save_goal(other, habit, 2)


def test_goal_progress_is_bounded_by_seven_days_and_user(user_factory):
    user = user_factory()
    other = user_factory(email="other@example.com")
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    save_goal(user, habit, 2)
    today = local_day(user)
    for offset in (0, 1, 6, 7):
        db.session.add(
            HabitEntry(
                user_id=user.id, habit_id=habit.id, completed_on=today - timedelta(days=offset)
            )
        )
    db.session.add(HabitEntry(user_id=other.id, habit_id=habit.id, completed_on=today))
    db.session.commit()
    goal = goals_for(user)[0]
    assert goal["days_done"] == 3
    assert goal["percent"] == 100


def test_checkin_updates_one_row_and_does_not_log_personal_values(client, user_factory, login):
    user = user_factory()
    login()
    assert (
        "Registro guardado"
        in client.post("/bitacora/", data={"energy": 2, "focus": 4}, follow_redirects=True).text
    )
    client.post("/bitacora/", data={"energy": 5, "focus": 3})
    assert db.session.scalar(db.select(db.func.count(DailyCheckIn.id))) == 1
    stored = db.session.scalar(db.select(DailyCheckIn))
    assert stored.user_id == user.id and stored.energy == 5 and stored.focus == 3
    events = db.session.scalars(db.select(AuditEvent).where(AuditEvent.action == "checkin.saved"))
    assert all(
        "energy" not in event.metadata_redacted and "focus" not in event.metadata_redacted
        for event in events
    )
    assert (
        "Selecciona un valor válido"
        in client.post("/bitacora/", data={"energy": 6, "focus": 3}).text
    )
    assert client.get("/bitacora/").headers["Cache-Control"] == "no-store"
    with pytest.raises(ValueError):
        save_checkin(user, 0, 3)


def test_history_does_not_expose_other_users_and_is_limited(user_factory):
    user = user_factory()
    other = user_factory(email="other@example.com")
    save_checkin(other, 5, 5)
    history = history_for(user)
    assert len(history["days"]) == 28
    assert history["checkins"] == [] and history["entries"] == 0
    assert history["active_days"] == 0


def test_database_enforces_new_uniqueness_and_ranges(user_factory):
    user = user_factory()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    save_goal(user, habit, 3)
    db.session.add(UserGoal(user_id=user.id, habit_id=habit.id, target_days=4))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
    db.session.add(DailyCheckIn(user_id=user.id, checked_on=local_day(user), energy=6, focus=3))
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()


def test_write_conflict_is_recoverable(user_factory):
    user = user_factory()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    with patch(
        "app.services.wellness.db.session.commit", side_effect=IntegrityError("race", {}, None)
    ):
        assert save_goal(user, habit, 3) is False
        assert save_checkin(user, 2, 3) is False


def test_date_boundary_uses_profile_zone_and_safe_fallback(user_factory):
    user = user_factory()
    instant = datetime(2026, 10, 14, 2, 0, tzinfo=UTC)
    with patch("app.services.clock.datetime") as clock:
        clock.now.return_value = instant
        assert local_day(user).isoformat() == "2026-10-13"
        user.profile.timezone = "Asia/Tokyo"
        assert local_day(user).isoformat() == "2026-10-14"
        user.profile.timezone = "not-a-zone"
        assert local_day(user).isoformat() == "2026-10-13"


def test_new_writes_require_csrf(client, app, user_factory, login):
    user_factory()
    login()
    app.config["WTF_CSRF_ENABLED"] = True
    for path in ("/metas/", "/bitacora/", "/metas/1/eliminar"):
        assert client.post(path).status_code == 400


def test_dashboard_completion_returns_to_panel_without_open_redirect(client, user_factory, login):
    user_factory()
    login()
    habit = db.session.scalar(db.select(Habit).order_by(Habit.id))
    assert (
        client.post(f"/habitos/{habit.id}/completar", data={"return_to": "panel"}).location
        == "/panel"
    )
    assert (
        client.post(
            f"/habitos/{habit.id}/completar", data={"return_to": "https://example.com"}
        ).location
        == "/habitos/"
    )
