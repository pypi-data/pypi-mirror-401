"""Health check endpoints."""

from fastapi import APIRouter

from app.core.logger import log

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.

    Returns:
        Health status
    """
    log.debug("Health check requested")
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> dict[str, str]:
    """
    Readiness check endpoint (for Kubernetes).

    Returns:
        Readiness status
    """
    # Add checks for database, cache, external services, etc.
    log.debug("Readiness check requested")
    return {"status": "ready"}