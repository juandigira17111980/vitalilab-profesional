# VitaliLab explicado desde cero

Manual de aprendizaje, instalación, programación y sustentación. Edición del 13 de octubre de 2026.

Vas a aprender cómo funciona VitaliLab siguiendo el viaje de una acción sencilla: una persona entra, crea su cuenta y registra un hábito. Ese recorrido conecta la pantalla, el código del servidor y la base de datos. Al final podrás instalar la aplicación, explicar su estructura, hacer un cambio pequeño, comprobarlo y demostrar qué sucede con los datos.

Este material empieza con fundamentos y llega a decisiones de diseño y operación. La experiencia se construye con las prácticas: leer un documento no convierte a alguien en experto. Tu objetivo inicial es comprender, ejecutar y explicar el proyecto con tus propias palabras.

La aplicación mejorada está en el repositorio privado `juandigira17111980/vitalilab-profesional`. La rama `staging` reúne la reconstrucción; `main` conserva la versión anterior. La copia académica se publica en `https://vitalilab.lab.nexostack.app`, con PostgreSQL propia y accesos individuales de gestión. La web histórica de Render no se reemplaza. Estudia esta edición y consulta su registro de pruebas antes de afirmar qué está validado; una demostración de laboratorio no equivale a una aprobación de producción.

## 1 Cómo estudiar y comprobar que entendiste

Estudia en este orden. No necesitas aprender todas las herramientas el primer día.

| Etapa | Qué aprenderás | Evidencia que debes producir |
|---|---|---|
| Fundamentos | Archivos, Python, navegador y servidor | Explicar el viaje de una petición |
| Montaje local | Descargar, instalar y arrancar | Abrir la página en tu equipo |
| Datos | Tablas, relaciones e integridad | Dibujar las siete entidades |
| Backend | Rutas, formularios y servicios | Seguir un registro de hábito en el código |
| Frontend | HTML, Jinja, CSS y JavaScript | Cambiar un texto y mostrar el resultado |
| Calidad | Pruebas, errores y control de versiones | Ejecutar una prueba y explicar su resultado |
| Publicación | NexoStack Docker y configuración | Completar una lista de verificación del despliegue |
| Sustentación | Demostración y preguntas | Exponer un caso de extremo a extremo |

Puedes repartirlo en ocho sesiones de 60 a 90 minutos, más tiempo de práctica. Si una sesión no alcanza, continúa al día siguiente. El criterio para avanzar es poder repetir el ejercicio y explicar el resultado, no cumplir un tiempo exacto.

Prepara una bitácora personal con cuatro apartados: qué intenté, qué ocurrió, cómo comprobé el resultado y qué todavía no entiendo. Guarda capturas de datos ficticios. Si aparece un error, copia su mensaje sin contraseñas ni direcciones de conexión y anota el comando que lo produjo.

Trabaja con un compañero. Una persona ejecuta y otra explica. Después intercambian roles. Si solo uno sabe hacer la demostración, el equipo todavía no está listo para sustentar.

## 2 Los conceptos que necesitas antes de abrir el proyecto

### 2.1 Archivo carpeta y ruta

Un archivo guarda contenido, como instrucciones de Python o estilos CSS. Una carpeta agrupa archivos. Una ruta indica dónde está algo. `app/models.py` significa que el archivo `models.py` está dentro de la carpeta `app`.

El archivo terminado en `.py` contiene Python; `.html` describe una pantalla; `.css` define su presentación; `.js` añade comportamiento en el navegador; `.md` es documentación en texto; `.yaml` y `.json` suelen contener configuración estructurada.

La carpeta raíz es la que contiene `README.md`, `requirements.txt` y `wsgi.py`. Muchos comandos deben ejecutarse desde allí. Si estás en la carpeta equivocada, la herramienta puede decir que no encuentra un archivo aunque ese archivo sí exista.

### 2.2 Código intérprete y terminal

El código fuente es el texto que escribimos para indicar qué debe hacer un programa. Python es el lenguaje de este backend. El intérprete de Python ejecuta sus instrucciones.

La terminal permite escribir órdenes. En Windows usaremos PowerShell. Una orden se ejecuta al presionar Enter. No copies el símbolo de la terminal ni las salidas esperadas como si fueran comandos.

Una variable da un nombre a un valor. Una condición decide según un resultado. Una función reúne instrucciones que podemos llamar. Una clase describe un tipo de objeto y sus capacidades. En este proyecto una clase puede representar un usuario o un formulario.

```python
def nivel_basico(puntos):
    if puntos >= 100:
        return "Explorador"
    return "Semilla"
```

Este ejemplo didáctico no reemplaza el código de VitaliLab. `def` crea la función; `puntos` es su entrada; `if` compara; `return` devuelve el resultado. La sangría agrupa instrucciones: Python no la considera decorativa. Con 120 devuelve Explorador y con 20 devuelve Semilla. El proyecto real utiliza cuatro niveles en `app/services/progress.py`.

### 2.3 Navegador frontend backend y base de datos

El navegador es el programa con el que abres la web. El frontend es lo que presenta y permite interactuar: textos, formularios, botones y menús. El backend recibe solicitudes, valida datos, aplica reglas y prepara respuestas. La base de datos conserva información entre solicitudes.

Piensa en un registro de hábito. El botón pertenece al frontend. La comprobación de quién está conectado pertenece al backend. El registro de que ese usuario completó ese hábito en esa fecha pertenece a la base de datos. Son tareas distintas dentro de la misma aplicación.

```text
Persona pulsa un botón
        |
Navegador envía una solicitud
        |
Flask identifica la ruta y el usuario
        |
Servicio aplica la regla del hábito
        |
PostgreSQL confirma un registro válido
        |
Flask prepara HTML con Jinja
        |
Navegador muestra el nuevo estado
```

### 2.4 URL ruta HTTP y respuesta

Una URL es una dirección completa, como `http://127.0.0.1:5000/panel`. `127.0.0.1` representa tu propio computador, `5000` es el puerto de desarrollo y `/panel` es la ruta de la aplicación. Ese enlace local no abre el proyecto en el computador de un compañero.

HTTP es el protocolo de intercambio entre navegador y servidor. GET suele solicitar una página; POST envía una acción o un formulario. Una respuesta tiene un código: 200 significa éxito; 302 indica redirección; 400, entrada inválida; 403, acceso prohibido; 404, recurso no encontrado; 429, demasiadas solicitudes; 500, fallo interno; 503, servicio temporalmente no disponible.

Después de un POST correcto, varias rutas redirigen. Así el navegador vuelve a pedir la página y muestra el estado actualizado. El nombre habitual es POST Redirect GET. Este patrón mejora la navegación; la restricción de la base de datos es la que impide que un hábito repetido se convierta en dos registros.

### 2.5 Biblioteca framework y dependencia

Una biblioteca aporta funciones ya desarrolladas. Un framework ofrece una estructura para construir aplicaciones. Flask relaciona rutas y funciones; SQLAlchemy permite trabajar con datos usando objetos y consultas; Jinja produce HTML con valores del servidor.

Las dependencias se declaran en `requirements.txt`. Los números fijan versiones para que el equipo instale una combinación conocida. `requirements-dev.txt` agrega herramientas para desarrollar y comprobar el proyecto. No debes instalar versiones distintas al azar cuando aparece un error: primero revisa el mensaje y compara tu entorno con estas listas.

### 2.6 Entorno local prueba y producción

Local es la copia en tu equipo. Staging es una copia compartida de prueba. Producción es la versión que usan personas reales. Usaremos cuentas y datos ficticios en las prácticas. Cada entorno compartido necesita su propia base de datos y sus propios secretos.

GitHub guarda el código y su historial. Render y Vercel ejecutan aplicaciones. Subir código a GitHub y publicarlo en internet son acciones diferentes. También es diferente publicar un PDF para estudiar y desplegar una aplicación que acepta registros.

### 2.7 Cómo leer las instrucciones de Python que encontrarás

Lee un archivo de arriba hacia abajo e identifica entradas, decisiones, llamadas y salida. No necesitas entender todos los nombres de una biblioteca al mismo tiempo. Empieza por estas formas:

| Escritura | Qué significa | Ejemplo del recorrido |
|---|---|---|
| from y import | Utilizar un nombre definido en otro módulo | Importar create_app desde app |
| = | Asignar un valor a un nombre | app = create_app() |
| == | Comparar si dos valores son iguales | role == "admin" |
| def y return | Definir una función y devolver su resultado | Un servicio devuelve True o False |
| if else y not | Tomar una decisión o negar una condición | Rechazar un hábito inactivo |
| None | Ausencia de un valor | Una consulta no encontró usuario |
| obj.nombre | Acceder a un atributo o método de un objeto | user.email y db.session.commit() |
| @decorador | Aplicar comportamiento a una función | login_required comprueba acceso |

`True` y `False` son valores booleanos. Una lista agrupa elementos en orden, como varios hábitos. Un diccionario relaciona claves y valores: `{"status": "ready"}` tiene una clave status y un valor ready. Por eso `response.json["status"]` consulta ese valor. Las comillas indican texto; los números se pueden sumar.

