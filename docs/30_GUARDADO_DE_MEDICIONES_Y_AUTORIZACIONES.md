# Guardado de mediciones: qué significa la autorización pendiente

Fecha: 16 de octubre de 2026. Alcance: corrección puntual del formulario de perfil y del inicio de personalización. No modifica tablas, historial, permisos institucionales ni fórmulas.

## Explicación sencilla

El cálculo y el permiso para guardar son cosas diferentes. El peso y la altura pueden ser números válidos y, aun así, el sistema impedir su almacenamiento porque falta una autorización. Cambiar los números no resuelve ese paso.

La captura reportada muestra una fecha de nacimiento que corresponde a una persona menor de edad. Antes de este ajuste, si la cuenta aún no tenía fecha guardada, el formulario aparecía habilitado. Al enviar la nueva fecha, el servidor detectaba la minoría de edad y bloqueaba correctamente el guardado, pero ponía un mensaje genérico sobre la institución debajo del peso. La pantalla seguía usando la fecha anterior para decidir qué mostrar. Ese comportamiento era confuso, especialmente en uso personal.

El diagnóstico del código no identifica una cuenta concreta ni demuestra por sí mismo qué autorización le falta a esa persona. Se necesita consultar su vinculación con una cuenta administrativa autorizada; no se alteran cuentas a partir de una captura.

## Qué se corrigió

1. El servidor valida los datos y calcula el estado de acceso con la fecha enviada cuando esta es válida.
2. El resultado distingue permiso habilitado, solicitud pendiente, vinculación retirada o no aprobada, colegio inactivo, revisión incompleta y grupo no disponible.
3. El impedimento aparece como un estado de autorización, no como un error numérico en el peso.
4. El inicio de personalización conserva los datos del intento en un apartado desplegable para corregir errores de escritura. No los guarda en la base mientras el permiso falte.
5. El aviso enlaza a la vinculación o a la corrección de fecha, según corresponda. Hábitos y rutinas generales siguen disponibles.

No se convierte una casilla del usuario en aprobación institucional. No se inventa autorización de un representante ni se conceden permisos docentes.

## Si es un estudiante: pasos del usuario

1. Abrir **Mi cuenta → Mi colegio**, o `/colegios/`.
2. Consultar el estado de la solicitud. Si no existe, escribir el colegio, grupo y rol reales para solicitar la vinculación.
3. Pedir al responsable que revise identidad, pertenencia y autorizaciones mediante el procedimiento institucional.
4. Una vez aprobada la vinculación y asignado un grupo activo, volver a **Personalizar mis rutinas**.
5. Introducir los datos reales, confirmar el guardado y continuar con el objetivo.

Elegir un colegio o marcar una casilla no sustituye el paso 3. No debe cambiarse la fecha real para eludirlo.

## Pasos de la administración

1. Ingresar con una cuenta individual que ya tenga rol administrativo. No compartir su contraseña con el estudiante.
2. Abrir **Administración escolar**, `/admin/colegios/`.
3. Si la solicitud se escribió manualmente, abrir la revisión de esa solicitud. Elegir el colegio verificado y el grupo activo correspondiente. Si no existen, crearlos primero desde la misma administración.
4. Comprobar identidad, pertenencia y autorizaciones fuera del formulario, conforme al procedimiento acordado. Solo después marcar la confirmación y aprobar.
5. En una solicitud de catálogo pendiente, abrir su revisión, asignar el grupo del mismo colegio y aprobar tras la comprobación.
6. Si una vinculación antigua figura aprobada pero tiene una revisión incompleta, no parchear indicadores directamente con SQL. Revisar el caso por el flujo administrativo; si hace falta sustituirla, retirarla y solicitar una nueva vinculación verificada. La retirada conserva el historial, pero desactiva el acceso escolar y la aportación a estadísticas. No retirar una cuenta sin informar al responsable.
7. Comprobar que el estudiante puede guardar. La aprobación no activa automáticamente la aportación a estadísticas; esa preferencia sigue siendo separada.

Las acciones administrativas requieren permisos y CSRF. Una persona usuaria normal no puede aprobar su propia vinculación.

## Si el uso es personal y la persona es menor

La versión actual no tiene un flujo independiente de autorización del representante para menores sin vinculación institucional. El guardado continúa bloqueado en ese caso. No se obliga a declarar un colegio ficticio para continuar, ni se promete que contactar a administración active un flujo que aún no existe.

Si la fecha se escribió mal, puede corregirse con la fecha verdadera. Si es correcta, siguen disponibles los hábitos y las rutinas generales. Incorporar autorización independiente para uso personal requeriría definir responsables, procedimiento, evidencias, revocación y tratamiento de datos; no forma parte de este arreglo puntual.

## Guion para sustentar

«El navegador recoge los datos; el backend comprueba si pueden guardarse. Una fecha nueva puede revelar que se trata de un menor. En ese caso no basta una casilla: se verifica la vinculación, la revisión y el grupo. Corregimos cómo se explica el impedimento, sin quitar el control. Si falta autorización, no se inserta una medición, no se activa el consentimiento y no se completan las rutinas personalizadas por ese intento».

## Evidencia y límites

- `tests/test_measurement_access.py`: primer envío de fecha de menor, corrección legítima, conservación temporal del intento, estados administrativos y guardado tras revisión válida.
- Pruebas previas de personalización, mediciones, privacidad y accesos se conservan.
- Se verifica que no se conceda participación en estadísticas automáticamente y que las respuestas privadas no se almacenen en caché.
- La revisión es funcional y focalizada; no certifica cumplimiento legal ni sustituye la validación institucional de autorizaciones.
- La verificación local, la integración y la publicación remota se registran por separado; este texto no las da por completadas antes de ejecutarlas.

### Resultado local de esta corrección

- 178 pruebas aprobadas; cobertura de aplicación 94,98 %. El servicio de personalización tiene cobertura completa en esta ejecución. Persisten cinco avisos de deprecación previamente existentes de dependencias y migraciones.
- Ruff y análisis estático Bandit sin hallazgos en la ejecución del arreglo.
- Navegador Chromium con base sintética en memoria y CSRF activo: reproducción del primer envío con fecha de menor, mensaje contextual y conservación de los campos para corrección.
- Anchuras 320, 390, 768 y 1366 píxeles: el documento no desborda horizontalmente en la pantalla revisada. Son pruebas de viewport de escritorio, no una certificación de dispositivos físicos.
- La autorización institucional sigue siendo una acción humana independiente de publicar esta corrección.
