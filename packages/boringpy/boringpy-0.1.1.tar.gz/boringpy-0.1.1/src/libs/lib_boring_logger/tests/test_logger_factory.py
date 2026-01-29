"""Tests for LoggerFactory."""

from lib_boring_logger import LoggerFactory, logger


def test_get_logger_simple() -> None:
    """Test getting the logger."""
    LoggerFactory.reset()
    log = LoggerFactory.get_logger()
    assert log is not None


def test_get_logger_with_custom_level() -> None:
    """Test getting a logger with custom log level."""
    LoggerFactory.reset()
    log = LoggerFactory.get_logger(level="DEBUG")
    assert log is not None


def test_create_logger_alias() -> None:
    """Test create_logger as an alias for get_logger."""
    LoggerFactory.reset()
    log = LoggerFactory.create_logger()
    assert log is not None


def test_logger_can_log_messages() -> None:
    """Test that logger can actually log messages."""
    LoggerFactory.reset()
    log = LoggerFactory.get_logger()

    # These should not raise exceptions
    log.debug("Debug message")
    log.info("Info message")
    log.success("Success message")
    log.warning("Warning message")
    log.error("Error message")


def test_logger_direct_import() -> None:
    """Test that logger can be imported directly."""
    # Should not raise exceptions
    logger.info("Direct import message")
    logger.success("Direct success message")


def test_reset_clears_logger() -> None:
    """Test that reset clears logger configuration."""
    LoggerFactory.reset()
    log = LoggerFactory.get_logger()
    assert log is not None

    LoggerFactory.reset()
    # Logger should still work after reset
    log.info("After reset")