En una clase, `self` se refiere al objeto sobre el que se trabaja. `self.password_hash` es el hash de ese usuario. Una llamada con paréntesis, como `user.set_password(...)`, ejecuta un método. Definir el modelo User no crea un usuario: construir un objeto, añadirlo a la sesión de datos y confirmar son pasos posteriores.

Una anotación como `habit_id: int` expresa el tipo esperado para facilitar lectura y herramientas. No equivale por sí sola a validar una entrada. La ruta, el formulario y la base aplican las validaciones reales. `Mapped[str]` describe una propiedad de texto que SQLAlchemy relaciona con una columna.

`try` intenta ejecutar un bloque y `except` trata una clase de error. En el servicio de hábitos, un error de integridad provoca rollback. `with` establece un contexto que prepara y libera recursos; las pruebas lo usan para trabajar con una aplicación concreta.

Finalmente, una expresión como `f"Hola, {nombre}"` inserta un valor en un texto. Ese texto sigue siendo presentación, no una orden SQL. En las consultas del proyecto se usan expresiones de SQLAlchemy, en lugar de concatenar valores del usuario dentro de instrucciones de datos.

**Comprueba tu aprendizaje.** Explica por qué cerrar el navegador no debe borrar los hábitos y por qué un archivo subido a GitHub no crea por sí solo un servidor.

## 3 Qué problema resuelve VitaliLab y qué se modificó

VitaliLab permite registrar hábitos cotidianos, ver puntos y constancia, editar un perfil y leer contenidos o comunicados. El administrador puede publicar comunicados y consultar eventos operativos. Las medidas son opcionales y su cálculo de IMC se usa como ejemplo educativo. No presentes los resultados como diagnóstico ni como evaluación clínica de menores.

El prototipo agrupaba muchas responsabilidades en un archivo. Esa forma ayuda a empezar, pero dificulta encontrar qué valida datos, qué los guarda y qué muestra la pantalla cuando el proyecto crece. La reconstrucción conserva Flask y separa las tareas por módulos.

| Problema inicial | Cambio realizado | Razón que puedes explicar |
|---|---|---|
| Responsabilidades mezcladas | Módulos de acceso, perfil, hábitos y administración | Encontrar y modificar una función con menos confusión |
| Esquema difícil de reproducir | Modelos y migraciones versionadas | Crear la misma estructura en otra base |
| Datos de identidad e información de perfil mezclados | Usuario y perfil separados | Dar a cada entidad una responsabilidad |
| Riesgo de progreso duplicado | Registro diario único y servicio idempotente | Un reintento no debe sumar dos veces |
| Contraseña tratada de manera insegura | Hash scrypt | Evitar guardar la contraseña legible |
| Pantallas con estructura repetida | Plantilla base y componentes reutilizados | Mantener navegación y formularios consistentes |
| Falta de comprobaciones automáticas | Pruebas y pipeline | Detectar regresiones antes de integrar |
| Publicación manual difícil de repetir | Configuración de despliegue | Explicar qué requiere cada ambiente |

No se reemplazaron todos los archivos históricos en el repositorio original. La reconstrucción vive en el repositorio privado autorizado. La aplicación antigua de Render sigue siendo un servicio separado. Para sustentar, compara evidencia del prototipo con el código nuevo; no afirmes que la web antigua ya ejecuta esta reconstrucción.

**Ejercicio de explicación.** Elige una fila y descríbela con un ejemplo. Para duplicados: una conexión lenta hace que una persona pulse dos veces. La nueva regla permite un solo registro usuario hábito fecha. Ese ejemplo explica el problema mejor que repetir la palabra idempotencia.

## 4 Montar el proyecto en Windows desde cero

### 4.1 Preparar herramientas

Necesitas Python 3.13, Git si vas a descargar desde el repositorio, un editor como Visual Studio Code y un navegador. Docker es una ruta avanzada opcional; no lo necesitas para la primera práctica con SQLite.

Abre PowerShell y comprueba:

```powershell
python --version
git --version
```

La primera orden debe indicar Python 3.13. Si Windows abre la tienda o no reconoce la orden, el intérprete no está configurado para esa terminal. Instálalo desde su sitio oficial y vuelve a abrir la terminal. Si `git` no está disponible, puedes comenzar con el ZIP entregado por el docente.

### 4.2 Obtener la versión correcta

El docente debe darte acceso al repositorio privado o una copia ZIP del código. No debes utilizar la contraseña del docente para descargarlo.

Si ya tienes permiso en GitHub, en la carpeta elegida para tus proyectos ejecuta:

```powershell
git clone --branch staging https://github.com/juandigira17111980/vitalilab-profesional.git vitalilab-estudio
Set-Location vitalilab-estudio
git branch --show-current
```

La salida debe mostrar `staging`. El docente entrega el ZIP del commit de esta edición o indica la rama de revisión correspondiente. `main` no contiene automáticamente las mejoras por ser la rama que GitHub muestra primero.

Si usas el ZIP, extráelo y entra a la carpeta que contiene `wsgi.py`. Un ZIP creado con `git archive` no incluye el historial `.git`; puedes ejecutar la aplicación, pero las órdenes de historial necesitan una copia clonada o un repositorio local nuevo para practicar.

### 4.3 Crear un entorno de Python exclusivo

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

`.venv` contiene el intérprete y las bibliotecas de esta copia. `-m pip` pide a ese intérprete que ejecute su instalador. Escribimos su ruta completa para que funcione aunque PowerShell impida activar scripts. No hace falta cambiar la política de seguridad del equipo para seguir esta guía.

Resultado esperado: la instalación termina sin error. El entorno no se sube a Git; otras personas lo reconstruyen desde las listas de dependencias.

### 4.4 Configurar la primera base de práctica

Ejecuta estas órdenes en la misma ventana donde vas a iniciar la aplicación:

```powershell
$env:APP_ENV = "development"
$env:DATABASE_URL = "sqlite:///vitalilab-aprendizaje.db"
$env:SECRET_KEY = (.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))")
$env:SESSION_COOKIE_SECURE = "false"
```

Una variable de entorno es un valor que el sistema entrega al programa sin escribirlo en su código. `APP_ENV` identifica el ambiente. `DATABASE_URL` selecciona la base. `SECRET_KEY` permite firmar sesiones y tokens. `SESSION_COOKIE_SECURE=false` es necesario para esta práctica HTTP local; en la web compartida se utiliza HTTPS y debe ser `true`.

El archivo SQLite quedará dentro de la carpeta `instance`. Es una base exclusiva de aprendizaje. No contiene datos de la web histórica. Al cerrar PowerShell estas variables de proceso se pierden; al retomar debes establecerlas otra vez. Mantén la misma clave durante una sesión de práctica, porque cambiarla invalida las cookies que firmaste antes.

`.env.example` es una lista de referencia, no una configuración lista para tu equipo. Copiarla a `.env` no garantiza que se cargue: el proyecto no declara `python-dotenv` como dependencia. Por eso este manual establece las variables explícitamente y no depende de esa carga automática. Su ejemplo PostgreSQL tampoco crea un servidor PostgreSQL al copiarlo.

### 4.5 Crear tablas y cargar el catálogo

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi:app db upgrade
.\.venv\Scripts\python.exe -m flask --app wsgi:app seed-habits
.\.venv\Scripts\python.exe -m flask --app wsgi:app db current
```

La primera orden aplica las migraciones pendientes. La segunda crea o sincroniza cuatro hábitos. La tercera muestra la revisión actual, `208469fd48ef`. El resultado del seed informa cuántos hábitos nuevos se crearon. Ejecutarlo nuevamente debe crear cero adicionales; actualiza el catálogo por su código único.

Si aparecen tablas inexistentes, revisa que aplicaste las migraciones a la misma `DATABASE_URL` con la que arrancarás. Si aparece rechazo de conexión a PostgreSQL, probablemente no estás usando la configuración SQLite de esta primera práctica.

### 4.6 Iniciar y abrir

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi:app run --host 127.0.0.1 --port 5000
```

Deja esta terminal abierta. Visita `http://127.0.0.1:5000` en el navegador. No actives `--debug` en un servicio publicado. Para detener el servidor local presiona Ctrl+C en esa terminal; detener el proceso no elimina el archivo de datos.

Abre también `/health` y `/ready`. `/health` devuelve JSON con estado y versión; `/ready` ejecuta una comprobación de conexión. Una respuesta 200 de `/ready` confirma que la base responde, pero por sí sola no demuestra que todas las tablas o todos los flujos sean correctos.

### 4.7 Crear un usuario y un administrador

En la pantalla de registro utiliza un correo de ejemplo, un apodo y una contraseña ficticia de al menos diez caracteres con mayúscula, minúscula y número. Acepta la política para completar el formulario. No uses tu contraseña personal de otro servicio.

