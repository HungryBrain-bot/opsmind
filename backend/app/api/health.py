from fastapi import APIRouter

from backend.app.config.settings import settings
from backend.app.schemas.health import HealthResponse

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

    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.app_env,
    )
