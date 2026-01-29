import base64

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


class RSASigner:
    """RSA signer used to generate PKCS#1 v1.5 signatures."""

    def __init__(self, private_key_pem: str):
        self.private_key = RSA.import_key(private_key_pem)

    def sign_message(self, message: str) -> str:
        """Signs the given message and returns a Base64-encoded signature."""
        h = SHA256.new(message.encode("utf-8"))
        signature = pkcs1_15.new(self.private_key).sign(h)
        return base64.b64encode(signature).decode("utf-8")