Para crear un administrador detén el servidor y ejecuta en la misma terminal:

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi:app create-admin
```

El comando pide correo, nombre y contraseña. La contraseña se introduce de manera oculta y se confirma. Usa otro correo ficticio distinto del usuario normal. Vuelve a iniciar el servidor y prueba ambos roles. No cambies un campo oculto de la pantalla para asignarte administración: el rol lo controla el servidor.

### 4.8 Retomar y compartir evidencia

Para retomar, entra a la raíz, restablece las variables de la práctica y ejecuta `flask run` con el intérprete de `.venv`. Conserva el mismo archivo SQLite si quieres observar persistencia. Una clave nueva obligará a iniciar sesión otra vez, pero no borra tus usuarios ni hábitos.

El docente puede recibir capturas del panel, la salida de `/ready` y la revisión Alembic. No incluyas la clave, el contenido de `.env` ni una cadena de conexión. Una persona debe poder repetir tu instalación en otra copia siguiendo estos pasos.

## 5 Leer la estructura y seguir el arranque

### 5.1 Mapa de archivos reales

```text
vitalilab-profesional/
  wsgi.py                   Punto de entrada de la web
  requirements.txt          Dependencias para ejecutar
  requirements-dev.txt      Herramientas para desarrollo
  pyproject.toml            Pruebas formato y entrada Vercel
  vercel.json               Configuración de la copia Vercel
  render.yaml               Configuración de la copia Render
  app/
    __init__.py             Construye la aplicación Flask
    config.py               Lee y valida la configuración
    extensions.py           Define las herramientas compartidas
    models.py               Describe las entidades de datos
    forms.py                Define campos y validaciones
    commands.py             Carga hábitos y crea administradores
    errors.py               Respuestas de error controladas
    main/routes.py          Inicio contenido panel y estado
    auth/routes.py          Registro acceso y recuperación
    profile/routes.py       Perfil y mediciones propias
    habits/routes.py        Listado y cumplimiento
    admin/routes.py         Comunicados y auditoría
    services/progress.py    Puntos niveles racha e IMC
    services/audit.py       Registra eventos sin datos sensibles
    services/email.py       Envía recuperación por SMTP
    templates/              Pantallas y componentes Jinja
    static/                 CSS JavaScript y marca SVG
  migrations/versions/      Cambios de estructura de la base
  scripts/build_vercel.py   Prepara archivos estáticos para CDN
  tests/                    Comprobaciones automatizadas
  docs/                     Material técnico y esta guía
  .github/workflows/ci.yml   Comprobaciones de GitHub Actions
```

Un módulo es una parte del proyecto que agrupa tareas relacionadas. Un blueprint es la forma que ofrece Flask para agrupar rutas. Por ejemplo, `auth` reúne acciones de acceso y utiliza el prefijo `/acceso`. Blueprint no es una tabla y no crea automáticamente un microservicio.

### 5.2 El primer archivo y la fábrica

`wsgi.py` contiene:

```python
from app import create_app

app = create_app()
```

La primera línea importa una función. La segunda construye una aplicación y la deja disponible con el nombre `app`. WSGI es el acuerdo mediante el que un servidor Python puede llamar a la aplicación para atender una petición. No necesitas implementar ese acuerdo desde cero para usar Flask.

`create_app` es una fábrica: una función que prepara y devuelve una aplicación. Carga configuración, inicializa extensiones, registra blueprints, errores, comandos y cabeceras. No crea las tablas. La orden de migración realiza esa tarea de manera explícita.

La misma fábrica permite construir una aplicación de pruebas con otra base y otra configuración. Esto evita que una prueba tenga que modificar datos de un usuario real para funcionar.

En Vercel la carpeta de la aplicación no permite escrituras de ejecución. La fábrica selecciona una carpeta temporal para `instance` cuando `VERCEL=1`. Esa carpeta es para archivos temporales; no se usa para guardar la PostgreSQL.

### 5.3 Por qué un monolito modular

Monolito significa que los módulos se entregan como una sola aplicación. Modular significa que tienen responsabilidades separadas. Podemos seguir una transacción de hábitos sin repartirla entre varios servidores ni administrar varias aplicaciones para una demostración académica.

La consecuencia es que los módulos comparten un despliegue y una base. Un error de arranque puede afectar a toda la aplicación. Esa limitación se trata con pruebas y módulos claros. Microservicios sería otra decisión, con más operación y coordinación; aquí no hay una necesidad demostrada que compense ese trabajo.

**Práctica.** Abre `wsgi.py`, sigue `create_app` y busca dónde se registra el blueprint de hábitos. Después identifica qué función atenderá un POST a `/habitos/1/completar`. Debes llegar a `complete` en `app/habits/routes.py`.

## 6 La base de datos y la razón de las siete entidades

### 6.1 Tabla fila columna y clave

Una tabla reúne registros del mismo tipo. Una fila representa un registro. Una columna guarda un atributo. En `users`, una fila representa un usuario y `email` es una columna.

La clave primaria identifica una fila. `users.id` distingue usuarios aunque tengan apodos iguales. Una clave foránea enlaza una fila con otra tabla. `habit_entries.user_id` indica a qué usuario pertenece ese cumplimiento. Una restricción es una regla que la propia base rechaza si se intenta incumplir.

Una relación uno a uno permite un perfil por usuario. Una relación uno a muchos permite muchas mediciones o cumplimientos para una persona. Entre usuarios y hábitos hay una relación muchos a muchos, resuelta mediante `habit_entries`: muchos usuarios completan muchos hábitos en fechas diferentes.

```text
users
  | un perfil por usuario
  +-- user_profiles
  | varias medidas opcionales
  +-- health_measurements
  | varios registros diarios
  +-- habit_entries -- muchos registros pertenecen a un hábito -- habits
  | un administrador puede escribir varios comunicados
  +-- announcements
  | un actor puede producir varios eventos
  +-- audit_events
