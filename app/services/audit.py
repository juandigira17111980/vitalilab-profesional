from app.extensions import db
from app.models import AuditEvent


def record_event(
    action: str,
    entity_type: str,
    entity_id: str | int | None = None,
    actor_user_id: int | None = None,
    metadata: dict | None = None,
) -> None:
    db.session.add(
        AuditEvent(
            action=action,
            entity_type=entity_type,
            entity_id=str(entity_id) if entity_id is not None else None,
            actor_user_id=actor_user_id,
            metadata_redacted=metadata or {},
        )
    )
