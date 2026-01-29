from abc import ABC, abstractmethod
from pathlib import Path

from utic_dev_tools.plugins.icon_converter.models.icon import Icon


class BaseIconConverter(ABC):
    """Base class for icon converters."""

    def __init__(self, file_path: str | Path):
        """
        Initialize the converter.

        Args:
            file_path: Path to the icon file
        """
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        self.file_extension = self.file_path.suffix.lower()

    @abstractmethod
    def validate(self) -> bool:
        """
        Validate if the file is a proper icon file.

        Returns:
            True if valid

        Raises:
            InvalidIconError: If the file is invalid
        """

    @abstractmethod
    def process(self) -> bytes:
        """
        Process the icon file (sanitize, modify, etc.).

        Returns:
            Processed icon file content as bytes
        """

    @abstractmethod
    def get_mime_type(self) -> str:
        """
        Get the MIME type for this icon type.

        Returns:
            MIME type string
        """

    @abstractmethod
    def get_encoding(self) -> str:
        """
        Get the encoding for this icon type.

        Returns:
            Encoding string
        """

    @abstractmethod
    def encode(self, data: bytes) -> str:
        """
        Encode the icon data.

        Args:
            data: Icon file content as bytes

        Returns:
            Encoded string
        """

    def convert(self) -> Icon:
        """
        Main conversion method that orchestrates the entire process.

        Returns:
            Icon model with conversion results
        """
        self.validate()

        processed_data = self.process()

        encoded_value = self.encode(processed_data)

        return Icon(
            value=encoded_value,
            original_file_extension=self.file_extension.lstrip("."),
            encoding=self.get_encoding(),
            mime_type=self.get_mime_type(),
        )
