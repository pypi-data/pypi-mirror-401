from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, Union

from .retry import RetryConfig

if TYPE_CHECKING:
    from ..credentials import SDKCredentials
    from ..environment import EnvConfig, RetornaEnvironment
    from ..logging import LoggingConfig


@dataclass(frozen=True)
class SDKConfig:
    """Main configuration object for the Retorna SDK.

    Bundles all core settings required by the SDK, including environment,
    credentials, logging, retry policies, and optional overrides for
    `base_url` and `scope`.
    """

    environment: Union["RetornaEnvironment", str]
    env_config: "EnvConfig"
    credentials: "SDKCredentials"
    logging_config: "LoggingConfig"
    retry_config: RetryConfig = RetryConfig()

    base_url_override: Optional[str] = None
    scope_override: Optional[str] = None

    @property
    def base_url(self) -> str:
        """Resolved base URL used for API requests."""
        return self.base_url_override or self.env_config.base_url

    @property
    def scope(self) -> str:
        """Resolved OAuth2 scope used for authentication."""
        return self.scope_override or self.env_config.scope
