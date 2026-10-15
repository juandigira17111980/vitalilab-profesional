"""Read PostgreSQL catalogs and produce a non-sensitive, reproducible DBA study kit."""

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "docs" / "dba"
PURPOSES = {
    "users": "Identidad de la cuenta, autenticación y estado de acceso.",
    "user_profiles": "Perfil, preferencias, contexto y confirmaciones de privacidad.",
    "health_measurements": "Historial de mediciones con el contexto del momento registrado.",
    "habits": "Catálogo de hábitos y puntos por cumplimiento.",
    "habit_entries": "Cumplimiento diario de cada hábito por usuario.",
    "user_goals": "Meta semanal del usuario para un hábito concreto.",
    "daily_checkins": "Bitácora de energía y enfoque por fecha.",
    "schools": "Catálogo institucional gestionado por administración.",
    "school_groups": "Grupos de un colegio y un año académico.",
    "school_memberships": "Vinculación revisada de una cuenta con una institución.",
    "teacher_group_assignments": "Asignación docente a grupos del mismo colegio.",
    "school_enrollment_requests": "Solicitud escrita que no concede permisos institucionales.",
    "personal_routines": "Cabecera privada de una rutina y control de su revisión.",
    "routine_exercises": "Ejercicios ordenados de una rutina, con dosis y descansos.",
    "routine_completions": "Actividad declarada por usuario, identificador de rutina y día.",
    "announcements": "Comunicados, autor y estado de publicación.",
    "audit_events": "Eventos técnicos con metadatos redactados, no un historial médico.",
}
MEANINGS = {
    "id": "Identificador de la fila; no representa una medida ni un código externo.",
    "created_at": "Instante de creación. Convención UTC sin zona incorporada al tipo SQL.",
    "updated_at": "Última modificación registrada por la aplicación, con convención UTC.",
    "user_id": "Cuenta propietaria o vinculada; véase la clave foránea.",
    "email": "Correo único para acceso; no debe exponerse con datos reales en una sustentación.",
    "password_hash": "Hash scrypt de acceso, nunca contraseña en texto. El ejemplo no es válido.",
    "role": "Rol de aplicación user/admin; distinto de un rol PostgreSQL y del rol escolar.",
    "status": "Estado permitido por el CHECK de esta tabla; no siempre comparte vocabulario.",
    "last_login_at": "Instante del último ingreso correcto.",
    "failed_login_count": "Intentos fallidos usados por el bloqueo temporal de la aplicación.",
    "locked_until": "Fin del bloqueo temporal; NULL significa que no hay fecha registrada.",
    "display_name": "Nombre o apodo mostrado en el perfil.",
    "birth_date": "Fecha de nacimiento opcional; permite obtener edad al medir.",
    "usage_mode": "Experiencia personal o institucional; no concede permisos por sí sola.",
    "institution_name": "Texto de contexto del perfil; no sustituye una vinculación verificada.",
    "reference_sex": "Referencia de crecimiento registrada, no identidad de género.",
    "movement_goal": "Objetivo funcional center, energy o strength; no categoría de IMC.",
    "movement_preference": "Preferencia adaptable, seated, supported o standing.",
    "personalization_completed_at": "Final del recorrido inicial; evita repetirlo en cada ingreso.",
    "measurement_consent_at": "Instante de la confirmación para guardar mediciones.",
    "grade": "Texto de grado, grupo o área conservado en el perfil.",
    "timezone": "Zona IANA utilizada para determinar el día local del usuario.",
    "privacy_version": "Versión de la política aceptada.",
    "privacy_accepted_at": "Instante de aceptación de la política.",
    "weight_kg": "Peso registrado en kilogramos, validado por límites técnicos.",
    "height_cm": "Altura registrada en centímetros; se convierte a metros al calcular IMC.",
    "bmi_snapshot": "IMC guardado en esa medición; no se recalcula al cambiar el perfil.",
    "age_months": "Edad en meses cumplidos en la fecha de la medición.",
    "reference_source": "Identificador de la referencia utilizada, cuando procede.",
    "growth_percentile": "Percentil descriptivo cuando el cálculo tiene contexto suficiente.",
    "measured_on": "Fecha de negocio de la medición; no equivale al instante created_at.",
    "code": "Código estable y único del catálogo correspondiente.",
    "name": "Nombre legible del elemento representado por esta tabla.",
    "description": "Descripción visible del hábito o rutina.",
    "category": "Agrupación del hábito para su presentación.",
    "icon": "Identificador del icono utilizado en la interfaz.",
    "points": "Puntos del hábito; no una columna de puntos acumulados por usuario.",
    "active": "Disponibilidad lógica del elemento, sin borrarlo físicamente.",
    "sort_order": "Posición de presentación del hábito.",
    "habit_id": "Hábito relacionado del catálogo.",
    "completed_on": "Día local al que corresponde un cumplimiento.",
    "target_days": "Meta entre uno y siete días para un hábito.",
    "checked_on": "Día de la entrada de bitácora; único por usuario y fecha.",
    "energy": "Energía declarada en escala de uno a cinco.",
    "focus": "Enfoque declarado en escala de uno a cinco.",
    "school_id": "Colegio asociado; también participa en claves foráneas compuestas.",
    "academic_year": "Año del grupo, independiente del año actual del servidor.",
    "group_id": "Grupo asociado; puede ser opcional en una membresía.",
    "requested_role": "Rol escolar solicitado student/teacher; requiere revisión de la aplicación.",
    "allow_aggregate": "Preferencia voluntaria de inclusión en agregados.",
    "aggregate_since": "Inicio de la preferencia vigente de agregación.",
    "reviewed_at": "Instante de revisión administrativa.",
    "reviewed_by_user_id": "Cuenta revisora opcional; SET NULL conserva el evento sin ella.",
    "authorization_confirmed": "Confirmación administrativa necesaria para la vinculación.",
    "membership_id": "Vinculación del docente, comprobada junto con school_id.",
    "routine_slug": "Identificador textual del catálogo o personal-ID; no es una FK física.",
    "school_name": "Nombre escrito por la persona solicitante, aún sin validación institucional.",
    "group_name": "Grupo escrito en la solicitud, no una FK al catálogo de grupos.",
    "goal": "Objetivo funcional de la rutina propia.",
    "revision": "Versión optimista de edición; evita sobrescribir cambios de otra ventana.",
    "routine_id": "Rutina personal a la que pertenece el ejercicio.",
    "position": "Posición de cero a once; única dentro de su rutina.",
    "sets": "Series entre uno y veinte; límite técnico, no prescripción individual.",
    "repetitions": "Repeticiones opcionales; debe existir repetición o duración.",
    "duration_seconds": "Duración opcional en segundos.",
    "rest_seconds": "Descanso en segundos según los límites técnicos.",
    "instructions": "Instrucciones escritas del ejercicio.",
    "visual": "Referencia de demostración SVG o custom; no contiene un archivo de imagen.",
    "author_user_id": "Cuenta autora del comunicado; no se borra si hay referencias RESTRICT.",
    "title": "Título del comunicado.",
    "body": "Contenido del comunicado, escapado al presentarlo en HTML.",
    "published_at": "Instante de publicación, si existe.",
    "actor_user_id": "Cuenta que originó el evento; puede quedar NULL al retirarse.",
    "action": "Tipo de acción auditada, sin contraseñas o medidas personales.",
    "entity_type": "Tipo lógico del objeto afectado.",
    "entity_id": "Identificador lógico como texto; no hay una FK polimórfica.",
    "metadata_redacted": "JSON técnico redactado; no es JSONB ni texto libre médico.",
}


