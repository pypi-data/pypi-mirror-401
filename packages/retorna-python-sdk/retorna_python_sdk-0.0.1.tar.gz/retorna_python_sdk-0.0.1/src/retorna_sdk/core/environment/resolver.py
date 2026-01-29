from typing import Optional, Union

from .config import ENV_CONFIG, EnvConfig
from .types import RetornaEnvironment


def resolve_env_config(
    environment: Union[RetornaEnvironment, str],
    base_url_override: Optional[str] = None,
    scope_override: Optional[str] = None,
) -> EnvConfig:
    """Resolves the environment configuration, applying optional overrides."""

    if isinstance(environment, str):
        try:
            environment = RetornaEnvironment(environment.lower())
        except ValueError:
            raise ValueError(
                f"Invalid environment '{environment}'. "
                f"Expected one of: {[e.value for e in RetornaEnvironment]}"
            )

    env_cfg = ENV_CONFIG[environment]

    return EnvConfig(
        base_url=base_url_override or env_cfg.base_url,
        scope=scope_override or env_cfg.scope,
    )
