# Auditoría profunda y plan de mejora de VitaliLab

**Versión:** 1.0  
**Fecha:** 30 de septiembre de 2026  
**Estado:** diagnóstico técnico inicial, previo a cualquier modificación de producción  
**Producción:** `www.vitalilab.space` / servicio Render `vitalilab`  
**Repositorio de origen:** `ega1026/vitalilab` — acceso de solo lectura  
**Repositorio de trabajo:** `juandigira17111980/vitalilab-profesional` — privado

## 1. Objetivo

Establecer una base segura y profesional para evolucionar VitaliLab en el orden correcto:

1. Base de datos y protección de información.
2. Backend, autenticación y reglas de negocio.
3. Frontend, experiencia de usuario y accesibilidad.
4. QA, observabilidad y despliegue controlado.

Producción no se modifica durante esta etapa. Todo cambio debe llegar primero a un ambiente Staging aislado y requiere aprobación antes de promoverse.

## 2. Alcance y evidencia revisada

- Código de la versión que Render identifica como activa: commit `a699b1d`.
- Cambio que Render intentó desplegar y marcó como fallido: commit `eb35d77`.
- Estructura completa del repositorio público y su historial relevante.
- Archivo SQLite actual y blobs SQLite históricos, sin consultar ni exponer datos personales.
- Rutas Flask, consultas SQL, sesiones, autenticación y scripts de inicialización.
- Plantillas Jinja, CSS, JavaScript, formularios, navegación y responsive.
- Configuración visible de Render compartida por el responsable del proyecto.

No se modificó Render, el dominio, las variables de producción ni la base de datos en ejecución. Tampoco se crearon usuarios de prueba en producción.

## 3. Hechos confirmados y supuestos pendientes

### Hechos confirmados

- Render mantiene activa la versión `a699b1d` y muestra fallido el intento `eb35d77`.
- Producción está organizada en `VitaliLab > Production`; existe un ambiente `Staging` vacío.
- El servicio productivo utiliza Python 3 y está en plan gratuito.
- El código activo es un monolito Flask con plantillas Jinja y acceso directo a SQLite.
- La clave de sesión está escrita en el código fuente público.
- Las contraseñas del código activo se guardan y comparan sin hash.
- La aplicación utiliza una ruta relativa para `vida_saludable.db`.
- `crear_db.py` contiene `DROP TABLE IF EXISTS usuarios` y puede borrar información si se ejecuta.
- No existen migraciones versionadas, pruebas automatizadas, CI, health checks ni configuración declarativa de despliegue.
- El archivo SQLite del commit activo está vacío; el historial contiene un blob SQLite de 16 KB con una tabla `perfiles` y cero registros. No se encontraron filas personales en ese blob histórico inspeccionado.
- El `main` fallido mezcla modelos SQLAlchemy nuevos con plantillas y rutas antiguas incompatibles.
- `requirements.txt` fue generado como un volcado amplio del entorno e incluye decenas de paquetes de Jupyter ajenos a la aplicación; no incluye un servidor WSGI como Gunicorn.

### Supuestos controlados que deben confirmarse

- La base SQLite creada dentro del contenedor de Render puede contener usuarios reales; no es visible desde Git.
- El motivo exacto del deploy fallido requiere los logs de Render. El código contiene suficientes incompatibilidades para impedir una publicación segura, pero no se atribuye una causa única sin esos logs.
- No se conoce todavía el volumen de usuarios, crecimiento esperado, criticidad horaria, RPO ni RTO.
- Debe confirmarse si la aplicación está dirigida a menores de edad y si recopila peso, altura u otros datos de salud reales.

## 4. Resumen ejecutivo

VitaliLab debe tratarse como un prototipo funcional, no como una aplicación lista para producción. El riesgo principal no es visual: es la combinación de credenciales inseguras, sesiones firmadas con una clave pública, almacenamiento SQLite no controlado y ausencia de migraciones, pruebas y recuperación.

La estrategia recomendada no es migrar a microservicios ni reescribir todo con otra tecnología. Para el tamaño actual conviene un **monolito modular Flask**, desplegado con un servidor WSGI, respaldado por PostgreSQL administrado y con una interfaz Jinja/CSS modernizada. Esta ruta reduce riesgo, costo y complejidad.

