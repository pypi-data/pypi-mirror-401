import logging
from unittest.mock import Mock, patch

from src.retorna_sdk.client import RetornaClient
from src.retorna_sdk.core import LoggingConfig, LoggingLevel


class TestRetornaClient:
    """Test cases for RetornaClient class."""

    def test_initialization(self, complete_sdk_config):
        """Test RetornaClient initialization with a valid configuration."""
        client = RetornaClient(complete_sdk_config)

        assert client.config == complete_sdk_config
        assert isinstance(client.logger, logging.Logger)
        assert client.logger.name == "retorna_sdk"

    def test_config_attribute(self, complete_sdk_config):
        """Test that the config attribute is properly set."""
        client = RetornaClient(complete_sdk_config)

        assert client.config is complete_sdk_config

        assert client.config.environment is not None
        assert client.config.credentials is not None
        assert client.config.logging_config is not None

    def test_logger_creation(self, complete_sdk_config):
        """Test that the logger is created with the correct configuration."""
        client = RetornaClient(complete_sdk_config)

        assert client.logger is not None
        assert client.logger.name == "retorna_sdk"
        assert client.logger.propagate is False

    @patch("src.retorna_sdk.client.client.create_sdk_logger")
    def test_logger_creation_called_with_config(
        self, mock_create_logger, complete_sdk_config
    ):
        """Test that create_sdk_logger is called with the correct logger config."""
        mock_logger = Mock(spec=logging.Logger)
        mock_create_logger.return_value = mock_logger

        client = RetornaClient(complete_sdk_config)

        mock_create_logger.assert_called_once_with(
            config=complete_sdk_config.logging_config
        )
        assert client.logger == mock_logger

    def test_different_logging_configs(self, sample_credentials, sample_env_config):
        """Test client creation with different logger configurations."""
        debug_config = type(
            "SDKConfig",
            (),
            {
                "environment": "production",
                "env_config": sample_env_config,
                "credentials": sample_credentials,
                "logging_config": LoggingConfig(level=LoggingLevel.DEBUG, enabled=True),
                "retry_config": type(
                    "RetryConfig", (), {"retries": 3, "backoff_ms": 200}
                )(),
                "base_url_override": None,
                "scope_override": None,
                "base_url": sample_env_config.base_url,
                "scope": sample_env_config.scope,
            },
        )()

        client_debug = RetornaClient(debug_config)
        assert client_debug.logger.level == logging.DEBUG

        disabled_config = type(
            "SDKConfig",
            (),
            {
                "environment": "production",
                "env_config": sample_env_config,
                "credentials": sample_credentials,
                "logging_config": LoggingConfig(enabled=False),
                "retry_config": type(
                    "RetryConfig", (), {"retries": 3, "backoff_ms": 200}
                )(),
                "base_url_override": None,
                "scope_override": None,
                "base_url": sample_env_config.base_url,
                "scope": sample_env_config.scope,
            },
        )()

        client_disabled = RetornaClient(disabled_config)
        assert client_disabled.logger.disabled is True

    def test_multiple_clients_same_config(self, complete_sdk_config):
        """Test creating multiple clients with the same configuration."""
        client1 = RetornaClient(complete_sdk_config)
        client2 = RetornaClient(complete_sdk_config)

        assert client1.config is client2.config

        assert client1.logger is client2.logger

    def test_multiple_clients_different_configs(
        self, complete_sdk_config, sample_credentials, sample_env_config
    ):
        """Test creating multiple clients with different configurations."""
        different_config = type(
            "SDKConfig",
            (),
            {
                "environment": "staging",
                "env_config": sample_env_config,
                "credentials": sample_credentials,
                "logging_config": LoggingConfig(level=LoggingLevel.ERROR),
                "retry_config": type(
                    "RetryConfig", (), {"retries": 5, "backoff_ms": 100}
                )(),
                "base_url_override": None,
                "scope_override": None,
                "base_url": sample_env_config.base_url,
                "scope": sample_env_config.scope,
            },
        )()

        client1 = RetornaClient(complete_sdk_config)
        client2 = RetornaClient(different_config)

        assert client1.config is not client2.config
        assert client1.config.environment == client2.config.environment

        assert client1.logger is client2.logger

    def test_client_attributes_immutable_reference(self, complete_sdk_config):
        """Test that a client maintains reference to the original config."""
        original_environment = complete_sdk_config.environment

        client = RetornaClient(complete_sdk_config)

        assert client.config.environment == original_environment

        assert client.config is complete_sdk_config

    def test_logger_functionality(self, complete_sdk_config):
        """Test that the logger actually works for logging."""
        client = RetornaClient(complete_sdk_config)

        client.logger.info("Test message")
        client.logger.error("Test error")
        client.logger.debug("Test debug")

    def test_client_initialization_with_minimal_config(
        self, sample_credentials, sample_env_config
    ):
        """Test client initialization with minimal configuration."""
        minimal_config = type(
            "SDKConfig",
            (),
            {
                "environment": "production",
                "env_config": sample_env_config,
                "credentials": sample_credentials,
                "logging_config": LoggingConfig(),
                "retry_config": type(
                    "RetryConfig", (), {"retries": 3, "backoff_ms": 200}
                )(),
                "base_url_override": None,
                "scope_override": None,
                "base_url": sample_env_config.base_url,
                "scope": sample_env_config.scope,
            },
        )()

        client = RetornaClient(minimal_config)

        assert client.config == minimal_config
        assert client.logger is not None
        assert client.logger.level == logging.ERROR

    def test_type_annotations(self, complete_sdk_config):
        """Test that the client works with proper type annotations."""
        client: RetornaClient = RetornaClient(complete_sdk_config)
        config_ref = client.config
        logger_ref = client.logger

        assert isinstance(client, RetornaClient)
        assert config_ref is not None
        assert isinstance(logger_ref, logging.Logger)
