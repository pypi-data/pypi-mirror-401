from dataclasses import dataclass


@dataclass(frozen=True)
class RetryConfig:
    """Retry policy for API requests.

    Specifies how many retry attempts are allowed and the base backoff
    duration between attempts.
    """

    retries: int = 3
    backoff_ms: int = 200
