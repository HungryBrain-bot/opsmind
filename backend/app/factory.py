from fastapi import FastAPI

from backend.app.api import api_router
from backend.app.config.settings import Settings


def create_app(settings: Settings) -> FastAPI:
    """
    Application Factory.

    Creates and configures the FastAPI application.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="AI Operations Platform powered by GraphRAG",
    )

    app.include_router(api_router)

    return app
