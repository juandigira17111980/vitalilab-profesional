import pytest

from app.extensions import db
from app.models import School, SchoolEnrollmentRequest, SchoolGroup, SchoolMembership
from app.services.enrollment import enrollment_for, review_manual_enrollment
from app.services.school import teacher_groups, teacher_membership


@pytest.fixture()
def review_world(user_factory):
    admin = user_factory(email="manual-admin@example.com", role="admin")
    schools = [School(code=f"review-{i}", name=f"Colegio verificado {i}") for i in range(2)]
    db.session.add_all(schools)
    db.session.flush()
    groups = [SchoolGroup(school_id=s.id, name="Grupo A", academic_year=2026) for s in schools]
    db.session.add_all(groups)
    db.session.commit()
    return admin, schools, groups


def request_data(**values):
    return {
        "school_name": "  Colegio Nuevo del Barrio  ",
        "group_name": "  Octavo B  ",
        "requested_role": "student",
        **values,
    }


def test_school_and_group_are_free_text_and_never_auto_create_membership(
    client, user_factory, login
):
    user = user_factory()
    login()
    page = client.get("/colegios/").text
    assert 'name="school_name"' in page and 'name="group_name"' in page
    assert 'name="school_id"' not in page and "de práctica" not in page
    response = client.post(
        "/colegios/", data=request_data(requested_role="teacher"), follow_redirects=True
    )
    assert "Pendiente de verificación" in response.text
    item = enrollment_for(user)
    assert item.school_name == "Colegio Nuevo del Barrio" and item.group_name == "Octavo B"
    assert item.status == "pending" and user.role == "user"
    assert user.profile.institution_name == item.school_name
    assert db.session.scalar(db.select(db.func.count(School.id))) == 0
    assert db.session.scalar(db.select(db.func.count(SchoolMembership.id))) == 0
    assert client.get("/docentes/").status_code == 403
    assert client.get("/admin/colegios/").status_code == 403
    assert teacher_membership(user) is None
    assert "Ya tienes una vinculación" in client.post("/colegios/", data=request_data()).text
    client.post("/colegios/retirar")
    assert item.status == "cancelled"
    assert client.post("/colegios/", data=request_data()).status_code == 302
    assert db.session.scalar(db.select(db.func.count(SchoolEnrollmentRequest.id))) == 1
    assert item.requested_role == "student"


@pytest.mark.parametrize(
    "data",
    [
        {"school_name": " "},
        {"school_name": "x" * 161},
        {"group_name": ""},
        {"group_name": "x" * 81},
        {"requested_role": "admin"},
    ],
)
def test_manual_request_validation(client, user_factory, login, data):
    user_factory()
    login()
    response = client.post("/colegios/", data=request_data(**data))
    assert "Revisa el colegio" in response.text
    assert db.session.scalar(db.select(db.func.count(SchoolEnrollmentRequest.id))) == 0


def test_review_requires_admin_verified_identity_and_same_school_group(
    client, user_factory, login, review_world
):
    admin, schools, groups = review_world
    user = user_factory()
    login()
    client.post("/colegios/", data=request_data())
    item = enrollment_for(user)
    assert client.get(f"/admin/colegios/altas/{item.id}").status_code == 403
    with pytest.raises(PermissionError):
        review_manual_enrollment(user, item.id, schools[0].id, groups[0].id, "approved", True)
    with pytest.raises(ValueError):
        review_manual_enrollment(admin, item.id, schools[0].id, groups[0].id, "approved", False)
    with pytest.raises(ValueError):
        review_manual_enrollment(admin, item.id, schools[0].id, groups[1].id, "approved", True)
    with pytest.raises(ValueError):
        review_manual_enrollment(admin, item.id, schools[0].id, 0, "approved", True)
    assert item.status == "pending"
    client.post("/acceso/salir")
    login(email=admin.email)
    assert "Colegio Nuevo del Barrio" in client.get("/admin/colegios/").text
    assert client.get(f"/admin/colegios/altas/{item.id}").status_code == 200
    response = client.post(
        f"/admin/colegios/altas/{item.id}",
        data={
            "school_id": schools[0].id,
            "group_id": groups[0].id,
            "decision": "approved",
            "verified": "y",
        },
    )
    assert response.status_code == 302
    member = db.session.scalar(
        db.select(SchoolMembership).where(SchoolMembership.user_id == user.id)
    )
    assert member.status == "approved" and member.authorization_confirmed
    assert member.reviewed_by_user_id == admin.id and member.group_id == groups[0].id
    assert item.status == "resolved" and user.role == "user"
    assert not member.allow_aggregate and teacher_membership(user) is None
    with pytest.raises(ValueError):
        review_manual_enrollment(admin, item.id, schools[0].id, groups[0].id, "approved", True)


def test_teacher_approval_does_not_assign_groups_and_rejection_can_be_resubmitted(
    client, user_factory, login, review_world
):
    admin, schools, _ = review_world
    user = user_factory()
    login()
    client.post("/colegios/", data=request_data(requested_role="teacher"))
    item = enrollment_for(user)
    review_manual_enrollment(admin, item.id, schools[0].id, 0, "rejected", False)
    assert item.status == "rejected"
    client.post("/colegios/", data=request_data(requested_role="teacher"))
    review_manual_enrollment(admin, item.id, schools[0].id, 0, "approved", True)
    assert teacher_membership(user) is not None and teacher_groups(user) == []
    assert user.role == "user"


def test_new_admin_review_and_manual_enrollment_enforce_csrf(
    client, app, user_factory, login, review_world
):
    admin, _, _ = review_world
    user_factory()
    login()
    app.config["WTF_CSRF_ENABLED"] = True
    assert client.post("/colegios/", data=request_data()).status_code == 400
    app.config["WTF_CSRF_ENABLED"] = False
    client.post("/acceso/salir")
    login(email=admin.email)
    app.config["WTF_CSRF_ENABLED"] = True
    assert client.post("/admin/colegios/altas/1").status_code == 400
