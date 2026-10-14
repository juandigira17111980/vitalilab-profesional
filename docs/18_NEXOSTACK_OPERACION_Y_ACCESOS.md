# NexoStack: operación y accesos de VitaliLab

Fecha de referencia: 13 de octubre de 2026, Colombia.

## 1 Objetivo autorizado

Publicar una copia académica independiente en el VPS NexoStack, manteniendo sin cambios la producción de Render y los proyectos existentes del servidor. No migrar datos de personas reales del prototipo.

URL objetivo: `https://vitalilab.lab.nexostack.app`. Estado antes de ejecutar: preparado, pendiente de evidencia de URL, base y acceso. Este documento se completará con los resultados reales, no con una promesa de 100/100.

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

Pendiente de completar con commit, fecha, versión Alembic, pruebas, respaldo, restauración y estado de las demás aplicaciones. Hasta completar ese registro, no presentar la URL objetivo como una web ya validada.

## 8 Alcance y límites

Laboratorio con datos ficticios; producción de Render no promovida. RPO/RTO, copias externas permanentes, alertas personales, SMTP y evaluación institucional de privacidad requieren definición antes de datos reales. Las fechas de hábito usan el día del servidor (en este montaje se fija America/Bogota); no la zona de cada perfil. Cambiar puntos del catálogo modifica la interpretación histórica. El cambio de clave no revoca globalmente todas las sesiones actuales.

Se inspeccionan código, configuración, pruebas y runtime con evidencias concretas. No es un pentest formal ni una certificación regulatoria o revisión humana integral línea por línea.
