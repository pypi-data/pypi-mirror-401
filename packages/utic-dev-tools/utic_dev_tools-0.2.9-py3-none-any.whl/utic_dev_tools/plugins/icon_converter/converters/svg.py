import optparse
import re
from xml.etree import ElementTree as ET

from scour import scour

from utic_dev_tools.plugins.icon_converter.converters.base import BaseIconConverter
from utic_dev_tools.plugins.icon_converter.errors import InvalidIconError
from utic_dev_tools.plugins.icon_converter.mixins.base64 import Base64Mixin


class SVGToBase64Converter(Base64Mixin, BaseIconConverter):
    """Converter for SVG icon files."""

    DANGEROUS_ELEMENTS = {
        "script",
        "iframe",
        "object",
        "embed",
        "foreignObject",
        "link",
        "use",
    }

    DANGEROUS_ATTRIBUTES = {
        "onclick",
        "onload",
        "onerror",
        "onmouseover",
        "onmouseout",
        "onmousemove",
        "onmouseenter",
        "onmouseleave",
        "onfocus",
        "onblur",
        "onchange",
        "onsubmit",
        "onkeydown",
        "onkeyup",
        "onkeypress",
        "onanimationstart",
        "onanimationend",
        "onanimationiteration",
        "ontransitionend",
    }

    SCOUR_OPTIONS = {"enable_viewboxing": True, "strip_xml_prolog": True}

    def validate(self) -> bool:
        """
        Validate if the file is a proper SVG file.

        Returns:
            True if valid

        Raises:
            InvalidIconError: If the file is not a valid SVG
        """
        try:
            content = self.file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError as e:
            raise InvalidIconError(f"File is not valid UTF-8 text: {e}") from e

        # Check if content contains SVG tag
        if not re.search(r"<svg[\s>]", content, re.IGNORECASE):
            raise InvalidIconError("File does not contain a valid SVG tag")

        # Try to parse as XML
        try:
            ET.fromstring(content)
        except ET.ParseError as e:
            raise InvalidIconError(f"Invalid XML structure: {e}") from e

        return True

    def _sanitize_remove_attributes(self, element: ET.Element) -> None:
        """
        Remove dangerous attributes from an XML element.

        Args:
            element: XML element to sanitize
        """
        attrs_to_remove = []
        for attr_name in element.attrib:
            # Check for event handlers (on*)
            clean_attr = attr_name.split("}")[-1]  # Remove namespace if present
            if clean_attr.lower() in self.DANGEROUS_ATTRIBUTES:
                attrs_to_remove.append(attr_name)
            # Check for javascript: in href/xlink:href
            elif "href" in clean_attr.lower():
                href_value = element.attrib[attr_name]
                href_lower = href_value.strip().lower()
                # Remove javascript: or dangerous data: URIs (keep data:image/)
                if href_lower.startswith("javascript:") or (
                    href_lower.startswith("data:") and not href_lower.startswith("data:image/")
                ):
                    attrs_to_remove.append(attr_name)

        for attr_name in attrs_to_remove:
            del element.attrib[attr_name]

    def _sanitize_remove_elements(self, element: ET.Element) -> None:
        """
        Remove dangerous elements from an XML element.

        Args:
            element: XML element to sanitize
        """
        # Remove dangerous child elements
        children_to_remove = []
        for child in element:
            tag_name = child.tag.split("}")[-1] if "}" in child.tag else child.tag
            if tag_name.lower() in self.DANGEROUS_ELEMENTS:
                children_to_remove.append(child)
            else:
                # Recursively sanitize children
                self._sanitize_element(child)

        for child in children_to_remove:
            element.remove(child)

    def _sanitize_element(self, element: ET.Element) -> None:
        """
        Recursively sanitize an XML element.

        Args:
            element: XML element to sanitize
        """
        self._sanitize_remove_attributes(element)
        self._sanitize_remove_elements(element)

    def _optimize_svg(self, content: str) -> str:
        """
        Optimize the SVG content.

        Args:
            content: SVG content to optimize

        Returns:
            Optimized SVG content
        """
        options = optparse.Values(self.SCOUR_OPTIONS)
        return scour.scourString(content, options)

    def process(self) -> bytes:
        """
        Process the SVG file: remove dimensions and sanitize.

        Returns:
            Processed SVG content as bytes
        """
        # Parse the SVG
        try:
            # Register namespaces to preserve them
            namespaces = dict(
                [node for _, node in ET.iterparse(self.file_path, events=["start-ns"])]
            )

            # Re-register namespaces
            for prefix, uri in namespaces.items():
                if prefix:
                    ET.register_namespace(prefix, uri)
                else:
                    # Default namespace
                    ET.register_namespace("", uri)

            tree = ET.parse(self.file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            raise InvalidIconError(f"Cannot parse SVG: {e}") from e

        # Sanitize the entire tree
        self._sanitize_element(root)

        # Convert back to string
        processed_content = ET.tostring(root, encoding="unicode", method="xml")

        # Optimize the SVG
        processed_content = self._optimize_svg(processed_content)

        return processed_content.encode("utf-8")

    def get_mime_type(self) -> str:
        """
        Get the MIME type for SVG files.

        Returns:
            MIME type string
        """
        return "image/svg+xml"
