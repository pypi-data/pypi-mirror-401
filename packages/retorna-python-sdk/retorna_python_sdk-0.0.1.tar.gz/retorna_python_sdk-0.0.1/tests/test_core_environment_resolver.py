import pytest

from src.retorna_sdk.core import RetornaEnvironment, resolve_env_config
from src.retorna_sdk.core.environment.config import ENV_CONFIG


class TestResolveEnvConfig:
    """Test cases for resolve_env_config function."""

    @pytest.mark.parametrize(
        "environment",
        [
            RetornaEnvironment.DEVELOP,
            RetornaEnvironment.STAGING,
            RetornaEnvironment.PRODUCTION,
        ],
    )
    def test_resolve_with_enum(self, environment):
        """Test resolving configuration with enum values."""
        config = resolve_env_config(environment)
        expected = ENV_CONFIG[environment]

        assert config.base_url == expected.base_url
        assert config.scope == expected.scope

    @pytest.mark.parametrize(
        "env_string,expected_enum",
        [
            ("develop", RetornaEnvironment.DEVELOP),
            ("staging", RetornaEnvironment.STAGING),
            ("production", RetornaEnvironment.PRODUCTION),
            ("DEVELOP", RetornaEnvironment.DEVELOP),
            ("STAGING", RetornaEnvironment.STAGING),
            ("PRODUCTION", RetornaEnvironment.PRODUCTION),
        ],
    )
    def test_resolve_with_string(self, env_string, expected_enum):
        """Test resolving configuration with string values (case-insensitive)."""
        config = resolve_env_config(env_string)
        expected = ENV_CONFIG[expected_enum]

        assert config.base_url == expected.base_url
        assert config.scope == expected.scope

    @pytest.mark.parametrize(
        "invalid_env", ["invalid", "test", "local", "", "dev", "prod"]
    )
    def test_resolve_with_invalid_string(self, invalid_env):
        """Test that invalid environment strings raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            resolve_env_config(invalid_env)

        assert "Invalid environment" in str(exc_info.value)
        assert invalid_env in str(exc_info.value)

    def test_resolve_with_base_url_override(self):
        """Test resolving configuration with base URL override."""
        custom_url = "https://custom-api.example.com"
        config = resolve_env_config(
            RetornaEnvironment.PRODUCTION, base_url_override=custom_url
        )

        assert config.base_url == custom_url
        assert config.scope == ENV_CONFIG[RetornaEnvironment.PRODUCTION].scope

    def test_resolve_with_scope_override(self):
        """Test resolving configuration with scope override."""
        custom_scope = "custom/scope"
        config = resolve_env_config(
            RetornaEnvironment.STAGING, scope_override=custom_scope
        )

        assert config.base_url == ENV_CONFIG[RetornaEnvironment.STAGING].base_url
        assert config.scope == custom_scope

    def test_resolve_with_both_overrides(self):
        """Test resolving configuration with both URL and scope overrides."""
        custom_url = "https://custom-api.example.com"
        custom_scope = "custom/scope"

        config = resolve_env_config(
            RetornaEnvironment.DEVELOP,
            base_url_override=custom_url,
            scope_override=custom_scope,
        )

        assert config.base_url == custom_url
        assert config.scope == custom_scope

    def test_resolve_with_none_overrides(self):
        """Test that None overrides don't affect the result."""
        config = resolve_env_config(
            RetornaEnvironment.PRODUCTION, base_url_override=None, scope_override=None
        )
        expected = ENV_CONFIG[RetornaEnvironment.PRODUCTION]

        assert config.base_url == expected.base_url
        assert config.scope == expected.scope

    def test_resolve_with_empty_string_overrides(self):
        """Test behavior with empty string overrides."""
        config = resolve_env_config(
            RetornaEnvironment.STAGING, base_url_override="", scope_override=""
        )
        expected = ENV_CONFIG[RetornaEnvironment.STAGING]

        assert config.base_url == expected.base_url
        assert config.scope == expected.scope
