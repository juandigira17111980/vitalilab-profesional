# Changelog

## Limpieza del montaje y explicación de referencias — 2026-10-15

- Retirada la configuración de un proveedor no utilizado, su script de copia de estáticos y la detección específica en la fábrica Flask.
- Conservados `wsgi:app`, Docker, el montaje NexoStack y la alternativa Render; sin cambios de modelo, migraciones, mediciones, permisos ni rutinas.
- Sustituidas las dos pruebas del adaptador por verificaciones de arranque Flask y entrega de CSS.
- Manuales actualizados con la diferencia entre NexoStack actual y Render histórico, sin instrucciones de alojamiento ajenas al montaje.
- Explicación de `app/data`, columnas OMS, ejemplo de lectura y guion de sustentación; CSV original y cálculo sin modificar.

Validación local de este corte: 150 pruebas aprobadas, cobertura 94,89 %, Ruff y análisis estático sin errores. Los cinco avisos de deprecación de dependencias existentes no se corrigen en esta limpieza. No requiere migración ni modificación de los servicios activos.

## Ajuste visual móvil — 2026-10-15

- Menú móvil con altura acotada y desplazamiento interno en pantallas bajas y horizontales.
- Bordes de campos y botones de contorno más distinguibles; foco de teclado uniforme y espacio de desplazamiento sobre la barra móvil.
- Sin cambios de backend, plantillas, datos, permisos, puntos, rutinas o dependencias. Evidencia en la [revisión visual](docs/29_REVISION_VISUAL_MOVIL.md).

## Personalización y rutinas propias — 2026-10-15

- Recorrido de medición, resultado, objetivo y biblioteca personalizada, completado una sola vez.
- Confirmación para guardar mediciones y verificación previa de vinculaciones escolares; sin prescripción por IMC.
- Colegio y grupo escritos manualmente, con revisión independiente de los permisos institucionales.
- Rutinas privadas con ejercicios ordenados, edición con control de revisión, archivo e idempotencia diaria de XP.
- Quince rutinas guiadas y demostraciones vectoriales propias, con diseño responsive y alternativas de texto.
- Retirada de avisos académicos de la interfaz, conservando privacidad, autorizaciones y contexto de salud.
- Migración aditiva a diecisiete entidades; CI con conservación de datos previos y pruebas de concurrencia PostgreSQL.
- Manual integral del sistema para estudio, operación y sustentación.

Publicado en NexoStack como `81b5650`, con CI verde, 150 pruebas y restauración aislada de las diecisiete entidades. Consulta [evidencia, alcance y pendientes operativos](docs/28_QA_Y_PUBLICACION_PERSONALIZACION.md). El servicio original de Render no se modificó.

Los cambios relevantes de VitaliLab se documentan siguiendo una adaptación de Keep a Changelog.

## [Unreleased]

### Conexión del dominio principal

- Rutas específicas para vitalilab.space y www conservando la dirección de laboratorio y su certificado independiente.
- Emisión HTTPS condicionada a DNS correcto de ambos nombres, sin cambios automáticos en Hostinger.
- Aplicación de configuración solo a la web, con respaldo y rechazo de cambios de código/esquema en esa operación.
- Guía 24: editar únicamente el CNAME www; conservar ALIAS, correo, nameservers y Render; validación y reversión.

### Bienestar personal y escolar (2026-10-14)

