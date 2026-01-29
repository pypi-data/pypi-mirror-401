"""Application lifespan management."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logger import log

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Manage application lifespan events.

    Startup:
        - Log application start
        - Initialize connections (database, cache, etc.)

    Shutdown:
        - Log application shutdown
        - Close connections

    Args:
        app: FastAPI application instance

    Yields:
        None
    """
    # Startup
    log.info(f"Starting {settings.app_name} v{settings.version}")
    log.info(f"Environment: {settings.environment}")
    log.info(f"Debug mode: {settings.debug}")
    log.info(f"Database: {settings.database_url.split('://', 1)[0]}")
    log.warning("Database migrations managed by Alembic")
    log.warning("Run 'make db-upgrade' to apply pending migrations")
    log.success(f"API ready on port {settings.port}")

    yield

    # Shutdown
    log.info(f"Shutting down {settings.app_name}")
    log.success("Shutdown complete")