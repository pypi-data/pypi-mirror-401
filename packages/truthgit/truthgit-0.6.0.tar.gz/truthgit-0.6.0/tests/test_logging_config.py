"""
Tests for TruthGit logging configuration.
"""

import logging
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Reset logging state before import
logging.getLogger("truthgit").handlers = []

from truthgit.logging_config import (
    LogContext,
    configure_logging,
    disable_logging,
    enable_logging,
    get_api_logger,
    get_logger,
    get_proof_logger,
    get_repository_logger,
    get_validator_logger,
    set_log_level,
)


@pytest.fixture(autouse=True)
def reset_logging():
    """Reset logging configuration before each test."""
    import truthgit.logging_config as lc

    lc._configured = False
    logger = logging.getLogger("truthgit")
    logger.handlers = []
    logger.setLevel(logging.NOTSET)
    yield


class TestConfigureLogging:
    """Tests for configure_logging function."""

    def test_creates_console_handler(self):
        """configure_logging creates a console handler."""
        configure_logging()
        logger = logging.getLogger("truthgit")
        assert len(logger.handlers) >= 1
        assert any(
            isinstance(h, logging.StreamHandler) for h in logger.handlers
        )

    def test_default_level_is_info(self):
        """Default log level is INFO."""
        configure_logging()
        logger = logging.getLogger("truthgit")
        assert logger.level == logging.INFO

    def test_custom_level(self):
        """Custom level is respected."""
        configure_logging(level="DEBUG")
        logger = logging.getLogger("truthgit")
        assert logger.level == logging.DEBUG

    def test_env_level(self):
        """Environment variable level is used."""
        with patch.dict(os.environ, {"TRUTHGIT_LOG_LEVEL": "WARNING"}):
            import truthgit.logging_config as lc

            lc._configured = False
            configure_logging()
            logger = logging.getLogger("truthgit")
            assert logger.level == logging.WARNING

    def test_file_handler(self):
        """File handler is created when log_file specified."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            configure_logging(log_file=str(log_file))

            logger = logging.getLogger("truthgit")
            file_handlers = [
                h for h in logger.handlers if isinstance(h, logging.FileHandler)
            ]
            assert len(file_handlers) >= 1

    def test_only_configures_once(self):
        """configure_logging only runs once."""
        configure_logging()
        handler_count = len(logging.getLogger("truthgit").handlers)

        configure_logging()  # Second call
        assert len(logging.getLogger("truthgit").handlers) == handler_count


class TestGetLogger:
    """Tests for get_logger function."""

    def test_returns_logger(self):
        """get_logger returns a Logger instance."""
        logger = get_logger(__name__)
        assert isinstance(logger, logging.Logger)

    def test_prefixes_name(self):
        """get_logger prefixes name with package name."""
        logger = get_logger("mymodule")
        assert logger.name == "truthgit.mymodule"

    def test_preserves_full_name(self):
        """get_logger preserves names starting with package name."""
        logger = get_logger("truthgit.validators")
        assert logger.name == "truthgit.validators"

    def test_configures_logging(self):
        """get_logger triggers logging configuration."""
        get_logger("test")
        logger = logging.getLogger("truthgit")
        assert len(logger.handlers) >= 1


class TestSetLogLevel:
    """Tests for set_log_level function."""

    def test_changes_level(self):
        """set_log_level changes the log level."""
        configure_logging(level="INFO")
        set_log_level("DEBUG")

        logger = logging.getLogger("truthgit")
        assert logger.level == logging.DEBUG

    def test_changes_handler_levels(self):
        """set_log_level changes handler levels too."""
        configure_logging(level="INFO")
        set_log_level("ERROR")

        logger = logging.getLogger("truthgit")
        for handler in logger.handlers:
            assert handler.level == logging.ERROR


class TestDisableEnableLogging:
    """Tests for disable_logging and enable_logging."""

    def test_disable_logging(self):
        """disable_logging disables the logger."""
        configure_logging()
        disable_logging()

        logger = logging.getLogger("truthgit")
        assert logger.disabled is True

    def test_enable_logging(self):
        """enable_logging re-enables the logger."""
        configure_logging()
        disable_logging()
        enable_logging()

        logger = logging.getLogger("truthgit")
        assert logger.disabled is False


class TestLogContext:
    """Tests for LogContext context manager."""

    def test_changes_level_in_context(self):
        """LogContext changes level within context."""
        configure_logging(level="INFO")

        with LogContext("DEBUG"):
            logger = logging.getLogger("truthgit")
            assert logger.level == logging.DEBUG

    def test_restores_level_after_context(self):
        """LogContext restores original level after exit."""
        configure_logging(level="INFO")

        with LogContext("DEBUG"):
            pass

        logger = logging.getLogger("truthgit")
        assert logger.level == logging.INFO

    def test_restores_on_exception(self):
        """LogContext restores level even if exception occurs."""
        configure_logging(level="INFO")

        try:
            with LogContext("DEBUG"):
                raise ValueError("Test error")
        except ValueError:
            pass

        logger = logging.getLogger("truthgit")
        assert logger.level == logging.INFO


class TestPreConfiguredLoggers:
    """Tests for pre-configured logger functions."""

    def test_get_validator_logger(self):
        """get_validator_logger returns validators logger."""
        logger = get_validator_logger()
        assert "validators" in logger.name

    def test_get_repository_logger(self):
        """get_repository_logger returns repository logger."""
        logger = get_repository_logger()
        assert "repository" in logger.name

    def test_get_proof_logger(self):
        """get_proof_logger returns proof logger."""
        logger = get_proof_logger()
        assert "proof" in logger.name

    def test_get_api_logger(self):
        """get_api_logger returns api logger."""
        logger = get_api_logger()
        assert "api" in logger.name


class TestLogOutput:
    """Tests for actual log output."""

    def test_logs_to_file(self):
        """Logger writes to file when configured."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            configure_logging(level="INFO", log_file=str(log_file))

            logger = get_logger("test")
            logger.info("Test message")

            # Flush handlers
            for handler in logging.getLogger("truthgit").handlers:
                handler.flush()

            content = log_file.read_text()
            assert "Test message" in content

    def test_respects_log_level(self):
        """Logger respects log level filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_file = Path(tmpdir) / "test.log"
            configure_logging(level="WARNING", log_file=str(log_file))

            logger = get_logger("test")
            logger.debug("Debug message")
            logger.info("Info message")
            logger.warning("Warning message")

            # Flush handlers
            for handler in logging.getLogger("truthgit").handlers:
                handler.flush()

            content = log_file.read_text()
            assert "Debug message" not in content
            assert "Info message" not in content
            assert "Warning message" in content
