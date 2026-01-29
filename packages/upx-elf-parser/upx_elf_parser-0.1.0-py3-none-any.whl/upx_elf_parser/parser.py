"""Core parsing logic for UPX-packed ELF files."""

import struct
import warnings
from io import BytesIO
from pathlib import Path

from elftools.common.exceptions import ELFError
from elftools.elf.constants import P_FLAGS
from elftools.elf.elffile import ELFFile

from .exceptions import (
    InvalidElfError,
    InvalidUpxStructureError,
    NoLoadSegmentError,
    UnsupportedElfTypeError,
)
from .models import (
    BlockInfo,
    ByteSection,
    CompressedBlock,
    LInfo,
    PInfo,
    UpxElfInfo,
)

_ELF_MAGIC = b"\x7fELF"
_ELF_HEADER_SIZE_32 = 52
_ELF_HEADER_SIZE_64 = 64
_UPX_INFO_SIZE = 12  # Size of l_info and p_info structures


def parse_upx_elf(
    file_path: str | Path,
    original_path: str | Path | None = None,
) -> UpxElfInfo:
    """Parse a UPX-packed ELF file and extract its structure.

    Args:
        file_path: Path to the UPX-packed ELF file.
        original_path: Optional path to the original (unpacked) ELF file.
            If provided, section names will be inferred from the original file.

    Returns:
        UpxElfInfo containing all parsed sections.

    Raises:
        FileNotFoundError: If the file does not exist.
        InvalidElfError: If the file is not a valid ELF file.
        UnsupportedElfTypeError: If the ELF type is not ET_EXEC.
        NoLoadSegmentError: If no suitable PT_LOAD segment is found.
        InvalidUpxStructureError: If the UPX structure cannot be parsed.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    file_data = file_path.read_bytes()

    if len(file_data) < _ELF_HEADER_SIZE_64:
        raise InvalidElfError("File too small to be a valid ELF file")

    if file_data[:4] != _ELF_MAGIC:
        raise InvalidElfError("File does not have ELF magic bytes")

    endianness = _detect_endianness(file_data)
    endian_char = ">" if endianness == "big" else "<"

    elf_info = _parse_elf_header(file_data, file_path)

    pt_load_data = file_data[: elf_info["segment_size"]]

    ph_end = elf_info["phdr_offset"] + (
        elf_info["phdr_count"] * elf_info["phdr_entry_size"]
    )

    l_info_start = ph_end
    l_info_end = l_info_start + _UPX_INFO_SIZE
    p_info_start = l_info_end
    p_info_end = p_info_start + _UPX_INFO_SIZE

    entry_point_offset = elf_info["entry_point"] - elf_info["segment_vaddr"]

    if entry_point_offset <= p_info_end:
        raise InvalidUpxStructureError(
            f"Entry point offset ({entry_point_offset}) is before p_info end ({p_info_end})"
        )

    if entry_point_offset > elf_info["segment_size"]:
        raise InvalidUpxStructureError(
            f"Entry point offset ({entry_point_offset}) exceeds segment size ({elf_info['segment_size']})"
        )

    if p_info_end > len(pt_load_data):
        raise InvalidUpxStructureError(
            "Not enough data for l_info and p_info extraction"
        )

    elf_header = ByteSection(
        address=0,
        data=pt_load_data[: elf_info["header_size"]],
        name=".elf_header",
    )

    program_headers = ByteSection(
        address=elf_info["phdr_offset"],
        data=pt_load_data[elf_info["phdr_offset"] : ph_end],
        name=".program_headers",
    )

    l_info = LInfo(
        section=ByteSection(
            address=l_info_start,
            data=pt_load_data[l_info_start:l_info_end],
            name=".l_info",
        )
    )

    p_info = PInfo(
        section=ByteSection(
            address=p_info_start,
            data=pt_load_data[p_info_start:p_info_end],
            name=".p_info",
        )
    )

    compressed_data = pt_load_data[p_info_end:entry_point_offset]
    section_names = []
    if original_path:
        original_path = Path(original_path)
        if original_path.exists():
            section_names = _get_section_names_from_original(original_path)

    compressed_blocks, displacement = _split_compressed_data(
        compressed_data, p_info_end, endian_char, section_names
    )

    loader = ByteSection(
        address=entry_point_offset,
        data=pt_load_data[entry_point_offset:],
        name=".loader",
    )

    return UpxElfInfo(
        file_path=str(file_path),
        is_64bit=bool(elf_info["is_64bit"]),
        endianness=endianness,
        entry_point=elf_info["entry_point"],
        elf_header=elf_header,
        program_headers=program_headers,
        l_info=l_info,
        p_info=p_info,
        compressed_blocks=compressed_blocks,
        loader=loader,
        displacement=displacement,
    )


def _detect_endianness(file_data: bytes) -> str:
    """Detect ELF file endianness from ELF header.

    Args:
        file_data: Raw ELF file data.

    Returns:
        'little' for little-endian, 'big' for big-endian.
    """
    if len(file_data) < 6:
        return "little"

    ei_data = file_data[5]
    if ei_data == 2:
        return "big"
    return "little"


def _parse_elf_header(file_data: bytes, file_path: Path) -> dict[str, int]:
    """Parse ELF header and find the first suitable PT_LOAD segment.

    Args:
        file_data: Raw file data.
        file_path: Path to the file (for error messages).

    Returns:
        Dictionary with ELF header information.

    Raises:
        InvalidElfError: If the file is not a valid ELF.
        UnsupportedElfTypeError: If the ELF type is not ET_EXEC.
        NoLoadSegmentError: If no suitable PT_LOAD segment is found.
    """
    try:
        file_obj = BytesIO(file_data)
        elf = ELFFile(file_obj)
        header = elf.header

        is_64bit = elf.elfclass == 64
        header_size = _ELF_HEADER_SIZE_64 if is_64bit else _ELF_HEADER_SIZE_32

        if header["e_type"] == "ET_DYN":
            warnings.warn(
                f"File '{file_path}' is ET_DYN (Position Independent Executable). "
                "Only ET_EXEC files are fully supported. Results may be inaccurate.",
                UserWarning,
                stacklevel=3,
            )
            raise UnsupportedElfTypeError(
                f"File '{file_path}' is ET_DYN. Only ET_EXEC files are supported."
            )

        if header["e_type"] != "ET_EXEC":
            raise UnsupportedElfTypeError(
                f"Unsupported ELF type: {header['e_type']}. Only ET_EXEC is supported."
            )

        entry_point = header.e_entry

        for segment in elf.iter_segments():
            if segment["p_type"] != "PT_LOAD":
                continue
            if segment["p_filesz"] != segment["p_memsz"]:
                continue
            flags = segment["p_flags"]
            if (flags & P_FLAGS.PF_R) and (flags & P_FLAGS.PF_X):
                return {
                    "header_size": header_size,
                    "phdr_entry_size": header.e_phentsize,
                    "phdr_count": header.e_phnum,
                    "phdr_offset": header.e_phoff,
                    "entry_point": entry_point,
                    "segment_vaddr": segment["p_vaddr"],
                    "segment_size": segment["p_filesz"],
                    "is_64bit": is_64bit,
                }

        raise NoLoadSegmentError("No suitable PT_LOAD segment found")

    except ELFError as e:
        raise InvalidElfError(f"Invalid ELF file: {e}") from e


def _get_section_names_from_original(original_path: Path) -> list[str]:
    """Get section names from original ELF file for block naming.

    Args:
        original_path: Path to the original ELF file.

    Returns:
        List of inferred segment names ('code', 'data', or section name).
    """
    try:
        with open(original_path, "rb") as f:
            elf_file = ELFFile(f)
            section_names = []

            for segment in elf_file.iter_segments():
                if segment["p_type"] != "PT_LOAD":
                    continue

                names_in_segment = []
                for section in elf_file.iter_sections():
                    sh_addr = section["sh_addr"]
                    p_vaddr = segment["p_vaddr"]
                    p_memsz = segment["p_memsz"]
                    sh_size = section["sh_size"]

                    if (
                        sh_addr >= p_vaddr
                        and sh_addr < p_vaddr + p_memsz
                        and sh_size > 0
                    ):
                        names_in_segment.append(section.name)

                if not names_in_segment:
                    continue

                if any(".text" in name for name in names_in_segment):
                    section_names.append("code")
                elif any(".data" in name for name in names_in_segment):
                    section_names.append("data")
                else:
                    section_names.append(names_in_segment[0].lstrip("."))

            return section_names

    except (ELFError, OSError):
        return []


def _parse_block_header(data: bytes, offset: int, endian_char: str) -> BlockInfo | None:
    """Parse a 12-byte UPX block header (b_info structure).

    Args:
        data: Raw data containing the header.
        offset: Offset to start parsing from.
        endian_char: Endianness indicator ('<' for little, '>' for big).

    Returns:
        BlockInfo or None if parsing fails.
    """
    if len(data) < offset + _UPX_INFO_SIZE:
        return None

    header_data = data[offset : offset + _UPX_INFO_SIZE]
    try:
        sz_unc, sz_cpr = struct.unpack(f"{endian_char}II", header_data[:8])
        b_method, b_ftid, b_cto8, b_unused = struct.unpack("BBBB", header_data[8:12])

        return BlockInfo(
            uncompressed_size=sz_unc,
            compressed_size=sz_cpr,
            method=b_method,
            filter_id=b_ftid,
            cto8=b_cto8,
            unused=b_unused,
        )
    except struct.error:
        return None


def _split_compressed_data(
    data: bytes,
    base_addr: int,
    endian_char: str,
    section_names: list[str],
) -> tuple[list[CompressedBlock], ByteSection | None]:
    """Split compressed data into individual blocks.

    Args:
        data: Compressed data to split.
        base_addr: Base address for the data.
        endian_char: Endianness indicator.
        section_names: List of inferred section names from original file.

    Returns:
        Tuple of (list of CompressedBlock, optional displacement section).
    """
    if not data:
        return [], None

    blocks = []
    offset = 0
    block_index = 0

    while offset < len(data):
        block_info = _parse_block_header(data, offset, endian_char)
        if block_info is None:
            break

        compressed_data_start = offset + _UPX_INFO_SIZE
        compressed_data_end = compressed_data_start + block_info.compressed_size

        if compressed_data_end > len(data):
            break

        if block_index == 0:
            inferred_segment = "header"
        elif block_index - 1 < len(section_names):
            inferred_segment = section_names[block_index - 1]
        else:
            inferred_segment = None

        if inferred_segment:
            header_name = f".b_info_{inferred_segment}"
            data_name = f".block_{inferred_segment}"
        else:
            header_name = f".b_info_{block_index}"
            data_name = f".block_{block_index}"

        header_section = ByteSection(
            address=base_addr + offset,
            data=data[offset:compressed_data_start],
            name=header_name,
        )

        data_section = ByteSection(
            address=base_addr + compressed_data_start,
            data=data[compressed_data_start:compressed_data_end],
            name=data_name,
        )

        blocks.append(
            CompressedBlock(
                index=block_index,
                block_info=block_info,
                header_section=header_section,
                data_section=data_section,
                inferred_segment=inferred_segment,
            )
        )

        offset = compressed_data_end
        block_index += 1

        if offset + _UPX_INFO_SIZE > len(data):
            break

    displacement = None
    if offset < len(data):
        remainder = data[offset:]
        if len(remainder) > 0:
            displacement = ByteSection(
                address=base_addr + offset,
                data=remainder,
                name=".displacement",
            )

    return blocks, displacement
