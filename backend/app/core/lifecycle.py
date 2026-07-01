"""
Application lifecycle management.

This module defines the startup and shutdown sequence
for the OpsMind application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.config.settings import Settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


def _create_directories(settings: Settings) -> None:
    """
    Create required application directories.
    """

    directories = [
        settings.data_dir,
        settings.logs_dir,
        settings.models_dir,
        settings.data_dir / "raw",
        settings.data_dir / "processed",
        settings.data_dir / "embeddings",
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    logger.info("application.directories.ready")


def _log_startup(settings: Settings) -> None:
    """
    Log application startup information.
    """

    logger.info(
        "application.started",
        extra={
            "app": settings.app_name,
            "version": settings.app_version,
            "environment": settings.app_env,
        },
    )


def _log_shutdown() -> None:
    """
    Log application shutdown.
    """

    logger.info("application.stopped")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application lifecycle.
    """
    logger.info("application.starting")

    settings: Settings = app.state.settings

    _create_directories(settings)

    _log_startup(settings)

    yield

    _log_shutdown()
