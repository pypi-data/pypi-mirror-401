"""Application configuration using Pydantic Settings."""

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    Attributes:
        app_name: Name of the application
        version: Application version
        environment: Current environment (development, staging, production)
        debug: Enable debug mode
        log_level: Logging level
        api_v1_prefix: API v1 route prefix
        database_url: Database connection URL
        db_echo: Echo SQL queries (for debugging)
        db_pool_size: Database connection pool size
        db_max_overflow: Max overflow connections
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "{{display_name}}"
    version: str = "{{version}}"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = True

    # Logging
    log_level: str = "INFO"

    # API
    api_v1_prefix: str = "/api/v1"

    # Server
    host: str = "0.0.0.0"
    port: int = {{port}}

    # Database
    database_url: str = "sqlite:///./{{package_name}}.db"
    db_echo: bool = False  # Set to True to see SQL queries
    db_pool_size: int = 5
    db_max_overflow: int = 10


@lru_cache
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Application settings
    """
    return Settings()
