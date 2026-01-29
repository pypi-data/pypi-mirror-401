import time
from typing import TYPE_CHECKING, Any, Dict

import requests

from .errors import HttpError
from .utils import parse_response

if TYPE_CHECKING:
    from ..config import RetryConfig


class HttpClient:
    """Lightweight HTTP client with retry logic and error handling."""

    def __init__(self, base_url: str, retry_config: "RetryConfig", logger=None):
        self.base_url = base_url.rstrip("/")
        self.retry_config = retry_config
        self.logger = logger

    def get(
        self,
        path: str,
        params: Dict[str, Any] | None = None,
        headers: Dict[str, str] | None = None,
    ):
        """Performs a GET request."""
        return self._request("GET", path, params=params, headers=headers)

    def post(
        self,
        path: str,
        body: Any | None = None,
        data: Any | None = None,
        headers: Dict[str, str] | None = None,
    ):
        """Performs a POST request."""
        return self._request(
            "POST", path, json_body=body, data_body=data, headers=headers
        )

    def _request(
        self,
        method: str,
        path: str,
        params: Dict[str, Any] | None = None,
        json_body: Any | None = None,
        data_body: Any | None = None,
        headers: Dict[str, str] | None = None,
    ):
        """Executes an HTTP request with retries and backoff."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = headers or {}

        retries = self.retry_config.retries
        backoff_ms = self.retry_config.backoff_ms

        for attempt in range(retries + 1):
            try:
                if self.logger:
                    self.logger.debug(
                        f"[HttpClient] {method} {url} params={params} body={json_body}"
                    )

                response = requests.request(
                    method,
                    url,
                    params=params,
                    json=json_body,
                    data=data_body,
                    headers=headers,
                    timeout=10,
                )

                if 200 <= response.status_code < 300:
                    if self.logger:
                        self.logger.debug(
                            f"[HttpClient] {method} OK ({response.status_code})"
                        )
                    return parse_response(response)

                if self.logger:
                    self.logger.error(
                        f"[HttpClient] HTTP {response.status_code} - {response.text}"
                    )

                raise HttpError(
                    response.status_code, response.text, response_body=response.text
                )

            except (requests.ConnectionError, requests.Timeout) as e:
                if attempt >= retries:
                    if self.logger:
                        self.logger.error("[HttpClient] Exhausted retries")
                    raise HttpError(0, f"Network error: {e}") from e

                sleep_time = (backoff_ms / 1000.0) * (2**attempt)
                if self.logger:
                    self.logger.warning(
                        f"[HttpClient] Network error, retrying in {sleep_time:.2f}s "
                        f"(attempt {attempt + 1}/{retries})"
                    )
                time.sleep(sleep_time)

        return None
