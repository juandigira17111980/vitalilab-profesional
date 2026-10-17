from datetime import date

import pytest

from app.extensions import db
from app.models import HealthMeasurement, SchoolMembership, User
from app.services.personalization import measurement_access, measurement_permission
from app.services.school import review_membership


def measurement_data(**changes):
    return {
        "weight_kg": "58",
        "height_cm": "174",
        "birth_date": "2009-11-11",
        "reference_sex": "unspecified",
        "measurement_consent": "y",
        **changes,
    }


@pytest.mark.parametrize("path", ["/perfil/inicio/medicion", "/perfil/"])
def test_first_minor_birth_date_has_actionable_notice_not_weight_error(
    client, user_factory, login, path
):
    user = user_factory()
    login()
    assert measurement_permission(user)  # Previously unknown birth date, initial GET.
    response = client.post(
        path,
        data={**measurement_data(), "display_name": "Mi perfil", "usage_mode": "personal"},
        follow_redirects=True,
    )
    assert response.status_code == 200
    if path == "/perfil/":
        assert 'data-measurement-access="minor-authorization"' in response.text
        assert "No se guardaron estas mediciones" in response.text
    else:
        assert "Tu objetivo, tu ritmo" in response.text
    assert "Tu institución debe verificar" not in response.text
    assert 'class="field-error"' not in response.text
    assert user.profile.birth_date is None
    assert user.profile.measurement_consent_at is None
    assert user.profile.personalization_completed_at is None
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert db.session.scalar(db.select(db.func.count(SchoolMembership.id))) == 0
    assert "no-store" in response.headers["Cache-Control"]


def test_legacy_minor_attempt_continues_to_goals_and_adult_can_still_save_optional_measurement(
    client, user_factory, login
):
    user = user_factory()
    login()
    blocked = client.post("/perfil/inicio/medicion", data=measurement_data())
    assert blocked.status_code == 302
    assert blocked.location.endswith("/perfil/inicio/objetivo")
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    saved = client.post("/perfil/inicio/medicion", data=measurement_data(birth_date="1990-11-11"))
    assert saved.status_code == 302 and saved.location.endswith("/perfil/inicio/objetivo")
    row = db.session.scalar(db.select(HealthMeasurement))
    assert str(row.bmi_snapshot) == "19.16"
    assert user.profile.birth_date == date(1990, 11, 11)


def test_known_minor_does_not_get_measurement_inputs_before_review(client, user_factory, login):
    user = user_factory()
    user.profile.birth_date = date(2014, 1, 1)
    db.session.commit()
    login()
    response = client.get("/perfil/inicio/medicion", follow_redirects=True)
    assert "Tu objetivo, tu ritmo" in response.text
    assert 'name="weight_kg"' not in response.text
    assert "Guardar mi objetivo y ver rutinas" in response.text
    assert client.get("/habitos/").status_code == 200


@pytest.mark.parametrize(
    "change,code",
    [
        ("pending", "membership-review"),
        ("rejected", "membership-review"),
        ("revoked", "membership-review"),
        ("school", "school-inactive"),
        ("group", "group-unavailable"),
        ("no-group", "group-unavailable"),
        ("consent", "authorization-review"),
        ("review-date", "authorization-review"),
        ("reviewer", "authorization-review"),
    ],
)
def test_access_explains_each_missing_requirement_without_weakening_permission(
    client, user_factory, login, student_authorization, change, code
):
    user = user_factory()
    user.profile.usage_mode = "institutional"
    user.profile.birth_date = date(2014, 1, 1)
    member = student_authorization(user)
    if change in {"pending", "rejected", "revoked"}:
        member.status = change
    elif change == "school":
        member.school.active = False
    elif change == "group":
        member.group.active = False
    elif change == "no-group":
        member.group_id = None
    elif change == "consent":
        member.authorization_confirmed = False
    elif change == "review-date":
        member.reviewed_at = None
    else:
        member.reviewed_by_user_id = None
    db.session.commit()
    assert not measurement_permission(user)
    access = measurement_access(user)
    assert not access.allowed and access.code == code
    login()
    for path in ("/perfil/inicio/medicion", "/perfil/"):
        response = client.post(
            path,
            data={
                **measurement_data(),
                "display_name": "Mi perfil",
                "usage_mode": "institutional",
            },
        )
        assert f'data-measurement-access="{code}"' in response.text
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 0
    assert user.profile.measurement_consent_at is None


def test_real_administrative_review_unblocks_measurement_without_enabling_aggregates(
    client, user_factory, login, student_authorization
):
    user = user_factory()
    user.profile.usage_mode = "institutional"
    user.profile.birth_date = date(2009, 11, 11)
    member = student_authorization(user)
    reviewer = db.session.get(User, member.reviewed_by_user_id)
    member.status = "pending"
    member.authorization_confirmed = False
    member.reviewed_at = None
    member.reviewed_by_user_id = None
    db.session.commit()
    login()
    blocked = client.post("/perfil/inicio/medicion", data=measurement_data())
    assert "pendiente de revisión" in blocked.text
    review_membership(reviewer, member.id, "approved", member.group_id, verified=True)
    assert measurement_access(user).allowed
    saved = client.post("/perfil/inicio/medicion", data=measurement_data())
    assert saved.status_code == 302
    assert saved.location.endswith("/perfil/inicio/objetivo")
    assert db.session.scalar(db.select(db.func.count(HealthMeasurement.id))) == 1
    assert not member.allow_aggregate
