# Backend de VitaliLab

## 1. Stack

- Python 3.13, Flask 3.1 y Gunicorn.
- SQLAlchemy 2 + Flask-SQLAlchemy.
- Alembic mediante Flask-Migrate.
- Flask-Login, Flask-WTF y Flask-Limiter.
- Psycopg 3 para PostgreSQL.

Las versiones están fijadas en `requirements.txt`; las herramientas de calidad en `requirements-dev.txt`.

## 2. Módulos

| Módulo | Responsabilidad |
|---|---|
| `main` | Inicio, contenidos, privacidad, dashboard, health/readiness |
| `auth` | Registro, login, logout y recuperación |
| `profile` | Datos propios y medidas opcionales |
| `habits` | Catálogo y cumplimiento diario |
| `admin` | Comunicados y eventos operativos |
| `services.progress` | IMC, puntos, niveles, racha y semana |
| `services.email` | SMTP para restablecimiento |
| `services.audit` | Eventos redactados |

## 3. Contrato de rutas real

| Método | Ruta | Acceso | Resultado |
|---|---|---|---|
| GET | `/` | Público | Inicio y comunicados publicados |
| GET | `/contenido/<slug>` | Público | `imc`, `bienestar`, `fundamentos` |
| GET | `/privacidad` | Público | Política informativa |
| GET | `/health` | Público/técnico | Proceso y versión |
| GET | `/ready` | Público/técnico | Conectividad DB, 200 o 503 |
| GET/POST | `/acceso/registro` | Anónimo | Alta segura |
| GET/POST | `/acceso/ingresar` | Anónimo | Sesión y retorno seguro |
| POST | `/acceso/salir` | Cualquiera | Cierre idempotente |
| GET/POST | `/acceso/recuperar` | Anónimo | Solicitud no enumerativa |
| GET/POST | `/acceso/restablecer/<token>` | Token válido | Cambio de contraseña |
| GET | `/panel` | Usuario | Resumen personal |
| GET/POST | `/perfil/` | Usuario | Perfil propio |
| GET | `/habitos/` | Usuario | Hábitos diarios |
| POST | `/habitos/<id>/completar` | Usuario | Cumplimiento idempotente |
| GET | `/admin/` | Admin | Panel y auditoría |
| POST | `/admin/anuncios` | Admin | Borrador |
| POST | `/admin/anuncios/<id>/publicar` | Admin | Publicación |
| POST | `/admin/anuncios/<id>/archivar` | Admin | Archivo |

## 4. Autenticación

El correo se normaliza antes de validar/buscar. Las contraseñas usan scrypt. Una consulta inexistente ejecuta igualmente una comparación contra hash ficticio para reducir enumeración por tiempo. Tras cinco fallos, la cuenta queda bloqueada 15 minutos. Un login correcto reinicia el contador.

Los enlaces de recuperación están firmados, caducan y contienen una firma derivada del hash actual; cambiar la contraseña invalida el token anterior.

## 5. Progreso

- `complete_habit` consulta primero y confía además en la restricción única para carreras concurrentes.
- La inserción y el evento de auditoría se confirman en la misma transacción.
- Los puntos son la suma del catálogo unido a eventos.
- La racha se calcula sobre días distintos.
- Los niveles son: Semilla (0), Explorador (100), Guardián (250) y Leyenda (500).

## 6. Errores

Hay vistas controladas para 400, 403, 404, 429 y 500. El error inesperado entrega un identificador de incidente, registra la traza en servidor y no la expone al usuario.

## 7. Correo

SMTP es configurable por ambiente. Si no está configurado, la respuesta al usuario permanece genérica y se registra una advertencia sin token. Staging debe completar `MAIL_HOST`, `MAIL_USERNAME`, `MAIL_PASSWORD` y `MAIL_FROM` antes de aprobar recuperación.

## 8. Pruebas

La suite cubre registro, duplicados, login/logout, bloqueo, recuperación, token invalidado, redirección abierta, CSRF real, puntos/racha/niveles, idempotencia, perfil, roles, comunicados, health/readiness, SMTP y comandos administrativos.

Resultado: **24 aprobadas, 90,41 % de cobertura**.

## 9. Estado

Backend: ✅ implementado y verificado localmente. SMTP real, PostgreSQL remoto y Staging: 🟡.
