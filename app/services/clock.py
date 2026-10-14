from datetime import UTC, datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.models import User


def local_day(user: User):
    """Use one date boundary for the user's habits, goals and reflections."""
    try:
        zone = ZoneInfo(user.profile.timezone)
    except ZoneInfoNotFoundError:
        zone = ZoneInfo("America/Bogota")
    return datetime.now(UTC).astimezone(zone).date()
