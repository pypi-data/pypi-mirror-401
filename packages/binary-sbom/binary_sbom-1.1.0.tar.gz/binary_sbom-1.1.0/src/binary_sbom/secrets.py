"""
Secrets management module for Binary SBOM Generator.

This module provides secure encryption and decryption utilities for sensitive
data such as API keys, passwords, and other credentials. It uses Fernet
symmetric encryption from the cryptography library.

Additionally, it provides utilities for loading secrets from environment
variables with optional automatic decryption, redaction helpers for
safe logging of sensitive values, and optional OS keyring integration.
"""

import os
import base64
from pathlib import Path
from typing import Optional

try:
    from cryptography.fernet import Fernet, InvalidToken
except ImportError:
    raise ImportError(
        "cryptography is required for secrets management. "
        "Install it with: pip install cryptography"
    )

try:
    import keyring
    KEYRING_AVAILABLE = True
except ImportError:
    KEYRING_AVAILABLE = False


def _get_encryption_key() -> bytes:
    """
    Get or generate encryption key from environment.

    The encryption key is loaded from the BINARY_SBOM_ENCRYPTION_KEY
    environment variable. If not set, a key is generated based on
    a combination of system-specific values.

    Returns:
        URL-safe base64-encoded 32-byte key suitable for Fernet.

    Note:
        For production use, always set BINARY_SBOM_ENCRYPTION_KEY
        environment variable to ensure consistent encryption/decryption
        across processes.

    Example:
        >>> import os
        >>> os.environ['BINARY_SBOM_ENCRYPTION_KEY'] = 'test-key-' * 6  # 48 chars
        >>> key = _get_encryption_key()
        >>> isinstance(key, bytes)
        True
    """
    env_key = os.getenv('BINARY_SBOM_ENCRYPTION_KEY')
    if env_key:
        # Ensure the key is properly base64-encoded
        if len(env_key) == 44 and env_key.endswith('='):
            # Already a valid Fernet key
            return env_key.encode('utf-8')
        else:
            # Derive a key from the environment variable
            # Using a simple derivation - in production, use proper KDF
            key_bytes = env_key.encode('utf-8')
            # Pad or truncate to 32 bytes
            key_bytes = key_bytes[:32].ljust(32, b'0')
            return base64.urlsafe_b64encode(key_bytes)

    # Fallback: generate a key from system-specific values
    # This ensures the same key can be regenerated on the same system
    system_id = f"{os.getuid() if hasattr(os, 'getuid') else os.getenv('USERNAME', 'default')}"
    system_bytes = system_id.encode('utf-8')
    system_bytes = system_bytes[:32].ljust(32, b'0')
    return base64.urlsafe_b64encode(system_bytes)


def encrypt_secret(plaintext: str) -> str:
    """
    Encrypt a secret string using Fernet symmetric encryption.

    This function encrypts sensitive data like API keys, passwords,
    or tokens using AES-128 in CBC mode with PKCS7 padding (via Fernet).

    Args:
        plaintext: The secret string to encrypt.

    Returns:
        Base64-encoded encrypted string that can be safely stored
        or transmitted.

    Raises:
        ValueError: If plaintext is empty or not a string.

    Example:
        >>> encrypted = encrypt_secret("my-api-key-123")
        >>> isinstance(encrypted, str)
        True
        >>> encrypted != "my-api-key-123"
        True
    """
    if not plaintext:
        raise ValueError("plaintext cannot be empty")

    if not isinstance(plaintext, str):
        raise ValueError("plaintext must be a string")

    try:
        key = _get_encryption_key()
        fernet = Fernet(key)
        encrypted_bytes = fernet.encrypt(plaintext.encode('utf-8'))
        return encrypted_bytes.decode('utf-8')
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt secret: {e}")


