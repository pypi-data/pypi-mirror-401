"""
Unit tests for the path validator module.

Tests path sanitization, directory traversal prevention, and symlink safety.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from binary_sbom.path_validator import (
    PathValidationError,
    sanitize_path,
    validate_file_path,
    validate_directory_path,
    check_symlink_safety,
)


class TestPathValidationError:
    """Test PathValidationError exception."""

    def test_path_validation_error_is_exception(self):
        """Test that PathValidationError is an Exception subclass."""
        assert issubclass(PathValidationError, Exception)

    def test_path_validation_error_can_be_raised(self):
        """Test that PathValidationError can be raised and caught."""
        with pytest.raises(PathValidationError):
            raise PathValidationError("Test error")

    def test_path_validation_error_message(self):
        """Test that PathValidationError preserves error message."""
        error_msg = "Test path validation error"
        with pytest.raises(PathValidationError, match=error_msg):
            raise PathValidationError(error_msg)


class TestSanitizePath:
    """Test path sanitization functionality."""

    def test_sanitize_path_with_absolute_path(self):
        """Test sanitizing an absolute path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = os.path.join(tmpdir, 'test.txt')
            Path(test_path).touch()

            result = sanitize_path(test_path)
            # On macOS, tmpdir might resolve to /private/var/... instead of /var/...
            # So we sanitize both for comparison
            assert os.path.realpath(result) == os.path.realpath(test_path) or result == test_path

    def test_sanitize_path_with_relative_path(self):
        """Test sanitizing a relative path."""
        result = sanitize_path('relative/path/../file.txt')
        # Should resolve to an absolute path
        assert os.path.isabs(result)
        # Should not contain '..'
        assert '..' not in result

    def test_sanitize_path_removes_dot_components(self):
        """Test that '.' components are removed."""
        result = sanitize_path('./test/./file.txt')
        assert '/./' not in result
        assert not result.startswith('./')

    def test_sanitize_path_removes_double_dot_components(self):
        """Test that '..' components are resolved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            test_path = os.path.join(subdir, '..', 'test.txt')
            result = sanitize_path(test_path)

            # Should resolve the '..' and not contain it
            assert '..' not in result

    def test_sanitize_path_expands_user_home(self):
        """Test that '~' is expanded to home directory."""
        with patch.dict(os.environ, {'HOME': '/test/home'}):
            result = sanitize_path('~/test.txt')
            # Should expand ~
            assert '~' not in result
            assert result.startswith('/test/home')

    def test_sanitize_path_with_path_object(self):
        """Test sanitizing a Path object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_path = Path(tmpdir) / 'test.txt'
            test_path.touch()

            result = sanitize_path(test_path)
            assert isinstance(result, str)
            assert os.path.isabs(result)

    def test_sanitize_path_rejects_null_bytes(self):
        """Test that paths with null bytes are rejected."""
        # Python's Path object may handle null bytes differently
        # Try with both the null byte in the string and Path creation
        test_path = '/test/path\x00file.txt'
        with pytest.raises((PathValidationError, ValueError)):
            sanitize_path(test_path)

    def test_sanitize_path_with_invalid_type(self):
        """Test that invalid path types raise PathValidationError."""
        with pytest.raises(PathValidationError, match='Invalid path type'):
            sanitize_path(123)

    def test_sanitize_path_with_invalid_type_list(self):
        """Test that list paths raise PathValidationError."""
        with pytest.raises(PathValidationError, match='Invalid path type'):
            sanitize_path(['path', 'to', 'file'])

    def test_sanitize_path_with_empty_string(self):
        """Test that empty string is handled properly."""
        result = sanitize_path('')
        # Should resolve to current directory
        assert os.path.isabs(result)

    def test_sanitize_path_resolves_symlinks(self):
        """Test that symbolic links are resolved."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a file and a symlink to it
            target_file = os.path.join(tmpdir, 'target.txt')
            Path(target_file).touch()

            symlink_path = os.path.join(tmpdir, 'symlink.txt')
            os.symlink(target_file, symlink_path)

            result = sanitize_path(symlink_path)
            # Should resolve to the actual file, not the symlink
            # Normalize paths for comparison (handles macOS /var vs /private/var)
            assert os.path.realpath(result) == os.path.realpath(target_file)

    def test_sanitize_path_with_nonexistent_path(self):
        """Test that non-existent paths are handled gracefully."""
        # Should not raise for non-existent paths (strict=False in resolve)
        result = sanitize_path('/nonexistent/path/file.txt')
        assert os.path.isabs(result)
        assert '..' not in result


class TestValidateFilePath:
    """Test file path validation functionality."""

    def test_validate_file_path_within_allowed_dir(self):
        """Test validating a file within allowed directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            result = validate_file_path(test_file, [tmpdir])
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(test_file)

    def test_validate_file_path_with_multiple_allowed_dirs(self):
        """Test validation with multiple allowed directories."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                test_file = os.path.join(tmpdir2, 'test.txt')
                Path(test_file).touch()

                result = validate_file_path(test_file, [tmpdir1, tmpdir2])
                # Normalize for macOS path resolution
                assert os.path.realpath(result) == os.path.realpath(test_file)

    def test_validate_file_path_outside_allowed_dir(self):
        """Test that file outside allowed directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = '/etc/passwd'

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(test_file, [tmpdir])

    def test_validate_file_path_with_empty_allowed_dirs(self):
        """Test that empty allowed_dirs list raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')

            with pytest.raises(PathValidationError, match='No allowed directories specified'):
                validate_file_path(test_file, [])

    def test_validate_file_path_with_directory_traversal(self):
        """Test that directory traversal is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try to escape with .. but still within allowed dir
            test_file = os.path.join(subdir, '..', 'test.txt')
            Path(test_file).touch()

            result = validate_file_path(test_file, [tmpdir])
            # Should resolve and be within allowed dir
            assert tmpdir in result

    def test_validate_file_path_with_symlink_escape(self):
        """Test that symlink escape is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create a file in other_dir
                target_file = os.path.join(other_dir, 'target.txt')
                Path(target_file).touch()

                # Create a symlink in tmpdir pointing outside
                symlink_path = os.path.join(tmpdir, 'escape.txt')
                os.symlink(target_file, symlink_path)

                # Symlink points outside allowed dir
                with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                    validate_file_path(symlink_path, [tmpdir])

    def test_validate_file_path_with_invalid_allowed_dir(self):
        """Test that invalid allowed directory raises error."""
        test_file = '/tmp/test.txt'

        with pytest.raises(PathValidationError, match='Invalid allowed directory'):
            validate_file_path(test_file, [123])

    def test_validate_file_path_with_invalid_file_path(self):
        """Test that invalid file path raises error."""
        with pytest.raises(PathValidationError, match='Cannot validate file path'):
            validate_file_path(123, ['/tmp'])

    def test_validate_file_path_relative_path_within_allowed(self):
        """Test that relative paths are validated correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test file
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            # Change to tmpdir and use relative path
            original_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                result = validate_file_path('test.txt', [tmpdir])
                # Should resolve to absolute path
                assert os.path.isabs(result)
            finally:
                os.chdir(original_cwd)

    def test_validate_file_path_with_path_objects(self):
        """Test that Path objects work for both arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'test.txt'
            test_file.touch()

            result = validate_file_path(test_file, [Path(tmpdir)])
            assert isinstance(result, str)

    def test_validate_file_path_exact_match_allowed_dir(self):
        """Test that file exactly matching allowed dir is handled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # This should work - the allowed dir itself
            result = validate_file_path(tmpdir, [tmpdir])
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(tmpdir)

    def test_validate_file_path_trailing_separator_handling(self):
        """Test that trailing separators are handled correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            # Allowed dir with trailing separator
            allowed_with_sep = tmpdir + os.sep
            result = validate_file_path(test_file, [allowed_with_sep])
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(test_file)

    def test_validate_file_path_blocks_double_dot_etc_passwd(self):
        """Test that ../../etc/passwd pattern is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try to access /etc/passwd using directory traversal
            traversal_path = os.path.join(subdir, '../../etc/passwd')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_triple_dot_etc_passwd(self):
        """Test that ../../../etc/passwd pattern is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir', 'nested')
            os.makedirs(subdir)

            # Try to access /etc/passwd using deep directory traversal
            traversal_path = os.path.join(subdir, '../../../etc/passwd')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_quadruple_dot_etc_passwd(self):
        """Test that ../../../../etc/passwd pattern is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'a', 'b', 'c')
            os.makedirs(subdir)

            # Try to access /etc/passwd using very deep directory traversal
            traversal_path = os.path.join(subdir, '../../../../../../etc/passwd')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_traversal_to_root(self):
        """Test that traversal to root directory is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try to escape to root
            traversal_path = os.path.join(subdir, '../../..')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_mixed_traversal_patterns(self):
        """Test that mixed traversal patterns are blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try mixed pattern: go up then down to escape
            traversal_path = os.path.join(subdir, '../subdir/../../etc/passwd')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_absolute_path_with_traversal(self):
        """Test that absolute paths with traversal components are handled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Absolute path outside allowed dir
            test_path = '/tmp/test.txt'

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(test_path, [tmpdir])

    def test_validate_file_path_blocks_traversal_to_system_binary(self):
        """Test that traversal to system binaries is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try to access system binaries
            traversal_path = os.path.join(subdir, '../../usr/bin/ls')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_blocks_traversal_to_user_home(self):
        """Test that traversal to user home is blocked."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir')
            os.makedirs(subdir)

            # Try to access user home directory
            traversal_path = os.path.join(subdir, '../../root/.ssh')

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_file_path(traversal_path, [tmpdir])

    def test_validate_file_path_allows_safe_traversal_within_allowed(self):
        """Test that safe traversal within allowed directory works."""
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, 'subdir', 'nested')
            os.makedirs(subdir)

            # Create a file in parent of nested
            parent_file = os.path.join(tmpdir, 'parent.txt')
            Path(parent_file).touch()

            # Navigate up from nested to parent (still within allowed dir)
            traversal_path = os.path.join(subdir, '../../parent.txt')

            result = validate_file_path(traversal_path, [tmpdir])
            # Should succeed and resolve to the file
            assert os.path.realpath(result) == os.path.realpath(parent_file)


class TestValidateDirectoryPath:
    """Test directory path validation functionality."""

    def test_validate_directory_path_within_allowed_base(self):
        """Test validating a directory within allowed base directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, 'subdir')
            os.makedirs(test_dir)

            result = validate_directory_path(test_dir, [tmpdir])
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(test_dir)

    def test_validate_directory_path_outside_allowed_base(self):
        """Test that directory outside allowed base raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = '/etc'

            with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                validate_directory_path(test_dir, [tmpdir])

    def test_validate_directory_path_empty_allowed_base_dirs(self):
        """Test that empty allowed_base_dirs raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, 'subdir')

            with pytest.raises(PathValidationError, match='No allowed base directories specified'):
                validate_directory_path(test_dir, [])

    def test_validate_directory_path_nonexistent_directory(self):
        """Test that non-existent directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, 'nonexistent')

            with pytest.raises(PathValidationError, match='Directory does not exist'):
                validate_directory_path(test_dir, [tmpdir])

    def test_validate_directory_path_file_instead_of_directory(self):
        """Test that a file path raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'file.txt')
            Path(test_file).touch()

            with pytest.raises(PathValidationError, match='Path is not a directory'):
                validate_directory_path(test_file, [tmpdir])

    def test_validate_directory_path_with_symlink_escape(self):
        """Test that symlink escape is detected for directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create a directory in other_dir
                target_dir = os.path.join(other_dir, 'target')
                os.makedirs(target_dir)

                # Create a symlink in tmpdir pointing outside
                symlink_path = os.path.join(tmpdir, 'escape')
                os.symlink(target_dir, symlink_path)

                # Symlink points outside allowed dir
                with pytest.raises(PathValidationError, match='outside allowed directory boundaries'):
                    validate_directory_path(symlink_path, [tmpdir])

    def test_validate_directory_path_with_symlink_inside_allowed(self):
        """Test that symlink within allowed directory is allowed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create actual directory
            target_dir = os.path.join(tmpdir, 'actual_dir')
            os.makedirs(target_dir)

            # Create symlink within allowed dir
            symlink_path = os.path.join(tmpdir, 'symlink_dir')
            os.symlink(target_dir, symlink_path)

            # Should work since symlink points within allowed dir
            result = validate_directory_path(symlink_path, [tmpdir])
            # Should resolve to actual directory
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(target_dir)

    def test_validate_directory_path_with_multiple_allowed_bases(self):
        """Test validation with multiple allowed base directories."""
        with tempfile.TemporaryDirectory() as tmpdir1:
            with tempfile.TemporaryDirectory() as tmpdir2:
                test_dir = os.path.join(tmpdir2, 'subdir')
                os.makedirs(test_dir)

                result = validate_directory_path(test_dir, [tmpdir1, tmpdir2])
                # Normalize for macOS path resolution
                assert os.path.realpath(result) == os.path.realpath(test_dir)

    def test_validate_directory_path_with_invalid_allowed_dir(self):
        """Test that invalid allowed directory raises error."""
        test_dir = '/tmp/test'

        with pytest.raises(PathValidationError, match='Invalid allowed base directory'):
            validate_directory_path(test_dir, [123])

    def test_validate_directory_path_with_invalid_directory_path(self):
        """Test that invalid directory path raises error."""
        with pytest.raises(PathValidationError, match='Cannot validate directory path'):
            validate_directory_path(123, ['/tmp'])

    def test_validate_directory_path_exact_match_allowed_base(self):
        """Test that directory exactly matching allowed base is handled."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = validate_directory_path(tmpdir, [tmpdir])
            # Normalize for macOS path resolution
            assert os.path.realpath(result) == os.path.realpath(tmpdir)

    def test_validate_directory_path_with_path_objects(self):
        """Test that Path objects work for both arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = Path(tmpdir) / 'subdir'
            test_dir.mkdir()

            result = validate_directory_path(test_dir, [Path(tmpdir)])
            assert isinstance(result, str)


