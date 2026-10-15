# Publicación de la copia de práctica en NexoStack

Edición del 13 de octubre de 2026, Colombia. Complementa los capítulos 11 a 13 del [manual desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md) y la [guía operativa](18_NEXOSTACK_OPERACION_Y_ACCESOS.md).

## 1 Qué se publica y qué se conserva

VitaliLab de práctica utiliza `https://vitalilab.lab.nexostack.app`, una PostgreSQL propia y el código del repositorio privado `juandigira17111980/vitalilab-profesional`. No sustituye la web original de Render ni migra sus datos. Los proyectos existentes del VPS no se reconstruyen ni se reinician para este montaje.

La primera publicación comprobada corresponde al commit `455d5ee4a23a8776607fd312607d77bdd91bdca9`, con CI aprobado. La versión activa se consulta en `/health`; cada actualización debe relacionar ese valor con su commit, resultado de pruebas y registro de despliegue.

## 2 Condiciones antes de publicar

1. Confirmar autorización sobre el laboratorio, no sobre una promoción productiva.
2. Verificar CI del commit, espacio de disco, memoria y nombres de recursos nuevos.
3. Guardar identificadores, imágenes, inicio y reinicios de los servicios anteriores.
4. Confirmar DNS y el proxy existentes, sin reemplazar su configuración.
5. Preparar credenciales propias y un esquema vacío con datos ficticios.

El administrador de infraestructura conserva la cuenta confiable del servidor. Los estudiantes reciben código y documentación; los responsables reciben accesos privados individuales.

## 3 Archivos que hacen reproducible el montaje

| Archivo | Responsabilidad |
|---|---|
| Dockerfile | Python, dependencias, usuario no root y Gunicorn |
| deploy/nexostack/compose.yaml | Web, tarea de migración, base, redes, volumen y límites |
| bootstrap.sh | Secretos aleatorios y certificado de base |
| init-database.sh | Usuario runtime sin privilegios de administración |
| deploy.sh | Bloqueo, build, backup previo, migración, seed y activación |
| backup.sh | Dump privado, huella SHA-256 y retención limitada |
| ops.sh y ssh-gateway.sh | Cinco operaciones exactas para gestores |
| vitalilab.sudoers | Privilegios únicamente para el control de VitaliLab |
| 99-vitalilab-operators.conf | Dos operadores agregados a la lista SSH existente |
| vitalilab-backup.timer | Backup diario del proyecto |
| vitalilab-check.timer | Comprobación periódica de readiness |

El `compose.yaml` de la raíz corresponde a desarrollo local y no se publica con sus secretos de ejemplo. Las contraseñas reales del VPS se generan fuera de Git.

## 4 Secuencia del administrador

1. Empaquetar el commit verificado con `git archive`, cargar el archivo por SSH y comparar SHA-256.
2. Extraer solamente en `/opt/labs/vitalilab/releases/<SHA completo>`.
3. Ejecutar `bootstrap.sh` para preparar configuración privada; no imprimirla.
4. Ejecutar `deploy.sh <SHA completo>` como administrador confiable.
5. Esperar base saludable, migraciones, seed, ausencia de deriva y web saludable.
6. Crear las cuentas individuales autorizadas con claves distintas, sin enviar secretos al chat.
7. Instalar únicamente los operadores, controles y timers de VitaliLab; validar sudoers y SSH antes de recargar.
8. Probar la URL, los permisos y la persistencia.
9. Crear un dump, restaurarlo en una base temporal, comparar tablas y Alembic y eliminar solo la base temporal.
10. Comparar el estado de todos los servicios previos y registrar el resultado.

No usar limpieza global de Docker, reinicio del VPS o del proxy, eliminación de volúmenes, migraciones sobre Supabase ajena o comandos `down` sobre otros proyectos. No se instala acceso a Docker ni una terminal de root para los gestores.

## 5 Seguridad de conexión y datos

