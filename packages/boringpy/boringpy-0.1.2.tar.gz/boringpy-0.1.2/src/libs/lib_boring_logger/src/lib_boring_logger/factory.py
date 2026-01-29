"""Terminal-focused logger for BoringPy using Loguru."""

import sys
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger

# Configure logger once when module is imported
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
    colorize=True,
)


class LoggerFactory:
    """
    Factory for getting the configured Loguru logger.

    The logger is preconfigured for terminal output with colors and clean formatting.
    You can use it directly or get it through the factory methods.
    """

    @classmethod
    def get_logger(cls, level: str = "INFO") -> "Logger":
        """
        Get the configured logger.

        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
                   Note: This changes the global log level for all subsequent calls

        Returns:
            The configured Loguru logger instance

        Examples:
            >>> from lib_boring_logger import LoggerFactory
            >>>
            >>> log = LoggerFactory.get_logger()
            >>> log.info("Starting application")
            >>> log.success("Task completed!")
            >>> log.error("Something went wrong")
            >>>
            >>> # Enable debug mode
            >>> log = LoggerFactory.get_logger(level="DEBUG")
            >>> log.debug("Detailed debugging info")
        """
        # Update log level if different from default
        if level != "INFO":
            logger.remove()
            logger.add(
                sys.stderr,
                format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
                level=level,
                colorize=True,
            )
        return logger

    @classmethod
    def create_logger(cls, name: str | None = None, level: str = "INFO") -> "Logger":
        """
        Get the logger (alias for get_logger for compatibility).

        Args:
            name: Ignored (kept for compatibility)
            level: Logging level

        Returns:
            The configured Loguru logger instance

        Examples:
            >>> log = LoggerFactory.create_logger()
            >>> log.info("Processing data")
        """
        return cls.get_logger(level=level)

    @classmethod
    def reset(cls) -> None:
        """
        Reset logger to default configuration (useful for testing).

        This removes all handlers and reconfigures with default settings.
        """
        logger.remove()
        logger.add(
            sys.stderr,
            format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
            level="INFO",
            colorize=True,
        )


# Export logger directly for simple usage
__all__ = ["LoggerFactory", "logger"]