```

### 6.2 Por qué separar en lugar de guardar todo junto

Si una sola fila mezcla correo, contraseña, nombre de hábito, puntaje acumulado y todos los pesos, repetimos datos o terminamos sobrescribiendo historial. Si el nombre de un hábito cambia, habría que modificar muchas filas. Si se pierde una actualización de puntaje, el saldo puede dejar de coincidir con lo realizado.

Separamos identidad, perfil, medidas, catálogo, cumplimientos, comunicados y eventos. Cada tabla responde a una pregunta concreta. Normalizar es organizar estas responsabilidades para reducir duplicación y anomalías. No significa dividir por dividir: se conservan juntas las columnas que describen la misma entidad.

### 6.3 Usuario y perfil

| Campo en users | Función |
|---|---|
| id | Identidad interna única |
| email | Correo normalizado y único |
| password_hash | Resultado scrypt sin contraseña legible |
| role y status | Rol user o admin y estado active o inactive |
| last_login_at | Último acceso correcto |
| failed_login_count y locked_until | Control de intentos y bloqueo temporal |
| created_at y updated_at | Fechas de creación y modificación |

`user_profiles` utiliza `user_id` como clave primaria y foránea a la vez. Eso impide crear dos perfiles para el mismo usuario. Contiene `display_name`, `birth_date`, `grade`, `timezone`, `privacy_version`, `privacy_accepted_at` y las fechas de creación y modificación. La fecha de nacimiento y el grado son opcionales.

El campo `timezone` prepara un dato de contexto, pero el cumplimiento diario actual usa `date.today()` del servidor. No afirmes que todas las fechas ya se calculan en la zona individual del perfil. Un próximo cambio podría utilizar esa zona de forma coherente en rutas y servicios.

### 6.4 Medidas y catálogo

`health_measurements` guarda `id`, `user_id`, `weight_kg`, `height_cm`, `bmi_snapshot`, `measured_on` y `created_at`. Peso y altura usan números decimales con dos posiciones. El IMC se guarda como una fotografía del cálculo de esa medición. Conservar filas distintas permite un historial cuando cambian las medidas; no se agrega otra fila si la última tiene exactamente los mismos valores.

La validación establece rangos de entrada y exige peso y altura juntos. El modelo tiene también restricciones de peso, altura e IMC. Los rangos son reglas del software; no son una recomendación individual de salud ni una valoración del crecimiento.

`habits` es el catálogo: `id`, `code`, `name`, `description`, `category`, `icon`, `points`, `active`, `sort_order`, `created_at` y `updated_at`. `code` es único y permite sincronizar el seed. `active` decide si aparece disponible; `sort_order` organiza la presentación.

### 6.5 Cumplimientos comunicados y auditoría

`habit_entries` contiene `id`, `user_id`, `habit_id`, `completed_on` y `created_at`. Su restricción más importante es:

```text
UNIQUE(user_id, habit_id, completed_on)
```

Esto significa que la combinación de esos tres valores no se puede repetir. Otro usuario sí puede completar el mismo hábito ese día; el mismo usuario puede completarlo otro día. La regla se evalúa sobre la combinación, no sobre cada columna por separado.

`announcements` guarda `id`, `author_user_id`, `title`, `body`, `status`, `published_at` y las fechas comunes. Los estados son `draft`, `published` y `archived`. La página pública consulta solo comunicados publicados.

`audit_events` guarda `id`, `actor_user_id`, `action`, `entity_type`, `entity_id`, `metadata_redacted` y `created_at`. Un evento permite saber que ocurrió una acción. No registra contraseña, token de recuperación ni medidas de salud. No es una copia completa de cada objeto ni un reemplazo del historial de negocio.

### 6.6 Qué pasa con las relaciones al borrar

CASCADE borra dependientes, como el perfil o las medidas de un usuario. RESTRICT impide borrar un elemento todavía utilizado, como un hábito con cumplimientos o un autor con comunicados. SET NULL conserva el evento pero deja sin actor su referencia cuando se elimina ese usuario.

Por eso no basta con decir que cualquier cuenta se puede eliminar siempre. Un autor de comunicados tiene una relación RESTRICT que requiere resolver antes esa referencia. Además, la aplicación actual no ofrece un formulario de eliminación de cuentas. La regla del esquema y una función disponible en pantalla son cosas distintas.

### 6.7 Índices transacciones y errores de concurrencia

Un índice ayuda a localizar datos por una columna o combinación. El historial necesita buscar por usuario y fecha, por eso existen índices compuestos para esos recorridos. Un índice también ocupa espacio y añade trabajo al escribir; se justifica por una consulta real.

Una transacción agrupa cambios que deben confirmarse juntos. `db.session.commit()` confirma; `db.session.rollback()` deshace cambios pendientes tras un fallo. El cumplimiento y su auditoría se insertan en la misma transacción.

Dos solicitudes pueden consultar casi al mismo tiempo y ambas creer que falta el registro. La consulta previa no basta. La restricción única hace que una inserción falle; el servicio captura `IntegrityError`, ejecuta rollback y devuelve que no se añadió un cumplimiento. Esta es la razón técnica de defender la integridad también en la base.

### 6.8 Por qué SQLite local y PostgreSQL compartido

SQLite es un motor que guarda esta práctica en un archivo. Facilita empezar sin otro servidor. PostgreSQL es un servidor de datos que permite conexiones compartidas, restricciones y operación administrada. En `staging` y `production` la configuración exige PostgreSQL y rechaza SQLite.

No afirmes que SQLite es inútil ni que PostgreSQL elimina todos los errores. La elección responde a cómo se ejecutará esta aplicación. En NexoStack los datos viven en la PostgreSQL independiente y su volumen persistente, no dentro de la imagen de la web. Si se utilizara Vercel, sería necesaria una base externa porque la función no ofrece almacenamiento local permanente.

### 6.9 Migraciones y restauración

El modelo describe el estado que queremos. La migración registra cómo pasar de un esquema a otro. Alembic mantiene una revisión actual en `alembic_version`.

| Revisión | Cambio |
|---|---|
| 0380d5595f5e | Crea las siete tablas con relaciones y restricciones |
| 208469fd48ef | Añade índices para claves foráneas y consultas |

`db upgrade` aplica cambios pendientes. `db check` compara modelo y esquema para detectar deriva. `db migrate` genera una propuesta: alguien debe leerla y revisarla antes de aplicarla. No editamos una migración que ya se ejecutó en un ambiente compartido.

Un backup es una copia recuperable; restauración es reconstruir una base con esa copia. El pipeline prueba `pg_dump` y `pg_restore` en PostgreSQL 18 aislado y compara catálogo, revisión Alembic y deriva. Ese ensayo no configura automáticamente backups del proveedor ni demuestra la recuperación de los datos reales de producción.

### 6.10 Consultar la práctica sin modificar datos

Detén el servidor o abre otra terminal con las mismas variables. Ejecuta:

```powershell
.\.venv\Scripts\python.exe -m flask --app wsgi:app shell
```

En el intérprete escribe:

```python
from app.extensions import db
from app.models import User, Habit, HabitEntry

db.session.scalar(db.select(db.func.count(User.id)))
db.session.scalar(db.select(db.func.count(Habit.id)))
db.session.scalar(db.select(db.func.count(HabitEntry.id)))
exit()
```

Debe haber cuatro hábitos después del seed. Los otros conteos dependen de tu práctica. Este ejercicio usa SELECT; no borra ni cambia registros. `db.select` construye una consulta; `scalar` devuelve un valor; `count` cuenta filas.

**Para sustentar.** Dibuja dos usuarios, un hábito y tres cumplimientos de fechas distintas. Identifica cuál sería el cuarto registro inválido. Explica qué protege UNIQUE y qué protege la sesión del usuario.

## 7 Backend explicado con recorridos de código

### 7.1 Responsabilidad de cada pieza

La ruta decide cómo responder a una solicitud. El formulario revisa tipos, longitudes y formatos. El servicio concentra una regla reutilizable. El modelo describe y protege los datos. La plantilla los presenta. Repartir así permite que una prueba compruebe un cálculo sin abrir un navegador.

Esta separación no convierte a la aplicación en una implementación completa de todas las capas de Clean Architecture. Es un monolito Flask con responsabilidades explícitas. Usa ese nombre y demuestra sus límites reales.

### 7.2 Registro paso a paso

Lee `register` en `app/auth/routes.py` y `RegisterForm` en `app/forms.py`.

1. Un GET devuelve la pantalla y un token CSRF.
2. El navegador envía apodo, correo, contraseña, confirmación y aceptación por POST.
3. Flask verifica CSRF y el formulario valida los campos.
4. El correo se normaliza para comparar sin espacios exteriores ni diferencias de mayúscula.
5. Se comprueba si ya existe.
6. Se crea `User` y se calcula su hash de contraseña.
7. Se asigna `UserProfile`; su referencia enlaza ambas entidades.
8. `flush` obtiene el identificador sin cerrar todavía la transacción.
9. Se registra un evento y `commit` confirma.
10. `login_user` establece la sesión y la respuesta redirige al panel.

```python
user = User(email=email)
user.set_password(form.password.data)
user.profile = UserProfile(display_name=form.display_name.data.strip())
db.session.add(user)
db.session.flush()
record_event("account.registered", "user", user.id, user.id)
db.session.commit()
```

Este fragmento proviene del proyecto. `add` prepara la inserción. `flush` envía cambios pendientes dentro de la transacción. `commit` la confirma. La comprobación de correo mejora el mensaje y la restricción única sigue defendiendo la base.

### 7.3 Acceso sesión y rol

Login compara el valor escrito con el hash usando `check_password_hash`. Nunca compara con una contraseña almacenada como texto. Tras cinco fallos conocidos se activa un bloqueo de quince minutos. Un acceso correcto reinicia el contador.

Autenticación responde quién eres. Autorización responde qué puedes hacer. `login_required` exige sesión; `admin_required` además exige el rol admin. Ocultar un enlace de administración en Jinja mejora la interfaz, pero la comprobación del servidor es la que protege la ruta.

Flask usa aquí su sesión predeterminada en una cookie firmada. El navegador conserva esa cookie; la firma detecta alteraciones. Firma no significa cifrado: no guardes contraseñas ni información sensible en la sesión. Flask-Login utiliza el identificador para cargar el usuario desde la base en otra petición. No existe una tabla de sesiones de servidor en esta implementación.

### 7.4 Completar un hábito

La ruta `complete` recibe `habit_id` como entero, exige sesión, aplica un límite de peticiones y valida el formulario. Busca que el hábito exista y esté activo. Después llama al servicio.

```python
if complete_habit(current_user, habit):
    flash(f"¡Bien! Sumaste {habit.points} puntos con {habit.name}.", "success")
else:
    flash("Este hábito ya estaba registrado hoy. Tus puntos no se duplicaron.", "info")
