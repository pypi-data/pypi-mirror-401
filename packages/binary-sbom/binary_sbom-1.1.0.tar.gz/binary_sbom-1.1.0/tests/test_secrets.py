"""
Unit tests for the secrets module.

Tests encryption, decryption, environment variable loading, log redaction,
and optional keyring integration.
"""

import base64
import os
import stat
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from binary_sbom.secrets import (
    _get_encryption_key,
    encrypt_secret,
    decrypt_secret,
    _ensure_secure_permissions,
    load_secret,
    redact_secret,
    get_keyring_secret,
    set_keyring_secret,
    delete_keyring_secret,
    KEYRING_AVAILABLE,
)


class TestGetEncryptionKey:
    """Test encryption key generation."""

    def test_get_key_from_env_var_valid_fernet_key(self):
        """Test loading a valid Fernet key from environment variable."""
        # A valid Fernet key is 44 bytes base64-encoded
        valid_key = base64.urlsafe_b64encode(b'test-key-32-bytes-1234567890abcd').decode('utf-8')
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': valid_key}):
            key = _get_encryption_key()
            assert isinstance(key, bytes)
            assert len(key) == 44

    def test_get_key_from_env_var_custom_string(self):
        """Test deriving key from custom environment variable string."""
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': 'my-custom-key-12345'}):
            key = _get_encryption_key()
            assert isinstance(key, bytes)
            # Should be base64-encoded
            assert len(key) == 44  # Fernet keys are always 44 bytes

    def test_get_key_fallback_to_system_id(self):
        """Test fallback to system-specific key when env var not set."""
        with patch.dict(os.environ, {}, clear=True):
            key = _get_encryption_key()
            assert isinstance(key, bytes)
            assert len(key) == 44

    def test_get_key_consistency(self):
        """Test that the same environment produces the same key."""
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': 'test-key-value'}):
            key1 = _get_encryption_key()
            key2 = _get_encryption_key()
            assert key1 == key2


class TestEncryptSecret:
    """Test secret encryption functionality."""

    def test_encrypt_secret_basic(self):
        """Test basic encryption of a secret string."""
        plaintext = "my-api-key-12345"
        encrypted = encrypt_secret(plaintext)
        assert isinstance(encrypted, str)
        assert encrypted != plaintext
        assert len(encrypted) > len(plaintext)

    def test_encrypt_secret_returns_different_ciphertext(self):
        """Test that encrypting the same value produces different ciphertext (due to IV)."""
        plaintext = "my-secret"
        encrypted1 = encrypt_secret(plaintext)
        encrypted2 = encrypt_secret(plaintext)
        # Fernet includes a random IV, so ciphertexts will be different
        assert encrypted1 != encrypted2
        # But both should decrypt to the same value
        assert decrypt_secret(encrypted1) == plaintext
        assert decrypt_secret(encrypted2) == plaintext

    def test_encrypt_secret_with_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            encrypt_secret("")

    def test_encrypt_secret_with_non_string(self):
        """Test that non-string input raises ValueError."""
        # None is treated as empty/falsy, so it raises "cannot be empty"
        with pytest.raises(ValueError, match="cannot be empty"):
            encrypt_secret(None)
        # Other non-string types raise "must be a string"
        with pytest.raises(ValueError, match="must be a string"):
            encrypt_secret(12345)

    def test_encrypt_secret_with_unicode(self):
        """Test encryption of unicode characters."""
        plaintext = "secret-with-unicode-ñoño-café"
        encrypted = encrypt_secret(plaintext)
        decrypted = decrypt_secret(encrypted)
        assert decrypted == plaintext

    def test_encrypt_secret_with_long_string(self):
        """Test encryption of a long string."""
        plaintext = "a" * 10000
        encrypted = encrypt_secret(plaintext)
        decrypted = decrypt_secret(encrypted)
        assert decrypted == plaintext


