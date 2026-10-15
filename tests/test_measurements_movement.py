from datetime import date, timedelta
from decimal import Decimal

import pytest

from app.extensions import db
from app.models import Habit, HabitEntry, HealthMeasurement, RoutineCompletion
from app.services.clock import local_day
from app.services.measurements import (
    age_in_months,
    growth_reference,
    growth_snapshot,
    reference_note,
)
from app.services.movement import register_routine, suggested_routine
from app.services.progress import complete_habit, progress_for


def test_growth_reference_is_complete_and_matches_published_example():
    assert len(growth_reference()) == 336
    snapshot = growth_snapshot(19, date(2017, 1, 1), "male", date(2026, 1, 1))
    assert snapshot["age_months"] == 108
    assert snapshot["reference_source"] == "WHO-2007-LMS"
    assert 92 < snapshot["growth_percentile"] < 94
    assert age_in_months(date(2017, 1, 15), date(2026, 1, 14)) == 107
    assert age_in_months(date(2027, 1, 1), date(2026, 1, 1)) is None
    assert (
        growth_snapshot(15.2441, date(2020, 12, 1), "female", date(2026, 1, 1))["growth_percentile"]
        == 50
    )


@pytest.mark.parametrize(
    "birth,sex",
    [
        (None, "male"),
        (date(2015, 1, 1), "unspecified"),
        (date(2025, 1, 1), "male"),
        (date(1990, 1, 1), "female"),
    ],
)
def test_growth_reference_is_not_guessed_when_missing_or_outside_range(birth, sex):
    snapshot = growth_snapshot(20, birth, sex, date(2026, 1, 1))
    assert snapshot["growth_percentile"] is None
    assert snapshot["reference_source"] is None


def test_extreme_value_is_not_extrapolated():
    assert (
        growth_snapshot(90, date(2015, 1, 1), "male", date(2026, 1, 1))["growth_percentile"] is None
    )


def test_child_measurements_are_neutral_and_saved_with_reference(
    client, user_factory, login, student_authorization
):
    user = user_factory()
    student_authorization(user)
    login()
    response = client.post(
        "/perfil/",
        data={
            "display_name": "Ejemplo infantil",
            "birth_date": "2015-01-01",
            "reference_sex": "male",
            "movement_goal": "center",
            "weight_kg": "30",
            "height_cm": "140",
            "usage_mode": "personal",
            "measurement_consent": "y",
        },
        follow_redirects=True,
    )
    assert "Perfil actualizado" in response.text
    row = db.session.scalar(db.select(HealthMeasurement))
    assert row.reference_sex == "male"
    assert row.age_months is not None and row.reference_source == "WHO-2007-LMS"
    assert "Percentil de referencia OMS" in reference_note(row)
    for forbidden in ("Sobrepeso", "Obesidad", "Bajo peso", "bajar de peso", "Dentro del rango"):
        assert forbidden not in response.text
    assert "Preparar mi espacio" in response.text
    assert suggested_routine(user)["slug"] == "fortalece-tu-centro"


@pytest.mark.parametrize(
    "weight,height",
    [("NaN", "170"), ("Infinity", "170"), ("20", "0"), ("500", "50"), ("-1", "100")],
)
def test_invalid_measurements_do_not_crash_or_create_rows(
    client, user_factory, login, weight, height
):
    user_factory()
    login()
    response = client.post(
        "/perfil/",
        data={"display_name": "Ejemplo", "weight_kg": weight, "height_cm": height},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "Revisa los campos" in response.text
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0


def test_smaller_child_values_and_unknown_age_do_not_use_adult_thresholds(
    client, user_factory, login
):
    user_factory()
    login()
    response = client.post(
        "/perfil/",
        data={
            "display_name": "Ejemplo",
            "weight_kg": "14",
            "height_cm": "100",
            "measurement_consent": "y",
        },
        follow_redirects=True,
    )
    assert "Perfil actualizado" in response.text
    assert "Sin interpretación por edad" in response.text
    row = db.session.scalar(db.select(HealthMeasurement))
    assert row.growth_percentile is None
    row.age_months = 150
    assert "No se aplican rangos adultos" in reference_note(row)
    row.age_months = 360
    assert "Una referencia descriptiva" in reference_note(row)


def test_tracking_is_private_year_scoped_and_has_accessible_table(client, user_factory, login):
    owner = user_factory(email="owner@example.com")
    other = user_factory()
    today = local_day(other)
    for user, year, value in (
        (owner, today.year, "33.33"),
        (other, today.year, "22.22"),
        (other, today.year - 1, "21.11"),
    ):
        db.session.add(
            HealthMeasurement(
                user_id=user.id,
                weight_kg=Decimal("70"),
                height_cm=Decimal("175"),
                bmi_snapshot=Decimal(value),
                measured_on=date(year, 1, 1),
            )
        )
    db.session.commit()
    login()
    response = client.get(f"/perfil/seguimiento?year={today.year}&user_id={owner.id}")
    assert response.status_code == 200
    assert (
        "22.22" in response.text and "33.33" not in response.text and "21.11" not in response.text
    )
    assert "<svg" in response.text and "<caption>Detalle" in response.text
    assert 'tabindex="0" role="region" aria-label="Mis mediciones del año"' in response.text
    assert "21.11" in client.get(f"/perfil/seguimiento?year={today.year - 1}").text
    assert client.get("/perfil/seguimiento?year=abc").status_code == 200
    assert client.get("/perfil/seguimiento?year=99999").status_code == 200
    assert "Aún no hay mediciones" in client.get("/perfil/seguimiento?year=2020").text


def test_routine_completion_is_daily_and_does_not_duplicate_xp(client, user_factory, login):
    user = user_factory()
    login()
    first = client.post(
        "/rutinas/fortalece-tu-centro/registrar", data={"origin": "profile"}, follow_redirects=True
    )
    assert "+15 XP" in first.text
    assert "Registrada hoy" not in first.text  # Default goal is a different routine.
    repeat = client.post("/rutinas/fortalece-tu-centro/registrar", follow_redirects=True)
    assert "no duplicamos" in repeat.text
    assert "Registrada hoy" in repeat.text
    second = client.post("/rutinas/despierta-tu-energia/registrar", follow_redirects=True)
    assert "ya había sumado" in second.text
    assert progress_for(user).points == 15
    assert db.session.scalar(db.select(db.func.count(HabitEntry.id))) == 1
    assert db.session.scalar(db.select(db.func.count(RoutineCompletion.id))) == 2
    assert client.post("/rutinas/desconocida/registrar").status_code == 404


def test_routine_and_existing_habit_share_the_same_points(user_factory):
    user = user_factory()
    habit = db.session.scalar(db.select(Habit).where(Habit.code == "gentle-movement"))
    assert complete_habit(user, habit)
    assert register_routine(user, "construye-tu-fuerza") == {"created": True, "points": 0}
    assert register_routine(user, "construye-tu-fuerza") == {"created": False, "points": 0}
    assert progress_for(user).points == 15
    row = db.session.scalar(db.select(RoutineCompletion))
    assert row.completed_on == local_day(user)
    row.completed_on -= timedelta(days=1)
    db.session.commit()
    assert register_routine(user, "construye-tu-fuerza")["created"]
    habit.active = False
    db.session.commit()
    assert register_routine(user, "fortalece-tu-centro") is None
