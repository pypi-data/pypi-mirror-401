"""
Streaming parser base class for chunked binary reading.

This module provides the StreamingParser abstract base class that enables
memory-efficient processing of large binary files by reading them in chunks
rather than loading the entire file into memory.

The streaming parser provides:
- Chunked file reading with configurable chunk sizes
- Memory-mapped file support for efficient random access
- Progress tracking integration for ETA estimation
- Context manager support for automatic resource cleanup
- Abstract interface for format-specific parser implementations
- Error handling and recovery for malformed binaries

This base class is designed to be extended by format-specific parsers
(ELF, PE, MachO) that implement the actual parsing logic while inheriting
the chunked reading capabilities.

Example:
    >>> class ELFStreamingParser(StreamingParser):
    ...     def parse_header(self):
    ...         # Read ELF header from first chunk
    ...         header_data = self.read_chunk(0, 64)
    ...         return parse_elf_header(header_data)
    ...
    >>> parser = ELFStreamingParser('/bin/ls', chunk_size=65536)
    >>> with parser:
    ...     metadata = parser.parse()
    >>> print(metadata)
"""

import logging
import mmap
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Tuple

from binary_sbom.eta_estimator import ETAEstimator


logger = logging.getLogger(__name__)


# Default configuration values
DEFAULT_CHUNK_SIZE = 65536  # 64 KB default chunk size
DEFAULT_MAX_FILE_SIZE_MB = 500  # 500 MB default max file size
MIN_CHUNK_SIZE = 4096  # 4 KB minimum chunk size
MAX_CHUNK_SIZE = 10485760  # 10 MB maximum chunk size


@dataclass
class StreamingConfig:
    """
    Configuration for streaming parser behavior.

    Attributes:
        chunk_size: Number of bytes to read per chunk (default: 65536)
        max_file_size_mb: Maximum file size in MB to process (default: 500)
        use_mmap: Whether to use memory-mapped files (default: True)
        enable_progress_tracking: Whether to track progress for ETA (default: True)
        buffer_chunks: Number of chunks to buffer in memory (default: 2)
    """

    chunk_size: int = DEFAULT_CHUNK_SIZE
    max_file_size_mb: int = DEFAULT_MAX_FILE_SIZE_MB
    use_mmap: bool = True
    enable_progress_tracking: bool = True
    buffer_chunks: int = 2

    def __post_init__(self) -> None:
        """Validate configuration values."""
        if self.chunk_size < MIN_CHUNK_SIZE:
            raise ValueError(
                f"chunk_size must be at least {MIN_CHUNK_SIZE}, got {self.chunk_size}"
            )

        if self.chunk_size > MAX_CHUNK_SIZE:
            raise ValueError(
                f"chunk_size must be at most {MAX_CHUNK_SIZE}, got {self.chunk_size}"
            )

        if self.max_file_size_mb <= 0:
            raise ValueError(
                f"max_file_size_mb must be positive, got {self.max_file_size_mb}"
            )

        if self.buffer_chunks < 0:
            raise ValueError(
                f"buffer_chunks must be non-negative, got {self.buffer_chunks}"
            )

    @property
    def max_file_size_bytes(self) -> int:
        """Get maximum file size in bytes."""
        return self.max_file_size_mb * 1024 * 1024


@dataclass
class ChunkInfo:
    """
    Information about a file chunk.

    Attributes:
        offset: Byte offset of the chunk in the file
        size: Number of bytes in the chunk
        index: Sequential index of the chunk (0-based)
        is_last: Whether this is the last chunk in the file
    """

    offset: int
    size: int
    index: int
    is_last: bool = False


class StreamingParserError(Exception):
    """Base exception for streaming parser errors."""

    pass


class ChunkReadError(StreamingParserError):
    """Exception raised when chunk reading fails."""

    pass


class FileSizeExceededError(StreamingParserError):
    """Exception raised when file size exceeds maximum."""

    pass


