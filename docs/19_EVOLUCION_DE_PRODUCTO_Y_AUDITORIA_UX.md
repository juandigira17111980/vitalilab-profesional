# Evolución de producto y auditoría UX de VitaliLab

Edición del 13 de octubre de 2026, Colombia. Esta evolución amplía la copia académica de NexoStack con herramientas personales de hábitos. No sustituye Render ni convierte automáticamente el laboratorio en un SaaS comercial certificado.

## Objetivo y contexto

El producto pasa de registrar cuatro hábitos a ayudar a elegir una acción, fijar una meta, practicar una rutina y revisar avances. Se conserva Flask con Jinja, PostgreSQL 18 y el monolito modular: cambiar a React o a microservicios no resuelve el problema observado en móvil.

SUPUESTO CONTROLADO: el primer público sigue siendo estudiantes y personas que quieren ordenar su rutina. No se implementan diagnósticos, consultas médicas, pagos, promesas de resultados clínicos o planes comerciales ficticios. Las instituciones y el modelo multiempresa son una fase posterior.

## Diagnóstico inicial y decisiones

| Hallazgo | Evidencia | Heurística | Prioridad y responsable | Corrección |
|---|---|---|---|---|
| Porcentaje lateral en el anillo | Captura Safari aportada; Chromium a 390 px no reproduce el desplazamiento | Consistencia y visibilidad | Media, frontend | Pseudo-elemento y cifra en la misma celda Grid, sin depender de posición absoluta |
| Titulares y tarjetas demasiado grandes | Revisión de CSS, mínimo de 300 px por hábito y titulares con interlineado .98 | Diseño minimalista | Media, UX/frontend | Escala tipográfica moderada, interlineado legible y tarjetas compactas |
| Ejemplo de progreso sin etiqueta explícita | Inicio muestra 3 de 4 y 75 % como ejemplo | Coincidencia con el mundo real | Media, UX/copy | Etiquetar la demostración; presentar datos reales solo en el espacio autenticado |
| Pocas acciones más allá de marcar hábitos | Catálogo de cuatro hábitos y panel sin metas personales | Control y flexibilidad | Mejora, producto/backend/DBA | Ocho hábitos, metas editables, bitácora, análisis de 28 días y seis rutinas |
| Privacidad ocupa mensajes de venta | Inicio y registro enfatizan protección en lugar del siguiente paso | Jerarquía y reconocimiento | Baja, copy | Beneficios funcionales en primer plano; política y consentimiento permanecen accesibles |
| Barras limitadas a cuatro hábitos | JavaScript fija el máximo en 4 | Visibilidad del estado | Media, frontend | Escala basada en el catálogo real y número accesible, sin recortar al ampliar el catálogo |

No eliminar protección ni consentimiento es una decisión de producto: la aplicación trata información personal. Se reduce su protagonismo comercial, no sus controles.

## Diseño de experiencia

La navegación autenticada agrupa Hoy, Hábitos, Metas, Progreso y Rutinas. Perfil, administración y salida quedan en un menú de cuenta. En móvil, cuatro destinos frecuentes tienen navegación inferior con espacio reservado y área segura; el menú principal conserva las opciones restantes.

El panel muestra primero acciones y un siguiente paso. Marcar un hábito desde él vuelve al mismo panel. La meta expresa días cumplidos dentro de los últimos siete días, no una exigencia de completar todo el catálogo. La bitácora registra percepción de energía y enfoque, no interpreta esos valores como diagnóstico.

Los estados vacíos explican cómo comenzar. Las confirmaciones de cambios se muestran sin tapar contenido; los formularios rechazan valores inválidos y las acciones destructivas requieren una acción explícita. La biblioteca es utilizable sin cuenta y sus rutinas tienen temporizador pausable, reiniciable y operación por teclado.

## Dirección creativa

| Campo | Decisión |
|---|---|
| Acción comercial | Probar una rutina o crear una cuenta, sin comprar un servicio inexistente |
| Marca | VitaliLab, símbolo vegetal y movimiento ascendente |
| Audiencia | Personas conscientes de que les cuesta mantener una rutina |
| Emoción | Calma, capacidad de empezar y claridad de progreso |
| Plataforma | Web responsive; no anuncio ni video |
| Restricciones | Mantener nombre, identidad verde, legibilidad, privacidad y datos ficticios del laboratorio |
| Estilo | Editorial cálido, tarjetas funcionales, contraste bosque/lima y espacios contenidos |
| Intención | Mostrar utilidad real y permitir probar antes de registrar |

La primera composición une una promesa breve con una vista de producto claramente identificada como ejemplo. El recorrido continúa con seis capacidades, una rutina que puede probarse y respuestas a dudas. Sin testimonios inventados, contadores de clientes ni urgencia falsa.