- Registro personal/institucional con segundo paso de colegio, grupo y rol solicitado; selección sin privilegios automáticos.
- Catálogo, grupos por año, vinculaciones pendientes, revisión administrativa y asignaciones docentes del mismo colegio.
- Panel docente limitado a grupos propios, agregados mensuales con mínimo diez participantes por indicador, redondeo y aporte voluntario revocable.
- Nueve rutinas, proyección limpia para clase y «Tu próximo paso» según objetivo funcional, no por IMC.
- Seguimiento anual propio con gráfica y tabla; referencia OMS 2007 LMS por edad al medir y sexo de referencia opcional, sin etiquetas ni extrapolación extrema.
- Registro transaccional de rutinas y hábito diario sin duplicar XP; restricciones y concurrencia verificadas en CI PostgreSQL.
- Migración aditiva `a903b5d7e214`: catorce entidades; no convierte textos libres anteriores en permisos.
- Permisos DML y backup/restore CI ampliados a las catorce entidades; Render y otros proyectos fuera del despliegue.
- Guías 22 y 23 con modelo, código, prácticas, amenazas, operación y límites: laboratorio con datos ficticios, no autorización clínica ni institucional.

### Enfoque personal o institucional (2026-10-14)

- Selector de enfoque en Mi perfil; institución y grado/grupo/área opcionales visibles solo en modo institucional con JavaScript.
- Elección persistida y validada en servidor y base de datos, independiente de roles y permisos.
- Migración aditiva `7ca6e014b982`: conserva grupos existentes y propone enfoque institucional cuando ya había un grupo no vacío.
- Cambiar a personal conserva el contexto anterior; desde institucional se puede editar o vaciar explícitamente.
- Pruebas de persistencia, autorización, CSRF, límites y migración con datos; guía de aprendizaje 21.

### Limpieza del pie de página (2026-10-14)

- Retirados el eslogan, el bloque «Explora» con sus enlaces y la línea de copyright/aviso educativo, según solicitud visual.
- Conservado el logo en un pie compacto, sin modificar navegación principal, rutas, consentimiento ni controles de seguridad.
- Pruebas de regresión en inicio y panel; verificación de rutas de contenido y privacidad.

### Evolución premium del laboratorio

- Nuevo inicio de producto, logo SVG, textos funcionales y navegación móvil con área segura.
- Corrección del anillo mediante Grid, tipografía más legible y tarjetas compactas.
- Ocho hábitos; seis rutinas con búsqueda y temporizador pausable, reanudable y reiniciable.
- Metas personales por hábito y bitácora diaria con rangos, unicidad y acceso propio.
- Mapa de actividad de 28 días y registro rápido desde Hoy.
- Migración aditiva 54e1c8bb7901 y permisos limitados para las dos tablas nuevas.
- Fechas de usuario coherentes entre hábitos, metas, bitácora y nuevas mediciones; tzdata explícita.
- 42 pruebas y 91,75 % local; CI ejercita las nueve entidades y su backup/restore.
- Documentación 19 y 20 con decisiones de UX, recorridos de datos y límites de SaaS comercial.

### Added

- Fábrica Flask y módulos de autenticación, perfil, hábitos, contenido y administración.
- Modelo SQLAlchemy normalizado y migraciones Alembic.
- Recuperación de acceso por SMTP configurable.
- Panel personal, panel administrativo, contenidos y sistema visual responsive.
- Health/readiness endpoints, contenedor no privilegiado, Compose y Render Blueprint.
- CI de calidad, PostgreSQL y construcción de contenedor.
- Suite automatizada y documentación académica/operativa.

### Security

- Contraseñas con hash scrypt.
- Protección CSRF, cookies endurecidas, CSP, HSTS condicional, anti-clickjacking y `nosniff`.
- Rate limits, bloqueo temporal y mensajes que no enumeran cuentas.
- Roles en servidor y auditoría con metadatos redactados.
- Secretos externos a Git y base PostgreSQL privada en Staging.

### Changed

- Sustitución del prototipo monolítico SQLite por un monolito modular preparado para PostgreSQL.
- Cálculo de puntos y rachas derivado de eventos diarios idempotentes.

### Fixed

- Duplicación de puntos por reenvío.
- Inconsistencias entre rutas, plantillas y modelo.
- Incompatibilidad CSRF detectada en prueba de navegador.
- Alta administrativa sin validación equivalente a la interfaz.
