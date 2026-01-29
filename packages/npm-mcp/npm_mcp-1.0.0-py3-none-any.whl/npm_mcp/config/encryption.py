"""Credential encryption for NPM MCP Server.

This module provides secure encryption/decryption of credentials using
the cryptography library's Fernet symmetric encryption.

Fernet guarantees that a message encrypted using it cannot be manipulated
or read without the key. It uses 128-bit AES in CBC mode and PKCS7 padding,
with HMAC using SHA256 for authentication.
"""

import stat
from pathlib import Path

from cryptography.fernet import Fernet


class CredentialEncryptor:
    """Handles encryption and decryption of credentials.

    Uses Fernet symmetric encryption from the cryptography library.
    Keys can be generated, saved to, and loaded from files.

    Attributes:
        _fernet: Fernet instance for encryption/decryption (None if no key set).
    """

    def __init__(self, key: bytes | None = None) -> None:
        """Initialize the encryptor.

        Args:
            key: Optional encryption key. If not provided, must call generate_key()
                or load_key() before encrypting/decrypting.
        """
        self._fernet: Fernet | None = Fernet(key) if key else None

    def generate_key(self) -> bytes:
        """Generate a new encryption key.

        Returns:
            A new Fernet encryption key (base64-encoded 32 bytes).
        """
        return Fernet.generate_key()

    def save_key(self, key: bytes, key_file: Path) -> None:
        """Save an encryption key to a file.

        The file is created with restrictive permissions (0o600) to ensure
        only the owner can read/write it.

        Args:
            key: The encryption key to save.
            key_file: Path where the key should be saved.
        """
        # Create parent directories if they don't exist
        key_file.parent.mkdir(parents=True, exist_ok=True)

        # Write key to file
        key_file.write_bytes(key)

        # Set restrictive permissions (owner read/write only)
        key_file.chmod(stat.S_IRUSR | stat.S_IWUSR)  # 0o600

    def load_key(self, key_file: Path) -> bytes:
        """Load an encryption key from a file.

        Args:
            key_file: Path to the key file.

        Returns:
            The encryption key.

        Raises:
            FileNotFoundError: If the key file doesn't exist.
        """
        if not key_file.exists():
            msg = f"Encryption key file not found: {key_file}"
            raise FileNotFoundError(msg)

        return key_file.read_bytes()

    def encrypt(self, plaintext: str) -> str:
        """Encrypt a plaintext string.

        Args:
            plaintext: The string to encrypt (e.g., a password).

        Returns:
            Base64-encoded encrypted string.

        Raises:
            ValueError: If no encryption key has been set.
        """
        if self._fernet is None:
            msg = "No encryption key set. Call generate_key() or load_key() first."
            raise ValueError(msg)

        encrypted_bytes = self._fernet.encrypt(plaintext.encode("utf-8"))
        return encrypted_bytes.decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        """Decrypt an encrypted string.

        Args:
            ciphertext: The base64-encoded encrypted string.

        Returns:
            The decrypted plaintext string.

        Raises:
            ValueError: If no encryption key has been set.
            InvalidToken: If the ciphertext is invalid or was encrypted with a
                different key.
        """
        if self._fernet is None:
            msg = "No encryption key set. Call generate_key() or load_key() first."
            raise ValueError(msg)

        decrypted_bytes = self._fernet.decrypt(ciphertext.encode("utf-8"))
        return decrypted_bytes.decode("utf-8")
