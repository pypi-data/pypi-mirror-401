"""
Integration tests for the streaming parser module.

Tests chunked binary reading, memory-mapped file support, LIEF integration,
and error handling for streaming parser functionality.
"""

import os
import tempfile
import mmap
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, PropertyMock

import pytest

from binary_sbom.streaming_parser import (
    ChunkInfo,
    ChunkReadError,
    FileSizeExceededError,
    LIEFStreamingParser,
    StreamingConfig,
    StreamingParser,
    StreamingParserError,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_MAX_FILE_SIZE_MB,
    MIN_CHUNK_SIZE,
    MAX_CHUNK_SIZE,
)


class TestStreamingConfig:
    """Test StreamingConfig configuration class."""

    def test_streaming_config_defaults(self):
        """Test that StreamingConfig initializes with correct defaults."""
        config = StreamingConfig()

        assert config.chunk_size == DEFAULT_CHUNK_SIZE
        assert config.max_file_size_mb == DEFAULT_MAX_FILE_SIZE_MB
        assert config.use_mmap is True
        assert config.enable_progress_tracking is True
        assert config.buffer_chunks == 2

    def test_streaming_config_custom_values(self):
        """Test StreamingConfig with custom values."""
        config = StreamingConfig(
            chunk_size=131072,  # 128 KB
            max_file_size_mb=200,
            use_mmap=False,
            enable_progress_tracking=False,
            buffer_chunks=4,
        )

        assert config.chunk_size == 131072
        assert config.max_file_size_mb == 200
        assert config.use_mmap is False
        assert config.enable_progress_tracking is False
        assert config.buffer_chunks == 4

    def test_streaming_config_chunk_size_too_small(self):
        """Test that chunk_size below minimum raises ValueError."""
        with pytest.raises(ValueError, match="chunk_size must be at least"):
            StreamingConfig(chunk_size=MIN_CHUNK_SIZE - 1)

    def test_streaming_config_chunk_size_too_large(self):
        """Test that chunk_size above maximum raises ValueError."""
        with pytest.raises(ValueError, match="chunk_size must be at most"):
            StreamingConfig(chunk_size=MAX_CHUNK_SIZE + 1)

    def test_streaming_config_invalid_max_file_size(self):
        """Test that non-positive max_file_size_mb raises ValueError."""
        with pytest.raises(ValueError, match="max_file_size_mb must be positive"):
            StreamingConfig(max_file_size_mb=0)

        with pytest.raises(ValueError, match="max_file_size_mb must be positive"):
            StreamingConfig(max_file_size_mb=-100)

    def test_streaming_config_invalid_buffer_chunks(self):
        """Test that negative buffer_chunks raises ValueError."""
        with pytest.raises(ValueError, match="buffer_chunks must be non-negative"):
            StreamingConfig(buffer_chunks=-1)

    def test_streaming_config_max_file_size_bytes_property(self):
        """Test max_file_size_bytes property conversion."""
        config = StreamingConfig(max_file_size_mb=100)

        assert config.max_file_size_bytes == 100 * 1024 * 1024


class TestChunkInfo:
    """Test ChunkInfo dataclass."""

    def test_chunk_info_creation(self):
        """Test creating ChunkInfo object."""
        info = ChunkInfo(offset=0, size=4096, index=0, is_last=False)

        assert info.offset == 0
        assert info.size == 4096
        assert info.index == 0
        assert info.is_last is False

    def test_chunk_info_defaults(self):
        """Test ChunkInfo with default values."""
        info = ChunkInfo(offset=0, size=4096, index=0)

        assert info.is_last is False  # Default value


