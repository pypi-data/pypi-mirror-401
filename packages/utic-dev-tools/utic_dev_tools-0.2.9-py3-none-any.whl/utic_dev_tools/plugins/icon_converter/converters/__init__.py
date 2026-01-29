from .svg import SVGToBase64Converter

ICON_CONVERTERS = {
    "svg": SVGToBase64Converter,
}

__all__ = ["ICON_CONVERTERS", "SVGToBase64Converter"]
