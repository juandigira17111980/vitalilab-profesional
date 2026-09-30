# Frontend, UX y accesibilidad

## 1. Enfoque

La interfaz convierte el producto en una experiencia educativa, sobria y accionable. La prioridad es que el usuario entienda su siguiente acción, no llenar la pantalla de estadísticas.

## 2. Sistema visual implementado

| Elemento | Decisión |
|---|---|
| Paleta | Verde bosque para confianza, lima para progreso, crema para descanso visual |
| Tipografía | Pila de sistema; no bloquea carga ni depende de terceros |
| Componentes | Botones, tarjetas, pills, formularios, alertas, métricas y estados reutilizables |
| Espaciado | Shell máximo de 1180 px y escala consistente |
| Movimiento | Transiciones breves y respeto a `prefers-reduced-motion` |
| Marca | Símbolo SVG propio, sin recursos remotos |

El CSS está centralizado en `app/static/css/app.css`; el JavaScript progresivo en `app/static/js/app.js`. La funcionalidad principal del servidor no depende de un framework de frontend.

## 3. Arquitectura de información

```text
Público: Inicio · Bienestar · IMC · Privacidad · Acceso/Registro
Usuario: Panel · Hábitos · Perfil · Salir
Admin: lo anterior + Administración
```

La navegación se adapta a menú móvil, actualiza `aria-expanded`/`aria-label` y cierra con Escape devolviendo el foco al botón.

## 4. Pantallas

- **Inicio:** propuesta de valor, representación conceptual de progreso, método, calculadora orientativa, comunicados y CTA.
- **Registro/login/recuperación:** etiquetas visibles, `autocomplete`, ayuda de contraseña, errores junto al campo y privacidad accesible.
- **Panel:** puntos, racha, nivel, progreso semanal y acciones del día.
- **Hábitos:** tarjetas táctiles, puntos visibles y estado textual además del color.
- **Perfil:** separa datos de presentación y medidas opcionales; contextualiza IMC.
- **Administración:** formulario, lista de comunicados y eventos sin exponer contraseñas/medidas.
- **Errores:** vistas coherentes 400/403/404/429/500.

## 5. Accesibilidad implementada

- HTML semántico, un `h1` principal y regiones de navegación.
- Enlace para saltar al contenido.
- Foco visible y controles nativos.
- Formularios con label, ayuda y errores.
- Alertas con `aria-live` y botón de cierre.
- Iconos decorativos ignorados o acompañados de texto.
- Estados no dependientes solo del color.
- Controles táctiles de aproximadamente 44–48 px.
- Movimiento reducido.

Pendiente antes de afirmar WCAG 2.2 AA completa: auditoría automática especializada, zoom 200 %, lector de pantalla y prueba con usuarios.

## 6. Responsive

Los breakpoints principales están en 900, 720 y 440 px. Se validó con navegador real:

| Vista | Resolución | Resultado |
|---|---:|---|
| Inicio | 1280+ px | ✅ jerarquía y secciones correctas |
| Dashboard | Escritorio | ✅ grilla, métricas y lateral |
| Inicio/dashboard | 390 × 844 | ✅ una columna, sin corte horizontal |
| Menú | 390 × 844 | ✅ abre, etiqueta cambia y cierra con Escape |
| Hábitos | 390 px | ✅ acción y estado legibles |
| Administración | 1280 × 900 | ✅ formulario/listas sin solapamiento |

## 7. Hallazgo E2E corregido

Las alertas estaban inicialmente superpuestas sobre el título móvil. Se movieron al flujo del documento y se elevó el menú para evitar que un mensaje ocultara acciones. La captura final del menú confirma el ajuste.

## 8. Rendimiento

No hay dependencias JavaScript de terceros, fuentes remotas ni imágenes pesadas. El activo de marca es SVG. Staging debe medir LCP, CLS e INP; no se publican cifras hasta disponer de URL y condiciones reproducibles.

## 9. Estado

Frontend y responsive: ✅ implementados y revisados visualmente. Conformidad WCAG completa y métricas reales: 🟡.
