# VitaliLab: guía de base de datos y sustentación

Edición del 15 de octubre de 2026. Dirigida a estudiantes que están aprendiendo programación. Este documento y su anexo describen el esquema físico comprobado en PostgreSQL, no una base imaginada desde una maqueta.

## 1. Qué recibirás y qué podrás demostrar

El paquete contiene un modelo entidad-relación editable y visual, el diccionario de todos los campos, SQL para crear la estructura, datos inventados, consultas comentadas y prácticas reversibles. La base publicada no se comparte: se prepara otra instancia para estudiar sin exponer información real.

El corte corresponde a PostgreSQL 18.6, revisión Alembic `c842d6e190ab`: **17 tablas de negocio, 148 columnas y 22 restricciones de clave foránea**. Además existe `alembic_version`, tabla técnica de una columna que indica la migración aplicada. Por eso un navegador de base de datos muestra 18 tablas en `public`: no es una contradicción.

Los archivos principales son:

| Archivo | Para qué sirve |
|---|---|
| `estructura_postgresql.sql` | Crear tablas, secuencias, restricciones e índices en una base vacía. No contiene filas ni contraseñas. |
| `datos_ficticios.sql` | Poblar únicamente la base de estudio con cinco cuentas inventadas y ejemplos en las 17 entidades. |
| `catalogo_postgresql.json` | Evidencia legible por herramientas de los tipos y relaciones del motor. No contiene registros de usuarios. |
| `diccionario_postgresql.md` | Explicar cada tabla, cada columna, sus límites, valores por defecto e índices. |
| `modelo_completo.svg` | Ampliar o imprimir el diagrama de las 17 tablas con todos sus campos. |
| `modelo_completo.mmd` y `.dot` | Editar y regenerar el diagrama, sin dibujar relaciones a mano. |
| `consultas_sustentacion.sql` | Trece demostraciones de lectura, identidad, relaciones y permisos. |
| `practicas_transacciones.sql` | Probar altas, cambios, borrados, integridad y recuperación con ROLLBACK. |

## 2. Los conceptos desde cero

Una base de datos organiza información que debe sobrevivir al cierre del navegador. PostgreSQL es el programa que la administra. Una tabla agrupa elementos del mismo tipo: `users` contiene cuentas; `health_measurements`, mediciones. Una fila representa un elemento. Una columna representa una característica: correo, fecha o altura.

Un tipo limita qué puede guardarse. `integer` contiene enteros; `numeric(5,2)` admite cinco dígitos en total, dos decimales; `boolean` representa verdadero o falso; `date` guarda un día; `timestamp without time zone` guarda fecha y hora sin incorporar la zona. VitaliLab usa una convención UTC en su código para los instantes, y la zona del perfil para el día de negocio.

`NULL` significa que no se registró un valor; no es cero ni una cadena vacía. `NOT NULL` obliga a dar un valor, pero no verifica por sí solo su significado. `CHECK` comprueba una regla: por ejemplo, energía entre uno y cinco. `UNIQUE` impide repetir una combinación: usuario, hábito y día. Un índice ayuda al motor a localizar filas, pero tiene costo de escritura y no garantiza acelerar cualquier consulta.

Una clave primaria o PK identifica una fila sin ambigüedad. Una clave foránea o FK exige que exista una fila relacionada. La relación no se crea por escribir `_id`: debe existir una restricción real en el motor. La FK compuesta comprueba varias columnas como una unidad.

Un esquema es un espacio de nombres dentro de una base, no otra base: `public.users` es la tabla `users` del esquema `public`. La cuenta de estudio también tendrá `practica_ega1026` para crear sus propias tablas sin alterar la estructura del proyecto.

## 3. Tres accesos que no deben confundirse

| Acceso | Qué permite | Qué NO implica |
|---|---|---|
| GitHub `ega1026` | Descargar o colaborar en el código según la invitación del repositorio. | No abre PostgreSQL ni da control del servidor. |
| Cuenta web de VitaliLab | Usar las pantallas y funciones autorizadas del producto. | No permite consultar tablas directamente. |
| Rol PostgreSQL `ega1026_estudio` | Leer y practicar en una copia sintética, cuando se active. | No da acceso a la base publicada, al dueño del motor ni a otros proyectos. |

El túnel SSH autentica primero al equipo con una llave. PostgreSQL después autentica su propio rol. Son dos capas distintas. La llave pública se puede compartir para autorizar el equipo; la privada y su frase de protección nunca se envían.

