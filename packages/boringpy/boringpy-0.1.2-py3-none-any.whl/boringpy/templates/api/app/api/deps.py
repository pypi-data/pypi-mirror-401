"""Common dependencies for API routes."""

from collections.abc import AsyncIterator

from app.core.config import Settings, get_settings


async def get_current_settings() -> AsyncIterator[Settings]:
    """
    Dependency to get current settings.

    Yields:
        Application settings
    """
    yield get_settings()