return redirect(url_for("habits.index"))
```

`current_user` viene de la sesión; no se acepta un identificador de usuario arbitrario desde el formulario. `flash` prepara un mensaje para la próxima pantalla. `url_for` obtiene la URL a partir del nombre de la ruta. El servicio hace la consulta, inserción, auditoría y confirmación que estudiamos en la base de datos.

Idempotencia significa que repetir esta misma acción del día deja el mismo resultado de negocio. Si ya existe, el servicio devuelve `False`. No significa que todos los POST de cualquier aplicación sean idempotentes.

### 7.5 Cómo se calculan los puntos y la racha

La aplicación suma los puntos del catálogo asociados a cumplimientos del usuario. Los cuatro hábitos sembrados valen 15, 15, 15 y 10; cumplir uno de cada uno produce 55 puntos. No hay una columna de saldo acumulado enviada por el navegador.

El diseño facilita comprobar la suma a partir de eventos, pero tiene una consecuencia: cambiar los puntos del catálogo puede recalcular el valor de registros antiguos. El seed también sincroniza esos valores. Mantén estable el catálogo de la práctica; si el producto necesita precios históricos por hábito, deberá añadirse una política o un valor snapshot por evento mediante migración.

La racha cuenta días consecutivos con al menos un cumplimiento. Si hoy aún no hay uno, puede continuar a partir de ayer. Un día sin cumplimiento rompe la secuencia. No equivale a cumplir todos los hábitos todos los días.

### 7.6 Perfil cálculo y comunicados

El perfil solo consulta medidas del usuario conectado. El formulario valida una fecha no futura y exige peso y altura juntos. El cálculo utiliza peso dividido por la altura en metros al cuadrado y se redondea a dos decimales. El backend conserva el valor validado; la calculadora pública de JavaScript muestra una orientación local sin registrar datos.

Un comunicado nace como borrador. El administrador lo publica o archiva con POST y CSRF. `main.home` consulta hasta tres publicados. Una persona normal no puede publicar un comunicado simplemente enviando la misma dirección desde su navegador: la ruta exige el rol.

### 7.7 Recuperación y límites de la función

La solicitud de recuperación responde de manera genérica exista o no el correo. El token está firmado, tiene caducidad y contiene una firma derivada del hash actual. Al cambiar la contraseña, el token antiguo deja de verificar. Eso no significa que el proyecto ya revoque todas las sesiones y cookies recordadas de todos los dispositivos; no hay una versión de sesión implementada para esa revocación global.

El servicio de correo usa SMTP configurable. Una prueba con un doble verifica la llamada a TLS, autenticación y envío. Para afirmar que un correo llegó, debe probarse con un proveedor real. Render Free bloquea puertos SMTP habituales; completar valores `MAIL_*` no supera esa restricción. La configuración de envío se resuelve según proveedor y plan antes de una demostración de recuperación real.

### 7.8 Rutas que conviene reconocer

| Ruta | Método principal | Qué demuestra |
|---|---|---|
| / | GET | Inicio y comunicados publicados |
| /acceso/registro | GET y POST | Formulario y creación de cuenta |
| /acceso/ingresar | GET y POST | Autenticación |
| /acceso/salir | POST | Cierre de sesión |
| /panel | GET | Progreso personal |
| /perfil/ | GET y POST | Perfil y medida propia |
| /habitos/ | GET | Catálogo del usuario |
| /habitos/1/completar | POST | Cumplimiento del hábito 1 |
| /admin/ | GET | Control por rol |
| /health y /ready | GET | Proceso y conexión |

Las rutas de usuario devuelven principalmente HTML o una redirección. No es una API JSON completa para una aplicación móvil. `/health` y `/ready` sí devuelven JSON. El inventario completo está en el documento de backend.

## 8 Frontend explicado desde la primera pantalla

### 8.1 HTML Jinja CSS y JavaScript

HTML organiza el contenido: título, párrafo, enlace, formulario. CSS decide el aspecto y la distribución. JavaScript responde a acciones en el navegador. Jinja es una herramienta del backend que construye el HTML usando variables y condiciones antes de enviarlo.

Cuando recibes una página, el navegador no ejecuta las instrucciones Jinja. Ya recibe su resultado. Esa es una diferencia importante frente a una interfaz React que consulta una API y construye muchas vistas en el cliente. VitaliLab no utiliza React, Next.js ni un proceso npm para su interfaz.

### 8.2 Plantilla base y herencia

`app/templates/base.html` contiene navegación, estilos, mensajes, área principal y pie. Una pantalla declara que extiende esa base y rellena sus bloques.

```html
{% extends "base.html" %}
{% block title %}Crear cuenta · VitaliLab{% endblock %}
{% block content %}
  <h1>Ejemplo de una pantalla</h1>
{% endblock %}
```

El ejemplo muestra la técnica, no es una pantalla nueva del proyecto. `extends` reutiliza la estructura. `block` indica el espacio que la pantalla puede completar. Modificar el encabezado de la base afecta a varias pantallas; por eso conviene revisar después acceso, panel y administración.

`{{ variable }}` muestra un valor. `{% if ... %}` decide si aparece una sección. `{% for ... %}` repite elementos. Jinja escapa texto por defecto para evitar interpretarlo automáticamente como HTML. No uses `safe` sobre datos de usuarios sin una razón y un proceso de sanitización.

### 8.3 Formularios y componentes

La macro `field` en `templates/macros/forms.html` construye un campo con etiqueta, ayuda y errores. Una macro es un fragmento reutilizable. El formulario Python define la validación; la macro define cómo presentar su resultado.

Un formulario de modificación incluye `form.hidden_tag()`, que agrega datos ocultos como el token CSRF. El token permite comprobar que la solicitud pertenece al flujo de esa sesión. No es la contraseña del usuario ni una prueba de que tenga rol administrador.

### 8.4 Estilos y adaptación al celular

`app/static/css/app.css` agrupa los estilos. Un selector decide qué elementos reciben una regla. Una clase como `.button` permite reutilizar presentación. Las variables CSS reúnen colores y medidas para facilitar cambios consistentes.

Las media queries cambian la distribución según el ancho. El sistema incluye cortes en 900, 720 y 440 píxeles. La prueba de 390 píxeles ayuda a observar una pantalla pequeña; no significa que se hayan comprobado todos los celulares del mercado.

La tipografía procede del sistema y la marca es SVG local. Esto evita depender de una descarga de fuentes o imágenes externas para la pantalla inicial.

### 8.5 Comportamiento del menú y de los mensajes

`app/static/js/app.js` busca elementos con atributos como `data-nav-toggle`. Al pulsar el botón cambia la clase del menú y actualiza `aria-expanded`. Escape lo cierra y devuelve el foco al botón. Otro manejador cierra mensajes.

El frontend principal funciona con formularios del servidor. Si desactivas JavaScript, la calculadora pública y ciertos detalles del menú o gráficos cambian, pero las reglas de registro de usuarios y hábitos siguen estando en Python. Esta separación evita confiar puntajes al navegador.

Accesibilidad significa que distintas personas puedan utilizar la interfaz, también con teclado o herramientas de apoyo. El proyecto incluye etiquetas, foco visible y mensajes anunciados. Todavía requiere una revisión formal para afirmar conformidad completa con WCAG.

### 8.6 Práctica de un cambio visible

En una copia local abre `app/templates/main/home.html`, cambia un texto corto y guarda. Actualiza el navegador y explica por qué no cambió ninguna tabla. Si modificas Python sin modo debug, detén y reinicia el servidor; guardar un archivo no obliga a un proceso ya iniciado a importar otra vez ese módulo.

Después abre la vista móvil del navegador, recorre con Tab y prueba Escape en el menú. Registra si el texto se lee, si hay corte horizontal y si puedes llegar al botón de registro. Vuelve al código para relacionar un comportamiento con su selector o atributo.

**Para sustentar.** Señala una parte producida por Jinja, una regla CSS y un evento JavaScript. Explica qué ocurre primero y en qué computador se ejecuta cada uno.

## 9 Probar el proyecto y aprender de los errores

### 9.1 Qué comprueba una prueba

Una prueba prepara una situación, ejecuta una acción y compara el resultado con lo esperado. Un `assert` expresa una condición que debe ser verdadera.

```python
response = client.get("/health")
assert response.status_code == 200
```

Este fragmento ilustra la forma. El cliente de pruebas realiza una solicitud sin abrir un navegador. La suite usa una base en memoria y desactiva algunos controles para casos específicos; también existe una prueba separada con CSRF real. No confundas esa configuración con la de publicación.

### 9.2 Ejecutar y leer el resultado

```powershell
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check app tests wsgi.py scripts migrations/versions
.\.venv\Scripts\python.exe -m ruff format --check app tests wsgi.py scripts migrations/versions
```

Pytest debe terminar con los casos aprobados. Ruff revisa errores y formato; no prueba por sí mismo el comportamiento de una pantalla. El número de pruebas puede aumentar al agregar casos; usa el resultado de tu versión y no memorices una cifra vieja.

Cobertura indica qué instrucciones y ramas pasaron por la ejecución de pruebas. El umbral configurado es 85 por ciento. Superarlo no demuestra ausencia de errores, privacidad aprobada ni que una web en la nube responda correctamente.

En `tests/conftest.py`, una fixture prepara objetos compartidos para las pruebas: aplicación, cliente y usuarios ficticios. Se crean tablas en memoria, se siembran hábitos y se limpian al terminar. Ese uso de `create_all` es específico de pruebas, no el procedimiento para migrar una base compartida.

### 9.3 Un ejercicio de regresión

Busca `test_habit_completion_is_idempotent` dentro de `tests/test_progress.py`. Puedes ejecutar el archivo completo:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/test_progress.py
```

Lee cómo prepara al usuario y al hábito, cómo repite la acción y qué cuenta compara. No alteres la lógica en una rama compartida para hacer que falle una demostración. Si quieres practicar un fallo, hazlo en una copia desechable y conserva la comparación del antes y después.

### 9.4 Errores frecuentes y cómo localizarlos

