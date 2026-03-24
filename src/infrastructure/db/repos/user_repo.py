import logging

from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities import User as UserEntity

from ..mappers import UserMapper
from ..models import User as UserModel

logger = logging.getLogger(__name__)


class UserRepo:
    """Repository implementation for User using SQLAlchemy."""

    __slots__ = ("_session", "_mapper")

    def __init__(self, session: AsyncSession, mapper: UserMapper):
        self._session = session
        self._mapper = mapper

    async def exists_by_email(self, email: str) -> bool:
        """Check if user with given email exists."""

        stmt = select(exists().where(UserModel.email == email))
        result = await self._session.execute(stmt)
        return result.scalar()

    async def save(self, user_entity: UserEntity) -> UserEntity:
        """Save user (create or update)."""

        user_model = self._mapper.to_model(user_entity)
        self._session.add(user_model)
        await self._session.flush()
        logger.info("New user created. User id: %s", user_model.id)
        return self._mapper.to_entity(user_model)
