from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4

from ..enums import UserRole
from ..value_objects import Email, Username


@dataclass(slots=True, repr=True)
class User:
    """User entity representing a registered user in the system."""

    email: Email
    password_hash: bytes = field(repr=False)

    id: UUID = field(default_factory=uuid4)
    username: Username = field(
        default_factory=lambda: Username("user_" + uuid4().hex[:8])
    )
    role: UserRole = UserRole.CLIENT
    is_confirmed: bool = False
    is_active: bool = False
    is_deleted: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