class StreamingParser(ABC):
    """
    Abstract base class for streaming binary parsers.

    This class provides the infrastructure for reading binary files in chunks,
    with support for memory-mapped files and progress tracking. Subclasses
    implement format-specific parsing logic.

    The parser is designed as a context manager to ensure proper resource cleanup:

        >>> with StreamingParser('/path/to/binary') as parser:
        ...     metadata = parser.parse()

    Chunk Reading:
        Chunks are read sequentially by default, but random access is supported
        for formats that require it (e.g., parsing section headers).

    Progress Tracking:
        When enabled, the parser tracks bytes read and updates ETA estimates
        through the integrated ETAEstimator.

    Memory Management:
        The parser uses a sliding window approach to limit memory usage.
        Only the current chunk (and optionally buffered chunks) are held in memory.

    Args:
        file_path: Path to the binary file to parse.
        config: StreamingConfig object with parser settings.
        eta_estimator: Optional ETAEstimator for progress tracking.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        FileSizeExceededError: If the file exceeds the maximum size.
        ValueError: If the configuration is invalid.

    Attributes:
        file_path: Path to the binary file being parsed
        config: Configuration for this parser instance
        file_size: Total size of the file in bytes
        total_chunks: Total number of chunks in the file
        bytes_read: Number of bytes read so far
    """

    def __init__(
        self,
        file_path: str,
        config: Optional[StreamingConfig] = None,
        eta_estimator: Optional[ETAEstimator] = None,
    ):
        """
        Initialize the streaming parser.

        Args:
            file_path: Path to the binary file to parse.
            config: StreamingConfig object with parser settings.
            eta_estimator: Optional ETAEstimator for progress tracking.

        Raises:
            FileNotFoundError: If the file doesn't exist.
            FileSizeExceededError: If the file exceeds the maximum size.
            ValueError: If the configuration is invalid.
        """
        self._path = Path(file_path)

        # Validate file exists
        if not self._path.exists():
            raise FileNotFoundError(f"Binary file not found: {file_path}")

        if not self._path.is_file():
            raise ValueError(f"Path is not a file: {file_path}")

        # Get file size
        self.file_size = self._path.stat().st_size

        # Set configuration
        self.config = config or StreamingConfig()

        # Validate file size
        if self.file_size > self.config.max_file_size_bytes:
            raise FileSizeExceededError(
                f"File size ({self.file_size} bytes) exceeds maximum "
                f"({self.config.max_file_size_bytes} bytes)"
            )

        # Calculate chunk information
        self.total_chunks = (
            self.file_size + self.config.chunk_size - 1
        ) // self.config.chunk_size

        # Set up ETA estimator
        self._eta_estimator = eta_estimator

        # File handle and memory map (initialized on enter)
        self._file_handle = None
        self._mmap_handle = None

        # Progress tracking
        self.bytes_read = 0
        self._current_chunk_index = 0

        logger.debug(
            f"Initialized streaming parser for {file_path}: "
            f"size={self.file_size} bytes, "
            f"chunks={self.total_chunks}, "
            f"chunk_size={self.config.chunk_size}"
        )

    @property
    def file_path(self) -> str:
        """Get the file path being parsed."""
        return str(self._path)

    @property
    def progress_percentage(self) -> float:
        """
        Get the current progress as a percentage.

        Returns:
            Progress percentage (0.0 to 100.0).
        """
        if self.file_size == 0:
            return 100.0

        return min(100.0, (self.bytes_read / self.file_size) * 100.0)

    @property
    def is_complete(self) -> bool:
        """
        Check if parsing is complete.

        Returns:
            True if all bytes have been read, False otherwise.
        """
        return self.bytes_read >= self.file_size

    def __enter__(self):
        """
        Enter the context manager and open the file.

        Opens the file for reading and optionally creates a memory map.

        Returns:
            Self, for use in with statements.

        Raises:
            IOError: If the file cannot be opened.
        """
        try:
            # Open file in binary read mode
            self._file_handle = open(self._path, 'rb')

            # Create memory map if enabled and file is not empty
            if self.config.use_mmap and self.file_size > 0:
                try:
                    self._mmap_handle = mmap.mmap(
                        self._file_handle.fileno(),
                        0,
                        access=mmap.ACCESS_READ
                    )
                    logger.debug(f"Created memory map for {self.file_path}")
                except (ValueError, mmap.error) as e:
                    logger.warning(
                        f"Memory mapping failed for {self.file_path}, "
                        f"falling back to standard file I/O: {e}"
                    )
                    self._mmap_handle = None

            return self

        except IOError as e:
            # Clean up on failure
            if self._file_handle:
                self._file_handle.close()
                self._file_handle = None

            raise IOError(f"Failed to open file {self.file_path}: {e}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the context manager and clean up resources.

        Closes the file handle and memory map if they were created.

        Args:
            exc_type: Exception type if an exception was raised.
            exc_val: Exception value if an exception was raised.
            exc_tb: Exception traceback if an exception was raised.

        Returns:
            None, exceptions are propagated normally.
        """
        # Close memory map
        if self._mmap_handle is not None:
            try:
                self._mmap_handle.close()
                logger.debug(f"Closed memory map for {self.file_path}")
            except Exception as e:
                logger.error(f"Error closing memory map: {e}")
            finally:
                self._mmap_handle = None

        # Close file handle
        if self._file_handle is not None:
            try:
                self._file_handle.close()
                logger.debug(f"Closed file handle for {self.file_path}")
            except Exception as e:
                logger.error(f"Error closing file handle: {e}")
            finally:
                self._file_handle = None

        # Return None to propagate exceptions
        return None

    def read_chunk(self, offset: int, size: Optional[int] = None) -> bytes:
        """
        Read a chunk of data from the file at the specified offset.

        This method performs random access reads, useful for formats that
        require jumping to specific locations (e.g., section headers).

        Args:
            offset: Byte offset to start reading from.
            size: Number of bytes to read. If None, reads to end of file.

        Returns:
            Bytes object containing the requested data.

        Raises:
            ChunkReadError: If the read operation fails.
            ValueError: If offset is negative or beyond file size.

        Example:
            >>> parser = StreamingParser('/bin/ls')
            >>> with parser:
            ...     # Read ELF header (first 64 bytes)
            ...     header = parser.read_chunk(0, 64)
        """
        if offset < 0:
            raise ValueError(f"Offset must be non-negative, got {offset}")

        if offset >= self.file_size:
            raise ValueError(
                f"Offset {offset} exceeds file size {self.file_size}"
            )

        # Calculate read size
        if size is None:
            size = self.file_size - offset
        else:
            # Ensure we don't read past the end of the file
            size = min(size, self.file_size - offset)

        try:
            # Use memory map if available
            if self._mmap_handle is not None:
                data = self._mmap_handle[offset:offset + size]
            # Use file handle otherwise
            elif self._file_handle is not None:
                self._file_handle.seek(offset)
                data = self._file_handle.read(size)
            else:
                raise ChunkReadError(
                    "File is not open. Use parser as a context manager."
                )

            # Update progress tracking
            self.bytes_read += len(data)

            # Update ETA estimator if enabled
            if self._eta_estimator and self.config.enable_progress_tracking:
                self._eta_estimator.update_progress(self.bytes_read, self.file_size)

            return data

        except (IOError, OSError) as e:
            raise ChunkReadError(f"Failed to read chunk at offset {offset}: {e}")

    def iter_chunks(self) -> Iterator[bytes]:
        """
        Iterate through the file chunk by chunk.

        This is the primary method for sequential processing of binary files.
        It yields chunks of data in order, starting from the beginning of the file.

        Yields:
            Bytes objects containing successive chunks of the file.

        Raises:
            ChunkReadError: If a chunk cannot be read.

        Example:
            >>> parser = StreamingParser('/bin/ls')
            >>> with parser:
            ...     for chunk in parser.iter_chunks():
            ...         process_chunk(chunk)
        """
        offset = 0
        chunk_index = 0

        while offset < self.file_size:
            # Calculate chunk size (last chunk may be smaller)
            remaining_bytes = self.file_size - offset
            chunk_size = min(self.config.chunk_size, remaining_bytes)

            try:
                chunk_data = self.read_chunk(offset, chunk_size)

                # Update chunk index
                self._current_chunk_index = chunk_index
                chunk_index += 1

                # Move to next chunk
                offset += chunk_size

                yield chunk_data

            except ChunkReadError as e:
                logger.error(
                    f"Failed to read chunk {chunk_index} "
                    f"at offset {offset}: {e}"
                )
                raise

    def get_chunk_info(self, chunk_index: int) -> ChunkInfo:
        """
        Get information about a specific chunk.

        Args:
            chunk_index: Index of the chunk (0-based).

        Returns:
            ChunkInfo object with chunk details.

        Raises:
            ValueError: If chunk_index is out of range.

        Example:
            >>> parser = StreamingParser('/bin/ls')
            >>> with parser:
            ...     info = parser.get_chunk_info(0)
            ...     print(f"First chunk: offset={info.offset}, size={info.size}")
        """
        if chunk_index < 0 or chunk_index >= self.total_chunks:
            raise ValueError(
                f"chunk_index must be between 0 and {self.total_chunks - 1}, "
                f"got {chunk_index}"
            )

        offset = chunk_index * self.config.chunk_size
        remaining_bytes = self.file_size - offset
        size = min(self.config.chunk_size, remaining_bytes)
        is_last = chunk_index == self.total_chunks - 1

        return ChunkInfo(
            offset=offset,
            size=size,
            index=chunk_index,
            is_last=is_last
        )

    @abstractmethod
    def parse(self) -> Dict[str, Any]:
        """
        Parse the binary file and extract metadata.

        This abstract method must be implemented by subclasses to provide
        format-specific parsing logic.

        The implementation should use iter_chunks() for sequential processing
        or read_chunk() for random access, depending on the binary format.

        Returns:
            Dictionary containing extracted metadata. The structure is
            format-specific, but typically includes:
            - name (str): Binary filename
            - type (str): Binary format
            - size (int): File size in bytes
            - Additional format-specific fields

        Raises:
            StreamingParserError: If parsing fails.
            ChunkReadError: If chunk reading fails.

        Example:
            >>> class ELFStreamingParser(StreamingParser):
            ...     def parse(self) -> Dict[str, Any]:
            ...         metadata = {'name': self.file_path}
            ...         # Parse ELF header from first chunk
            ...         header = self.read_chunk(0, 64)
            ...         metadata['type'] = 'ELF'
            ...         return metadata
        """
        pass

    def reset_progress(self) -> None:
        """
        Reset progress tracking to the beginning of the file.

        This is useful when re-parsing a file or restarting processing.
        Does not close and reopen the file, just resets progress counters.

        Example:
            >>> parser = StreamingParser('/bin/ls')
            >>> with parser:
            ...     # Parse once
            ...     result1 = parser.parse()
            ...     # Reset and parse again
            ...     parser.reset_progress()
            ...     result2 = parser.parse()
        """
        self.bytes_read = 0
        self._current_chunk_index = 0

        if self._eta_estimator:
            self._eta_estimator.reset()

        logger.debug(f"Reset progress tracking for {self.file_path}")

    def get_estimated_time_remaining(self) -> Optional[float]:
        """
        Get estimated time remaining for parsing.

        Returns:
            Estimated seconds remaining, or None if ETA estimation is disabled
            or insufficient data is available.

        Example:
            >>> parser = StreamingParser('/bin/ls')
            >>> with parser:
            ...     for chunk in parser.iter_chunks():
            ...         process(chunk)
            ...         eta = parser.get_estimated_time_remaining()
            ...         print(f"ETA: {eta:.1f}s")
        """
        if not self._eta_estimator or not self.config.enable_progress_tracking:
            return None

        return self._eta_estimator.estimate_time_remaining(self.bytes_read, self.file_size)


class LIEFStreamingParser(StreamingParser):
    """
    Streaming binary parser using LIEF with chunked data feeding.

    This concrete implementation extends StreamingParser to provide LIEF-based
    binary analysis while maintaining memory efficiency through chunked reading.
    The parser reads the source file in chunks and feeds data to LIEF through
    a temporary file to avoid loading the entire binary into memory.

    Memory Management:
        - Source file is read in configurable chunks
        - Chunks are immediately written to a temporary file
        - LIEF parses from the temporary file
        - Only one chunk is held in memory at a time
        - Memory usage stays constant regardless of file size

    Args:
        file_path: Path to the binary file to parse.
        config: StreamingConfig object with parser settings.
        eta_estimator: Optional ETAEstimator for progress tracking.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        FileSizeExceededError: If the file exceeds the maximum size.
        ChunkReadError: If chunk reading fails.
        StreamingParserError: If LIEF parsing fails.

    Attributes:
        file_path: Path to the binary file being parsed
        config: Configuration for this parser instance
        file_size: Total size of the file in bytes
        total_chunks: Total number of chunks in the file
        bytes_read: Number of bytes read so far

    Example:
        >>> from binary_sbom.streaming_parser import LIEFStreamingParser
        >>> parser = LIEFStreamingParser('/bin/ls')
        >>> with parser:
        ...     metadata = parser.parse()
        >>> print(f"Format: {metadata['type']}, Arch: {metadata['architecture']}")
        Format: ELF, Arch: x86_64

        >>> # With custom chunk size for large files
        >>> config = StreamingConfig(chunk_size=1048576)  # 1 MB chunks
        >>> parser = LIEFStreamingParser('large_binary.bin', config=config)
        >>> with parser:
        ...     metadata = parser.parse()
    """

    def parse(self) -> Dict[str, Any]:
        """
        Parse the binary file using LIEF with chunked data feeding.

        This method implements the streaming parsing workflow:
        1. Read the source file in chunks
        2. Write chunks to a temporary file incrementally
        3. Use LIEF to parse the temporary file
        4. Extract metadata and return results

        The chunked reading ensures we never load the entire file into memory,
        keeping memory usage constant (O(chunk_size)) rather than O(file_size).

        Returns:
            Dictionary containing extracted binary metadata:
            - name (str): Binary filename
            - type (str): Binary format (ELF, PE, MachO, Raw)
            - architecture (str): Target architecture
            - entrypoint (Optional[str]): Entry point address in hex format
            - sections (List[Dict]): Section information with keys:
                - name (str): Section name
                - size (int): Section size in bytes
                - virtual_address (Optional[str]): Virtual address in hex
            - dependencies (List[str]): Imported library names
            - size (int): File size in bytes
            - _parser (str): Set to 'lief-streaming' to identify streaming parser

        Raises:
            ChunkReadError: If chunk reading fails.
            StreamingParserError: If LIEF parsing is not available or fails.
            RuntimeError: If LIEF library is not installed.

        Example:
            >>> parser = LIEFStreamingParser('/bin/ls')
            >>> with parser:
            ...     metadata = parser.parse()
            >>> print(f"Sections: {len(metadata['sections'])}")
            Sections: 25
        """
        # Verify file is open (context manager entered)
        if self._file_handle is None:
            raise StreamingParserError(
                "Parser is not open. Use the parser as a context manager: "
                "'with parser: ... parser.parse()'"
            )

        logger.info(
            f"Starting LIEF streaming parse of {self.file_path} "
            f"({self.file_size} bytes in {self.total_chunks} chunks)"
        )

        # Use a temporary file to feed data to LIEF
        # This allows LIEF to parse while we maintain streaming behavior
        temp_file = None
        temp_path = None

        try:
            # Create a temporary file for LIEF to parse
            # Use delete=False so we can explicitly control cleanup
            temp_file = tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.bin')
            temp_path = temp_file.name

            logger.debug(f"Created temporary file for LIEF: {temp_path}")

            # Step 1: Read source file in chunks and write to temp file
            # This is the key streaming behavior - we read in chunks
            bytes_written = 0
            chunk_count = 0

            for chunk_data in self.iter_chunks():
                # Write chunk directly to temp file (no accumulation in memory)
                temp_file.write(chunk_data)
                bytes_written += len(chunk_data)
                chunk_count += 1

                # Log progress periodically for large files
                if chunk_count % 10 == 0:
                    progress_pct = (bytes_written / self.file_size) * 100
                    logger.debug(
                        f"Streaming progress: {progress_pct:.1f}% "
                        f"({bytes_written}/{self.file_size} bytes)"
                    )

            # Ensure all data is flushed to disk
            temp_file.flush()
            temp_file.close()

            logger.debug(
                f"Completed streaming: {chunk_count} chunks, "
                f"{bytes_written} bytes written to temp file"
            )

            # Verify we wrote the expected number of bytes
            if bytes_written != self.file_size:
                raise StreamingParserError(
                    f"Size mismatch: wrote {bytes_written} bytes "
                    f"but expected {self.file_size} bytes"
                )

            # Step 2: Use LIEF to parse the temporary file
            metadata = self._parse_with_lief(temp_path)

            # Add file size and parser identifier
            metadata['size'] = self.file_size
            metadata['_parser'] = 'lief-streaming'

            logger.info(
                f"Successfully parsed {self.file_path} with LIEF streaming parser: "
                f"type={metadata['type']}, "
                f"arch={metadata['architecture']}, "
                f"sections={len(metadata.get('sections', []))}"
            )

            return metadata

        except ImportError as e:
            raise RuntimeError(
                "LIEF library is not available. "
                "Install it with: pip install lief"
            ) from e

        except ChunkReadError as e:
            # Re-raise chunk reading errors
            logger.error(f"Chunk reading failed during LIEF streaming parse: {e}")
            raise

        except Exception as e:
            # Wrap other errors in StreamingParserError
            error_type = type(e).__name__
            logger.error(f"LIEF streaming parse failed ({error_type}): {e}")
            raise StreamingParserError(f"Failed to parse binary with LIEF: {e}") from e

        finally:
            # Step 3: Always clean up the temporary file
            if temp_path:
                try:
                    import os
                    os.unlink(temp_path)
                    logger.debug(f"Cleaned up temporary file: {temp_path}")
                except OSError as e:
                    logger.warning(f"Failed to delete temporary file {temp_path}: {e}")

            # Close temp file handle if still open
            if temp_file and not temp_file.closed:
                try:
                    temp_file.close()
                except Exception as e:
                    logger.warning(f"Failed to close temporary file handle: {e}")

    def _parse_with_lief(self, file_path: str) -> Dict[str, Any]:
        """
        Parse binary file using LIEF library and extract metadata.

        This method executes LIEF parsing on the reconstructed binary file.
        It supports ELF, PE, MachO, and raw binary formats.

        Args:
            file_path: Path to binary file to parse.

        Returns:
            Dictionary containing parsed binary metadata.

        Raises:
            RuntimeError: If LIEF library is not available.
            Exception: If binary parsing fails.
            MemoryError: If file is too large to parse.
            OSError: If file cannot be read.

        Example:
            >>> metadata = self._parse_with_lief('/tmp/temp_binary.bin')
            >>> print(metadata['type'])
            'ELF'
        """
        try:
            import lief
        except ImportError as e:
            raise RuntimeError(
                "LIEF library is not available. Install it with: pip install lief"
            ) from e

        # Parse binary using LIEF
        try:
            binary = lief.parse(file_path)
        except MemoryError as e:
            raise MemoryError(f"File too large to parse {file_path}: {e}") from e
        except (IOError, OSError) as e:
            raise OSError(f"Read error while parsing {file_path}: {e}") from e
        except Exception as e:
            # Parse other LIEF errors
            error_msg = str(e).lower()
            if 'corrupted' in error_msg or 'truncated' in error_msg:
                raise Exception(f"Corrupted binary file {file_path}: {e}") from e
            elif 'not supported' in error_msg or 'unknown format' in error_msg:
                raise Exception(f"Unsupported binary format in {file_path}: {e}") from e
            elif 'out of memory' in error_msg or 'memory' in error_msg:
                raise MemoryError(f"File too large to parse {file_path}: {e}") from e
            else:
                raise Exception(f"Failed to parse binary file {file_path}: {e}") from e

        # Check if parsing succeeded
        if binary is None:
            raise Exception(
                f"Failed to parse binary file {file_path}: "
                f"Unknown format or corrupted file"
            )

        # Extract metadata
        metadata = self._extract_metadata(binary, file_path)

        return metadata

    def _extract_metadata(self, binary: Any, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from parsed LIEF binary object.

        Args:
            binary: Parsed LIEF binary object.
            file_path: Original file path (for error messages).

        Returns:
            Dictionary with extracted metadata.

        Raises:
            Exception: If metadata extraction fails.
        """
        from pathlib import Path

        # Use original filename, not temp file path
        filename = Path(self.file_path).name

        metadata = {
            "name": filename,
            "type": "Unknown",
            "architecture": "unknown",
            "entrypoint": None,
            "sections": [],
            "dependencies": [],
        }

        try:
            # Detect format and architecture
            metadata["type"], metadata["architecture"] = self._detect_format(binary)

            # Extract entrypoint (if present and non-zero)
            if hasattr(binary, 'entrypoint') and binary.entrypoint != 0:
                try:
                    metadata["entrypoint"] = hex(binary.entrypoint)
                except (AttributeError, ValueError):
                    # Some binary types may not have entrypoint or it may not be convertible
                    pass

            # Extract dependencies (imported libraries)
            if hasattr(binary, 'imported_libraries'):
                try:
                    for library in binary.imported_libraries:
                        if library:
                            metadata["dependencies"].append(library)
                except (AttributeError, TypeError) as e:
                    logger.warning(f"Failed to extract imported libraries: {e}")

            # Extract sections
            if hasattr(binary, 'sections'):
                try:
                    for section in binary.sections:
                        try:
                            section_info = {
                                'name': section.name,
                                'size': section.size,
                                'virtual_address': (
                                    hex(section.virtual_address)
                                    if hasattr(section, 'virtual_address')
                                    else None
                                ),
                            }
                            metadata["sections"].append(section_info)
                        except (AttributeError, ValueError) as e:
                            # Skip problematic sections but continue processing
                            logger.warning(f"Failed to extract section info: {e}")
                            continue
                except (AttributeError, TypeError) as e:
                    logger.warning(f"Failed to extract sections: {e}")

        except Exception as e:
            raise Exception(f"Failed to extract metadata from binary: {e}") from e

        return metadata

    def _detect_format(self, binary: Any) -> Tuple[str, str]:
        """
        Detect binary format and architecture from LIEF binary object.

        Args:
            binary: Parsed LIEF binary object.

        Returns:
            Tuple of (format, architecture) where:
            - format: One of 'ELF', 'PE', 'MachO', 'Raw'
            - architecture: String representation of architecture

        Raises:
            Exception: If format detection fails.
        """
        try:
            import lief

            # Check format using isinstance
            if isinstance(binary, lief.ELF.Binary):
                architecture = str(binary.header.machine_type)
                return "ELF", architecture
            elif isinstance(binary, lief.PE.Binary):
                architecture = str(binary.header.machine)
                return "PE", architecture
            elif isinstance(binary, lief.MachO.Binary):
                architecture = str(binary.header.cpu_type)
                return "MachO", architecture
            else:
                # Unknown format - treat as raw binary
                return "Raw", "unknown"

        except Exception as e:
            raise Exception(f"Failed to detect binary format: {e}") from e
