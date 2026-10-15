# Dos enfoques de perfil, explicados desde cero

Fecha: 14 de octubre de 2026. Alcance: preferencia individual de perfil, no plataforma institucional multiusuario.

## 1. Qué problema resolvemos

Antes, todas las personas veían «Grado o grupo». Esa pregunta tiene sentido en una institución, pero no necesariamente para alguien que cuida sus hábitos por cuenta propia. Ahora la persona elige el contexto de uso sin crear otra cuenta.

| Elección | Qué permite | Qué no cambia |
|---|---|---|
| Uso personal | Usar hábitos, metas, rutinas y progreso sin pedir contexto institucional | Su cuenta e historial |
| Uso institucional | Añadir institución y grado, grupo o área, ambos opcionales | Su cuenta, historial y permisos |

Una preferencia **describe** cómo usas el producto. Un rol **autoriza** lo que puedes hacer. No son lo mismo. Seleccionar «institucional» no convierte a nadie en administrador, docente ni miembro verificado de una institución.

## 2. Paso a paso para la persona usuaria

1. Ingresa con tu cuenta y abre **Mi cuenta → Mi perfil**.
2. Elige **Uso personal** o **Uso institucional**.
3. En personal, con JavaScript activo, no se muestran ni envían los campos de institución y grupo.
4. En institucional, puedes completar institución y grado/grupo/área; no es obligatorio. No escribas información sensible en estos campos.
5. Pulsa **Guardar cambios**. Al recargar, la elección permanece.
6. Puedes alternar sin perder hábitos, metas, bitácoras ni medidas.

Para evitar borrar información por accidente, pasar a personal conserva el contexto institucional que ya estaba guardado, aunque no lo muestra. Para eliminar ese contexto, selecciona institucional, vacía los dos campos y guarda. Puedes regresar después a personal.

Sin JavaScript, ambos campos permanecen visibles con una explicación de que solo aplican al enfoque institucional. El servidor sigue validando la elección e ignora esos campos cuando guardas en personal: la seguridad no depende del navegador.

## 3. Qué recorre el código al guardar

1. `app/templates/profile/edit.html` muestra dos opciones nativas de radio con etiquetas clicables y navegación por teclado.
2. `app/static/js/app.js` escucha la elección, muestra u oculta el bloque institucional y lo deshabilita al usar personal. También sincroniza el estado al restaurar la página con el botón Atrás.
3. El formulario hace POST a `/perfil/` con protección CSRF.
4. `ProfileForm` en `app/forms.py` solo acepta `personal` o `institutional`, valida longitudes y recorta espacios de institución/grupo.
5. `app/profile/routes.py` obtiene el perfil de la sesión autenticada, nunca de un identificador enviado por el cliente. Guarda solo campos permitidos. Solo modifica institución/grupo si el enfoque es institucional.
6. SQLAlchemy actualiza `user_profiles`. La base también restringe los valores del modo.
7. La auditoría registra `profile.updated` con el modo; no copia el nombre de institución ni el grupo al registro de auditoría.
8. El servidor redirige al perfil (patrón POST-Redirect-GET), para que recargar no reenvíe el formulario. La tarjeta del panel identifica el enfoque guardado.

## 4. Qué cambia en la base de datos

Motor compartido: PostgreSQL 18, carga transaccional y modelo relacional. Desarrollo/pruebas: SQLite. No cambiamos de motor ni añadimos tablas.

| Columna de `user_profiles` | Regla | Motivo |
|---|---|---|
| `usage_mode` | VARCHAR(20), NOT NULL, DEFAULT `personal`, CHECK de dos valores | Preferencia persistente y validada |
| `institution_name` | VARCHAR(160), opcional | Contexto que la persona declara |
| `grade` (ya existía) | VARCHAR(80), opcional | Reutiliza grado, grupo o área sin duplicarlo |

La migración nueva es `7ca6e014b982`, sucesora de `54e1c8bb7901`. Agrega dos columnas y una restricción. Conserva los valores antiguos: si ya había un grupo no vacío, propone modo institucional; para los demás, personal. No inventa un nombre de institución ni verifica pertenencia. Cada persona puede corregir esa preferencia.

No añadimos índices porque el perfil se busca por su clave primaria `user_id`; no hay una consulta por modo que justifique otro índice. El nombre de institución no es un `institution_id`: aún no hay membresías ni administración de organizaciones.

## 5. Cómo probarlo y sustentarlo

Practica con cuentas ficticias, no con las de Juan o Emanuel:

1. Comprueba que una cuenta nueva empiece en personal.
2. Selecciona institucional y guarda «Instituto de práctica», «Grupo A».
3. Recarga y verifica los tres valores.
4. Cambia a personal; comprueba que se oculte el bloque y que continúen tus hábitos/metas.
5. Regresa a institucional: los datos anteriores deben seguir ahí.
6. Vacía institución y grupo y guarda: ahora deben quedar vacíos.
7. Repite a 390 px y en escritorio. Prueba Tab, flechas del grupo de radios y botón Guardar.

`tests/test_profile_modes.py` cubre valores por defecto, persistencia, limpieza explícita, preservación al alternar, entradas inválidas, longitudes, CSRF, sesión, ausencia de escalamiento de permisos y migración con grupos históricos. El CI también comprueba modos y CHECK en PostgreSQL mediante `scripts/verify_postgres_release.py`, deriva de esquema y backup/restore.

Pregunta de sustentación: **«¿Por qué una persona que escribe el nombre de una institución no puede ver los datos de otras personas?»** Respuesta: porque eso solo guarda contexto en su perfil; no crea membresías ni cambia las comprobaciones de autorización del servidor.

## 6. Publicación y reversión

Se usa rama de funcionalidad, PR hacia `staging`, CI y publicación aislada de VitaliLab en NexoStack. Antes de aplicar la migración, el procedimiento de despliegue genera un respaldo. La revisión debe coincidir con `flask db current` y `flask db check` no debe mostrar deriva. `/health` identifica el commit publicado y `/ready` comprueba disponibilidad de base de datos.

Si se revierte la interfaz, se conserva el esquema ampliado y se vuelve a la versión compatible anterior. **No se ejecuta downgrade sobre datos vivos**: eliminaría las dos columnas nuevas. El downgrade solo sirve para bases desechables. No se toca `main`, Render original ni otros servicios del VPS.

## 7. Qué queda fuera de esta entrega

No se implementan organizaciones reales, invitaciones, panel de docentes, informes grupales, pagos ni aislamiento multitenant. Esas funciones necesitan un alcance separado: identidad institucional verificable, membresías, roles, consentimiento y permisos de lectura por organización. El selector no se presenta como sustituto de esos controles.