| Mensaje o síntoma | Qué revisar primero |
|---|---|
| No module named flask | Estás usando el Python equivocado o faltan dependencias |
| No such table | Migración y DATABASE_URL de esa terminal |
| Puerto ocupado | Otro proceso usa 5000; practica con 5001 |
| CSRF token missing | El POST no incluye token o perdió la sesión |
| 403 en administración | Rol de la cuenta conectada |
| 429 | Espera el periodo del límite y revisa qué acción repetiste |
| Perfil sin medición | Peso y altura deben validarse juntos |
| /health bien y /ready mal | Conexión de base o disponibilidad |
| Pantalla sin estilos en Vercel | Build de public/static y URL del archivo CSS |
| Recuperación sin correo | Credenciales servicio y restricciones del alojamiento |

Lee el primer error útil y el archivo al que apunta. Un traceback es una lista del recorrido que terminó en fallo. El servidor puede registrar detalle; la pantalla pública de un error 500 no debe mostrar secretos ni toda la traza.

### 9.5 Health y readiness no sustituyen la práctica

Una respuesta 200 del proceso no confirma que registro, cookies y consultas estén bien. En una publicación prueba el formulario completo, la persistencia y los permisos. Utiliza datos ficticios y evita agotar el rate limit ejecutando repetidamente la misma demostración.

## 10 Git GitHub y el trabajo del equipo

### 10.1 Historial rama commit y revisión

Git guarda cambios de archivos en commits. Una rama señala una línea de trabajo. GitHub aloja el repositorio y facilita revisiones. Un pull request presenta cambios para compararlos antes de integrarlos.

Un commit no es una copia de la base ni de tu entorno `.venv`. `.gitignore` indica archivos que no se deben versionar: bases locales, secretos, archivos temporales y resultados. No borra automáticamente un secreto que ya se haya subido en el pasado; ese incidente exige retirarlo del uso y revisar el historial.

### 10.2 Tu primer cambio en una rama

En una copia clonada y sin cambios pendientes:

```powershell
git switch staging
git pull --ff-only origin staging
git switch -c docs/mi-practica
```

Modifica solo un texto o una explicación, comprueba el resultado y revisa:

```powershell
git status
git diff
git add docs/mi-practica.md
git commit -m "docs(learning): agrega mi explicacion de una ruta"
```

Para esas últimas órdenes debes crear antes `docs/mi-practica.md` con tu explicación. `git diff` muestra lo que realmente cambió. `git add` selecciona el archivo; `commit` registra esa selección. Evita `git add .` por costumbre cuando todavía no sabes qué archivos contiene tu carpeta.

Subir una rama requiere permiso del propietario. `git push -u origin docs/mi-practica` publica tus commits en ese repositorio, pero no cambia directamente el sitio histórico. Presenta el pull request hacia `staging`; el docente revisa propósito, resultados y documentación.

### 10.3 Qué hace el pipeline

`.github/workflows/ci.yml` ejecuta tres trabajos. Calidad instala dependencias, revisa formato, hace análisis de seguridad, corre pruebas y audita dependencias. PostgreSQL aplica migraciones, carga catálogo y ensaya restauración. Contenedor construye la imagen Docker.

CI significa integración continua: comprobar cambios de forma repetible. Un resultado verde está asociado a un commit. Si modificas después el código, debes comprobar ese nuevo commit. No presentes como validación actual un resultado obtenido para otra versión.

Publicación continua exige además conectar el alojamiento y observar el resultado. En Render el Blueprint propone publicar tras pasar los checks. En Vercel revisamos la configuración de su proyecto y la rama; los nombres de ambientes no son idénticos en todas las plataformas.

## 11 Entender el montaje completo antes de desplegar

### 11.1 Las piezas de una publicación

| Pieza | Qué aporta | Qué no hace por sí sola |
|---|---|---|
| Repositorio GitHub | Código e historial | No ejecuta automáticamente el backend |
| Vercel o Render | Ejecución y dirección web | No inventa las tablas ni tus secretos |
| PostgreSQL | Datos persistentes | No construye la interfaz |
| Variables de entorno | Configuración por ambiente | No deben convertirse en documentación pública |
| Migraciones | Estructura de datos | No copian usuarios históricos automáticamente |
| Pruebas y revisión | Evidencia de funcionamiento | No sustituyen comprobar la web publicada |

Build significa preparar una entrega: instalar bibliotecas y preparar archivos. Deploy significa colocarla y activarla en el alojamiento. Log es el registro de mensajes del proceso. HTTPS protege el transporte entre navegador y servidor. Un dominio es un nombre amigable; para practicar puede utilizarse la dirección generada por el proveedor.

### 11.2 El montaje elegido en NexoStack

NexoStack es el VPS de laboratorio que ya utiliza el propietario. La copia de VitaliLab se monta allí como un proyecto Docker separado. No se reemplaza Render ni se utiliza la base de Mercanta o Murano. El archivo `deploy/nexostack/compose.yaml` reúne web, migrador y PostgreSQL propia. El migrador es una tarea puntual; no queda atendiendo solicitudes.

La web corre con el usuario 10001 y raíz de archivos de solo lectura. Tiene una carpeta temporal para `instance` y un límite de 384 MiB. La base tiene límite de 256 MiB y un volumen persistente específico. Esos límites son máximos de uso, no una reserva exclusiva ni una promesa de soportar cualquier número de usuarios.

Traefik, el proxy existente, reconoce únicamente el dominio de VitaliLab y envía esas solicitudes al puerto 10000 de su web. No se reinicia el proxy para agregar el contenedor. La base no publica el puerto 5432 y permanece en la red interna de VitaliLab. Solo la web pertenece también a la red de entrada compartida: varios proyectos comparten el VPS y el proxy, no sus tablas ni contraseñas.

### 11.3 Por qué el contenedor no es la base de datos

La imagen contiene código y bibliotecas. Un contenedor ejecuta esa imagen. El volumen conserva datos aparte. Cambiar la imagen de la web no debe borrar usuarios ni hábitos.

PostgreSQL 18 en la imagen oficial usa una carpeta versionada dentro de `/var/lib/postgresql`. Por eso el volumen de esta edición se monta allí; no se reutiliza sin revisión el ejemplo antiguo de `/var/lib/postgresql/data`. La persistencia debe comprobarse después de recrear el servicio, no deducirse solo al leer YAML.

La carpeta `/opt/labs/vitalilab/releases` guarda versiones por commit. `current` señala la activa. `secrets` contiene valores privados y `backups` conserva dumps. Un estudiante recibe el código, no esos secretos ni la llave principal del servidor.

### 11.4 Roles y conexiones de la base

`DATABASE_URL` reúne servidor, usuario, contraseña y nombre de base. Es un secreto. `vitalilab_owner` administra únicamente la PostgreSQL independiente de este laboratorio y ejecuta migraciones. La web utiliza `vitalilab_app`, que puede consultar y modificar las siete tablas de negocio, pero no crear bases, roles o tablas.

La conexión de la aplicación verifica el certificado y el nombre `db` con `sslmode=verify-full`. La comprobación real registró TLS 1.3. HTTPS del navegador y TLS de base son conexiones distintas: un candado en la página no prueba cómo se conectó PostgreSQL.

El rate limit actual usa memoria de un worker y se reinicia con el proceso. Para varias instancias o usuarios reales habría que implementar y comprobar almacenamiento compartido. La autenticación y los datos de negocio no se trasladan a esa memoria temporal.

## 12 Publicar y gestionar la copia de práctica en NexoStack

### 12.1 Distinguir estudiante y administrador de infraestructura

El estudiante sigue primero el montaje local y practica con datos ficticios. El administrador de infraestructura publica versiones verificadas. No se entrega a todos los alumnos la cuenta principal del VPS ni el grupo Docker.

Para esta edición se autorizó una copia de laboratorio en `https://vitalilab.lab.nexostack.app`. La web original de Render continúa aparte. La publicación nueva no migra automáticamente sus personas ni sus registros.

### 12.2 Preparar la versión y comprobar el servidor

El administrador identifica el commit de la rama `staging`, verifica el resultado de CI y guarda el estado de las aplicaciones que ya funcionan: identificadores, imágenes, fechas de inicio y reinicios. Comprueba memoria, disco, nombres de contenedores y resolución del dominio antes de crear el proyecto.

El código se empaqueta desde un commit con `git archive`. Se carga por SSH y se compara su SHA-256. Así se sabe qué versión llegó y se evita copiar el entorno local, una base de desarrollo o un archivo privado por accidente.

### 12.3 Crear configuración privada y la PostgreSQL

`bootstrap.sh` genera secretos aleatorios en el servidor, prepara un certificado exclusivo de base y no imprime contraseñas. El ejemplo `runtime.env.example` enseña los nombres de las variables; sus palabras de referencia no se utilizan como contraseñas reales.

El contenedor PostgreSQL inicializa una base vacía y el rol de la aplicación. Solo sus propios servicios pueden alcanzar la red de datos. No se abre acceso universal al puerto 5432 ni se conectan las migraciones al Supabase de los otros proyectos.

### 12.4 Construir migrar y activar

La orden del administrador tiene esta forma:

```bash
bash deploy/nexostack/deploy.sh SHA_COMPLETO_VERIFICADO
```

