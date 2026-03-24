import psycopg2
import pytest
import pytest_asyncio
from psycopg2.errors import DuplicateDatabase
from sqlalchemy import create_engine as create_sync_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.infrastructure.db.models import Base

from .db.settings import TestDatabaseSettings


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


@pytest_asyncio.fixture
async def db_session(async_engine):
    """Provides isolated db session with auto-rollback."""

    AsyncSessionLocal = async_sessionmaker(
        async_engine, expire_on_commit=False, autoflush=False
    )
    async with AsyncSessionLocal() as session:
        transaction = await session.begin()
        try:
            yield session
        finally:
            await transaction.rollback()
