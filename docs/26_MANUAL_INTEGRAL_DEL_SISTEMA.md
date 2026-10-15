# Manual integral de VitaliLab

## Propósito de este manual

Este documento explica cómo funciona VitaliLab y cómo mantenerlo sin poner en riesgo sus datos ni otros servicios del servidor. Está dirigido a estudiantes que están aprendiendo programación y a las personas que administran el proyecto. Puedes leerlo de principio a fin para estudiar, o consultar un capítulo durante una práctica.

La plataforma reúne bienestar personal y escolar. Permite organizar hábitos, metas, bitácora, mediciones y rutinas. La versión descrita incorpora personalización en dos pasos, colegios escritos manualmente y rutinas privadas creadas por el usuario. No es un servicio de diagnóstico ni un sistema que prescriba ejercicio a partir del IMC.

El código, las migraciones y las pruebas son las fuentes técnicas. Los resultados y la versión publicados deben consultarse en el informe de la entrega, no deducirse de que una función aparezca descrita aquí. Los documentos anteriores conservan cortes históricos de siete, nueve o catorce entidades; el modelo de esta edición tiene diecisiete tablas de negocio y una tabla de control de migraciones.

## Cómo estudiar el proyecto

Primero utiliza la aplicación con una cuenta de práctica local. Registra un hábito y observa qué cambia. Después identifica la ruta que recibe esa acción, el servicio que aplica la regla y la tabla que guarda el resultado. Este recorrido ayuda a relacionar una pantalla con el código sin intentar memorizar todas las carpetas.

En una segunda sesión completa el recorrido de medición y objetivo. En una tercera crea una rutina de dos ejercicios y comprueba que editarla no modifica los puntos anteriores. Deja las prácticas administrativas y de despliegue para cuando comprendas las diferencias entre una cuenta de aplicación, una cuenta de GitHub y una cuenta del servidor.

Para sustentar una decisión, explica cuatro cosas: qué problema resuelve, dónde está implementada, qué riesgo controla y cómo se comprueba. Por ejemplo: «La restricción diaria evita duplicar puntos; está en una clave única de la base y en el servicio de registro; se prueba enviando la misma acción dos veces».

## Qué significa cada componente

El frontend es la parte que presenta información y recibe acciones en el navegador. En este proyecto se construye con plantillas HTML, estilos CSS y pequeños módulos JavaScript. El backend es el programa que recibe peticiones, comprueba permisos y ejecuta reglas. Se implementa en Python con Flask. La base de datos conserva los registros entre reinicios. En el servidor se utiliza PostgreSQL.

Git guarda versiones del código. GitHub aloja el repositorio y ejecuta verificaciones automáticas. Docker empaqueta la aplicación y sus dependencias en una imagen. Un contenedor ejecuta esa imagen. Docker Compose describe cómo se conectan los contenedores del proyecto. El proxy Traefik recibe las conexiones HTTPS y las dirige a la aplicación correspondiente.

Un dominio es una dirección legible, como `vitalilab.space`. DNS indica a qué servidor corresponde esa dirección. El certificado TLS permite que el navegador compruebe el nombre del sitio y cifre la comunicación. Tener un dominio y un certificado no sustituye los permisos del backend ni una política de tratamiento de datos.

## Arquitectura general

VitaliLab es un monolito modular: existe una aplicación, dividida en módulos con responsabilidades distintas. Esta elección mantiene el despliegue y el aprendizaje manejables. Separarla en microservicios ahora introduciría más redes, credenciales y operaciones sin una necesidad medida que lo justifique.

El recorrido de una petición es navegador, proxy HTTPS, Gunicorn, aplicación Flask, servicio de negocio y PostgreSQL. La respuesta vuelve por el mismo camino. Las plantillas se generan en el servidor. JavaScript añade temporizadores y edición dinámica, pero no es la autoridad para conceder puntos ni permisos.

| Componente | Responsabilidad | Ubicación |
|---|---|---|
| Fábrica de aplicación | Crear Flask y registrar extensiones, módulos y cabeceras | `app/__init__.py` |
| Configuración | Leer variables externas y validar entornos | `app/config.py` |
| Formularios | Validar entradas y representar controles | `app/forms.py`, `app/school/forms.py`, `app/wellness/forms.py` |
| Modelos | Representar tablas y restricciones | `app/models.py` |
| Rutas | Recibir peticiones y devolver respuestas | `app/*/routes.py` |
| Servicios | Aplicar reglas de negocio | `app/services/` |
| Presentación | Construir pantallas y comportamiento del navegador | `app/templates/`, `app/static/` |
| Migraciones | Evolucionar el esquema de forma versionada | `migrations/versions/` |
| Verificación | Comprobar comportamiento, seguridad y operación | `tests/`, `scripts/`, `.github/workflows/ci.yml` |
| Infraestructura | Describir el servicio aislado en NexoStack | `deploy/nexostack/` |