`SHA_COMPLETO_VERIFICADO` representa los 40 caracteres del commit que pasó CI. No se copia literalmente esa palabra. El procedimiento se ejecuta como infraestructura confiable en la versión cargada del VPS, no en la terminal de un estudiante.

El script valida Compose, construye la imagen, inicia su base, aplica las dos migraciones, sincroniza cuatro hábitos y comprueba deriva. Después concede los permisos de negocio a la web y activa solo su contenedor. Las migraciones no se ejecutan al visitar una pantalla.

La tarea de migración usa `--no-deps` después de verificar la base, para no recrear una dependencia saludable como efecto de la tarea puntual. Un bloqueo evita dos despliegues de VitaliLab simultáneos. Si hay una versión anterior, se respalda antes de la actualización.

### 12.5 Verificar la publicación con una persona ficticia

1. Abre la dirección HTTPS y verifica estilos, JavaScript y la marca local.
2. Visita `/health` y compara su versión con el commit publicado.
3. Visita `/ready`; una respuesta 200 confirma conexión, no todo el esquema.
4. Crea una cuenta ficticia mediante el formulario real, con CSRF activo.
5. Completa un hábito y observa sus 15 puntos.
6. Repite el POST del mismo hábito en una prueba controlada: debe quedar un cumplimiento.
7. Cierra e inicia sesión; el progreso debe conservarse.
8. Prueba que una cuenta normal no puede entrar a `/admin/`.
9. Con un administrador comprueba borrador, publicación y archivo de un comunicado.
10. Revisa móvil, teclado y errores; reinicia solo la web de VitaliLab y vuelve a comprobar datos.

No intentes saltar las restricciones del navegador en una web ajena. Las pruebas de solicitudes repetidas se hacen únicamente sobre el laboratorio autorizado y con datos ficticios.

### 12.6 Los accesos de Juan y Emanuel

Hay dos cuentas individuales de administrador de aplicación. Permiten gestionar comunicados y ver un resumen de auditoría; no son cuentas administradoras del VPS. Cada persona recibe sus credenciales de forma privada.

También hay dos llaves independientes para gestión básica de infraestructura. El acceso utiliza SSH con un comando forzado: únicamente estado, salud, reinicio de la web, backup y eventos del monitor. No permite una terminal libre, cambiar código, leer secretos, descargar bases o administrar otras aplicaciones.

El administrador agregó solamente esos dos nombres a la lista de usuarios SSH permitidos, conservando los accesos anteriores. Validó la configuración antes de recargar el servicio. Las restricciones de cada llave impiden transferencia de archivos y reenvío de puertos.

La [guía de operación y accesos](18_NEXOSTACK_OPERACION_Y_ACCESOS.md) explica cómo entrar y qué orden corresponde a cada acción. No compartas una llave ni una contraseña entre ambos responsables. Si alguien deja el proyecto, revoca la cuenta de aplicación y su llave: son permisos distintos.

### 12.7 Respaldar restaurar y observar

El timer de VitaliLab produce un respaldo diario a las 02:30 de Colombia, con hasta cinco minutos de variación. Conserva 14 días en la carpeta privada del proyecto. El monitor comprueba `/ready` cada cinco minutos y registra fallos en systemd; esto no significa que ya envíe mensajes personales de alerta.

Un respaldo se comprueba restaurando en otra base, comparando las siete tablas y la revisión Alembic y verificando deriva. En esta entrega se hizo esa prueba y se eliminó únicamente la base temporal; se conservó la base activa y su dump.

Un archivo en el mismo VPS no basta frente a pérdida del servidor. Se debe conservar una copia fuera del host mediante un canal protegido, definir retención y ensayar recuperación. Los objetivos propuestos para laboratorio son RPO de 24 horas y RTO de una hora; no son garantías de disponibilidad ni una prueba de recuperación de todo NexoStack.

### 12.8 Actualizar o regresar sin tocar otro proyecto

Un cambio sigue rama, PR, pruebas y `staging`. Solo después se publica su commit en VitaliLab. Los operadores básicos no despliegan código nuevo ni ejecutan migraciones: eso sigue a cargo de infraestructura.

Para regresar a un código anterior, debe conservarse compatibilidad con el esquema. No ejecutes `db downgrade` ni borres un volumen para arreglar una pantalla. Una restauración real requiere diagnóstico, respaldo y aprobación. No se utilizan limpieza global de Docker, reinicio del proxy ni comandos sobre Mercanta, Murano o Krono 57.

**Para sustentar.** Señala la diferencia entre imagen, contenedor y volumen. Después explica por qué gestionar un comunicado no autoriza entrar al VPS y cómo se demuestra que una versión nueva conservó los datos.

## 13 Render y Vercel como alternativas

### 13.1 El Render histórico queda sin cambios

La aplicación original utiliza el repositorio `ega1026/vitalilab`; la reconstrucción pertenece al repositorio privado `juandigira17111980/vitalilab-profesional`. Compartir permisos del primer repositorio no es lo mismo que reemplazar un servicio publicado.

La base temporal `vitalilab-staging-db` que se creó en Render estaba disponible al 13 de octubre, con acceso externo cerrado y vencimiento el 31 de octubre a las 21:36 de Colombia. No es la base de este laboratorio NexoStack. El servicio web Staging de Render no se creó en esa revisión por el acceso Git pendiente. No se elimina esa base ni se cambia producción como consecuencia de esta publicación.

Render Free puede dormir por inactividad, no aporta backups administrados para PostgreSQL Free y bloquea puertos SMTP 25, 465 y 587. Sus valores de configuración no superan esos límites. Una implementación en Render utiliza `render.yaml`, Gunicorn y una base independiente, con validación propia antes de dar una URL por aprobada.

### 13.2 La configuración Vercel no está en uso

El código conserva una adaptación opcional a Vercel: entrada `wsgi:app`, `vercel.json`, el script que prepara `public/static` y una carpeta temporal al detectar ese runtime. Esa ruta ejecutaría Flask como función administrada y necesitaría PostgreSQL externa accesible con TLS.

NexoStack ejecuta Gunicorn y su PostgreSQL privada. No necesita una cuenta de Vercel, ejecutar `npx vercel login` ni convertir la base Render en pública. No confundas archivos de una alternativa con el proveedor realmente utilizado. La comparación sirve para aprender que una misma aplicación puede tener configuraciones de infraestructura diferentes.

### 13.3 Qué sigue pendiente antes de producción real

La entrega es una copia académica con datos ficticios. SMTP y recepción de correo, alertas personales, automatización offsite, accesibilidad formal y decisiones institucionales de privacidad requieren validación adicional. La existencia de la URL no elimina los límites de fechas por servidor, puntos históricos del catálogo ni sesiones sin revocación global.

La decisión de reemplazar Render con este proyecto es posterior y exige aprobación, ensayo de migración de datos y plan de reversión. No se presenta una demostración de laboratorio como una sustitución productiva ya aprobada.

## 14 Laboratorios con resultados observables

### 14.1 Laboratorio de montaje

Instala desde una copia limpia, configura SQLite, migra y siembra. Abre inicio, `/health` y `/ready`. Produce captura, revisión Alembic y conteo de cuatro hábitos. Para aprobar, un compañero debe reproducir el montaje con tus notas.

### 14.2 Laboratorio de identidad

Registra un usuario ficticio. En la base local consulta únicamente si el hash empieza por el método scrypt, sin mostrarlo completo. Cierra e inicia sesión. Explica por qué el sistema comprueba una contraseña mediante hash y por qué la cookie no debe contenerla.

### 14.3 Laboratorio de integridad

Anota el número inicial de `habit_entries`. Completa una pausa activa, compara el conteo y observa la suma. Repite la acción del día y confirma que sigue habiendo una sola entrada de esa combinación. Explica cómo cooperan servicio y restricción.

### 14.4 Laboratorio de permisos

Con usuario normal intenta entrar a `/admin/`. Con admin crea un comunicado ficticio, deja el borrador, confirma que no aparece públicamente y luego publícalo. Produce evidencia de ambos estados y del 403. Explica por qué ocultar un botón no reemplaza el control por rol.

### 14.5 Laboratorio de frontend

En una rama local cambia un texto de ayuda y una medida CSS pequeña. Revisa escritorio y móvil. Compara `git diff` y revierte manualmente solo tu cambio si falla. No cambies IDs usados por JavaScript sin buscar también sus consumidores.

### 14.6 Laboratorio de modelo de datos

Dibuja las siete entidades con sus claves. Crea ejemplos ficticios en papel y predice si una combinación duplicada sería rechazada. Después compara con el caso de prueba. Para un cambio real de esquema, prepara una migración nueva en una base desechable con revisión del docente; no practiques `downgrade` sobre datos compartidos.

### 14.7 Laboratorio de pruebas

Ejecuta Pytest, interpreta un caso y documenta su preparación, acción y comparación. Señala una propiedad que no comprueba esa prueba. Así demuestras que entiendes el alcance y no solo que viste una línea verde.

### 14.8 Laboratorio de publicación