class TestStreamingParserInitialization:
    """Test StreamingParser initialization and validation."""

    def test_streaming_parser_file_not_found(self):
        """Test that non-existent file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError, match="Binary file not found"):
            StreamingParser('/nonexistent/file.bin')

    def test_streaming_parser_path_is_directory(self):
        """Test that directory path raises ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with pytest.raises(ValueError, match="Path is not a file"):
                StreamingParser(tmpdir)

    def test_streaming_parser_file_too_large(self):
        """Test that file exceeding max size raises FileSizeExceededError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            # Write 1 MB of data
            f.write(b'x' * (1024 * 1024))
            temp_path = f.name

        try:
            config = StreamingConfig(max_file_size_mb=0.5)  # 512 KB limit

            with pytest.raises(FileSizeExceededError, match="File size .* exceeds maximum"):
                StreamingParser(temp_path, config=config)
        finally:
            os.unlink(temp_path)

    def test_streaming_parser_success_initialization(self):
        """Test successful parser initialization."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'some binary content')
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            assert parser.file_path == temp_path
            assert parser.file_size == len(b'some binary content')
            assert parser.total_chunks > 0
            assert parser.bytes_read == 0
            assert parser._current_chunk_index == 0
            assert parser._file_handle is None
            assert parser._mmap_handle is None
        finally:
            os.unlink(temp_path)

    def test_streaming_parser_custom_config(self):
        """Test parser initialization with custom config."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            # Write 128 KB of data
            f.write(b'x' * (128 * 1024))
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=4096)  # 4 KB chunks
            parser = StreamingParser(temp_path, config=config)

            assert parser.config.chunk_size == 4096
            assert parser.total_chunks == (128 * 1024 + 4096 - 1) // 4096
        finally:
            os.unlink(temp_path)

    def test_streaming_parser_with_eta_estimator(self):
        """Test parser initialization with ETA estimator."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test content')
            temp_path = f.name

        try:
            mock_eta = MagicMock()
            parser = StreamingParser(temp_path, eta_estimator=mock_eta)

            assert parser._eta_estimator is mock_eta
        finally:
            os.unlink(temp_path)


