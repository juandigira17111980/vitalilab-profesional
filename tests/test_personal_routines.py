import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import AuditEvent, HabitEntry, PersonalRoutine, RoutineCompletion, RoutineExercise
from app.services.movement import register_routine
from app.services.personal_routines import personal_routines_for
from app.services.progress import progress_for


def routine_payload(**changes):
    return {
        "name": "  Mi pausa  ",
        "description": "Un momento para mí",
        "goal": "strength",
        "revision": "0",
        "exercises-0-name": "Presión de palmas",
        "exercises-0-sets": "3",
        "exercises-0-repetitions": "8",
        "exercises-0-duration_seconds": "20",
        "exercises-0-rest_seconds": "30",
        "exercises-0-visual": "palms",
        "exercises-0-instructions": "Sin contener la respiración",
        **changes,
    }


@pytest.mark.parametrize("path", ["/mis-rutinas/nueva", "/mis-rutinas/1/", "/mis-rutinas/1/editar"])
def test_private_routines_require_login(client, path):
    response = client.get(path)
    assert response.status_code == 302 and response.headers["Cache-Control"] == "no-store"


def test_private_routine_create_edit_complete_archive_preserves_history(
    client, user_factory, login
):
    user = user_factory()
    login()
    response = client.post("/mis-rutinas/nueva", data=routine_payload(), follow_redirects=True)
    assert "Tu rutina está guardada" in response.text
    routine = db.session.scalar(db.select(PersonalRoutine))
    assert routine.user_id == user.id and routine.name == "Mi pausa"
    assert len(routine.exercises) == 1 and routine.exercises[0].sets == 3
    assert "exercises/palms.svg" in response.text
    assert "Mi pausa" in client.get("/rutinas/").text
    assert 'value="1"' in client.get(f"/mis-rutinas/{routine.id}/editar").text
    response = client.post(
        f"/mis-rutinas/{routine.id}/editar",
        data=routine_payload(name="Pausa renovada", revision="1"),
    )
    assert response.status_code == 302
    assert routine.revision == 2 and routine.name == "Pausa renovada"
    assert db.session.scalar(db.select(db.func.count(RoutineExercise.id))) == 1
    response = client.post(f"/mis-rutinas/{routine.id}/registrar", follow_redirects=True)
    assert "+15 XP" in response.text
    client.post(f"/mis-rutinas/{routine.id}/registrar")
    assert register_routine(user, "fortalece-tu-centro")["points"] == 0
    assert progress_for(user).points == 15
    assert db.session.scalar(db.select(db.func.count(HabitEntry.id))) == 1
    response = client.post(f"/mis-rutinas/{routine.id}/archivar", follow_redirects=True)
    assert "puntos se conservan" in response.text
    assert not routine.active and personal_routines_for(user) == []
    assert progress_for(user).points == 15
    assert db.session.scalar(db.select(db.func.count(RoutineCompletion.id))) == 2
    assert client.get(f"/mis-rutinas/{routine.id}/").status_code == 404
    assert register_routine(user, routine.slug) is None


def test_other_user_cannot_read_edit_complete_or_archive_and_html_is_escaped(
    client, user_factory, login
):
    owner = user_factory(email="owner@example.com")
    user_factory()
    login(email=owner.email)
    client.post("/mis-rutinas/nueva", data=routine_payload(name="<script>alert(1)</script>"))
    routine = db.session.scalar(db.select(PersonalRoutine))
    assert "<script>alert(1)</script>" not in client.get(f"/mis-rutinas/{routine.id}/").text
    client.post("/acceso/salir")
    login()
    for path in (f"/mis-rutinas/{routine.id}/", f"/mis-rutinas/{routine.id}/editar"):
        assert client.get(path).status_code == 404
    for action in ("editar", "registrar", "archivar"):
        assert (
            client.post(f"/mis-rutinas/{routine.id}/{action}", data=routine_payload()).status_code
            == 404
        )
    assert "alert(1)" not in client.get("/rutinas/").text
    assert routine.active and routine.user_id == owner.id


