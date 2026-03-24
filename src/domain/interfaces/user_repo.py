from typing import Protocol

from domain.entities import User as UserEntity


class IUserRepo(Protocol):
    """User repository interface."""

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        ...

    async def save(self, user: UserEntity) -> UserEntity:
        """Save user (create or update)."""
        ...
