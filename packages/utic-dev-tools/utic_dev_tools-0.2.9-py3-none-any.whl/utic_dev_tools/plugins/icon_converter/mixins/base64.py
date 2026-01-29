import base64


class Base64Mixin:
    """Mixin for base64 encoding."""

    def get_encoding(self) -> str:
        """Get the encoding for this icon type."""
        return "base64"

    def encode(self, data: bytes) -> str:
        """Encode the data to base64."""
        return base64.b64encode(data).decode("utf-8")