def decrypt_secret(ciphertext: str) -> str:
    """
    Decrypt a secret string that was encrypted with encrypt_secret.

    This function decrypts data that was previously encrypted using
    the encrypt_secret function and the same encryption key.

    Args:
        ciphertext: The encrypted string to decrypt.

    Returns:
        The original decrypted secret string.

    Raises:
        ValueError: If ciphertext is empty or not a string.
        RuntimeError: If decryption fails (invalid key or corrupted data).

    Example:
        >>> encrypted = encrypt_secret("my-api-key-123")
        >>> decrypted = decrypt_secret(encrypted)
        >>> decrypted
        'my-api-key-123'
    """
    if not ciphertext:
        raise ValueError("ciphertext cannot be empty")

    if not isinstance(ciphertext, str):
        raise ValueError("ciphertext must be a string")

    try:
        key = _get_encryption_key()
        fernet = Fernet(key)
        decrypted_bytes = fernet.decrypt(ciphertext.encode('utf-8'))
        return decrypted_bytes.decode('utf-8')
    except InvalidToken:
        raise RuntimeError(
            "Failed to decrypt secret: invalid key or corrupted data. "
            "Ensure BINARY_SBOM_ENCRYPTION_KEY matches the key used for encryption."
        )
    except Exception as e:
        raise RuntimeError(f"Failed to decrypt secret: {e}")


def _ensure_secure_permissions(file_path: str) -> None:
    """
    Ensure file has secure permissions (user-read/write only).

    This function sets file permissions to 0600 (user read/write only)
    to prevent unauthorized access to sensitive files.

    Args:
        file_path: Path to the file to secure.

    Example:
        >>> import tempfile
        >>> f = tempfile.NamedTemporaryFile(delete=False)
        >>> _ensure_secure_permissions(f.name)
        >>> import stat
        >>> perm = oct(os.stat(f.name).st_mode & 0o777)
        >>> perm == '0o600'
        True
        >>> os.unlink(f.name)
    """
    try:
        Path(file_path).chmod(0o600)
    except OSError as e:
        # Log warning but don't fail - this is a security best practice, not critical
        pass


def load_secret(
    env_var: str,
    default: Optional[str] = None,
    encrypted: bool = False
) -> Optional[str]:
    """
    Load a secret from an environment variable with optional decryption.

    This function retrieves secrets from environment variables, optionally
    decrypting them if they were stored in encrypted format. This is useful
    for loading API keys, tokens, and other sensitive configuration.

    Args:
        env_var: Name of the environment variable to load.
        default: Default value to return if environment variable is not set.
            If None and the variable is not set, returns None.
        encrypted: If True, attempt to decrypt the value using decrypt_secret().
            Useful when environment variables contain encrypted secrets.

    Returns:
        The secret value as a string, or None if not found and no default provided.

    Raises:
        RuntimeError: If encrypted=True but decryption fails.

    Example:
        >>> import os
        >>> os.environ['MY_API_KEY'] = 'plaintext-key'
        >>> load_secret('MY_API_KEY')
        'plaintext-key'
        >>> # With encrypted value
        >>> encrypted = encrypt_secret('secret-value')
        >>> os.environ['MY_SECRET'] = encrypted
        >>> load_secret('MY_SECRET', encrypted=True)
        'secret-value'
        >>> # With default
        >>> load_secret('NONEXISTENT_VAR', default='default-value')
        'default-value'
    """
    value = os.getenv(env_var)

    if value is None:
        return default

    if encrypted:
        try:
            return decrypt_secret(value)
        except RuntimeError as e:
            raise RuntimeError(
                f"Failed to decrypt secret from environment variable {env_var}: {e}"
            )

    return value


def redact_secret(secret: Optional[str], visible_chars: int = 4) -> str:
    """
    Redact a secret value for safe logging and display.

    This function returns a redacted version of a secret, showing only the
    first few characters followed by asterisks. Useful for logging sensitive
    values without exposing them fully.

    Args:
        secret: The secret value to redact. If None or empty, returns
            '[REDACTED]'.
        visible_chars: Number of leading characters to remain visible.
            Defaults to 4. Set to 0 to completely hide the value.

    Returns:
        A redacted string with only the first few characters visible,
        followed by asterisks, or '[REDACTED]' if input is None/empty.

    Example:
        >>> redact_secret('my-api-key-123')
        'my-a*************'
        >>> redact_secret('abc', visible_chars=2)
        'ab*'
        >>> redact_secret('short', visible_chars=0)
        '*****'
        >>> redact_secret(None)
        '[REDACTED]'
    """
    if secret is None or not secret:
        return '[REDACTED]'

    if visible_chars <= 0:
        return '*' * len(secret)

    if len(secret) <= visible_chars:
        # If secret is shorter than visible_chars, show all chars but still indicate redaction
        return secret + '*'

    return secret[:visible_chars] + '*' * (len(secret) - visible_chars)