La separación es práctica, no una declaración de Clean Architecture estricta: los servicios utilizan SQLAlchemy y conocen los modelos. No hay una capa de repositorios artificial que solo copie cada llamada del ORM. La regla importante es evitar que las plantillas calculen permisos y que los controladores concentren operaciones de negocio complejas.

## Estructura del repositorio

En la raíz están el punto de entrada `wsgi.py`, dependencias, Dockerfile, configuración de pruebas y documentación general. `app/auth` contiene acceso y recuperación; `app/profile` gestiona perfil, mediciones y personalización; `app/habits` registra hábitos; `app/wellness` contiene metas, bitácora y rutinas; `app/school` gestiona vinculaciones y panel docente; `app/admin` administra comunicados.

`app/services/measurements.py` conserva el cálculo de referencias de crecimiento. `personalization.py` organiza el acceso al recorrido y las mediciones. `personal_routines.py` guarda y archiva rutinas del propietario. `movement.py` conecta una actividad con el hábito diario. `school.py` controla permisos y agregados. `enrollment.py` recibe nombres libres y permite su revisión sin convertirlos automáticamente en membresías.

Las carpetas `.venv`, `instance`, `output` y los archivos de credenciales no forman parte de la entrega de código. `.gitignore` evita incluirlos por accidente, pero no es un sistema de cifrado: antes de un commit también hay que revisar la lista de archivos y sus cambios.

## Experiencias y permisos

| Persona | Puede hacer | No puede obtener por marcar una opción |
|---|---|---|
| Visitante | Consultar contenido y biblioteca general | Historial o rutinas privadas |
| Usuario personal | Gestionar sus hábitos, metas, bitácora, perfil y rutinas | Cuentas o datos de otras personas |
| Solicitante institucional | Escribir colegio, grupo y rol; ver su solicitud | Permisos de docente o pertenencia verificada |
| Estudiante aprobado | Completar su espacio y consultar su seguimiento | Mediciones de compañeros |
| Docente aprobado | Consultar grupos asignados y preparar actividades | Detalle individual del alumnado o grupos ajenos |
| Administrador de aplicación | Revisar solicitudes, catálogo, grupos, asignaciones y comunicados | Administración general del VPS por tener ese rol |
| Operador de VitaliLab | Estado, salud, respaldo y reinicio de su servicio autorizado | Gestionar Mercanta, Murano, Krono57 u otras bases |

Hay dos conceptos diferentes: `users.role` es el rol global, usuario o administrador. `school_memberships.requested_role` describe estudiante o docente dentro de un colegio. Un docente no se convierte en administrador global. Escribir «Docente» en el formulario crea una solicitud, no una autorización.

## Recorrido del usuario personal

Después del registro, el usuario puede empezar con hábitos sin introducir medidas corporales. Si desea completar su espacio de rutinas, abre «Personalizar mi espacio». El primer paso solicita peso y altura con sus unidades y una confirmación explícita para guardarlos. La fecha de nacimiento ayuda a contextualizar el dato. La referencia de crecimiento se mantiene opcional.

Al guardar se muestra el IMC calculado. En el segundo paso se elige postura y estabilidad, energía y movimiento, o fuerza y tonificación. También se indica si se prefieren alternativas sentadas, con apoyo, de pie o adaptables. Al completar el paso se registra la fecha de finalización y se abre la biblioteca filtrada.

El recorrido no vuelve a exigir mediciones en cada ingreso. Cambiar el objetivo no crea una medición nueva. Actualizar la medición conserva las anteriores. Registrar exactamente los mismos valores y contexto en el mismo día no agrega otra fila desde este flujo.

## Recorrido escolar y autorizaciones

La persona escribe manualmente colegio y grupo o área, y solicita un rol. El formulario no obliga a escoger entre los dos colegios iniciales. Esa información se guarda en `school_enrollment_requests`, separada de las membresías verificadas. No se crea un colegio público ni un grupo autorizado con cada texto recibido.

La administración revisa identidad, pertenencia y autorizaciones mediante el procedimiento institucional. Si el colegio o el grupo verificado no existe, lo registra desde Administración escolar. Después relaciona la solicitud con ese catálogo y decide. Para un estudiante debe elegir un grupo activo del mismo colegio. Para un docente, aprobar la identidad no asigna grupos: esa acción se realiza por separado.

