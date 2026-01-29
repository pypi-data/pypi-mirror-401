class IconConverterError(Exception):
    """Base exception for icon converter errors."""


class InvalidIconError(IconConverterError):
    """Raised when the icon file is invalid or corrupted."""


class UnsupportedFileTypeError(IconConverterError):
    """Raised when the file type is not supported."""
