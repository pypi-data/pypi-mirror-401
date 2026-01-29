from dataclasses import dataclass

from .types import LoggingLevel


@dataclass(frozen=True)
class LoggingConfig:
    """Logging configuration for the SDK."""

    level: LoggingLevel = LoggingLevel.ERROR
    enabled: bool = True
