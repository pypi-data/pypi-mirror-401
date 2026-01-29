import pytest

from src.retorna_sdk.core import EnvConfig, RetornaEnvironment
from src.retorna_sdk.core.environment.config import ENV_CONFIG


class TestEnvConfig:
    """Test cases for EnvConfig dataclass."""

    def test_creation(self):
        """Test EnvConfig creation with valid parameters."""
        config = EnvConfig(base_url="https://api.example.com", scope="test/scope")
        assert config.base_url == "https://api.example.com"
        assert config.scope == "test/scope"

    def test_immutability(self, sample_env_config):
        """Test that EnvConfig is immutable (frozen)."""
        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_env_config.base_url = "new_url"

    def test_equality(self):
        """Test EnvConfig equality comparison."""
        config1 = EnvConfig("https://api.example.com", "test/scope")
        config2 = EnvConfig("https://api.example.com", "test/scope")
        config3 = EnvConfig("https://other.example.com", "test/scope")

        assert config1 == config2
        assert config1 != config3


class TestEnvConfigMapping:
    """Test cases for ENV_CONFIG constant."""

    def test_all_environments_mapped(self, all_environments):
        """Test that all environments have configuration mappings."""
        for env in all_environments:
            assert env in ENV_CONFIG
            assert isinstance(ENV_CONFIG[env], EnvConfig)

    def test_config_values_not_empty(self):
        """Test that all configurations have non-empty values."""
        for env, config in ENV_CONFIG.items():
            assert config.base_url.strip()
            assert config.scope.strip()
            assert config.base_url.startswith(("http://", "https://"))

    def test_unique_base_urls(self):
        """Test that each environment has a unique base URL."""
        base_urls = [config.base_url for config in ENV_CONFIG.values()]
        assert len(set(base_urls)) == len(base_urls)

    def test_develop_environment_config(self):
        """Test specific configuration for develop environment."""
        config = ENV_CONFIG[RetornaEnvironment.DEVELOP]
        assert "develop" in config.base_url
        assert config.scope == "test/full_access"

    def test_staging_environment_config(self):
        """Test specific configuration for staging environment."""
        config = ENV_CONFIG[RetornaEnvironment.STAGING]
        assert "staging" in config.base_url
        assert config.scope == "test/full_access"

    def test_production_environment_config(self):
        """Test specific configuration for production environment."""
        config = ENV_CONFIG[RetornaEnvironment.PRODUCTION]
        assert "production" in config.base_url
        assert config.scope == "prod/full_access"
