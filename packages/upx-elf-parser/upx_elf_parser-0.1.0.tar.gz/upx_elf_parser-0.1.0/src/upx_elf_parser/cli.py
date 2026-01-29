"""Command-line interface for upx-elf-parser."""

import argparse
import json
import sys
from pathlib import Path

from .exceptions import UpxElfParserError
from .parser import parse_upx_elf


def main() -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        prog="upx-elf-parser",
        description="Parse UPX-packed ELF files and extract their structure.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  upx-elf-parser packed_binary
  upx-elf-parser packed_binary --original original_binary
  upx-elf-parser packed_binary --output result.json
  upx-elf-parser packed_binary --no-data
""",
    )

    parser.add_argument(
        "file",
        type=Path,
        help="Path to the UPX-packed ELF file",
    )

    parser.add_argument(
        "-o",
        "--original",
        type=Path,
        help="Path to the original (unpacked) ELF file for better section naming",
        default=None,
    )

    parser.add_argument(
        "--output",
        type=Path,
        help="Output file path (default: stdout)",
        default=None,
    )

    parser.add_argument(
        "--no-data",
        action="store_true",
        help="Exclude raw data (hex) from output to reduce size",
    )

    parser.add_argument(
        "--indent",
        type=int,
        default=2,
        help="JSON indentation level (default: 2)",
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )

    args = parser.parse_args()

    try:
        result = parse_upx_elf(args.file, args.original)
        output = result.to_dict()

        if args.no_data:
            output = _strip_hex_data(output)

        json_output = json.dumps(output, indent=args.indent, ensure_ascii=False)

        if args.output:
            args.output.write_text(json_output, encoding="utf-8")
            print(f"Output written to: {args.output}", file=sys.stderr)
        else:
            print(json_output)

        return 0

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except UpxElfParserError as e:
        print(f"Parse error: {e}", file=sys.stderr)
        return 1

    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        return 130


def _strip_hex_data(data: dict[str, object]) -> dict[str, object]:
    """Remove hex data fields from output to reduce size."""
    from typing import Any

    result: dict[str, Any] = data.copy()

    for key in [
        "elf_header",
        "program_headers",
        "l_info",
        "p_info",
        "loader",
        "displacement",
    ]:
        val = result.get(key)
        if val and isinstance(val, dict):
            result[key] = {k: v for k, v in val.items() if k != "data_hex"}

    blocks = result.get("compressed_blocks")
    if blocks and isinstance(blocks, list):
        new_blocks = []
        for block in blocks:
            if not isinstance(block, dict):
                continue
            new_block = block.copy()
            header = new_block.get("header")
            if header and isinstance(header, dict):
                new_block["header"] = {
                    k: v for k, v in header.items() if k != "data_hex"
                }
            block_data = new_block.get("data")
            if block_data and isinstance(block_data, dict):
                new_block["data"] = {
                    k: v for k, v in block_data.items() if k != "data_hex"
                }
            new_blocks.append(new_block)
        result["compressed_blocks"] = new_blocks

    return result


if __name__ == "__main__":
    sys.exit(main())
