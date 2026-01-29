import json
from typing import Dict

from requests import Response


def parse_response(response: Response):
    """Parses a Response into JSON or raw text."""
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text


def build_headers(
    token: str, signature: str, nonce: str, extra: Dict[str, str]
) -> Dict[str, str]:
    """Builds the default headers for a signed request."""
    return {
        "Authorization": f"Bearer {token}",
        "nonce": nonce,
        "signature": signature,
        "Content-Type": "application/json",
        **(extra or {}),
    }
