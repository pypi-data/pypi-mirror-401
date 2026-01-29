import pytest

from src.retorna_sdk.core import LoggingConfig, LoggingLevel


class TestLoggingConfig:
    """Test cases for LoggingConfig dataclass."""

    def test_default_creation(self):
        """Test LoggingConfig creation with default parameters."""
        config = LoggingConfig()
        assert config.level == LoggingLevel.ERROR
        assert config.enabled is True

    def test_creation_with_parameters(self):
        """Test LoggingConfig creation with custom parameters."""
        config = LoggingConfig(level=LoggingLevel.DEBUG, enabled=False)
        assert config.level == LoggingLevel.DEBUG
        assert config.enabled is False

    def test_immutability(self, sample_logging_config):
        """Test that LoggingConfig is immutable (frozen)."""
        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_logging_config.level = LoggingLevel.DEBUG

        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_logging_config.enabled = False

    def test_equality(self):
        """Test LoggingConfig equality comparison."""
        config1 = LoggingConfig(LoggingLevel.INFO, True)
        config2 = LoggingConfig(LoggingLevel.INFO, True)
        config3 = LoggingConfig(LoggingLevel.DEBUG, True)

        assert config1 == config2
        assert config1 != config3

    @pytest.mark.parametrize(
        "level",
        [
            LoggingLevel.NONE,
            LoggingLevel.ERROR,
            LoggingLevel.WARN,
            LoggingLevel.INFO,
            LoggingLevel.DEBUG,
        ],
    )
    def test_all_logging_levels(self, level):
        """Test creation with all valid logging levels."""
        config = LoggingConfig(level=level)
        assert config.level == level

    @pytest.mark.parametrize("enabled", [True, False])
    def test_enabled_flag(self, enabled):
        """Test creation with different enabled values."""
        config = LoggingConfig(enabled=enabled)
        assert config.enabled == enabled
