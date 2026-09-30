# Centro de documentación técnica de VitaliLab

Fuente de verdad técnica y académica del proyecto. Los documentos separan cuatro estados: implementado localmente, verificado por pruebas, validado en Staging y promovido a Production.

Fecha de corte: **30 de septiembre de 2026**.

| Marca | Significado |
|---|---|
| ✅ | Implementado y comprobado con evidencia local o de repositorio |
| 🟡 | Preparado, pero requiere evidencia remota o decisión del propietario |
| 🔴 | Bloquea Production |
| ⚪ | Fuera del alcance verificado o pendiente de información externa |

## Lectura recomendada

1. [Documento Maestro Técnico](01_DOCUMENTO_MAESTRO_TECNICO.md)
2. [Auditoría profunda inicial](AUDITORIA_PROFUNDA_Y_PLAN_DE_MEJORA.md)
3. [Arquitectura y estructura](02_ARQUITECTURA_Y_ESTRUCTURA.md)
4. [Modelo de datos y DBA](03_MODELO_DE_DATOS_DBA.md)
5. [Backend](04_BACKEND.md)
6. [Frontend, UX y accesibilidad](05_FRONTEND_UX.md)
7. [Seguridad y privacidad](06_SEGURIDAD_Y_PRIVACIDAD.md)
8. [Git y trazabilidad](07_GIT_Y_TRAZABILIDAD.md)
9. [Infraestructura y Render](08_INFRAESTRUCTURA_Y_DEPLOY_RENDER.md)
10. [QA y pruebas](09_QA_Y_PRUEBAS.md)
11. [Guía de sustentación](10_GUIA_DE_SUSTENTACION.md)
12. [Bitácora verificable](11_BITACORA_DE_CAMBIOS.md)
13. [Manual de operación](12_MANUAL_DE_OPERACION.md)
14. [Informe QA y readiness](13_INFORME_QA_Y_READINESS.md)

## Resultado actual

- ✅ Repositorio privado, estrategia de ramas y PR documental.
- ✅ Monolito modular Flask reconstruido.
- ✅ Modelo relacional de siete tablas y dos migraciones.
- ✅ Controles de autenticación, autorización, CSRF, cabeceras y auditoría.
- ✅ Diseño responsive probado en navegador real a 390 px y 1280 px.
- ✅ 24 pruebas, 90,41 % de cobertura, análisis estático y dependencias limpios.
- ✅ CI verde: calidad, PostgreSQL 18 y construcción Docker.
- 🟡 PR funcional abierto y despliegue de Staging pendiente.
- 🔴 Production permanece congelada hasta aprobación, backup y validación final.

## Regla de evidencia

Un cambio no se presenta como desplegado si solo existe localmente. Cada promoción debe registrar rama, commit, CI, URL de Staging, smoke tests, responsable y resultado. Nunca se adjuntan secretos ni datos personales.
