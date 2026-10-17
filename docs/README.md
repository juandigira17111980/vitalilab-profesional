# Centro de documentación técnica de VitaliLab

Fuente de verdad técnica y académica del proyecto. Los documentos separan cuatro estados: implementado localmente, verificado por pruebas, validado en Staging y promovido a Production.

Fecha de actualización documental: **16 de octubre de 2026**. Las pruebas y auditorías históricas conservan su fecha de ejecución.

## Edición actual

La [guía del guardado de mediciones y autorizaciones](30_GUARDADO_DE_MEDICIONES_Y_AUTORIZACIONES.md) explica el bloqueo reportado, su corrección de interfaz, los pasos para revisión administrativa y la limitación del uso personal de menores. No elimina verificaciones ni convierte los ejemplos en autorizaciones reales.

Para estudiar específicamente PostgreSQL, consultar la [guía DBA y de sustentación](dba/README.md), el [diccionario físico de 148 campos](dba/diccionario_postgresql.md), el [modelo completo](dba/modelo_completo.svg) y su [evidencia de validación](dba/VALIDACION.md). El paquete incluye SQL de estructura, datos inventados y ejercicios; no comparte la base publicada. El acceso individual se activa tras recibir la llave pública del compañero.

Empieza por el [manual integral del sistema](26_MANUAL_INTEGRAL_DEL_SISTEMA.md): explicación progresiva de todo el proyecto, modelo de diecisiete entidades, backend, frontend, seguridad, Git, DNS, infraestructura y prácticas de sustentación. La [especificación de personalización y rutinas propias](25_PERSONALIZACION_Y_RUTINAS.md) relaciona los cambios con sus criterios de aceptación. Las guías anteriores siguen siendo útiles, pero describen los cortes históricos identificados en cada una.

El [diccionario completo y mapa de rutas](27_DICCIONARIO_Y_RUTAS_GENERADAS.md) se genera desde los modelos y direcciones reales; no consulta ni exporta datos del servidor.

El [informe de verificación y publicación](28_QA_Y_PUBLICACION_PERSONALIZACION.md) registra el corte de personalización, 150 pruebas, la restauración de las diecisiete entidades, la convivencia con los otros proyectos y las condiciones pendientes para operación institucional real. El cierre más reciente se consulta en el manual integral y en `/health`.

La [revisión visual móvil](29_REVISION_VISUAL_MOVIL.md) documenta el ajuste mínimo de menú, contraste y foco, con el código de negocio y la base sin cambios.

El manual integral incluye ahora ese ajuste explicado desde cero, un ejercicio guiado y el cierre publicado `815b6e2`. También explica la carpeta `app/data`, las columnas de la referencia OMS y un guion de sustentación, distinguiendo ese recurso de los datos personales en PostgreSQL. Su edición PDF reúne el texto y el diccionario de datos/rutas en un único documento compartible; las cifras de pruebas se distinguen de las limitaciones y pendientes reales.

La actualización del comprobante de Google queda publicada como `6ac329e`, con 154 pruebas locales, cobertura 94,90 %, CI aprobado y comprobación pública en el dominio principal y `www`. El manual distingue la publicación del archivo de la confirmación que debe realizar el propietario en Search Console; no da la indexación por completada.

## Empieza aquí si eres estudiante

Lee [VitaliLab explicado desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md) antes de los documentos por especialidad. Está escrito para primeros fundamentos de programación: cada concepto se relaciona con un archivo, una práctica y una explicación de sustentación.

La [guía de publicación de la copia](16_PUBLICACION_DE_LA_COPIA_DE_PRACTICA.md) detalla NexoStack. La [guía del docente](17_GUIA_DEL_DOCENTE_Y_EVIDENCIAS.md) contiene sesiones y criterios de aprendizaje. La [operación y accesos](18_NEXOSTACK_OPERACION_Y_ACCESOS.md) reúne permisos, respaldos y evidencia del laboratorio. Render se conserva como alternativa independiente y sitio histórico, no como una publicación nueva de esta edición. Se retiraron las configuraciones de alojamiento no utilizadas.

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
- ⚪ Web Render Staging no creada en ese corte histórico.
- 🔴 Production permanece congelada hasta aprobación, backup y validación final.

## Evolución premium

20. [Diseño de producto y auditoría UX](19_EVOLUCION_DE_PRODUCTO_Y_AUDITORIA_UX.md)
21. [Guía de funciones y QA premium](20_GUIA_DE_FUNCIONES_Y_QA_PREMIUM.md)

Este corte amplía la base original de siete entidades con metas y bitácora: nueve tablas de negocio, tres revisiones, ocho hábitos, seis rutinas y 42 pruebas locales con 91,75 % de cobertura. Los resultados de siete entidades y 28 pruebas anteriores se conservan como evidencia histórica. La guía nueva explica la extensión; la publicación requiere CI y comprobación remota del commit.

## Enfoques de perfil: personal e institucional

22. [Cómo funcionan los dos enfoques de perfil](21_ENFOQUES_PERSONAL_E_INSTITUCIONAL.md)

La cuarta revisión, `7ca6e014b982`, añadió dos columnas al perfil sin crear tablas nuevas. En ese corte la selección solo personalizaba el formulario; la extensión siguiente incorpora vinculaciones y permisos reales.

## Experiencia personal y escolar

23. [Diseño del módulo escolar y decisiones de seguridad](22_DISENO_MODULO_ESCOLAR.md)
24. [Guía escolar desde cero y validación](23_GUIA_ESCOLAR_Y_VALIDACION.md)

La quinta revisión, `a903b5d7e214`, amplía a catorce entidades y añade colegios, grupos, vinculaciones revisadas, asignaciones y rutinas registradas. Incluye seguimiento propio, referencia OMS documentada y próximo paso por objetivo funcional. Consulta la guía 23 para los recorridos de estudiante, docente y administrador, controles, pruebas y restricciones del piloto. No se habilita la recopilación de datos reales de menores por publicar esta versión.

## Regla de evidencia

25. [Conexión del dominio principal de Hostinger](24_DOMINIO_PRINCIPAL_HOSTINGER.md): cambio mínimo del CNAME, preparación sin emisión prematura, activación y reversión. Conectar la dirección pública no elimina Render ni importa sus cuentas.

Un cambio no se presenta como desplegado si solo existe localmente. Cada promoción debe registrar rama, commit, CI, URL de Staging, smoke tests, responsable y resultado. Nunca se adjuntan secretos ni datos personales.
