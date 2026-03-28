import psycopg2
import pytest
import pytest_asyncio
from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.application.use_cases import RegisterUser
from src.domain.password_validator import PasswordValidator
from src.infrastructure.auth.password_hasher import PasswordHasher
from src.infrastructure.db.mappers import UserMapper
from src.infrastructure.db.models import Base
from src.infrastructure.db.repos import UserRepo
from src.infrastructure.db.uow import UnitOfWork

from .infrastucture.db.settings import TestDatabaseSettings


@pytest.fixture(scope="session")
def db_settings():
    """Get test db settings."""

    return TestDatabaseSettings()


@pytest.fixture(scope="session")
def create_test_db(db_settings):
    """Create test db using sync url"""

    conn = psycopg2.connect(db_settings.base_db_url)
    conn.autocommit = True
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE {db_settings.TEST_DB_NAME}")
    except DuplicateDatabase:
        # just ignore it
        pass
    finally:
        cursor.close()
        conn.close()


@pytest.fixture(scope="session")
def create_and_delete_tables(db_settings, create_test_db):
    """Create tables for tests and drop them after tests."""

    sync_engine = create_sync_engine(db_settings.sync_url, echo=False)
    try:
        Base.metadata.create_all(sync_engine)
        yield sync_engine
        Base.metadata.drop_all(sync_engine)
    finally:
        sync_engine.dispose()


@pytest_asyncio.fixture
async def async_engine(db_settings, create_and_delete_tables):
    """Provides async engine for tests."""

    engine = create_async_engine(
        db_settings.async_url, echo=False, pool_size=10, max_overflow=2
    )
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(loop_scope="function")
async def db_session(async_engine):
    """Provide database session per test."""

    session_maker = async_sessionmaker(
        async_engine, expire_on_commit=False, autoflush=False
    )
    async with session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture
def user_repo(db_session):
    """Provide user repo instance for tests."""

    return UserRepo(db_session, UserMapper)


@pytest.fixture
def uow(db_session, user_repo):
    """Provide uow instance for tests."""

    return UnitOfWork(db_session, user_repo)


@pytest.fixture(scope="session")
def password_hasher():
    """Provide password hasher instance for tests."""

    return PasswordHasher()


@pytest.fixture(scope="session")
def password_validator():
    """Provide password validator instance for tests."""

    return PasswordValidator()


@pytest.fixture
def register_user(uow, password_validator, password_hasher):
    """Provide register use case instance for tests."""

    return RegisterUser(uow, password_validator, password_hasher)
