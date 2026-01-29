"""Test suite for SDKConfigBuilder class."""

import pytest

from src.retorna_sdk.client import RetornaClient, SDKConfigBuilder
from src.retorna_sdk.core import (LoggingConfig, LoggingLevel,
                                  RetornaEnvironment, RetryConfig, SDKConfig)


class TestSDKConfigBuilder:
    """Test cases for SDKConfigBuilder class."""

    def test_initialization(self, sdk_config_builder):
        """Test SDKConfigBuilder initialization with default values."""
        assert sdk_config_builder._environment is None
        assert sdk_config_builder._client_id is None
        assert sdk_config_builder._client_secret is None
        assert sdk_config_builder._private_key is None
        assert isinstance(sdk_config_builder._logging_config, LoggingConfig)
        assert isinstance(sdk_config_builder._retry_config, RetryConfig)
        assert sdk_config_builder._base_url_override is None
        assert sdk_config_builder._scope_override is None

    def test_environment_with_enum(self, sdk_config_builder):
        """Test setting environment with RetornaEnvironment enum."""
        result = sdk_config_builder.environment(RetornaEnvironment.PRODUCTION)

        assert result is sdk_config_builder
        assert sdk_config_builder._environment == RetornaEnvironment.PRODUCTION

    @pytest.mark.parametrize("env_string", ["develop", "staging", "production"])
    def test_environment_with_string(self, sdk_config_builder, env_string):
        """Test setting environment with string values."""
        result = sdk_config_builder.environment(env_string)

        assert result is sdk_config_builder
        assert sdk_config_builder._environment == env_string

    def test_client_id(self, sdk_config_builder):
        """Test setting client ID."""
        test_id = "test_client_id"
        result = sdk_config_builder.client_id(test_id)

        assert result is sdk_config_builder
        assert sdk_config_builder._client_id == test_id

    def test_client_secret(self, sdk_config_builder):
        """Test setting client secret."""
        test_secret = "test_client_secret"
        result = sdk_config_builder.client_secret(test_secret)

        assert result is sdk_config_builder
        assert sdk_config_builder._client_secret == test_secret

    def test_private_key(self, sdk_config_builder, sample_private_key):
        """Test setting private key."""
        test_key = sample_private_key
        result = sdk_config_builder.private_key(test_key)

        assert result is sdk_config_builder
        assert sdk_config_builder._private_key == test_key

    def test_logging_level_with_enum(self, sdk_config_builder):
        """Test setting logging level with LoggingLevel enum."""
        result = sdk_config_builder.logging_level(LoggingLevel.DEBUG)

        assert result is sdk_config_builder
        assert sdk_config_builder._logging_config.level == LoggingLevel.DEBUG
        assert sdk_config_builder._logging_config.enabled is True

    @pytest.mark.parametrize("level_string", ["none", "error", "warn", "info", "debug"])
    def test_logging_level_with_string(self, sdk_config_builder, level_string):
        """Test setting logging level with string values."""
        result = sdk_config_builder.logging_level(level_string)

        assert result is sdk_config_builder
        assert sdk_config_builder._logging_config.level == LoggingLevel(level_string)

    def test_disable_logging(self, sdk_config_builder):
        """Test disabling logging."""
        result = sdk_config_builder.disable_logging()

        assert result is sdk_config_builder
        assert sdk_config_builder._logging_config.level == LoggingLevel.NONE
        assert sdk_config_builder._logging_config.enabled is False

    def test_base_url_override(self, sdk_config_builder):
        """Test setting base URL override."""
        test_url = "https://custom.api.com"
        result = sdk_config_builder.base_url_override(test_url)

        assert result is sdk_config_builder
        assert sdk_config_builder._base_url_override == test_url

    def test_base_scope_override(self, sdk_config_builder):
        """Test setting base scope override."""
        test_scope = "custom/scope"
        sdk_config_builder.base_scope_override(test_scope)

        assert sdk_config_builder._scope_override == test_scope

    def test_method_chaining(self, sdk_config_builder, sample_private_key):
        """Test that methods can be chained together."""
        result = (
            sdk_config_builder.environment(RetornaEnvironment.STAGING)
            .client_id("test_id")
            .client_secret("test_secret")
            .private_key(sample_private_key)
            .logging_level(LoggingLevel.INFO)
            .base_url_override("https://custom.api.com")
        )

        assert result is sdk_config_builder
        assert sdk_config_builder._environment == RetornaEnvironment.STAGING
        assert sdk_config_builder._client_id == "test_id"
        assert sdk_config_builder._client_secret == "test_secret"
        assert sdk_config_builder._private_key == sample_private_key
        assert sdk_config_builder._logging_config.level == LoggingLevel.INFO
        assert sdk_config_builder._base_url_override == "https://custom.api.com"


