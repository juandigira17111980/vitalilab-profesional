# Cómo contribuir a VitaliLab

## Flujo obligatorio

1. Partir de `staging` actualizado.
2. Crear una rama `feat/*`, `fix/*`, `refactor/*`, `test/*` o `docs/*`.
3. Mantener commits pequeños con formato `tipo(alcance): descripción`.
4. Abrir Pull Request hacia `staging`.
5. Exigir pruebas, revisión y validación de seguridad antes de integrar.
6. Promover de `staging` a `main` únicamente después de aprobación funcional.

## Reglas de seguridad

- Nunca subir `.env`, tokens, claves, bases SQLite, respaldos o datos personales.
- No registrar contraseñas, cookies, tokens ni información de salud en logs.
- Toda modificación de esquema debe usar una migración versionada y tener plan de rollback.
- No realizar despliegues manuales a producción desde ramas de trabajo.

## Checklist de Pull Request

- [ ] El cambio tiene alcance claro.
- [ ] No contiene secretos ni datos personales.
- [ ] Incluye pruebas proporcionales al riesgo.
- [ ] Las migraciones fueron revisadas y son reversibles o tienen recuperación documentada.
- [ ] La documentación fue actualizada.
- [ ] Fue validado en Staging.
