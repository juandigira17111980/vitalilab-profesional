# Personalización y rutinas propias — especificación de cambio

Fecha: 15 de octubre de 2026. Base de código: `56cee00`. Estado inicial: implementación en curso, NO aprobación de producción.

## Objetivo y límites

Ampliar VitaliLab en NexoStack, sin modificar el Render original ni otros proyectos del VPS. Conservar cuentas, hábitos, puntos, historial y permisos existentes. Retirar los avisos de entorno académico de la interfaz, no las salvaguardas de privacidad ni el contexto del IMC.

## Decisiones de UX y negocio

1. La personalización se completa una vez. Cada acceso no exige pesarse. Se pueden actualizar las mediciones voluntariamente.
2. Recorrido: medición → resultado descriptivo del IMC → objetivo y modo de movimiento → biblioteca personalizada. Hábitos y biblioteca general siguen disponibles.
3. Un estudiante necesita una vinculación revisada y autorizada antes de recoger mediciones en este recorrido. El consentimiento para estadísticas sigue siendo independiente y opcional.
4. El objetivo dirige la selección de rutinas, NO una etiqueta de IMC. No se aplican umbrales de adultos a menores, no hay recompensas por cambiar de peso y no se prescribe una carga por el IMC.
5. Colegio y grupo se escriben manualmente. Son una solicitud, nunca una autorización. La administración los relaciona con un colegio y grupo verificados antes de aprobar. Escribir un nombre no permite consultar alumnos.
6. Las rutinas propias son privadas: nombre, objetivo, ejercicios ordenados, series, repeticiones o segundos, descansos e instrucciones. Crear, editar y archivar; archivar conserva registros y XP.
7. Registrar una rutina propia utiliza el mismo hábito de movimiento que las guiadas: una concesión de XP por hábito y día, incluso con solicitudes concurrentes.
8. Las demostraciones son ilustraciones esquemáticas locales, coherentes con la marca, con alternativas de texto y sin personas identificables ni servicios externos. No equivalen a validación clínica.

## Arquitectura y datos

Monolito modular Flask existente; no cambio de motor ni framework. PostgreSQL, carga transaccional relacional (OLTP). Migración aditiva: campos de personalización en `user_profiles` y tres entidades nuevas: solicitudes de colegio manuales, rutinas personales y ejercicios de rutina. Las membresías y claves compuestas de aislamiento escolar permanecen intactas.

## Criterios de aceptación y evidencia exigida

| Cambio | Verificación |
|---|---|
| Presentación | Sin banners académicos/ficticios en HTML público; información de privacidad veraz |
| Colegios manuales | Nombre libre; rechazo de entradas inválidas; ninguna elevación de privilegios; aprobación administrativa explícita |
| Recorrido | No saltar resultado/objetivo por URL o POST; repetición de login sin nueva medición; no guardar sin consentimiento |
| Rutinas propias | CRUD privado, límites y validación numérica; aislamiento de propietario; conflictos de edición; conservación al archivar |
| Puntos | Idempotencia diaria y concurrencia PostgreSQL; compatibilidad con hábitos y rutinas guiadas |
| Interfaz | Flujo completo, estados vacíos/errores, teclado, imágenes, móvil 320/390 px y escritorio |
| Datos | Migración desde revisión anterior sin pérdida, sin divergencia ORM/DDL; backup y restauración aislada |
| Publicación | CI verde, backup, rollback compatible, salud/versión/HTTPS, contenedores ajenos sin recrear |
| Estudio | Manual integral del sistema, diccionario de datos, rutas, seguridad, Git, infraestructura, operación y ejercicios |

## Dirección visual y textos

Objetivo: facilitar completar un perfil y empezar una actividad; audiencia personal y escolar; plataforma web móvil/escritorio; emoción: autonomía y confianza. Preservar marca verde oscuro/lima, tipografía y navegación. Ilustraciones vectoriales de dos posiciones, fondo claro, proporciones estables y sin promesas corporales. No hacen falta herramientas generativas ni videos publicitarios para este alcance.

Textos: sustituir avisos técnicos por orientación concreta; CTA «Calcular y continuar», «Guardar mi objetivo», «Crear mi rutina», «Registrar en mi día». Evitar etiquetas corporales, urgencia artificial y afirmaciones clínicas. La mejora de conversión es una hipótesis: no se declara sin medición con usuarios reales.

## Control de publicación

La auditoría debe separar la verificación técnica de los requisitos operativos para tratar datos reales de menores: responsable de datos, autorizaciones institucionales y del representante, revisión profesional de actividades, retención, recuperación y alertas. No se declarará «100/100» ni certificación legal o clínica sin evidencia. El detalle y el veredicto se registrarán tras las pruebas.

El 15 de octubre el propietario confirmó mantener el repositorio público (opción 2). Esta decisión no permite publicar credenciales, exportaciones de base de datos ni información de usuarios. La revisión de código y los manuales públicos no contienen esos valores.
