from typing import Any, Optional


class HttpError(Exception):
    """Represents an HTTP request failure."""

    def __init__(
        self, status_code: int, message: str, response_body: Optional[Any] = None
    ):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.response_body = response_body
