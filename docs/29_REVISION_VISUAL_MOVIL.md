# Revisión visual móvil: cambios mínimos, funciones intactas

Fecha: 15 de octubre de 2026, America/Bogota. Modo: revisión focalizada de frontend y UX. Base de Git: `ce0da69`; aplicación publicada al comenzar: `81b5650`.

## Alcance solicitado

Mejorar únicamente presentación o facilidad de uso cuando exista una razón comprobable. Mantener identidad, contenido y funciones existentes. No se modifican Python, plantillas, JavaScript, formularios, permisos, puntos, catálogo, migraciones, dependencias ni configuración de infraestructura. El único archivo de aplicación modificado es `app/static/css/premium.css`; lo demás es documentación.

## Diagnóstico y decisión

La distribución actual ya presenta títulos claros, botones amplios, números separados y tarjetas adaptadas. Se conserva: no se reemplaza el diseño por preferencia estética. Tampoco se cambia el copy, porque el propósito y los botones principales resultan coherentes con el recorrido existente. No se promete mayor conversión sin pruebas con usuarios reales.

| Código | Hallazgo | Impacto / heurística | Responsable | Acción |
|---|---|---|---|---|
| MOV-01 | Menú móvil desplegado con Mi cuenta: el borde inferior llegaba a 734 px en una pantalla de 568 px de alto | Medio: opciones finales difíciles de alcanzar; control y libertad del usuario | Frontend/UX | Altura máxima dependiente del viewport y desplazamiento interno, sin eliminar opciones |
| MOV-02 | Borde de campos `#cbd4d0` sobre blanco: 1,51:1 | Bajo: delimitación tenue del control; reconocimiento y consistencia | Frontend/UX | Borde `#7a8d80`: 3,53:1 sobre blanco; mismo tono en botones de contorno |
| MOV-03 | Inputs y áreas de texto no compartían el contorno fuerte de foco del selector | Bajo: señal de teclado menos uniforme; visibilidad del estado | Frontend/UX | Foco de 3 px, separado 2 px, `#177b69`: 5,16:1 sobre blanco |
| MOV-04 | El desplazamiento al enfocar controles cortos podía ignorar el espacio ocupado por la barra inferior | Bajo: control temporalmente cubierto | Frontend/UX | Reserva inferior de desplazamiento en móvil, sin cambiar la barra ni la estructura del documento |

El menú corregido termina a 548 px en pantallas de 568 px de alto, y a 370 px en horizontal con 390 px de alto. Se comprobó que la última opción queda visible al desplazarse y que Escape cierra el menú devolviendo el foco. No se reduce ningún botón ni se ocultan funciones para conseguir que quepa.

## Dirección visual y textos conservados

| Criterio | Decisión |
|---|---|
| Objetivo | Encontrar opciones y completar formularios con claridad |
| Marca | VitaliLab, verde bosque/lima, SVG y tipografía existentes |
| Audiencia | Uso personal y comunidad educativa |
| Plataforma | Web adaptable a móvil, tablet y escritorio |
| Emoción | Confianza, autonomía y calma, sin presión corporal |
| Restricción | Ningún cambio de datos, negocio o autorización |
| Composición | Mantener jerarquía, tarjetas, espacios y navegación actuales |
| Recursos creativos | No se necesitan imágenes generativas ni videos; no se reemplazan ilustraciones |

La revisión de copy preserva títulos y CTA existentes: son concretos y no prometen resultados médicos ni usan etiquetas corporales negativas. No se introducen variantes comerciales en este alcance solo visual.

## Validación ejecutada antes de publicar

- 150 pruebas funcionales aprobadas; cobertura 94,89 %. Permanecen cinco advertencias de deprecación de dependencias, no errores.
- Repetición de los 37 estados/anchos del recorrido con cuentas ficticias locales: medición, objetivo, biblioteca, editor y errores, rutina propia, temporizador, XP, perfil, seguimiento, solicitud escolar, administración y docente. Resultado final sin hallazgos de las comprobaciones de layout, ARIA e infracciones automáticas utilizadas.
- 54 combinaciones adicionales: nueve pantallas por seis anchos, 320, 360, 390, 430, 768 y 1440 px. Sin desbordes horizontales, números recortados ni botones/filtros evaluados por debajo del objetivo de 44 × 44 px. Auditoría automática WCAG A/AA evaluada sin infracciones detectadas.
- Menú desplegado y Mi cuenta a 320 × 568, 390 × 568 y 844 × 390, más comparación de escritorio a 1440 × 900. Última acción alcanzable; cierre por Escape correcto; menú de escritorio conservado.
- Revisión visual de capturas de portada, biblioteca, panel, editor y menú. Contraste calculado para las combinaciones concretas anteriores. El borde nuevo también alcanza 3,18:1 contra el fondo claro `#f2f4eb` de botones transparentes.
- Foco de teclado visible y etiquetas accesibles comprobados por muestreo. No se modifican orden de tabulación, nombres de campos ni asociaciones de los formularios.

Una ejecución inicial midió una navegación antes de que terminaran de cargar sus hojas de estilo. Se corrigió la sincronización del ensayo para esperar carga y fuentes; se repitió el recorrido completo desde cuentas locales reiniciadas y quedó correcto. No se ocultó una infracción ni se debilitó CSP para conseguir ese resultado.

## Publicación acotada y reversión

La entrega requiere PR y CI verde antes de publicar. El procedimiento compara los archivos con el release anterior y rechaza cualquier diferencia fuera de CSS y documentación. Construye la imagen y sustituye únicamente la web mediante `--no-deps`, conservando la configuración existente. No ejecuta migraciones, seeds, concesiones de permisos ni cambios de DNS.

Antes/después se comprueban PostgreSQL y los demás contenedores mediante ID, hora de arranque y reinicios; también se comparan la revisión de esquema y el inventario de versiones de dependencias. Se conserva la imagen anterior para revertir solo la web si falla salud o compatibilidad. La versión y resultado remoto se anotan en el comentario de cierre del PR; la validación local no se presenta como evidencia de publicación.

## Veredicto y límites

**Apta para la mejora visual acotada**, con las limitaciones declaradas. No se asigna un score global de producción por revisar CSS. Los pendientes operativos del [informe anterior](28_QA_Y_PUBLICACION_PERSONALIZACION.md) siguen sin cambios.

Las verificaciones se hicieron con un navegador real de escritorio y viewports adaptados, no con todos los teléfonos físicos ni todas las versiones de Safari/Android. No se certifican WCAG, un pentest, entregabilidad de correo o rendimiento de campo. Los campos altos y el teclado virtual necesitan además una comprobación en dispositivos físicos; no se afirma que todos sus casos estén cubiertos por emulación.

## Especialidades aplicadas

`auditor-qa-final`: hallazgos concretos, evidencia y límites. `desarrollador-web-fullstack`: parche exclusivo de CSS y regresión. `chief-ux-officer`: alcance táctil, altura visible, contraste y foco. `director-creativo-ai`: preservar identidad y composición, sin activos nuevos innecesarios. `copywriter-senior`: conservar el lenguaje claro ya existente, sin claims nuevos. Git/DevOps se limita al control de versiones y publicación de esa misma presentación.
