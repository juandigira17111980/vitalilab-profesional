"""Emit a code-derived reference; reads metadata only, never connects to a user database."""

import argparse
import inspect
import json
from pathlib import Path

from app import create_app
from app.extensions import db


def reference():
    app = create_app({"TESTING": True, "APP_ENV": "development", "RATELIMIT_ENABLED": False})
    root = Path(__file__).resolve().parents[1]
    with app.app_context():
        tables = []
        for table in sorted(db.metadata.tables.values(), key=lambda item: item.name):
            tables.append(
                {
                    "name": table.name,
                    "columns": [
                        {
                            "name": column.name,
                            "type": str(column.type),
                            "nullable": column.nullable,
                            "primary_key": column.primary_key,
                            "references": [key.target_fullname for key in column.foreign_keys],
                        }
                        for column in table.columns
                    ],
                    "constraints": sorted(
                        str(item.sqltext) for item in table.constraints if hasattr(item, "sqltext")
                    ),
                    "unique": sorted(
                        ", ".join(column.name for column in item.columns)
                        for item in table.constraints
                        if item.__class__.__name__ == "UniqueConstraint"
                    ),
                    "indexes": sorted(
                        item.name + " (" + ", ".join(column.name for column in item.columns) + ")"
                        for item in table.indexes
                    ),
                }
            )
        routes = []
        for route in sorted(app.url_map.iter_rules(), key=lambda item: str(item)):
            if route.endpoint == "static":
                continue
            function = inspect.unwrap(app.view_functions[route.endpoint])
            source = Path(inspect.getsourcefile(function)).resolve().relative_to(root).as_posix()
            routes.append(
                {
                    "path": str(route),
                    "methods": sorted(route.methods - {"HEAD", "OPTIONS"}),
                    "endpoint": route.endpoint,
                    "source": source,
                }
            )
        return {"tables": tables, "routes": routes}


def markdown(data):
    lines = [
        "# Referencia técnica derivada del código",
        "",
        "Este anexo se genera desde los modelos y las rutas de la aplicación. "
        "No consulta la base publicada ni exporta datos personales.",
        "",
        "Tipos, nulabilidad y relaciones corresponden a los modelos versionados; "
        "la coincidencia con el esquema se verifica mediante migraciones y db check.",
        "",
        "## Cómo leer el diccionario",
        "",
        "PK identifica una fila; FK exige una fila relacionada; "
        "NULL indica si un valor puede faltar. "
        "Una restricción única impide repetir una combinación. Los campos created_at y updated_at "
        "conservan creación y última modificación en UTC.",
        "",
        "Los nombres que terminan en _id son referencias, _on son fechas de negocio "
        "y _at son instantes. active controla disponibilidad; "
        "status representa un estado del proceso. "
        "Consulta el manual integral para las reglas de permisos y el significado de cada entidad.",
        "",
    ]
    for table in data["tables"]:
        lines += [
            f"## Tabla {table['name']}",
            "",
            "| Campo | Tipo | Permite NULL | Clave y relación |",
            "|---|---|---|---|",
        ]
        for column in table["columns"]:
            key = "PK" if column["primary_key"] else ""
            if column["references"]:
                key += ("; " if key else "") + "FK → " + ", ".join(column["references"])
            lines.append(
                f"| `{column['name']}` | {column['type']} | "
                f"{'Sí' if column['nullable'] else 'No'} | {key or '—'} |"
            )
        lines.append("")
        for title, values in (
            ("Combinaciones únicas", table["unique"]),
            ("Restricciones de valores", table["constraints"]),
            ("Índices declarados", table["indexes"]),
        ):
            lines += [f"{title}:"]
            lines += (
                [f"- `{value}`" for value in values]
                if values
                else ["No adicionales a las claves indicadas."]
            )
            lines.append("")
    lines += [
        "## Mapa de rutas",
        "",
        "Este mapa muestra direcciones y funciones reales. No representa una API pública "
        "contractual ni concede acceso: los decoradores y servicios comprueban sesión, rol, "
        "propietario y colegio según el caso. Toda acción POST requiere CSRF.",
        "",
        "| Ruta | Método | Función | Archivo |",
        "|---|---|---|---|",
    ]
    for route in data["routes"]:
        path = route["path"]
        lines.append(
            f"| `{path}` | {', '.join(route['methods'])} | "
            f"`{route['endpoint']}` | `{route['source']}` |"
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()
    data = reference()
    print(json.dumps(data, ensure_ascii=False) if args.format == "json" else markdown(data))
