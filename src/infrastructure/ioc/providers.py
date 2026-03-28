from typing import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.application.use_cases import RegisterUser
from src.domain.interfaces.password_hasher import IPasswordHasher
from src.domain.interfaces.uow import IUnitOfWork
from src.domain.interfaces.user_repo import IUserRepo
from src.domain.password_validator import PasswordValidator
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.db.uow import UnitOfWork

from ..config.db import DBSettings
from ..db.mappers import UserMapper
from ..db.repos import UserRepo


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


class MapperProvider(Provider):
    """Provider for domain mappers."""

    @provide(scope=Scope.APP)
    def get_user_mapper(self) -> UserMapper:
        """Provide user mapper."""

        return UserMapper()


class RepoProvider(Provider):
    """Provider for repository instances."""

    @provide(scope=Scope.REQUEST)
    def get_user_repo(session: AsyncSession, mapper: UserMapper) -> IUserRepo:
        """Provides a UserRepository instance."""

        return UserRepo(session, mapper)


class UOWProvider(Provider):
    """Provider for Unit of Work instances."""

    @provide(scope=Scope.REQUEST)
    def get_uow(session: AsyncSession, user_repo: IUserRepo) -> IUnitOfWork:
        """Provides a UnitOfWork instance."""

        return UnitOfWork(session, user_repo)


class HelperProvider(Provider):
    """Provider for helper instances."""

    @provide(scope=Scope.APP)
    def get_password_hasher(self) -> IPasswordHasher:
        """Provides a PasswordHasher instance."""

        return PasswordHasher

    @provide(scope=Scope.APP)
    def get_password_validator(self) -> PasswordValidator:
        """Provides a PasswordValidator instance."""

        return PasswordValidator()


class UseCaseProvider(Provider):
    """Provider for use cases instances."""

    @provide(scope=Scope.REQUEST)
    def get_register_user(
        self,
        uow: IUnitOfWork,
        password_validator: PasswordValidator,
        password_hasher: IPasswordHasher,
    ) -> RegisterUser:
        """Provides a RegisterUser instance."""

        return RegisterUser(uow, password_validator, password_hasher)