Al iniciar sesión, un estudiante que aún no haya completado la personalización es dirigido a ese recorrido. Antes de guardar mediciones escolares debe existir una vinculación aprobada con revisión y autorización registradas. La fecha de nacimiento es necesaria en ese recorrido estudiantil. La aplicación no inventa autorizaciones ni las deduce de escribir un correo o colegio.

Si la revisión está pendiente, se explica el motivo y se ofrecen hábitos y rutinas generales. No se obliga a revelar mediciones para utilizar todas las funciones básicas. El consentimiento para estadísticas es otra decisión, está apagado inicialmente y puede retirarse. La aprobación de una membresía nunca lo activa por defecto.

## Rutinas guiadas y rutinas propias

La biblioteca contiene quince rutinas guiadas. Nueve propuestas de movimiento se distribuyen entre tres objetivos; las demás ayudan a organizar pausas, calma, descanso y enfoque. Las preferencias de movimiento filtran alternativas generales. Este filtro no es una evaluación clínica de capacidad ni una garantía de que un ejercicio sea adecuado para una persona concreta.

Cada rutina guiada tiene un identificador estable, descripción, pasos, duración orientativa, hábito asociado y referencia visual. Los pasos se leen antes de comenzar. El temporizador utiliza una hora de finalización para reducir el desfase cuando el navegador ralentiza una pestaña. Al terminar no registra automáticamente una actividad: el usuario decide si realmente la completó.

Las rutinas propias admiten nombre, descripción y objetivo. Cada una contiene hasta doce ejercicios ordenados. Se escribe el nombre del ejercicio y se indican series, repeticiones, segundos, descanso e instrucciones. Se puede usar repeticiones, duración o ambas. La guía visual se elige únicamente si corresponde al ejercicio; una actividad libre no recibe una demostración inventada.

El límite de treinta rutinas activas por persona acota la lista y el consumo de recursos. Puede archivarse una para crear otra. Archivar no elimina sus cumplimientos ni resta puntos. La revisión de edición evita que una ventana antigua sobrescriba cambios guardados desde otra. Si aparece el aviso de conflicto, hay que recargar y volver a revisar la información antes de guardar.

Los números máximos permitidos por el formulario son límites técnicos, no recomendaciones deportivas. El sistema no indica que una plancha de dos minutos o cinco series de abdominales sean adecuadas por tener cierto IMC. En menores, el adulto responsable debe revisar edad, capacidad y actividad; si se necesita una pauta individual, corresponde a personal cualificado.

## Cómo se calcula y presenta el IMC

El cálculo divide el peso en kilogramos por la altura en metros elevada al cuadrado. Por ejemplo, 70 kg y 175 cm corresponden a aproximadamente 22,86. Primero se transforma 175 cm a 1,75 m; después se divide 70 entre el cuadrado de 1,75. Confundir centímetros y metros produce un error importante, por eso la interfaz muestra las unidades y el servidor valida la combinación.

`health_measurements.bmi_snapshot` guarda el resultado de ese momento. También se conservan, si existen, edad en meses, referencia utilizada y percentil. No se recalculan las mediciones antiguas porque alguien corrija después su perfil: un registro histórico debe seguir representando el contexto en el que se guardó.

La referencia implementada es OMS 2007 mediante una tabla LMS local de 336 registros, con procedencia y huellas documentadas en `app/data/README.md`. Cubre las referencias incluidas entre 61 y 228 meses. No se extrapolan resultados fuera de los límites definidos por el código. Si falta información, no se aplica un criterio adulto como sustituto de una referencia infantil.

La gráfica personal reúne los registros del año solicitado y ofrece una tabla legible. La curva usa el último registro por día para no superponer puntos del mismo día; la tabla conserva el detalle. El usuario consulta exclusivamente su propio historial. No hay una clasificación pública por peso, IMC o percentil.

El CDC explica que el IMC infantil debe contextualizarse por edad y sexo y que no es un diagnóstico ni una fuente de orientación clínica individual. Esa precaución no significa que VitaliLab use las curvas del CDC: el cálculo de percentiles de este proyecto utiliza la referencia OMS descrita anteriormente.

Fuente de contexto: https://www.cdc.gov/bmi/child-teen-calculator/calculator.html

Orientación general sobre actividad por edad: https://www.cdc.gov/physical-activity-basics/guidelines/children.html

## Modelo relacional y decisiones de DBA

PostgreSQL guarda relaciones entre cuentas, registros y colegios. La carga principal es transaccional: muchas acciones pequeñas sobre los datos del usuario. Se utiliza un modelo relacional porque requiere integridad, relaciones verificables y operaciones atómicas. No se cambia de motor para añadir rutinas ni se introduce una segunda base innecesaria.

