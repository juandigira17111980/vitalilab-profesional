# Contribuir a VitaliLab

## Flujo

1. Cree una rama `feat/*`, `fix/*`, `docs/*` o `chore/*` desde `staging`.
2. Mantenga un alcance coherente y no incluya secretos, datos personales ni bases.
3. Ejecute Ruff, Pytest y `flask db check` cuando aplique.
4. Actualice pruebas, documentación y bitácora en el mismo cambio.
5. Abra PR hacia `staging`; Production se promueve desde `staging` a `main` con aprobación.

## Estándar de cambio

- Rutas: solo coordinación HTTP.
- Reglas reutilizables: servicios.
- Datos: ORM y migración versionada.
- Acciones mutantes: sesión/rol, CSRF y validación del servidor.
- UI: semántica, foco, responsive y estados de error.
- Migraciones aplicadas en ambientes compartidos no se reescriben.

## Puerta local

```text
ruff check app tests wsgi.py migrations/versions
ruff format --check app tests wsgi.py migrations/versions
pytest
flask --app wsgi:app db check
```

Use commits `tipo(alcance): descripción`. El PR debe explicar prueba, riesgo, migración, rollback y variables nuevas solo por nombre.
