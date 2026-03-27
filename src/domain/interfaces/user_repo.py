from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.mappers import UserMapper

from ..entities import User as UserEntity


class IUserRepo(Protocol):
    """User repository interface."""

    _session: AsyncSession
    _mapper: UserMapper

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        ...

    async def save(self, user: UserEntity) -> UserEntity:
        """Save user (create or update)."""
        ...
