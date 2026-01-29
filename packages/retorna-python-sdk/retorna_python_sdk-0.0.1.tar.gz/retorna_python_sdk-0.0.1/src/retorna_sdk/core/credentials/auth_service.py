import logging
from typing import TYPE_CHECKING, Tuple

from .utils import build_basic_auth_header

if TYPE_CHECKING:
    from ..environment import EnvConfig
    from ..http import HttpClient
    from .credentials import SDKCredentials


class AuthService:
    """Handles authentication against the Retorna OAuth2 API."""

    def __init__(
        self,
        http_client: "HttpClient",
        credentials: "SDKCredentials",
        environment: "EnvConfig",
        logger: logging.Logger,
    ):
        self.http = http_client
        self.credentials = credentials
        self.environment = environment
        self.logger = logger

    def fetch_access_token(self) -> Tuple[str, int]:
        """Requests a new OAuth2 access token using client credentials.

        Returns:
            A tuple containing the access token and its expiration time (in seconds).
        """
        self.logger.debug("Fetching OAuth2 access token...")

        auth_header = build_basic_auth_header(
            client_id=self.credentials.client_id,
            client_secret=self.credentials.client_secret,
        )

        response = self.http.post(
            path="/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "scope": self.environment.scope,
            },
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )

        self.logger.debug(
            f"Access token received (expires in {response.get('expires_in')}s)"
        )

        return response["access_token"], response["expires_in"]
