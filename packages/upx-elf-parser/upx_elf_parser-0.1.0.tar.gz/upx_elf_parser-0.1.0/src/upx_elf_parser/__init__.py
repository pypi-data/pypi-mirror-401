"""upx-elf-parser: A Python library for parsing UPX-packed ELF files.

This library provides tools to parse and analyze UPX-packed ELF executables,
extracting their internal structure including headers, compressed blocks,
and loader code.

Example:
    >>> from upx_elf_parser import parse_upx_elf
    >>> result = parse_upx_elf("packed_binary")
    >>> print(result.compression_ratio)
    0.35
    >>> for block in result.compressed_blocks:
    ...     print(f"{block.header_section.name}: {block.block_info.compressed_size} bytes")
"""

from .exceptions import (
    InvalidElfError,
    InvalidUpxStructureError,
    NoLoadSegmentError,
    UnsupportedElfTypeError,
    UpxElfParserError,
)
from .models import (
    BlockInfo,
    ByteSection,
    CompressedBlock,
    LInfo,
    PInfo,
    UpxElfInfo,
)
from .parser import parse_upx_elf

__version__ = "0.1.0"
__all__ = [
    # Main API
    "parse_upx_elf",
    # Data models
    "BlockInfo",
    "ByteSection",
    "CompressedBlock",
    "LInfo",
    "PInfo",
    "UpxElfInfo",
    # Exceptions
    "UpxElfParserError",
    "InvalidElfError",
    "InvalidUpxStructureError",
    "NoLoadSegmentError",
    "UnsupportedElfTypeError",
]
