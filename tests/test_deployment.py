from pathlib import Path

from app import create_app


def test_factory_uses_the_standard_flask_instance_directory():
    application = create_app({"TESTING": True, "RATELIMIT_ENABLED": False})
    assert Path(application.instance_path) == Path(application.root_path).parent / "instance"
    assert Path(application.instance_path).is_dir()
    assert application.test_client().get("/health").status_code == 200


def test_flask_serves_the_stylesheet_referenced_by_the_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "/static/css/app.css" in response.text
    stylesheet = client.get("/static/css/app.css")
    assert stylesheet.status_code == 200
    assert stylesheet.mimetype == "text/css"
    assert stylesheet.data
