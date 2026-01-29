"""Loguru logger integration with FastAPI."""

import logging
import sys
from contextvars import ContextVar
from typing import Any

from loguru import logger

from app.core.config import get_settings

# Context variable for request tracing
_trace_id_context: ContextVar[str | None] = ContextVar("trace_id", default=None)

settings = get_settings()


class InterceptHandler(logging.Handler):
    """
    Intercept standard logging and redirect to Loguru.

    This captures logs from FastAPI, Uvicorn, and other libraries
    that use Python's standard logging module.
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record by redirecting it to Loguru.

        Args:
            record: The log record from standard logging
        """
        # Get corresponding Loguru level
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller to get correct stack depth
        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def _add_trace_id_to_record(record: dict) -> None:
    """
    Add trace ID to log record if not present.

    This ensures all logs have a trace_id, even if they come from
    intercepted standard logging (Uvicorn, FastAPI, etc).

    Args:
        record: Loguru log record
    """
    if "trace_id" not in record["extra"]:
        trace_id = _trace_id_context.get() or "no-trace"
        record["extra"]["trace_id"] = trace_id


def setup_logging() -> None:
    """
    Configure logging for the application.

    - Removes default Loguru handler
    - Adds custom handler with proper formatting
    - Intercepts standard library logging
    - Configures Uvicorn and FastAPI loggers
    """
    # Remove default handler
    logger.remove()

    # Add custom handler with formatting and patcher
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<yellow>{extra[trace_id]}</yellow> - "
            "<level>{message}</level>"
        ),
        colorize=True,
        backtrace=settings.debug,
        diagnose=settings.debug,
        # Add patcher to ensure trace_id exists
        filter=_add_trace_id_to_record,
    )

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO, force=True)

    # Configure framework loggers
    for logger_name in [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "starlette",
    ]:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True


def configure_logger(**kwargs: Any) -> Any:
    """
    Bind extra context to logger (like trace_id).

    Args:
        **kwargs: Extra context to bind

    Returns:
        Logger with bound context
    """
    # Get trace_id from context if available
    trace_id = _trace_id_context.get() or "no-trace"
    return logger.bind(trace_id=trace_id, **kwargs)


def set_trace_id(trace_id: str) -> None:
    """
    Set trace ID for current request context.

    Args:
        trace_id: Trace ID to set
    """
    _trace_id_context.set(trace_id)


def get_trace_id() -> str | None:
    """
    Get current trace ID from context.

    Returns:
        Current trace ID or None
    """
    return _trace_id_context.get()


# Export configured logger
log = configure_logger()