class TestSDKConfigBuilderValidation:
    """Test cases for SDKConfigBuilder validation."""

    def test_validate_success(self, configured_builder):
        """Test validation passes with all required fields."""
        configured_builder._validate()

    def test_validate_missing_environment(self, sdk_config_builder, sample_private_key):
        """Test validation fails when the environment is missing."""
        (
            sdk_config_builder.client_id("test_id")
            .client_secret("test_secret")
            .private_key(sample_private_key)
        )

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        assert "environment" in str(exc_info.value)
        assert "Missing required SDK config parameters" in str(exc_info.value)

    def test_validate_missing_client_id(self, sdk_config_builder, sample_private_key):
        """Test validation fails when client_id is missing."""
        (
            sdk_config_builder.environment(RetornaEnvironment.PRODUCTION)
            .client_secret("test_secret")
            .private_key(sample_private_key)
        )

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        assert "client_id" in str(exc_info.value)

    def test_validate_missing_client_secret(
        self, sdk_config_builder, sample_private_key
    ):
        """Test validation fails when client_secret is missing."""
        (
            sdk_config_builder.environment(RetornaEnvironment.PRODUCTION)
            .client_id("test_id")
            .private_key(sample_private_key)
        )

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        assert "client_secret" in str(exc_info.value)

    def test_validate_missing_private_key(self, sdk_config_builder):
        """Test validation fails when private_key is missing."""
        (
            sdk_config_builder.environment(RetornaEnvironment.PRODUCTION)
            .client_id("test_id")
            .client_secret("test_secret")
        )

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        assert "private_key" in str(exc_info.value)

    def test_validate_multiple_missing_fields(self, sdk_config_builder):
        """Test validation fails with multiple missing required fields."""
        sdk_config_builder.environment(RetornaEnvironment.PRODUCTION)

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        error_message = str(exc_info.value)
        assert "client_id" in error_message
        assert "client_secret" in error_message
        assert "private_key" in error_message

    def test_validate_all_missing_fields(self, sdk_config_builder):
        """Test validation fails when all required fields are missing."""
        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder._validate()

        error_message = str(exc_info.value)
        assert "environment" in error_message
        assert "client_id" in error_message
        assert "client_secret" in error_message
        assert "private_key" in error_message


class TestSDKConfigBuilderBuild:
    """Test cases for SDKConfigBuilder build functionality."""

    def test_build_success(self, configured_builder, sample_private_key):
        """Test a successful build with all required parameters."""
        config = configured_builder.build()

        assert isinstance(config, SDKConfig)
        assert config.environment == RetornaEnvironment.PRODUCTION
        assert config.credentials.client_id == "test_client_id"
        assert config.credentials.client_secret == "test_client_secret"
        assert config.credentials.private_key == sample_private_key

    def test_build_with_custom_logging(self, configured_builder):
        """Test build with custom logging configuration."""
        config = configured_builder.logging_level(LoggingLevel.DEBUG).build()

        assert config.logging_config.level == LoggingLevel.DEBUG
        assert config.logging_config.enabled is True

    def test_build_with_disabled_logging(self, configured_builder):
        """Test build with disabled logging."""
        config = configured_builder.disable_logging().build()

        assert config.logging_config.level == LoggingLevel.NONE
        assert config.logging_config.enabled is False

    def test_build_with_overrides(self, configured_builder):
        """Test build with URL and scope overrides."""
        custom_url = "https://custom.api.com"
        custom_scope = "custom/scope"

        config = (
            configured_builder.base_url_override(custom_url)
            .base_scope_override(custom_scope)
            .build()
        )

        assert config.base_url_override == custom_url
        assert config.base_url == custom_url

    def test_build_with_string_environment(
        self, sdk_config_builder, sample_private_key
    ):
        """Test build with an environment specified as string."""
        config = (
            sdk_config_builder.environment("staging")
            .client_id("test_id")
            .client_secret("test_secret")
            .private_key(sample_private_key)
            .build()
        )

        assert config.environment == "staging"

    def test_build_failure_missing_params(self, sdk_config_builder):
        """Test build fails when required parameters are missing."""
        with pytest.raises(ValueError):
            sdk_config_builder.build()

    def test_build_creates_credentials(self, configured_builder, sample_private_key):
        """Test that build creates a proper credentials object."""
        config = configured_builder.build()

        assert config.credentials.client_id == "test_client_id"
        assert config.credentials.client_secret == "test_client_secret"
        assert config.credentials.private_key == sample_private_key

    def test_build_uses_default_retry_config(self, configured_builder):
        """Test that build uses default retry configuration."""
        config = configured_builder.build()

        assert config.retry_config.retries == 3
        assert config.retry_config.backoff_ms == 200

    def test_build_resolves_environment_config(self, configured_builder):
        """Test that build properly resolves environment configuration."""
        config = configured_builder.build()

        assert config.env_config is not None
        assert config.env_config.base_url
        assert config.env_config.scope

    def test_multiple_builds_same_builder(self, configured_builder):
        """Test that multiple builds from the same builder work correctly."""
        config1 = configured_builder.build()
        config2 = configured_builder.build()

        assert config1 == config2
        assert config1 is not config2