### Dictamen inicial

**NO-GO para desplegar `main` en producción.**  
**GO para construir una nueva línea segura en el repositorio privado y publicarla únicamente en Staging.**

## 5. Matriz priorizada de hallazgos

| ID | Severidad | Área | Hallazgo | Impacto | Acción |
|---|---|---|---|---|---|
| SEC-01 | Crítica | Seguridad | Contraseñas en texto plano en la versión activa | Compromiso total de cuentas | Hash Argon2id/scrypt, rotación y eventual restablecimiento obligatorio |
| SEC-02 | Crítica | Seguridad | `SECRET_KEY` pública y fija | Falsificación potencial de sesiones | Rotar y almacenar solo en secretos de Render |
| DBA-01 | Crítica | Datos | SQLite en filesystem del servicio | Pérdida o divergencia de información | Migrar a PostgreSQL administrado con backup probado |
| DEP-01 | Crítica | Deploy | Producción y `main` no coinciden; último deploy falló | Publicación no reproducible | Congelar producción y reconstruir Staging desde baseline controlado |
| BE-01 | Alta | Backend | Backend y plantillas de `main` tienen endpoints/modelos incompatibles | Errores 500 y navegación rota | Unificar contrato entre rutas, modelos y vistas |
| DBA-02 | Alta | Datos | Script destructivo con `DROP TABLE` | Borrado accidental | Retirar script y usar Alembic/Flask-Migrate |
| BE-02 | Alta | Backend | Formularios POST sin CSRF | Acciones forzadas desde otros sitios | Flask-WTF/CSRF global y pruebas negativas |
| BE-03 | Alta | Backend | Los retos pueden sumar puntos repetidamente | Fraude de puntos y datos inconsistentes | Registro diario normalizado + restricción única |
| SEC-03 | Alta | Seguridad | Sin rate limiting, bloqueo ni recuperación de contraseña | Fuerza bruta y cuentas irrecuperables | Límites por IP/cuenta, tokens expirables, auditoría |
| PRIV-01 | Alta | Privacidad | Posibles datos de salud y menores sin flujo de consentimiento visible | Riesgo regulatorio y reputacional | Minimización, autorización, privacidad y revisión jurídica |
| OPS-01 | Alta | Operación | Sin backup/restore probado, logs estructurados ni health checks | Incidentes difíciles de detectar y recuperar | Política de backup, restauración, `/health` y alertas |
| FE-01 | Media | Frontend | Navegación móvil deficiente y estilos inline extendidos | Baja usabilidad y alto costo de mantenimiento | Layout responsive y sistema de componentes CSS/Jinja |
| FE-02 | Media | Accesibilidad | Labels sin asociación, foco y mensajes no anunciados | Barreras de acceso | WCAG AA básica, teclado, `aria-live`, contraste y targets táctiles |
| QA-01 | Alta | Calidad | No existen pruebas automatizadas | Regresiones invisibles | Pirámide mínima de tests y pipeline CI |

## 6. Auditoría DBA y plan de mejora

### 6.1 Estado actual

El motor activo es SQLite y la carga esperada es transaccional OLTP: usuarios, perfiles, hábitos y avances diarios. El modelo activo concentra autenticación, perfil, métricas y gamificación en una sola tabla `usuarios`.

Problemas confirmados:

- Una tabla mezcla responsabilidades incompatibles.
- `edad` se almacena como número fijo y queda obsoleta; si el dato es necesario debería derivarse de fecha de nacimiento, con minimización y justificación.
- `peso`, `altura` e `imc` usan cero como valor por defecto; cero confunde “sin dato” con un valor real inválido. Deben ser `NULL` cuando no existan.
- `grado`, `nivel` y `rol` son textos libres sin catálogo ni restricción.
- No hay historial real de hábitos: solo acumulados en la fila del usuario.
- No existe garantía de una sola actualización por usuario y día.
- No hay campos consistentes `created_at`, `updated_at`, `deleted_at` ni actor de modificación.
- No existen migraciones ni rollback.
- Las claves foráneas no están habilitadas en SQLite y no hay integridad relacional que proteja el dominio.
- El script de creación y la tabla creada al iniciar no coinciden: uno omite `nivel` y además borra la tabla existente.

