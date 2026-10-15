# Dominio principal en Hostinger y NexoStack

Solicitud del propietario: usar `vitalilab.space` y `www.vitalilab.space` para la nueva versión. No eliminar Render ni modificar correo, nameservers, bases de datos o aplicaciones ajenas. Esta conexión no importa cuentas de Render ni convierte el laboratorio en un producto clínico autorizado para datos reales de menores.

## 1. Estado comprobado antes del cambio

- Dominio: `vitalilab.space`. DNS gestionado con nameservers `aster.dns-parking.com` y `helios.dns-parking.com`.
- Captura de Hostinger: `CNAME www → vitalilab.onrender.com`, TTL 14400; `ALIAS @ → www.vitalilab.space`, TTL 14400.
- DNS público confirma que `www` sigue en Render; raíz resolvía a 216.24.57.16 y 216.24.57.18.
- NexoStack: `vitalilab.lab.nexostack.app → 2.24.101.70`.
- No se observó registro CAA restrictivo en la consulta pública de esta revisión. Debe volver a verificarse si falla la emisión.

Un dominio es una dirección, no una copia de archivos. DNS dirige el navegador al servidor; el proxy reconoce el nombre solicitado y el certificado acredita la conexión HTTPS. Las tres piezas deben estar coordinadas.

## 2. Paso del propietario en Hostinger

1. Abre Dominios → `vitalilab.space` → DNS / Nameservers → Registros DNS.
2. Conserva una captura/exportación de la zona actual.
3. Busca **CNAME**, nombre **www**, contenido **vitalilab.onrender.com**.
4. Pulsa el lápiz y cambia **solo el contenido/destino** a **vitalilab.lab.nexostack.app**, sin `https://` ni `/`.
5. Conserva tipo CNAME, nombre www y TTL 14400. Guarda.
6. En la configuración final comprobada, conserva **ALIAS**, nombre **@**, contenido **vitalilab.lab.nexostack.app**. El alias de raíz apunta directamente al destino de NexoStack. No escribas ese destino en el campo Nombre. No agregues un registro A para el mismo nombre www: entraría en conflicto con el CNAME.
7. No cambies nameservers, MX, TXT, SPF, DKIM, DMARC, CAA o registros de otros servicios. No uses «restablecer zona».
8. Avisa al responsable de infraestructura cuando guardes. Un registro actualizado en pantalla no prueba propagación global ni emisión de HTTPS.

Los registros anteriores tienen caché de cuatro horas y Hostinger indica que la propagación puede tardar hasta 24 horas. No prometemos corte instantáneo o sin transición de certificado. Durante la propagación algunas redes pueden mostrar aún Render. No introduzcas datos hasta que se confirme HTTPS válido en ambas direcciones.

## 3. Preparación del servidor sin cambiar DNS

`compose.yaml` conserva los routers del laboratorio y añade dos routers exclusivos `vitalilab-main-http` y `vitalilab-main-https` para la raíz/www. No se utilizan comodines de dominio. Los tres nombres acceden a la misma aplicación y PostgreSQL de VitaliLab; no son ambientes nuevos.

La ruta HTTP redirige a HTTPS. Los certificados del laboratorio siguen independientes. La configuración base **no solicita** certificados para la raíz/www mientras sus DNS sigan en Render. Que una prueba con Host forzado llegue a la app no confirma un certificado público válido para el dominio.

`domain-https.yaml` añade el resolver ya existente `letsencrypt` solo al router principal. `scripts/check_domain_dns.py` exige que ambos nombres resuelvan exclusivamente a `2.24.101.70`; rechaza destino antiguo, mezcla de IP, IPv6 inesperado y errores DNS. No inspecciona ni cambia la cuenta Hostinger.

`apply-domain.sh` solo permite una entrega sin diferencias de aplicación, migraciones, dependencias o wsgi respecto de la activa. Toma respaldo y recrea exclusivamente la web con `--no-deps`, manteniendo base, volumen, proxy y demás proyectos. No ejecuta migraciones ni borra recursos. El despliegue completo normal también selecciona el override HTTPS únicamente si la comprobación DNS pasa.

## 4. Activación HTTPS por infraestructura

Después del cambio en Hostinger:

1. Comparar la zona autoritativa y resolutores públicos para raíz y www. Confirmar que no existe AAAA antiguo y revisar CAA. Una comprobación desde un único resolutor no garantiza propagación mundial.
2. Confirmar el commit aprobado por CI y la ruta activa `/opt/labs/vitalilab/current`.
3. Ejecutar con la cuenta de infraestructura, indicando el SHA completo que contiene esta entrega:

```text
sudo bash /opt/labs/vitalilab/releases/SHA_COMPLETO/deploy/nexostack/apply-domain.sh SHA_COMPLETO --require-dns
```

`SHA_COMPLETO` es un marcador, no una orden lista para copiar. El script devuelve sin modificar servicios si el DNS no está listo. Cuando pasa, añade el override y Traefik solicita certificado para raíz y www. No se reinicia ni reconfigura globalmente el proxy.

4. Verificar **sin desactivar la validación TLS** `https://vitalilab.space/health`, `https://www.vitalilab.space/health` y `/ready` en ambos. La versión debe coincidir con el commit activado.
5. Comprobar redirección HTTP → HTTPS, certificado/SAN/cadena, assets, registro/login/logout, cookies Secure y formularios CSRF usando una cuenta ficticia.
6. Comparar IDs, imágenes, inicios y reinicios de los demás contenedores y de PostgreSQL. Registrar evidencia sin secretos.

Los cookies de sesión son por host. Una persona puede tener que iniciar sesión nuevamente al pasar del dominio del laboratorio a la raíz o a www. No se amplía el dominio de cookies a todos los subdominios. SMTP y recuperación real siguen sujetos a la configuración previamente documentada.

## 5. Qué significa terminado

- Preparado: configuración integrada, web responde a los Host de raíz/www mediante prueba controlada; laboratorio sigue saludable. **DNS/HTTPS principal pueden seguir pendientes.**
- Conectado: registros públicos apuntan al VPS y ambas direcciones muestran el commit esperado con certificado válido.
- Validado: flujos autenticados y coexistencia comprobados; resultado registrado en el PR de la entrega.

Las tres etapas se completaron para el commit `56cee00` y la evidencia quedó en el PR 11. Las tres direcciones sirven la misma aplicación de NexoStack. Cada release posterior debe volver a comprobar versión, TLS y flujos. La edición del 15 de octubre retira el banner académico por solicitud del propietario; no elimina las salvaguardas ni certifica adecuación médica por utilizar un dominio comercial.

## 6. Reversión

Para devolver ambas direcciones al sitio anterior, restaurar el CNAME `www → vitalilab.onrender.com` y el ALIAS `@ → www.vitalilab.space`, según la captura original. La configuración actual de raíz apunta directamente a NexoStack: cambiar solo www dejaría los dos nombres en servidores distintos. La caché también afecta al regreso. No ejecutar esta reversión sin autorización del propietario. Render, su base y el proyecto original se conservan separados.

Un rollback de configuración de NexoStack se realiza con la versión anterior verificada y solo su web. No ejecutar `down -v`, borrar volúmenes, restaurar una base sobre la activa ni reiniciar el VPS/proxy. Los respaldos quedan conservados en el directorio privado del proyecto.

## Fuentes oficiales

- [Hostinger: CNAME, destino, edición y propagación](https://www.hostinger.com/support/4738777-how-to-manage-cname-records-at-hostinger/).
- [Traefik: TLS, resolver y necesidad de DNS correcto](https://doc.traefik.io/traefik/reference/routing-configuration/http/tls/overview/).
