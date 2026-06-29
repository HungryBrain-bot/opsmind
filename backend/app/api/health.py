from fastapi import APIRouter

from backend.app.config.settings import settings
from backend.app.schemas.health import HealthResponse
from backend.app.core.logging import configure_logging, get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("", response_model=HealthResponse)
def health() -> HealthResponse:
    """
    Health check endpoint.

    Returns the current application status.
    """

    logger.info("health.request")

    
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
    )
