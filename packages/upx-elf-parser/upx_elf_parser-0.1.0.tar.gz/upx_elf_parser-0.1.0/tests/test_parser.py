"""Tests for the UPX ELF parser."""

import pytest

from upx_elf_parser import (
    ByteSection,
    InvalidElfError,
    parse_upx_elf,
)
from upx_elf_parser.models import BlockInfo
from upx_elf_parser.parser import _detect_endianness, _parse_block_header


class TestDetectEndianness:
    """Tests for endianness detection."""

    def test_little_endian(self):
        """Test detection of little-endian ELF."""
        # EI_DATA = 1 (ELFDATA2LSB)
        data = b"\x7fELF\x02\x01"
        assert _detect_endianness(data) == "little"

    def test_big_endian(self):
        """Test detection of big-endian ELF."""
        # EI_DATA = 2 (ELFDATA2MSB)
        data = b"\x7fELF\x02\x02"
        assert _detect_endianness(data) == "big"

    def test_short_data(self):
        """Test with data too short to determine endianness."""
        data = b"\x7fELF"
        assert _detect_endianness(data) == "little"

    def test_invalid_data(self):
        """Test with non-ELF data."""
        data = b"NOT_ELF_DATA"
        assert _detect_endianness(data) == "little"


class TestParseBlockHeader:
    """Tests for block header parsing."""

    def test_valid_little_endian(self):
        """Test parsing a valid little-endian block header."""
        # sz_unc=4096, sz_cpr=1024, method=14, ftid=0, cto8=0, unused=0
        data = bytes(
            [
                0x00,
                0x10,
                0x00,
                0x00,  # sz_unc = 4096
                0x00,
                0x04,
                0x00,
                0x00,  # sz_cpr = 1024
                0x0E,
                0x00,
                0x00,
                0x00,  # method=14, ftid=0, cto8=0, unused=0
            ]
        )
        result = _parse_block_header(data, 0, "<")

        assert result is not None
        assert isinstance(result, BlockInfo)
        assert result.uncompressed_size == 4096
        assert result.compressed_size == 1024
        assert result.method == 14
        assert result.filter_id == 0

    def test_valid_big_endian(self):
        """Test parsing a valid big-endian block header."""
        # sz_unc=4096, sz_cpr=1024
        data = bytes(
            [
                0x00,
                0x00,
                0x10,
                0x00,  # sz_unc = 4096 (big-endian)
                0x00,
                0x00,
                0x04,
                0x00,  # sz_cpr = 1024 (big-endian)
                0x0E,
                0x00,
                0x00,
                0x00,  # method=14, ftid=0, cto8=0, unused=0
            ]
        )
        result = _parse_block_header(data, 0, ">")

        assert result is not None
        assert result.uncompressed_size == 4096
        assert result.compressed_size == 1024

    def test_insufficient_data(self):
        """Test with insufficient data."""
        data = b"\x00\x10\x00\x00"  # Only 4 bytes
        result = _parse_block_header(data, 0, "<")
        assert result is None

    def test_with_offset(self):
        """Test parsing at a non-zero offset."""
        prefix = b"\x00" * 10
        header = bytes(
            [
                0x00,
                0x10,
                0x00,
                0x00,
                0x00,
                0x04,
                0x00,
                0x00,
                0x0E,
                0x00,
                0x00,
                0x00,
            ]
        )
        data = prefix + header
        result = _parse_block_header(data, 10, "<")

        assert result is not None
        assert result.uncompressed_size == 4096


class TestParseUpxElfErrors:
    """Tests for error handling in parse_upx_elf."""

    def test_file_not_found(self, tmp_path):
        """Test FileNotFoundError for non-existent file."""
        with pytest.raises(FileNotFoundError):
            parse_upx_elf(tmp_path / "nonexistent")

    def test_file_too_small(self, tmp_path):
        """Test InvalidElfError for file too small."""
        small_file = tmp_path / "small"
        small_file.write_bytes(b"\x7fELF" + b"\x00" * 10)

        with pytest.raises(InvalidElfError, match="too small"):
            parse_upx_elf(small_file)

    def test_not_elf_magic(self, tmp_path):
        """Test InvalidElfError for non-ELF file."""
        not_elf = tmp_path / "not_elf"
        not_elf.write_bytes(b"NOT_ELF" + b"\x00" * 100)

        with pytest.raises(InvalidElfError, match="magic"):
            parse_upx_elf(not_elf)


class TestByteSection:
    """Tests for ByteSection dataclass."""

    def test_len(self):
        """Test __len__ method."""
        section = ByteSection(
            address=0,
            data=b"\x00\x01\x02\x03",
            name=".test",
        )
        assert len(section) == 4

    def test_frozen(self):
        """Test that ByteSection is immutable."""
        section = ByteSection(
            address=0,
            data=b"\x00",
            name=".test",
        )
        with pytest.raises(AttributeError):
            section.address = 100


class TestUpxElfInfo:
    """Tests for UpxElfInfo dataclass."""

    def test_to_dict(self):
        """Test to_dict method produces valid JSON-serializable output."""
        from upx_elf_parser.models import LInfo, PInfo, UpxElfInfo

        info = UpxElfInfo(
            file_path="test",
            is_64bit=True,
            endianness="little",
            entry_point=0x1000,
            elf_header=ByteSection(0, b"\x7fELF", ".elf_header"),
            program_headers=ByteSection(64, b"\x00" * 56, ".program_headers"),
            l_info=LInfo(ByteSection(120, b"\x00" * 12, ".l_info")),
            p_info=PInfo(ByteSection(132, b"\x00" * 12, ".p_info")),
            compressed_blocks=[],
            loader=ByteSection(144, b"\x00" * 100, ".loader"),
        )

        result = info.to_dict()

        assert result["file_path"] == "test"
        assert result["is_64bit"] is True
        assert result["entry_point"] == 0x1000
        assert "elf_header" in result
        assert result["elf_header"]["name"] == ".elf_header"

    def test_compression_ratio_zero_division(self):
        """Test compression_ratio with zero uncompressed size."""
        from upx_elf_parser.models import LInfo, PInfo, UpxElfInfo

        info = UpxElfInfo(
            file_path="test",
            is_64bit=True,
            endianness="little",
            entry_point=0x1000,
            elf_header=ByteSection(0, b"\x7fELF", ".elf_header"),
            program_headers=ByteSection(64, b"\x00" * 56, ".program_headers"),
            l_info=LInfo(ByteSection(120, b"\x00" * 12, ".l_info")),
            p_info=PInfo(ByteSection(132, b"\x00" * 12, ".p_info")),
            compressed_blocks=[],
            loader=None,
        )

        assert info.compression_ratio == 0.0
