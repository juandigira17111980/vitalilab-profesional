# Seguridad y privacidad

## 1. Alcance

Este documento cubre controles técnicos y de proceso para proteger cuentas, datos personales, información relacionada con salud y la operación en Render. No constituye concepto jurídico; las obligaciones concretas deben validarse según usuarios, institución y jurisdicción.

## 2. Hallazgos críticos observados

- 🔴 Secreto de sesión incluido en código.
- 🔴 Contraseñas almacenadas/comparadas sin hash seguro en la versión activa revisada.
- 🔴 Formularios mutantes sin una protección CSRF verificable.
- 🔴 Reglas de puntos y rachas manipulables mediante solicitudes repetidas.
- 🔴 Scripts de base de datos con acciones destructivas.
- 🟡 No se verificó política de privacidad, recuperación de cuenta, retención ni respuesta a incidentes.
- 🟡 La aplicación maneja medidas corporales; pueden constituir datos sensibles según contexto y uso.

Estas condiciones impiden considerar la versión auditada lista para una promoción profesional sin correcciones.

## 3. Modelo de amenazas simplificado

| Activo | Amenaza | Control principal |
|---|---|---|
| Cuentas | Robo/reutilización de contraseña | Hash robusto, rate limiting, recuperación segura |
| Sesión | Secuestro o fijación | Secreto fuerte, cookie segura, rotación y expiración |
| Perfil/medidas | Acceso de otro usuario | Autorización por propiedad y mínimo privilegio |
| Puntos/racha | Manipulación o repetición | Cálculo en servidor, unicidad y transacción |
| Base de datos | Pérdida o exposición | PostgreSQL privado, backup, cifrado en tránsito y acceso restringido |
| Despliegue | Cambio no autorizado | Ramas protegidas por proceso, PR, secretos en Render y rollback |
| Logs | Filtración de datos | Redacción y política de retención |

## 4. Autenticación y contraseñas

- Usar funciones de hash de contraseña provistas por Werkzeug u otra biblioteca mantenida; Argon2id puede evaluarse según compatibilidad.
- Nunca cifrar de forma reversible ni registrar contraseñas.
- Definir longitud mínima y permitir frases largas, pegado y gestores.
- Mensajes de acceso/recuperación no revelan si una cuenta existe.
- Limitar intentos y registrar señales de abuso sin almacenar datos excesivos.
- Recuperación mediante token aleatorio, de un solo uso, con expiración y almacenamiento seguro.
- Invalidar sesiones relevantes después de un cambio de contraseña.

Si existen cuentas con contraseña en texto legible, el plan debe incluir migración controlada o restablecimiento obligatorio y comunicación responsable.

## 5. Sesiones y cookies

Configuración esperada en Staging/Production:

```text
SESSION_COOKIE_SECURE=true
SESSION_COOKIE_HTTPONLY=true
SESSION_COOKIE_SAMESITE=Lax (o más estricto si el flujo lo permite)
```

- `SECRET_KEY` aleatoria, externa al repositorio y distinta por ambiente.
- Regenerar la sesión al autenticar.
- Expiración razonable y cierre de sesión efectivo.
- No guardar datos sensibles innecesarios en la cookie de sesión.

## 6. Autorización

Cada solicitud valida:

1. Que existe una sesión válida.
2. Que el rol permite la acción.
3. Que el recurso pertenece al usuario cuando aplica.
4. Que el estado del recurso permite la transición.

Ocultar un botón no es una medida de seguridad. El servidor debe rechazar solicitudes directas no autorizadas.

## 7. Entradas, CSRF y contenido

- Proteger formularios y peticiones mutantes con CSRF.
- Validar en servidor longitud, formato, tipo y rango.
- Usar consultas parametrizadas/ORM; nunca concatenar SQL.
- Mantener autoescape de Jinja y revisar cualquier uso de contenido marcado como seguro.
- Restringir subidas por tipo, tamaño y almacenamiento si se incorporan en el futuro.
- Aplicar límites de frecuencia a login, registro, recuperación y acciones abusables.

