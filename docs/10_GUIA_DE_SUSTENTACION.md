# Guía de sustentación académica

## 1. Idea central

VitaliLab debe presentarse como un proceso de ingeniería: se recibió un prototipo, se auditó con evidencia, se identificaron riesgos, se diseñó una arquitectura objetivo y cada mejora se implementa, prueba y despliega de forma controlada.

No se debe afirmar que una propuesta ya está implementada. La transparencia técnica fortalece la sustentación.

## 2. Estructura sugerida de la exposición

| Sección | Tiempo sugerido | Mensaje principal |
|---|---:|---|
| Problema y usuarios | 2 min | Qué necesidad atiende VitaliLab |
| Estado original | 3 min | Cómo funcionaba y qué limitaciones tenía |
| Auditoría y riesgos | 4 min | Evidencia priorizada, no opiniones |
| Arquitectura objetivo | 4 min | Por qué monolito modular y tres ambientes |
| Base de datos | 4 min | Normalización, integridad, migraciones y backup |
| Backend y seguridad | 4 min | Reglas en servidor, autenticación y permisos |
| Frontend y UX | 3 min | Componentes, móvil, accesibilidad y claridad |
| Git, QA e infraestructura | 3 min | Trazabilidad, Staging, pruebas y rollback |
| Demostración y resultados | 5 min | Flujo comprobado en Staging |
| Aprendizajes y siguiente paso | 2 min | Qué se logró y qué sigue |

Ajustar a la duración asignada por la institución.

## 3. Reparto por roles

- Arquitectura/líder: contexto, decisiones, integración y roadmap.
- DBA: modelo entidad-relación, restricciones, migración y recuperación.
- Backend/seguridad: módulos, reglas, autenticación, autorización y pruebas.
- Frontend/UX: recorrido, componentes, accesibilidad y evidencia visual.
- DevOps/QA: Git, ambientes, pipeline, health, rollback y resultados.

Si hay menos estudiantes, una persona asume varias áreas, pero todos deben entender el flujo completo.

## 4. Relato del antes y después

### Antes

- Aplicación Flask monolítica.
- Datos, autenticación y gamificación mezclados.
- SQLite y creación destructiva de esquema.
- Contraseñas y secreto con riesgos críticos.
- Plantillas duplicadas y responsive incompleto.
- Sin pruebas, migraciones ni Staging funcional.

### Después esperado

- Monolito modular con responsabilidades claras.
- PostgreSQL normalizado y migraciones.
- Contraseñas con hash, sesiones y formularios protegidos.
- Reglas de hábitos idempotentes y transaccionales.
- Interfaz reutilizable, móvil y accesible.
- Flujo Local → Staging → Production con pruebas y rollback.

En cada entrega, sustituir “esperado” por resultados concretos de la bitácora.

## 5. Demostración recomendada

La demo se realiza en Staging, nunca improvisando cambios en Production.

1. Mostrar la versión/commit desplegado.
2. Registrar un usuario ficticio.
3. Completar perfil con datos de prueba.
4. Completar un hábito.
5. Repetir la acción y demostrar que no duplica puntos.
6. Mostrar progreso y racha.
7. Intentar una acción no autorizada y mostrar rechazo controlado.
8. Cerrar sesión.
9. Mostrar el reporte de pruebas.
10. Mostrar la bitácora que conecta cambio y evidencia.

Preparar capturas o video corto de respaldo por si falla internet; no incluir secretos ni datos reales.

## 6. Preguntas probables y respuestas

### ¿Por qué no microservicios?

El alcance no justifica su costo operativo. Un monolito modular logra separación, pruebas y mantenibilidad con menos infraestructura.

### ¿Por qué cambiar SQLite?

SQLite sirve localmente, pero una aplicación compartida necesita mejor concurrencia, persistencia administrada, integridad y copias. PostgreSQL cubre esas necesidades.

### ¿Cómo evitan sumar puntos dos veces?

El servidor usa una restricción única por usuario, hábito y fecha y una transacción. Un reintento devuelve el estado existente.

### ¿Cómo protegen las contraseñas?

Se almacena un hash lento y con sal mediante biblioteca mantenida; nunca texto legible. También se protegen sesiones, intentos y recuperación.

### ¿Cómo saben que funciona?

Cada requisito tiene pruebas; la versión pasa por Staging y queda ligada a commit y reporte.

### ¿Qué hacen con datos de salud?

Se minimizan, restringen y excluyen de logs; se define finalidad, retención y eliminación. La plataforma es educativa, no diagnóstica.

### ¿Qué ocurre si falla un despliegue?

Se conserva versión estable, se monitorean smoke tests y existe rollback. Las migraciones se ensayan con backup/restauración.

## 7. Evidencias necesarias

- Diagramas actual/objetivo y modelo entidad-relación.
- Pull requests y commits.
- Resultados de pruebas.
- Capturas antes/después comparables.
- Staging y health check.
- Ensayo de backup/restauración y rollback.
- Matriz de hallazgos y bitácora.

## 8. Qué no mostrar ni afirmar

- Credenciales, tokens, `.env`, conexiones o datos personales.
- Que el sistema es “100 % seguro”.
- Que una propuesta está terminada sin commit, prueba y Staging.
- Que el IMC es un diagnóstico.
- Que un deploy exitoso demuestra calidad por sí solo.
- Que Production se modificó sin autorización y evidencia.

## 9. Lista previa

- [ ] Todos conocen objetivo y reglas.
- [ ] Demo con datos ficticios.
- [ ] Staging funciona desde una versión identificada.
- [ ] Plan B de demostración.
- [ ] Diagramas coinciden con código.
- [ ] Pruebas recientes.
- [ ] Pendientes declarados honestamente.
- [ ] Sin secretos en pantalla.
- [ ] Tiempo y transiciones ensayados.

## 10. Estado

La guía está lista para estudio, pero debe actualizarse con capturas, métricas y resultados después de cada fase.