## 4. Separación segura para esta práctica

La copia se define en `deploy/study/compose.yaml`: proyecto Docker propio, PostgreSQL propio, volumen propio y red interna propia. No utiliza los volúmenes, redes ni secretos del sitio. El puerto de la base solo escucha en `127.0.0.1:55432` del servidor; no se abre PostgreSQL a Internet. El estudio no cambia Render, el dominio público ni las otras aplicaciones.

Los límites iniciales son 256 MB de memoria, medio CPU, 128 procesos y 15 conexiones totales. El rol de estudio tiene un máximo de cuatro conexiones y límites de tiempo. Son límites de contención para una práctica pequeña, no una garantía de rendimiento ni un dimensionamiento para producción.

El permiso previsto permite SELECT, INSERT, UPDATE y DELETE sobre las 17 tablas de datos inventados, uso de sus secuencias y lectura de `alembic_version`. No concede TRUNCATE, cambios de estructura en `public`, administración de roles, creación de bases, superusuario, replicación ni lectura de archivos del servidor. En `practica_ega1026` sí puede crear sus tablas. Los permisos de otras bases técnicas de esa instancia también están cerrados para el alumno.

Esta amplitud de lectura es aceptable SOLO porque toda la copia es ficticia. No debe reutilizarse este rol ni su política sobre datos reales. El SQL directo no reproduce automáticamente las reglas de propiedad y anonimización de la aplicación: esas reglas están implementadas en backend. No se afirma que haya RLS por tener `NOBYPASSRLS`.

El acceso personal permanece **NOLOGIN** hasta recibir y validar una llave pública y preparar la entrega privada de la contraseña PostgreSQL. Crear la copia y probar sus permisos con el administrador no equivale a que el compañero ya se haya conectado.

## 5. Crear la llave en el Windows del compañero

Estos pasos los ejecuta `ega1026` en SU computadora, no en la de Juan. Abrir PowerShell y comprobar el cliente OpenSSH:

```powershell
ssh -V
```

Si no existe el comando, instalar **Cliente OpenSSH** desde las características opcionales de Windows o pedir ayuda al administrador del equipo. No instalar un servidor SSH para esta actividad.

