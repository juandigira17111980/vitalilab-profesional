# Guía de funciones y QA de la evolución premium

13 de octubre de 2026, Colombia. Esta guía complementa el manual desde cero: el núcleo original conserva sus siete entidades y se amplía con dos. El proyecto actual tiene nueve tablas de negocio, tres revisiones Alembic, ocho hábitos y seis rutinas. La nueva guía no declara facturación, organizaciones ni asesoría clínica implementadas.

## Qué cambió para la persona

| Espacio | Qué puedes hacer | Dónde se conserva |
|---|---|---|
| Hoy | Registrar un hábito sin salir del panel, consultar tus metas y elegir una pausa | habit_entries y user_goals |
| Hábitos | Elegir entre ocho acciones, sin obligación de completarlas todas | habits y habit_entries |
| Metas | Crear, ajustar o retirar una frecuencia por hábito | user_goals |
| Bitácora | Registrar energía y enfoque percibidos, con actualización del mismo día | daily_checkins |
| Progreso | Consultar actividad de 28 días y metas de los últimos siete | Consultas del servidor; no guarda otra copia de los totales |
| Rutinas | Buscar seis actividades y usar sus temporizadores sin cuenta | Catálogo editorial versionado; reloj local del navegador |

El inicio público muestra un ejemplo identificado como tal, no estadísticas de otra persona. El IMC no desaparece: su calculadora se traslada al contenido de indicadores educativos, accesible desde el pie de página. La privacidad sigue disponible y el registro exige consentimiento, pero los mensajes principales presentan las herramientas.

## Práctica paso a paso

En local, usa datos ficticios. El montaje del manual sigue siendo válido: entorno Python 3.13, variables de desarrollo, instalación de requirements, `db upgrade`, `seed-habits` y arranque. `tzdata` se declara para que Windows y Linux interpreten las mismas zonas IANA. No necesitas la cuenta del VPS ni las credenciales de Juan o Emanuel.

1. Crea una cuenta ficticia. En Hoy, registra una hidratación: comprueba confirmación, puntos y permanencia en el mismo panel.
2. En Metas, elige hidratación y tres días. Guarda. Si la registraste hoy, debe aparecer un día de avance. Elige el mismo hábito y dos días: debe cambiar la meta, no aparecer otra tarjeta del mismo hábito.
3. Registra energía 2 y enfoque 4 en Bitácora. Guarda otra vez con energía 4: debe existir una sola fila del día, con el valor nuevo.
4. Abre Progreso. Comprueba que hay 28 fechas, que el día del registro tiene una acción y que el objetivo de hidratación continúa visible. No se infieren causas ni diagnósticos desde la bitácora.
5. En Rutinas, filtra por Descanso y luego busca «pantalla». Cambia el filtro o vuelve a Todas si no hay resultados.
6. Prueba Un minuto para volver a ti. Comienza, pausa, espera y continúa: durante la pausa el número no debe cambiar. Reinicia: debe volver a 01:00. El reloj no registra automáticamente un hábito.
7. Retira tu meta y acepta la confirmación. Comprueba que desaparece la tarjeta, pero tu hábito y tus puntos permanecen.
8. Cierra sesión y crea otro usuario ficticio. Sus metas y su bitácora deben estar vacías. Copiar el identificador de una meta ajena no concede acceso: el servidor debe responder 404 a su eliminación.

Para sustentar, explica qué parte calculó el navegador y cuál el servidor. El temporizador no requiere base; la meta necesita persistencia, integridad y autorización. Una tarjeta visible es solo presentación: la prueba importante incluye volver a entrar y comprobar el dato.

## Cómo sigue el dato desde la pantalla

### Meta

`GoalForm` valida que el hábito pertenece al catálogo activo y que la frecuencia es de uno a siete días. La ruta `wellness.goals` toma al usuario de la sesión; no acepta un usuario enviado por el formulario. `save_goal` consulta la combinación usuario/hábito y crea o actualiza. La restricción única protege también frente a dos solicitudes simultáneas.

`goals_for` cuenta los cumplimientos de ese hábito desde hoy menos seis días hasta hoy, según la zona del perfil. No suma actividad de otra persona ni registros anteriores a esa ventana. El porcentaje visual se limita a 100; los días registrados reales siguen visibles si superan el objetivo. Retirar una meta no elimina HabitEntry: son entidades distintas.

### Bitácora

`CheckInForm` acepta únicamente valores 1 a 5. `save_checkin` utiliza la fecha del usuario y la combinación usuario/fecha. Una segunda escritura normal actualiza la misma fila. La auditoría registra que hubo un cambio, pero no guarda energía ni enfoque en sus metadatos. No se añade un campo de texto libre sensible.