class TestStreamingParserProperties:
    """Test StreamingParser property methods."""

    def test_progress_percentage_empty_file(self):
        """Test progress_percentage for empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)
            assert parser.progress_percentage == 100.0
        finally:
            os.unlink(temp_path)

    def test_progress_percentage_partial_read(self):
        """Test progress_percentage during partial read."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)
            parser.bytes_read = 500

            assert parser.progress_percentage == 50.0
        finally:
            os.unlink(temp_path)

    def test_progress_percentage_complete(self):
        """Test progress_percentage when complete."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)
            parser.bytes_read = 1000

            assert parser.progress_percentage == 100.0
        finally:
            os.unlink(temp_path)

    def test_is_complete_true(self):
        """Test is_complete returns True when all bytes read."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)
            parser.bytes_read = 1000

            assert parser.is_complete is True
        finally:
            os.unlink(temp_path)

    def test_is_complete_false(self):
        """Test is_complete returns False when not all bytes read."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)
            parser.bytes_read = 500

            assert parser.is_complete is False
        finally:
            os.unlink(temp_path)


class TestStreamingParserContextManager:
    """Test StreamingParser context manager functionality."""

    def test_context_manager_enter_with_mmap(self):
        """Test entering context manager creates memory map."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 4096)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=True)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                assert parser._file_handle is not None
                assert parser._mmap_handle is not None
        finally:
            os.unlink(temp_path)

    def test_context_manager_enter_without_mmap(self):
        """Test entering context manager without memory map."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 4096)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=False)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                assert parser._file_handle is not None
                assert parser._mmap_handle is None
        finally:
            os.unlink(temp_path)

    def test_context_manager_exit_closes_handles(self):
        """Test exiting context manager closes file handles."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 4096)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=True)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                file_handle = parser._file_handle
                mmap_handle = parser._mmap_handle

            # After exiting, handles should be closed
            assert parser._file_handle is None
            assert parser._mmap_handle is None
        finally:
            os.unlink(temp_path)

    def test_context_manager_mmap_failure_fallback(self):
        """Test that mmap failure falls back to file I/O."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 4096)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=True)
            parser = StreamingParser(temp_path, config=config)

            # Mock mmap to raise error
            with patch('binary_sbom.streaming_parser.mmap.mmap') as mock_mmap:
                mock_mmap.side_effect = mmap.error("Cannot mmap")

                with parser:
                    # Should fall back to file handle only
                    assert parser._file_handle is not None
                    assert parser._mmap_handle is None
        finally:
            os.unlink(temp_path)


class TestStreamingParserReadChunk:
    """Test StreamingParser.read_chunk method."""

    def test_read_chunk_with_mmap(self):
        """Test reading chunk using memory map."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_data = b'Hello, World!'
            f.write(test_data)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=True)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                chunk = parser.read_chunk(0, len(test_data))

                assert chunk == test_data
                assert parser.bytes_read == len(test_data)
        finally:
            os.unlink(temp_path)

    def test_read_chunk_without_mmap(self):
        """Test reading chunk using file handle."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_data = b'Hello, World!'
            f.write(test_data)
            temp_path = f.name

        try:
            config = StreamingConfig(use_mmap=False)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                chunk = parser.read_chunk(0, len(test_data))

                assert chunk == test_data
                assert parser.bytes_read == len(test_data)
        finally:
            os.unlink(temp_path)

    def test_read_chunk_negative_offset(self):
        """Test that negative offset raises ValueError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test')
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                with pytest.raises(ValueError, match="Offset must be non-negative"):
                    parser.read_chunk(-1, 10)
        finally:
            os.unlink(temp_path)

    def test_read_chunk_offset_beyond_file_size(self):
        """Test that offset beyond file size raises ValueError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test')
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                with pytest.raises(ValueError, match="Offset .* exceeds file size"):
                    parser.read_chunk(100, 10)
        finally:
            os.unlink(temp_path)

    def test_read_chunk_not_open(self):
        """Test that reading without context manager raises ChunkReadError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test')
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with pytest.raises(ChunkReadError, match="File is not open"):
                parser.read_chunk(0, 10)
        finally:
            os.unlink(temp_path)

    def test_read_chunk_auto_size_calculation(self):
        """Test read_chunk with None size reads to end."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_data = b'Hello, World!'
            f.write(test_data)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                # Read from offset 5 to end
                chunk = parser.read_chunk(5, None)

                assert chunk == test_data[5:]
                assert parser.bytes_read == len(test_data[5:])
        finally:
            os.unlink(temp_path)

    def test_read_chunk_updates_eta_estimator(self):
        """Test that read_chunk updates ETA estimator."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            mock_eta = MagicMock()
            config = StreamingConfig(enable_progress_tracking=True)
            parser = StreamingParser(temp_path, config=config, eta_estimator=mock_eta)

            with parser:
                parser.read_chunk(0, 500)

                # Verify ETA was updated
                mock_eta.update_progress.assert_called_once_with(500, 1000)
        finally:
            os.unlink(temp_path)


class TestStreamingParserIterChunks:
    """Test StreamingParser.iter_chunks method."""

    def test_iter_chunks_small_file(self):
        """Test iterating chunks for small file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_data = b'x' * 100
            f.write(test_data)
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=40)  # 40 byte chunks
            parser = StreamingParser(temp_path, config=config)

            with parser:
                chunks = list(parser.iter_chunks())

                # Should have 3 chunks: 40, 40, 20
                assert len(chunks) == 3
                assert len(chunks[0]) == 40
                assert len(chunks[1]) == 40
                assert len(chunks[2]) == 20
                assert parser.bytes_read == 100
        finally:
            os.unlink(temp_path)

    def test_iter_chunks_updates_progress(self):
        """Test that iter_chunks updates progress tracking."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 100)
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=40)
            parser = StreamingParser(temp_path, config=config)

            with parser:
                chunk_count = 0
                for chunk in parser.iter_chunks():
                    chunk_count += 1
                    assert parser._current_chunk_index == chunk_count - 1

                assert chunk_count == 3
                assert parser.bytes_read == 100
        finally:
            os.unlink(temp_path)

    def test_iter_chunks_single_chunk(self):
        """Test iterating chunks when file fits in single chunk."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            test_data = b'x' * 100
            f.write(test_data)
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=1000)  # Larger than file
            parser = StreamingParser(temp_path, config=config)

            with parser:
                chunks = list(parser.iter_chunks())

                assert len(chunks) == 1
                assert chunks[0] == test_data
        finally:
            os.unlink(temp_path)

    def test_iter_chunks_empty_file(self):
        """Test iterating chunks for empty file."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                chunks = list(parser.iter_chunks())

                assert len(chunks) == 0
        finally:
            os.unlink(temp_path)


