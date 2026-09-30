# Matriz de trazabilidad de la reconstrucción

Esta matriz permite sustentar qué problema se resolvió, dónde se implementó, cómo se probó y en qué documento se explica. La evidencia remota corresponde a los PR #2 y #3 del repositorio privado.

| Requisito | Implementación | Evidencia de prueba | Documento | Estado |
|---|---|---|---|---|
| Arquitectura mantenible | Fábrica Flask y blueprints por dominio | Importación, rutas y 24 pruebas | `02_ARQUITECTURA_Y_ESTRUCTURA.md` | ✅ |
| Identidad segura | scrypt, CSRF, bloqueo, rate limit y reset firmado | `tests/test_auth.py` | `04_BACKEND.md`, `06_SEGURIDAD_Y_PRIVACIDAD.md` | ✅ |
| Privacidad mínima | aceptación versionada y medidas opcionales | Registro y perfil | `06_SEGURIDAD_Y_PRIVACIDAD.md` | ✅ técnica / 🟡 institucional |
| Autorización | sesión y rol admin en servidor | 403 usuario, flujos admin | `04_BACKEND.md` | ✅ |
| Integridad de hábitos | restricción única diaria e idempotencia | progreso y doble envío | `03_MODELO_DE_DATOS_DBA.md` | ✅ |
| Progreso consistente | puntos, nivel y racha derivados de eventos | `tests/test_progress.py` | `04_BACKEND.md` | ✅ |
| Base migrable | dos revisiones Alembic, constraints e índices | upgrade y `db check` PostgreSQL 18 | `03_MODELO_DE_DATOS_DBA.md` | ✅ |
| Recuperación de datos | `pg_dump` y `pg_restore` en base aislada | PR #3, job `postgres-migration` | `03_MODELO_DE_DATOS_DBA.md` | ✅ técnica / 🟡 proveedor |
| Interfaz profesional | sistema visual responsive y navegación móvil | Chromium 1280 px y 390 px | `05_FRONTEND_UX.md` | ✅ / 🟡 WCAG formal |
| Seguridad HTTP | CSP, HSTS, no-store y cabeceras defensivas | `tests/test_routes.py` | `06_SEGURIDAD_Y_PRIVACIDAD.md` | ✅ |
| Calidad automatizada | Ruff, Pytest, cobertura, Bandit y `pip-audit` | CI verde PR #2/#3 | `09_QA_Y_PRUEBAS.md` | ✅ |
| Entrega reproducible | Docker no root, Compose y Blueprint | build Docker y esquema Blueprint válido | `08_INFRAESTRUCTURA_Y_DEPLOY_RENDER.md` | ✅ configuración |
| Trazabilidad | ramas, commits, PR, bitácora y rollback | historial Git/GitHub | `07_GIT_Y_TRAZABILIDAD.md`, `11_BITACORA_DE_CAMBIOS.md` | ✅ |
| Ambiente de prueba | servicio y PostgreSQL exclusivos de Staging | smoke tests STG-01–10 | `08_INFRAESTRUCTURA_Y_DEPLOY_RENDER.md` | 🟡 acceso Render |
| Producción controlada | promoción solo desde `staging` aprobada | checklist y autorización | `12_MANUAL_DE_OPERACION.md` | 🔴 congelada |

## Lectura del estado

- ✅ significa implementado y comprobado.
- 🟡 exige una evidencia externa o decisión del propietario.
- 🔴 indica una promoción expresamente no autorizada.

La matriz no convierte una configuración preparada en una ejecución realizada. La URL, el commit y los smoke tests de Render Staging deben agregarse a la bitácora cuando el propietario conecte el repositorio privado.
