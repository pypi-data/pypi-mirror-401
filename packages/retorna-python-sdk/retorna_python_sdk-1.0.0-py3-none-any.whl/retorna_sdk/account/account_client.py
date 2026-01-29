from typing import List

from ..core import SignedHttpClient
from ..models import Route


class AccountClient:
    """Client for account-related API operations."""

    def __init__(self, signed_client: SignedHttpClient):
        self._client = signed_client

    def get_balance(self) -> int:
        """Returns the current account balance."""
        response = self._client.get("/balance")
        return response.get("totalBalance")

    def get_routes(self) -> List[Route]:
        """Retrieve the list of available routes."""
        response = self._client.get("/accounts/routes")
        return [Route.from_dict(item) for item in response]