class TestDecryptSecret:
    """Test secret decryption functionality."""

    def test_decrypt_secret_basic(self):
        """Test basic decryption of an encrypted secret."""
        plaintext = "my-api-key-12345"
        encrypted = encrypt_secret(plaintext)
        decrypted = decrypt_secret(encrypted)
        assert decrypted == plaintext
        assert decrypted != encrypted

    def test_decrypt_secret_roundtrip(self):
        """Test that encrypt-decrypt roundtrip preserves the original value."""
        original = "test-secret-key-abc123"
        encrypted = encrypt_secret(original)
        decrypted = decrypt_secret(encrypted)
        assert decrypted == original

    def test_decrypt_secret_with_empty_string(self):
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            decrypt_secret("")

    def test_decrypt_secret_with_non_string(self):
        """Test that non-string input raises ValueError."""
        with pytest.raises(ValueError, match="must be a string"):
            decrypt_secret(12345)

    def test_decrypt_secret_with_invalid_ciphertext(self):
        """Test that invalid ciphertext raises RuntimeError."""
        with pytest.raises(RuntimeError, match="Failed to decrypt"):
            decrypt_secret("not-a-valid-ciphertext")

    def test_decrypt_secret_with_wrong_key(self):
        """Test that using a different encryption key fails."""
        # Encrypt with one key
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': 'key-one-1234567890123456789012'}):
            encrypted = encrypt_secret("secret-value")

        # Try to decrypt with a different key
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': 'key-two-1234567890123456789012'}):
            with pytest.raises(RuntimeError, match="invalid key or corrupted"):
                decrypt_secret(encrypted)


class TestEnsureSecurePermissions:
    """Test secure file permissions setting."""

    def test_ensure_secure_permissions_on_file(self):
        """Test that file permissions are set to 0600."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            # Set permissive permissions first
            os.chmod(temp_path, 0o644)

            # Apply secure permissions
            _ensure_secure_permissions(temp_path)

            # Check permissions are 0600
            file_stat = os.stat(temp_path)
            permissions = stat.filemode(file_stat.st_mode)
            assert permissions.startswith('-rw-------')

        finally:
            os.unlink(temp_path)

    def test_ensure_secure_permissions_on_nonexistent_file(self):
        """Test that nonexistent file doesn't raise error (best-effort)."""
        # Should not raise an exception
        _ensure_secure_permissions("/nonexistent/path/file.txt")


class TestLoadSecret:
    """Test loading secrets from environment variables."""

    def test_load_secret_from_env_var(self):
        """Test loading a secret from environment variable."""
        with patch.dict(os.environ, {'TEST_API_KEY': 'my-secret-key'}):
            secret = load_secret('TEST_API_KEY')
            assert secret == 'my-secret-key'

    def test_load_secret_with_default(self):
        """Test loading with default value when env var not set."""
        with patch.dict(os.environ, {}, clear=True):
            secret = load_secret('NONEXISTENT_VAR', default='default-value')
            assert secret == 'default-value'

    def test_load_secret_without_default(self):
        """Test loading returns None when env var not set and no default."""
        with patch.dict(os.environ, {}, clear=True):
            secret = load_secret('NONEXISTENT_VAR')
            assert secret is None

    def test_load_secret_with_encrypted_true(self):
        """Test loading and decrypting an encrypted secret."""
        plaintext = "my-encrypted-secret"
        encrypted = encrypt_secret(plaintext)

        with patch.dict(os.environ, {'ENCRYPTED_SECRET': encrypted}):
            secret = load_secret('ENCRYPTED_SECRET', encrypted=True)
            assert secret == plaintext

    def test_load_secret_with_encrypted_false(self):
        """Test loading without decryption when encrypted=False."""
        encrypted = encrypt_secret("my-secret")

        with patch.dict(os.environ, {'SECRET_VAR': encrypted}):
            secret = load_secret('SECRET_VAR', encrypted=False)
            # Should return the encrypted value as-is
            assert secret == encrypted

    def test_load_secret_with_invalid_encrypted(self):
        """Test that invalid encrypted value raises RuntimeError."""
        with patch.dict(os.environ, {'BAD_SECRET': 'invalid-ciphertext'}):
            with pytest.raises(RuntimeError, match="Failed to decrypt"):
                load_secret('BAD_SECRET', encrypted=True)

    def test_load_secret_empty_string(self):
        """Test loading an empty string from environment."""
        with patch.dict(os.environ, {'EMPTY_VAR': ''}):
            secret = load_secret('EMPTY_VAR')
            assert secret == ''

    def test_load_secret_with_whitespace(self):
        """Test loading a secret with whitespace."""
        with patch.dict(os.environ, {'WHITESPACE_VAR': '  spaced-out  '}):
            secret = load_secret('WHITESPACE_VAR')
            assert secret == '  spaced-out  '


