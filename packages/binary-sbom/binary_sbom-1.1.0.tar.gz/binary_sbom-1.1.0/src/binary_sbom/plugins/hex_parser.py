"""
Intel HEX Parser Plugin for Binary SBOM Generator.

This plugin provides parsing capabilities for Intel HEX format files (.hex) commonly
used in embedded systems and microcontroller firmware development.

The Intel HEX format is a text-based representation of binary data that encodes
binary data as ASCII hexadecimal values. Each line (record) in the file represents
a specific type of data or control information.

Record Types:
- Data Record (0x00): Contains actual data/code
- End of File Record (0x01): Marks the end of the file
- Extended Segment Address Record (0x02): Specifies upper 16 bits of address
- Start Segment Address Record (0x03): Specifies starting execution address
- Extended Linear Address Record (0x04): Specifies upper 16 bits of 32-bit address
- Start Linear Address Record (0x05): Specifies starting execution address (32-bit)

This plugin validates Intel HEX format checksums and extracts metadata including
start address, end address, data segment information, and record counts.
"""

from pathlib import Path
from typing import Dict, Any, List
import re

from binary_sbom.plugins.api import BinaryParserPlugin


class HexParser(BinaryParserPlugin):
    """Parser for Intel HEX format files (.hex).

    This plugin handles Intel HEX format files commonly used in embedded systems
    development and microcontroller programming. The format encodes binary data
    as ASCII hexadecimal values with each line representing a record.

    Intel HEX Format Structure:
    - Start code: ':' (colon, ASCII 0x3A)
    - Byte count: 1 hex byte (number of data bytes in record)
    - Address: 2 hex bytes (16-bit or 32-bit depending on record type)
    - Record type: 1 hex byte (0x00-0x05)
    - Data: 0-255 hex bytes (payload)
    - Checksum: 1 hex byte (two's complement of sum of all preceding bytes)

    The plugin validates:
    - Line format (all lines must start with ':')
    - Checksum validation for all records
    - Record type validation
    - Address range and data segment information

    Example:
        >>> from pathlib import Path
        >>> from binary_sbom.plugins.hex_parser import HexParser
        >>>
        >>> parser = HexParser()
        >>> metadata = parser.parse(Path('/path/to/firmware.hex'))
        >>> print(metadata['packages'][0]['startAddress'])
        '0x0000'
        >>> print(metadata['packages'][0]['endAddress'])
        '0x3FFF'
    """

    # Intel HEX record types
    RECORD_DATA = 0x00
    RECORD_EOF = 0x01
    RECORD_EXTENDED_SEGMENT_ADDR = 0x02
    RECORD_START_SEGMENT_ADDR = 0x03
    RECORD_EXTENDED_LINEAR_ADDR = 0x04
    RECORD_START_LINEAR_ADDR = 0x05

    # Regular expression for Intel HEX line validation
    # Format: :LLAAAATTDDDD...CC
    # LL = byte count, AAAA = address, TT = type, DD = data, CC = checksum
    HEX_LINE_PATTERN = re.compile(r'^:([0-9A-Fa-f]{2})([0-9A-Fa-f]{4})([0-9A-Fa-f]{2})([0-9A-Fa-f]*)([0-9A-Fa-f]{2})$')

    def get_name(self) -> str:
        """Return unique plugin name.

        Returns:
            "HexParser" as the unique identifier for this plugin.
        """
        return "HexParser"

    def get_supported_formats(self) -> List[str]:
        """Return list of supported file extensions.

        Returns:
            List containing '.hex' extension.
        """
        return ['.hex']

    def can_parse(self, file_path: Path) -> bool:
        """Check if this plugin can parse the given file.

        This method performs a fast check to determine if the file is in Intel HEX
        format by verifying:
        1. File extension is .hex (fast check)
        2. File exists and is readable
        3. File contains lines starting with ':' (Intel HEX format marker)

        Args:
            file_path: Path to the binary file to check.

        Returns:
            True if the file appears to be in Intel HEX format, False otherwise.
        """
        # Fast extension check first
        if file_path.suffix.lower() != '.hex':
            return False

        # Verify file exists
        if not file_path.exists() or not file_path.is_file():
            return False

        # Validate content - check for Intel HEX format marker
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Read first line and check if it starts with ':'
                first_line = f.readline().strip()
                if not first_line.startswith(':'):
                    return False

                # Validate first line format with regex
                match = self.HEX_LINE_PATTERN.match(first_line)
                if not match:
                    return False

                # Verify byte count matches data length
                byte_count = int(match.group(1), 16)
                data_hex = match.group(4)
                if len(data_hex) != byte_count * 2:
                    return False

            return True

        except (OSError, IOError, UnicodeDecodeError):
            return False

    def parse(self, file_path: Path) -> Dict[str, Any]:
        """Parse Intel HEX file and return metadata dictionary.

        This method parses an Intel HEX format file and extracts metadata including:
        - Address range (start and end addresses)
        - Data segment count
        - Record type statistics
        - Checksum validation status

        Args:
            file_path: Path to the Intel HEX file to parse.

        Returns:
            Dictionary with 'packages', 'relationships', and 'annotations' keys.

        Raises:
            FileNotFoundError: If file doesn't exist.
            ValueError: If file format is invalid or checksums fail.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Intel HEX file not found: {file_path}")

        try:
            # Parse all records from the file
            records = []
            line_number = 0
            checksum_errors = []

            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line_number += 1
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Validate and parse the line
                    try:
                        record = self._parse_line(line, line_number)
                        if record:
                            records.append(record)
                    except ValueError as e:
                        checksum_errors.append(f"Line {line_number}: {e}")

            # Raise error if there were checksum failures
            if checksum_errors:
                raise ValueError(f"Checksum validation failed:\n" + "\n".join(checksum_errors))

            # Extract metadata from parsed records
            metadata = self._extract_metadata(records)

            # Create firmware package
            firmware_package = {
                'name': file_path.stem,
                'type': 'firmware',
                'format': 'Intel HEX',
                'startAddress': f"0x{metadata['start_addr']:04X}" if metadata['start_addr'] is not None else 'unknown',
                'endAddress': f"0x{metadata['end_addr']:04X}" if metadata['end_addr'] is not None else 'unknown',
                'dataSegments': metadata['data_segments'],
                'description': f'Intel HEX firmware, address range 0x{metadata["start_addr"]:04X}-0x{metadata["end_addr"]:04X}' if metadata['start_addr'] is not None else 'Intel HEX firmware',
                'spdx_id': 'SPDXRef-firmware',
                'download_location': 'NOASSERTION',
            }

            packages = [firmware_package]
            relationships = []
            annotations = []

            # Add parsing annotation with statistics
            annotation_text = (
                f'Parsed by {self.get_name()} v{self.version}. '
                f'Total records: {metadata["total_records"]}, '
                f'Data records: {metadata["data_records"]}, '
                f'Address range: 0x{metadata["start_addr"]:04X}-0x{metadata["end_addr"]:04X}, '
                f'Checksums validated successfully'
            )

            annotations.append({
                'spdx_id': 'SPDXRef-firmware',
                'type': 'OTHER',
                'text': annotation_text
            })

            return {
                'packages': packages,
                'relationships': relationships,
                'annotations': annotations
            }

        except (OSError, IOError) as e:
            raise ValueError(f"Error reading Intel HEX file: {e}")
        except Exception as e:
            raise ValueError(f"Failed to parse Intel HEX file: {e}")

    def _parse_line(self, line: str, line_number: int) -> Dict[str, Any]:
        """Parse a single Intel HEX record line.

        Args:
            line: Text line from Intel HEX file.
            line_number: Line number for error reporting.

        Returns:
            Dictionary containing record information.

        Raises:
            ValueError: If line format is invalid or checksum fails.
        """
        # Validate line format with regex
        match = self.HEX_LINE_PATTERN.match(line)
        if not match:
            raise ValueError(f"Invalid Intel HEX line format: '{line}'")

        byte_count_hex = match.group(1)
        address_hex = match.group(2)
        record_type_hex = match.group(3)
        data_hex = match.group(4)
        checksum_hex = match.group(5)

        # Parse fields
        byte_count = int(byte_count_hex, 16)
        address = int(address_hex, 16)
        record_type = int(record_type_hex, 16)
        checksum_expected = int(checksum_hex, 16)

        # Validate byte count matches data length
        if len(data_hex) != byte_count * 2:
            raise ValueError(f"Byte count ({byte_count}) doesn't match data length ({len(data_hex) // 2})")

        # Parse data bytes
        data = []
        for i in range(0, len(data_hex), 2):
            data.append(int(data_hex[i:i+2], 16))

        # Calculate and verify checksum
        # Checksum is two's complement of sum of all bytes (excluding start code ':')
        checksum_calculated = (byte_count + (address >> 8) + (address & 0xFF) +
                              record_type + sum(data)) & 0xFF
        checksum_calculated = ((~checksum_calculated) + 1) & 0xFF

        if checksum_calculated != checksum_expected:
            raise ValueError(
                f"Checksum mismatch: expected 0x{checksum_expected:02X}, "
                f"calculated 0x{checksum_calculated:02X}"
            )

        return {
            'byte_count': byte_count,
            'address': address,
            'record_type': record_type,
            'data': data,
            'line_number': line_number
        }

    def _extract_metadata(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract metadata from parsed records.

        Args:
            records: List of parsed record dictionaries.

        Returns:
            Dictionary containing metadata including start address, end address,
            and record counts.
        """
        # Initialize metadata
        metadata = {
            'start_addr': None,
            'end_addr': None,
            'data_segments': 0,
            'total_records': len(records),
            'data_records': 0,
            'extended_linear_addr': 0,
            'extended_segment_addr': 0,
        }

        current_segment_start = None
        current_segment_end = None

        for record in records:
            record_type = record['record_type']
            address = record['address']
            data = record['data']

            if record_type == self.RECORD_DATA:
                # Data record - update address range
                metadata['data_records'] += 1

                # Apply extended address if set
                if metadata['extended_linear_addr'] > 0:
                    full_address = (metadata['extended_linear_addr'] << 16) | address
                else:
                    full_address = address

                # Update start address
                if metadata['start_addr'] is None or full_address < metadata['start_addr']:
                    metadata['start_addr'] = full_address

                # Update end address
                data_end = full_address + len(data) - 1
                if metadata['end_addr'] is None or data_end > metadata['end_addr']:
                    metadata['end_addr'] = data_end

                # Track segment information
                if current_segment_start is None:
                    current_segment_start = full_address
                    current_segment_end = data_end
                elif full_address == current_segment_end + 1:
                    # Continuous data
                    current_segment_end = data_end
                else:
                    # Gap detected - new segment
                    metadata['data_segments'] += 1
                    current_segment_start = full_address
                    current_segment_end = data_end

            elif record_type == self.RECORD_EXTENDED_LINEAR_ADDR:
                # Extended Linear Address record (sets upper 16 bits of 32-bit address)
                if len(data) >= 2:
                    metadata['extended_linear_addr'] = (data[0] << 8) | data[1]

            elif record_type == self.RECORD_EXTENDED_SEGMENT_ADDR:
                # Extended Segment Address record
                if len(data) >= 2:
                    metadata['extended_segment_addr'] = (data[0] << 8) | data[1]

            elif record_type == self.RECORD_EOF:
                # End of File record
                pass

        # Count the last segment if we had data
        if current_segment_start is not None:
            metadata['data_segments'] += 1

        return metadata

    @property
    def version(self) -> str:
        """Plugin version string.

        Returns:
            "1.0.0" as the initial version of this plugin.
        """
        return "1.0.0"
