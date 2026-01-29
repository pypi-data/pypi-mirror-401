import base64


def build_basic_auth_header(client_id: str, client_secret: str) -> str:
    """Constructs a Basic Auth header using the provided credentials."""
    token = f"{client_id}:{client_secret}".encode("utf-8")
    encoded = base64.b64encode(token).decode("utf-8")
    return f"Basic {encoded}"
