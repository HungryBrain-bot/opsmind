from fastapi import APIRouter, Depends

from backend.app.config.settings import Settings
from backend.app.core.dependencies import get_settings
from backend.app.core.logging import get_logger
from backend.app.schemas.health import HealthResponse

logger = get_logger(__name__)

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("", response_model=HealthResponse)
def health(
    settings: Settings = Depends(get_settings),
) -> HealthResponse:
    """
    Health check endpoint.

    Returns the current application status.
    """

    logger.info("health.check.requested")

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,  # or app_env if that's your field
    )