### 6.2 Motor recomendado

**PostgreSQL administrado** para Staging y Producción, en instancias separadas. La decisión se justifica por persistencia, concurrencia multiusuario, integridad ACID, restricciones, backups y migraciones; no por moda. SQLite puede conservarse únicamente para pruebas unitarias muy acotadas, aunque las pruebas de integración deben ejecutarse contra PostgreSQL para evitar diferencias de motor.

### 6.3 Modelo objetivo inicial

#### `users`

- `id`: bigint o UUID, PK.
- `email_normalized`: correo en minúsculas, único y no nulo.
- `password_hash`: nunca contraseña reversible.
- `role`: enum controlado o FK a roles.
- `is_active`.
- `email_verified_at`.
- `last_login_at`.
- `password_changed_at`.
- `created_at`, `updated_at`.

#### `user_profiles`

- `user_id`: PK/FK a `users` con borrado definido.
- `display_name`.
- Datos opcionales estrictamente necesarios.
- Evitar almacenar edad, peso o altura si la funcionalidad no los requiere realmente.

#### `habits`

- Catálogo de hábitos activos: hidratación, sueño, pausa activa, etc.
- Nombre, descripción, puntos y estado.

#### `habit_entries`

- `id`, `user_id`, `habit_id`, `entry_date`, `completed_at`.
- Restricción única `(user_id, habit_id, entry_date)`.
- FKs indexadas.

#### `daily_checkins`

- `id`, `user_id`, `check_date`, puntos calculados y auditoría.
- Restricción única `(user_id, check_date)`.

#### `announcements`

- `id`, `title`, `content`, `author_user_id`, `published_at`, estado y auditoría.

#### `audit_events`

- Eventos críticos: login fallido, cambio de contraseña, modificación administrativa y exportación de datos.
- Nunca almacenar contraseñas, tokens ni valores sensibles en el detalle.

### 6.4 Índices y restricciones

- Único por correo normalizado.
- Índices en todas las FKs.
- Único compuesto para hábitos diarios.
- Índices por `(user_id, entry_date DESC)` para historial.
- Checks para valores válidos cuando existan métricas numéricas.
- Paginación para listados administrativos.
- Ningún índice adicional se declarará “optimización” sin medir consultas y `EXPLAIN ANALYZE` en datos representativos.

### 6.5 Migración de datos

1. Inventariar la base real de Render: tamaño, tablas, filas y usuarios activos, sin exportar datos a chats.
2. Tomar backup cifrado y verificar su integridad.
3. Definir RPO/RTO y una ventana de corte adecuada al volumen real.
4. Crear esquema PostgreSQL mediante Alembic.
5. Exportar SQLite con un script versionado y verificaciones de conteos.
6. Convertir contraseñas a hash durante la migración si aún son texto plano; por seguridad se recomienda forzar restablecimiento posterior.
7. Anonimizar información usada en Staging.
8. Importar, comparar conteos y reglas de integridad.
9. Ejecutar pruebas funcionales y de restauración.
10. Programar el corte de producción únicamente después de aprobación.

Para el volumen pequeño esperado, una ventana breve y controlada es más segura que implementar dual-write. Esta decisión se revisará cuando conozcamos usuarios y tráfico reales.

### 6.6 Backup y recuperación

- Backup administrado según el plan contratado y exportación lógica cifrada adicional.
- Retención propuesta inicial: 7 diarios, 4 semanales y 3 mensuales, sujeta a costo y obligaciones reales.
- Prueba mensual de restauración en un entorno aislado.
- RPO y RTO deben ser acordados; no se afirmará alta disponibilidad sin una prueba documentada.

## 7. Auditoría backend y plan de mejora

### 7.1 Diagnóstico

El backend actual concentra configuración, creación de esquema, consultas SQL, sesiones y reglas de puntos en un solo archivo. Para la escala actual sigue siendo correcto conservar un monolito, pero debe volverse modular y testeable.

Incompatibilidades confirmadas en `eb35d77`:

