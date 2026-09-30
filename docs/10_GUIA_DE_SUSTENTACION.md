# Guía de sustentación académica

## 1. Tesis

VitaliLab demuestra un proceso completo de ingeniería: se auditó un prototipo con riesgos reales, se preservó Production, se reconstruyó la solución por capas, se protegió la integridad de los datos y cada afirmación se respalda con código, migración o prueba.

## 2. Relato del antes y después

| Antes | Después verificable |
|---|---|
| Flask centralizado | Fábrica y cinco blueprints |
| SQLite compartido | PostgreSQL para ambientes + SQLite solo local |
| Datos mezclados | 7 tablas normalizadas |
| Contraseñas inseguras | Hash scrypt, bloqueo y recuperación |
| Doble puntaje posible | Constraint diario + transacción idempotente |
| UI inconsistente | Sistema visual responsive y accesible |
| Sin pruebas | 24 pruebas, 90,41 % |
| Sin pipeline | CI, Docker y Render Blueprint |

## 3. Exposición sugerida (20–25 min)

1. Problema y usuarios: 2 min.
2. Auditoría original y riesgos: 3 min.
3. Decisiones de arquitectura: 3 min.
4. Modelo de datos e integridad: 4 min.
5. Backend y seguridad: 4 min.
6. Frontend y accesibilidad: 3 min.
7. Git, CI, Render y rollback: 3 min.
8. Demostración: 5 min.
9. Límites y siguientes gates: 2 min.

## 4. Demo reproducible

En Staging y con datos ficticios:

1. Mostrar `/health`, `/ready` y commit desplegado.
2. Registrar una cuenta y explicar el hash/consentimiento sin mostrar secretos.
3. Abrir dashboard en escritorio y móvil.
4. Completar un hábito; intentar repetir y mostrar que no duplica.
5. Editar perfil con medida opcional y explicar el IMC educativo.
6. Entrar como usuario normal a `/admin/` y mostrar 403.
7. Entrar como admin, crear/publicar un comunicado.
8. Mostrar el comunicado en inicio y la auditoría de metadatos.
9. Cerrar sesión.
10. Mostrar CI verde, migraciones y reporte QA.

Preparar capturas locales como respaldo; no contienen credenciales reales.

## 5. Reparto por roles

- Arquitectura: alcance, decisiones y flujo integral.
- DBA: ER, restricciones, índices, migraciones y restauración.
- Backend/seguridad: autenticación, autorización, idempotencia y errores.
- Frontend/UX: sistema visual, responsive y accesibilidad.
- DevOps/QA: ramas, CI, Render, health, rollback y score.

## 6. Preguntas y respuestas

**¿Por qué monolito y no microservicios?**
Porque los dominios comparten transacciones y el volumen académico no compensa el costo distribuido. La modularidad ya permite evolucionar.

**¿Por qué PostgreSQL?**
Por persistencia administrada, concurrencia, restricciones, backups y operación compartida; SQLite queda como herramienta local.

**¿Cómo evitan puntos duplicados?**
La clave única usuario+hábito+fecha protege la DB; el servicio trata un reintento como idempotente y recalcula desde eventos.

**¿Dónde se guardan los puntos?**
No hay un saldo manipulable. Se suman los puntos del catálogo unidos a cumplimientos reales.

**¿Cómo protegen contraseñas?**
Scrypt con sal, límites, bloqueo temporal, token firmado e invalidación tras cambio.

**¿Por qué no dicen 100 % seguro?**
Porque la seguridad absoluta no existe. Se documentan controles, evidencia, límites y gates pendientes.

**¿Qué pasa si falla un despliegue?**
Render conserva despliegues; se vuelve al commit saludable. Los datos solo se restauran desde backup ensayado y con compatibilidad analizada.

**¿Qué harían con contraseñas antiguas en texto?**
No se copian. Se fuerza restablecimiento seguro y se migra el resto de la identidad.

## 7. Frases técnicas correctas

- “Validado localmente” no significa “desplegado”.
- “Cobertura 90,41 %” no significa ausencia de defectos.
- “IMC orientativo” no significa diagnóstico.
- “GO a Staging” no significa aprobación de Production.
- “Backup” solo es confiable después de restaurarlo.

## 8. Checklist

- [ ] Staging y plan B disponibles.
- [ ] Datos completamente ficticios.
- [ ] CI y commit identificables.
- [ ] Ningún secreto en pantalla.
- [ ] Cada diagrama coincide con código.
- [ ] Cada integrante puede explicar la idempotencia.
- [ ] Límites declarados sin ocultarlos.
