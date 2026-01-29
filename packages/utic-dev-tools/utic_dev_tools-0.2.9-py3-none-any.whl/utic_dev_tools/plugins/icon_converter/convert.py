from pathlib import Path

from utic_dev_tools.plugins.icon_converter.converters import ICON_CONVERTERS
from utic_dev_tools.plugins.icon_converter.errors import UnsupportedFileTypeError
from utic_dev_tools.plugins.icon_converter.models.icon import Icon


def convert(file_path: Path) -> Icon:
    """
    Convert an icon file to a base64 encoded JSON object.

    Args:
        file_path: Path to the icon file

    Returns:
        Icon model with conversion results

    Raises:
        UnsupportedFileTypeError: If the file extension is not supported.
    """
    file_extension = file_path.suffix.lower()[1:]
    try:
        converter = ICON_CONVERTERS[file_extension](file_path)
        return converter.convert()
    except KeyError as e:
        raise UnsupportedFileTypeError(
            f"File type '{file_extension}' is not supported. "
            f"Supported types: {', '.join(ICON_CONVERTERS.keys())}"
        ) from e