- `index.html` referencia rutas que ya no existen en el backend nuevo.
- `perfil.html` espera un objeto `usuario` y campos que el modelo `User` nuevo no posee.
- Las plantillas llaman `logout`, pero el backend nuevo no define esa ruta.
- La verificación renderiza una plantilla cuyo formulario referencia `completar_perfil`, endpoint inexistente.
- El checklist usa una plantilla informativa que no implementa ese flujo.
- El panel administrativo reutiliza una plantilla sin interfaz administrativa.
- La aplicación puede iniciar en `debug=True` y no define servidor WSGI de producción.

Estas inconsistencias justifican el **NO-GO** del `main` actual.

### 7.2 Arquitectura objetivo

```text
app/
├── __init__.py          fábrica de aplicación y extensiones
├── config.py            configuración por ambiente
├── extensions.py        db, migrate, csrf, limiter, login manager
├── auth/                registro, login, logout, recuperación
├── users/               perfil y preferencias
├── habits/              hábitos, check-ins, puntos y rachas
├── content/             contenido educativo y comunicados
├── admin/               administración y auditoría
├── templates/           layouts y vistas por módulo
└── static/              estilos y JavaScript versionados
migrations/              esquema versionado
tests/                   unitarias, integración y E2E
```

No se propone REST API completa hasta que exista un consumidor real distinto de la web. Las vistas server-side de Flask son suficientes y reducen complejidad. Si más adelante se crea app móvil o integración externa, se diseñará `/api/v1` con contratos explícitos.

### 7.3 Seguridad backend prioritaria

- Hash de contraseñas con Argon2id o scrypt y comparación segura.
- Rotación de `SECRET_KEY`; cookies `Secure`, `HttpOnly` y `SameSite` según ambiente.
- CSRF global en todos los formularios mutantes.
- Rate limiting por IP y cuenta en login, registro, verificación y recuperación.
- Política de contraseña, recuperación con token de un solo uso y expiración.
- Invalidación de sesiones al cambiar contraseña.
- Autorización server-side para administración; nunca confiar solo en la interfaz.
- Validación y normalización de correo, nombres y métricas.
- Errores al usuario sin stack trace ni detalles internos.
- Cabeceras CSP, HSTS cuando todo sea HTTPS, `X-Content-Type-Options`, `Referrer-Policy` y protección de framing.
- Dependencias mínimas, bloqueadas y escaneadas.

### 7.4 Reglas de negocio a corregir

- Un hábito solo puede acreditarse una vez por día.
- La racha se calcula desde fechas consecutivas, no se incrementa ciegamente con cada POST.
- Los puntos se derivan de eventos registrados y auditables.
- Debe manejarse el caso de usuario eliminado/inactivo y registros concurrentes.
- Las transacciones deben agrupar creación de entradas, cálculo de puntos y actualización de estado.
- El IMC debe presentarse como orientación, validar rangos y no almacenarse sin necesidad y consentimiento.

### 7.5 Operación y observabilidad

- Gunicorn u otro WSGI soportado, nunca el servidor de desarrollo.
- `/health/live` para proceso y `/health/ready` para conectividad de BD.
- Logs estructurados con `request_id`, ruta, estado y duración, sin PII.
- Manejo central de errores 400/401/403/404/409/422/429/500.
- Métricas mínimas: tasa de error, latencia p95, logins fallidos y conexiones de BD.
- Arranque no debe crear ni alterar tablas automáticamente.

### 7.6 Pruebas backend

- Unitarias: puntos, rachas, niveles y validaciones.
- Integración: registro, login, logout, CSRF, restricciones únicas y transacciones.
- Seguridad: fuerza bruta, sesión, autorización e inputs inválidos.
- Contrato entre rutas y plantillas para detectar `url_for` inexistentes.
- Prueba de migración desde una copia anonimizada.
- Objetivo inicial razonable: cobertura alta en reglas de dominio críticas, sin usar un porcentaje global como sustituto de calidad.

## 8. Auditoría frontend y plan de mejora

### 8.1 Estado actual

La identidad verde es coherente y la aplicación comunica rápidamente su propósito. Sin embargo, la implementación mezcla grandes cantidades de estilo inline, HTML repetido y scripts embebidos, lo que dificulta mantener consistencia y aplicar una política CSP fuerte.

Problemas principales:

