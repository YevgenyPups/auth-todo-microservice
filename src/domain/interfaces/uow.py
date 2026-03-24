from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from ..interfaces.user_repo import IUserRepo


class IUnitOfWork(Protocol):
    """Transaction boundary protocol.

    Manages atomic operations with explicit commit and automatic rollback
    on exceptions. Used as a async context manager.
    """

    _session: AsyncSession
    user_repo: IUserRepo

    async def __aenter__(self):
        """Enter context, start transaction."""
        ...

    async def __aexit__(self, exc_type, exc, tb):
        """Exit context. Rollback if exception, otherwise commit."""
        ...

    async def commit(self) -> None:
        """Commit transaction explicitly."""
        ...

    async def rollback(self) -> None:
        """Rollback transaction explicitly."""
        ...
