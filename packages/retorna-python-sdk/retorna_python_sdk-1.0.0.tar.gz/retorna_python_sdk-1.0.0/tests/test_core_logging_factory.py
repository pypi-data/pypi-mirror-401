import logging
from unittest.mock import Mock, patch

import pytest

from src.retorna_sdk.core import LoggingConfig, LoggingLevel, create_sdk_logger


class TestCreateSdkLogger:
    """Test cases for the create_sdk_logger function."""

    def test_logger_name(self):
        """Test that the logger has the correct name."""
        config = LoggingConfig()
        logger = create_sdk_logger(config)
        assert logger.name == "retorna_sdk"

    def test_logger_propagation_disabled(self):
        """Test that logger propagation is disabled."""
        config = LoggingConfig()
        logger = create_sdk_logger(config)
        assert logger.propagate is False

    def test_disabled_logger_when_not_enabled(self):
        """Test that logger is disabled when enabled=False."""
        config = LoggingConfig(enabled=False)
        logger = create_sdk_logger(config)
        assert logger.disabled is True

    def test_disabled_logger_when_level_none(self):
        """Test that the logger is disabled when the level is NONE."""
        config = LoggingConfig(level=LoggingLevel.NONE, enabled=True)
        logger = create_sdk_logger(config)
        assert logger.disabled is True

    def test_enabled_logger_configuration(self):
        """Test that logger is properly enabled with a valid configuration."""
        config = LoggingConfig(level=LoggingLevel.INFO, enabled=True)
        logger = create_sdk_logger(config)
        assert logger.disabled is False

    @pytest.mark.parametrize(
        "sdk_level,expected_level",
        [
            (LoggingLevel.ERROR, logging.ERROR),
            (LoggingLevel.WARN, logging.WARNING),
            (LoggingLevel.INFO, logging.INFO),
            (LoggingLevel.DEBUG, logging.DEBUG),
        ],
    )
    def test_logging_level_mapping(self, sdk_level, expected_level):
        """Test that SDK logging levels map correctly to Python logging levels."""
        config = LoggingConfig(level=sdk_level, enabled=True)
        logger = create_sdk_logger(config)
        assert logger.level == expected_level

    def test_handler_creation(self):
        """Test that a handler is created when none exists."""
        config = LoggingConfig(level=LoggingLevel.INFO, enabled=True)
        logger = create_sdk_logger(config)

        assert len(logger.handlers) == 1
        handler = logger.handlers[0]
        assert isinstance(handler, logging.StreamHandler)

    def test_handler_not_duplicated(self):
        """Test that handlers are not duplicated on multiple calls."""
        config = LoggingConfig(level=LoggingLevel.INFO, enabled=True)

        logger1 = create_sdk_logger(config)
        initial_handler_count = len(logger1.handlers)

        logger2 = create_sdk_logger(config)

        assert logger1 is logger2
        assert len(logger2.handlers) == initial_handler_count

    def test_formatter_configuration(self):
        """Test that the handler has the correct formatter."""
        config = LoggingConfig(level=LoggingLevel.INFO, enabled=True)
        logger = create_sdk_logger(config)

        handler = logger.handlers[0]
        formatter = handler.formatter
        assert formatter is not None
        assert "[RetornaSDK]" in formatter._fmt

    def test_disabled_logger_returns_early(self):
        """Test that disabled loggers return early without full configuration."""
        config = LoggingConfig(enabled=False)
        logger = create_sdk_logger(config)

        assert logger.disabled is True
        assert len(logger.handlers) == 0

    @patch("logging.StreamHandler")
    @patch("logging.Formatter")
    def test_handler_setup_calls(self, mock_formatter, mock_handler):
        """Test that handler setup makes correct calls."""
        mock_handler_instance = Mock()
        mock_formatter_instance = Mock()
        mock_handler.return_value = mock_handler_instance
        mock_formatter.return_value = mock_formatter_instance

        config = LoggingConfig(level=LoggingLevel.INFO, enabled=True)

        logger = logging.getLogger("retorna_sdk")
        logger.handlers.clear()

        create_sdk_logger(config)

        mock_formatter.assert_called_once_with(
            "[RetornaSDK] %(levelname)s - %(message)s"
        )

        mock_handler_instance.setFormatter.assert_called_once_with(
            mock_formatter_instance
        )

    def test_multiple_configs_same_logger(self):
        """Test behavior when creating loggers with different configs for the same name."""
        config1 = LoggingConfig(level=LoggingLevel.ERROR, enabled=True)
        logger1 = create_sdk_logger(config1)

        config2 = LoggingConfig(level=LoggingLevel.DEBUG, enabled=True)
        logger2 = create_sdk_logger(config2)

        assert logger1 is logger2
        assert logger2.level == logging.DEBUG

    def test_re_enable_disabled_logger(self):
        """Test that a previously disabled logger can be re-enabled."""

        config_disabled = LoggingConfig(enabled=False)
        logger = create_sdk_logger(config_disabled)
        assert logger.disabled is True

        config_enabled = LoggingConfig(level=LoggingLevel.INFO, enabled=True)
        logger = create_sdk_logger(config_enabled)
        assert logger.disabled is False
        assert logger.level == logging.INFO
