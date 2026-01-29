from src.retorna_sdk.core import RetornaEnvironment


class TestRetornaEnvironment:
    """Test cases for RetornaEnvironment enum."""

    def test_enum_values(self):
        """Test that enum values are correct."""
        assert RetornaEnvironment.DEVELOP == "develop"
        assert RetornaEnvironment.STAGING == "staging"
        assert RetornaEnvironment.PRODUCTION == "production"

    def test_enum_membership(self):
        """Test enum membership operations."""
        assert "develop" in RetornaEnvironment
        assert "staging" in RetornaEnvironment
        assert "production" in RetornaEnvironment
        assert "invalid" not in RetornaEnvironment

    def test_enum_iteration(self, all_environments):
        """Test that all environments are accessible via iteration."""
        enum_values = list(RetornaEnvironment)
        assert len(enum_values) == 3
        for env in all_environments:
            assert env in enum_values
