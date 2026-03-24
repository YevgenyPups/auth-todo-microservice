from pydantic_settings import BaseSettings, SettingsConfigDict


class DBSettings(BaseSettings):
    """
    Database connection settings.

    Provides two connection URLs:
    - async_url: for application (inside Docker container, uses internal port)
    - sync_url: for Alembic migrations (from host machine, uses external port)
    """

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_EXTERNAL_PORT: int
    DB_EXTERNAL_HOST: str = "localhost"
    DB_INTERNAL_PORT: int = 5432
    DEBUG: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def async_url(self) -> str:
        """Async URL for application."""

        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_INTERNAL_PORT}"
            f"/{self.DB_NAME}"
        )

    @property
    def sync_url(self) -> str:
        """Sync URL for Alembic migrations."""

        return (
            f"postgresql://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_EXTERNAL_HOST}:{self.DB_EXTERNAL_PORT}"
            f"/{self.DB_NAME}"
        )