| Tabla | Qué representa | Relación principal |
|---|---|---|
| `users` | Identidad, acceso y estado de la cuenta | Una cuenta por correo |
| `user_profiles` | Datos visibles, contexto y preferencias | Un perfil por cuenta |
| `health_measurements` | Mediciones históricas y contexto del cálculo | Muchas mediciones por cuenta |
| `habits` | Catálogo de hábitos y puntos | Un hábito tiene muchos registros |
| `habit_entries` | Cumplimientos por día | Usuario, hábito y fecha únicos |
| `announcements` | Comunicados y publicación | Autor administrador |
| `audit_events` | Acciones relevantes sin copiar datos sensibles | Actor y entidad |
| `user_goals` | Metas de frecuencia de un hábito | Usuario y hábito únicos |
| `daily_checkins` | Energía y enfoque declarados | Una bitácora por usuario y fecha |
| `schools` | Colegios gestionados por la administración | Colegio con muchos grupos |
| `school_groups` | Grupo dentro de colegio y año | Grupo pertenece a un colegio |
| `school_memberships` | Vinculación revisada y autorizaciones | Una membresía actual por cuenta |
| `teacher_group_assignments` | Grupos asignados a docentes | Una asignación por docente y grupo |
| `routine_completions` | Rutinas registradas cada día | Usuario, rutina y fecha únicos |
| `school_enrollment_requests` | Colegio y grupo escritos sin verificar | Una solicitud actual por cuenta |
| `personal_routines` | Cabecera privada y revisión de edición | Muchas rutinas por propietario |
| `routine_exercises` | Ejercicios ordenados de una rutina propia | Muchas filas por rutina |

La normalización evita repetir datos sin necesidad. Por ejemplo, un cumplimiento apunta al hábito en vez de duplicar todo su nombre, descripción y configuración. En cambio, el IMC histórico se conserva deliberadamente como instantánea para no reinterpretar el pasado. Son decisiones distintas justificadas por el uso del dato.

Una clave primaria identifica una fila. Una clave foránea exige que el registro relacionado exista. Una clave única impide duplicados según una regla del negocio. Un `CHECK` limita valores aceptables aunque una entrada llegue directamente a la base. Un índice ayuda a encontrar filas, pero también cuesta espacio y trabajo en las escrituras; no se crea para cada columna por rutina.

Las claves compuestas escolares obligan a que grupo y membresía pertenezcan al mismo colegio. Un identificador de grupo válido de otro colegio sigue siendo inválido para esa membresía. Esta protección existe en la base y en el servicio. Las nuevas solicitudes manuales no alteran esas claves ni convierten texto libre en un identificador autorizado.

La rutina personal se separa de sus ejercicios porque puede contener varios, cada uno con sus propios tiempos. `position` conserva el orden y es única dentro de la rutina. El rango de posición admite doce filas. La restricción de dosis exige repeticiones o duración; no permite guardar un ejercicio vacío. `revision` permite detectar ediciones desactualizadas.

`routine_completions.routine_slug` utiliza identificadores del catálogo y el formato interno `personal-ID` para rutinas propias. No es una clave foránea a un único catálogo porque hay dos orígenes. Antes de registrar una rutina propia, el servicio comprueba su propietario y que esté activa. Los registros se conservan al archivar para mantener la bitácora y los puntos.

## Puntos y transacciones

Completar una rutina crea un cumplimiento de rutina y trata de registrar el hábito asociado. Ambas operaciones pertenecen a una transacción. Si el mismo hábito ya está registrado ese día, se conserva el nuevo cumplimiento de rutina, pero no se conceden otros puntos. Las rutinas de movimiento propias y guiadas comparten el hábito de movimiento.

La primera protección es una clave única por usuario, rutina y fecha. La segunda es otra clave única por usuario, hábito y fecha. Así se cubren tanto el doble clic sobre la misma rutina como dos rutinas diferentes que utilizan el mismo hábito. Un botón deshabilitado ayuda a la experiencia, pero no sustituye esas reglas del servidor.

SQLAlchemy utiliza transacciones anidadas para manejar el intento de insertar un duplicado esperado sin descartar la actividad válida. Las pruebas de PostgreSQL envían dos solicitudes simultáneas para verificar el comportamiento real de las restricciones. La prueba de SQLite es útil para lógica y formularios, pero por sí sola no demuestra la concurrencia del motor publicado.

La fecha diaria se calcula con la zona del perfil, con alternativa a `America/Bogota`. Los tiempos de auditoría y revisión se guardan siguiendo la convención UTC. Distinguir la fecha del hábito del instante de auditoría evita asignar el mismo día según el reloj local de cada equipo.

