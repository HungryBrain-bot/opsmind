"""
Centralized logging configuration for OpsMind.

This module configures application logging and provides
a consistent logger interface for all application modules.
"""

import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from backend.app.config.settings import Settings

LOGGER_NAME = "opsmind"

TEXT_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs log records as JSON.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        return json.dumps(log_record)


def configure_logging(settings: Settings) -> None:
    """
    Configure the OpsMind logging system.

    This function initializes the application logger and
    configures console/file handlers based on application settings.
    """

    logger = logging.getLogger(LOGGER_NAME)

    # Prevent duplicate log messages when running with --reload
    logger.handlers.clear()

    logger.setLevel(settings.log_level.upper())

    logger.propagate = False

    #
    # Formatter
    #
    if settings.log_format.lower() == "json":
        formatter: logging.Formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(TEXT_FORMAT)

    #
    # Console Handler
    #
    if settings.enable_console_logging:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    #
    # File Handler
    #
    if settings.enable_file_logging:
        log_path = Path(settings.log_file)

        # Create logs directory if it doesn't exist
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_path,
            maxBytes=5 * 1024 * 1024,   # 5 MB
            backupCount=5,
            encoding="utf-8",
        )

        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    logger.info("application.logging.configured")


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Example:
        logger = get_logger(__name__)
    """

    if name.startswith("backend.app."):
        name = name.replace("backend.app.", "")

    return logging.getLogger(f"{LOGGER_NAME}.{name}")