La dirección se implementa con SVG, HTML y CSS propios: no hacen falta fotos sintéticas ni marcas de terceros. No se compra ni recomienda una licencia de un generador de imágenes. Como instrucción creativa reproducible: sujeto, panel VitaliLab; acción, elegir una pequeña acción diaria; entorno, lienzo crema; técnica, composición estática con espacio reservado; estilo, verde bosque y lima; emoción, calma; exclusiones, texto superpuesto y estadísticas inventadas; formato, 320 a 1440 px. La variante conserva el diseño y cambia solo el titular para un futuro test.

## Textos y conversión

El diagnóstico de copy detecta una promesa amplia sin mecanismo suficientemente visible. La nueva propuesta conecta la acción con la meta y el progreso, conserva un CTA de baja fricción y permite practicar una rutina sin registro.

- Versión optimizada: «Haz espacio para los hábitos que te hacen bien».
- Versión orientada a acción: «Elige una acción. Dale continuidad esta semana».
- Versión editorial elegida: «Tu bienestar, con un plan que sí cabe en tu día».

La última versión establece el mecanismo del producto sin vender un resultado médico. Los CTA son «Crear mi plan» y «Probar una rutina». La hipótesis comercial es que probar una herramienta antes del registro reduce incertidumbre; no se afirma un aumento de conversión sin tráfico y medición.

Para validar, prueba primero solo el titular, con idéntico CTA y resto de la página. Mide acceso a registro, cuenta creada y primer hábito, respetando consentimiento y sin introducir seguimiento de terceros por defecto. Antes de venta masiva, realiza cinco pruebas de usabilidad y registra tarea completada, tiempo y obstáculos.

## Datos, backend y seguridad

Se añaden dos entidades sin modificar ni borrar las siete anteriores:

| Entidad | Campos y restricciones | Relación y acceso |
|---|---|---|
| user_goals | id, user_id, habit_id, target_days 1 a 7, created_at, updated_at; única por usuario y hábito | FK usuario CASCADE, hábito RESTRICT; siempre consulta por usuario autenticado |
| daily_checkins | id, user_id, checked_on, energy 1 a 5, focus 1 a 5, created_at, updated_at; única por usuario y fecha | FK usuario CASCADE; el mismo día actualiza una fila, no duplica |

Los índices únicos cubren los filtros de usuario y las claves de negocio. No se introduce texto libre sensible. Las fechas de los nuevos módulos usan la zona del perfil, con retorno seguro a America/Bogota. La migración es aditiva y la versión anterior puede operar con las tablas nuevas sin usarlas. No se ejecuta downgrade sobre datos vivos para volver al código anterior.

Los servicios separan cálculos y escritura de las rutas. Los formularios conservan CSRF, validación de rangos y catálogo autorizado. Las metas de otra persona no pueden eliminarse ni leerse. Los eventos de auditoría no incluyen los valores de energía/enfoque ni contraseñas. Las páginas privadas tienen Cache-Control no-store. El usuario SQL de la web recibe DML solo sobre las dos tablas nuevas, además de sus permisos anteriores.

## Despliegue y validación

Rama de funcionalidad, pruebas y PR hacia staging; main no se modifica. La publicación utiliza exclusivamente vitalilab-lab, con backup previo, migración, permisos y comprobación posterior. Se comparan los contenedores ajenos antes y después. El rollback reactiva la imagen anterior y conserva el esquema aditivo y el volumen.

La auditoría de esta intervención profundiza en código nuevo, rutas de escritura, validaciones, aislamiento por usuario y pantallas principales. Se revisan por muestreo seguridad e infraestructura existentes. No sustituye pentest, pruebas de carga representativas, validación clínica ni conformidad legal.

Los criterios de salida son: pruebas sin regresión; migración y comprobación de deriva; operación real de metas, bitácora y rutinas; revisión de 320, 360, 390, 768 y 1440 px; ausencia de desborde y superposición de cifras; teclado y foco; controles principales de al menos 44 px como objetivo de diseño; auditoría automática de accesibilidad y Lighthouse antes/después. Las pruebas Chromium no prueban por sí mismas un iPhone real.

El tamaño mínimo AA de WCAG 2.2 es 24 px con excepciones; 44 px se adopta como objetivo más cómodo, no se presenta como el mínimo AA. Véanse [tamaño de objetivo W3C](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html) y [contraste W3C](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

## Camino hacia un SaaS vendible

Esta entrega permite demostrar un producto personal funcional. La venta institucional requiere organizaciones y aislamiento de tenant probado, roles de miembros y docentes, invitaciones, autorización y privacidad aplicables a menores, facturación real, recuperación de cuenta y revocación de sesiones, monitorización con avisos, operación offsite automatizada y pruebas de carga. Añadir tarjetas «Pro» o una tabla de precios sin esas capacidades no constituye un SaaS.

Los resultados finales, versión y hallazgos pendientes se registran en el informe de cierre. Los skills solicitados aportan auditoría final, heurísticas UX, implementación, coherencia de identidad y textos verificables; Git, arquitectura, DBA, backend, infraestructura y Playwright completan las capas técnicas. No se utilizan subagentes.
