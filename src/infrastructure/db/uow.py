import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.interfaces.user_repo import IUserRepo

logger = logging.getLogger(__name__)


class UnitOfWork:
    """SQLAlchemy Unit of Work pattern implementation."""

    def __init__(self, session: AsyncSession, user_repo: IUserRepo):
        """Initialize with async SQLAlchemy session."""

        self._session = session
        self.user_repo = user_repo

    async def __aenter__(self):
        """Enter context. Returns self."""
        await self._session.begin()
        xid = await self._session.scalar(text("select pg_current_xact_id()"))
        logger.debug(f"Transaction started: {xid}")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """Exit context. Rollback if exception, otherwise require explicit commit."""

        if exc_type is not None:
            logger.debug(f"Transaction will rollback due to {exc_type.__name__}: {exc}")
            await self.rollback()
        else:
            await self.commit()

    async def commit(self) -> None:
        """Commit transaction explicitly."""

        xid = await self._session.scalar(text("select pg_current_xact_id()"))
        await self._session.commit()
        logger.debug(f"Transaction committed: {xid}")

    async def rollback(self) -> None:
        """Rollback transaction explicitly."""

        xid = await self._session.scalar(text("select pg_current_xact_id()"))
        await self._session.rollback()
        logger.debug(f"Transaction rolled back: {xid}")
