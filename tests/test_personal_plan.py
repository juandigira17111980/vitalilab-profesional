from datetime import date

import pytest

from app.extensions import db
from app.models import HabitEntry, HealthMeasurement, SchoolMembership, utcnow
from app.services.personalization import (
    measurement_permission,
    personalization_ready,
    student_setup_required,
)
from app.services.progress import progress_for


@pytest.mark.parametrize("birth", [None, date(2014, 1, 1), date(1990, 1, 1)])
def test_personal_plan_needs_only_goal_and_preference_not_health_data(
    client, user_factory, login, birth
):
    user = user_factory()
    user.profile.birth_date = birth
    db.session.commit()
    login()
    entry = client.get("/rutinas/?para=mi")
    assert entry.location.endswith("/perfil/inicio/objetivo")
    response = client.get(entry.location)
    assert "No necesitas registrar peso ni altura" in response.text
    assert 'name="weight_kg"' not in response.text
    assert 'name="height_cm"' not in response.text
    assert 'name="birth_date"' not in response.text
    assert "institución debe verificar" not in response.text
    assert "data-bmi-preview" in response.text
    response = client.post(
        "/perfil/inicio/objetivo",
        data={"movement_goal": "strength", "movement_preference": "seated"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert "2 rutinas disponibles" in response.text
    assert "Fuerza suave con tus manos" in response.text
    assert personalization_ready(user)
    assert user.profile.birth_date == birth
    assert user.profile.measurement_consent_at is None
    assert user.profile.usage_mode == "personal"
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert db.session.scalar(db.select(db.func.count(SchoolMembership.id))) == 0
    # The plan remains usable without granting the right to store minors' measurements.
    if birth == date(2014, 1, 1):
        assert not measurement_permission(user)
    client.post("/rutinas/construye-tu-fuerza/registrar")
    assert progress_for(user).points == 15
    assert db.session.scalar(db.select(db.func.count(HabitEntry.id))) == 1
    client.post("/acceso/salir")
    result = login()
    assert result.request.path == "/panel"
    assert client.get("/rutinas/?para=mi").status_code == 200


def test_goal_post_does_not_accept_or_store_injected_health_fields(client, user_factory, login):
    user = user_factory()
    login()
    client.post(
        "/perfil/inicio/objetivo",
        data={
            "movement_goal": "energy",
            "movement_preference": "adaptable",
            "weight_kg": "58",
            "height_cm": "174",
            "birth_date": "2009-11-11",
            "measurement_consent": "y",
            "authorization_confirmed": "true",
        },
    )
    assert personalization_ready(user)
    assert user.profile.birth_date is None
    assert user.profile.measurement_consent_at is None
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0


def test_school_cannot_reuse_personal_completion_to_skip_measurement_and_approval(
    client, user_factory, login, student_authorization
):
    user = user_factory()
    user.profile.personalization_completed_at = utcnow()
    user.profile.usage_mode = "institutional"
    member = student_authorization(user)
    db.session.commit()
    assert not personalization_ready(user)
    assert student_setup_required(user)
    login()
    for path in ("/perfil/inicio/objetivo?personal=1", "/rutinas/?para=mi"):
        result = client.get(path)
        assert result.status_code == 302
        assert result.location.endswith("/perfil/inicio/medicion")
    result = client.post(
        "/perfil/inicio/objetivo",
        data={
            "movement_goal": "strength",
            "movement_preference": "seated",
            "usage_mode": "personal",
        },
    )
    assert result.location.endswith("/perfil/inicio/medicion")
    assert user.profile.usage_mode == "institutional"
    assert user.profile.movement_goal == "energy"
    assert member.authorization_confirmed
    assert not member.allow_aggregate


def test_pending_school_stays_scoped_even_after_personal_plan_was_completed(
    client, user_factory, login
):
    user = user_factory()
    login()
    client.post(
        "/perfil/inicio/objetivo",
        data={"movement_goal": "energy", "movement_preference": "adaptable"},
    )
    client.post(
        "/colegios/",
        data={
            "school_name": "Colegio de pruebas",
            "group_name": "Grupo A",
            "requested_role": "student",
        },
    )
    assert student_setup_required(user)
    assert not personalization_ready(user)
    assert client.get("/habitos/").status_code == 200
    assert client.get("/rutinas/?para=mi").location.endswith("/perfil/inicio/medicion")
