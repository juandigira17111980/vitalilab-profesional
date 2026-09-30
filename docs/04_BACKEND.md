# Backend de VitaliLab

## 1. Propósito

Definir el comportamiento del servidor, sus módulos, contratos, reglas de negocio y pruebas. Este documento diferencia el backend observado del backend objetivo.

## 2. Estado actual observado

En el commit activo de producción analizado se encontró:

- Flask con rutas, sesiones, consultas SQLite y reglas en el mismo archivo.
- SQL ejecutado directamente.
- Clave de sesión codificada en el código.
- Registro y comparación de contraseñas sin hash seguro.
- Puntos y racha actualizados sin una restricción diaria robusta.
- Ausencia de pruebas automatizadas, migraciones, health check y servidor WSGI de producción verificable.

En una versión posterior que falló al desplegar se observó un intento de usar SQLAlchemy y nuevas entidades, pero sus rutas, modelos y plantillas no comparten el mismo contrato. También se detectaron referencias a endpoints o variables ausentes.

## 3. Diseño objetivo

Se propone mantener Flask y dividir el backend en módulos:

| Módulo | Responsabilidades |
|---|---|
| `auth` | Registro, acceso, cierre, recuperación y protección de sesión |
| `users` | Perfil, preferencias y medidas |
| `habits` | Catálogo, cumplimiento, puntos, rachas y niveles |
| `content` | Contenidos de nutrición, ejercicio y bienestar |
| `admin` | Anuncios, gestión autorizada y auditoría |
| `shared` | Errores, seguridad, validadores y utilidades |

La ruta recibe y valida; el servicio decide; el ORM persiste; la plantilla presenta.

## 4. Contrato de rutas propuesto

Los nombres son la línea base y se validan antes de implementarlos.

| Método | Ruta | Acceso | Comportamiento |
|---|---|---|---|
| GET | `/` | Público | Presenta inicio y propuesta de valor |
| GET/POST | `/auth/register` | Anónimo | Crea cuenta validada |
| GET/POST | `/auth/login` | Anónimo | Autentica y crea sesión |
| POST | `/auth/logout` | Autenticado | Finaliza sesión |
| GET/POST | `/auth/forgot-password` | Anónimo | Inicia recuperación sin revelar si existe el correo |
| GET/POST | `/profile` | Autenticado | Consulta y actualiza perfil propio |
| GET | `/dashboard` | Autenticado | Presenta progreso consolidado |
| GET | `/habits` | Autenticado | Lista hábitos disponibles |
| POST | `/habits/<id>/complete` | Autenticado | Registra cumplimiento idempotente |
| GET | `/content/<slug>` | Según publicación | Muestra contenido educativo |
| GET/POST | `/admin/announcements` | Administrador | Gestiona anuncios |
| GET | `/health` | Técnico | Indica que el proceso responde |

Toda ruta mutante usa `POST`, `PUT/PATCH` o `DELETE`, nunca un `GET` con efectos secundarios.

## 5. Casos de uso críticos

### Registro

1. Normalizar correo.
2. Validar formato, longitud de contraseña y aceptación de privacidad.
3. Rechazar duplicado con respuesta genérica y segura.
4. Generar hash usando una biblioteca reconocida.
5. Crear usuario y perfil mínimo dentro de una transacción.
6. Registrar evento de auditoría sin guardar la contraseña.

### Inicio de sesión

1. Aplicar límite de intentos por identidad/origen con cuidado de no bloquear legítimos.
2. Buscar cuenta por correo normalizado.
3. Verificar hash con función resistente a ataques temporales.
4. Regenerar sesión, establecer cookies seguras y actualizar último acceso.
5. Responder con mensaje genérico ante credenciales inválidas.

### Completar hábito

1. Confirmar sesión y hábito activo.
2. Usar la fecha de negocio según zona horaria definida.
3. Insertar cumplimiento bajo restricción única.
4. Calcular puntos y racha en servidor y en la misma transacción.
5. En reintento, devolver el estado ya existente sin sumar otra vez.

## 6. Servicios de dominio sugeridos

```text
AuthService.register(...)
AuthService.authenticate(...)
ProfileService.update_own_profile(...)
HabitService.complete_habit(user_id, habit_id, date)
ProgressService.calculate_daily_summary(user_id, date)
AnnouncementService.publish(actor, announcement_id)
```

Los servicios reciben tipos validados y devuelven resultados de negocio; no dependen de HTML.

## 7. Manejo de errores

| Tipo | Respuesta al usuario | Registro interno |
|---|---|---|
| Validación | Campo y explicación clara | Nivel informativo, sin valores sensibles |
| No autenticado | Solicitar acceso | Evento mínimo |
| No autorizado | Mensaje 403 | Actor, acción y recurso |
| No encontrado | 404 controlado | Ruta e identificador no sensible |
| Conflicto | Explicar duplicado/idempotencia | Contexto de operación |
| Error inesperado | Mensaje neutral + ID de incidente | Excepción, correlación y traza segura |

Production nunca muestra trazas ni activa `debug=True`.

## 8. Configuración y dependencias

Variables esperadas, solo por nombre:

```text
APP_ENV
SECRET_KEY
DATABASE_URL
SESSION_COOKIE_SECURE
SESSION_COOKIE_SAMESITE
LOG_LEVEL
PASSWORD_RESET_TOKEN_TTL
```

La lista definitiva estará en `.env.example`, sin valores reales. Las dependencias deben ser mínimas, tener versión compatible y revisarse por vulnerabilidades. El paquete de producción debe incluir un servidor WSGI como Gunicorn cuando Render use Linux.

## 9. Pruebas del backend

### Unitarias

- Normalización de correo.
- Política de contraseña.
- Cálculo de IMC con límites y redondeo definidos.
- Cálculo de puntos, nivel y racha.
- Autorización por rol.

### Integración

- Registro crea datos coherentes.
- Correo duplicado no crea segunda cuenta.
- Login correcto/incorrecto y logout.
- Usuario no puede editar otro perfil.
- Dos solicitudes del mismo hábito no duplican puntos.
- Migraciones crean y actualizan el esquema.

### Flujo completo

- Registro → perfil → hábito → dashboard → cierre de sesión.
- Administrador publica un anuncio y usuario lo visualiza.
- Recuperación de acceso sin filtración de existencia de cuenta.

## 10. Criterios de aceptación

- Cero contraseñas o secretos en código, logs o base de datos legible.
- Todas las rutas mutantes protegidas con sesión, autorización y CSRF cuando corresponda.
- Las reglas críticas se ejecutan en servidor y tienen pruebas.
- La app inicia mediante un comando de producción documentado.
- `/health` responde y Render puede usarlo.
- Los errores no muestran trazas al público.
- La documentación de rutas coincide con las rutas reales.

## 11. Estado

El backend objetivo está **🟡 propuesto**. La implementación funcional todavía no se ha realizado ni desplegado en Staging.
