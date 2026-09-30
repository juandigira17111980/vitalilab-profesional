# Estrategia y ejecución de QA

## 1. Resultado local

| Puerta | Resultado |
|---|---|
| Ruff check/format | ✅ sin hallazgos |
| Pytest | ✅ 24/24 |
| Cobertura | ✅ 90,41 %; umbral 85 % |
| Dependencias | ✅ `pip-audit`: sin vulnerabilidades conocidas |
| Migración base vacía | ✅ |
| Deriva Alembic | ✅ ninguna |
| Navegador escritorio/móvil | ✅ |
| Consola navegador | ✅ 0 errores/advertencias finales |
| Docker | ✅ imagen construida en GitHub Actions |
| PostgreSQL real | ✅ migraciones/seed/check en PostgreSQL 18 CI |
| Backup/restauración | ✅ `pg_dump`/`pg_restore` y comparación aislada en PostgreSQL 18 CI |
| SAST | ✅ Bandit sin hallazgos medios/altos |
| Staging | 🟡 pendiente |

## 2. Casos automatizados

| Grupo | Casos principales |
|---|---|
| Auth | alta, normalización, hash, duplicado, login/logout, bloqueo, token, reset, redirección segura, CSRF |
| Progreso | IMC, niveles, evento único, puntos, racha y ruta idempotente |
| Perfil | medida válida, validación cruzada, no duplicar medición idéntica |
| Roles/admin | 403, borrador, publicar y archivar |
| Operación | health/readiness, DB caída, seed, SMTP y CLI admin |
| Público | contenidos, privacidad implícita, 404 y cabeceras |

## 3. Recorrido visual real

Playwright controló Chromium y verificó:

1. Inicio y estructura semántica.
2. Registro con privacidad y CSRF activo.
3. Dashboard recién creado.
4. Vista móvil 390 × 844.
5. Menú, etiqueta accesible y cierre con Escape.
6. Cumplimiento de hábito y cambio a 1/4.
7. Logout, login admin y acceso por rol.
8. Creación/publicación de comunicado y visualización en inicio.

Durante esta prueba se encontraron y corrigieron dos defectos de integración: expiración CSRF incompatible y validación insuficiente del comando administrativo.

## 4. CI

El workflow corre en PR/push hacia ramas relevantes:

- `quality`: Python 3.13, dependencias, Ruff, Bandit, Pytest y `pip-audit`.
- `postgres-migration`: PostgreSQL 18, upgrade, seed, `db check`, backup, restore y verificación de datos/esquema.
- `container-build`: construcción del Dockerfile.

Render solo auto-despliega `staging` cuando los checks asociados pasan.

Ejecuciones GitHub de los PR #2 y #3: **tres jobs aprobados** en cada cierre.

## 5. Matriz pendiente de Staging

| ID | Prueba | Salida requerida |
|---|---|---|
| STG-01 | Build y arranque | Deploy Live |
| STG-02 | `/health` y `/ready` | 200/200 |
| STG-03 | Alta/login/logout | Flujo completo |
| STG-04 | Hábito doble | Un evento y mismos puntos |
| STG-05 | Perfil/IMC | Valor, contexto y persistencia |
| STG-06 | Rol admin | Usuario 403; admin permitido |
| STG-07 | SMTP | Correo y token funcionales |
| STG-08 | Headers/TLS | Secure, HSTS, CSP |
| STG-09 | Logs | Sin 5xx/secretos |
| STG-10 | Backup/restauración del proveedor | Conteos, relaciones, cifrado y retención |

## 6. Severidad

- Bloqueante: pérdida/exposición de datos, auth rota, app no inicia.
- Alta: flujo principal o integridad incorrectos.
- Media: impacto acotado con alternativa.
- Baja: detalle visual/documental.

No hay defectos bloqueantes abiertos en la ejecución local. La falta de evidencia remota es una condición de release, no un fallo oculto.

## 7. Gate de salida

Staging puede desplegarse cuando el PR esté en CI verde. Production solo con cero bloqueantes, Staging aprobado, SMTP si es requisito, restauración, privacidad, rollback y autorización.
