"""Study exports must remain complete, reproducible and free of application data."""

import json
from pathlib import Path

import pytest

from app.extensions import db
from scripts.export_dba_study import (
    PURPOSES,
    dictionary,
    graphviz,
    mermaid,
    relationships,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs/dba"


@pytest.fixture
def catalog():
    return json.loads((DEST / "catalogo_postgresql.json").read_text(encoding="utf-8"))


def test_complete_catalog_matches_models(app, catalog):
    validate(catalog)
    assert len(catalog["tables"]) == 17
    assert sum(len(t["columns"]) for t in catalog["tables"]) == 148
    assert len(list(relationships(catalog))) == 22
    with app.app_context():
        assert set(PURPOSES) == set(db.metadata.tables)
        for table in catalog["tables"]:
            model = db.metadata.tables[table["name"]]
            assert {c["name"] for c in table["columns"]} == set(model.columns.keys())
            assert {
                (tuple(k["columns"]), k["target_table"], tuple(k["target_columns"]))
                for k in table["constraints"]
                if k["kind"] == "f"
            } == {
                (
                    tuple(e.parent.name for e in fk.elements),
                    fk.referred_table.name,
                    tuple(e.column.name for e in fk.elements),
                )
                for fk in model.foreign_key_constraints
            }


def test_generated_sources_are_current(catalog):
    assert dictionary(catalog) == (DEST / "diccionario_postgresql.md").read_text(encoding="utf-8")
    assert mermaid(catalog) == (DEST / "modelo_completo.mmd").read_text(encoding="utf-8")
    assert graphviz(catalog) == (DEST / "modelo_completo.dot").read_text(encoding="utf-8")


def test_unknown_schema_is_rejected(catalog):
    catalog["migration_revision"] = "unknown"
    with pytest.raises(ValueError, match="Unexpected schema"):
        validate(catalog)


def test_physical_relationships_not_invented(catalog):
    keys = [(t["name"], k["columns"]) for t, k in relationships(catalog)]
    assert ("routine_completions", ["routine_slug"]) not in keys
    assert ("school_enrollment_requests", ["school_name"]) not in keys
    assert ("school_memberships", ["group_id", "school_id"]) in keys
    assert ("teacher_group_assignments", ["membership_id", "school_id"]) in keys
    source = mermaid(catalog)
    assert 'users ||--o| user_profiles : "user_id"' in source
    assert 'users o|--o{ audit_events : "actor_user_id"' in source


def test_schema_export_has_no_rows_or_roles():
    ddl = (DEST / "estructura_postgresql.sql").read_text(encoding="utf-8")
    for unsafe in ("INSERT INTO", "COPY public.", "CREATE ROLE", "PASSWORD '", "CREATE FUNCTION"):
        assert unsafe not in ddl
    assert ddl.count("CREATE TABLE public.") == 18


def test_seed_and_practice_are_guarded():
    for filename in ("datos_ficticios.sql", "practicas_transacciones.sql"):
        sql = (DEST / filename).read_text(encoding="utf-8")
        assert "current_database() <> 'vitalilab_estudio_ega1026'" in sql
        assert "vitalilab_staging" not in sql
    seed = (DEST / "datos_ficticios.sql").read_text(encoding="utf-8")
    assert "@example.invalid" in seed
    assert "not-a-real-login-hash" in seed
    assert "ROLLBACK;" in (DEST / "practicas_transacciones.sql").read_text(encoding="utf-8")


def test_study_role_is_not_activated_or_privileged():
    sql = (ROOT / "deploy/study/roles.sql").read_text(encoding="utf-8")
    assert "ega1026_estudio NOLOGIN NOSUPERUSER NOCREATEDB NOCREATEROLE" in sql
    assert "GRANT SELECT ON ALL TABLES" in sql
    assert "GRANT CONNECT" in sql
    assert "GRANT CREATE ON SCHEMA public" not in sql
    assert "pg_read_all_data" not in sql
    assert "PASSWORD '" not in sql


def test_study_instance_has_no_production_mounts_or_networks():
    compose = (ROOT / "deploy/study/compose.yaml").read_text(encoding="utf-8")
    assert "127.0.0.1:55432:5432" in compose
    assert "ssl=on" in compose
    assert "internal: true" in compose
    assert "vitalilab-db-lab" not in compose
    assert "/opt/labs/vitalilab/" not in compose
