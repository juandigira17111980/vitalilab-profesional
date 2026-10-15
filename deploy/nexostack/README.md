# VitaliLab en NexoStack: laboratorio aislado

Este montaje utiliza Docker Compose y el proxy Traefik existente, como los laboratorios del VPS. No recrea Coolify ni usa las bases Supabase de Mercanta/Murano. No convierte este servicio manual en un recurso administrado por el panel de Coolify.

Destino original: `https://vitalilab.lab.nexostack.app`. El propietario autorizó añadir `vitalilab.space` y `www.vitalilab.space`, conservando Render. Ver `docs/24_DOMINIO_PRINCIPAL_HOSTINGER.md` para las etapas de DNS y HTTPS; preparación no equivale a conexión terminada.

## Componentes

- Proyecto Compose `vitalilab-lab`, carpeta `/opt/labs/vitalilab`.
- Web no root (UID 10001), raíz de archivos de solo lectura, 384 MiB y 0,75 CPU.
- PostgreSQL 18 propia: 256 MiB, 0,5 CPU, volumen `vitalilab-lab-pgdata` montado en `/var/lib/postgresql`.
- Red de datos interna; la base no publica puertos y no pertenece a `coolify`.
- Solo la web utiliza la red de entrada compartida `coolify`. Compartir proxy/host no equivale a aislamiento físico entre clientes; nunca montar el socket Docker en la web.
- TLS de base con certificado de nombre `db`, CA específica y `sslmode=verify-full`.
- `vitalilab_owner` solo para migración/backup; `vitalilab_app` sin superusuario, creación de roles, bases o tablas.
- Secretos generados en el servidor y no versionados. No copiar `.env` local de desarrollo.

## Despliegue del administrador de infraestructura

1. Validar el commit mediante CI y guardar el estado de los contenedores existentes.
2. Crear un archivo del commit con `git archive`, cargarlo por SSH y extraerlo en `/opt/labs/vitalilab/releases/<SHA completo>`.
3. Aplicar `bootstrap.sh` una sola vez: secretos y certificado, sin imprimir contraseñas.
4. Ejecutar como administrador `bash deploy/nexostack/deploy.sh <SHA completo>` desde esa versión.
5. El script valida Compose, construye la imagen, inicia solo su base, migra, carga el catálogo, concede DML al usuario de aplicación y sustituye solo su web.
6. Probar HTTPS, cookies, registro, hábito repetido, permisos y persistencia. Comparar todos los contenedores previos con su estado inicial.
7. Registrar commit, imagen, revisión Alembic, URL, pruebas y límites. El sitio de Render se conserva sin cambios.

No usar `docker compose down -v`, `docker system prune`, ni reiniciar el proxy o el daemon Docker para este despliegue. Los comandos de este montaje fijan su proyecto y archivo Compose; no se ejecutan sobre una carpeta ajena.

## Acceso limitado de gestión

Los usuarios Linux `vitalilab-juan` y `vitalilab-emanuel` utilizan llaves independientes, con comando SSH forzado, sin terminal, transferencia de archivos ni reenvío de puertos. No pertenecen a `docker` ni `sudo`.

`ssh-gateway.sh` solo acepta `status`, `health`, `restart`, `backup` y `events`. `vitalilab.sudoers` concede únicamente esas cinco invocaciones exactas a `ops.sh`, propiedad de root. No permite cambiar código, exportar datos, restaurar o eliminar una base, leer secretos o operar otro proyecto.

La lista SSH existente admite root y nexoadmin. `99-vitalilab-operators.conf` agrega únicamente los dos operadores, sin quitar nombres anteriores ni habilitar contraseñas. Se valida con `sshd -t`, se comprueba la lista efectiva y se recarga SSH, no se reinicia el VPS. El monitor utiliza `DynamicUser` para no compartir la identidad global nobody.

En la aplicación, las cuentas individuales con rol `admin` gestionan comunicados y consultan el resumen de auditoría. Ese rol no administra el VPS ni ofrece un editor libre de SQL. No hay una cuenta principal compartida.

## Respaldos y monitoreo

- `backup.sh` crea un dump custom y su SHA-256, con permisos privados; retención de 14 días solo en `/opt/labs/vitalilab/backups`.
- Timer diario: 07:30 UTC, equivalente a 02:30 Colombia, con hasta cinco minutos de variación.
- `vitalilab-check.timer` comprueba `/ready` cada cinco minutos y registra fallos en systemd. Esto no envía todavía alertas por correo o WhatsApp.
- El administrador debe copiar el respaldo fuera del servidor mediante un canal protegido. Un respaldo que solo vive en el mismo disco no protege contra pérdida del VPS.
- Restaurar para comprobar en una base temporal independiente y comparar esquema, catálogo, usuarios y cumplimientos. Nunca ensayar un restore encima de los datos en uso.

Para este laboratorio, objetivos propuestos: RPO de 24 horas con copia fuera del host y RTO de una hora. No son un SLA ni una prueba de recuperación de todo el servidor. La retención externa y alertas personales deben acordarse antes de usar datos reales.

## Rollback y mantenimiento

Una versión anterior se despliega indicando su SHA completo a `deploy.sh`; el script realiza un respaldo antes de migrar. Solo es seguro regresar código si conserva compatibilidad con el esquema. No ejecutar `db downgrade` sobre una base compartida sin ensayo y aprobación.

El certificado interno dura 365 días: el administrador debe renovarlo antes de vencer y comprobar ambos clientes. El certificado público lo solicita el resolver existente de Traefik; se valida su emisión real durante la publicación.

La memoria del rate limit sigue siendo de un worker y se reinicia con el proceso. SMTP real, revocación global de sesiones, operación offsite y revisión formal de accesibilidad siguen siendo puntos de readiness; no se declaran resueltos por crear contenedores.