- Navegación móvil sin menú compacto; la cabecera puede ocupar demasiado espacio o superponerse.
- Login y registro compiten en la misma pantalla sin jerarquía clara.
- Varios `label` no usan `for`/`id` y faltan `autocomplete` adecuados.
- No hay recuperación de contraseña, mostrar/ocultar contraseña ni explicación de privacidad.
- Falta un layout base Jinja; encabezados, metadatos y dependencias se duplican.
- Dependencias CDN sin estrategia de integridad, versión controlada o fallback.
- Mensajes de error no tienen región `aria-live`.
- Faltan estados explícitos de carga, error, vacío y éxito.
- La pantalla de carga simula conexión aunque no verifica disponibilidad real.
- El contador de agua de portada no persiste y puede confundirse con una función real.
- El gráfico usa metas fijas y no representa una serie temporal verdadera.
- Las páginas informativas sobre salud requieren lenguaje responsable, fuente y advertencia de orientación no diagnóstica.

### 8.2 Estrategia frontend recomendada

No se recomienda React/Next.js en esta fase. Jinja, CSS modular y JavaScript progresivo son suficientes, más ligeros y coherentes con Flask. Se incorporará un framework solo si aparecen interacciones complejas que lo justifiquen.

### 8.3 Sistema visual y componentes

- `base.html` con navegación, footer, mensajes y bloques extensibles.
- Macros/componentes para campo, botón, alerta, tarjeta, métrica y estado vacío.
- Tokens CSS para color, tipografía, espaciado, radios, sombras y estados.
- Eliminar estilos inline gradualmente para habilitar CSP.
- Navegación móvil accesible con botón, foco y estado expandido.
- Jerarquía clara: acción primaria, secundaria y enlaces informativos.
- Panel con información real: resumen de hoy, progreso semanal, racha válida y siguiente acción.

### 8.4 Accesibilidad

- Objetivo WCAG 2.1 AA como línea base técnica.
- Navegación completa por teclado y foco visible.
- Labels asociados, mensajes con `aria-live`, títulos jerárquicos y alt descriptivos.
- Contraste medido, no estimado visualmente.
- Targets táctiles adecuados y diseño responsive desde móvil.
- Respeto por `prefers-reduced-motion`.

### 8.5 Rendimiento y calidad visual

- Medición Lighthouse antes/después en móvil y escritorio.
- Objetivos: LCP ≤ 2.5 s, INP ≤ 200 ms y CLS ≤ 0.1 cuando el entorno permita medirlos de forma representativa.
- Optimizar logo e imágenes, fijar dimensiones y minimizar recursos bloqueantes.
- Evitar cargar librerías completas si solo se usa una fracción.
- Pruebas visuales de portada, acceso y panel en anchos representativos.

## 9. Privacidad y datos sensibles

