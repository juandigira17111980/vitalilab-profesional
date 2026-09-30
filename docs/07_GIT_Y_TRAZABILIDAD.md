# Git, colaboración y trazabilidad

## 1. Repositorios

| Repositorio | Uso |
|---|---|
| `ega1026/vitalilab` | Fuente histórica de solo lectura |
| `juandigira17111980/vitalilab-profesional` | Desarrollo privado autorizado |

El repositorio original no se modifica. Las bases, secretos, logs, capturas temporales y backups están ignorados.

## 2. Ramas

```text
main                        release aprobada / Production
staging                     integración / Render Staging
feat/reconstruccion-profesional
docs/*, fix/*, chore/*      trabajos específicos
```

La protección se aplica por PR, CI y aprobación aunque el plan no permita reglas avanzadas.

## 3. Flujo

1. Rama desde `staging` actualizado.
2. Implementación, pruebas y documentación.
3. PR hacia `staging`.
4. Tres jobs CI: calidad, migración PostgreSQL y contenedor.
5. Despliegue y smoke test en Staging.
6. Aprobación funcional/visual.
7. PR `staging` → `main` para una release.
8. Backup, ventana, despliegue y observación de Production.

## 4. Convenciones

```text
feat(scope): capacidad
fix(scope): corrección
security(scope): control
test(scope): cobertura
docs(scope): conocimiento
chore(scope): infraestructura
```

Los commits no incluyen correos, usuarios, datos médicos ni secretos.

## 5. Pull requests

Contenido obligatorio: problema, alcance, decisión, riesgos, migraciones, variables por nombre, pruebas, evidencia visual, rollback y documentación. Un cambio de datos no se aprueba sin `db check` y estrategia de recuperación.

## 6. Evidencia registrada

| Hito | Evidencia |
|---|---|
| Auditoría documental | PR #1 fusionado a `staging`, commit `182f96d` |
| Reconstrucción | Rama `feat/reconstruccion-profesional` |
| Calidad local | 24 pruebas, 90,41 %, Ruff limpio |
| Migraciones | `0380d5595f5e` y `208469fd48ef` |
| PR funcional | 🟡 se completa al cerrar esta entrega |
| Release Production | 🔴 no autorizada |

## 7. Versionado

La reconstrucción es candidata `v0.1.0`. `v1.0.0` solo se crea con Staging, restauración, seguridad, aceptación y Production aprobados.