class TestRedactSecret:
    """Test secret redaction for safe logging."""

    def test_redact_secret_basic(self):
        """Test basic redaction with default visible_chars."""
        secret = "my-api-key-12345"
        redacted = redact_secret(secret)
        # 16 chars total, 4 visible + 12 asterisks
        assert redacted == "my-a************"

    def test_redact_secret_custom_visible_chars(self):
        """Test redaction with custom visible characters."""
        secret = "my-api-key-12345"
        redacted = redact_secret(secret, visible_chars=2)
        # 16 chars total, 2 visible + 14 asterisks
        assert redacted == "my**************"

    def test_redact_secret_zero_visible(self):
        """Test complete redaction with visible_chars=0."""
        secret = "my-secret"
        redacted = redact_secret(secret, visible_chars=0)
        # 9 chars total, all replaced with asterisks
        assert redacted == "*********"

    def test_redact_secret_short_string(self):
        """Test redaction of a string shorter than visible_chars."""
        secret = "abc"
        redacted = redact_secret(secret, visible_chars=4)
        # Should show all chars plus an asterisk
        assert redacted == "abc*"

    def test_redact_secret_none(self):
        """Test redaction of None returns [REDACTED]."""
        redacted = redact_secret(None)
        assert redacted == "[REDACTED]"

    def test_redact_secret_empty_string(self):
        """Test redaction of empty string returns [REDACTED]."""
        redacted = redact_secret("")
        assert redacted == "[REDACTED]"

    def test_redact_secret_exactly_visible_chars(self):
        """Test redaction when len(secret) == visible_chars."""
        secret = "abcd"
        redacted = redact_secret(secret, visible_chars=4)
        assert redacted == "abcd*"

    def test_redact_secret_one_less_than_visible(self):
        """Test redaction when len(secret) == visible_chars - 1."""
        secret = "abc"
        redacted = redact_secret(secret, visible_chars=4)
        assert redacted == "abc*"