## Backend paso a paso

Para estudiar una operación empieza por su ruta. El decorador de ruta relaciona una dirección y un método HTTP con una función. `GET` consulta; `POST` envía una acción. `login_required` exige sesión y `admin_required` comprueba el rol global. Los formularios validan el contenido recibido antes de llamar al servicio.

El servicio comprueba reglas que no deben depender de la pantalla. Por ejemplo, `owned_routine` filtra por identificador, propietario y estado activo. Si un usuario modifica la dirección para pedir la rutina de otra persona, no obtiene el objeto. El servidor responde 404, sin revelar si esa rutina existe para otra cuenta.

En una modificación de rutina se bloquea la fila en PostgreSQL y se compara la revisión enviada con la vigente. Si no coinciden, se devuelve un conflicto y no se reemplaza la versión nueva. Al crear se serializa el control del cupo por propietario para que dos ventanas no superen el límite mediante una carrera.

Los errores de negocio se convierten en mensajes comprensibles. Una petición sin CSRF se rechaza. Un objeto ajeno devuelve 404; un área administrativa sin permiso, 403. Los errores inesperados tienen página general y registro técnico, sin enseñar secretos ni trazas del servidor al visitante.

## Frontend paso a paso

`base.html` comparte navegación, estilos, mensajes y pie de página. Las pantallas extienden esa base para no duplicar toda la estructura. Las macros de formularios colocan etiqueta, control, ayuda y errores de forma consistente. La ayuda y los errores se relacionan con el control para que también puedan entenderse con tecnologías de asistencia.

CSS usa rejillas flexibles y columnas que permiten encogerse sin desbordar. Los números de ejercicios se presentan en bloques separados con etiquetas, no superpuestos sobre una ilustración. Las imágenes reservan ancho y alto para reducir saltos de contenido. En móvil se usa una sola columna para ejercicios y los controles mantienen espacio táctil.

`personalization.js` añade o quita ejercicios del formulario y renumera los campos antes del envío. No decide qué datos se guardan: el servidor vuelve a validarlos. El botón para añadir otra fila también funciona sin JavaScript mediante un envío que vuelve a mostrar el formulario, sin crear la rutina.

Las demostraciones son SVG propios alojados con el sitio. No descargan imágenes de usuarios ni ejecutan código externo. Una figura de detalle tiene descripción alternativa y texto de apoyo. La ilustración es esquemática: no acredita una técnica clínica ni debe asociarse a un ejercicio que el usuario escribió si no corresponde.

## Seguridad y privacidad

Las contraseñas se guardan mediante hash scrypt, no en texto legible. El acceso utiliza sesiones de Flask con cookies configuradas como HttpOnly y SameSite Lax; en HTTPS se activa Secure. El servicio no se convierte en un sistema JWT por añadir perfiles escolares: cambiar de mecanismo sin necesidad introduciría riesgo y complejidad.

Los formularios que modifican datos requieren un token CSRF. El servidor valida números, longitudes, opciones y propiedad. Las plantillas escapan el texto del usuario para evitar que un nombre de rutina se interprete como HTML ejecutable. La política de contenido restringe scripts, estilos e imágenes a los orígenes previstos.

La auditoría registra acción, actor, entidad y metadatos mínimos. No copia peso, altura, contraseñas ni instrucciones privadas completas. Es útil para rastrear una aprobación, pero no es una prueba de que exista una autorización jurídica válida: la institución conserva y verifica sus soportes mediante su procedimiento.

El panel docente consulta solamente grupos asignados. Cada indicador mensual requiere un mínimo de diez participantes elegibles y se aplica supresión y redondeo. No se revelan conteos pequeños ni mediciones individuales. Los registros anteriores a la aprobación y al consentimiento para estadísticas no se incorporan retroactivamente. Estas medidas reducen riesgo de identificación, sin prometer anonimato absoluto.

El servicio sigue necesitando responsables humanos: definir tratamiento de datos, retención, atención de solicitudes, autorizaciones y revisión de actividades. Una mejora visual o una prueba automática no certifica cumplimiento legal ni seguridad clínica. No hay que introducir datos reales de menores para practicar las pruebas de este manual.

## Versiones de base de datos

| Revisión | Propósito |
|---|---|
| `0380d5595f5e` | Esquema profesional inicial |
| `208469fd48ef` | Índices de rutas de consulta |
| `54e1c8bb7901` | Metas personales y bitácora |
| `7ca6e014b982` | Enfoques personal e institucional |
| `a903b5d7e214` | Colegios, permisos, referencias y registro de rutinas |
| `c842d6e190ab` | Personalización, solicitudes manuales y rutinas privadas |

