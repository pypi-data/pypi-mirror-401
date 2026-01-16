"""Authentication types for Obra.

Lightweight dataclasses for authentication results.
This module is eagerly loaded to support type checking.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class AuthResult:
    """Result of a successful authentication."""

    firebase_uid: str
    email: str
    id_token: str
    refresh_token: str
    auth_provider: str
    display_name: str | None = None
    expires_at: datetime | None = None


__all__ = ["AuthResult"]
