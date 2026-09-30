# Bitácora verificable de cambios

## 1. Evidencia de la reconstrucción

| Fecha | Área | Cambio | Evidencia | Estado |
|---|---|---|---|---|
| 2026-09-30 | Git | Repositorio privado y ramas `main`/`staging` | Historial remoto | ✅ |
| 2026-09-30 | Documentación | Auditoría inicial integrada | PR #1, commit `182f96d` | ✅ |
| 2026-09-30 | Arquitectura | Fábrica Flask y módulos por dominio | `app/` | ✅ |
| 2026-09-30 | DBA | 7 tablas, constraints e índices | migraciones `0380d5595f5e`, `208469fd48ef` | ✅ local |
| 2026-09-30 | Backend | Auth, perfil, hábitos, progreso, admin y errores | rutas/servicios | ✅ local |
| 2026-09-30 | Seguridad | scrypt, CSRF, RBAC, rate limits, cookies y headers | pruebas/código | ✅ local |
| 2026-09-30 | Frontend | Sistema visual, responsive y componentes | CSS/Jinja/JS + capturas | ✅ local |
| 2026-09-30 | QA | 24 pruebas, cobertura 90,41 %, Ruff limpio | salida reproducible | ✅ |
| 2026-09-30 | E2E | Registro, hábito, admin, comunicado y móvil | Playwright/Chromium | ✅ local |
| 2026-09-30 | Infra | Docker, Compose, Render Blueprint y CI | archivos versionados | ✅ configurado |
| 2026-09-30 | CI | Calidad, PostgreSQL 18 y build Docker | GitHub Actions PR #2 | ✅ |

## 2. Defectos encontrados durante validación

| ID | Hallazgo | Corrección | Regresión |
|---|---|---|---|
| DEF-001 | Espacios/caso del correo fallaban antes de normalizar | Filtro previo de formulario | Registro con correo espaciado |
| DEF-002 | `timedelta` CSRF incompatible con librería actual | TTL de 7200 segundos | POST real con CSRF activo |
| DEF-003 | Perfil aceptaba peso sin altura por corto circuito de `Optional` | Validación cruzada en ambos campos | Caso inválido |
| DEF-004 | CLI admin permitía correo reservado/clave débil | email-validator + política común | Tres casos CLI |
| DEF-005 | Alerta móvil ocultaba contenido/menú | Alerta en flujo y z-index del menú | Captura 390 px |

## 3. Evidencia remota pendiente

| Hito | Requerido |
|---|---|
| PR funcional | URL, commit y revisión |
| CI final tras actualización menor | tres jobs verdes |
| Render Staging | URL y deploy/commit |
| SMTP Staging | correo ficticio recibido |
| Backup/restauración | fecha, duración, conteos y responsable |
| Production | aprobación explícita; no ejecutada |

## 4. Historial de releases

| Versión | Rama | Staging | Production |
|---|---|---|---|
| `v0.1.0` candidata | `feat/reconstruccion-profesional` | Pendiente | No promovida |