Solo la web comparte la red del proxy. PostgreSQL permanece en una red interna sin puertos publicados. La web conecta por TLS con verificación del certificado y nombre del servidor. Se comprobó TLS 1.3 y el rol `vitalilab_app` sin superusuario, CREATEDB, CREATEROLE ni CREATE de esquema.

Las migraciones usan otro rol en esta misma PostgreSQL independiente. La base persistente no está en la imagen web. En PostgreSQL 18 se monta el volumen en `/var/lib/postgresql`, de acuerdo con su estructura versionada.

La web utiliza una identidad no root, archivos de solo lectura, temporales limitados, capacidades eliminadas y límites de memoria/CPU. Los logs de acceso no incluyen direcciones de recuperación ni cabeceras o contraseñas.

## 6 Lista de aceptación

| Prueba | Evidencia esperada |
|---|---|
| Entrada pública | HTTPS válido, HTTP redirige y assets locales cargan |
| Proceso y datos | /health con commit y /ready con 200 |
| Registro | Usuario ficticio creado con CSRF activo |
| Persistencia | Login posterior conserva progreso tras reinicio propio |
| Hábito repetido | Un cumplimiento, sin sumar otra vez |
| Perfil | Validación cruzada y datos del usuario conectado |
| Administración | Usuario normal 403 y cada administrador autorizado 200 |
| Comunicado | Borrador privado, publicación visible y archivo correcto |
| Móvil y teclado | Navegación y formularios utilizables |
| Gestión SSH | Cinco operaciones permitidas, otras órdenes y forwarding rechazados |
| Base | TLS y permisos runtime mínimos comprobados |
| Recuperación | Dump restaurado aparte, conteos/revisión iguales y sin deriva |
| Convivencia | Servicios previos conservan IDs, imágenes, inicio y reinicios |

La aceptación se completa con la evidencia de [operación y accesos](18_NEXOSTACK_OPERACION_Y_ACCESOS.md). No memorizar una nota técnica: explicar el resultado, sus límites y cómo repetirlo.

## 7 Lo que todavía requiere una decisión productiva

El laboratorio usa un worker con rate limiting en memoria. SMTP real, alertas personales, retención offsite automatizada, accesibilidad formal y privacidad institucional requieren validación adicional. No declarar 100/100 ni producción aprobada a partir de un conjunto de pruebas.

Un grupo que comparte una IP puede alcanzar los límites de registro/acceso de la aplicación. Organice las primeras prácticas en local; una prueba simultánea de toda la clase requiere dimensionar y revisar su política de límites, no deshabilitar controles sin evaluar el riesgo.

Cada usuario recibe instrucciones y una llave propias en archivos privados separados del paquete académico. Debe retirarse su llave y revocarse su cuenta cuando deje de gestionar el proyecto. La recuperación por correo no está conectada a un proveedor real en esta entrega.

## 8 Alternativas conservadas

`render.yaml` sigue describiendo una alternativa Render Staging. La base temporal creada allí no es la de NexoStack y no se expone al exterior. El montaje actual utiliza exclusivamente la configuración de `deploy/nexostack/`; se retiraron los adaptadores de proveedores no utilizados.

La elección actual aprovecha el VPS ya disponible. Un cambio futuro de proveedor requiere autorización, comprobación de sus condiciones vigentes y una nueva validación de la URL.

## 9 Referencias

- [Docker Compose](https://docs.docker.com/compose/)
- [Imagen oficial PostgreSQL y volumen de la versión 18](https://hub.docker.com/_/postgres)
- [Traefik y proveedor Docker](https://doc.traefik.io/traefik/reference/install-configuration/providers/docker/)
- [OpenSSH y AllowUsers](https://man.openbsd.org/sshd_config)
- [Roles y permisos de Coolify](https://coolify.io/docs/core/team/roles-and-permissions)
- [Límites Render Free](https://render.com/docs/free)
