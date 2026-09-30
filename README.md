# VitaliLab Profesional

Repositorio privado de trabajo para auditar, estabilizar y evolucionar VitaliLab sin modificar la producción actual hasta contar con aprobación expresa.

## Estado actual

- Producción permanece en el repositorio original y en el servicio actual de Render.
- Este repositorio no contiene bases de datos, usuarios, contraseñas ni secretos.
- La rama `staging` es la base de integración y pruebas.
- Los cambios se realizan en ramas de trabajo y se integran mediante Pull Request.

## Flujo de ramas

```text
main                 producción aprobada
staging              integración y despliegue de prueba
feat/*, fix/*         funcionalidades y correcciones
docs/*                auditoría y documentación
```

## Orden de intervención

1. Seguridad y control de datos.
2. Modelo PostgreSQL y migraciones.
3. Backend modular Flask.
4. Frontend, UX y accesibilidad.
5. QA, observabilidad y despliegue en Staging.
6. Aprobación explícita antes de producción.

## Documento principal

Ver [Auditoría profunda y plan de mejora](docs/AUDITORIA_PROFUNDA_Y_PLAN_DE_MEJORA.md).

## Regla de seguridad

Nunca se deben versionar archivos `.env`, bases SQLite, respaldos, tokens, claves o datos personales. Usar `.env.example` únicamente como plantilla sin valores reales.
Repositorio profesional para auditoria y evolucion segura de VitaliLab