Crear una carpeta de llaves y elegir un nombre exclusivo, sin sobrescribir llaves existentes:

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.ssh"
Test-Path "$env:USERPROFILE\.ssh\vitalilab_ega1026"
Test-Path "$env:USERPROFILE\.ssh\vitalilab_ega1026.pub"
```

Si cualquiera devuelve `True`, detenerse y revisar: no reemplazar archivos. Si ambas devuelven `False`, ejecutar:

```powershell
ssh-keygen -t ed25519 -C "ega1026-vitalilab-estudio" -f "$env:USERPROFILE\.ssh\vitalilab_ega1026"
```

Escribir una frase de protección personal cuando la pida; no se ve al escribir y no se comparte. Se generan dos archivos: `vitalilab_ega1026` es PRIVADO, `vitalilab_ega1026.pub` es PÚBLICO. Mostrar únicamente el público:

```powershell
Get-Content "$env:USERPROFILE\.ssh\vitalilab_ega1026.pub"
```

Compartir el archivo `.pub` o la línea que empieza por `ssh-ed25519`. No enviar el archivo sin extensión, contraseñas, tokens, capturas de secretos ni códigos de recuperación. El operador confirmará la huella del servidor por un canal conocido y habilitará una identidad SSH restringida a este túnel; no se ampliarán las cuentas de operación existentes.

## 6. Conectarse y ver el modelo en DBeaver

Instalar DBeaver Community desde su sitio oficial y crear una conexión PostgreSQL. **No intentar conectar antes de que el operador confirme la activación individual.** El certificado público de esta copia y la contraseña individual se entregarán por separado, nunca dentro del PDF, Git ni el ZIP.

La opción más fácil de comprobar es abrir un túnel en una ventana de PowerShell después de activar la llave:

```powershell
ssh -N -T -o ExitOnForwardFailure=yes -L 127.0.0.1:55433:127.0.0.1:55432 -i "$env:USERPROFILE\.ssh\vitalilab_ega1026" vitalilab-estudio-ega1026@vitalilab.lab.nexostack.app
```

Es un procedimiento preparado, no un acceso ya habilitado. Confirmar la huella SSH con la que entregue el operador; si cambia inesperadamente, detenerse. Mantener esa ventana abierta. El puerto 55433 pertenece a su computadora y 55432 al servidor. El comando no pide ni ofrece una consola de administración.

En DBeaver, la pestaña principal usaría estos valores con ese túnel:

| Campo | Valor |
|---|---|
| Host | `localhost` |
| Puerto local | `55433` |
| Base | `vitalilab_estudio_ega1026` |
| Usuario | `ega1026_estudio` |
| Contraseña | La individual entregada por canal privado; no está en este documento. |
| SSL | `verify-full`, usando el certificado público entregado de esta copia. |

En la configuración del driver se usa `sslmode=verify-full` y `sslrootcert` apuntando al certificado público recibido. No aceptar todos los certificados ni deshabilitar la verificación para ocultar un error. El certificado identifica `localhost` y `127.0.0.1` porque la conexión entra por el túnel.

Pulsar probar conexión. Abrir base, esquemas, `public`, tablas. Deben aparecer las 17 de negocio y `alembic_version`. El esquema personal aparecerá separado. Seleccionar las tablas del proyecto y abrir **ER Diagram**; los nombres exactos del menú pueden variar entre versiones. Ampliar, mover entidades y exportar la vista para una presentación. DBeaver dibuja lo que lee de las FK: no inventa reglas que solo existan en Python.

Al terminar, desconectar DBeaver y cerrar el túnel con Ctrl+C. Si falla: revisar activación de la llave, frase de protección, huella, ventana del túnel, puerto ocupado, nombre de base, usuario y certificado, en ese orden. No enviar capturas con contraseñas visibles.

## 7. Cómo leer el modelo entidad-relación

Una cuenta puede tener cero o un perfil desde el punto de vista de la FK física: `user_profiles.user_id` es PK y FK, así que nunca hay dos perfiles para la misma cuenta. La aplicación crea uno al registrar la cuenta, pero la base por sí sola no obliga a que toda cuenta tenga perfil. Esta diferencia entre regla del sistema y restricción SQL es una buena pregunta de sustentación.

Una cuenta puede tener muchas mediciones; cada medición pertenece a una cuenta. Un hábito puede tener muchas entradas; cada entrada corresponde a un usuario, un hábito y un día. `UNIQUE(user_id, habit_id, completed_on)` impide registrar dos veces ese mismo cumplimiento. La FK evita un hábito inexistente; la unicidad evita duplicar el cumplimiento: resuelven problemas diferentes.

Una rutina personal tiene muchos ejercicios. La cabecera conserva nombre, propietario y objetivo; el detalle conserva orden, series, repeticiones, duración y descanso. No se crean doce columnas para doce ejercicios. El límite de posiciones y su unicidad ordenan los detalles sin duplicar posiciones dentro de una rutina.

En el diagrama completo, cada caja es una tabla y cada flecha apunta desde la FK hija a la clave referenciada. PK significa clave primaria; FK, clave foránea; `?`, campo que admite NULL. Una flecha con dos nombres representa una sola FK compuesta, no dos relaciones independientes. El Mermaid editable expresa además cardinalidades: `||` exactamente uno, `o|` cero o uno y `o{` cero o muchos.

El esquema tiene 22 restricciones FK, aunque haya más columnas participantes: una FK compuesta cuenta como una restricción. El diagrama grande conserva todos los 148 campos; se entrega aparte en formato amplio para no comprimirlos de manera ilegible en una hoja A4.

## 8. Recorrido completo por las 17 entidades

**Identidad.** `users` conserva correo único, hash, rol global, estado y bloqueo. `user_profiles` separa información de presentación, experiencia personal/institucional, preferencias, fechas de consentimiento y personalización. No se repite el hash en perfiles ni mediciones.

**Seguimiento.** `health_measurements` guarda un historial: peso, altura, IMC calculado en ese momento, fecha y contexto de crecimiento si procede. Un nuevo registro no reemplaza el anterior. `bmi_snapshot` permite explicar el resultado histórico sin reinterpretarlo silenciosamente cuando cambia el perfil.

**Constancia.** `habits` es el catálogo común. `habit_entries` es la evidencia diaria. `user_goals` es una meta semanal por usuario y hábito. `daily_checkins` guarda energía y enfoque declarados, no XP. Separar catálogo, meta, acción y percepción evita mezclar conceptos distintos en una misma tabla.

**Instituciones.** `schools` conserva el catálogo verificado. `school_groups` distingue colegio, año académico y nombre de grupo. `school_memberships` conserva la solicitud de rol, aprobación, autorizaciones y preferencia de participación en agregados; un usuario tiene como máximo una vinculación en este modelo. `teacher_group_assignments` limita grupos de una vinculación docente. `school_enrollment_requests` guarda colegio y grupo escritos libremente antes de validarlos: esos textos no son permisos ni FK al catálogo.

**Movimiento.** `personal_routines` es la cabecera privada, con revisión para detectar ediciones concurrentes. `routine_exercises` es su detalle ordenado. `routine_completions` registra usuario, identificador textual de rutina, hábito relacionado y fecha. `routine_slug` **no tiene FK** a `personal_routines`: también identifica rutinas del catálogo de código. No debe dibujarse una relación física inexistente.

**Operación.** `announcements` almacena comunicados y su autor. `audit_events` guarda acciones técnicas con metadatos redactados; `entity_id` es texto lógico, no una FK polimórfica a todas las tablas. `metadata_redacted` es `json` en PostgreSQL, no `jsonb`. No debe convertirse en un depósito de datos médicos o contraseñas.

El anexo de diccionario explica los **148 campos**, los DEFAULT físicos, todas las restricciones e índices de cada entidad, sin omitir columnas que no se muestran en las pantallas.

## 9. Las relaciones más importantes, explicadas

La FK compuesta `(group_id, school_id)` de una membresía apunta a `(id, school_id)` de un grupo. Así una solicitud para el colegio 1 no puede asignarse al grupo 3 del colegio 2. La PK `id` ya identifica al grupo, pero la unicidad adicional del par permite que PostgreSQL compruebe esa pertenencia en una sola FK.

Las asignaciones docentes utilizan dos FK compuestas: membresía/colegio y grupo/colegio. La pertenencia al mismo colegio está comprobada en SQL. Que la membresía sea docente, esté aprobada y tenga autorización se comprueba además en backend: la FK por sí sola no comprueba el valor de `requested_role` ni de `status` en otra fila.

`CASCADE` elimina dependientes al borrar la fila referenciada, por ejemplo ejercicios al borrar su rutina. `RESTRICT` impide un borrado con referencias, por ejemplo un hábito usado por entradas. `SET NULL` conserva una fila y vacía su referencia opcional, por ejemplo el actor de una auditoría. Ninguna de estas acciones autoriza borrar usuarios reales en una sustentación.

La existencia de una FK no significa que cualquiera pueda leer el dato relacionado. Integridad y autorización son conceptos diferentes. Una unión SQL puede ser correcta y aun así ser inadecuada para mostrarla a un docente con datos reales.

## 10. Del formulario al registro PostgreSQL

Ejemplo: guardar una rutina propia. El navegador presenta un formulario Jinja y envía los datos. Flask comprueba sesión y CSRF; el backend valida propietario, objetivo, número de ejercicios, dosis y revisión. SQLAlchemy prepara operaciones parametrizadas dentro de una transacción. PostgreSQL verifica PK, FK, UNIQUE, CHECK y NOT NULL. Si todo es correcto se confirma la transacción; si algo falla se revierte. La página luego presenta el resultado sin exponer la contraseña del motor.

`app/models.py` declara el modelo Python. `migrations/versions` explica cómo evolucionó el esquema. Las rutas y servicios coordinan reglas y permisos. El servidor web usa su propio rol limitado; no usa el superusuario que administra PostgreSQL. El material de estudio no cambia este recorrido.

Los valores por defecto del ORM y del motor no son lo mismo. Si Python asigna `created_at`, el SQL manual también debe enviarlo cuando la columna SQL no tiene DEFAULT. El diccionario físico distingue ambos casos para evitar que una inserción de estudiante falle por una suposición incorrecta.

## 11. Primera práctica: leer sin modificar

Abrir `consultas_sustentacion.sql` y ejecutar cada consulta por separado. Primero confirmar base y usuario; después mostrar tablas, campos y restricciones. Explicar una unión antes de ejecutar la siguiente. No memorizar resultados sin comprender las columnas de enlace.

Con los datos iniciales: la cuenta 3 tiene dos mediciones, una rutina con dos ejercicios y tres entradas de hábitos que suman 35 XP. La cuenta 4 tiene una entrada que suma 10 XP. La cuenta 5 tiene una solicitud escrita pendiente, sin membresía aprobada. Son ejemplos inventados y sus fechas son fijas para que el resultado sea repetible.

Los puntos se calculan desde `habit_entries` y `habits.points`. No se suma de nuevo `routine_completions`, porque una rutina puede marcar ese mismo hábito. No existe una columna de saldo XP en `users`. La unicidad diaria es parte de la idempotencia y las transacciones del backend completan esa garantía.

La consulta de colegios muestra filas individuales SOLO porque esta copia es sintética. No es un reemplazo del panel docente anonimizado. Con dos estudiantes no se debe afirmar que se cumple el umbral de los reportes reales.

## 12. Segunda práctica: integridad y transacciones

Una transacción agrupa cambios: o se confirman juntos con COMMIT o se deshacen con ROLLBACK. Un fallo no debe dejar media rutina guardada. Un SAVEPOINT permite revertir una parte sin abandonar todo el trabajo; el script utiliza bloques de excepción PostgreSQL para demostrar errores esperados y continuar.

Ejecutar `practicas_transacciones.sql` como archivo completo en psql. En DBeaver retirar únicamente la línea `\set ON_ERROR_STOP on`, que pertenece a psql, y ejecutar el resto como script con la transacción explícita; no ejecutar COMMIT ni reconfigurar autocommit en la mitad.

La práctica inserta, lee, cambia y elimina una fila temporal; intenta un cumplimiento duplicado, un grupo ajeno a su colegio, cero series y borrar un hábito referenciado. Cada error esperado produce un aviso OK. Luego demuestra que el estudiante no puede alterar `public.users` ni crear roles, pero sí una tabla en su esquema personal. Finalmente prueba CASCADE de ejercicios y termina en ROLLBACK. Deben volver los dos ejercicios y no quedar la tabla temporal.

No escribir contraseñas ni medidas reales en ejercicios. No ejecutar estos archivos contra la base publicada. El archivo comprueba el nombre de base y aborta si el destino no es el de estudio. Para reiniciar toda la práctica, pedir al operador reconstruir SOLO esta instancia o restaurar su respaldo sintético; el estudiante no necesita permiso de destruir la base.

## 13. Estructura, migraciones, copias e índices

La exportación de estructura se obtiene con `pg_dump --schema-only --no-owner --no-acl`. No contiene registros ni roles originales y no es una copia de seguridad de los datos del sitio. Primero se restaura en una base VACÍA, luego se carga la semilla inventada y después se asignan permisos de estudio. No se importa sobre una base en uso.

`alembic_version` no describe cada tabla: indica la revisión vigente. Los archivos de migración explican cambios anteriores, desde el núcleo inicial hasta las 17 entidades actuales. El modelo Python expresa la estructura deseada y `flask db check` ayuda a detectar diferencias. Editar una migración histórica aplicada no actualiza de forma segura los servidores existentes.

Un backup completo incluye datos y estructura; una restauración ensayada verifica que realmente puede recuperarse. Para esta copia se puede hacer un respaldo sintético y restaurarlo en otra base de la MISMA instancia de estudio, comparar estructura y conteos y retirar solo esa base temporal. Eso no demuestra recuperación ante la pérdida total del VPS: para esa garantía hace falta una copia fuera del servidor y otro ensayo.

Los índices actuales figuran en el anexo. Una PK o UNIQUE suele tener su índice de apoyo. Un índice compuesto tiene orden: uno que empieza por `user_id` puede servir para un filtro de usuario. Con cinco usuarios inventados, un recorrido secuencial puede ser la mejor decisión. `EXPLAIN` describe el plan; no se afirma mejora de rendimiento sin medir antes y después con una carga representativa.

## 14. Guion para una sustentación de 15 minutos

| Minutos | Demostración | Qué explicar |
|---|---|---|
| 0-2 | Base y usuario con SELECT de identidad. | Por qué no es superusuario ni la base publicada. |
| 2-4 | Tablas y diagrama. | 17 entidades, 148 campos, 22 FK, más Alembic técnica. |
| 4-6 | Usuario, perfil y mediciones. | Uno a uno opcional en SQL y uno a muchos histórico. |
| 6-8 | Rutina con dos ejercicios. | Normalización de cabecera/detalle y orden único. |
| 8-10 | Colegio, grupo y membresía. | FK compuesta y diferencia entre solicitud y aprobación. |
| 10-12 | XP y duplicado rechazado. | SUM, UNIQUE, idempotencia y transacción. |
| 12-14 | Cambios reversibles y permisos denegados. | CHECK, CASCADE, RESTRICT, esquema personal y ROLLBACK. |
| 14-15 | Migración, respaldo y límites. | Cómo se mantiene y qué no se ha certificado. |

La evidencia que se comparte debe recortar resultados ficticios y estructura, nunca contraseñas, datos reales o llaves privadas. Una captura de DBeaver no prueba comprensión por sí sola: el estudiante debe predecir qué JOIN necesita y por qué una operación será rechazada.

## 15. Preguntas de estudio y respuestas guía

**¿Por qué PostgreSQL y no un archivo Excel?** Necesitamos relaciones verificables, transacciones y escrituras concurrentes con permisos. Excel puede apoyar análisis, pero no reemplaza el motor transaccional de la aplicación.

**¿Por qué hay perfil aparte de usuario?** Separar autenticación de presentación evita repetir credenciales y aclara responsabilidades. La PK/FK permite como máximo un perfil por cuenta.

**¿Para qué sirve una tabla intermedia?** Conserva una relación con datos propios. Una entrada de hábito une usuario y hábito, pero agrega un día; una asignación une membresía y grupo con un colegio coherente.

**¿Qué protege un CHECK y qué no?** Impide valores SQL fuera de un rango, pero no comprueba por sí solo identidad, diagnóstico médico, autorización docente ni consentimiento legal.

**¿Por qué el nombre del colegio no da permisos?** Un texto se puede escribir libremente; la vinculación del catálogo necesita revisión y comprobaciones. Una cadena no es una aprobación.

**¿Todo `_id` es FK?** No. `audit_events.entity_id` es texto lógico; debe inspeccionarse la restricción. `routine_slug` tampoco es FK a la tabla de rutinas personales.

**¿Por qué no usar el IMC como receta de ejercicio?** Es un indicador descriptivo; la aplicación orienta el movimiento por objetivo y preferencias. En menores se considera contexto de crecimiento y no se aplican directamente umbrales de adultos. Esta guía documenta datos y no da orientación clínica.

**¿Por qué el SQL manual pide fechas?** Muchos valores se asignan en Python y no tienen DEFAULT en PostgreSQL. La definición física del anexo es la referencia para una inserción manual.

**¿Qué significa tener acceso limitado?** Puede practicar sobre datos inventados, no administrar roles, otra base o el sitio. Ni GitHub ni DBeaver convierten esa cuenta en administrador del VPS.

**¿Por qué 18 tablas si el modelo dice 17?** Las 17 representan el negocio; `alembic_version` es técnica y no se cuenta como entidad de bienestar.

## 16. Mantenimiento y fuentes

Para actualizar este paquete: aplicar primero cambios de esquema mediante el flujo aprobado, volver a extraer SOLO catálogos y estructura, comparar con los modelos, regenerar diagrama/diccionario, ejecutar las prácticas en la copia y revisar visualmente los PDF. No sustituir catálogos por filas de producción. El JSON capturado corresponde al corte indicado, no se actualiza mágicamente cuando cambia el sitio.

El exportador `scripts/export_dba_study.py` funciona sin conexión usando el catálogo versionado. La opción `--collect` exige acceso de operador y solo lee metadatos; no debe habilitarse ese acceso administrativo al estudiante. El despliegue de estudio y sus secretos quedan separados de los de la web.

Fuentes primarias para ampliar el estudio:

- PostgreSQL 18, roles: https://www.postgresql.org/docs/18/sql-createrole.html
- PostgreSQL 18, permisos: https://www.postgresql.org/docs/18/sql-grant.html
- PostgreSQL 18, exportación: https://www.postgresql.org/docs/18/app-pgdump.html
- DBeaver, conexión SSH: https://dbeaver.com/docs/dbeaver/SSH-Configuration/
- DBeaver, diagramas: https://dbeaver.com/docs/dbeaver/ER-Diagrams/
- OpenSSH, restricciones del servidor: https://man.openbsd.org/sshd_config.5

Consultar [evidencia de preparación](VALIDACION.md) para distinguir lo ejecutado de lo pendiente. Esta guía se complementa con el [diccionario físico completo](diccionario_postgresql.md) y el manual integral del sistema del proyecto.
