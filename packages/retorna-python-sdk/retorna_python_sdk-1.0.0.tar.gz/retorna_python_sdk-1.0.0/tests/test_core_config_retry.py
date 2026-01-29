import pytest

from src.retorna_sdk.core import RetryConfig


class TestRetryConfig:
    """Test cases for RetryConfig dataclass."""

    def test_default_creation(self):
        """Test RetryConfig creation with default parameters."""
        config = RetryConfig()
        assert config.retries == 3
        assert config.backoff_ms == 200

    def test_creation_with_parameters(self):
        """Test RetryConfig creation with custom parameters."""
        config = RetryConfig(retries=5, backoff_ms=500)
        assert config.retries == 5
        assert config.backoff_ms == 500

    def test_immutability(self, sample_retry_config):
        """Test that RetryConfig is immutable (frozen)."""
        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_retry_config.retries = 10

        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_retry_config.backoff_ms = 1000

    def test_equality(self):
        """Test RetryConfig equality comparison."""
        config1 = RetryConfig(3, 200)
        config2 = RetryConfig(3, 200)
        config3 = RetryConfig(5, 200)

        assert config1 == config2
        assert config1 != config3

    @pytest.mark.parametrize(
        "retries,backoff", [(1, 100), (5, 500), (10, 1000), (0, 0)]
    )
    def test_various_configurations(self, retries, backoff):
        """Test creation with various retry configurations."""
        config = RetryConfig(retries=retries, backoff_ms=backoff)
        assert config.retries == retries
        assert config.backoff_ms == backoff
