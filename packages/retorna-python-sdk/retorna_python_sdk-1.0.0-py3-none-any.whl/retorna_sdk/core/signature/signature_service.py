from typing import Any, Dict, Tuple

from .signer import RSASigner
from .utils import generate_nonce, minify_json, stringify_query


class SignatureService:
    """Generates cryptographic signatures for signed API requests."""

    def __init__(self, private_key_pem: str):
        self.signer = RSASigner(private_key_pem)

    def sign_body(self, body: Dict[str, Any]) -> Tuple[str, str]:
        """Signs a request body for POST operations."""
        nonce = generate_nonce()
        minified_body = minify_json(body)
        message = f"{minified_body}{nonce}"
        signature = self.signer.sign_message(message)
        return signature, nonce

    def sign_path_and_query(
        self, path: str, params: Dict[str, Any] | None
    ) -> Tuple[str, str]:
        """Signs a URL path and query parameters for GET operations."""
        nonce = generate_nonce()
        query_string = stringify_query(params or {})
        message = f"{path}?{query_string}{nonce}"
        signature = self.signer.sign_message(message)
        return signature, nonce
