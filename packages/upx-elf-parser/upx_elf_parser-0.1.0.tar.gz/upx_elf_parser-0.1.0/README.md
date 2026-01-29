# upx-elf-parser

A Python library for parsing UPX-packed ELF files.

[![PyPI version](https://badge.fury.io/py/upx-elf-parser.svg)](https://badge.fury.io/py/upx-elf-parser)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

`upx-elf-parser` extracts and analyzes the internal structure of UPX-packed ELF executables. It parses the packed binary and separates it into its components:

- ELF Header
- Program Headers
- UPX l_info structure
- UPX p_info structure
- Compressed blocks (with b_info headers)
- Loader code
- Displacement data (if present)

This is useful for malware analysis, reverse engineering, and security research involving packed Linux binaries.

## Installation

### Using uv (recommended)

```bash
uv add upx-elf-parser
```

### Using pip

```bash
pip install upx-elf-parser
```

### From source

```bash
git clone https://github.com/bolin8017/upx-elf-parser.git
cd upx-elf-parser
uv sync
```

## Quick Start

### As a Library

```python
from upx_elf_parser import parse_upx_elf

# Parse a UPX-packed ELF file
result = parse_upx_elf("packed_binary")

# Access parsed components
print(f"Entry point: 0x{result.entry_point:x}")
print(f"Compression ratio: {result.compression_ratio:.2%}")
print(f"Number of compressed blocks: {len(result.compressed_blocks)}")

# Iterate over compressed blocks
for block in result.compressed_blocks:
    print(f"  {block.header_section.name}: "
          f"{block.block_info.compressed_size} -> "
          f"{block.block_info.uncompressed_size} bytes")

# Access raw data
print(f"Loader size: {len(result.loader)} bytes")
```

### With Original File (for better section naming)

If you have access to the original unpacked binary, you can provide it for more accurate section naming:

```python
result = parse_upx_elf("packed_binary", original_path="original_binary")

# Blocks will be named based on original segments:
# .b_info_header, .block_header
# .b_info_code, .block_code
# .b_info_data, .block_data
```

### Command Line Interface

```bash
# Basic usage - output JSON to stdout
upx-elf-parser packed_binary

# Save to file
upx-elf-parser packed_binary --output result.json

# With original file for better naming
upx-elf-parser packed_binary --original original_binary

# Exclude raw hex data (smaller output)
upx-elf-parser packed_binary --no-data

# Custom indentation
upx-elf-parser packed_binary --indent 4
```

## Output Structure

The parser returns an `UpxElfInfo` object with the following structure:

```python
@dataclass
class UpxElfInfo:
    file_path: str           # Path to parsed file
    is_64bit: bool           # True for 64-bit ELF
    endianness: str          # 'little' or 'big'
    entry_point: int         # Entry point address
    elf_header: ByteSection  # ELF header
    program_headers: ByteSection
    l_info: LInfo            # UPX loader info
    p_info: PInfo            # UPX program info
    compressed_blocks: list[CompressedBlock]
    loader: ByteSection      # Decompression stub
    displacement: ByteSection | None  # Remaining bytes
```

### JSON Output Example

```json
{
  "file_path": "packed_binary",
  "is_64bit": true,
  "endianness": "little",
  "entry_point": 4198400,
  "compression_ratio": 0.35,
  "elf_header": {
    "name": ".elf_header",
    "address": 0,
    "size": 64
  },
  "compressed_blocks": [
    {
      "index": 0,
      "inferred_segment": "header",
      "block_info": {
        "uncompressed_size": 4096,
        "compressed_size": 1024,
        "method": 14,
        "filter_id": 0
      }
    }
  ]
}
```

## Supported Files

- **ELF Type**: ET_EXEC (static executables)
- **Architecture**: 32-bit and 64-bit
- **Endianness**: Little-endian and big-endian
- **UPX Version**: Tested with UPX 3.x and 4.x

**Note**: ET_DYN (Position Independent Executables / PIE) files are not supported and will raise `UnsupportedElfTypeError`.

## Error Handling

```python
from upx_elf_parser import (
    parse_upx_elf,
    InvalidElfError,
    UnsupportedElfTypeError,
    InvalidUpxStructureError,
    NoLoadSegmentError,
)

try:
    result = parse_upx_elf("some_file")
except FileNotFoundError:
    print("File not found")
except InvalidElfError:
    print("Not a valid ELF file")
except UnsupportedElfTypeError:
    print("Only ET_EXEC files are supported")
except InvalidUpxStructureError:
    print("Could not parse UPX structure")
except NoLoadSegmentError:
    print("No suitable PT_LOAD segment found")
```

## Development

### Setup

```bash
git clone https://github.com/bolin8017/upx-elf-parser.git
cd upx-elf-parser
uv sync --all-extras
```

### Run Tests

```bash
uv run pytest
```

### Lint and Format

```bash
uv run ruff check src tests
uv run ruff format src tests
```

### Type Check

```bash
uv run mypy src
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## References

- [UPX - the Ultimate Packer for eXecutables](https://upx.github.io/)
- [ELF Specification](https://refspecs.linuxfoundation.org/elf/elf.pdf)
- [UPX Source Code](https://github.com/upx/upx)