def ssh_read(command: str, sql: str | None = None) -> str:
    executable = shutil.which("ssh")
    if not executable:
        raise RuntimeError("OpenSSH client is required for metadata collection")
    # Fixed administrator alias and fixed catalog-only commands; no external input.
    result = subprocess.run(  # nosec B603
        [executable, "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "nexostack-vps", command],
        input=sql,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
        timeout=60,
    )
    return result.stdout


def collect() -> dict:
    sql = (ROOT / "deploy/study/catalog.sql").read_text(encoding="utf-8")
    data = json.loads(
        ssh_read(
            "sudo -n docker exec -i vitalilab-db-lab psql -X -U vitalilab_owner "
            "-d vitalilab_staging -v ON_ERROR_STOP=1 -At -f -",
            sql,
        )
    )
    validate(data)
    ddl = ssh_read(
        "sudo -n docker exec vitalilab-db-lab pg_dump -U vitalilab_owner "
        "-d vitalilab_staging --schema=public --schema-only --no-owner --no-acl "
        "--lock-wait-timeout=5s"
    )
    forbidden = ("INSERT INTO", "COPY public.", "CREATE FUNCTION", "CREATE ROLE", "CREATE DATABASE")
    if any(value in ddl for value in forbidden):
        raise ValueError("Unexpected executable objects or data in schema-only export")
    ddl = "\n".join(
        line
        for line in ddl.splitlines()
        if not line.startswith(("\\restrict ", "\\unrestrict "))
        and line.strip() != "CREATE SCHEMA public;"
    )
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "estructura_postgresql.sql").write_text(
        "-- SOLO ESTRUCTURA: no contiene filas, roles ni contrasenas.\n"
        "-- Restaurar UNICAMENTE en una base de estudio VACIA; public ya debe existir.\n"
        + ddl
        + "\n",
        encoding="utf-8",
    )
    (DEST / "catalogo_postgresql.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return data


def validate(data: dict) -> None:
    names = {table["name"] for table in data["tables"]}
    if names != set(PURPOSES) or data["migration_revision"] != "c842d6e190ab":
        raise ValueError("Unexpected schema: stop and review the actual database")
    for table in data["tables"]:
        for column in table["columns"]:
            if column["name"] not in MEANINGS:
                raise ValueError(f"Missing explanation: {table['name']}.{column['name']}")


def dictionary(data: dict) -> str:
    lines = [
        "# Diccionario fisico completo de PostgreSQL",
        "",
        f"Extraido de catalogos PostgreSQL {data['postgres_version']}; "
        f"revision Alembic `{data['migration_revision']}`. No se exportaron filas.",
        "",
        "Los tipos y DEFAULT de este documento son los del motor, no tipos genericos del ORM. "
        "Sin DEFAULT SQL no significa sin valor en la aplicacion: Flask/SQLAlchemy aplica "
        "varios valores al insertar. SQL manual debe suministrarlos. Las fechas timestamp "
        "son sin zona horaria y el codigo usa la convencion UTC.",
        "",
    ]
    for table in data["tables"]:
        lines += [f"## {table['name']}", "", PURPOSES[table["name"]], ""]
        lines += [
            "| Campo | Tipo PostgreSQL | Nulo | Explicacion |",
            "|---|---|---|---|",
        ]
        for col in table["columns"]:
            marker = " [PK]" if col["primary_key"] else ""
            lines.append(
                f"| `{col['name']}`{marker} | {col['type']} | "
                f"{'Si' if col['nullable'] else 'No'} | {MEANINGS[col['name']]} |"
            )
        lines += ["", "### Defaults del motor", ""]
        defaults = [col for col in table["columns"] if col["default"] is not None]
        lines += [f"- `{col['name']}`: `{col['default']}`" for col in defaults] or [
            "No hay DEFAULT SQL en esta tabla."
        ]
        lines += ["", "### Claves, relaciones y restricciones", ""]
        lines += [f"- `{item['name']}`: `{item['definition']}`" for item in table["constraints"]]
        lines += ["", "### Indices fisicos", ""]
        lines += [f"- `{item['definition']}`" for item in table["indexes"]]
        lines += [""]
    return "\n".join(lines)


def relationships(data: dict):
    for table in data["tables"]:
        for key in table["constraints"]:
            if key["kind"] == "f":
                yield table, key


def mermaid(data: dict) -> str:
    lines = ["erDiagram"]
    for table in data["tables"]:
        lines.append(f"    {table['name']} {{")
        fk_columns = {
            name for key in table["constraints"] if key["kind"] == "f" for name in key["columns"]
        }
        for col in table["columns"]:
            typename = re.sub(r"[^A-Za-z0-9_]", "_", col["type"])
            marks = ("PK" if col["primary_key"] else "") + (
                ",FK" if col["primary_key"] and col["name"] in fk_columns else ""
            )
            if not marks and col["name"] in fk_columns:
                marks = "FK"
            lines.append(f"        {typename} {col['name']} {marks}".rstrip())
        lines.append("    }")
    for table, key in relationships(data):
        columns = set(key["columns"])
        optional = any(c["nullable"] for c in table["columns"] if c["name"] in columns)
        unique = any(
            k["kind"] in {"p", "u"} and set(k["columns"]) == columns for k in table["constraints"]
        )
        parent, child = ("o|" if optional else "||"), ("o|" if unique else "o{")
        lines.append(
            f"    {key['target_table']} {parent}--{child} {table['name']} : "
            + '"'
            + "+".join(key["columns"])
            + '"'
        )
    return "\n".join(lines) + "\n"


def graphviz(data: dict) -> str:
    lines = [
        "digraph vitalilab {",
        'graph [rankdir=LR, bgcolor="white", nodesep=0.35, ranksep=1.1, splines=polyline];',
        'node [shape=plain, fontname="Arial", fontsize=11];',
        'edge [fontname="Arial", fontsize=8, color="#64756e", arrowsize=0.65];',
    ]
    for table in data["tables"]:
        rows = [
            '<TR><TD COLSPAN="2" BGCOLOR="#123c35"><FONT COLOR="white">'
            f"<B>{table['name']}</B></FONT></TD></TR>"
        ]
        fk_columns = {c for k in table["constraints"] if k["kind"] == "f" for c in k["columns"]}
        for col in table["columns"]:
            marks = ("PK " if col["primary_key"] else "") + (
                "FK " if col["name"] in fk_columns else ""
            )
            label = html.escape(marks + col["name"] + (" ?" if col["nullable"] else ""))
            rows.append(
                f'<TR><TD PORT="{col["name"]}" ALIGN="LEFT">{label}</TD>'
                f'<TD ALIGN="LEFT">{html.escape(col["type"])}</TD></TR>'
            )
        lines.append(
            f'"{table["name"]}" [label=<<TABLE BORDER="0" CELLBORDER="1" '
            'CELLSPACING="0" CELLPADDING="5" COLOR="#afbbb5">' + "".join(rows) + "</TABLE>>];"
        )
    for table, key in relationships(data):
        label = "+".join(key["columns"])
        lines.append(
            f'"{table["name"]}":"{key["columns"][0]}" -> '
            f'"{key["target_table"]}":"{key["target_columns"][0]}" '
            f'[label="{label}"];'
        )
    return "\n".join(lines) + "\n}\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    args = parser.parse_args()
    catalog = (
        collect()
        if args.collect
        else json.loads((DEST / "catalogo_postgresql.json").read_text(encoding="utf-8"))
    )
    validate(catalog)
    for filename, content in (
        ("diccionario_postgresql.md", dictionary(catalog)),
        ("modelo_completo.mmd", mermaid(catalog)),
        ("modelo_completo.dot", graphviz(catalog)),
    ):
        (DEST / filename).write_text(content, encoding="utf-8")
    print(
        json.dumps(
            {
                "tables": len(catalog["tables"]),
                "columns": sum(len(t["columns"]) for t in catalog["tables"]),
                "foreign_keys": sum(1 for _ in relationships(catalog)),
            }
        )
    )
