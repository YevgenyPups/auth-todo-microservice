from typing import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..config.db import DBSettings


class SettingsProvider(Provider):
    """Provides application configuration settings."""

    @provide(scope=Scope.APP)
    def db_settings(self) -> DBSettings:
        """Provide database settings from environment variables."""

        return DBSettings()


class DBSessionProvider(Provider):
    """Provide database settings from environment variables."""

    @provide(scope=Scope.APP)
    def get_session_engine(self, db_settings: DBSettings) -> AsyncEngine:
        """Create async database engine with connection pooling."""

        return create_async_engine(
            url=db_settings.async_url,
            echo=db_settings.DEBUG,
            pool_size=10,
            max_overflow=2,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: AsyncEngine) -> async_sessionmaker:
        """Create session factory bound to the engine."""

        return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

    @provide(scope=Scope.REQUEST)
    async def get_session(
        self, session_factory: async_sessionmaker
    ) -> AsyncIterator[AsyncSession]:
        """Create database session per HTTP request."""

        async with session_factory() as session:
            yield session
