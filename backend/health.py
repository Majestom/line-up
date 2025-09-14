from datetime import datetime, timezone
from fastapi import APIRouter

from config import settings
from models import HealthResponse
from api_client import reqres_client

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for monitoring and load balancer probes.

    Checks the status of the service and its dependencies.

    Returns:
        HealthResponse: Service health information including external API status
    """
    # Check external API availability
    external_api_status = await reqres_client.check_health()

    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(timezone.utc).isoformat(),
        version=settings.version,
        external_api_status=external_api_status,
        environment=settings.node_env
    )