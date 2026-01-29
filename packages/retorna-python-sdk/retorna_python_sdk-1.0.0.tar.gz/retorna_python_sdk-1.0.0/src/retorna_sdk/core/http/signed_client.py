from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple

from .errors import HttpError
from .utils import build_headers

if TYPE_CHECKING:
    from ..credentials.token_manager import TokenManager
    from ..signature import SignatureService
    from .client import HttpClient


class SignedHttpClient:
    """HTTP client that applies request signing and token management."""

    def __init__(
        self,
        http_client: "HttpClient",
        signature_service: "SignatureService",
        token_manager: "TokenManager",
        logger=None,
    ):
        self.http = http_client
        self.signer = signature_service
        self.tokens = token_manager
        self.logger = logger

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """Performs a signed GET request."""
        return self._signed_request("GET", path=path, params=params, headers=headers)

    def post(
        self,
        path: str,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        """Performs a signed POST request."""
        return self._signed_request("POST", path=path, body=body, headers=headers)

    def _sign(
        self, method: str, path: str, params: Dict[str, Any], body: Dict[str, Any]
    ) -> Tuple[str, str]:
        """Compute digital signature and nonce for the request."""
        if method == "POST":
            return self.signer.sign_body(body)
        return self.signer.sign_path_and_query(
            path=f"/{path.lstrip('/')}",
            params=params,
        )

    def _execute(self, method: str, path: str, *, params=None, body=None, headers=None):
        """Delegates execution to the underlying HttpClient."""
        if method == "GET":
            return self.http.get(path, params=params, headers=headers)
        elif method == "POST":
            return self.http.post(path, body=body, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

    def _signed_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retry: bool = True,
    ):
        """Execute a signed request with token refresh fallback."""
        params = params or {}
        body = body or {}
        base_headers = headers or {}

        token = self.tokens.get_access_token()
        signature, nonce = self._sign(method, path, params, body)
        signed_headers = build_headers(token, signature, nonce, base_headers)

        try:
            return self._execute(
                method, path, params=params, body=body, headers=signed_headers
            )

        except HttpError as e:
            if retry and e.status_code in (401, 403):
                self.logger.warning(
                    f"[SignedHttpClient] {e.status_code} → refreshing token..."
                )

                self.tokens.refresh_token()
                new_token = self.tokens.get_access_token()

                signature, nonce = self._sign(method, path, params, body)
                retry_headers = build_headers(new_token, signature, nonce, base_headers)

                return self._execute(
                    method, path, params=params, body=body, headers=retry_headers
                )

            raise e
