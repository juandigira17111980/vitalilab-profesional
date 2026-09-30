# Centro de documentación técnica de VitaliLab

Este directorio es la fuente oficial de documentación del proyecto académico **VitaliLab**. Su propósito es permitir que el equipo estudie, construya, pruebe y sustente el sistema con evidencia técnica, sin confundir lo que ya existe con lo que todavía está propuesto.

## Estado de la documentación

Fecha de corte: **30 de septiembre de 2026**.

| Marca | Significado |
|---|---|
| ✅ Implementado y verificado | Existe evidencia revisada en código, Git o Render. |
| 🟡 Propuesto | Diseño aprobado como orientación, pendiente de implementación. |
| 🔴 Hallazgo crítico | Riesgo que debe resolverse antes de promover a producción. |
| ⚪ Pendiente de evidencia | No se puede confirmar hasta contar con código, logs o datos del entorno. |

> Regla académica: durante la sustentación solo se debe presentar como “implementado” aquello que figure con evidencia en la bitácora y en una prueba reproducible.

## Ruta de lectura recomendada

1. [Documento Maestro Técnico](01_DOCUMENTO_MAESTRO_TECNICO.md): visión integral y fuente de verdad.
2. [Auditoría profunda y plan de mejora](AUDITORIA_PROFUNDA_Y_PLAN_DE_MEJORA.md): diagnóstico inicial y prioridades.
3. [Arquitectura y estructura](02_ARQUITECTURA_Y_ESTRUCTURA.md): organización actual y arquitectura objetivo.
4. [Modelo de datos y DBA](03_MODELO_DE_DATOS_DBA.md): entidades, relaciones, restricciones, migraciones y operación.
5. [Backend](04_BACKEND.md): módulos, rutas, reglas de negocio, errores y pruebas.
6. [Frontend y experiencia de usuario](05_FRONTEND_UX.md): pantallas, componentes, responsive y accesibilidad.
7. [Seguridad y privacidad](06_SEGURIDAD_Y_PRIVACIDAD.md): controles técnicos y tratamiento de datos.
8. [Git y trazabilidad](07_GIT_Y_TRAZABILIDAD.md): ramas, commits, revisiones y entregas.
9. [Infraestructura y despliegue](08_INFRAESTRUCTURA_Y_DEPLOY_RENDER.md): Local, Staging y Production.
10. [QA y pruebas](09_QA_Y_PRUEBAS.md): estrategia, casos y criterios de salida.
11. [Guía de sustentación](10_GUIA_DE_SUSTENTACION.md): relato, demostración y preguntas esperables.
12. [Bitácora de cambios](11_BITACORA_DE_CAMBIOS.md): qué se cambió realmente, cuándo y con qué evidencia.

## Alcance actual

### Confirmado

- ✅ Se creó el repositorio privado `juandigira17111980/vitalilab-profesional`.
- ✅ Se establecieron las ramas `main`, `staging` y `docs/auditoria-profunda`.
- ✅ Se organizó el proyecto `VitaliLab` en Render con ambientes `Production` y `Staging`.
- ✅ `Production` conserva el servicio actual; `Staging` está creado y vacío.
- ✅ Se realizó una auditoría estática inicial de código, base de datos versionada, UX, seguridad e infraestructura observable.

### Aún no implementado

- 🟡 Rediseño y migración de la base de datos.
- 🟡 Refactorización modular del backend.
- 🟡 Renovación visual y responsive del frontend.
- 🟡 Endurecimiento completo de seguridad.
- 🟡 Pipeline de pruebas y despliegue automatizado.
- 🟡 Servicio funcional de Staging y pruebas de aceptación.

## Cómo mantener esta documentación

Todo cambio técnico debe actualizar, como mínimo:

1. El documento especializado afectado.
2. La matriz de trazabilidad del Documento Maestro Técnico.
3. La bitácora, con fecha, rama, commit, prueba y resultado.
4. La guía de sustentación si cambia el flujo demostrable.

La documentación se modifica mediante rama y pull request; no se edita directamente en `main` ni se declara un cambio terminado sin evidencia.
