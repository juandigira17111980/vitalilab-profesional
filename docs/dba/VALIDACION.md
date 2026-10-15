# Evidencia de preparación y límites

Fecha: 15 de octubre de 2026. Responsable de autorización: propietario del proyecto. Destinatario de estudio: identidad GitHub `ega1026`.

## Comprobado

- Lectura de catálogos y exportación SOLO de estructura de PostgreSQL 18.6, revisión `c842d6e190ab`. No se exportaron filas, hashes de cuentas ni secretos del sitio.
- Inventario: 17 entidades de negocio, 148 columnas, 22 restricciones FK; `alembic_version` se documenta aparte como tabla técnica.
- Modelo completo generado desde catálogos; diccionario de tipos físicos, nulabilidad, defaults, restricciones e índices. Las pruebas comparan columnas y FK con los modelos Python versionados.
- Diez pruebas específicas del paquete: integridad documental, reproducibilidad, relaciones reales, exportación sin datos, destino de estudio, permisos/configuración y comparación estricta de catálogos.
- Suite local completa: **164 pruebas aprobadas**, cobertura de aplicación **94,90 %**, Ruff/formato y Bandit sin hallazgos de los niveles evaluados; revisión de dependencias sin vulnerabilidades conocidas. Se conservan cinco avisos de deprecación de dependencias existentes, sin modificar la aplicación en este corte.

## Instancia ejecutada y comprobada en NexoStack

- Creada `vitalilab_estudio_ega1026` en un contenedor PostgreSQL propio, con recursos, red, almacenamiento y secretos separados; estado healthy. Puerto publicado exclusivamente en `127.0.0.1:55432` y conexión TLS con `verify-full` comprobada.
- Semilla ficticia presente en las 17 entidades. Ejecución de las trece consultas y del script de prácticas como rol de estudio mediante SET ROLE; cambios revertidos y conteos iniciales conservados.
- Rol `ega1026_estudio` NOLOGIN, sin superusuario, creación de bases/roles, replicación ni bypass RLS. Sin CREATE en `public`, sin UPDATE de Alembic ni CONNECT a la base técnica `postgres`; CREATE únicamente en su esquema personal. No existe este rol en la instancia publicada.
- Respaldo completo SOLO de la copia sintética y restauración en una base temporal de esa instancia. Comparados el esquema y los 17 conteos; retirada únicamente esa base temporal creada para la prueba. El respaldo ficticio se conserva con permisos privados en el área exclusiva de estudio.
- Las 17 tablas, 148 columnas, tipos, nulabilidad, defaults, nombres de restricciones, FK e índices coinciden con los catálogos capturados. PostgreSQL reescribe algunos CHECK de listas durante dump/restore: la comparación normaliza exclusivamente casts equivalentes de constantes varchar a text, conservando todos los valores y el resto de la expresión. No se ignoran reglas ni cambios numéricos.
- Comprobada continuidad de los contenedores existentes, sin cambios de identidad, inicio o reinicios durante la verificación. El arranque de estudio también comprobó que los 31 contenedores previos siguieran ejecutándose. No se desplegó código web ni se escribió en la base publicada.
- Primer cierre CI `934d6ef`: calidad, PostgreSQL con semilla/prácticas y construcción de contenedor aprobados en el [run 38813536379](https://github.com/juandigira17111980/vitalilab-profesional/actions/runs/38813536379). El cierre documental posterior se consulta en el PR 19.

Conteos de la semilla: users 5, user_profiles 5, health_measurements 3, habits 3, habit_entries 4, user_goals 2, daily_checkins 2, schools 2, school_groups 3, school_memberships 3, teacher_group_assignments 1, school_enrollment_requests 1, personal_routines 1, routine_exercises 2, routine_completions 1, announcements 1 y audit_events 1. Todos son inventados.

## Pendiente de la persona

El propietario indicó que el compañero no tiene llave SSH. Debe generarla en su equipo y entregar SOLO el archivo `.pub`. Faltan autorización de esa llave, identidad/túnel restringidos, entrega privada de contraseña y certificado, y comprobación de conexión desde su computadora. La cuenta de estudio permanece NOLOGIN: probar permisos mediante SET ROLE no demuestra que el compañero ya tenga acceso. No se ha dado acceso administrativo al VPS ni a la base publicada.

## Lo que esta entrega no certifica

No es auditoría clínica/legal, autorización para tratar datos reales de menores, mejora de rendimiento medida ni alta disponibilidad. Una restauración en el mismo VPS no acredita recuperación tras perder todo el servidor. La copia sintética no incluye el historial ni las cuentas del sitio.
