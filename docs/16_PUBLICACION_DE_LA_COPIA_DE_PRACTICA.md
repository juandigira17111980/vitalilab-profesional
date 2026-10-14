# Publicación de la copia de práctica

Edición del 13 de octubre de 2026. Esta guía operativa complementa los capítulos 11 a 13 del [manual desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md). Primero se aprende y verifica en local; después se prueba una URL compartida.

## 1 Estado confirmado y decisiones pendientes

El repositorio privado pertenece a `juandigira17111980` y se llama `vitalilab-profesional`. La reconstrucción se integra en `staging`; el Render histórico utiliza otro repositorio, `ega1026/vitalilab`. No confundir un cambio en nuestro repositorio con un cambio ya ejecutado por ese servicio.

La base `vitalilab-staging-db` de Render estaba disponible el 13 de octubre, con acceso externo cerrado. No existe todavía un servicio web de Staging validado. La cuenta Render tiene credencial Git `ega1026`; por eso no se resolvió el acceso al repositorio privado nuevo. La instancia gratuita concreta vence el 31 de octubre a las 21:36 de Colombia.

Para Vercel se añadieron `vercel.json`, entrada `wsgi:app`, preparación de `public/static` y carpeta temporal de ejecución. Esa preparación no crea una cuenta Vercel ni una PostgreSQL externa.

## 2 Lo que necesita el docente

1. Iniciar sesión en Vercel desde el navegador con su propia cuenta.
2. Crear un proyecto separado, llamado `vitalilab-practica` o equivalente disponible.
3. Elegir una PostgreSQL de práctica accesible desde Vercel, con TLS y costo autorizado.
4. Configurar secretos en los campos privados del proveedor.
5. Aplicar migraciones y verificar el recorrido funcional.

No debe enviar tokens o contraseñas por chat. Una autorización por navegador permite conectar el CLI sin compartirlos. Crear un plan pagado exige una decisión explícita de costo, no una inferencia a partir de la necesidad de publicar.

## 3 Configuración incluida en el código

`pyproject.toml` selecciona `wsgi:app` como entrada Vercel. El build definido en `vercel.json` ejecuta `python scripts/build_vercel.py`, que copia los archivos de `app/static` a `public/static`. Las plantillas siguen usando `/static/css/app.css`, `/static/js/app.js` y `/static/img/brand-mark.svg`.

El bundle excluye documentación, pruebas, migraciones y activos públicos. Las migraciones se ejecutan desde una terminal o job administrado antes de usar la copia. No se hacen dentro de una solicitud de usuario.

Al detectar `VERCEL=1`, Flask ubica `instance` en la carpeta temporal del runtime. Esa adaptación resuelve la escritura de ejecución en un bundle de solo lectura; no convierte archivos temporales en almacenamiento permanente.

Las pruebas de despliegue verifican carpeta temporal y preservación de las direcciones estáticas. La validación del esquema oficial de `vercel.json` también pasó localmente. Todavía se requiere una construcción real con Vercel y una URL funcional.

## 4 Secuencia por CLI

Desde la raíz del proyecto y con Node.js disponible:

```powershell
npx vercel login
npx vercel link
```

Seleccione la cuenta correcta y el proyecto nuevo de práctica. Si aparece otro proyecto, corrija la selección antes de continuar. Configure en Preview `APP_ENV=staging`, `APP_VERSION`, `SECRET_KEY`, `DATABASE_URL`, `SESSION_COOKIE_SECURE=true` y `SESSION_COOKIE_SAMESITE=Lax`.

La conexión PostgreSQL debe ser del ambiente de práctica y seguir los parámetros TLS del proveedor. La base Render cerrada no admite esta conexión externa mediante su host interno. No se debe cambiar esa protección a acceso universal como atajo.

Desde una terminal autorizada, con esas variables privadas cargadas, ejecute:

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi:app db upgrade
.\.venv\Scripts\python.exe -m flask --app wsgi:app seed-habits
.\.venv\Scripts\python.exe -m flask --app wsgi:app db check
npx vercel deploy
```

No añada `--prod` para este primer Preview. Guarde la URL y el commit. La configuración local de enlace `.vercel` está ignorada por Git.

## 5 Secuencia por el panel

Elija crear proyecto e importar el repositorio privado autorizado. Revise qué rama contiene esta edición y el framework Flask. El build está en el archivo de configuración. Cargue las variables del ambiente correspondiente y prepare la base.

La importación inicial puede publicar el ambiente llamado Production del proyecto de demostración. No es el servicio Render histórico, pero debe quedar nombrado y documentado como copia académica. Después mantenga Previews para revisiones y no asigne el dominio real a esta copia antes de aprobar la transición.

## 6 Lista de aceptación de la URL

| Prueba | Evidencia esperada |
|---|---|
| Inicio y recursos públicos | HTTPS y CSS JS SVG cargados |
| Health | 200 y versión del commit |
| Readiness | 200 y PostgreSQL disponible |
| Registro y sesión | Cuenta ficticia accede al panel |
| Persistencia | Login posterior conserva datos |
| Hábito repetido | Un evento diario y puntos sin duplicación |
| Perfil | Validación cruzada y datos de usuario propio |
| Administración | Usuario normal 403 y admin permitido |
| Comunicado | Borrador privado y publicación visible |
| Móvil y teclado | Menú usable y formularios legibles |
| Recuperación | Correo real solo si servicio configurado y comprobado |
| Logs | Sin errores recurrentes ni secretos |

Si Preview exige acceso, confirme cómo ingresarán los estudiantes según el plan y la protección disponible. Un enlace protegido no es automáticamente una URL abierta para todo el grupo.

## 7 Límites que no deben ocultarse

El rate limiting actual utiliza memoria del proceso. Vercel puede ejecutar varias instancias y esa memoria no es un contador global. Antes de usuarios reales debe implementarse y verificarse almacenamiento compartido compatible o protección central.

SMTP requiere servicio real y compatibilidad del alojamiento. Render Free bloquea puertos SMTP usuales; no basta completar `MAIL_*`. Cambiar el transporte a una API de correo sería otra implementación.

La aplicación exige PostgreSQL en staging y production. No se usa SQLite del bundle ni `/tmp` para conservar registros compartidos. Un backup probado en CI no equivale a retención y recuperación operativas del proveedor.

## 8 Registro de publicación

Al terminar, complete fecha, propietario, proyecto, ambiente, URL, commit, versión Alembic, proveedor de datos, resultados de la lista anterior y limitaciones. Registre nombres de variables, nunca sus valores privados.

Si falta cuenta, permiso o base, el estado es preparado para publicación y la práctica continúa en local. No se sustituye esa evidencia con una captura del sitio histórico.

## 9 Fuentes oficiales

- [Flask en Vercel](https://vercel.com/docs/frameworks/backend/flask)
- [Runtime Python](https://vercel.com/docs/functions/runtimes/python)
- [Ambientes Vercel](https://vercel.com/docs/deployments/environments)
- [Flask en Render](https://render.com/docs/deploy-flask)
- [Conexión Git a Render](https://render.com/docs/git-provider)
- [Restricciones Render Free](https://render.com/docs/free)
