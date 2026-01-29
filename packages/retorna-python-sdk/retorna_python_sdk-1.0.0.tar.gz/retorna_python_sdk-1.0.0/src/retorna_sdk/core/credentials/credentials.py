from dataclasses import dataclass


@dataclass(frozen=True)
class SDKCredentials:
    """Authentication credentials for the Retorna SDK."""

    client_id: str
    client_secret: str
    private_key: str
