from app.extensions import db
from app.models import Announcement, HealthMeasurement


def test_health_readiness_and_security_headers(client):
    health = client.get("/health")
    ready = client.get("/ready")
    assert health.json["status"] == "ok"
    assert ready.json["status"] == "ready"
    assert "default-src 'self'" in health.headers["Content-Security-Policy"]
    assert health.headers["X-Frame-Options"] == "DENY"


def test_private_pages_redirect_anonymous_user(client):
    response = client.get("/panel")
    assert response.status_code == 302
    assert "/acceso/ingresar" in response.location


def test_profile_stores_optional_measurement(client, user_factory, login):
    user = user_factory()
    login()
    response = client.post(
        "/perfil/",
        data={
            "display_name": "Nombre actualizado",
            "grade": "10 A",
            "weight_kg": "70",
            "height_cm": "175",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    measurement = db.session.scalar(
        db.select(HealthMeasurement).where(HealthMeasurement.user_id == user.id)
    )
    assert float(measurement.bmi_snapshot) == 22.86


def test_admin_authorization_and_announcement_flow(client, user_factory, login):
    user_factory()
    login()
    assert client.get("/admin/").status_code == 403

    client.post("/acceso/salir")
    admin = user_factory(email="admin@example.com", role="admin")
    login(email=admin.email)
    response = client.post(
        "/admin/anuncios",
        data={"title": "Nueva jornada", "body": "Participa en la actividad de bienestar."},
        follow_redirects=True,
    )
    assert "Borrador guardado" in response.text
    announcement = db.session.scalar(db.select(Announcement))
    response = client.post(f"/admin/anuncios/{announcement.id}/publicar", follow_redirects=True)
    assert "Anuncio publicado" in response.text
    assert announcement.status == "published"
    response = client.post(f"/admin/anuncios/{announcement.id}/archivar", follow_redirects=True)
    assert "Anuncio archivado" in response.text
    assert announcement.status == "archived"


def test_profile_validation_and_measurement_deduplication(client, user_factory, login):
    user = user_factory()
    login()
    invalid = client.post(
        "/perfil/",
        data={"display_name": "Usuario", "weight_kg": "70"},
        follow_redirects=True,
    )
    assert "Revisa los campos marcados" in invalid.text

    payload = {
        "display_name": "Usuario",
        "grade": "10 A",
        "weight_kg": "70",
        "height_cm": "175",
    }
    client.post("/perfil/", data=payload)
    client.post("/perfil/", data=payload)
    count = db.session.scalar(
        db.select(db.func.count(HealthMeasurement.id)).where(HealthMeasurement.user_id == user.id)
    )
    assert count == 1


def test_public_content_and_not_found(client):
    assert client.get("/").status_code == 200
    assert client.get("/contenido/imc").status_code == 200
    assert client.get("/contenido/no-existe").status_code == 404
    assert client.get("/ruta-inexistente").status_code == 404
