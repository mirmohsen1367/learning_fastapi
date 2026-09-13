"""Import all active database models so Alembic can discover them."""

from app.models.song import Song, Album
from app.models.user import User

__all__ = ["Album", "Song", "User"]
