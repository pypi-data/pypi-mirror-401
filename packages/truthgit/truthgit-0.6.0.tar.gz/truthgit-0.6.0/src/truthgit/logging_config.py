"""
TruthGit Logging Configuration.

Provides centralized logging setup for the TruthGit package.
Supports console output with configurable levels and optional file logging.

Usage:
    from truthgit.logging_config import get_logger

    logger = get_logger(__name__)
    logger.info("Verifying claim...")
    logger.debug("Details: %s", details)

Environment Variables:
    TRUTHGIT_LOG_LEVEL: Set log level (DEBUG, INFO, WARNING, ERROR)
    TRUTHGIT_LOG_FILE: Path to log file (optional)
"""

import logging
import os
import sys
from pathlib import Path

# Default configuration
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DEFAULT_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Package logger name
PACKAGE_NAME = "truthgit"

# Configured flag to prevent multiple configurations
_configured = False


def configure_logging(
    level: str | None = None,
    log_file: str | Path | None = None,
    format_string: str | None = None,
    date_format: str | None = None,
) -> None:
    """
    Configure logging for the TruthGit package.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for logging
        format_string: Custom format string for log messages
        date_format: Custom date format string
    """
    global _configured

    if _configured:
        return

    # Get configuration from environment or use defaults
    level = level or os.getenv("TRUTHGIT_LOG_LEVEL", DEFAULT_LOG_LEVEL)
    log_file = log_file or os.getenv("TRUTHGIT_LOG_FILE")
    format_string = format_string or DEFAULT_LOG_FORMAT
    date_format = date_format or DEFAULT_DATE_FORMAT

    # Get the numeric level
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    # Configure the package logger
    package_logger = logging.getLogger(PACKAGE_NAME)
    package_logger.setLevel(numeric_level)

    # Avoid duplicate handlers
    if package_logger.handlers:
        _configured = True
        return

    # Create formatter
    formatter = logging.Formatter(format_string, date_format)

    # Console handler (always)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    package_logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_path = Path(log_file)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        package_logger.addHandler(file_handler)

    # Don't propagate to root logger
    package_logger.propagate = False

    _configured = True


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Args:
        name: Module name (typically __name__)

    Returns:
        Logger instance configured for TruthGit

    Example:
        logger = get_logger(__name__)
        logger.info("Processing claim")
    """
    # Ensure logging is configured
    configure_logging()

    # If name starts with package name, use as-is
    if name.startswith(PACKAGE_NAME):
        return logging.getLogger(name)

    # Otherwise, prefix with package name
    return logging.getLogger(f"{PACKAGE_NAME}.{name}")


def set_log_level(level: str) -> None:
    """
    Change the log level at runtime.

    Args:
        level: New log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    package_logger = logging.getLogger(PACKAGE_NAME)
    package_logger.setLevel(numeric_level)
    for handler in package_logger.handlers:
        handler.setLevel(numeric_level)


def disable_logging() -> None:
    """Disable all TruthGit logging."""
    logging.getLogger(PACKAGE_NAME).disabled = True


def enable_logging() -> None:
    """Re-enable TruthGit logging."""
    logging.getLogger(PACKAGE_NAME).disabled = False


class LogContext:
    """
    Context manager for temporary log level changes.

    Example:
        with LogContext("DEBUG"):
            # Debug logging enabled here
            validate_claim(...)
        # Original level restored
    """

    def __init__(self, level: str):
        self.level = level
        self.original_level = None

    def __enter__(self):
        package_logger = logging.getLogger(PACKAGE_NAME)
        self.original_level = package_logger.level
        set_log_level(self.level)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.original_level is not None:
            logging.getLogger(PACKAGE_NAME).setLevel(self.original_level)
            for handler in logging.getLogger(PACKAGE_NAME).handlers:
                handler.setLevel(self.original_level)
        return False


# Pre-configured loggers for main modules
def get_validator_logger() -> logging.Logger:
    """Get logger for validators module."""
    return get_logger("truthgit.validators")


def get_repository_logger() -> logging.Logger:
    """Get logger for repository module."""
    return get_logger("truthgit.repository")


def get_proof_logger() -> logging.Logger:
    """Get logger for proof module."""
    return get_logger("truthgit.proof")


def get_api_logger() -> logging.Logger:
    """Get logger for API module."""
    return get_logger("truthgit.api")
