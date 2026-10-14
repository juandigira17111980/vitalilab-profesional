# NexoStack: operación y accesos de VitaliLab

Fecha de referencia: 13 de octubre de 2026, Colombia.

## 1 Objetivo autorizado

Publicar una copia académica independiente en el VPS NexoStack, manteniendo sin cambios la producción de Render y los proyectos existentes del servidor. No migrar datos de personas reales del prototipo.

URL publicada y comprobada: `https://vitalilab.lab.nexostack.app`. Primera publicación verificada: commit `455d5ee4a23a8776607fd312607d77bdd91bdca9`. La versión activa se consulta en `/health`; las revisiones posteriores deben comprobar su propio commit. Laboratorio aprobado para práctica, no promoción de producción.

## 2 Qué significa el montaje para un estudiante

Un VPS es un computador remoto. Docker ejecuta cada servicio en un contenedor; Compose describe cómo se conectan. El proxy recibe HTTPS y envía únicamente el dominio de VitaliLab a su web. La web convierte formularios en operaciones sobre su PostgreSQL. Un volumen conserva esos datos al sustituir la web.

La carpeta y el proyecto de Docker se llaman VitaliLab, no Mercanta. La base es nueva y sus usuarios son diferentes. Los puertos de base no están publicados en internet. Aun así, un mismo VPS comparte hardware y el proxy: por eso ponemos límites de recursos y verificamos los servicios antes y después.

Los archivos concretos y procedimientos están en [deploy/nexostack](../deploy/nexostack/README.md). El archivo local `compose.yaml` sigue siendo un ejemplo de desarrollo, no se utiliza en el VPS con sus contraseñas de ejemplo.

## 3 Tres niveles de acceso diferentes

| Nivel | Quién | Qué permite | Qué no permite |
|---|---|---|---|
| Estudiante | Cuenta de usuario | Perfil propio, hábitos y progreso | Administrar comunicados o servidor |
| Administrador de la aplicación | Juan y Emanuel, cuentas separadas | Comunicados y resumen de auditoría | SQL libre, bases ajenas o administración del VPS |
| Operador básico de infraestructura | Llave propia para cada persona | Estado, salud, reinicio de la web, backup y eventos del monitor | Terminal libre, cambios de código, eliminación, restore, archivos privados o Docker general |

El administrador de infraestructura conserva despliegue, migraciones y restauración. No entregamos Coolify Admin ni el grupo Docker a un operador básico: administrar un recurso desde un panel privilegiado puede abrir acceso al servidor compartido.

## 4 Cómo entrar a la aplicación

1. Abre la URL de VitaliLab con HTTPS.
2. Elige ingresar; utiliza tu correo individual y la contraseña entregada por un canal privado.
3. Abre Administración para crear un comunicado, guardarlo como borrador y publicarlo.
4. Cierra sesión al terminar. No compartas cuenta entre integrantes ni captures contraseñas en la sustentación.

Las credenciales y las llaves no se incorporan a Git, al PDF ni al ZIP académico. Un archivo privado de acceso se entrega a cada responsable, no al grupo de estudiantes. Recuperación por correo solo se declara disponible después de configurar y probar un proveedor real; no hay SMTP real confirmado en esta entrega.

## 5 Gestión básica desde Windows

Guarda tu llave en una carpeta privada de tu equipo y no la subas al repositorio. OpenSSH debe estar disponible. El administrador entrega el host y un archivo de instrucciones individual con rutas reales. La forma de las órdenes es:

```powershell
ssh -i RUTA_A_TU_LLAVE vitalilab-juan@HOST_NEXOSTACK status
ssh -i RUTA_A_TU_LLAVE vitalilab-juan@HOST_NEXOSTACK health
ssh -i RUTA_A_TU_LLAVE vitalilab-juan@HOST_NEXOSTACK restart
ssh -i RUTA_A_TU_LLAVE vitalilab-juan@HOST_NEXOSTACK backup
ssh -i RUTA_A_TU_LLAVE vitalilab-juan@HOST_NEXOSTACK events
```

`RUTA_A_TU_LLAVE` y `HOST_NEXOSTACK` son referencias que deben sustituirse con los datos privados de entrega; no son órdenes listas para copiar. Emanuel usa `vitalilab-emanuel`. Reiniciar interrumpe brevemente solo la web de VitaliLab, no borra su volumen. Los operadores no pueden descargar un dump con esa llave; el administrador controla las exportaciones de datos.

Si se pierde o expone una llave, retírala de la cuenta correspondiente y emite otra. No desactives las restricciones para solucionar un error de conexión. Al terminar el acceso de una persona, revoca tanto la llave como su cuenta de aplicación: son permisos separados.

## 6 Evidencias que se exigirán al publicar