class TestStreamingParserGetChunkInfo:
    """Test StreamingParser.get_chunk_info method."""

    def test_get_chunk_info_first_chunk(self):
        """Test getting info for first chunk."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=100)
            parser = StreamingParser(temp_path, config=config)

            info = parser.get_chunk_info(0)

            assert info.offset == 0
            assert info.size == 100
            assert info.index == 0
            assert info.is_last is False
        finally:
            os.unlink(temp_path)

    def test_get_chunk_info_last_chunk(self):
        """Test getting info for last chunk."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 950)  # 9.5 chunks of 100 bytes
            temp_path = f.name

        try:
            config = StreamingConfig(chunk_size=100)
            parser = StreamingParser(temp_path, config=config)

            info = parser.get_chunk_info(9)

            assert info.offset == 900
            assert info.size == 50  # Last chunk is smaller
            assert info.index == 9
            assert info.is_last is True
        finally:
            os.unlink(temp_path)

    def test_get_chunk_info_invalid_index(self):
        """Test that invalid chunk index raises ValueError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with pytest.raises(ValueError, match="chunk_index must be between"):
                parser.get_chunk_info(-1)

            with pytest.raises(ValueError, match="chunk_index must be between"):
                parser.get_chunk_info(1000)
        finally:
            os.unlink(temp_path)


class TestStreamingParserResetProgress:
    """Test StreamingParser.reset_progress method."""

    def test_reset_progress(self):
        """Test resetting progress tracking."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            mock_eta = MagicMock()
            parser = StreamingParser(temp_path, eta_estimator=mock_eta)

            with parser:
                # Simulate reading some data
                parser.bytes_read = 500
                parser._current_chunk_index = 5

                # Reset
                parser.reset_progress()

                assert parser.bytes_read == 0
                assert parser._current_chunk_index == 0
                mock_eta.reset.assert_called_once()
        finally:
            os.unlink(temp_path)

    def test_reset_progress_without_eta(self):
        """Test resetting progress without ETA estimator."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                parser.bytes_read = 500
                parser._current_chunk_index = 5

                # Should not raise even without ETA
                parser.reset_progress()

                assert parser.bytes_read == 0
                assert parser._current_chunk_index == 0
        finally:
            os.unlink(temp_path)


class TestStreamingParserGetEstimatedTimeRemaining:
    """Test StreamingParser.get_estimated_time_remaining method."""

    def test_get_eta_with_estimator(self):
        """Test getting ETA when estimator is configured."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            mock_eta = MagicMock()
            mock_eta.estimate_time_remaining.return_value = 42.0
            config = StreamingConfig(enable_progress_tracking=True)
            parser = StreamingParser(temp_path, config=config, eta_estimator=mock_eta)

            with parser:
                parser.bytes_read = 500
                eta = parser.get_estimated_time_remaining()

                assert eta == 42.0
                mock_eta.estimate_time_remaining.assert_called_once_with(500, 1000)
        finally:
            os.unlink(temp_path)

    def test_get_eta_without_estimator(self):
        """Test getting ETA when no estimator is configured."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            parser = StreamingParser(temp_path)

            with parser:
                eta = parser.get_estimated_time_remaining()

                assert eta is None
        finally:
            os.unlink(temp_path)

    def test_get_eta_progress_tracking_disabled(self):
        """Test getting ETA when progress tracking is disabled."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'x' * 1000)
            temp_path = f.name

        try:
            mock_eta = MagicMock()
            config = StreamingConfig(enable_progress_tracking=False)
            parser = StreamingParser(temp_path, config=config, eta_estimator=mock_eta)

            with parser:
                eta = parser.get_estimated_time_remaining()

                assert eta is None
        finally:
            os.unlink(temp_path)


