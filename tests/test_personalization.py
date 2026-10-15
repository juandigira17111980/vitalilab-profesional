from datetime import date

import pytest

from app.extensions import db
from app.models import HealthMeasurement, School, SchoolGroup, SchoolMembership, utcnow
from app.services.personalization import measurement_permission, student_setup_required


def measurement_data(**changes):
    return {
        "weight_kg": "70",
        "height_cm": "175",
        "birth_date": "1990-01-01",
        "reference_sex": "unspecified",
        "measurement_consent": "y",
        **changes,
    }


def approve_student(user, admin):
    school = School(code="setup-school", name="Colegio de pruebas")
    db.session.add(school)
    db.session.flush()
    group = SchoolGroup(school_id=school.id, name="Grupo A", academic_year=2026)
    db.session.add(group)
    db.session.flush()
    user.profile.usage_mode = "institutional"
    member = SchoolMembership(
        user_id=user.id,
        school_id=school.id,
        group_id=group.id,
        requested_role="student",
        status="approved",
        authorization_confirmed=True,
        reviewed_at=utcnow(),
        reviewed_by_user_id=admin.id,
    )
    db.session.add(member)
    db.session.commit()
    return member


@pytest.mark.parametrize("path", ["/perfil/inicio/medicion", "/perfil/inicio/objetivo"])
def test_setup_needs_login_and_never_caches(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Cache-Control"] == "no-store"


def test_setup_sequence_result_goal_filters_and_no_repeat_on_login(client, user_factory, login):
    user = user_factory()
    login()
    assert client.get("/perfil/inicio/objetivo").location.endswith("/perfil/inicio/medicion")
    assert (
        client.post("/perfil/inicio/objetivo", data={"movement_goal": "strength"}).status_code
        == 302
    )
    assert user.profile.personalization_completed_at is None
    response = client.post(
        "/perfil/inicio/medicion", data=measurement_data(), follow_redirects=True
    )
    assert "22.86" in response.text and "Ahora, dale un propósito" in response.text
    assert user.profile.measurement_consent_at is not None
    assert user.profile.personalization_completed_at is None
    # Same day, same input does not append a second snapshot.
    client.post("/perfil/inicio/medicion", data=measurement_data())
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 1
    response = client.post(
        "/perfil/inicio/objetivo",
        data={"movement_goal": "strength", "movement_preference": "seated"},
        follow_redirects=True,
    )
    assert "2 rutinas disponibles" in response.text
    assert (
        "Fuerza suave con tus manos" in response.text
        and "Explora el apoyo en pared" not in response.text
    )
    assert user.profile.personalization_completed_at is not None
    client.post("/acceso/salir")
    response = client.post(
        "/acceso/ingresar", data={"email": user.email, "password": "SecurePass123"}
    )
    assert response.location.endswith("/panel")
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 1
    assert "/perfil/inicio/objetivo" in client.get("/rutinas/?para=mi").text


@pytest.mark.parametrize(
    "values",
    [
        {"measurement_consent": ""},
        {"weight_kg": ""},
        {"height_cm": ""},
        {"weight_kg": "NaN"},
        {"height_cm": "Infinity"},
        {"height_cm": "0"},
        {"weight_kg": "500", "height_cm": "50"},
        {"birth_date": "2100-01-01"},
    ],
)
def test_setup_rejects_invalid_missing_or_unconsented_data(client, user_factory, login, values):
    user = user_factory()
    login()
    response = client.post("/perfil/inicio/medicion", data=measurement_data(**values))
    assert response.status_code == 200
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert user.profile.measurement_consent_at is None


def test_student_is_prompted_once_but_habits_are_not_blocked(client, user_factory):
    user = user_factory()
    admin = user_factory(email="reviewer@example.com", role="admin")
    member = approve_student(user, admin)
    user.profile.birth_date = date(2014, 1, 1)
    db.session.commit()
    assert student_setup_required(user)
    response = client.post(
        "/acceso/ingresar", data={"email": user.email, "password": "SecurePass123"}
    )
    assert response.location.endswith("/perfil/inicio/medicion")
    assert client.get("/habitos/").status_code == 200
    client.post(
        "/perfil/inicio/medicion",
        data=measurement_data(
            birth_date="2014-01-01", reference_sex="male", weight_kg="40", height_cm="150"
        ),
    )
    row = db.session.scalar(db.select(HealthMeasurement))
    assert row.reference_source == "WHO-2007-LMS"
    assert user.profile.personalization_completed_at is None
    client.post(
        "/perfil/inicio/objetivo",
        data={"movement_goal": "center", "movement_preference": "adaptable"},
    )
    assert not student_setup_required(user)
    assert not member.allow_aggregate
    client.post("/acceso/salir")
    response = client.post(
        "/acceso/ingresar", data={"email": user.email, "password": "SecurePass123"}
    )
    assert response.location.endswith("/panel")


def test_pending_school_and_known_minor_cannot_store_measurements_even_with_direct_post(
    client, user_factory, login
):
    user = user_factory()
    login()
    client.post(
        "/colegios/",
        data={"school_name": "Colegio libre", "group_name": "8 B", "requested_role": "student"},
    )
    assert student_setup_required(user)
    assert not measurement_permission(user)
    for path in ("/perfil/inicio/medicion", "/perfil/"):
        client.post(
            path,
            data={**measurement_data(), "display_name": "Alumno", "usage_mode": "institutional"},
        )
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert "necesita una verificación" in client.get("/perfil/inicio/medicion").text
    user.profile.usage_mode = "personal"
    user.profile.birth_date = date(2014, 1, 1)
    db.session.commit()
    assert not measurement_permission(user)


def test_goal_cannot_be_spoofed_or_completed_without_consent(client, user_factory, login):
    user = user_factory()
    login()
    client.post("/perfil/inicio/medicion", data=measurement_data())
    for data in (
        {"movement_goal": "bmi-high", "movement_preference": "seated"},
        {"movement_goal": "strength", "movement_preference": "dangerous"},
    ):
        assert client.post("/perfil/inicio/objetivo", data=data).status_code == 200
        assert user.profile.personalization_completed_at is None
    user.profile.measurement_consent_at = None
    db.session.commit()
    assert (
        client.post(
            "/perfil/inicio/objetivo",
            data={"movement_goal": "strength", "movement_preference": "seated"},
        ).status_code
        == 302
    )


def test_personal_library_cannot_skip_setup_and_csrf_is_enforced(client, app, user_factory, login):
    assert client.get("/rutinas/?para=mi").status_code == 302
    user_factory()
    login()
    assert client.get("/rutinas/?para=mi").location.endswith("/perfil/inicio/medicion")
    app.config["WTF_CSRF_ENABLED"] = True
    assert client.post("/perfil/inicio/medicion", data=measurement_data()).status_code == 400
    assert client.post("/perfil/inicio/objetivo").status_code == 400


def test_authorized_student_must_provide_age_context_but_can_use_habits(
    client, user_factory, login, student_authorization
):
    user = user_factory()
    user.profile.usage_mode = "institutional"
    student_authorization(user)
    login()
    for path in ("/perfil/inicio/medicion", "/perfil/"):
        response = client.post(
            path,
            data={
                **measurement_data(birth_date=""),
                "display_name": "Estudiante",
                "usage_mode": "institutional",
            },
        )
        assert "Completa tu fecha de nacimiento" in response.text
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert client.get("/habitos/").status_code == 200
