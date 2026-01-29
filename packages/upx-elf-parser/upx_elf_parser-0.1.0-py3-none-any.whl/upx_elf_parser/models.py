"""Data models for upx-elf-parser."""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ByteSection:
    """Represents a section of bytes extracted from the ELF file.

    Attributes:
        address: Virtual address of the section.
        data: Raw bytes of the section.
        name: Name of the section.
    """

    address: int
    data: bytes
    name: str

    def __len__(self) -> int:
        """Return the length of the section data."""
        return len(self.data)


@dataclass(frozen=True)
class BlockInfo:
    """UPX block header information (b_info structure).

    Attributes:
        uncompressed_size: Size of uncompressed data.
        compressed_size: Size of compressed data.
        method: Compression method.
        filter_id: Filter ID.
        cto8: Checksum-to-8.
        unused: Unused byte.
    """

    uncompressed_size: int
    compressed_size: int
    method: int
    filter_id: int
    cto8: int
    unused: int


@dataclass(frozen=True)
class CompressedBlock:
    """Represents a compressed block in UPX structure.

    Attributes:
        index: Block index (0-based).
        block_info: Block header information.
        header_section: The b_info header section.
        data_section: The compressed data section.
        inferred_segment: Inferred original segment name (if available).
    """

    index: int
    block_info: BlockInfo
    header_section: ByteSection
    data_section: ByteSection
    inferred_segment: str | None = None


@dataclass(frozen=True)
class LInfo:
    """UPX l_info structure (12 bytes after program headers).

    Contains information about the loader.
    """

    section: ByteSection


@dataclass(frozen=True)
class PInfo:
    """UPX p_info structure (12 bytes after l_info).

    Contains information about the packed program.
    """

    section: ByteSection


@dataclass
class UpxElfInfo:
    """Complete parsed information from a UPX-packed ELF file.

    Attributes:
        file_path: Path to the parsed file.
        is_64bit: Whether the ELF is 64-bit.
        endianness: Endianness of the ELF ('little' or 'big').
        entry_point: Entry point address.
        elf_header: ELF header section.
        program_headers: Program headers section.
        l_info: UPX l_info structure.
        p_info: UPX p_info structure.
        compressed_blocks: List of compressed blocks.
        loader: Loader code section.
        displacement: Optional displacement section (remaining bytes).
    """

    file_path: str
    is_64bit: bool
    endianness: str
    entry_point: int
    elf_header: ByteSection
    program_headers: ByteSection
    l_info: LInfo
    p_info: PInfo
    compressed_blocks: list[CompressedBlock] = field(default_factory=list)
    loader: ByteSection | None = None
    displacement: ByteSection | None = None

    @property
    def total_compressed_size(self) -> int:
        """Return total size of all compressed blocks."""
        return sum(block.block_info.compressed_size for block in self.compressed_blocks)

    @property
    def total_uncompressed_size(self) -> int:
        """Return total uncompressed size of all blocks."""
        return sum(
            block.block_info.uncompressed_size for block in self.compressed_blocks
        )

    @property
    def compression_ratio(self) -> float:
        """Return compression ratio (compressed/uncompressed)."""
        if self.total_uncompressed_size == 0:
            return 0.0
        return self.total_compressed_size / self.total_uncompressed_size

    def get_all_sections(self) -> list[ByteSection]:
        """Return all sections in order."""
        sections = [
            self.elf_header,
            self.program_headers,
            self.l_info.section,
            self.p_info.section,
        ]
        for block in self.compressed_blocks:
            sections.append(block.header_section)
            sections.append(block.data_section)
        if self.displacement:
            sections.append(self.displacement)
        if self.loader:
            sections.append(self.loader)
        return sections

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "file_path": self.file_path,
            "is_64bit": self.is_64bit,
            "endianness": self.endianness,
            "entry_point": self.entry_point,
            "compression_ratio": self.compression_ratio,
            "elf_header": _section_to_dict(self.elf_header),
            "program_headers": _section_to_dict(self.program_headers),
            "l_info": _section_to_dict(self.l_info.section),
            "p_info": _section_to_dict(self.p_info.section),
            "compressed_blocks": [
                {
                    "index": block.index,
                    "inferred_segment": block.inferred_segment,
                    "block_info": {
                        "uncompressed_size": block.block_info.uncompressed_size,
                        "compressed_size": block.block_info.compressed_size,
                        "method": block.block_info.method,
                        "filter_id": block.block_info.filter_id,
                        "cto8": block.block_info.cto8,
                        "unused": block.block_info.unused,
                    },
                    "header": _section_to_dict(block.header_section),
                    "data": _section_to_dict(block.data_section),
                }
                for block in self.compressed_blocks
            ],
            "displacement": (
                _section_to_dict(self.displacement) if self.displacement else None
            ),
            "loader": _section_to_dict(self.loader) if self.loader else None,
        }


def _section_to_dict(section: ByteSection) -> dict[str, Any]:
    """Convert ByteSection to dictionary."""
    return {
        "name": section.name,
        "address": section.address,
        "size": len(section.data),
        "data_hex": section.data.hex(),
    }
