# Verificación y publicación: personalización y rutinas propias

Fecha de corte: 15 de octubre de 2026, America/Bogota. Revisión focalizada de la ampliación y de su convivencia con el sistema existente. No es una certificación clínica, jurídica ni un pentest.

## 1. Resultado ejecutivo

La ampliación está implementada y publicada en **https://vitalilab.space**, sobre el servicio existente de **NexoStack**. `www.vitalilab.space` y `vitalilab.lab.nexostack.app` resuelven al mismo servicio y base. No se desplegó ni modificó el servicio original de Render.

Versión web comprobada: `81b56501281b26553d14079d6b3899fadbf15267`. Migración: `c842d6e190ab`. El esquema contiene diecisiete tablas de negocio más `alembic_version`. `main` permanece en `e0ec6e5730bdb1e7a5f0154e20c04bb09be71408`; el flujo de la publicación existente utiliza `staging`.

Veredicto de esta entrega: **funcionalidad técnica verificada, con restricciones operativas documentadas**. No se declara «100/100» ni autorización para empezar a recoger datos reales de menores. La verificación institucional sigue siendo obligatoria. Retirar los avisos académicos de la interfaz no sustituye las condiciones de operación señaladas en la sección 6.

## 2. Trazabilidad reproducible

| Evidencia | Identificador o resultado |
|---|---|
| Cambios funcionales y revisión final | `142c51c2e9d137f5abde5ccfc0fa299ed2f937f4`, `9b5bfe731594bc942eaa0970d10310ae52d69a99` |
| Integración | [PR 12](https://github.com/juandigira17111980/vitalilab-profesional/pull/12), rama de funcionalidad hacia `staging` |
| CI de revisión final | [38689815754](https://github.com/juandigira17111980/vitalilab-profesional/actions/runs/38689815754), tres trabajos correctos |
| CI del commit integrado y publicado | [38689996532](https://github.com/juandigira17111980/vitalilab-profesional/actions/runs/38689996532), tres trabajos correctos |
| Integridad del archivo enviado | SHA-256 `25b156a08d1a4cf7861c4770832035fb6b6f66f09f94804f4e4d0022ada6c775` |
| Release anterior conservado | `56cee00ba2f297e33b16db8bf1870bb62b115a33` |
| Respaldo previo a migrar | `vitalilab-20261015T060317450941768Z.dump` |
| Respaldo posterior restaurado | `vitalilab-20261015T060504210666542Z.dump`, checksum verificado |
| Esquema publicado | Upgrade desde `a903b5d7e214`; `db check` sin nuevas operaciones |
| Convivencia | Solo se sustituyó `vitalilab-web-lab`; PostgreSQL y otros 29 contenedores conservaron ID, inicio y reinicios |

El repositorio se mantiene público por decisión expresa del propietario del 15 de octubre. No se versionan secretos, dumps ni registros personales. Los archivos de evidencia detallada de contenedores y las copias permanecen en el directorio privado de VitaliLab del servidor.

## 3. Matriz de aceptación ejecutada

| Requisito | Prueba y resultado |
|---|---|
| Sin banners de laboratorio o datos ficticios | Plantilla base y textos actualizados; portada pública comprobada |
| Colegio y grupo manuales | Formulario y validación; solicitud pendiente sin crear permisos ni colegios autorizados automáticamente |
| Acceso docente verificado | Pruebas de revisión administrativa y asignación; marcar docente no concede grupos; cuenta normal recibe 403 |
| Personalización una vez | Estudiante autorizado completa el flujo; siguientes accesos van a Hoy sin guardar otra medición |
| Medición antes del objetivo | GET/POST directo no permite saltar autorización, medición ni consentimiento; IMC visible en el segundo paso |
| Edad contextual en estudiantes | Fecha de nacimiento exigida al guardar mediciones escolares; sin umbrales adultos aplicados a menores |
| Rutinas por propósito y preferencia | Filtros de postura, energía o fuerza y modalidad de movimiento; no se prescribe carga según IMC |
| Rutinas propias privadas | Crear, editar y archivar; lectura ajena 404; control de revisión 409; límite de rutinas y ejercicios |
| Datos de cada ejercicio | Series, repeticiones o segundos, descansos, orden, instrucciones; límites en formulario y base |
| Demostraciones | SVG locales con texto alternativo; ejercicio libre permite no elegir una ilustración inexacta |
| Temporizador | Inicio, pausa y reinicio probados; no registra actividad automáticamente |
| XP sin duplicación | Rutinas guiadas y privadas comparten el hábito diario; repetición y concurrencia PostgreSQL comprobadas |
| Archivo conserva historial | Desactiva la rutina, no borra sus actividades ni los puntos ganados |
| Conservación de datos previos | CI migra una base en la revisión anterior con perfil y medición; comprueba valores y ausencia de consentimiento fabricado |
| Restauración completa | CI y servidor: dump restaurado en otra base, revisión y conteos de las 17 entidades iguales |
| Documentación | Manual progresivo, referencia de todas las columnas y rutas, criterios y esta evidencia |

### Pruebas automatizadas

150 pruebas locales aprobadas, cobertura total **94,89 %**. Ruff y formato correctos; Bandit sin hallazgos de la severidad evaluada; auditoría de dependencias de CI correcta. Cinco advertencias de deprecación de dependencias no fueron errores. Esto no significa que el 94,89 % de todos los comportamientos posibles esté demostrado.

PostgreSQL 18 en CI comprueba migración, integridad, aislamiento escolar, registro concurrente, restricción de dosis, coherencia ORM/esquema y restauración. Las pruebas SQLite de desarrollo no se presentan como sustituto de esas pruebas PostgreSQL.

### Navegador y accesibilidad

En entorno local con CSRF activo y cuentas ficticias se probaron 37 combinaciones de pantalla/estado y tamaño, incluyendo 320, 390 y 1440 píxeles. Se recorrieron estudiante, cuenta personal, administración, revisión de solicitudes, docente y proyección. No quedaron desbordes horizontales, identificadores repetidos, referencias ARIA rotas ni infracciones detectadas por las reglas automáticas WCAG A/AA utilizadas.

En el dominio público se revisaron portada y biblioteca a 320, 390 y 1440 píxeles: seis combinaciones sin desborde, imágenes rotas ni IDs repetidos. Se inspeccionaron capturas móviles de tarjetas y ejercicios. La comprobación automática de accesibilidad completa corresponde al entorno local; la política CSP pública bloqueó la inyección de la herramienta de auditoría y no se debilitó para ejecutarla. No se declara certificación WCAG ni una prueba completa con lectores de pantalla.

### Prueba funcional del dominio

Solo se modificó una cuenta de verificación ficticia ya existente. Se completó medición y objetivo; se creó y editó una rutina, se registró dos veces y se archivó. La base conserva una rutina archivada y un único registro de esa rutina. El siguiente login y logout se comprobaron por separado: acceso a `/panel`, sin repetir personalización. Se verificaron cookie Secure/HttpOnly/SameSite Lax y sin alcance de dominio compartido, vistas privadas sin caché y rechazo 403 de administración y docentes.

Durante el ensayo, una comprobación esperaba el nombre incorrecto de una tarjeta; se corrigió la expectativa, no el producto. También se recibió un 429 al repetir accesos demasiado rápido. Se respetó el límite y el login posterior pasó; no se desactivó el control para conseguir un resultado favorable.

Los tres nombres públicos devolvieron salud y disponibilidad con el SHA previsto bajo validación TLS normal, sin desactivar la comprobación de certificados.

## 4. Hallazgos de la ampliación corregidos

| Código | Hallazgo | Responsable técnico | Corrección y evidencia |
|---|---|---|---|
| PERS-01 | La validación individual opcional no garantizaba repeticiones o segundos | Backend/DBA | Validación cruzada y CHECK SQL; entradas vacías rechazadas |
| PERS-02 | Formularios de acciones repetían el ID del CSRF | Frontend | Token oculto sin ID en listas; repetición de auditoría DOM correcta |
| PERS-03 | El estilo podía mostrar el botón de quitar cuando debía estar oculto | Frontend/UX | Regla `[hidden]` explícita; formulario inicial y clonado comprobados |
| PERS-04 | Clonar ejercicios debía actualizar referencias de accesibilidad | Frontend | Renumeración de name/id/for/aria-describedby; auditoría sin referencias rotas |
| PERS-05 | Un formulario escolar antiguo podía competir con la solicitud manual | Backend | Bloqueo del propietario y rechazo de solicitudes simultáneas por el camino legado |
| PERS-06 | Un cambio de carpeta de release podía recrear la base por el bind de inicialización | Infraestructura | Base existente validada y conservada; ID, arranque y reinicios iguales en publicación |
| PERS-07 | Un DNS temporalmente fallido podía retirar la configuración TLS principal | Infraestructura | Fallo cerrado si TLS principal ya está activo; no se elimina el resolver |

No se encontraron críticos abiertos de esta ampliación en los flujos evaluados. Esto no equivale a afirmar que no existe ninguna vulnerabilidad en todo el sistema.

## 5. Despliegue, convivencia y reversión

El archivo de un commit con CI verde se validó por checksum y por nombres/tipos de sus miembros antes de extraerlo en una carpeta nueva y acotada. Se validó la sintaxis de los scripts y la configuración. Se tomó respaldo antes de migrar. La migración fue aditiva; no se borraron tablas anteriores ni se rellenaron consentimientos por defecto.

El resolver DNS del VPS todavía tenía una respuesta desactualizada para `www`. La comprobación de activación utilizó un espacio de montaje privado de ese proceso con resolución pública, verificando ambos nombres. No se cambió el DNS global, Hostinger, el proxy compartido ni la configuración de los otros proyectos.

PostgreSQL mantuvo su contenedor y volumen existentes; la cuenta web recibió permisos DML sobre las tres tablas nuevas, sin privilegios administrativos. Se sustituyó únicamente la web de VitaliLab. Las evidencias antes/después comparan los 31 contenedores, no solo su estado visual.

Después de publicar se generó otro dump y se restauró en una base temporal de nombre explícito. Alembic, número de tablas y conteos de las 17 entidades coincidieron. Se eliminó únicamente esa base temporal tras la prueba; el dump y la base activa se conservaron. No se probaron tiempos de recuperación de todo el VPS ni pérdida del servidor completo.

La reversión documentada conserva el esquema aditivo y usa el ayudante nuevo `rollback-web.sh` para activar una imagen anterior compatible, sin migrar ni recrear la base. La imagen y carpeta anteriores permanecen disponibles. Su sintaxis se validó en CI; **no se ejecutó una reversión deliberada del sitio público** en esta entrega. Antes de usarla se debe volver a verificar compatibilidad y generar un respaldo. No ejecutar el script de despliegue antiguo contra una revisión de Alembic que ese código desconoce.

## 6. Pendientes operativos y responsables

El contexto incluye datos personales sensibles y posible alumnado menor de edad. Se aplica mayor cautela a autorización, privacidad y recuperación. No se asigna un puntaje de producción integral a partir de este muestreo de una ampliación.

| Código | Pendiente y riesgo | Nivel para operación real | Responsable | Acción y condición de cierre |
|---|---|---|---|---|
| OPS-01 | No se aportaron evidencias de procedimiento institucional, responsable de datos y autorizaciones de representantes | Alto; bloquea incorporación de menores reales | Propietario e institución | Definir responsable, soportes, finalidades, acceso, conservación y revocación; registrar autorización antes de aprobar vinculaciones. No se presume aceptación de riesgo |
| OPS-02 | Respaldo local no cubre pérdida completa del VPS; no se probó copia externa automática | Alto para continuidad productiva | Infraestructura/DBA y propietario | Elegir destino cifrado independiente, restringir acceso y ensayar recuperación; definir RPO/RTO con evidencia antes de ofrecer garantías de continuidad |
| OPS-03 | SMTP y recepción real de recuperación de contraseña no comprobados | Medio; limita recuperación autónoma | Backend/infraestructura | Configurar proveedor y remitente verificado con secretos fuera de Git; probar envío y recepción con cuentas autorizadas |
| OPS-04 | Monitor local no demuestra aviso externo entregado | Medio | Infraestructura/propietario | Elegir canal y destinatarios, provocar una alerta controlada y registrar su recepción |
| OPS-05 | Rutinas generales y esquemas no cuentan con validación clínica individual | Alto si se ofrecen como prescripción o plan escolar validado | Responsable de bienestar/institución | Validar contenidos y adaptaciones antes de ese uso; conservar la selección por objetivo, no por etiqueta de IMC |
| OPS-06 | Limitador en memoria, sesión sin revocación global al cambiar contraseña | Medio; endurecimiento pendiente | Backend/seguridad | Mantener una sola instancia actual, evaluar almacén persistente antes de escalar y añadir versión de sesión con pruebas de revocación |
| OPS-07 | Sin pentest formal, revisión asistiva completa ni prueba de carga representativa | No revisado; no se presume aprobado | Seguridad, QA/UX e infraestructura | Ejecutar verificaciones específicas antes de ampliar público, volumen o compromisos de servicio; registrar alcance y resultados |

No se contrataron proveedores, enviaron invitaciones ni inventaron autorizaciones para cerrar estas tareas. Los responsables son perfiles de trabajo propuestos; no se atribuye aceptación formal a una persona sin su confirmación.

## 7. Uso y estudio de la entrega

1. Entrar a **Mi perfil** y escoger personal o institucional. Para el enfoque escolar, escribir colegio y grupo en **Mi colegio** y enviar la solicitud. La administración revisa y vincula con entidades verificadas; un docente necesita además asignación a grupos.
2. Abrir **Personalizar mis rutinas**. Estudiantes deben tener verificación/autorización antes de guardar medidas. Completar la medición y confirmar el guardado.
3. Ver el IMC descriptivo, elegir propósito y modalidad de movimiento. El sistema no asigna una carga por peso.
4. En **Rutinas**, consultar **Para mi objetivo** o crear una rutina con ejercicios propios. Una ilustración solo se elige si representa la actividad; no se inventa una demostración de cualquier ejercicio escrito.
5. Guardar, abrir y registrar la actividad. Repetir el registro no duplica XP. Archivar retira la rutina activa conservando la bitácora.
6. Para aprender el código, empezar por el [manual integral](26_MANUAL_INTEGRAL_DEL_SISTEMA.md) y contrastar una acción con el [diccionario y rutas](27_DICCIONARIO_Y_RUTAS_GENERADAS.md). Practicar con datos ficticios en local, no con registros reales de estudiantes.

El manual de estudio explica el sistema completo; esta entrega complementa, no reescribe como actuales, los informes históricos anteriores. La copia PDF para lectura fue renderizada y revisada visualmente, con 35 páginas; el texto versionado sigue siendo la fuente mantenible.

## 8. Alcance de esta auditoría

Esta revisión se basa en código, configuración, documentación, capturas y ejecuciones compartidas. Incluyó inspección directa del repositorio y comprobaciones acotadas del runtime de NexoStack; no sustituye la inspección de otros repositorios no compartidos, un penetration test formal ni una revisión humana integral línea por línea de autenticación o datos regulados.

En profundidad: código nuevo, reglas de propiedad, autorización para mediciones, solicitud escolar, validaciones, idempotencia, migración, respaldos y convivencia del despliegue. Por muestreo: módulos existentes cubiertos por regresión y recorridos de navegador. No revisado/aprobado: soportes jurídicos reales, revisión clínica, entregabilidad SMTP, recuperación total del VPS, prueba de carga representativa y certificación de accesibilidad.

La evidencia corresponde a esta versión y fecha. Un cambio posterior de esquema, dependencias, permisos, DNS o infraestructura requiere repetir las comprobaciones pertinentes.

### Criterios utilizados

- `auditor-qa-final`: evidencia por criterio, pruebas negativas, alcance y pendientes con responsable; sin certificación inventada.
- `desarrollador-web-fullstack` y `chief-ux-officer`: recorrido progresivo, formularios accesibles, controles compactos y auditoría móvil.
- `director-creativo-ai` y `copywriter-senior`: coherencia visual de las guías y textos de autonomía, sin estigma corporal ni promesas clínicas. Se eligieron SVG propios, no una campaña generativa.
- `arquitecto-backend-desktop` y `arquitecto-dba-empresarial`: autorización en servidor, transacciones, propiedad privada, restricciones e integridad de la migración.
- `arquitecto-infra-devops` y `git-github-devops`: release por SHA y CI, respaldo, reversión acotada y convivencia sin cambios en otros proyectos.
