#!/usr/bin/env python
"""
Command-line interface for icon converter.

Usage:
    python cli.py <svg_file>
    python cli.py <svg_file> -o output.json
"""

import argparse
import sys
from pathlib import Path

from utic_dev_tools.plugins.icon_converter import convert
from utic_dev_tools.plugins.icon_converter.errors import IconConverterError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert icon files to base64 encoded JSON with sanitization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s icon.svg
  %(prog)s path/to/logo.svg > output.json
  %(prog)s icon.svg -o output.json
        """,
    )

    parser.add_argument("file", type=str, help="Path to the icon file (currently supports .svg)")

    parser.add_argument(
        "-o", "--output", type=str, help="Output file path (default: stdout)", default=None
    )

    args = parser.parse_args()

    try:
        file_path = Path(args.file)
        result_json = convert(file_path).model_dump_json(indent=2)

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result_json)
            print(f"✓ Successfully converted {args.file} -> {args.output}", file=sys.stderr)
        else:
            print(result_json)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except IconConverterError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
