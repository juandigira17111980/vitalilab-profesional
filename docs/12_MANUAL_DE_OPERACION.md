# Manual de operación

## 1. Arranque local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
flask --app wsgi:app db upgrade
flask --app wsgi:app seed-habits
flask --app wsgi:app run
```

Use una DB desechable y un `SECRET_KEY` local. No comparta `.env`.

## 2. Pruebas y diagnóstico

```powershell
ruff check app tests wsgi.py migrations/versions
ruff format --check app tests wsgi.py migrations/versions
pytest
flask --app wsgi:app db check
```

`/health` confirma proceso; `/ready` confirma DB. Un health verde con readiness rojo indica problema de conectividad/migración, no de servidor web.

## 3. Crear administrador

```powershell
flask --app wsgi:app create-admin
```

El comando solicita correo, nombre y contraseña sin escribirla en historial. No pase una clave real como argumento en un terminal compartido.

## 4. Cambio de esquema

1. Modificar modelos.
2. `flask --app wsgi:app db migrate -m "descripcion"`.
3. Leer el archivo generado; Alembic no comprende toda intención de negocio.
4. Probar `upgrade`, `downgrade` cuando sea seguro y `upgrade` de nuevo en DB desechable.
5. Ejecutar `db check` y pruebas.
6. Documentar compatibilidad y rollback.

Nunca edite una migración ya aplicada en un ambiente compartido.

## 5. Despliegue Staging

1. PR a `staging` y CI verde.
2. Crear Blueprint en Render desde `render.yaml`.
3. Confirmar proyecto/ambiente `VitaliLab / Staging`.
4. Completar solo en Render los valores `MAIL_*`.
5. Verificar deploy Live y `/ready`.
6. Ejecutar matriz STG-01…10.
7. Registrar evidencia en bitácora.

## 6. Backup y restauración

Para PostgreSQL gestionado, preferir backups del proveedor más exportación controlada antes de migraciones importantes. Una copia manual se guarda cifrada fuera del repositorio.

```text
pg_dump --format=custom --no-owner --file=vitalilab.dump DATABASE_URL
pg_restore --clean --if-exists --no-owner --dbname=RESTORE_URL vitalilab.dump
```

Verificar versión Alembic, conteos, FK, duplicados y un flujo ficticio. Eliminar de forma segura copias temporales según política.

## 7. Rollback

- Código: seleccionar el deploy sano anterior o desplegar su commit/tag.
- Esquema: no ejecutar downgrade destructivo automático. Evaluar compatibilidad; restaurar solo con autorización.
- Después: `/health`, `/ready`, login, dashboard, hábito y logs.

Criterios de reversión: health/readiness sostenidos en rojo, errores 5xx, login roto, integridad incorrecta o migración fallida.

## 8. Rotación de secretos

1. Crear valor nuevo en el ambiente correcto.
2. Identificar impacto: cambiar `SECRET_KEY` cierra sesiones; SMTP cambia entrega.
3. Actualizar Render sin copiar valores a chat/PR.
4. Desplegar y probar.
5. Revocar valor anterior.
6. Registrar fecha, propietario y resultado, nunca el secreto.

## 9. Incidentes

- Registrar hora, ambiente, commit, síntoma y alcance.
- No pegar tokens, cadenas DB, cookies ni datos de salud.
- Contener y revertir si el impacto continúa.
- Preservar logs; corregir, verificar y documentar causa raíz.

## 10. Mantenimiento mensual

- Revisar dependencias y alertas.
- Verificar expiración/costo de DB Staging.
- Probar recuperación y un backup restaurado.
- Revisar 5xx, latencia, reinicios y rate limits.
- Desactivar cuentas administrativas no usadas.
- Mantener documentos y diagrama alineados.