class TestLIEFStreamingParserParse:
    """Test LIEFStreamingParser.parse method."""

    def test_parse_not_open_raises_error(self):
        """Test that parse() without context manager raises StreamingParserError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'test')
            temp_path = f.name

        try:
            parser = LIEFStreamingParser(temp_path)

            with pytest.raises(StreamingParserError, match="Parser is not open"):
                parser.parse()
        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_success(self, mock_lief):
        """Test successful LIEF parsing with streaming."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'ELF binary content here')
            temp_path = f.name

        try:
            # Create mock binary object
            mock_binary = MagicMock()
            mock_binary.name = 'test_binary'
            mock_binary.entrypoint = 0x400000
            mock_binary.imported_libraries = ['libc.so.6', 'libm.so.6']

            # Create sections
            sections = []
            for name, size, vaddr in [('.text', 4096, 0x400000), ('.data', 1024, 0x401000)]:
                section = MagicMock()
                section.configure_mock(name=name, size=size, virtual_address=vaddr)
                sections.append(section)
            mock_binary.sections = sections

            # Mock LIEF to return our mock binary
            mock_lief.parse.return_value = mock_binary
            mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

            parser = LIEFStreamingParser(temp_path)

            with parser:
                metadata = parser.parse()

                # Verify basic metadata
                assert metadata['name'] == 'test_binary'
                assert metadata['type'] == 'ELF'
                assert metadata['architecture'] != 'unknown'
                assert 'sections' in metadata
                assert len(metadata['sections']) == 2
                assert 'dependencies' in metadata
                assert len(metadata['dependencies']) == 2
                assert metadata['size'] == len(b'ELF binary content here')
                assert metadata['_parser'] == 'lief-streaming'

                # Verify all bytes were read
                assert parser.bytes_read == parser.file_size

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_creates_and_cleans_temp_file(self, mock_lief):
        """Test that parse() creates temp file and cleans it up."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_binary.name = 'test'
            mock_binary.entrypoint = 0
            mock_binary.imported_libraries = []
            mock_binary.sections = []
            mock_lief.parse.return_value = mock_binary
            mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with patch('binary_sbom.streaming_parser.tempfile.NamedTemporaryFile') as mock_temp:
                    mock_temp_file = MagicMock()
                    mock_temp.return_value = mock_temp_file
                    mock_temp_file.name = '/tmp/test_temp.bin'
                    mock_temp_file.__enter__ = Mock(return_value=mock_temp_file)
                    mock_temp_file.__exit__ = Mock(return_value=False)

                    metadata = parser.parse()

                    # Verify temp file was created and written to
                    mock_temp.assert_called_once()
                    mock_temp_file.write.assert_called()
                    mock_temp_file.flush.assert_called_once()
                    mock_temp_file.close.assert_called_once()

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_size_mismatch_raises_error(self, mock_lief):
        """Test that size mismatch during streaming raises StreamingParserError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_binary = MagicMock()
            mock_binary.name = 'test'
            mock_binary.entrypoint = 0
            mock_binary.imported_libraries = []
            mock_binary.sections = []
            mock_lief.parse.return_value = mock_binary

            parser = LIEFStreamingParser(temp_path)

            with parser:
                # Manually set bytes_read to create size mismatch
                parser.bytes_read = parser.file_size - 1

                with pytest.raises(StreamingParserError, match="Size mismatch"):
                    parser.parse()

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief', None)
    def test_parse_lief_not_available(self):
        """Test that missing LIEF raises RuntimeError."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(RuntimeError, match="LIEF library is not available"):
                    parser.parse()

        finally:
            os.unlink(temp_path)


class TestLIEFStreamingParserParseWithLief:
    """Test LIEFStreamingParser._parse_with_lief method."""

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_with_lief_memory_error(self, mock_lief):
        """Test that MemoryError during LIEF parsing is handled."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = MemoryError('Out of memory')

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(MemoryError, match="File too large to parse"):
                    parser._parse_with_lief(temp_path)

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_with_lief_io_error(self, mock_lief):
        """Test that IOError during LIEF parsing is handled."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = IOError('Read failed')

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(OSError, match="Read error while parsing"):
                    parser._parse_with_lief(temp_path)

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_with_lief_corrupted_file(self, mock_lief):
        """Test that corrupted file error is detected."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = Exception('File is corrupted')

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(Exception, match="Corrupted binary file"):
                    parser._parse_with_lief(temp_path)

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_with_lief_unsupported_format(self, mock_lief):
        """Test that unsupported format error is detected."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_lief.parse.side_effect = Exception('Format not supported')

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(Exception, match="Unsupported binary format"):
                    parser._parse_with_lief(temp_path)

        finally:
            os.unlink(temp_path)

    @patch('binary_sbom.streaming_parser.lief')
    def test_parse_with_lief_returns_none(self, mock_lief):
        """Test that LIEF returning None raises Exception."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b'binary data')
            temp_path = f.name

        try:
            mock_lief.parse.return_value = None

            parser = LIEFStreamingParser(temp_path)

            with parser:
                with pytest.raises(Exception, match="Failed to parse binary file"):
                    parser._parse_with_lief(temp_path)

        finally:
            os.unlink(temp_path)


