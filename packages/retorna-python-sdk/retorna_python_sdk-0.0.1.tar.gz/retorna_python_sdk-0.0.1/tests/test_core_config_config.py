import pytest

from src.retorna_sdk.core import RetornaEnvironment, RetryConfig, SDKConfig


class TestSDKConfig:
    """Test cases for SDKConfig dataclass."""

    def test_creation_with_minimal_params(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test SDKConfig creation with minimal required parameters."""
        config = SDKConfig(
            environment=RetornaEnvironment.PRODUCTION,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
        )

        assert config.environment == RetornaEnvironment.PRODUCTION
        assert config.env_config == sample_env_config
        assert config.credentials == sample_credentials
        assert config.logging_config == sample_logging_config
        assert isinstance(config.retry_config, RetryConfig)
        assert config.base_url_override is None
        assert config.scope_override is None

    def test_creation_with_all_params(self, complete_sdk_config):
        """Test SDKConfig creation with all parameters."""
        assert complete_sdk_config.environment == RetornaEnvironment.STAGING
        assert complete_sdk_config.env_config is not None
        assert complete_sdk_config.credentials is not None
        assert complete_sdk_config.logging_config is not None
        assert complete_sdk_config.retry_config is not None

    def test_creation_with_overrides(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test SDKConfig creation with URL and scope overrides."""
        config = SDKConfig(
            environment="production",
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
            base_url_override="https://custom.api.com",
            scope_override="custom/scope",
        )

        assert config.base_url_override == "https://custom.api.com"
        assert config.scope_override == "custom/scope"

    def test_immutability(self, complete_sdk_config):
        """Test that SDKConfig is immutable (frozen)."""
        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            complete_sdk_config.environment = RetornaEnvironment.DEVELOP

        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            complete_sdk_config.base_url_override = "new_url"

    def test_base_url_property_without_override(self, complete_sdk_config):
        """Test base_url property returns env_config.base_url when no override."""
        expected_url = complete_sdk_config.env_config.base_url
        assert complete_sdk_config.base_url == expected_url

    def test_base_url_property_with_override(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test base_url property returns override when provided."""
        override_url = "https://override.api.com"
        config = SDKConfig(
            environment=RetornaEnvironment.PRODUCTION,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
            base_url_override=override_url,
        )

        assert config.base_url == override_url
        assert config.base_url != sample_env_config.base_url

    def test_scope_property_without_override(self, complete_sdk_config):
        """Test scope property returns env_config.scope when no override."""
        expected_scope = complete_sdk_config.env_config.scope
        assert complete_sdk_config.scope == expected_scope

    def test_scope_property_with_override(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test scope property returns override when provided."""
        override_scope = "custom/override_scope"
        config = SDKConfig(
            environment=RetornaEnvironment.STAGING,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
            scope_override=override_scope,
        )

        assert config.scope == override_scope
        assert config.scope != sample_env_config.scope

    def test_properties_with_both_overrides(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test properties when both URL and scope overrides are provided."""
        override_url = "https://override.api.com"
        override_scope = "custom/override_scope"

        config = SDKConfig(
            environment=RetornaEnvironment.DEVELOP,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
            base_url_override=override_url,
            scope_override=override_scope,
        )

        assert config.base_url == override_url
        assert config.scope == override_scope

    def test_default_retry_config(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test that the default retry config is properly set."""
        config = SDKConfig(
            environment=RetornaEnvironment.PRODUCTION,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
        )

        assert config.retry_config.retries == 3
        assert config.retry_config.backoff_ms == 200

    def test_custom_retry_config(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test SDKConfig with custom retry configuration."""
        custom_retry = RetryConfig(retries=10, backoff_ms=1000)
        config = SDKConfig(
            environment=RetornaEnvironment.STAGING,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
            retry_config=custom_retry,
        )

        assert config.retry_config.retries == 10
        assert config.retry_config.backoff_ms == 1000

    def test_environment_as_string(
        self, sample_credentials, sample_env_config, sample_logging_config
    ):
        """Test SDKConfig creation with environment as string."""
        config = SDKConfig(
            environment="staging",
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
        )

        assert config.environment == "staging"

    def test_equality(
        self,
        complete_sdk_config,
        sample_credentials,
        sample_env_config,
        sample_logging_config,
    ):
        """Test SDKConfig equality comparison."""
        config1 = SDKConfig(
            environment=RetornaEnvironment.PRODUCTION,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
        )
        config2 = SDKConfig(
            environment=RetornaEnvironment.PRODUCTION,
            env_config=sample_env_config,
            credentials=sample_credentials,
            logging_config=sample_logging_config,
        )

        assert config1 == config2
        assert config1 != complete_sdk_config
