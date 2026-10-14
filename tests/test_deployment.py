import tempfile
from pathlib import Path

from app import create_app
from scripts.build_vercel import prepare_static_assets


def test_vercel_factory_uses_writable_temporary_instance_path(monkeypatch):
    monkeypatch.setenv("VERCEL", "1")
    application = create_app({"TESTING": True, "RATELIMIT_ENABLED": False})
    assert Path(application.instance_path) == Path(tempfile.gettempdir()) / "vitalilab-instance"
    assert application.test_client().get("/health").status_code == 200


def test_vercel_assets_keep_the_urls_rendered_by_jinja(tmp_path):
    source = tmp_path / "app" / "static" / "css"
    source.mkdir(parents=True)
    (source / "app.css").write_text("body { color: black; }", encoding="utf-8")
    assert prepare_static_assets(tmp_path) == 1
    assert (tmp_path / "public" / "static" / "css" / "app.css").read_text(
        encoding="utf-8"
    ) == "body { color: black; }"
