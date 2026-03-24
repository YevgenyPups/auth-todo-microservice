from pydantic_settings import BaseSettings, SettingsConfigDict


class TestDatabaseSettings(BaseSettings):
    """Test Database connection settings."""

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_INTERNAL_PORT: int = 5432
    TEST_DB_NAME: str = "auth_db_test"
    BASE_DB_NAME: str = "postgres"
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def async_url(self) -> str:
        """Async URL for connection to test db"""

        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_INTERNAL_PORT}"
            f"/{self.TEST_DB_NAME}"
        )

    @property
    def sync_url(self) -> str:
        """Sync URL for Alembic migrations."""

        return (
            f"postgresql://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_INTERNAL_PORT}"
            f"/{self.TEST_DB_NAME}"
        )

    @property
    def base_db_url(self) -> str:
        """Sync URL for connection to base db."""

        return (
            f"postgresql://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_INTERNAL_PORT}"
            f"/{self.BASE_DB_NAME}"
        )
