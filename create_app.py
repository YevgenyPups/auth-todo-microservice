import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from config.logger import setup_logger

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

    return FastAPI(title="Auth Todo Service", lifespan=lifespan, debug=True)


if __name__ == "__main__":

    app = create_app()

    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
