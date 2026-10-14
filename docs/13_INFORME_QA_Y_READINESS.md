# Informe técnico preproducción — VitaliLab

Fecha: **30 de septiembre de 2026**  
Versión: candidata `v0.1.0`, rama `staging`, integración `2120e31`
Decisión preliminar: **GO para PR/CI y Staging; NO-GO para Production**  
Preparación actual: **90/100 — Apto con observaciones**

Esta cifra corresponde a la rúbrica interna del corte original; no es una nota académica ni una certificación de seguridad. La edición formativa del 13 de octubre agrega 26 pruebas y 90,43 % local, preparación Vercel y guías para estudiantes. Una nueva publicación debe cerrar acceso, PostgreSQL del proveedor, controles compartidos, recorrido remoto y recuperación antes de valorar su preparación operativa.

Escala: 0–40 No apto · 41–60 Riesgo alto · 61–75 Requiere correcciones · 76–90 Apto con observaciones · 91–100 Apto para producción.

Se usa calibración de sistema educativo con datos personales y medidas de salud: alto rigor, aunque el producto no es clínico.

## 1. Resumen ejecutivo

La reconstrucción elimina los bloqueantes técnicos observados en el prototipo: credenciales inseguras, esquema no migrable, duplicación de progreso, acoplamiento, falta de pruebas y frontend inconsistente. No hay hallazgos críticos abiertos en el código local revisado.

La salida a Production no se recomienda todavía porque faltan evidencias remotas y organizacionales: Render Staging, SMTP, backup operativo del proveedor, accesibilidad y política institucional. Todos tienen plan, pero un plan no equivale a una prueba.

## 2. Estado por área

| Área | Estado | Observación |
|---|---|---|
| Documentación | ✅ | Arquitectura, DBA, backend, UX, seguridad, infra, QA y operación |
| Arquitectura | ✅ | Monolito modular coherente con alcance |
| Base de datos | ✅/🟡 | Modelo, migraciones y restore aislado aprobados; resta política operativa del proveedor |
| Backend | ✅ | Flujos, errores y reglas cubiertos |
| Frontend | 🟡 | Responsive aprobado; resta auditoría WCAG especializada |
| Seguridad | 🟡 | Controles técnicos; resta privacidad institucional y escaneo externo |
| Infraestructura | 🟡 | CI y Docker aprobados; Render Staging no ejecutado aún |

## 3. Cálculo reproducible

Score inicial: 100.

| ID | Hallazgo abierto | Severidad | Plan formal | Deducción |
|---|---|---|---:|---:|
| OPS-01 | Staging sin evidencia final | Alto | Sí | -3 |
| PRIV-01 | Política institucional/menores no aprobada | Alto | Sí | -3 |
| AUTH-01 | SMTP real no configurado | Medio | Sí | -2 |
| A11Y-01 | WCAG/lector de pantalla no auditados formalmente | Medio | Sí | -2 |
| Total | | | | **-10** |

Resultado: **100 - 10 = 90/100**. No hay áreas sin información y no se aplican deducciones ocultas.

## 4. Evidencia aprobada

- 24 pruebas aprobadas y 90,41 % de cobertura.
- Análisis/formato limpio.
- Dos migraciones y ausencia de deriva.
- Registro real con CSRF, sesiones, rol admin e idempotencia.
- Navegador 390 px y 1280 px sin error de consola.
- Configuración no root, health/readiness, DB privada y CI.
- `pip-audit` sin vulnerabilidades conocidas en dependencias de producción.
- GitHub Actions en verde: calidad, PostgreSQL 18 y construcción Docker.
- Backup/restore aislado en PostgreSQL 18 con verificación de datos, Alembic y deriva.
- Bandit sin hallazgos medios/altos.
- Production no modificada.

## 5. Hallazgos abiertos y responsables

| ID | Responsable | Acción de cierre | Bloquea |
|---|---|---|---|
| OPS-01 | DevOps/propietario | PR, 3 jobs verdes, Blueprint y smoke test | Production |
| DBA-OPS | DBA/propietario | Definir backup cifrado, retención y restore del proveedor | Production |
| PRIV-01 | Institución | Aprobar finalidad, menores, retención y canal | Production |
| AUTH-01 | Propietario | Cargar SMTP y probar correo ficticio | Recuperación compartida |
| A11Y-01 | UX/QA | axe/lector/zoom y registro de resultado | Afirmación WCAG |

## 6. Recomendación por perfil

- Arquitectura: conservar el monolito modular; no introducir microservicios.
- DBA: ejecutar job PostgreSQL, backup y restore antes de datos reales.
- Backend: mantener puntos derivados y pruebas al cambiar reglas.
- Frontend: validar lector de pantalla y métricas en Staging.
- Seguridad: aprobar privacidad y agregar escaneo de cadena de suministro.
- DevOps: crear Staging desde Blueprint, observar logs y documentar rollback.

## 7. Criterio para 100/100

El score solo puede llegar a 100 cuando cada hallazgo se cierre con evidencia: Staging funcional, SMTP real, política operativa de backup, privacidad institucional y accesibilidad formal. Subir el número sin esas pruebas sería una afirmación falsa.

## Alcance de esta auditoría

Esta es una auditoría documental y técnica basada en lo entregado y ejecutado para revisión: código, configuración, migraciones, pruebas, navegador local, capturas y documentación. No sustituye:

- inspección directa de infraestructura o datos de Production no compartidos;
- un penetration test formal;
- revisión jurídica de tratamiento de datos personales/salud/menores;
- revisión humana línea por línea en áreas de máxima sensibilidad;
- pruebas de carga o accesibilidad con usuarios reales.

Cobertura declarada: arquitectura, esquema, migraciones, backend, UI, autenticación, autorización, controles HTTP, pruebas, SAST, restore aislado e infraestructura como código se revisaron a fondo; Render Staging, PostgreSQL del proveedor, SMTP, backup operativo, Production, pentest, rendimiento y validación jurídica no se han verificado en vivo.