class TestCheckSymlinkSafety:
    """Test symlink safety checking functionality."""

    def test_check_symlink_safety_with_regular_file(self):
        """Test that regular file passes symlink safety check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            result = check_symlink_safety(test_file, tmpdir)
            assert result is True

    def test_check_symlink_safety_with_safe_symlink(self):
        """Test that symlink within allowed directory is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create target file
            target_file = os.path.join(tmpdir, 'target.txt')
            Path(target_file).touch()

            # Create symlink within allowed dir
            symlink_path = os.path.join(tmpdir, 'link.txt')
            os.symlink(target_file, symlink_path)

            result = check_symlink_safety(symlink_path, tmpdir)
            assert result is True

    def test_check_symlink_safety_with_escaping_symlink(self):
        """Test that symlink escaping allowed directory is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create target file outside allowed dir
                target_file = os.path.join(other_dir, 'target.txt')
                Path(target_file).touch()

                # Create symlink in allowed dir pointing outside
                symlink_path = os.path.join(tmpdir, 'escape.txt')
                os.symlink(target_file, symlink_path)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_with_directory_symlink_escape(self):
        """Test that directory symlink escape is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create target directory outside allowed dir
                target_dir = os.path.join(other_dir, 'target_dir')
                os.makedirs(target_dir)

                # Create symlink in allowed dir pointing outside
                symlink_path = os.path.join(tmpdir, 'escape_dir')
                os.symlink(target_dir, symlink_path)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_with_chain_symlinks(self):
        """Test that chained symlinks are followed."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create target file
            target_file = os.path.join(tmpdir, 'target.txt')
            Path(target_file).touch()

            # Create first symlink
            link1 = os.path.join(tmpdir, 'link1.txt')
            os.symlink(target_file, link1)

            # Create second symlink pointing to first
            link2 = os.path.join(tmpdir, 'link2.txt')
            os.symlink(link1, link2)

            result = check_symlink_safety(link2, tmpdir)
            assert result is True

    def test_check_symlink_safety_with_chain_escape(self):
        """Test that symlink escape through chain is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create target file outside allowed dir
                target_file = os.path.join(other_dir, 'target.txt')
                Path(target_file).touch()

                # Create first symlink to outside
                link1 = os.path.join(tmpdir, 'link1.txt')
                os.symlink(target_file, link1)

                # Create second symlink pointing to first
                link2 = os.path.join(tmpdir, 'link2.txt')
                os.symlink(link1, link2)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(link2, tmpdir)

    def test_check_symlink_safety_with_relative_symlink(self):
        """Test that relative symlinks are resolved correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create target file
            target_file = os.path.join(tmpdir, 'target.txt')
            Path(target_file).touch()

            # Create relative symlink
            symlink_path = os.path.join(tmpdir, 'link.txt')
            os.symlink('target.txt', symlink_path)

            result = check_symlink_safety(symlink_path, tmpdir)
            assert result is True

    def test_check_symlink_safety_with_invalid_file_path(self):
        """Test that invalid file path raises error."""
        # The error message comes from sanitize_path, not check_symlink_safety
        with pytest.raises(PathValidationError, match='Invalid path type'):
            check_symlink_safety(123, '/tmp')

    def test_check_symlink_safety_with_invalid_allowed_dir(self):
        """Test that invalid allowed directory raises error."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = os.path.join(tmpdir, 'test.txt')
            Path(test_file).touch()

            # The error message comes from sanitize_path, not check_symlink_safety
            with pytest.raises(PathValidationError, match='Invalid path type'):
                check_symlink_safety(test_file, 123)

    def test_check_symlink_safety_exact_match_allowed_dir(self):
        """Test that path matching allowed dir exactly is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = check_symlink_safety(tmpdir, tmpdir)
            assert result is True

    def test_check_symlink_safety_with_path_objects(self):
        """Test that Path objects work for both arguments."""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_file = Path(tmpdir) / 'test.txt'
            test_file.touch()

            result = check_symlink_safety(test_file, Path(tmpdir))
            assert result is True

    def test_check_symlink_safety_symlink_to_system_file(self):
        """Test that symlink to /etc/passwd is detected as escape."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create symlink to /etc/passwd
            symlink_path = os.path.join(tmpdir, 'passwd_link')
            os.symlink('/etc/passwd', symlink_path)

            with pytest.raises(PathValidationError, match='Symlink escape detected'):
                check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_symlink_to_system_binary(self):
        """Test that symlink to /usr/bin is detected as escape."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create symlink to /usr/bin
            symlink_path = os.path.join(tmpdir, 'bin_link')
            os.symlink('/usr/bin', symlink_path)

            with pytest.raises(PathValidationError, match='Symlink escape detected'):
                check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_symlink_to_user_home(self):
        """Test that symlink to user home is detected as escape."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create symlink to /root
            symlink_path = os.path.join(tmpdir, 'root_link')
            os.symlink('/root', symlink_path)

            with pytest.raises(PathValidationError, match='Symlink escape detected'):
                check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_symlink_to_parent_directory(self):
        """Test that symlink to parent directory is detected as escape."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as parent_dir:
                # Get parent of tmpdir
                tmpdir_parent = os.path.dirname(tmpdir)

                # Create symlink to parent
                symlink_path = os.path.join(tmpdir, 'parent_link')
                os.symlink(tmpdir_parent, symlink_path)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_relative_symlink_escape(self):
        """Test that relative symlink escaping allowed dir is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create symlink using relative path that escapes
                # ../../../other_dir should escape tmpdir
                subdir = os.path.join(tmpdir, 'subdir')
                os.makedirs(subdir)

                symlink_path = os.path.join(subdir, 'escape_link')
                # Create relative symlink pointing outside
                os.symlink('../../../../../..' + other_dir, symlink_path)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_broken_symlink_inside_allowed(self):
        """Test that broken symlink within allowed dir is safe."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create symlink to non-existent file within allowed dir
            symlink_path = os.path.join(tmpdir, 'broken_link')
            os.symlink('nonexistent.txt', symlink_path)

            # Should be safe even if broken (target would be within allowed dir)
            result = check_symlink_safety(symlink_path, tmpdir)
            assert result is True

    def test_check_symlink_safety_broken_symlink_escape(self):
        """Test that broken symlink escaping allowed dir is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create symlink to non-existent file outside allowed dir
                symlink_path = os.path.join(tmpdir, 'escape_link')
                target = os.path.join(other_dir, 'nonexistent.txt')
                os.symlink(target, symlink_path)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(symlink_path, tmpdir)

    def test_check_symlink_safety_circular_symlink_chain(self):
        """Test that circular symlink chain raises PathValidationError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create circular symlinks within allowed dir
            link1 = os.path.join(tmpdir, 'link1')
            link2 = os.path.join(tmpdir, 'link2')

            os.symlink(link2, link1)
            os.symlink(link1, link2)

            # Circular symlinks cause resolution errors
            with pytest.raises(PathValidationError, match='Cannot resolve path'):
                check_symlink_safety(link1, tmpdir)

    def test_check_symlink_safety_symlink_to_symlink_escape(self):
        """Test that symlink through intermediate directory escape is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create a file in other_dir
                target_file = os.path.join(other_dir, 'target.txt')
                Path(target_file).touch()

                # Create intermediate directory in tmpdir with symlink to other_dir
                int_dir = os.path.join(tmpdir, 'intermediate')
                os.makedirs(int_dir)

                escape_link = os.path.join(int_dir, 'escape_dir')
                os.symlink(other_dir, escape_link)

                # Create symlink in tmpdir pointing to intermediate/escape_dir/target.txt
                final_link = os.path.join(tmpdir, 'final_link')
                os.symlink(os.path.join('intermediate', 'escape_dir', 'target.txt'), final_link)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(final_link, tmpdir)

    def test_check_symlink_safety_deep_chain_escape(self):
        """Test that deep symlink chain escape is detected."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with tempfile.TemporaryDirectory() as other_dir:
                # Create target file outside
                target_file = os.path.join(other_dir, 'target.txt')
                Path(target_file).touch()

                # Create chain of symlinks: link1 -> link2 -> link3 -> outside
                link1 = os.path.join(tmpdir, 'link1')
                link2 = os.path.join(tmpdir, 'link2')
                link3 = os.path.join(tmpdir, 'link3')

                os.symlink(link2, link1)
                os.symlink(link3, link2)
                os.symlink(target_file, link3)

                with pytest.raises(PathValidationError, match='Symlink escape detected'):
                    check_symlink_safety(link1, tmpdir)