class TestLIEFStreamingParserExtractMetadata:
    """Test LIEFStreamingParser._extract_metadata method."""

    @patch('binary_sbom.streaming_parser.lief')
    def test_extract_metadata_elf(self, mock_lief):
        """Test metadata extraction for ELF binary."""
        mock_binary = MagicMock()
        mock_binary.name = 'test_binary'
        mock_binary.entrypoint = 0x400500
        mock_binary.imported_libraries = ['libc.so.6', 'libssl.so.1.1']

        sections = []
        for name, size in [('.text', 4096), ('.data', 2048)]:
            section = MagicMock()
            section.configure_mock(name=name, size=size, virtual_address=0x400000)
            sections.append(section)
        mock_binary.sections = sections

        mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

        parser = LIEFStreamingParser('/fake/path')

        metadata = parser._extract_metadata(mock_binary, '/fake/path')

        assert metadata['name'] == 'test_binary'
        assert metadata['type'] == 'ELF'
        assert metadata['architecture'] != 'unknown'
        assert metadata['entrypoint'] == hex(0x400500)
        assert len(metadata['sections']) == 2
        assert len(metadata['dependencies']) == 2

    @patch('binary_sbom.streaming_parser.lief')
    def test_extract_metadata_without_sections(self, mock_lief):
        """Test metadata extraction when binary has no sections."""
        mock_binary = MagicMock()
        mock_binary.name = 'minimal'
        mock_binary.entrypoint = 0
        mock_binary.imported_libraries = []

        # Remove sections attribute
        del mock_binary.sections

        mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

        parser = LIEFStreamingParser('/fake/path')

        metadata = parser._extract_metadata(mock_binary, '/fake/path')

        assert metadata['name'] == 'minimal'
        assert metadata['sections'] == []
        assert metadata['dependencies'] == []

    @patch('binary_sbom.streaming_parser.lief')
    def test_extract_metadata_filters_empty_dependencies(self, mock_lief):
        """Test that empty strings are filtered from dependencies."""
        mock_binary = MagicMock()
        mock_binary.name = 'test'
        mock_binary.entrypoint = 0
        mock_binary.imported_libraries = ['libc.so.6', '', 'libm.so.6', '', '']
        mock_binary.sections = []

        mock_lief.ELF.Binary = lambda x: isinstance(x, MagicMock)

        parser = LIEFStreamingParser('/fake/path')

        metadata = parser._extract_metadata(mock_binary, '/fake/path')

        assert len(metadata['dependencies']) == 2
        assert 'libc.so.6' in metadata['dependencies']
        assert '' not in metadata['dependencies']


