from enum import Enum


class RetornaEnvironment(str, Enum):
    """Supported environments for the Retorna SDK."""

    DEVELOP = "develop"
    STAGING = "staging"
    PRODUCTION = "production"
