from dataclasses import dataclass
from datetime import datetime
from typing import Self
from uuid import UUID

from src.domain.entities import User as UserEntity


@dataclass(frozen=True, slots=True)
class RegisterUserDTO:
    """Input DTO for user registration."""

    email: str
    password: str


@dataclass(frozen=True, slots=True)
class UserDTO:
    """Output DTO representing user data."""

    id: UUID
    email: str
    username: str
    role: str
    is_confirmed: bool
    is_active: bool
    is_deleted: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user_entity: UserEntity) -> Self:
        """Convert domain User entity to UserDTO."""

        return cls(
            id=user_entity.id,
            email=user_entity.email.value,
            username=user_entity.username.value,
            role=user_entity.role.value,
            is_confirmed=user_entity.is_confirmed,
            is_active=user_entity.is_active,
            is_deleted=user_entity.is_deleted,
            created_at=user_entity.created_at,
            updated_at=user_entity.updated_at,
        )
