import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from src.infrastructure.config.logger import setup_logger
from src.infrastructure.ioc.di import get_providers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Async context manager for managing the lifespan of the FastAPI app."""

    logging.info("Starting app")

    yield

    logging.info("Stopping app")


def create_app() -> FastAPI:
    """Create and configure FastAPI application instance."""

    setup_logger()

    app = FastAPI(title="Auth Todo Service", lifespan=lifespan, debug=True)
    container = make_async_container(*get_providers().values())

    setup_dishka(container, app)
    return app
