from dataclasses import dataclass

from .types import RetornaEnvironment


@dataclass(frozen=True)
class EnvConfig:
    """Environment-specific API configuration."""

    base_url: str
    scope: str


ENV_CONFIG: dict[RetornaEnvironment, EnvConfig] = {
    RetornaEnvironment.DEVELOP: EnvConfig(
        base_url="https://juv1y5r7j0.execute-api.us-east-1.amazonaws.com/develop",
        scope="test/full_access",
    ),
    RetornaEnvironment.STAGING: EnvConfig(
        base_url="https://g4mtm3uz70.execute-api.us-east-1.amazonaws.com/staging",
        scope="test/full_access",
    ),
    RetornaEnvironment.PRODUCTION: EnvConfig(
        base_url="https://glog27kdkf.execute-api.us-east-1.amazonaws.com/production",
        scope="prod/full_access",
    ),
}
