# Uso personal sencillo: objetivo, rutinas e IMC opcional

Fecha: 16 de octubre de 2026. Este ajuste sucede a la corrección del mensaje de autorización y resuelve el bloqueo de la experiencia personal sin incorporar un proceso nuevo de autorizaciones.

## Explicación desde cero

Antes se exigía guardar una medición para elegir el objetivo. Una persona menor en uso personal no podía guardar sin autorización y, por esa dependencia, tampoco llegaba a sus rutinas personalizadas. Elegir «energía», «postura» o «fuerza» no necesita guardar peso ni altura.

Separamos dos acciones: preparar un plan de movimiento y guardar un historial de mediciones. La primera puede hacerse sin la segunda.

## Qué hace ahora la persona usuaria

1. Inicia sesión con su cuenta personal.
2. Abre **Rutinas → Personalizar mi espacio**, o **Mi perfil → Personalizar mis rutinas**.
3. Elige su objetivo y cómo prefiere moverse.
4. Pulsa **Guardar mi objetivo y ver rutinas**.
5. Consulta las opciones, crea su rutina o registra una actividad como antes.

No necesita colegio, grupo, peso, altura ni fecha de nacimiento para ese recorrido. Tampoco debe cambiar su fecha verdadera para continuar. El objetivo y la preferencia pueden actualizarse después.

## Consulta opcional del IMC

**Consultar mi IMC (opcional)** permanece cerrado hasta que la persona quiera usarlo. Introduce peso en kilogramos y altura en centímetros; el navegador calcula `peso / (altura / 100)²` y muestra el número.

Con 58 kg y 174 cm el resultado es 19,16. El ejemplo explica la operación; no clasifica el cuerpo ni indica ejercicios. La consulta no interpreta referencias infantiles ni asigna rangos clínicos.

Los campos no tienen atributo `name` y están fuera del formulario del objetivo. El botón es `type="button"`: no envía un formulario. JavaScript no utiliza peticiones, cookies, almacenamiento local ni sesión para esos valores. Al abandonar la página se limpian los campos y el resultado. Esto no controla capturas o almacenamiento ajenos a la aplicación, como una fotografía tomada por la persona.

Sin JavaScript la consulta no calcula, pero elegir el objetivo y usar las rutinas sigue funcionando con el formulario normal. El resultado opcional no filtra rutinas ni otorga puntos.

## Diferencia con guardar un historial

Consultar localmente no crea una fila en `health_measurements`. Guardar un historial sigue siendo una acción diferente y conserva su validación de permiso y confirmación.

Este ajuste no habilita almacenamiento de mediciones de menores sin autorización, no fabrica consentimiento y no concede permisos escolares. La falta de permiso de almacenamiento ya no impide preparar el plan personal. En el perfil, el historial opcional queda en un apartado desplegable. No se presenta una tarjeta vacía si una cuenta personal no tiene mediciones. Los registros anteriores se conservan.

## Qué se guarda en PostgreSQL al elegir el objetivo

Solo se actualizan las preferencias correspondientes de `user_profiles`: `movement_goal`, `movement_preference`, `personalization_completed_at` y el `updated_at` normal del perfil. Se registra el evento técnico en `audit_events`, sin copiar medidas. No se activa `measurement_consent_at` al elegir un objetivo.

No se crean columnas o tablas. El modelo conserva sus 17 entidades de negocio, 148 campos y 22 claves foráneas; la tabla técnica de migraciones tampoco cambia.

## El modo institucional mantiene sus requisitos

`personalization_ready()` distingue los modos. En uso personal comprueba el objetivo completado. En institucional exige también medición, confirmación y permiso vigente.

Completar primero un plan personal y después vincularse como estudiante no sustituye la revisión escolar. Enviar `usage_mode=personal` al formulario del objetivo tampoco cambia el modo: solo se aceptan objetivo y preferencia. Hábitos y biblioteca general siguen disponibles mientras se revisa una vinculación.

## Archivos para estudiar

- `app/profile/routes.py`: objetivo personal sin medición y validaciones de guardado independientes.
- `app/services/personalization.py`: estado del plan distinto del permiso de almacenamiento.
- `app/wellness/routes.py`: acceso al catálogo filtrado según el estado correcto.
- `app/templates/profile/setup_goal.html`: recorrido personal de dos pasos.
- `app/templates/profile/_bmi_preview.html`: consulta opcional fuera del formulario.
- `app/static/js/personalization.js`: cálculo local y limpieza al salir.
- `tests/test_personal_plan.py`: plan sin mediciones, puntos, datos adicionales ignorados y separación escolar.

## Práctica de sustentación

Crear una cuenta personal de prueba. Elegir un objetivo sin introducir medidas y comprobar que aparecen rutinas. Abrir la consulta del IMC y calcular el ejemplo. La tabla `health_measurements` no debe recibir filas por esa consulta. Registrar una rutina utiliza los puntos existentes; consultar IMC no suma puntos.

Guion: «Personalizamos con el objetivo y la preferencia, no con el peso. El IMC opcional se calcula en el navegador sin almacenarse. Un historial utiliza otra acción protegida. Quitamos una dependencia innecesaria sin quitar permisos ni mezclar el uso personal con el escolar».

## Verificación y límites

184 pruebas locales aprobadas, cobertura 95,07 %. Se incluyen accesos por edad, datos extra en el objetivo y cambio posterior a modo escolar. Persisten cinco avisos de deprecación existentes. Ruff, sintaxis JavaScript y análisis estático forman parte de la validación.

Navegador Chromium local con datos sintéticos y CSRF activo: ejemplo 58/174 → 19,16; decimal con coma; rechazo de vacío, NaN, infinito, altura cero y unidades equivocadas. El observador de red no recibió peticiones durante el cálculo. No se utilizaron datos de cuentas reales para estos ensayos.

Revisión funcional focalizada, no estudio clínico, pentest ni certificación general de producción. La verificación móvil por viewport y la publicación remota se registran aparte tras ejecutarlas; no se requieren migraciones.