Una migración es un cambio de estructura versionado, no una copia de la base. La sexta revisión añade campos y tablas. No convierte consentimientos antiguos en nuevos, no modifica el historial de medidas y no borra membresías. Se comprueba que el esquema final coincide con los modelos.

En una base de práctica puede ensayarse un downgrade para comprender la reversión de estructura. En el servicio real, eliminar tablas nuevas destruiría información. El rollback previsto para esta entrega consiste en volver al código compatible anterior y conservar el esquema añadido, después de un respaldo. No se restaura una copia encima de la base en uso para «probar».

## Preparar el entorno local

Necesitas Git y Python compatible con el proyecto. Clona el repositorio con la cuenta autorizada. No pidas ni pegues contraseñas en el chat o en archivos del repositorio. Si el repositorio es privado, el gestor de credenciales o una llave debe resolver el acceso. Comprueba la visibilidad real en GitHub; no la deduzcas del nombre del proyecto.

En PowerShell, dentro de la copia local, crea el entorno de dependencias y ejecútalo con su ruta explícita:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m flask --app wsgi:app db upgrade
.\.venv\Scripts\python.exe -m flask --app wsgi:app seed-habits
.\.venv\Scripts\python.exe -m flask --app wsgi:app run
```

La configuración de desarrollo usa SQLite si no se proporciona una conexión. Es útil para aprender y ejecutar pruebas. Para comprobar el comportamiento publicado se utiliza PostgreSQL en CI. Staging y producción rechazan SQLite en la validación de arranque. No copies el archivo de secretos del servidor al equipo de un estudiante.

El servidor de desarrollo escucha localmente y no es Gunicorn. No expongas ese proceso como publicación real. La instancia del VPS se ejecuta con la imagen Docker, un proceso Gunicorn y la configuración de red específica del despliegue.

## Trabajo profesional con Git y GitHub

El repositorio es `juandigira17111980/vitalilab-profesional`. La rama `main` original se mantiene separada del trabajo publicado en NexoStack; el flujo existente integra en `staging`. Un nombre de rama no demuestra que un servicio sea un entorno de pruebas: hay que comprobar qué URL y base utiliza realmente.

Para una mejora se crea una rama de funcionalidad desde la integración vigente. Se revisa el diff, se ejecutan pruebas y se realizan commits con propósito claro. Después se abre un pull request hacia `staging`. GitHub ejecuta CI; si falla, se corrige antes de integrar. El despliegue utiliza el SHA completo verificado, no «lo último que haya en una carpeta».

```powershell
git status --short --branch
git switch staging
git pull --ff-only origin staging
git switch -c feat/mi-mejora
# Editar y comprobar la mejora antes de continuar
git diff
git add app tests docs
git commit -m "feat(rutinas): describe la mejora concreta"
git push -u origin feat/mi-mejora
```

No utilices ese ejemplo para incluir todos los archivos sin revisarlos: `git add` debe apuntar únicamente a los cambios que entiendes. Nunca uses un push forzado en una rama compartida para resolver una discrepancia que todavía no has investigado. La revisión de otra persona es recomendable; una comprobación automática no debe presentarse como aprobación humana.

La visibilidad pública permite leer el código a cualquier persona. No permite iniciar sesión como usuario ni acceder a la base, pero exige especial cuidado con documentación y credenciales. Cambiar la visibilidad requiere una decisión del propietario. La entrega técnica no debe publicar tokens, cadenas de conexión reales ni exportaciones de datos.

## Qué comprueba la integración continua

El flujo tiene tres trabajos: calidad, PostgreSQL y construcción del contenedor. Calidad ejecuta Ruff, comprobación de formato, Bandit, pytest y revisión de vulnerabilidades de dependencias. No equivale a un pentest, pero detecta errores que no deberían llegar al servidor.

PostgreSQL se inicia en una base descartable. Se aplica la revisión anterior, se crea una pequeña muestra de datos antiguos y se actualiza a la nueva revisión. Después se comprueban conservación, restricciones escolares, registros concurrentes de rutinas guiadas y propias, y ausencia de diferencias entre esquema y modelos.

La verificación de respaldo crea un dump, lo restaura en otra base de CI y compara conteos de las diecisiete entidades. Un `db check` en la restauración comprueba el esquema. Esto demuestra ese procedimiento y ese conjunto de datos; no es una simulación de pérdida de todo el VPS ni una garantía de tiempo de recuperación para cualquier volumen.

El trabajo Docker confirma que la imagen puede construirse. Publicar exige además comprobar configuración, permisos mínimos, respaldo previo, migración y salud del servicio real. No hay que confundir que CI esté verde con que el despliegue se haya realizado.

## Infraestructura de NexoStack

La aplicación tiene su propia carpeta `/opt/labs/vitalilab`, su proyecto Compose `vitalilab-lab`, una web y una PostgreSQL específicas. La web utiliza el usuario no root 10001, raíz de solo lectura, límites de memoria y CPU y un sistema de archivos temporal acotado. No monta el socket Docker.

La base no publica el puerto 5432 en Internet. Está en una red interna y usa TLS con validación del certificado. El usuario de aplicación tiene permisos para leer y modificar las tablas previstas, pero no es el propietario de migración ni un superusuario. El volumen conserva los datos aunque se sustituya la web.

Solo la web se conecta a la red de entrada que utiliza Traefik. No se reinicia el proxy para publicar una versión de VitaliLab y no se utilizan las bases de otros proyectos. Compartir el VPS y el proxy no ofrece aislamiento físico: por eso hay límites y se verifica que los contenedores ajenos no cambien.

Los nombres que incluyen `lab` y la variable histórica `APP_ENV=staging` identifican el montaje existente. No se renombran contenedores ni bases solo para retirar un aviso visual: hacerlo podría afectar volúmenes, comandos y respaldos. La página puede tener una presentación profesional sin ocultar en la documentación cómo está configurada realmente.

## Dominio de Hostinger y HTTPS

El dominio principal `vitalilab.space`, su variante `www` y `vitalilab.lab.nexostack.app` apuntan al mismo servicio de NexoStack. No son tres copias independientes y no importan las cuentas de Render. El servicio original de Render se conserva separado.

La configuración DNS esperada utiliza CNAME `www` hacia `vitalilab.lab.nexostack.app` y ALIAS con nombre `@` hacia ese mismo destino. No debe ponerse el dominio de NexoStack en el campo de nombre del ALIAS: `@` representa la raíz del dominio comprado. Los servidores DNS de Hostinger permanecen sin cambios.

Antes de emitir un certificado se comprueba la resolución pública y la ausencia de destinos incompatibles. Las reglas Traefik de estos nombres apuntan a la web de VitaliLab. Se verifica el certificado con validación de nombre y cadena, no desactivando la seguridad del cliente. La configuración de DNS y HTTPS se amplía en la guía 24.

## Desplegar sin afectar otros proyectos

Solo el administrador de infraestructura autorizado realiza este procedimiento. Primero registra el SHA vigente, la revisión de migración, el estado de salud y las identidades de los contenedores. Confirma espacio y memoria disponibles. Genera el archivo de un commit comprobado y verifica su integridad antes de extraerlo como una nueva carpeta de release.

El script fija rutas y proyecto Compose. Construye la imagen de VitaliLab, crea un respaldo y ejecuta la migración con la cuenta propietaria. Concede los permisos necesarios a la cuenta de aplicación y sustituye únicamente la web. La base existente y los servicios ajenos no deben recrearse por un cambio de pantalla.

`deploy/nexostack/deploy.sh` comprueba que PostgreSQL pertenece al proyecto previsto, está sano y usa la imagen esperada. Si ya existe, no ejecuta una recreación de la base. Esto evita que la ruta del archivo de inicialización, distinta en cada release, provoque un reinicio innecesario. Un cambio de configuración de PostgreSQL requiere una operación planificada aparte. Si HTTPS del dominio principal ya está activo y falla la comprobación DNS, el script se detiene: no retira silenciosamente el certificado configurado.

Después se comprueban `/health`, `/ready`, versión, HTTPS, acceso, permisos y una actividad con cuenta de verificación. Se comparan los contenedores ajenos con el registro previo. La evidencia debe indicar qué se probó, con qué cuenta de prueba y sin incluir datos personales ni credenciales.

Si falla una comprobación, no se sigue promoviendo a ciegas. Se revisa el error y se vuelve al código compatible anterior si corresponde, conservando la base y el respaldo. Nunca se ejecuta `docker compose down -v`, una limpieza global de Docker, un reinicio del proxy compartido o una migración de otro proyecto para arreglar VitaliLab.

Para esta migración aditiva, `deploy/nexostack/rollback-web.sh` recibe el SHA completo de una imagen anterior ya construida. Tras verificar compatibilidad y generar un respaldo, cambia solo la web, sin ejecutar migraciones ni recrear PostgreSQL. Se ejecuta el ayudante nuevo con el SHA anterior; no el antiguo script de despliegue, que desconoce la sexta revisión de esquema. Las carpetas e imágenes necesarias para la reversión se conservan. Este mecanismo no autoriza volver a cualquier versión arbitraria.

## Operación y accesos individuales

Las cuentas de aplicación de Juan y Emanuel son individuales; no debe compartirse una contraseña principal. Un administrador de aplicación puede gestionar comunicados y vinculaciones. No recibe por ello una consola del servidor ni acceso libre a tablas de estudiantes.

Los operadores de infraestructura tienen un acceso separado y restringido a acciones de VitaliLab: estado, salud, reinicio de su web, respaldo y resumen de eventos. No pertenecen al grupo Docker ni pueden elegir otro contenedor. Una llave privada es un secreto y nunca debe incluirse en este documento.

El sistema tiene un respaldo diario y un monitor periódico de disponibilidad. El monitor registra fallos en el servidor; eso no demuestra que se envíen avisos externos a una persona. La copia local tiene retención de catorce días. Para recuperar ante pérdida del VPS hace falta una copia fuera de ese servidor y un procedimiento probado.

SMTP, alertas externas, responsable del tratamiento y validación institucional son tareas de operación que necesitan configuración y evidencia. No se presentan como resueltas por retirar mensajes académicos. Antes de incorporar alumnado real, el responsable debe comprobarlas y registrar la decisión de uso con sus condiciones.

## Prácticas para aprender sin riesgo

Práctica de hábitos: utiliza dos cuentas locales. Registra el mismo hábito dos veces con una cuenta y comprueba que la otra conserva cero registros. Explica por qué un campo oculto con el identificador de otra persona no debe cambiar el propietario.

Práctica de personalización: intenta abrir el paso de objetivo antes de guardar la medición. Comprueba que el servidor vuelve al paso anterior. Completa el recorrido y vuelve a ingresar; verifica que no se crea otra medición por iniciar sesión. Prueba una entrada sin altura, otra sin consentimiento y una combinación de unidades errónea.

Práctica de rutinas: crea dos ejercicios, guarda y abre dos ventanas de edición. Guarda una y después intenta guardar la otra con la revisión antigua. Explica por qué se produce un conflicto. Registra la rutina, completa otra de movimiento y comprueba que no se duplican puntos. Archiva la primera y revisa que se conserva la puntuación.

Práctica escolar: solicita un colegio escrito que todavía no existe. Comprueba que no puedes acceder al panel docente. Con la cuenta administradora local crea el catálogo verificado y revisa la solicitud. Asigna un grupo al docente; intenta acceder a un grupo ajeno y explica por qué debe rechazarse.

Práctica de datos: en una base descartable aplica las migraciones, inspecciona claves e índices y ejecuta las pruebas. Nunca practiques borrados, restauraciones o consultas exploratorias de información personal sobre la base publicada.

## Preguntas para la sustentación

¿Por qué existe una tabla de solicitudes además de membresías? Porque un nombre escrito no acredita identidad ni autorización. ¿Por qué los ejercicios están en otra tabla? Porque una rutina contiene varias filas ordenadas y cada una tiene sus propios valores. ¿Por qué un botón deshabilitado no evita duplicados por sí solo? Porque se puede enviar otra petición fuera de la interfaz.

¿Por qué no se eligen abdominales según IMC? Porque ese dato no determina capacidad ni una pauta individual, especialmente en menores. ¿Por qué se guarda la referencia en la medición? Para conservar el contexto histórico. ¿Por qué el docente ve agregados y no fichas individuales? Para limitar exposición y respetar el propósito definido.

¿Qué diferencia hay entre una copia de seguridad y alta disponibilidad? Una copia permite recuperar datos; alta disponibilidad mantiene o restablece servicio con otra instancia. Este montaje no se declara un clúster de alta disponibilidad. ¿Qué prueba que una versión está publicada? La correspondencia entre commit verificado, configuración, `/health`, pruebas del sitio y registro de despliegue.

## Cómo seguir ampliando el sistema

Empieza por una necesidad y un criterio de aceptación comprobable. Si se añade compartir rutinas con clases, no basta con hacer pública la tabla actual: haría falta diseñar permisos, consentimiento, revisión de contenido y aislamiento por colegio. Si se ofrece venta SaaS, se deben definir responsables, soporte, recuperación, contratación y observabilidad antes de prometer un nivel de servicio.

Antes de optimizar una consulta mide el problema. Antes de aumentar capacidad ejecuta una prueba de carga comparable y registra latencias y errores. Antes de afirmar accesibilidad completa realiza una evaluación con personas y tecnologías de asistencia. Las pruebas automáticas y este manual sirven para construir evidencia, no para sustituir esas verificaciones.

El siguiente responsable debe encontrar un sistema comprensible: código versionado, decisiones explicadas, datos protegidos, un procedimiento para publicar y una manera de volver atrás. Esa es la base para aprender, sustentar y mantener VitaliLab.