class TestSDKConfigBuilderBuildClient:
    """Test cases for SDKConfigBuilder build_client functionality."""

    def test_build_client_success(self, configured_builder):
        """Test a successful client build."""
        client = configured_builder.build_client()

        assert isinstance(client, RetornaClient)
        assert isinstance(client.config, SDKConfig)
        assert client.config.environment == RetornaEnvironment.PRODUCTION

    def test_build_client_with_custom_config(self, configured_builder):
        """Test client build with custom configuration."""
        client = (
            configured_builder.logging_level(LoggingLevel.DEBUG)
            .base_url_override("https://custom.api.com")
            .build_client()
        )

        assert client.config.logging_config.level == LoggingLevel.DEBUG
        assert client.config.base_url == "https://custom.api.com"

    def test_build_client_failure_missing_params(self, sdk_config_builder):
        """Test build_client fails when required parameters are missing."""
        with pytest.raises(ValueError):
            sdk_config_builder.build_client()

    def test_build_client_vs_build_consistency(
        self, configured_builder, sample_private_key
    ):
        """Test that build_client creates a client with equivalent config to build."""
        config = configured_builder.build()

        fresh_builder = (
            SDKConfigBuilder()
            .environment(RetornaEnvironment.PRODUCTION)
            .client_id("test_client_id")
            .client_secret("test_client_secret")
            .private_key(sample_private_key)
        )

        client = fresh_builder.build_client()

        assert client.config == config


class TestSDKConfigBuilderEdgeCases:
    """Test edge cases and error conditions for SDKConfigBuilder."""

    def test_invalid_logging_level_string(self, sdk_config_builder):
        """Test that an invalid logging level string raises ValueError."""
        with pytest.raises(ValueError):
            sdk_config_builder.logging_level("invalid_level")

    def test_empty_string_parameters(self, sdk_config_builder):
        """Test behavior with empty string parameters."""
        (
            sdk_config_builder.environment("")
            .client_id("")
            .client_secret("")
            .private_key("")
        )

        with pytest.raises(ValueError):
            sdk_config_builder.build()

    def test_none_parameters(self, sdk_config_builder):
        """Test behavior with None parameters."""
        (
            sdk_config_builder.environment(None)  # type: ignore[arg-type]
            .client_id(None)  # type: ignore[arg-type]
            .client_secret(None)  # type: ignore[arg-type]
            .private_key(None)
        )  # type: ignore[arg-type]

        with pytest.raises(ValueError):
            sdk_config_builder.build()

    def test_overwriting_configuration(self, sdk_config_builder):
        """Test that configuration can be overwritten."""
        (
            sdk_config_builder.environment(RetornaEnvironment.DEVELOP).client_id(
                "initial_id"
            )
        )

        (
            sdk_config_builder.environment(RetornaEnvironment.PRODUCTION).client_id(
                "final_id"
            )
        )

        assert sdk_config_builder._environment == RetornaEnvironment.PRODUCTION
        assert sdk_config_builder._client_id == "final_id"

    def test_partial_configuration_build_failure(self, sdk_config_builder):
        """Test that partial configuration fails at build time."""
        (
            sdk_config_builder.environment(RetornaEnvironment.PRODUCTION).client_id(
                "test_id"
            )
        )

        with pytest.raises(ValueError) as exc_info:
            sdk_config_builder.build()

        error_message = str(exc_info.value)
        assert "client_secret" in error_message
        assert "private_key" in error_message
        assert "client_id" not in error_message
        assert "environment" not in error_message
