# Frontend, UX y accesibilidad

## 1. Objetivo

Convertir VitaliLab en una experiencia coherente, clara, móvil y accesible, sin perder su enfoque educativo. La interfaz debe ayudar a comprender y mantener hábitos; no debe presentar indicadores como diagnósticos médicos.

## 2. Estado actual observado

- Plantillas Jinja con navegación y estilos repetidos.
- CSS y JavaScript embebidos en varias páginas.
- Adaptación móvil incompleta, especialmente en navegación.
- Formularios con oportunidades de mejora en etiquetas, asociación `for/id`, autocompletado y mensajes.
- Contratos inconsistentes entre algunas plantillas y rutas de una versión posterior.
- Falta de estados estandarizados: cargando, vacío, error, éxito y sin permiso.

## 3. Arquitectura de información propuesta

```text
Público
├── Inicio
├── Contenidos educativos
├── Iniciar sesión
└── Crear cuenta

Usuario autenticado
├── Resumen / Dashboard
├── Mis hábitos
├── Mi progreso
├── Mi perfil
└── Cerrar sesión

Administrador
├── Anuncios
├── Catálogo de hábitos
└── Auditoría operativa
```

## 4. Sistema visual base

Antes de diseñar pantallas se establecerán tokens reutilizables:

| Categoría | Definición esperada |
|---|---|
| Color | Primario, secundario, fondo, superficie, texto, éxito, alerta y error con contraste validado |
| Tipografía | Familia, escala de títulos/cuerpo y alturas de línea |
| Espaciado | Escala consistente, por ejemplo 4/8/12/16/24/32 px |
| Bordes | Radio y grosor definidos |
| Sombras | Uso limitado para jerarquía, no decoración excesiva |
| Movimiento | Transiciones cortas, respetando `prefers-reduced-motion` |

La identidad visual definitiva se validará con el equipo. Este documento no inventa una marca final.

## 5. Componentes reutilizables

- Layout principal y navegación responsive.
- Encabezado de página y migas cuando aporten orientación.
- Botones primario/secundario/peligro, con estado deshabilitado y foco.
- Campos, etiquetas, ayuda y errores accesibles.
- Tarjeta de hábito y control de cumplimiento.
- Indicadores de puntos, racha y nivel con explicación textual.
- Alertas/flash consistentes.
- Modal solo cuando sea necesario, con gestión correcta del foco.
- Tabla o lista adaptable para administración.
- Estados vacío, carga, error y éxito.

## 6. Pantallas y criterios

### Inicio

- Explica en una frase qué resuelve VitaliLab.
- CTA claro para registro o acceso.
- No promete resultados clínicos.
- Contenido esencial visible y rápido en móvil.

### Registro y acceso

- Una etiqueta visible por campo.
- `autocomplete` apropiado (`email`, `new-password`, `current-password`).
- Errores junto al campo y resumen accesible si hay varios.
- Política de privacidad disponible antes de aceptar.
- Contraseña con requisitos claros, sin impedir pegar desde gestor.

### Dashboard

- Prioriza “qué hago hoy” sobre estadísticas decorativas.
- Distingue progreso diario, puntos acumulados y racha.
- Explica qué causa cada cambio.
- No depende solo del color para comunicar estado.

### Perfil y medidas

- Indica qué dato es obligatorio y por qué.
- Usa unidades visibles.
- Explica el alcance educativo del IMC.
- Permite corregir/eliminar datos conforme a política definida.

### Administración

- Acciones peligrosas requieren confirmación proporcional.
- Los permisos se validan también en backend.
- Tablas se convierten en tarjetas o permiten desplazamiento accesible en móvil.

## 7. Responsive

Anchos mínimos de validación sugeridos:

- 360 px: teléfono pequeño.
- 390/414 px: teléfono común.
- 768 px: tableta.
- 1024 px: portátil pequeño.
- 1440 px: escritorio.

No basta con que “quepa”: se verifican orden de lectura, navegación con teclado, tamaño táctil, ausencia de desplazamiento horizontal y jerarquía de contenido.

## 8. Accesibilidad

Objetivo recomendado: WCAG 2.2 nivel AA en los flujos principales.

Lista mínima:

- HTML semántico y un `h1` por pantalla.
- Contraste suficiente.
- Foco visible y orden lógico con teclado.
- Enlace para saltar al contenido.
- Texto alternativo útil o imagen decorativa ignorada.
- Etiquetas y descripciones conectadas a formularios.
- Errores anunciados y no comunicados solo por color.
- Botones reales para acciones; enlaces para navegación.
- Zoom al 200 % sin pérdida funcional.
- Movimiento reducido respetado.

## 9. Rendimiento

- CSS y JavaScript propios separados, minificables y cacheables.
- Imágenes en tamaño y formato adecuados.
- Fuentes limitadas y con estrategia de carga.
- JavaScript progresivo: el flujo esencial no depende de una librería innecesaria.
- Consultas del dashboard preparadas en backend para evitar trabajo repetido en plantilla.
- Presupuesto inicial a medir en Staging: LCP, CLS e INP en dispositivos modestos.

## 10. Pruebas visuales y de experiencia

- Capturas antes/después con misma resolución.
- Revisión de todos los estados, no solo el “camino feliz”.
- Recorrido completo por teclado.
- Prueba con lector de pantalla en registro y hábitos.
- Prueba móvil real o emulación controlada.
- Sesión breve con usuarios de prueba y registro de fricciones.
- Verificación de enlaces, navegación y mensajes de error.

## 11. Evidencia esperada

Cada pantalla mejorada deberá registrar:

| Evidencia | Ejemplo |
|---|---|
| Problema original | Captura y descripción reproducible |
| Decisión | Componente/patrón elegido y motivo |
| Implementación | PR y archivos afectados |
| Prueba | Resoluciones, navegador, teclado y resultado |
| Resultado | Captura de Staging y aprobación |

## 12. Estado

La mejora de frontend está **🟡 propuesta**. Aún no se ha aplicado un rediseño funcional al código del proyecto privado.
