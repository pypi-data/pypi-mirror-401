"""Custom exceptions for upx-elf-parser."""


class UpxElfParserError(Exception):
    """Base exception for upx-elf-parser."""


class InvalidElfError(UpxElfParserError):
    """Raised when the file is not a valid ELF file."""


class UnsupportedElfTypeError(UpxElfParserError):
    """Raised when the ELF type is not supported (e.g., ET_DYN)."""


class InvalidUpxStructureError(UpxElfParserError):
    """Raised when the UPX structure cannot be parsed."""


class NoLoadSegmentError(UpxElfParserError):
    """Raised when no suitable PT_LOAD segment is found."""
