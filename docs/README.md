# Centro de documentación técnica de VitaliLab

Fuente de verdad técnica y académica del proyecto. Los documentos separan cuatro estados: implementado localmente, verificado por pruebas, validado en Staging y promovido a Production.

Fecha de actualización documental: **14 de octubre de 2026**. Las pruebas y auditorías históricas conservan su fecha de ejecución.

## Empieza aquí si eres estudiante

Lee [VitaliLab explicado desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md) antes de los documentos por especialidad. Está escrito para primeros fundamentos de programación: cada concepto se relaciona con un archivo, una práctica y una explicación de sustentación.

La [guía de publicación de la copia](16_PUBLICACION_DE_LA_COPIA_DE_PRACTICA.md) detalla NexoStack. La [guía del docente](17_GUIA_DEL_DOCENTE_Y_EVIDENCIAS.md) contiene sesiones y criterios de aprendizaje. La [operación y accesos](18_NEXOSTACK_OPERACION_Y_ACCESOS.md) reúne permisos, respaldos y evidencia del laboratorio. Render y Vercel se conservan como alternativas, no como publicaciones nuevas de esta edición.

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
15. [Matriz de trazabilidad](14_MATRIZ_TRAZABILIDAD.md)
16. [Manual de aprendizaje desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md)
17. [Publicación de la copia de práctica](16_PUBLICACION_DE_LA_COPIA_DE_PRACTICA.md)
18. [Guía del docente y evidencias](17_GUIA_DEL_DOCENTE_Y_EVIDENCIAS.md)
19. [NexoStack operación y accesos](18_NEXOSTACK_OPERACION_Y_ACCESOS.md)

## Resultado del montaje inicial (histórico)

- ✅ Repositorio privado, estrategia de ramas y PR documental.
- ✅ Monolito modular Flask reconstruido.
- ✅ Modelo relacional de siete tablas y dos migraciones.
- ✅ Controles de autenticación, autorización, CSRF, cabeceras y auditoría.
- ✅ Diseño responsive probado en navegador real a 390 px y 1280 px.
- ✅ 28 pruebas, 90,67 % local, análisis estático y dependencias limpios en CI de esta edición.
- ✅ PR #2 fusionado a `staging`; CI verde en la integración.
- ✅ CI de cierre: calidad, SAST, PostgreSQL 18, backup/restore y construcción Docker.
- ✅ CLI Render autorizado y PostgreSQL de práctica disponible, confirmado el 13 de octubre.
- ✅ Copia NexoStack con PostgreSQL propia, HTTPS y dos accesos individuales de gestión.
- ✅ Backup y restore aislado comprobados; timers específicos del proyecto activos.
- ⚪ Web Render Staging no creada y Vercel preparado como alternativa no utilizada.
- 🔴 Production permanece congelada hasta aprobación, backup y validación final.

## Evolución premium

20. [Diseño de producto y auditoría UX](19_EVOLUCION_DE_PRODUCTO_Y_AUDITORIA_UX.md)
21. [Guía de funciones y QA premium](20_GUIA_DE_FUNCIONES_Y_QA_PREMIUM.md)

Este corte amplía la base original de siete entidades con metas y bitácora: nueve tablas de negocio, tres revisiones, ocho hábitos, seis rutinas y 42 pruebas locales con 91,75 % de cobertura. Los resultados de siete entidades y 28 pruebas anteriores se conservan como evidencia histórica. La guía nueva explica la extensión; la publicación requiere CI y comprobación remota del commit.

## Enfoques de perfil: personal e institucional

22. [Cómo funcionan los dos enfoques de perfil](21_ENFOQUES_PERSONAL_E_INSTITUCIONAL.md)

La cuarta revisión, `7ca6e014b982`, añade dos columnas al perfil sin crear tablas nuevas: siguen siendo nueve entidades. Esta selección personaliza el formulario; no implementa membresías, organizaciones multiusuario ni permisos institucionales.

## Regla de evidencia

Un cambio no se presenta como desplegado si solo existe localmente. Cada promoción debe registrar rama, commit, CI, URL de Staging, smoke tests, responsable y resultado. Nunca se adjuntan secretos ni datos personales.
