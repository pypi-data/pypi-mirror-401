from enum import Enum


class LoggingLevel(str, Enum):
    """Supported logging levels for the SDK."""

    NONE = "none"
    ERROR = "error"
    WARN = "warn"
    INFO = "info"
    DEBUG = "debug"