@pytest.mark.parametrize(
    "change",
    [
        {"name": " "},
        {"name": "x" * 81},
        {"goal": "admin"},
        {"revision": "bad"},
        {"exercises-0-name": ""},
        {"exercises-0-sets": "0"},
        {"exercises-0-sets": "21"},
        {"exercises-0-repetitions": "201"},
        {"exercises-0-duration_seconds": "-1"},
        {"exercises-0-rest_seconds": "601"},
        {"exercises-0-visual": "https://evil.test/a.svg"},
        {"exercises-0-duration_seconds": "", "exercises-0-repetitions": ""},
    ],
)
def test_private_routine_validates_each_field_server_side(client, user_factory, login, change):
    user_factory()
    login()
    response = client.post("/mis-rutinas/nueva", data=routine_payload(**change))
    assert response.status_code == 200 and "Revisa los campos marcados" in response.text
    assert db.session.scalar(db.select(db.func.count(PersonalRoutine.id))) == 0


def test_rep_only_or_time_only_and_zero_rest_are_supported(client, user_factory, login):
    user_factory()
    login()
    for changes in ({"exercises-0-repetitions": ""}, {"exercises-0-duration_seconds": ""}):
        assert (
            client.post(
                "/mis-rutinas/nueva",
                data=routine_payload(**changes, **{"exercises-0-rest_seconds": "0"}),
            ).status_code
            == 302
        )
    assert db.session.scalar(db.select(db.func.count(PersonalRoutine.id))) == 2


def test_stale_editor_does_not_overwrite_newer_version(client, user_factory, login):
    user_factory()
    login()
    client.post("/mis-rutinas/nueva", data=routine_payload())
    routine = db.session.scalar(db.select(PersonalRoutine))
    client.post(
        f"/mis-rutinas/{routine.id}/editar", data=routine_payload(name="Nuevo", revision="1")
    )
    response = client.post(
        f"/mis-rutinas/{routine.id}/editar", data=routine_payload(name="Perder", revision="1")
    )
    assert response.status_code == 409 and "otra ventana" in response.text
    assert routine.name == "Nuevo" and routine.revision == 2


def test_exercise_limit_and_no_js_add_button(client, user_factory, login):
    user_factory()
    login()
    response = client.post(
        "/mis-rutinas/nueva", data={**routine_payload(), "intent": "add-exercise"}
    )
    assert 'name="exercises-1-name"' in response.text
    assert db.session.scalar(db.select(db.func.count(PersonalRoutine.id))) == 0
    payload = routine_payload()
    for index in range(1, 13):
        payload.update(
            {
                key.replace("exercises-0-", f"exercises-{index}-"): value
                for key, value in routine_payload().items()
                if key.startswith("exercises-")
            }
        )
    response = client.post("/mis-rutinas/nueva", data=payload)
    assert "hasta 12 ejercicios" in response.text
    assert db.session.scalar(db.select(db.func.count(PersonalRoutine.id))) == 0


def test_database_dose_constraint_and_audit_does_not_copy_user_text(client, user_factory, login):
    user_factory()
    login()
    client.post("/mis-rutinas/nueva", data=routine_payload())
    exercise = db.session.scalar(db.select(RoutineExercise))
    exercise.duration_seconds = None
    exercise.repetitions = None
    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()
    event = db.session.scalar(
        db.select(AuditEvent).where(AuditEvent.action == "personal_routine.created")
    )
    assert event.metadata_redacted == {"exercise_count": 1}


def test_csrf_on_every_private_mutation(client, app, user_factory, login):
    user_factory()
    login()
    app.config["WTF_CSRF_ENABLED"] = True
    for path in (
        "/mis-rutinas/nueva",
        "/mis-rutinas/1/editar",
        "/mis-rutinas/1/registrar",
        "/mis-rutinas/1/archivar",
    ):
        assert client.post(path, data=routine_payload()).status_code == 400


def test_active_routine_quota_is_enforced(client, user_factory, login, monkeypatch):
    user = user_factory()
    login()
    client.post("/mis-rutinas/nueva", data=routine_payload())
    monkeypatch.setattr("app.services.personal_routines.MAX_ROUTINES", 1)
    response = client.post("/mis-rutinas/nueva", data=routine_payload())
    assert response.status_code == 409
    assert len(personal_routines_for(user)) == 1


def test_oversized_identifiers_fail_closed_and_slug_is_canonical(client, user_factory, login):
    user = user_factory()
    login()
    assert client.get("/mis-rutinas/999999999999999999999/").status_code == 404
    client.post("/mis-rutinas/nueva", data=routine_payload())
    routine = db.session.scalar(db.select(PersonalRoutine))
    assert register_routine(user, f"personal-0{routine.id}")["created"]
    assert not register_routine(user, routine.slug)["created"]
    assert db.session.scalar(db.select(db.func.count(RoutineCompletion.id))) == 1
    assert client.post(f"/rutinas/{routine.slug}/registrar").status_code == 404
