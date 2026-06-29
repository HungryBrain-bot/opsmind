from fastapi import FastAPI

from backend.app.api import api_router
from backend.app.config.settings import Settings
from backend.app.core.logging import configure_logging, get_logger


def create_app(settings: Settings) -> FastAPI:
    """
    Application Factory.

    Creates and configures the FastAPI application.
    """

    configure_logging(settings)

    logger = get_logger(__name__)

    logger.info("application.starting")

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI Operations Platform powered by GraphRAG",
    )

    app.include_router(api_router)

    logger.info("application.started")

    return app
