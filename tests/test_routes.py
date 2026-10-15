import pytest

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


@pytest.mark.parametrize("path", ["/", "/panel"])
def test_footer_only_shows_brand(client, user_factory, login, path):
    if path == "/panel":
        user_factory()
        login()
    response = client.get(path)
    assert response.status_code == 200
    footer = response.text.split('<footer class="site-footer">', 1)[1].split("</footer>", 1)[0]
    assert 'class="brand brand--footer"' in footer
    assert 'aria-label="VitaliLab, inicio"' in footer
    assert footer.count("<a ") == 1
    assert "<p" not in footer
    assert "<h2" not in footer
    for removed in (
        "Haz espacio para lo que te hace bien.",
        "Explora",
        "Rutinas guiadas",
        "Indicadores educativos",
        "Cómo funciona",
        "Privacidad",
        "Proyecto educativo; no sustituye orientación médica.",
        "©",
    ):
        assert removed not in footer


def test_footer_cleanup_preserves_privacy_and_content_routes(client):
    registration = client.get("/acceso/registro")
    assert registration.status_code == 200
    assert 'href="/privacidad"' in registration.text
    assert 'name="privacy_accepted"' in registration.text
    for path in ("/privacidad", "/contenido/imc", "/contenido/fundamentos", "/rutinas/"):
        assert client.get(path).status_code == 200


@pytest.mark.parametrize("environment", ["development", "staging", "production"])
def test_professional_presentation_has_no_academic_demo_banners(client, app, environment):
    app.config["APP_ENV"] = environment
    for path in ("/", "/privacidad", "/rutinas/", "/acceso/registro"):
        page = client.get(path).text.lower()
        for text in (
            "laboratorio académico",
            "datos ficticios",
            "piloto académico",
            "versión académica",
            "no es el sitio de producción",
            "antes de producción",
        ):
            assert text not in page


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
            "measurement_consent": "y",
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
        "measurement_consent": "y",
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