class TestLIEFStreamingParserDetectFormat:
    """Test LIEFStreamingParser._detect_format method."""

    @patch('binary_sbom.streaming_parser.lief')
    def test_detect_format_elf(self, mock_lief):
        """Test format detection for ELF binary."""
        class MockELFBinary:
            pass

        mock_binary = MockELFBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.machine_type = 'EM_X86_64'
        mock_lief.ELF.Binary = MockELFBinary

        parser = LIEFStreamingParser('/fake/path')

        format_type, arch = parser._detect_format(mock_binary)

        assert format_type == 'ELF'
        assert arch == 'EM_X86_64'

    @patch('binary_sbom.streaming_parser.lief')
    def test_detect_format_pe(self, mock_lief):
        """Test format detection for PE binary."""
        class MockPEBinary:
            pass

        mock_binary = MockPEBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.machine = 'IMAGE_FILE_MACHINE_AMD64'
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = MockPEBinary

        parser = LIEFStreamingParser('/fake/path')

        format_type, arch = parser._detect_format(mock_binary)

        assert format_type == 'PE'
        assert arch == 'IMAGE_FILE_MACHINE_AMD64'

    @patch('binary_sbom.streaming_parser.lief')
    def test_detect_format_macho(self, mock_lief):
        """Test format detection for MachO binary."""
        class MockMachOBinary:
            pass

        mock_binary = MockMachOBinary()
        mock_binary.header = MagicMock()
        mock_binary.header.cpu_type = 'CPU_TYPE_ARM64'
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = lambda x: False
        mock_lief.MachO.Binary = MockMachOBinary

        parser = LIEFStreamingParser('/fake/path')

        format_type, arch = parser._detect_format(mock_binary)

        assert format_type == 'MachO'
        assert arch == 'CPU_TYPE_ARM64'

    @patch('binary_sbom.streaming_parser.lief')
    def test_detect_format_raw(self, mock_lief):
        """Test format detection for raw binary."""
        mock_binary = MagicMock()
        mock_lief.ELF.Binary = lambda x: False
        mock_lief.PE.Binary = lambda x: False
        mock_lief.MachO.Binary = lambda x: False

        parser = LIEFStreamingParser('/fake/path')

        format_type, arch = parser._detect_format(mock_binary)

        assert format_type == 'Raw'
        assert arch == 'unknown'


class TestStreamingParserErrors:
    """Test streaming parser error handling."""

    def test_chunk_read_error_is_exception(self):
        """Test that ChunkReadError is an Exception subclass."""
        assert issubclass(ChunkReadError, Exception)

    def test_file_size_exceeded_error_is_exception(self):
        """Test that FileSizeExceededError is an Exception subclass."""
        assert issubclass(FileSizeExceededError, Exception)

    def test_streaming_parser_error_is_exception(self):
        """Test that StreamingParserError is an Exception subclass."""
        assert issubclass(StreamingParserError, Exception)

    def test_chunk_read_error_can_be_raised(self):
        """Test that ChunkReadError can be raised and caught."""
        with pytest.raises(ChunkReadError):
            raise ChunkReadError("Test chunk read error")

    def test_file_size_exceeded_error_can_be_raised(self):
        """Test that FileSizeExceededError can be raised and caught."""
        with pytest.raises(FileSizeExceededError):
            raise FileSizeExceededError("Test file size exceeded")

    def test_streaming_parser_error_can_be_raised(self):
        """Test that StreamingParserError can be raised and caught."""
        with pytest.raises(StreamingParserError):
            raise StreamingParserError("Test streaming parser error")
