# Guía del docente y evidencias de aprendizaje

El [manual desde cero](15_MANUAL_DE_APRENDIZAJE_Y_SUSTENTACION.md) permite que estudiantes con primeros fundamentos recorran una aplicación completa. Esta guía ayuda a acompañar las prácticas y evaluar comprensión, sin exigir que memoricen definiciones ni una calificación técnica del producto.

## 1 Preparar la primera sesión

Entregue el PDF y una copia del código de la misma versión. Si el estudiante recibe un ZIP, recuerde que puede ejecutar el código pero no incluye el historial Git. Compruebe Python 3.13 y una carpeta de trabajo propia.

Use SQLite local para la primera práctica y correos ficticios. Reserve PostgreSQL y Vercel para la etapa de despliegue. No entregue un `.env` real, contraseñas administrativas compartidas o una copia de datos de la institución.

Pida una bitácora por estudiante. Cada evidencia debe incluir acción, resultado observado y explicación. Si se trabaja en parejas, intercambie quién ejecuta y quién explica.

## 2 Plan de ocho sesiones

| Sesión | Contenido | Actividad | Criterio para continuar |
|---|---|---|---|
| 1 | Archivos Python y petición web | Dibujar navegador servidor y datos | Distingue qué ejecuta cada pieza |
| 2 | Montaje Windows | Entorno migración seed y arranque | Repite instalación sin configuración ajena |
| 3 | Datos | Diagrama de siete tablas y registros en papel | Explica claves y duplicado diario |
| 4 | Backend | Recorrido de registro y hábito | Localiza ruta formulario servicio y modelo |
| 5 | Frontend | Cambio de texto y navegación móvil | Diferencia Jinja CSS y JavaScript |
| 6 | Calidad y Git | Prueba diff commit y revisión | Relaciona evidencia con versión |
| 7 | Publicación | Preparar Preview con docente | Explica variables persistencia y límites |
| 8 | Sustentación | Demo y preguntas al azar | Todos operan y responden sobre un flujo |

Las sesiones orientan el orden, no una promesa de dominio en ocho horas. Ajuste la duración al nivel del grupo y repita los ejercicios que no puedan explicar.

## 3 Resultados de referencia

Después de migrar, `db current` debe mostrar `208469fd48ef`. Después de sembrar una base nueva hay cuatro hábitos. Repetir el seed crea cero hábitos adicionales. Los puntos iniciales son 15, 15, 15 y 10; una entrada de cada hábito suma 55.

Una combinación usuario hábito fecha repetida debe dejar un cumplimiento. Usuarios distintos y fechas distintas sí pueden producir otros. Pida que el estudiante prediga antes de ejecutar.

Un usuario autenticado normal recibe 403 en `/admin/`; un visitante sin sesión normalmente es redirigido al acceso. No son el mismo caso. Un comunicado en borrador no debe aparecer en inicio; al publicarlo sí.

Una medida validada guarda el cálculo del servidor. Enviar solo peso o solo altura debe mostrar validación. Cambiar un texto de plantilla no debe crear una tabla nueva.

`/health` confirma proceso y `/ready` ejecuta una consulta de conexión. Ninguno sustituye la prueba de registro, sesión y consultas de la aplicación.

## 4 Preguntas para detectar comprensión

1. Señale qué función maneja el botón de completar un hábito.
2. Explique por qué `current_user` es preferible a aceptar un usuario enviado por el formulario.
3. Dibuje un caso rechazado por UNIQUE y otro permitido.
4. Explique por qué la consulta previa no basta con solicitudes simultáneas.
5. Compare `flush`, `commit` y `rollback` dentro del recorrido del registro.
6. Muestre dónde se construye HTML y dónde se ejecuta el menú.
7. Explique por qué guardar un token CSRF no sustituye comprobar el rol.
8. Distinga firma de cookie y cifrado de contenido.
9. Prediga qué sucede con el puntaje histórico si cambia el catálogo.
10. Explique por qué un Preview de Vercel necesita PostgreSQL externa.
11. Identifique qué pasos prepara el build y cuáles cambian la base.
12. Señale una comprobación que todavía debe hacerse en la URL real.

Espere ejemplos y referencias a archivos, no respuestas idénticas a la guía. Si alguien recita que se utiliza Clean Architecture completa, JWT, React o una tabla de sesiones, pídale evidencia: esta implementación no usa esas capacidades.

## 5 Plan B para la sustentación

Mantenga una copia local probada y cuentas ficticias preparadas. Si falla internet, demuestre localmente e identifique el ambiente en voz alta. Conserve capturas de roles, idempotencia y CI del commit como apoyo, sin presentarlas como un despliegue nuevo en vivo.

Si todavía no hay proveedor de correo, explique y demuestre las pruebas del transporte y de los tokens; no prometa que llegó un correo real. Si no hay conformidad WCAG formal, muestre los controles implementados y declare la revisión pendiente.

## 6 Evidencia mínima por estudiante

- Montaje propio y revisión Alembic.
- Diagrama de entidades con claves y relación diaria.
- Recorrido escrito de una ruta con cuatro archivos relacionados.
- Cambio pequeño acompañado de diff y comprobación.
- Explicación de una prueba y de algo que esa prueba no cubre.
- Demostración de permisos y hábito repetido.
- Respuesta a una limitación real del sistema.

Evalúe también si el estudiante reconoce incertidumbre y sabe buscar. Decir que no recuerda un dato y localizarlo correctamente tiene más valor que inventar una función.

## 7 Cierre académico y cierre operativo

El cierre académico exige que el grupo comprenda y reproduzca el proyecto. El cierre operativo añade URL, persistencia, correo cuando corresponda, controles compartidos, recuperación y aceptación del propietario. La entrega técnica mantiene ambas evidencias separadas para que una nota de sustentación no se confunda con una garantía de producción.
