"""Example script demonstrating lib_boring_logger usage."""

from lib_boring_logger import LoggerFactory, logger

# The simplest way - just import and use!
logger.info("Starting BoringPy example script")
logger.success("Dependencies loaded successfully")

# Different log levels
logger.debug("This won't show (default level is INFO)")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error message")
logger.critical("This is critical!")

# Success messages (great for CLI feedback)
logger.success("API workspace created: src/apps/my_api")
logger.success("Database connection established")
logger.success("Tests passed!")

# Error handling with logging
try:
    result = 10 / 2
    logger.success(f"Calculation result: {result}")
except ZeroDivisionError as e:
    logger.error(f"Operation failed: {e}")

# Using the factory (if you need to change log level)
debug_log = LoggerFactory.get_logger(level="DEBUG")
debug_log.debug("Now debug messages will show!")
debug_log.info("Back to regular logging")

logger.info("Example script completed!")
