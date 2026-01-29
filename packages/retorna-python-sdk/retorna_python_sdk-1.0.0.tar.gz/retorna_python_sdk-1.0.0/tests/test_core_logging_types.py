from src.retorna_sdk.core import LoggingLevel


class TestLoggingLevel:
    """Test cases for LoggingLevel enum."""

    def test_enum_values(self):
        """Test that enum values are correct."""
        assert LoggingLevel.NONE == "none"
        assert LoggingLevel.ERROR == "error"
        assert LoggingLevel.WARN == "warn"
        assert LoggingLevel.INFO == "info"
        assert LoggingLevel.DEBUG == "debug"

    def test_enum_membership(self):
        """Test enum membership operations."""
        assert "none" in LoggingLevel
        assert "error" in LoggingLevel
        assert "warn" in LoggingLevel
        assert "info" in LoggingLevel
        assert "debug" in LoggingLevel
        assert "invalid" not in LoggingLevel

    def test_enum_iteration(self, all_logging_levels):
        """Test that all logging levels are accessible via iteration."""
        enum_values = list(LoggingLevel)
        assert len(enum_values) == 5
        for level in all_logging_levels:
            assert level in enum_values