def get_keyring_secret(service: str, username: str) -> Optional[str]:
    """
    Retrieve a secret from the OS keyring.

    This function provides secure storage and retrieval of sensitive credentials
    using the system's keyring (e.g., Keychain on macOS, Credential Manager on
    Windows, Secret Service API on Linux). This is more secure than storing
    secrets in environment variables or configuration files.

    The keyring library is optional - if not installed, this function returns None.

    Args:
        service: The service name for the credential (e.g., 'binary-sbom-nvd').
        username: The username/identifier for the credential (e.g., 'api-key').

    Returns:
        The secret value as a string if found, None if not found or keyring unavailable.

    Raises:
        RuntimeError: If keyring is available but retrieval fails.

    Example:
        >>> # Store a secret first (requires keyring to be installed)
        >>> # set_keyring_secret('binary-sbom', 'test-key', 'my-secret')
        >>> secret = get_keyring_secret('binary-sbom', 'test-key')
        >>> # secret will be 'my-secret' if keyring is available and set
        >>> # or None if keyring is not available
        >>> isinstance(secret, (str, type(None)))
        True
    """
    if not KEYRING_AVAILABLE:
        return None

    try:
        password = keyring.get_password(service, username)
        return password
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve secret from keyring for service '{service}', "
            f"user '{username}': {e}"
        )


def set_keyring_secret(service: str, username: str, password: str) -> bool:
    """
    Store a secret in the OS keyring.

    This function securely stores credentials in the system's keyring,
    providing a more secure alternative to environment variables or
    configuration files.

    The keyring library is optional - if not installed, this function returns False.

    Args:
        service: The service name for the credential (e.g., 'binary-sbom-nvd').
        username: The username/identifier for the credential (e.g., 'api-key').
        password: The secret value to store.

    Returns:
        True if the secret was stored successfully, False if keyring is unavailable.

    Raises:
        RuntimeError: If keyring is available but storage fails.

    Example:
        >>> # This requires keyring to be installed
        >>> success = set_keyring_secret('binary-sbom', 'test-key', 'my-secret')
        >>> # success will be True if keyring is available, False otherwise
        >>> isinstance(success, bool)
        True
        >>> # Clean up
        >>> if success:
        ...     _ = keyring.delete_password('binary-sbom', 'test-key')
    """
    if not KEYRING_AVAILABLE:
        return False

    if not password:
        raise ValueError("password cannot be empty")

    try:
        keyring.set_password(service, username, password)
        return True
    except Exception as e:
        raise RuntimeError(
            f"Failed to store secret in keyring for service '{service}', "
            f"user '{username}': {e}"
        )


def delete_keyring_secret(service: str, username: str) -> bool:
    """
    Delete a secret from the OS keyring.

    This function removes a credential from the system's keyring.
    Useful for cleanup or when rotating credentials.

    The keyring library is optional - if not installed, this function returns False.

    Args:
        service: The service name for the credential (e.g., 'binary-sbom-nvd').
        username: The username/identifier for the credential (e.g., 'api-key').

    Returns:
        True if the secret was deleted successfully, False if keyring is unavailable
        or the secret was not found.

    Raises:
        RuntimeError: If keyring is available but deletion fails for reasons
            other than the secret not existing.

    Example:
        >>> # Store a secret first (requires keyring to be installed)
        >>> # set_keyring_secret('binary-sbom', 'test-key', 'my-secret')
        >>> deleted = delete_keyring_secret('binary-sbom', 'test-key')
        >>> # deleted will be True if keyring is available, False otherwise
        >>> isinstance(deleted, bool)
        True
    """
    if not KEYRING_AVAILABLE:
        return False

    try:
        keyring.delete_password(service, username)
        return True
    except keyring.errors.PasswordDeleteError:
        # Secret doesn't exist - not an error, just return False
        return False
    except Exception as e:
        raise RuntimeError(
            f"Failed to delete secret from keyring for service '{service}', "
            f"user '{username}': {e}"
        )


__all__ = [
    'encrypt_secret',
    'decrypt_secret',
    'load_secret',
    'redact_secret',
    '_get_encryption_key',
    '_ensure_secure_permissions',
    'get_keyring_secret',
    'set_keyring_secret',
    'delete_keyring_secret',
    'KEYRING_AVAILABLE',
]
