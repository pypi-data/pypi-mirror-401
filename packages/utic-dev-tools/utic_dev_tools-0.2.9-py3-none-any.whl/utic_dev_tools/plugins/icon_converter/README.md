# Icon Converter

A utility for converting icon files to base64-encoded JSON format with sanitization and optimization.

## Features

- **SVG Support**: Converts SVG files to base64-encoded JSON
- **Security**: Sanitizes SVG files by removing dangerous elements (`script`, `iframe`, `object`, etc.) and event handlers
- **Optimization**: Uses [scour](https://github.com/scour-project/scour) to optimize SVG files
- **Validation**: Validates icon files before processing
- **CLI & Library**: Use as a command-line tool or import as a Python module

## Usage

### As a Library

```python
from pathlib import Path
from utic_dev_tools.plugins.icon_converter import convert

result = convert(Path("icon.svg"))
# Returns:
# {
#     "value": "PHN2ZyB4bWxucz0i...",  # base64-encoded content
#     "original_file_extension": "svg",
#     "encoding": "base64",
#     "mime_type": "image/svg+xml"
# }
```

### As a CLI Tool

```bash
# Output to stdout
python -m utic_dev_tools.plugins.icon_converter.cli icon.svg

# Save to file
python -m utic_dev_tools.plugins.icon_converter.cli icon.svg -o output.json
```

## Output Format

The converter returns a dictionary with the following structure:

- `value`: Base64-encoded icon content
- `original_file_extension`: Original file extension (e.g., "svg")
- `encoding`: Encoding type ("base64")
- `mime_type`: MIME type of the icon (e.g., "image/svg+xml")

## Security

The SVG converter automatically removes:

- Dangerous elements: `script`, `iframe`, `object`, `embed`, `foreignObject`, `link`, `use`
- Event handlers: `onclick`, `onload`, `onerror`, etc.
- Dangerous `href` attributes containing JavaScript or non-image data URIs

## Extending

To add support for new icon formats, create a new converter class that inherits from `BaseIconConverter`:

```python
from utic_dev_tools.plugins.icon_converter.converters.base import BaseIconConverter

class MyIconConverter(BaseIconConverter):
    def validate(self) -> bool:
        # Validation logic
        pass

    def process(self) -> bytes:
        # Processing logic
        pass

    def get_mime_type(self) -> str:
        return "image/my-format"

    def get_encoding(self) -> str:
        return "base64"

    def encode(self, data: bytes) -> str:
        # Encoding logic
        pass
```

Then register it in `converters/__init__.py`:

```python
ICON_CONVERTERS = {
    "svg": SVGToBase64Converter,
    "myformat": MyIconConverter,
}
```
