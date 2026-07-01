from fastapi import FastAPI

from backend.app.api import api_router
from backend.app.config.settings import Settings
from backend.app.core.lifecycle import lifespan
from backend.app.core.logging import configure_logging


def create_app(settings: Settings) -> FastAPI:
    """
    Application Factory.

    Creates and configures the FastAPI application.
    """

    configure_logging(settings)

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI Operations Platform powered by GraphRAG",
        lifespan=lifespan,
    )

    app.state.settings = settings

    app.include_router(api_router)

    return app