Completa la lista de NexoStack sobre la copia autorizada, junto al docente. Anota cuál ambiente, qué commit y qué base se usaron. Prueba desde otra sesión de navegador. Para aprobar necesitas persistencia y rol comprobados, no solo que abra la página inicial. No necesitas acceso administrativo al VPS para demostrar una ruta de aplicación.

## 15 Preparar una sustentación que demuestre comprensión

### 15.1 Un guion de treinta minutos

| Minutos | Exposición | Evidencia |
|---|---|---|
| 0 a 3 | Problema y funciones | Inicio y usuarios objetivo |
| 3 a 7 | Prototipo y decisiones de cambio | Comparación antes y después |
| 7 a 12 | Modelo relacional | Diagrama y combinación única |
| 12 a 17 | Registro y hábito de extremo a extremo | Ruta formulario servicio y tabla |
| 17 a 21 | Interfaz y accesibilidad | Plantilla base CSS menú móvil |
| 21 a 25 | Seguridad Git y pruebas | Rol CSRF hash y CI del commit |
| 25 a 29 | Demostración | Hábito sin duplicación y comunicado |
| 29 a 30 | Estado y próximos pasos | Qué está validado y qué falta |

Si el docente asigna menos tiempo, reduce la demostración y conserva el recorrido completo de un caso. Preparar el relato exige seleccionar; leer todos los archivos durante la exposición no demuestra que comprendes sus relaciones.

### 15.2 Cómo responder sin memorizar

Para cada respuesta usa problema, decisión y evidencia. Si preguntan por PostgreSQL, explica primero que la aplicación compartida necesita datos persistentes, después la elección del motor y al final la migración o el ensayo que lo demuestra.

**Por qué siete tablas.** Cada entidad representa una responsabilidad y evita mezclar identidad, catálogo, historial y eventos. Muestra una relación específica.

**Cómo se evita duplicación.** La sesión identifica al usuario, la ruta valida y el servicio consulta. La combinación única de la base resuelve también solicitudes simultáneas.

**Dónde están los puntos.** Se calculan desde cumplimientos y puntos del catálogo. Si cambian los puntos del catálogo, puede cambiar la interpretación histórica; esa consecuencia debe conocerse.

**Qué hace Jinja.** Construye HTML en el servidor con datos de la ruta. El navegador recibe el resultado y aplica CSS y JavaScript.

**Qué es una migración.** Un cambio de esquema versionado que permite reproducir una transición. No es una exportación de usuarios ni una copia de seguridad.

**Cómo funciona la sesión.** Cookie firmada de Flask más usuario cargado de la base. La firma evita modificación silenciosa; no cifra su contenido.

**Por qué persisten los datos en NexoStack.** La web utiliza su PostgreSQL y un volumen separado. Cambiar la imagen de la aplicación no elimina ese volumen. Se demuestra reiniciando únicamente VitaliLab y comprobando el mismo cumplimiento.

**Qué está pendiente.** Una URL nueva validada, correo real, operación de backups, decisiones institucionales y revisión formal de accesibilidad. No declares todos esos puntos resueltos por tener pruebas locales.

### 15.3 Qué debe saber cada integrante

Cada integrante debe montar la copia, explicar una ruta completa y reconocer el esquema. Después pueden especializarse: una persona presenta datos, otra backend, otra interfaz y otra publicación y QA. Nadie debería quedar limitado a leer una diapositiva que no puede relacionar con un archivo.

El docente puede pedir al azar que indiquen dónde se valida un campo, dónde se comprueba el rol y dónde se confirma una transacción. Practiquen encontrar esas respuestas en menos de dos minutos, explicando el razonamiento.

### 15.4 Rúbrica para aprender

| Criterio | Evidencia para aprobar |
|---|---|
| Comprensión | Explica las responsabilidades sin confundir navegador servidor y datos |
| Reproducción | Instala y arranca desde una copia limpia |
| Datos | Dibuja relaciones y predice una restricción |
| Código | Sigue un caso sin saltar de pantalla a base por intuición |
| Práctica | Hace un cambio pequeño y comprueba su efecto |
| Calidad | Explica una prueba y su alcance |
| Honestidad técnica | Distingue preparado probado localmente y publicado |
| Trabajo de equipo | Todos pueden operar y responder sobre el flujo |

Esta rúbrica mide competencias; no asigna automáticamente una nota institucional ni exige memorizar porcentajes. Una sustentación puede ser clara aunque identifique trabajo pendiente, siempre que se describa con evidencia y un plan concreto.

## 16 Ruta para profundizar después del primer dominio

Cuando puedas explicar esta versión, mejora una capacidad por vez. Primero escribe pruebas de límites de formularios y un caso de error. Después diseña un cambio de esquema pequeño y revisa su migración. Luego estudia transacciones concurrentes y cómo ensayar una restauración. Finalmente analiza despliegue, conexiones y monitoreo con una URL real.

Extensiones posibles del proyecto son calcular fechas con la zona del usuario, conservar el puntaje histórico por evento, revocar sesiones después de un cambio de clave, integrar almacenamiento compartido del rate limit y mejorar accesibilidad con herramientas y personas. Son ejercicios futuros; no figuran como funciones ya terminadas.

Para aprender una herramienta, formula una pregunta verificable. Por ejemplo: qué pasa con una segunda inserción concurrente, qué cookie cambia al salir o qué consulta usa el índice. Diseña un experimento en una base de prueba y documenta lo observado. Esa práctica construye criterio técnico.

## 17 Glosario de consulta

| Palabra | Significado en este proyecto |
|---|---|
| Backend | Código Python que atiende solicitudes y aplica reglas |
| Blueprint | Grupo de rutas Flask de un módulo |
| Build | Preparación de dependencias y archivos de una entrega |
| CDN | Red que sirve recursos públicos como CSS y SVG |
| Commit | Versión de cambios registrada por Git |
| Constraint | Regla de integridad exigida por la base |
| CSRF | Defensa para solicitudes de modificación vinculadas a la sesión |
| Deploy | Activación de una versión en el alojamiento |
| Fixture | Preparación reutilizable de una prueba |
| Frontend | Contenido y comportamiento presentado en navegador |
| Hash | Resultado de una función de derivación usado para comprobar la clave |
| Idempotencia | Repetir una acción determinada conserva su resultado de negocio |
| Índice | Estructura que ayuda a localizar filas |
| Jinja | Motor que construye HTML con datos del backend |
| Migración | Transición versionada de estructura de datos |
| ORM | Herramienta que relaciona objetos y tablas y construye consultas |
| Preview | Publicación de revisión antes de promover una versión |
| Pull request | Propuesta de cambios para revisión e integración |
| Rollback | Recuperación de versión o reversión de cambios pendientes según contexto |
| Seed | Carga o sincronización del catálogo inicial |
| Sesión | Estado que permite reconocer al usuario entre peticiones |
| Staging | Ambiente compartido destinado a pruebas |
| Transacción | Grupo de cambios que se confirma o deshace conjuntamente |
| WSGI | Acuerdo entre servidor Python y aplicación web |

## 18 Material de referencia y estado de entrega

El documento maestro y los capítulos técnicos continúan como referencia detallada. Empieza por este manual y consulta después `03_MODELO_DE_DATOS_DBA.md`, `04_BACKEND.md`, `05_FRONTEND_UX.md` y `09_QA_Y_PRUEBAS.md`. La operación actual está en `18_NEXOSTACK_OPERACION_Y_ACCESOS.md`. La guía de sustentación reúne un guion breve; la matriz de trazabilidad enlaza requisitos y evidencia.

Las instrucciones de proveedores se verificaron el 13 de octubre de 2026. Sus pantallas, límites y precios pueden cambiar. Cuando la documentación del proveedor contradiga una receta antigua, compara la versión y valida el cambio en un ambiente de práctica.

Fuentes oficiales para profundizar:

- Python y entornos virtuales: https://docs.python.org/3/library/venv.html
- Tutorial Flask: https://flask.palletsprojects.com/en/stable/tutorial/
- Sesiones Flask: https://flask.palletsprojects.com/en/stable/quickstart/#sessions
- Consultas SQLAlchemy: https://docs.sqlalchemy.org/en/20/tutorial/data_select.html
- Migraciones Flask Migrate: https://flask-migrate.readthedocs.io/en/latest/
- Git y fundamentos: https://git-scm.com/book/es/v2
- Flask en Vercel: https://vercel.com/docs/frameworks/backend/flask
- Runtime Python de Vercel: https://vercel.com/docs/functions/runtimes/python
- Ambientes Vercel: https://vercel.com/docs/deployments/environments
- Flask en Render: https://render.com/docs/deploy-flask
- Conexión Git a Render: https://render.com/docs/git-provider
- Límites Render Free: https://render.com/docs/free

La entrega académica está lista cuando un estudiante puede reproducirla con datos ficticios y explicar las decisiones. La publicación se cierra cuando una URL del commit de entrega pasa el recorrido funcional. La aprobación de producción es un paso posterior del responsable del proyecto.