La aplicación no ofrece la bitácora a otros usuarios ni al panel de administración. Esto no impide el acceso de un administrador autorizado de infraestructura a una base o un respaldo: «solo tú» describe el acceso ordinario en la aplicación, no cifrado extremo a extremo. El laboratorio requiere datos ficticios.

### Rutina

`app/wellness/catalog.py` es el catálogo editorial. Las rutas públicas solo filtran y presentan ese contenido. `wellness.js` mantiene un tiempo límite y recalcula lo que queda; no resta un segundo por cada llamada del navegador, porque una pestaña en segundo plano puede retrasar llamadas. Pausar conserva lo restante; reiniciar recupera la duración inicial. Un reloj no prueba que una persona haya realizado la acción.

### Fechas y progreso

`app/services/clock.py` calcula la fecha con la zona del perfil y vuelve a America/Bogota si una zona no se encuentra. Hábitos, metas, bitácora y nuevas mediciones usan ese límite diario. La prueba de medianoche utiliza el mismo instante UTC y comprueba fechas distintas en Bogotá y Tokio. Las fechas históricas guardadas no se reescriben.

## Diccionario de las dos entidades nuevas

| Campo | Tipo | Función y regla |
|---|---|---|
| user_goals.id | Integer PK | Identificador de la meta |
| user_goals.user_id | Integer FK NOT NULL | Dueño; referencia users con CASCADE |
| user_goals.habit_id | Integer FK NOT NULL | Hábito; referencia habits con RESTRICT |
| user_goals.target_days | Integer NOT NULL | Frecuencia objetivo, CHECK entre 1 y 7 |
| user_goals.created_at y updated_at | DateTime NOT NULL | Timestamps UTC convencionales del proyecto |
| daily_checkins.id | Integer PK | Identificador del registro |
| daily_checkins.user_id | Integer FK NOT NULL | Dueño; referencia users con CASCADE |
| daily_checkins.checked_on | Date NOT NULL | Fecha de la persona al registrar |
| daily_checkins.energy y focus | Integer NOT NULL | Percepciones en escala 1 a 5, con CHECK |
| daily_checkins.created_at y updated_at | DateTime NOT NULL | Creación y actualización |

UNIQUE(user_id, habit_id) y UNIQUE(user_id, checked_on) evitan duplicados y crean índices útiles para consultas por usuario. El nuevo esquema normaliza objetivos y percepciones en responsabilidades separadas; no mete listas JSON dentro de users ni duplica los totales del progreso.

Migración: `54e1c8bb7901`, después de `208469fd48ef`. Agrega dos tablas sin alterar las siete originales. En producción o laboratorio con registros no se ejecuta downgrade para volver al frontend anterior: se vuelve al código compatible y se dejan las tablas adicionales. Un downgrade borra las metas y bitácoras y se reserva a bases desechables.

## Contratos y archivos

| Ruta | Método | Acceso | Efecto |
|---|---|---|---|
| /metas/ | GET, POST | Sesión | Listar las propias y guardar una frecuencia válida |
| /metas/id/eliminar | POST | Sesión, CSRF, propiedad | Retirar una meta propia, 404 si no existe para esa persona |
| /bitacora/ | GET, POST | Sesión | Consultar registros propios y guardar el día |
| /progreso/ | GET | Sesión | Actividad propia de 28 días |
| /rutinas/ | GET | Público | Buscar y filtrar contenido |
| /rutinas/slug/ | GET | Público | Instrucciones y temporizador; 404 para slug desconocido |

Rutas: `app/wellness/routes.py`. Casos de uso: `app/services/wellness.py`. Modelo: `app/models.py`. Formularios: `app/forms.py`. Plantillas: `app/templates/wellness`. Diseño común: `app/static/css/premium.css`; iconos: macro SVG propia. El CSS de producto se carga después del CSS base y sus URLs incorporan la versión de la aplicación para evitar mostrar una hoja vieja después del despliegue.

## Informe QA por área

La auditoría combina revisión de repositorio y navegador, no es solo documental. La revisión profunda cubre cambios nuevos, rutas privadas, validación, CSRF, propiedad, datos, migración y pantallas principales. Seguridad e infraestructura anteriores se revisan por muestreo; no se sustituye pentest, auditoría clínica ni prueba de carga.