class TestKeyringSecrets:
    """Test OS keyring integration (with mocking)."""

    def test_get_keyring_secret_when_unavailable(self):
        """Test that get_keyring_secret returns None when keyring unavailable."""
        if not KEYRING_AVAILABLE:
            secret = get_keyring_secret('test-service', 'test-user')
            assert secret is None

    def test_set_keyring_secret_when_unavailable(self):
        """Test that set_keyring_secret returns False when keyring unavailable."""
        if not KEYRING_AVAILABLE:
            result = set_keyring_secret('test-service', 'test-user', 'password')
            assert result is False

    def test_delete_keyring_secret_when_unavailable(self):
        """Test that delete_keyring_secret returns False when keyring unavailable."""
        if not KEYRING_AVAILABLE:
            result = delete_keyring_secret('test-service', 'test-user')
            assert result is False

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_get_keyring_secret_success(self):
        """Test successful retrieval from keyring."""
        import sys
        from unittest.mock import MagicMock

        # Create a mock keyring module
        mock_keyring = MagicMock()
        mock_keyring.get_password.return_value = 'my-retrieved-secret'

        # Inject it into the secrets module
        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            secret = get_keyring_secret('test-service', 'test-user')
            assert secret == 'my-retrieved-secret'
            mock_keyring.get_password.assert_called_once_with('test-service', 'test-user')
        finally:
            # Restore original
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_get_keyring_secret_not_found(self):
        """Test that get_keyring_secret returns None when secret not found."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()
        mock_keyring.get_password.return_value = None

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            secret = get_keyring_secret('test-service', 'test-user')
            assert secret is None
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_get_keyring_secret_error(self):
        """Test that get_keyring_secret raises RuntimeError on failure."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()
        mock_keyring.get_password.side_effect = Exception("Keyring error")

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            with pytest.raises(RuntimeError, match="Failed to retrieve"):
                get_keyring_secret('test-service', 'test-user')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_set_keyring_secret_success(self):
        """Test successful storage to keyring."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()
        mock_keyring.set_password.return_value = None

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            result = set_keyring_secret('test-service', 'test-user', 'my-password')
            assert result is True
            mock_keyring.set_password.assert_called_once_with('test-service', 'test-user', 'my-password')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_set_keyring_secret_empty_password(self):
        """Test that set_keyring_secret raises ValueError for empty password."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            with pytest.raises(ValueError, match="cannot be empty"):
                set_keyring_secret('test-service', 'test-user', '')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_set_keyring_secret_error(self):
        """Test that set_keyring_secret raises RuntimeError on failure."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()
        mock_keyring.set_password.side_effect = Exception("Keyring error")

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            with pytest.raises(RuntimeError, match="Failed to store"):
                set_keyring_secret('test-service', 'test-user', 'password')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_delete_keyring_secret_success(self):
        """Test successful deletion from keyring."""
        from unittest.mock import MagicMock

        mock_keyring = MagicMock()
        mock_keyring.delete_password.return_value = None

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = mock_keyring

        try:
            result = delete_keyring_secret('test-service', 'test-user')
            assert result is True
            mock_keyring.delete_password.assert_called_once_with('test-service', 'test-user')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_delete_keyring_secret_not_found(self):
        """Test that delete_keyring_secret returns False when secret not found."""
        from types import ModuleType
        from unittest.mock import MagicMock

        # Create a real PasswordDeleteError exception class
        class PasswordDeleteError(Exception):
            pass

        # Create a proper errors module
        errors_module = ModuleType('errors')
        errors_module.PasswordDeleteError = PasswordDeleteError

        # Create keyring module with errors
        keyring_module = ModuleType('keyring')
        keyring_module.errors = errors_module
        keyring_module.delete_password = MagicMock(side_effect=PasswordDeleteError())

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = keyring_module

        try:
            result = delete_keyring_secret('test-service', 'test-user')
            assert result is False
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')

    @patch('binary_sbom.secrets.KEYRING_AVAILABLE', True)
    def test_delete_keyring_secret_error(self):
        """Test that delete_keyring_secret raises RuntimeError on unexpected error."""
        from types import ModuleType
        from unittest.mock import MagicMock

        # Create a proper errors module with PasswordDeleteError
        class PasswordDeleteError(Exception):
            pass

        errors_module = ModuleType('errors')
        errors_module.PasswordDeleteError = PasswordDeleteError

        # Create keyring module with errors
        keyring_module = ModuleType('keyring')
        keyring_module.errors = errors_module
        # Raise a regular exception (not PasswordDeleteError)
        keyring_module.delete_password = MagicMock(side_effect=Exception("Keyring error"))

        import binary_sbom.secrets as secrets_module
        original_keyring = getattr(secrets_module, 'keyring', None)
        secrets_module.keyring = keyring_module

        try:
            with pytest.raises(RuntimeError, match="Failed to delete"):
                delete_keyring_secret('test-service', 'test-user')
        finally:
            if original_keyring:
                secrets_module.keyring = original_keyring
            else:
                delattr(secrets_module, 'keyring')


class TestSecretsIntegration:
    """Integration tests for secrets module workflows."""

    def test_encrypt_decrypt_workflow(self):
        """Test complete encrypt-decrypt workflow."""
        original = "my-super-secret-api-key-12345"
        encrypted = encrypt_secret(original)
        decrypted = decrypt_secret(encrypted)
        assert decrypted == original
        assert encrypted != original

    def test_load_and_encrypt_workflow(self):
        """Test loading from env, encrypting, and decrypting."""
        plaintext = "workflow-test-secret"

        # Simulate storing encrypted secret in environment
        encrypted = encrypt_secret(plaintext)
        with patch.dict(os.environ, {'WORKFLOW_SECRET': encrypted}):
            # Load and decrypt
            loaded = load_secret('WORKFLOW_SECRET', encrypted=True)
            assert loaded == plaintext

    def test_redact_workflow(self):
        """Test redaction for safe logging of secrets."""
        secret = load_secret('NONEXISTENT', default='my-default-key')
        redacted = redact_secret(secret)
        # Should not contain the full secret
        assert 'my-default-key' not in redacted
        # Should show first 4 chars
        assert redacted.startswith('my-d')

    def test_multiple_secrets_same_key(self):
        """Test encrypting multiple secrets with the same key."""
        secret1 = "first-secret-123"
        secret2 = "second-secret-456"

        encrypted1 = encrypt_secret(secret1)
        encrypted2 = encrypt_secret(secret2)

        # Both should decrypt correctly
        assert decrypt_secret(encrypted1) == secret1
        assert decrypt_secret(encrypted2) == secret2

        # Encrypted values should be different
        assert encrypted1 != encrypted2

    def test_environment_key_consistency(self):
        """Test that using same env key produces consistent results."""
        test_key = 'consistent-test-key-123456789012345'

        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': test_key}):
            plaintext = "consistency-test"
            encrypted1 = encrypt_secret(plaintext)

        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': test_key}):
            encrypted2 = encrypt_secret(plaintext)

        # Should be able to decrypt both with the same key
        with patch.dict(os.environ, {'BINARY_SBOM_ENCRYPTION_KEY': test_key}):
            assert decrypt_secret(encrypted1) == plaintext
            assert decrypt_secret(encrypted2) == plaintext
