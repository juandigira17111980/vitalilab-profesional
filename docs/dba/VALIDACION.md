# Evidencia de preparación y límites

Fecha: 15 de octubre de 2026. Responsable de autorización: propietario del proyecto. Destinatario de estudio: identidad GitHub `ega1026`.

## Comprobado

- Lectura de catálogos y exportación SOLO de estructura de PostgreSQL 18.6, revisión `c842d6e190ab`. No se exportaron filas, hashes de cuentas ni secretos del sitio.
- Inventario: 17 entidades de negocio, 148 columnas, 22 restricciones FK; `alembic_version` se documenta aparte como tabla técnica.
- Modelo completo generado desde catálogos; diccionario de tipos físicos, nulabilidad, defaults, restricciones e índices. Las pruebas comparan columnas y FK con los modelos Python versionados.
- Ocho pruebas específicas del paquete: integridad documental, reproducibilidad, relaciones reales, exportación sin datos, destino de estudio y separación de permisos/configuración.

## Preparado, pendiente de evidencia de ejecución

- Configuración de instancia PostgreSQL de estudio con recursos, red, almacenamiento y secretos propios, puerto local y TLS.
- Semilla ficticia en las 17 entidades, consultas guiadas y prácticas con ROLLBACK. Su ejecución remota y el resultado CI se registrarán en este mismo documento al completar las comprobaciones.
- Rol limitado `ega1026_estudio`, inicialmente NOLOGIN; no es el dueño del motor ni el rol web.

## Pendiente de la persona

El propietario indicó que el compañero no tiene llave SSH. Debe generarla en su equipo y entregar SOLO el archivo `.pub`. Faltan autorización de esa llave, túnel restringido, entrega privada de contraseña y certificado, y comprobación de conexión desde su computadora. No se ha dado acceso al VPS ni a la base publicada.

## Lo que esta entrega no certifica

No es auditoría clínica/legal, autorización para tratar datos reales de menores, mejora de rendimiento medida ni alta disponibilidad. Una restauración en el mismo VPS no acredita recuperación tras perder todo el servidor. La copia sintética no incluye el historial ni las cuentas del sitio.
