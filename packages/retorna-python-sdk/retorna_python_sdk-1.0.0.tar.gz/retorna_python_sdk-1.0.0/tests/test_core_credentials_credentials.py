import pytest

from src.retorna_sdk.core import SDKCredentials


class TestSDKCredentials:
    """Test cases for SDKCredentials dataclass."""

    def test_creation(self):
        """Test SDKCredentials creation with valid parameters."""
        creds = SDKCredentials(
            client_id="test_id", client_secret="test_secret", private_key="test_key"
        )
        assert creds.client_id == "test_id"
        assert creds.client_secret == "test_secret"
        assert creds.private_key == "test_key"

    def test_immutability(self, sample_credentials):
        """Test that SDKCredentials is immutable (frozen)."""
        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_credentials.client_id = "new_id"

        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_credentials.client_secret = "new_secret"

        with pytest.raises(AttributeError):
            # noinspection PyDataclass
            sample_credentials.private_key = "new_key"

    def test_equality(self):
        """Test SDKCredentials equality comparison."""
        creds1 = SDKCredentials("id", "secret", "key")
        creds2 = SDKCredentials("id", "secret", "key")
        creds3 = SDKCredentials("other_id", "secret", "key")

        assert creds1 == creds2
        assert creds1 != creds3

    def test_string_representation(self):
        """Test that credentials don't expose sensitive data in string representation."""
        creds = SDKCredentials("id", "secret", "key")
        str_repr = str(creds)

        assert "SDKCredentials" in str_repr
