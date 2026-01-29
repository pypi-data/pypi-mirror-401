# mypy: check-untyped-defs
from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Self, Union, cast

from ..core import (LoggingConfig, LoggingLevel, RetryConfig, SDKConfig,
                    SDKCredentials, resolve_env_config)
from .client import RetornaClient

if TYPE_CHECKING:
    from ..core import RetornaEnvironment


class SDKConfigBuilder:
    """Builder for creating SDKConfig and RetornaClient instances."""

    def __init__(self):
        self._environment: Optional[Union[str, "RetornaEnvironment"]] = None
        self._client_id: Optional[str] = None
        self._client_secret: Optional[str] = None
        self._private_key: Optional[str] = None
        self._logging_config: LoggingConfig = LoggingConfig()
        self._retry_config: RetryConfig = RetryConfig()
        self._base_url_override: Optional[str] = None
        self._scope_override: Optional[str] = None

    def environment(self, env: Union[str, "RetornaEnvironment"]) -> Self:
        """Sets the target environment."""
        self._environment = env
        return self

    def client_id(self, value: str) -> Self:
        """Sets the OAuth2 client ID."""
        self._client_id = value
        return self

    def client_secret(self, value: str) -> Self:
        """Sets the OAuth2 client secret."""
        self._client_secret = value
        return self

    def private_key(self, value: str) -> Self:
        """Sets the private key used for signing."""
        self._private_key = value
        return self

    def logging_level(self, level: Union[str, LoggingLevel]) -> Self:
        """Sets the logging level."""
        if isinstance(level, str):
            level = LoggingLevel(level)
        self._logging_config = LoggingConfig(level=level)
        return self

    def disable_logging(self) -> Self:
        """Disables logging."""
        self._logging_config = LoggingConfig(level=LoggingLevel.NONE, enabled=False)
        return self

    def base_url_override(self, url: str) -> Self:
        """Overrides the default base URL."""
        self._base_url_override = url
        return self

    def base_scope_override(self, scope: str) -> Self:
        """Overrides the default OAuth scope."""
        self._scope_override = scope
        return self

    def _validate(self):
        missing = []
        if not self._environment:
            missing.append("environment")
        if not self._client_id:
            missing.append("client_id")
        if not self._client_secret:
            missing.append("client_secret")
        if not self._private_key:
            missing.append("private_key")

        if missing:
            raise ValueError(
                f"Missing required SDK config parameters: {', '.join(missing)}"
            )

    def build(self) -> SDKConfig:
        """Builds and returns an SDKConfig instance."""
        self._validate()

        self._client_id = cast(str, self._client_id)
        self._client_secret = cast(str, self._client_secret)
        self._private_key = cast(str, self._private_key)
        self._environment = cast(Union[str, "RetornaEnvironment"], self._environment)

        env_config = resolve_env_config(
            environment=self._environment,
            base_url_override=self._base_url_override,
        )

        creds = SDKCredentials(
            client_id=self._client_id,
            client_secret=self._client_secret,
            private_key=self._private_key,
        )

        return SDKConfig(
            environment=self._environment,
            env_config=env_config,
            credentials=creds,
            logging_config=self._logging_config,
            retry_config=self._retry_config,
            base_url_override=self._base_url_override,
        )

    def build_client(self) -> RetornaClient:
        """Builds and returns a RetornaClient."""
        return RetornaClient(self.build())
