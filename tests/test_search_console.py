import pytest

from app.extensions import db

VERIFICATION_PATH = "/google758e0558a7bc12dd.html"
VERIFICATION_BODY = b"google-site-verification: google758e0558a7bc12dd.html"


@pytest.mark.parametrize("host", ["vitalilab.space", "www.vitalilab.space"])
def test_google_ownership_file_is_public_and_exact(client, host):
    response = client.get(VERIFICATION_PATH, base_url=f"https://{host}")
    assert response.status_code == 200
    assert response.data == VERIFICATION_BODY
    assert response.mimetype == "text/html"
    assert "Location" not in response.headers
    assert "Set-Cookie" not in response.headers
    assert response.headers["X-Robots-Tag"] == "noindex"
    assert response.headers["Cache-Control"] == "public, max-age=300"
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_google_file_does_not_query_the_database_and_supports_head(client, monkeypatch):
    def reject_query(*args, **kwargs):
        raise AssertionError("The ownership file must not query user data")

    monkeypatch.setattr(db.session, "execute", reject_query)
    monkeypatch.setattr(db.session, "scalars", reject_query)
    assert client.get(VERIFICATION_PATH).data == VERIFICATION_BODY
    response = client.head(VERIFICATION_PATH)
    assert response.status_code == 200
    assert response.data == b""
    assert response.content_length == len(VERIFICATION_BODY)


def test_google_verification_is_not_a_generic_file_or_write_endpoint(client):
    assert client.get("/google-unknown.html").status_code == 404
    assert client.get("/google758e0558a7bc12dd.html/extra").status_code == 404
    assert client.post(VERIFICATION_PATH).status_code == 405
