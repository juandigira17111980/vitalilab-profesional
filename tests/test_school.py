from datetime import timedelta
from decimal import Decimal

import pytest

from app.extensions import db
from app.models import (
    Habit,
    HabitEntry,
    HealthMeasurement,
    School,
    SchoolGroup,
    SchoolMembership,
    TeacherGroupAssignment,
    User,
    UserProfile,
    utcnow,
)
from app.services.clock import local_day
from app.services.school import (
    assign_teacher,
    membership_for,
    report_for_group,
    request_membership,
    review_membership,
    seed_schools,
    teacher_groups,
    teacher_membership,
)


@pytest.fixture()
def school_world(user_factory):
    admin = user_factory(email="school-admin@example.com", role="admin")
    assert seed_schools() == 2
    assert seed_schools() == 0
    schools = list(db.session.scalars(db.select(School).order_by(School.id)))
    groups = [
        SchoolGroup(school_id=school.id, name="Grupo ficticio", academic_year=local_day(admin).year)
        for school in schools
    ]
    db.session.add_all(groups)
    db.session.commit()
    return {"admin": admin, "schools": schools, "groups": groups}


def make_teacher(user_factory, world, index=0):
    user = user_factory(email=f"teacher-{index}@example.com")
    member = request_membership(user, world["schools"][index].id, 0, "teacher")
    review_membership(world["admin"], member.id, "approved", verified=True)
    assign_teacher(world["admin"], member.id, world["groups"][index].id)
    return user, member


