# Seguridad y privacidad

## 1. Alcance

Este documento registra controles técnicos. No sustituye la revisión jurídica/institucional exigible para datos personales, salud o menores.

## 2. Controles implementados

| Dominio | Control | Evidencia |
|---|---|---|
| Contraseñas | scrypt con sal mediante Werkzeug | Hash distinto al texto y pruebas |
| Enumeración | Mensajes genéricos y hash ficticio | Pruebas de cuenta inexistente |
| Fuerza bruta | 5/min y 20/h por endpoint + bloqueo de cuenta tras 5 fallos | Configuración y prueba |
| Registro/recuperación | Límites 8/h y 5/h | Decoradores Limiter |
| Recuperación | Token firmado, una hora e invalidación por cambio de hash | Pruebas |
| Sesiones | Cookies HttpOnly, SameSite Lax, Secure en HTTPS y vida de 8 h | Configuración |
| CSRF | Global para formularios; logout también usa POST | Prueba con CSRF activo |
| Autorización | `login_required` y `admin_required` del lado servidor | Prueba usuario/admin |
| Inyección | ORM y expresiones parametrizadas | Revisión de código |
| XSS | Autoescape Jinja y CSP sin inline scripts | Plantillas/cabecera |
| Clickjacking | `frame-ancestors 'none'` y `X-Frame-Options: DENY` | Prueba de headers |
| MIME/referrer/permisos | `nosniff`, referrer estricto y cámara/mic/geoloc deshabilitados | Middleware |
| Transporte | HSTS cuando `SESSION_COOKIE_SECURE=true` | Configuración |
| Cache | `no-store` en panel, perfil, hábitos y admin | Middleware |
| Auditoría | Eventos de cuenta/sesión/hábito/comunicado, sin datos sensibles | Tabla y panel |
| Secretos | Variables externas; `.env`, DB y backups ignorados | `.gitignore`/`.env.example` |

## 3. Datos tratados

| Categoría | Obligatorio | Finalidad |
|---|---:|---|
| Correo | Sí | Identidad y recuperación |
| Nombre/apodo | Sí | Presentación |
| Fecha de nacimiento/grado | No | Contexto educativo |
| Peso/altura/IMC | No | Seguimiento educativo opcional |
| Cumplimientos | Sí para la función | Progreso, puntos y racha |
| Auditoría | Operativo | Seguridad y trazabilidad |

No se registran contraseñas, hashes, tokens, cookies ni medidas en logs/auditoría. `metadata_redacted` contiene solo fecha u otro metadato no sensible aprobado.

## 4. Privacidad por diseño

- Aceptación de privacidad versionada al crear la cuenta.
- Medidas opcionales y acceso limitado al propietario.
- No se copian datos reales a pruebas o Staging.
- Mensaje permanente de alcance educativo/no diagnóstico.
- Eventos administrativos visibles sin abrir perfiles de salud.

Antes de Production deben aprobarse responsable del tratamiento, contacto, finalidad, base jurídica, edad mínima/consentimiento, retención, corrección, eliminación e incidentes.

## 5. Límites conocidos

- Rate limiting usa memoria y un worker. Escalar horizontalmente exige Redis compartido.
- SMTP real no ha sido conectado; la lógica se prueba con doble.
- `pip-audit 2.10.1` no encontró vulnerabilidades conocidas en dependencias y Bandit no encontró hallazgos medios/altos. No sustituyen pentest ni escaneo especializado de secretos; si el plan lo permite, se recomienda Dependabot/CodeQL.
- La CSP permite estilos propios por archivo; agregar analítica o CDN exige revisar la política.
- No existe MFA; no es requisito del primer alcance, pero se recomienda para administradores en una fase posterior.

## 6. Respuesta a incidentes

1. Contener acceso o despliegue sin borrar evidencia.
2. Preservar versión, hora, logs y alcance.
3. Rotar secretos y corregir causa.
4. Restaurar versión/datos validados.
5. Verificar health, acceso y ausencia de recurrencia.
6. Comunicar según responsable y obligación.
7. Registrar postmortem y control preventivo.

## 7. Gate de Production

- [x] Hash, CSRF, autorización, validación, cabeceras y errores.
- [x] Secretos fuera de Git y configuración separada.
- [x] Pruebas críticas locales.
- [x] CI final en verde.
- [ ] SMTP y recuperación real en Staging.
- [x] Auditoría local de dependencias sin vulnerabilidades conocidas.
- [x] SAST del código Python con Bandit.
- [ ] Escaneo especializado de secretos del commit final.
- [x] Backup/restauración aislada en PostgreSQL 18 CI.
- [ ] Política de privacidad aprobada.
- [ ] Aprobación de release.

## 8. Estado

Controles de aplicación: ✅. Controles organizacionales y verificación remota: 🟡; bloquean Production donde se indica.