| Área | Estado de cierre local | Evidencia |
|---|---|---|
| Arquitectura | Coherente con el monolito modular | Blueprint, servicios, modelos y plantillas separados |
| DBA | Nueve entidades, migración aditiva sin deriva local | upgrade y db check sobre una SQLite nueva |
| Backend | Validación, sesión, CSRF y propiedad comprobados | 42 pruebas; rangos, duplicados, conflicto de escritura y acceso ajeno |
| Frontend y UX | Sin hallazgos automáticos en pantallas ensayadas | 45 combinaciones por motor, Chromium y WebKit; 320, 360, 390, 768 y 1440 px |
| Accesibilidad automática | Sin violaciones detectadas del conjunto ejecutado | axe en nueve pantallas a 390 y 1440 por motor; no equivale a conformidad total |
| Seguridad estática | Sin hallazgos medios/altos detectados | Ruff y Bandit; cabeceras y controles conservados |
| Infraestructura | Preparada para actualizar solo VitaliLab | Permisos DML de dos tablas nuevas, backup previo y esquema compatible |
| Publicación | Gate posterior al cierre local | Exige CI PostgreSQL/Docker, versión activa, flujos reales y comparación de contenedores |

Cobertura local: 91,75 %, umbral 85 %. Una advertencia de deprecación de Flask-Login procede de la dependencia, no de un fallo de las 42 pruebas. CI ejercita las dos entidades en una PostgreSQL desechable llamada exactamente vitalilab_test y compara los nueve conteos en el restore; el script rechaza otro destino antes de escribir.

WebKit mantuvo centrado el anillo y operó el temporizador: 00:50 en marcha, 00:50 después de pausar, 00:00 al terminar y 01:00 al reiniciar. El recorrido por teclado mostró un foco sólido de 3 px. Los controles principales se diseñan para 44 px, como objetivo más conservador que el mínimo AA de 24 px y sus excepciones. La instrumentación automática de WebKit puede intentar insertar estilos que CSP rechaza; navegación normal se comprobó por separado sin eliminar CSP. No se prueba un iPhone físico con este ensayo.

Lighthouse inicial sobre NexoStack: rendimiento 98, accesibilidad 96, buenas prácticas 100, SEO 100, LCP 1,34 segundos y CLS 0 en esa ejecución de laboratorio. La medición de la versión nueva se realiza sobre la misma URL después de publicar; no se extrapola a INP de usuarios reales ni se atribuye mejora comercial a esos números.

## Hallazgos pendientes y preparación comercial

No se asigna una nota 100/100 a toda la plataforma. Para el objetivo de SaaS comercial, la calibración usa el perfil de datos personales sensibles: crítico resta 35, alto sin plan 15, alto con plan formal 3, medio 2 y bajo 0,5. Este corte comercial no permite producción masiva:

| Código | Hallazgo abierto | Nivel | Responsable y plan | Bloquea venta masiva |
|---|---|---|---|---|
| COM01 | Privacidad institucional y autorización de datos sensibles/menores pendientes | Alto con plan | Negocio/seguridad: finalidad, minimización, consentimiento, retención y revisión especializada antes del piloto real | Sí |
| COM02 | Recuperación por correo real y revocación global de sesiones incompletas | Alto con plan | Backend/infra: SMTP probado y versión de sesión revocable, con pruebas de cuentas existentes | Sí |
| COM03 | Organizaciones, aislamiento tenant y facturación no implementados | Alto con plan | Arquitectura/DBA/backend: diseñar contratos y autorización; pruebas cruzadas antes de habilitar instituciones | Sí |
| COM04 | Offsite recurrente, avisos personales y capacidad a escala no validados | Alto con plan | Infra/QA: destino externo, ensayo de recuperación y carga sin afectar VPS compartido | Sí |
| COM05 | Validación formal con personas, lectores de pantalla e iPhone físico pendiente | Medio | UX/QA: cinco participantes, tareas y revisión asistiva; repetir correcciones | No para el laboratorio |
| COM06 | Puntos históricos siguen dependiendo del valor actual del catálogo | Medio | DBA/backend: snapshot de puntos por cumplimiento y migración para reglas comerciales futuras | No para el laboratorio |

Score comercial de este corte: 100 menos 4 × 3 menos 2 × 2 = 84/100, apto con observaciones en la rúbrica pero con gates comerciales bloqueados. El plan documentado reduce la deducción, no convierte un pendiente en resuelto. El laboratorio usa datos ficticios y no presenta planes comerciales. La aceptación de esta entrega corresponde a demo y aprendizaje tras el gate remoto, no a sustitución de Render.

## Lista para entregar y sustentar

Comprueba el commit de `/health`, CI del PR, `/ready`, los ocho hábitos, persistencia de metas y bitácora, timer y vista móvil. No compartas credenciales de gestores con alumnos. Conserva capturas y un relato de una acción desde formulario hasta restricción SQL. Los accesos de Juan y Emanuel siguen individuales; la publicación no necesita entregar administración global del VPS.