VitaliLab puede tratar correos, edad, peso, altura, IMC y hábitos de estudiantes. En Colombia, los datos relativos a la salud se consideran datos sensibles y su tratamiento exige condiciones reforzadas; la información de niños, niñas y adolescentes requiere especial cuidado. Deben definirse finalidad, minimización, autorización, retención, derechos del titular y medidas de seguridad antes de ampliar la recolección. Referencias oficiales: [Ley 1581 de 2012](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981) y [SIC: tratamiento de datos sensibles relativos a la salud](https://sedeelectronica.sic.gov.co/publicaciones/boletin-juridico/concepto/tratamiento-de-datos-sensibles-relativos-la-salud).

Acciones requeridas:

- Confirmar si participan menores y obtener revisión jurídica específica.
- Publicar política de privacidad y aviso de tratamiento comprensible.
- Recoger solo datos indispensables para una finalidad documentada.
- Separar consentimiento, autenticación y perfil.
- Definir retención, eliminación y exportación de datos.
- Anonimizar Staging y cualquier dataset de QA.
- Mantener registro de accesos administrativos y exportaciones.

Este apartado es una señal técnica de cumplimiento y no sustituye asesoría jurídica.

## 10. Git, ambientes e infraestructura

### Estado logrado

- Repositorio privado creado bajo control del responsable.
- Ramas `main`, `staging` y `docs/auditoria-profunda` creadas.
- Producción original sin modificaciones.
- Render organizado con `Production` y `Staging` separados.
- Staging permanece vacío hasta contar con una baseline limpia y desplegable.

### Flujo objetivo

```text
rama de trabajo
      ↓ Pull Request + pruebas
   staging ─────────→ Render Staging + PostgreSQL Staging
      ↓ aprobación funcional y técnica
     main ──────────→ Producción, únicamente con autorización
```

### Controles a incorporar

- Protección/ruleset de `main` y `staging` si el plan de GitHub lo permite.
- CI: lint, pruebas, análisis de dependencias, build y secret scan.
- Deploy automático solo a Staging.
- Producción con aprobación manual, backup previo y rollback documentado.
- Variables y bases separadas por ambiente.
- Configuración de Render declarativa cuando la aplicación ya sea reproducible.

## 11. Roadmap recomendado

| Fase | Objetivo | Entregables | Salida obligatoria |
|---|---|---|---|
| 0 | Control y evidencia | repo privado, ramas, informe, inventario de Render | producción congelada y trazabilidad |
| 1 | Baseline segura | secretos fuera, `.gitignore`, dependencias mínimas, WSGI, health | build local reproducible |
| 2 | DBA | esquema PostgreSQL, Alembic, seed anonimizado, backup/restore | migraciones repetibles en Staging |
| 3 | Backend | módulos Flask, auth segura, reglas de hábitos, errores/logs | tests críticos aprobados |
| 4 | Frontend | layout, responsive, formularios, accesibilidad, panel | QA visual móvil/escritorio |
| 5 | Staging | servicio y BD aislados, variables, monitoreo | aprobación del responsable |
| 6 | Migración | backup real, ensayo, corte y rollback | Go/No-Go documentado |
| 7 | Producción | despliegue aprobado y verificación | observación y cierre |

## 12. Backlog por prioridad y esfuerzo relativo

### P0 — Bloqueante

- Rotar secretos y eliminar valores del código.
- Definir tratamiento de contraseñas existentes.
- Identificar y respaldar la base real de Render.
- Crear baseline desplegable con dependencias mínimas.
- Impedir despliegues de `main` original.

### P1 — Próximo ciclo

- PostgreSQL + migraciones.
- Autenticación, CSRF, rate limiting y recuperación.
- Modelo de hábitos diarios e integridad.
- Health checks, logs y pruebas de integración.
- Layout base y navegación móvil.

### P2 — Evolución

- Panel con historial real.
- Administración y auditoría.
- Accesibilidad completa y medición de rendimiento.
- Observabilidad y alertas.
- Automatización de backup y restauración.

### P3 — Solo si el negocio lo justifica

- API pública/versionada.
- App móvil.
- Cache distribuida.
- Procesamiento asíncrono.
- Microservicios.

## 13. Definition of Done para Staging

- Repositorio sin secretos, bases ni datos personales.
- Instalación reproducible desde cero.
- Migraciones versionadas contra PostgreSQL Staging.
- Login seguro, CSRF, rate limiting y autorización probados.
- Flujos críticos cubiertos por pruebas.
- Frontend responsive y navegable por teclado.
- Estados loading/error/empty/success implementados donde apliquen.
- Health check, logs y rollback disponibles.
- Datos de prueba sintéticos o anonimizados.
- Revisión QA con resultado Go para Staging.

## 14. Información faltante para cerrar el diseño

1. ¿La base de producción tiene usuarios reales o solo pruebas?
2. ¿La aplicación está dirigida a menores de edad?
3. ¿Cuántos usuarios y accesos concurrentes se esperan?
4. ¿Cuánta pérdida de datos y cuánto tiempo de caída son aceptables?
5. Captura o exportación textual de los logs del deploy `eb35d77`, sin secretos.
6. Lista de nombres de variables configuradas en Render, sin mostrar valores.
7. Confirmación de si Render tiene disco persistente o base gestionada asociada.

## 15. Próxima acción recomendada

No crear todavía el servicio web de Staging. Primero debe construirse en este repositorio una baseline limpia basada en `a699b1d`, retirar la base SQLite, reemplazar secretos y dejar un build reproducible. Después se conectará Render Staging a la rama `staging` y se añadirá una PostgreSQL independiente.