- HTTPS válido, redirección de HTTP y CSS/JavaScript/SVG correctos.
- `/health` con el commit publicado y `/ready` con 200.
- Dos migraciones, siete tablas y cuatro hábitos iniciales.
- Registro con CSRF, login, sesión segura y rol administrativo.
- Un único cumplimiento al repetir el hábito del día.
- Persistencia tras reiniciar solo VitaliLab.
- Usuario de base de la web sin superusuario/CREATEDB/CREATEROLE/DDL y conexión TLS real.
- Backup y restauración aislada con conteos y revisión Alembic comparados.
- Llaves separadas y rechazo de comandos arbitrarios o reenvío.
- Estado final de los 29 contenedores anteriores comparado con sus identificadores, imágenes, fechas de inicio y reinicios.

La comprobación remota no reemplaza pruebas unitarias. Un contenedor saludable tampoco certifica privacidad, seguridad completa ni rendimiento a cualquier carga.

## 7 Registro de resultado

| Comprobación | Resultado observado |
|---|---|
| CI del primer release | Tres trabajos aprobados, run 38500297528 |
| Pruebas locales de cierre | 28 aprobadas, cobertura 90,67 % |
| URL | HTTPS, /health y /ready con 200 |
| Esquema | Alembic 208469fd48ef, sin deriva |
| Catálogo | Cuatro hábitos |
| Runtime SQL | vitalilab_app, TLS 1.3 y sin privilegios administrativos/CREATE |
| Web | UID 10001, raíz de solo lectura y sin puertos publicados en el host |
| Accesos | Login y admin de Juan/Emanuel probados; cookie Secure/HttpOnly; logout correcto |
| Gestores SSH | Ambos ejecutan status; id rechazado con salida 2; forwarding rechazado |
| Hábito repetido | Respuesta 200 y mensaje de no duplicación; un cumplimiento conservado |
| Interfaz real | Registro, hábito y perfil ficticio; 390/1280 px sin desborde, consola sin errores |
| Persistencia y permiso normal | Tras reinicio propio: perfil conservado y /admin/ con 403 |
| Comunicados | Borrador no público, publicación visible y archivo correcto con cuenta autorizada |
| Backup y restore | Dump 20261014T022937Z, siete conteos y Alembic iguales, sin deriva |
| Tiempo del restore | 9,37 segundos para esta base pequeña; no es RTO del VPS completo |
| Convivencia inicial | Los 29 contenedores previos conservan ID, imagen, inicio y reinicios |

El dump capturó tres usuarios y perfiles, cuatro hábitos, un cumplimiento y ocho eventos en ese instante. Esos conteos son evidencia de esa copia, no valores fijos para una base que sigue recibiendo práctica. La base temporal `vitalilab_restore_qa_20261013` se eliminó al terminar; la base activa y el respaldo permanecieron.

El ensayo de restore ejecutó una tarea puntual que inicialmente recreó solo su dependencia PostgreSQL. El volumen conservó los datos. Se ajustó el comando a `run --no-deps` después de validar la base, para evitar ese efecto en las tareas posteriores. El monitor se cambió de nobody a una identidad dinámica específica. La lista SSH se amplió solo con los dos operadores tras validar sintaxis y comprobar que root/nexoadmin se conservan.

El reinicio deliberado de la web produjo una respuesta 503 durante su breve transición; al volver a saludable se confirmó el perfil persistente y el rechazo 403 de admin al usuario normal. No se presenta una interrupción de mantenimiento como pérdida de datos ni como prueba de disponibilidad continua. Las llaves de ambos operadores se probaron; Emanuel también generó un backup con su permiso limitado.

CI verificable: [ejecución del release inicial](https://github.com/juandigira17111980/vitalilab-profesional/actions/runs/38500297528). Los resultados adicionales y la versión final del paquete se registran con la entrega, sin incluir credenciales.

## 9 Criterios utilizados

- `arquitecto-infra-devops`: aislamiento lógico, límites de recursos, HTTPS, respaldo, monitor y reversión.
- `git-github-devops`: rama separada, commit identificable, PR y CI antes de activar.
- `auditor-qa-final`: evidencias reales, pruebas negativas, convivencia y separación de laboratorio/producción.
- `arquitecto-dba-empresarial`: PostgreSQL relacional propia, rol DML, TLS, volumen y restore aislado.
- `arquitecto-backend-desktop`: revisión de sesión/configuración y prueba de cookie remember Secure.
- `desarrollador-web-fullstack`: flujo completo, formularios, permisos y validación de interfaz publicada.
- `playwright`: prueba en navegador de registro, hábito y pantalla móvil, sin confundirla con tests unitarios.
- `pages:write-page` y `pdf:pdf`: manual progresivo fiel al código y revisión de su presentación para estudiantes.

## 8 Alcance y límites

Laboratorio con datos ficticios; producción de Render no promovida. RPO/RTO, copias externas permanentes, alertas personales, SMTP y evaluación institucional de privacidad requieren definición antes de datos reales. Las fechas de hábito usan el día del servidor (en este montaje se fija America/Bogota); no la zona de cada perfil. Cambiar puntos del catálogo modifica la interpretación histórica. El cambio de clave no revoca globalmente todas las sesiones actuales.

Se inspeccionan código, configuración, pruebas y runtime con evidencias concretas. No es un pentest formal ni una certificación regulatoria o revisión humana integral línea por línea.
