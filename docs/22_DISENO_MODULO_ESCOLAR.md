# Diseño de la experiencia personal y escolar

Fecha del diseño: 14 de octubre de 2026 (Colombia). Estado inicial: implementación en rama, no publicado todavía.

## Objetivo y hechos

VitaliLab ya usa Flask modular, SQLAlchemy, PostgreSQL en el laboratorio NexoStack, sesiones, CSRF, roles globales user/admin y nueve tablas de negocio. El perfil personal/institucional actual solo almacena una preferencia; no acredita pertenencia ni acceso docente. Se conserva la producción original de Render.

## Decisiones y supuestos controlados

- Se amplía el monolito con módulo `school` y servicios de seguimiento/movimiento. Sin microservicios ni dependencias de gráficos externas.
- Catálogo inicial con los dos nombres proporcionados por el propietario. Son opciones de un piloto académico, no evidencia de convenios ni autorizaciones de esos colegios.
- Una vinculación institucional vigente por cuenta en esta edición. Un docente podrá tener varios grupos del mismo colegio.
- Estudiantes y docentes solicitan vinculación. Las solicitudes quedan pendientes hasta revisión de un administrador. Seleccionar docente no modifica el rol global ni permite leer reportes.
- Solo administradores crean grupos por año escolar, validan solicitudes y asignan docentes. Ninguna solicitud pública puede crear un grupo o asignarse permisos.
- Los reportes requieren colegio/grupo activos, vinculación docente aprobada, grupo asignado y enfoque institucional. Toda revocación se aplica en cada petición.
- Estadísticas agregadas por mes calendario del año del grupo. Umbral mínimo: diez estudiantes distintos que hayan habilitado compartir agregados; cada indicador mensual también debe alcanzar diez participantes. Sin filtros por sexo/edad, nombres, exportaciones individuales ni informes de grupos pequeños. Supresión y redondeo reducen riesgos, pero no equivalen a anonimato matemático.
- Compartir agregados es opcional, revocable y desactivado por defecto. El laboratorio se usa con datos ficticios. Antes de datos reales, el colegio debe completar autorizaciones, responsabilidades, revisión de contenido y procedimiento para menores.
- Las mediciones y el historial pertenecen a la persona, no al docente. Se conserva el historial y se ofrece filtro anual con tabla accesible y gráfica sin juicios corporales.
- La interpretación infantil exige referencia documentada por edad y sexo. Sin datos suficientes no se aplican umbrales adultos. No se atribuye un diagnóstico al IMC ni se decide una rutina solo por ese número.
- «Tu próximo paso» se personaliza por objetivo funcional elegido (centro, energía o fuerza), con adaptación suave y opción de detenerse. No recompensa cambios corporales.
- Una rutina se registra una vez por usuario/día; su hábito asociado también sigue siendo único por día. Varias rutinas del mismo hábito no duplican XP.

## Modelo relacional

1. `schools`: catálogo, identificador estable y estado activo.
2. `school_groups`: colegio, nombre, año y estado; unicidad colegio/año/nombre.
3. `school_memberships`: usuario único, colegio, grupo opcional, rol solicitado, estado, revisión administrativa, consentimiento de agregados. Los grupos deben pertenecer al mismo colegio mediante FK compuesta.
4. `teacher_group_assignments`: vinculación docente, colegio y grupo; claves compuestas evitan asignaciones cruzadas entre colegios.
5. `routine_completions`: usuario, rutina, día, hábito asociado; UNIQUE usuario/rutina/día.
6. Extensión de perfil con objetivo funcional y referencia sexual opcional; metadatos de medición para interpretación reproducible cuando proceda. No se deduce sexo a partir de nombre ni identidad.

No se convierten nombres libres anteriores en membresías aprobadas ni se clasifican personas automáticamente por colegio. Migración aditiva después de `7ca6e014b982`; rollback de código conservando tablas y columnas nuevas.

## Flujos y contratos

- `/colegios/`: estado de la propia vinculación, solicitud, retiro y preferencia de agregados.
- `/docentes/`: grupos propios asignados; `/docentes/grupos/<id>`: reporte agregado con autorización explícita.
- `/docentes/rutinas/<slug>/proyectar`: vista limpia de clase; sin datos personales.
- `/admin/colegios/`: catálogo, grupos, revisión de solicitudes y asignaciones; solo admin.
- `/perfil/`: mediciones voluntarias, referencias neutrales y próximo paso.
- `/perfil/seguimiento`: historial anual propio, sin parámetro de usuario externo.
- `/rutinas/<slug>/registrar`: POST con CSRF, sesión y protección contra duplicación.

## Plan y aceptación

1. Modelo y migración; comprobar datos existentes y ausencia de deriva.
2. Servicios de autorización, vinculaciones y agregados con denegación por defecto.
3. Formulario/registro, panel docente, administración y proyección.
4. Seguimiento y próximo paso; registrar rutinas sin sumar XP dos veces.
5. Pruebas de permisos cruzados, revocación, grupos pequeños, opt-out, fechas, referencia infantil, duplicados y regresión.
6. QA móvil/escritorio, CI PostgreSQL con backup/restore de todas las entidades y despliegue aislado con respaldo previo.

Una publicación del piloto no se presentará como autorización clínica, certificación de cumplimiento ni habilitación para recoger datos reales de menores. Los resultados y limitaciones se registrarán en el informe de QA del cambio.