@pytest.mark.parametrize(
    "path",
    [
        "/colegios/",
        "/docentes/",
        "/docentes/grupos/1",
        "/docentes/rutinas/pausa-activa/proyectar",
        "/admin/colegios/",
    ],
)
def test_school_requires_session_and_no_store(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert response.headers["Cache-Control"] == "no-store"


def test_requesting_teacher_never_grants_permissions(client, school_world, user_factory, login):
    user = user_factory()
    login()
    response = client.post(
        "/colegios/",
        data={
            "school_id": school_world["schools"][0].id,
            "group_id": 0,
            "requested_role": "teacher",
        },
        follow_redirects=True,
    )
    assert "Pendiente de verificación" in response.text
    assert user.role == "user"
    assert teacher_membership(user) is None
    assert client.get("/docentes/").status_code == 403
    assert client.get("/admin/colegios/").status_code == 403
    assert client.get("/docentes/grupos/1").status_code == 404
    repeat = client.post(
        "/colegios/",
        data={
            "school_id": school_world["schools"][0].id,
            "group_id": 0,
            "requested_role": "teacher",
        },
        follow_redirects=True,
    )
    assert "Ya tienes una vinculación" in repeat.text


def test_cross_school_request_and_unknown_role_are_rejected(
    client, school_world, user_factory, login
):
    user = user_factory()
    login()
    school, other_group = school_world["schools"][0], school_world["groups"][1]
    response = client.post(
        "/colegios/",
        data={"school_id": school.id, "group_id": other_group.id, "requested_role": "student"},
    )
    assert "debe pertenecer" in response.text
    response = client.post(
        "/colegios/", data={"school_id": school.id, "group_id": 0, "requested_role": "admin"}
    )
    assert "válidos" in response.text
    assert membership_for(user) is None
    with pytest.raises(ValueError):
        request_membership(user, 9999, 0, "teacher")


def test_teacher_approval_assignment_revocation_and_tenant_isolation(
    client, school_world, user_factory, login
):
    teacher, member = make_teacher(user_factory, school_world)
    login(email=teacher.email)
    assert "Panel docente" in client.get("/panel").text
    assert client.get("/docentes/").status_code == 200
    assert client.get(f"/docentes/grupos/{school_world['groups'][0].id}").status_code == 200
    assert client.get(f"/docentes/grupos/{school_world['groups'][1].id}").status_code == 404
    projection = client.get("/docentes/rutinas/fortalece-tu-centro/proyectar")
    assert projection.status_code == 200
    assert "Fortalece tu centro" in projection.text
    assert teacher.email not in projection.text
    assert client.get("/docentes/rutinas/no-existe/proyectar").status_code == 404
    teacher.profile.usage_mode = "personal"
    db.session.commit()
    assert client.get("/docentes/").status_code == 403
    assert client.get("/docentes/rutinas/pausa-activa/proyectar").status_code == 403
    teacher.profile.usage_mode = "institutional"
    review_membership(school_world["admin"], member.id, "revoked")
    assert client.get("/docentes/").status_code == 403
    assert teacher_groups(teacher) == []
    assert db.session.scalar(db.select(db.func.count(TeacherGroupAssignment.id))) == 0


def test_approval_checks_and_cross_school_assignments(school_world, user_factory):
    student = user_factory()
    member = request_membership(student, school_world["schools"][0].id, 0, "student")
    with pytest.raises(PermissionError):
        review_membership(student, member.id, "approved", verified=True)
    with pytest.raises(ValueError):
        review_membership(school_world["admin"], member.id, "approved")
    with pytest.raises(ValueError):
        review_membership(school_world["admin"], member.id, "approved", verified=True)
    with pytest.raises(ValueError):
        review_membership(
            school_world["admin"],
            member.id,
            "approved",
            group_id=school_world["groups"][1].id,
            verified=True,
        )
    review_membership(
        school_world["admin"],
        member.id,
        "approved",
        group_id=school_world["groups"][0].id,
        verified=True,
    )
    with pytest.raises(ValueError):
        assign_teacher(school_world["admin"], member.id, school_world["groups"][0].id)
    with pytest.raises(PermissionError):
        assign_teacher(student, member.id, school_world["groups"][0].id)
    teacher, teacher_member = make_teacher(user_factory, school_world)
    with pytest.raises(ValueError):
        assign_teacher(school_world["admin"], teacher_member.id, school_world["groups"][1].id)
    assert not assign_teacher(
        school_world["admin"], teacher_member.id, school_world["groups"][0].id
    )
    teacher.status = "inactive"
    assert teacher_membership(teacher) is None


def test_withdraw_and_rerequest_never_reuse_teacher_permissions(
    client, school_world, user_factory, login
):
    teacher, member = make_teacher(user_factory, school_world)
    login(email=teacher.email)
    response = client.post("/colegios/retirar", follow_redirects=True)
    assert "Vinculación retirada" in response.text
    assert member.status == "revoked"
    assert not member.allow_aggregate
    assert client.get("/docentes/").status_code == 403
    new_member = request_membership(teacher, school_world["schools"][1].id, 0, "teacher")
    assert new_member.id == member.id
    assert new_member.status == "pending"
    assert teacher_groups(teacher) == []
    assert db.session.scalar(db.select(db.func.count(User.id))) == 2


def test_pausing_group_or_school_removes_teacher_access(school_world, user_factory):
    teacher, _ = make_teacher(user_factory, school_world)
    group, school = school_world["groups"][0], school_world["schools"][0]
    group.active = False
    db.session.commit()
    with pytest.raises(PermissionError):
        report_for_group(teacher, group.id)
    group.active = True
    school.active = False
    db.session.commit()
    assert teacher_membership(teacher) is None
    assert teacher_groups(teacher) == []


def test_student_consent_is_optional_and_reset_on_reapproval(
    client, school_world, user_factory, login
):
    student = user_factory()
    login()
    response = client.post(
        "/colegios/estadisticas", data={"allow_aggregate": "y"}, follow_redirects=True
    )
    assert "después de aprobar" in response.text
    member = request_membership(
        student, school_world["schools"][0].id, school_world["groups"][0].id, "student"
    )
    assert not member.allow_aggregate
    review_membership(
        school_world["admin"], member.id, "approved", school_world["groups"][0].id, True
    )
    response = client.post(
        "/colegios/estadisticas", data={"allow_aggregate": "y"}, follow_redirects=True
    )
    assert "Preferencia actualizada" in response.text
    assert member.allow_aggregate and member.aggregate_since
    response = client.post("/colegios/estadisticas", data={}, follow_redirects=True)
    assert not member.allow_aggregate and member.aggregate_since is None
    assert response.status_code == 200


def test_admin_ui_controls_catalog_groups_reviews_and_assignments(
    client, school_world, user_factory, login
):
    candidate = user_factory()
    member = request_membership(candidate, school_world["schools"][0].id, 0, "teacher")
    login(email=school_world["admin"].email)
    assert client.get("/admin/colegios/").status_code == 200
    response = client.post(
        "/admin/colegios/crear",
        data={"school-code": "colegio-qa", "school-name": "Colegio QA ficticio"},
        follow_redirects=True,
    )
    assert "Colegio creado" in response.text
    assert (
        "identificador ya"
        in client.post(
            "/admin/colegios/crear",
            data={"school-code": "colegio-qa", "school-name": "Duplicado"},
            follow_redirects=True,
        ).text
    )
    assert (
        "Revisa el nombre"
        in client.post(
            "/admin/colegios/crear",
            data={"school-code": "@@", "school-name": "a"},
            follow_redirects=True,
        ).text
    )
    payload = {
        "group-school_id": school_world["schools"][0].id,
        "group-name": "Grupo B",
        "group-academic_year": local_day(candidate).year,
    }
    assert (
        "Grupo creado"
        in client.post("/admin/colegios/grupos", data=payload, follow_redirects=True).text
    )
    assert (
        "Ya existe ese grupo"
        in client.post("/admin/colegios/grupos", data=payload, follow_redirects=True).text
    )
    assert (
        "Revisa el colegio"
        in client.post(
            "/admin/colegios/grupos",
            data={**payload, "group-academic_year": 1},
            follow_redirects=True,
        ).text
    )
    path = f"/admin/colegios/solicitudes/{member.id}"
    assert client.get(path).status_code == 200
    assert (
        "verificación"
        in client.post(
            path, data={"decision": "approved", "group_id": 0}, follow_redirects=True
        ).text
    )
    response = client.post(
        path, data={"decision": "approved", "group_id": 0, "verified": "y"}, follow_redirects=True
    )
    assert "Revisión guardada" in response.text
    assignment = {
        "assignment-membership_id": member.id,
        "assignment-group_id": school_world["groups"][0].id,
    }
    assert (
        "Grupo asignado"
        in client.post("/admin/colegios/asignaciones", data=assignment, follow_redirects=True).text
    )
    assert (
        "ya existe"
        in client.post("/admin/colegios/asignaciones", data=assignment, follow_redirects=True).text
    )
    assert (
        "mismo colegio"
        in client.post(
            "/admin/colegios/asignaciones",
            data={**assignment, "assignment-group_id": school_world["groups"][1].id},
            follow_redirects=True,
        ).text
    )
    assert (
        "Selecciona un docente"
        in client.post("/admin/colegios/asignaciones", data={}, follow_redirects=True).text
    )
    item = db.session.scalar(db.select(TeacherGroupAssignment))
    assert (
        "Asignación retirada"
        in client.post(
            f"/admin/colegios/asignaciones/{item.id}/retirar", follow_redirects=True
        ).text
    )
    assert (
        "Estado actualizado"
        in client.post(
            f"/admin/colegios/colegio/{school_world['schools'][0].id}/estado", follow_redirects=True
        ).text
    )
    assert (
        "Estado actualizado"
        in client.post(
            f"/admin/colegios/grupo/{school_world['groups'][0].id}/estado", follow_redirects=True
        ).text
    )
    assert client.post("/admin/colegios/otro/1/estado").status_code == 400


def add_cohort(world, count=10):
    now = utcnow()
    day = local_day(world["admin"])
    habit = db.session.scalar(db.select(Habit).where(Habit.code == "gentle-movement"))
    members = []
    for number in range(count):
        user = User(email=f"cohort-{number}@example.com", password_hash="not-a-login-fixture")
        user.profile = UserProfile(
            display_name=f"Nombre privado {number}", usage_mode="institutional"
        )
        db.session.add(user)
        db.session.flush()
        member = SchoolMembership(
            user_id=user.id,
            school_id=world["schools"][0].id,
            group_id=world["groups"][0].id,
            requested_role="student",
            status="approved",
            authorization_confirmed=True,
            allow_aggregate=True,
            aggregate_since=now - timedelta(days=2),
            reviewed_at=now - timedelta(days=3),
            reviewed_by_user_id=world["admin"].id,
        )
        db.session.add(member)
        db.session.add(
            HealthMeasurement(
                user_id=user.id,
                weight_kg=Decimal("45"),
                height_cm=Decimal("150"),
                bmi_snapshot=Decimal("20"),
                measured_on=day,
                growth_percentile=Decimal("50"),
                reference_source="WHO-2007-LMS",
                age_months=150,
                reference_sex="male",
            )
        )
        db.session.add(HabitEntry(user_id=user.id, habit_id=habit.id, completed_on=day))
        members.append(member)
    db.session.commit()
    return members


def test_small_cohort_never_exposes_count_names_or_measurements(
    client, school_world, user_factory, login
):
    teacher, _ = make_teacher(user_factory, school_world)
    add_cohort(school_world, 9)
    login(email=teacher.email)
    response = client.get(f"/docentes/grupos/{school_world['groups'][0].id}")
    assert "no hay suficientes" in response.text
    assert "Nombre privado" not in response.text
    assert "cohort-" not in response.text
    assert "45.00" not in response.text


def test_aggregates_suppress_each_month_and_respect_opt_out_and_old_rows(
    client, school_world, user_factory, login
):
    teacher, _ = make_teacher(user_factory, school_world)
    members = add_cohort(school_world)
    report = report_for_group(teacher, school_world["groups"][0].id)
    current = report["months"][local_day(teacher).month - 1]
    assert current["growth"] == 10 and current["activity"] == 10 and current["percentile"] == 50
    assert any(month["growth"] is None for month in report["months"])
    login(email=teacher.email)
    response = client.get(f"/docentes/grupos/{school_world['groups'][0].id}")
    assert "Promedio aproximado" in response.text
    assert (
        'tabindex="0" role="region" aria-label="Indicadores mensuales del grupo"' in response.text
    )
    assert "Nombre privado" not in response.text
    assert "cohort-" not in response.text
    # One historical/nonconsented measurement must suppress the metric, not expose nine.
    row = db.session.scalar(
        db.select(HealthMeasurement).where(HealthMeasurement.user_id == members[0].user_id)
    )
    row.created_at = members[0].aggregate_since - timedelta(days=1)
    db.session.commit()
    assert (
        report_for_group(teacher, school_world["groups"][0].id)["months"][
            local_day(teacher).month - 1
        ]["growth"]
        is None
    )
    members[0].allow_aggregate = False
    db.session.commit()
    assert not report_for_group(teacher, school_world["groups"][0].id)["sufficient"]


def test_school_posts_enforce_csrf(client, app, school_world, user_factory, login):
    user_factory()
    login()
    app.config["WTF_CSRF_ENABLED"] = True
    for path in (
        "/colegios/",
        "/colegios/retirar",
        "/colegios/estadisticas",
        "/admin/colegios/crear",
        "/rutinas/fortalece-tu-centro/registrar",
    ):
        assert client.post(path).status_code == 400


def test_seed_command_does_not_reactivate_paused_schools(app, school_world):
    school_world["schools"][0].active = False
    db.session.commit()
    result = app.test_cli_runner().invoke(args=["seed-schools"])
    assert result.exit_code == 0
    assert not school_world["schools"][0].active