## 8. Cabeceras y transporte

- HTTPS obligatorio.
- HSTS tras confirmar dominio y subdominios.
- `Content-Security-Policy` adaptada a los recursos reales.
- `X-Content-Type-Options: nosniff`.
- `Referrer-Policy` restrictiva.
- Política de `frame-ancestors` para evitar clickjacking.
- Evitar scripts y estilos inline para facilitar una CSP fuerte.

## 9. Secretos

- Secretos solo en el gestor de variables de Render y en almacenamiento local ignorado por Git.
- Valores diferentes para Local, Staging y Production.
- `.env.example` solo contiene nombres y ejemplos no sensibles.
- Nunca pegar secretos en issues, PR, documentación, capturas o logs.
- Rotar de inmediato cualquier secreto que haya sido publicado.
- Mantener inventario de propietario, propósito, ambiente, fecha de rotación y dependencias, sin registrar el valor.

## 10. Privacidad y datos de salud

Aplicar minimización: pedir solo lo necesario y explicar finalidad. Peso, altura, fecha de nacimiento u otros indicadores pueden requerir controles reforzados.

Antes de Production se debe definir:

- Responsable del tratamiento y canal de contacto.
- Finalidades y base de tratamiento.
- Datos obligatorios y opcionales.
- Tiempo de retención y procedimiento de eliminación/corrección.
- Acceso restringido y registro de operaciones administrativas.
- Política para usuarios menores de edad, si pueden registrarse.
- Texto que aclare que la plataforma es educativa y no sustituye consejo médico.

Referencias iniciales para validación institucional/jurídica:

- [Ley 1581 de 2012 sobre protección de datos personales en Colombia — Función Pública](https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=49981).
- [Orientación de la Superintendencia de Industria y Comercio sobre datos sensibles relativos a la salud](https://sedeelectronica.sic.gov.co/publicaciones/boletin-juridico/concepto/tratamiento-de-datos-sensibles-relativos-la-salud).

## 11. Logs y auditoría

Registrar:

- Inicio/cierre de sesión y fallos agregados.
- Cambios administrativos.
- Errores con ID de correlación.
- Despliegues y migraciones.

No registrar:

- Contraseñas, hashes, tokens o cookies.
- Valores completos de salud.
- Cuerpos de formularios personales.
- URLs con tokens de recuperación.

## 12. Dependencias y cadena de suministro

- Mantener un archivo de dependencias mínimo y versionado.
- Ejecutar análisis de vulnerabilidades y actualización controlada.
- Revisar licencias cuando se incorporen recursos de terceros.
- CI debe instalar desde fuente reproducible, ejecutar pruebas y fallar ante secretos detectados.
- Las acciones de CI se fijan a versiones confiables y con permisos mínimos.

## 13. Respuesta a incidentes

1. Contener: desactivar credencial/ruta afectada sin destruir evidencia.
2. Preservar: registrar hora, versión, logs y alcance con acceso restringido.
3. Erradicar: corregir causa y rotar secretos.
4. Recuperar: desplegar versión validada y vigilar recurrencia.
5. Comunicar: responsables y usuarios según impacto y obligación aplicable.
6. Aprender: documentar causa, control faltante y acción preventiva.

## 14. Checklist antes de Production

- [ ] No hay secretos en Git ni historial relevante sin tratar.
- [ ] Todas las contraseñas usan hash seguro.
- [ ] CSRF, autorización y límites se prueban.
- [ ] Cookies y HTTPS están configurados.
- [ ] CSP y cabeceras se verifican en Staging.
- [ ] Logs no contienen datos sensibles.
- [ ] Backup y restauración funcionan.
- [ ] Dependencias no tienen hallazgos críticos sin aceptar formalmente.
- [ ] Existe política de privacidad revisada.
- [ ] Existe rollback y responsable de incidente.

## 15. Estado

La política y los controles están **🟡 documentados como objetivo**. Los hallazgos críticos pertenecen a la versión revisada y aún deben corregirse mediante código, migraciones y pruebas antes de afirmar cumplimiento.
