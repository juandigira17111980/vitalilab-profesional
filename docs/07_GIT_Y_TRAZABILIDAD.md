# Git, colaboración y trazabilidad

## 1. Objetivo

Usar Git como evidencia del proceso académico y como control de cambios profesional. Cada mejora debe poder rastrearse desde el problema hasta la implementación, la prueba y el despliegue.

## 2. Repositorios

| Repositorio | Uso | Permiso conocido |
|---|---|---|
| `ega1026/vitalilab` | Fuente original de referencia | Lectura para la cuenta de trabajo |
| `juandigira17111980/vitalilab-profesional` | Desarrollo privado y documentación profesional | Administración autorizada |

No se modifica el repositorio original sin permiso de su propietario. No se copian bases de datos con información personal ni archivos secretos.

## 3. Estrategia de ramas

```mermaid
gitGraph
    commit id: "main estable"
    branch staging
    branch feature_cambio
    checkout feature_cambio
    commit id: "implementación y pruebas"
    checkout staging
    merge feature/cambio id: "PR revisado"
    checkout main
    merge staging id: "release aprobada"
```

| Rama | Propósito | Regla |
|---|---|---|
| `main` | Estado candidato a Production | No recibe trabajo directo |
| `staging` | Integración y despliegue de prueba | Solo PR revisado |
| `feature/*` | Funcionalidad o mejora | Una intención coherente |
| `fix/*` | Corrección | Incluye reproducción y prueba |
| `docs/*` | Documentación | Actualiza fuente de verdad |
| `chore/*` | Infraestructura/mantenimiento | Explica impacto operativo |

En cuentas o planes sin reglas automáticas de protección, la protección se cumple por procedimiento y revisión explícita.

## 4. Flujo de trabajo

1. Registrar el hallazgo o requisito con criterio de aceptación.
2. Crear rama desde `staging` actualizada.
3. Implementar cambios pequeños y verificables.
4. Actualizar pruebas y documentación.
5. Abrir pull request hacia `staging`.
6. Revisar código, datos, seguridad, UX e infraestructura según impacto.
7. Desplegar en Staging y adjuntar evidencia.
8. Aprobar y fusionar.
9. Para una entrega, abrir PR `staging` → `main` con checklist de release.
10. Desplegar Production solo con aprobación y plan de rollback.

## 5. Convención de commits

Formato recomendado:

```text
tipo(alcance): descripción breve en imperativo
```

Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore` y `security`.

Ejemplos:

```text
security(auth): almacena contraseñas con hash seguro
feat(habits): evita doble cumplimiento por día
docs(dba): actualiza diagrama tras migración 003
test(auth): cubre bloqueo de edición de perfil ajeno
```

El mensaje no debe contener nombres de usuarios, correos, credenciales o datos médicos.

## 6. Contenido mínimo de un pull request

- Problema y objetivo.
- Alcance incluido y excluido.
- Decisiones importantes.
- Riesgos y compatibilidad de datos.
- Cómo probar localmente.
- Resultado de pruebas automáticas.
- Evidencia visual si cambia UI.
- Migración, backup y rollback si cambia datos.
- Variables nuevas solo por nombre.
- Documentación actualizada.

## 7. Matriz de evidencia por cambio

| Campo | Descripción |
|---|---|
| Requisito/hallazgo | Por qué se hace |
| Rama | Dónde se trabajó |
| Commit/PR | Qué modificación exacta contiene |
| Prueba | Cómo se verificó |
| Staging | Fecha/resultado sin credenciales |
| Aprobación | Quién autorizó promover |
| Release | Versión o commit en Production |
| Rollback | Versión anterior y procedimiento |

La [bitácora](11_BITACORA_DE_CAMBIOS.md) resume esta información para la sustentación.

## 8. Versionado de entregas

- `v0.x.y`: desarrollo académico antes de estabilidad.
- `v1.0.0`: primera versión que cumple alcance y checklist de producción.
- Parche: corrección compatible.
- Menor: funcionalidad compatible.
- Mayor: cambio incompatible o migración significativa.

No se etiqueta una release sin pruebas y documentación.

## 9. Archivos que no deben versionarse

- `.env` o archivos con credenciales.
- Bases SQLite con datos reales.
- Backups/exportaciones y logs.
- Tokens y certificados privados.
- Carpetas virtuales y cachés.
- Capturas que revelen datos o secretos.

## 10. Estado actual

- ✅ Repositorio privado creado.
- ✅ Ramas `main`, `staging` y `docs/auditoria-profunda` creadas.
- ✅ Auditoría y paquete documental en pull request hacia `staging`.
- 🟡 Reglas automáticas de rama, CI y releases todavía pendientes.
- 🟡 Aún no existen PR funcionales de datos, backend o frontend.
