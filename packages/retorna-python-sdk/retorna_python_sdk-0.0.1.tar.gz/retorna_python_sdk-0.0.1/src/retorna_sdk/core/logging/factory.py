import logging
from typing import TYPE_CHECKING

from .types import LoggingLevel

if TYPE_CHECKING:
    from .config import LoggingConfig


def create_sdk_logger(config: "LoggingConfig") -> logging.Logger:
    """Creates the logger used by the Retorna SDK."""
    logger = logging.getLogger("retorna_sdk")

    logger.propagate = False

    if not config.enabled or config.level == LoggingLevel.NONE:
        logger.disabled = True
        return logger

    logger.disabled = False

    logger.setLevel(
        {
            LoggingLevel.ERROR: logging.ERROR,
            LoggingLevel.WARN: logging.WARNING,
            LoggingLevel.INFO: logging.INFO,
            LoggingLevel.DEBUG: logging.DEBUG,
        }[config.level]
    )

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("[RetornaSDK] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
