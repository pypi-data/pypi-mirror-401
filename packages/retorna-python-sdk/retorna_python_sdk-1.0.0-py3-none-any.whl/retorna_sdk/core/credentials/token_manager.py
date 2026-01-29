import time
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from logging import Logger

    from .auth_service import AuthService


class TokenManager:
    """Manages retrieval and caching of OAuth2 access tokens."""

    def __init__(
        self,
        auth_service: "AuthService",
        logger: "Logger",
    ):
        self.auth = auth_service
        self.logger = logger

        self._access_token: Optional[str] = None
        self._expires_at: float = 0

    def get_access_token(self) -> str:
        """Returns a valid access token, refreshing it if necessary."""
        if not self._is_token_valid():
            self.logger.debug("Access token missing or expired — refreshing...")
            self.refresh_token()

        if self._access_token is None:
            raise RuntimeError("Failed to obtain access token")

        return self._access_token

    def refresh_token(self) -> None:
        """Requests a new access token and updates the cached expiration."""
        if self._is_token_valid():
            return

        self.logger.info("Requesting new access token...")

        token, expires_in = self.auth.fetch_access_token()
        self._access_token = token
        self._expires_at = time.time() + (expires_in * 0.9)

        self.logger.debug(
            f"Access token obtained — expires in {expires_in}s "
            f"(cached until {self._expires_at})."
        )

    def _is_token_valid(self) -> bool:
        return self._access_token is not None and time.time() < self._expires_at
