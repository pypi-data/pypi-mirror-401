"""Token cache with encrypted disk storage for NPM MCP Server.

This module provides encrypted token caching to disk:
- Per-instance token files
- Automatic cache directory creation
- Token expiration validation on load
- Secure encryption using CredentialEncryptor

Usage:
    from npm_mcp.auth.token_cache import TokenCache
    from npm_mcp.config.encryption import CredentialEncryptor

    encryptor = CredentialEncryptor(key=encryption_key)
    cache = TokenCache(cache_dir=Path.home() / ".npm-mcp" / "tokens", encryptor=encryptor)

    # Save token
    cache.save_token("production", jwt_token)

    # Load token
    token = cache.load_token("production")

    # Delete token
    cache.delete_token("production")

    # Clear all tokens
    cache.clear_all()
"""

import base64
import json
from datetime import UTC, datetime
from pathlib import Path

import structlog
from cryptography.fernet import InvalidToken

from npm_mcp.config.encryption import CredentialEncryptor

logger = structlog.get_logger(__name__)


class TokenCache:
    """Manages encrypted token caching to disk.

    Provides secure storage and retrieval of JWT tokens with automatic
    expiration validation and per-instance file management.

    Attributes:
        cache_dir: Directory where token cache files are stored.
        encryptor: CredentialEncryptor instance for encryption/decryption.
    """

    def __init__(self, cache_dir: Path, encryptor: CredentialEncryptor) -> None:
        """Initialize the token cache.

        Args:
            cache_dir: Directory path for storing cached tokens.
            encryptor: CredentialEncryptor instance for token encryption.
        """
        self.cache_dir = cache_dir
        self.encryptor = encryptor
        logger.info("token_cache_initialized", cache_dir=str(cache_dir))

    def _get_cache_file_path(self, instance_name: str) -> Path:
        """Get the cache file path for an instance.

        Args:
            instance_name: Name of the NPM instance.

        Returns:
            Path to the cache file for this instance.
        """
        return self.cache_dir / f"{instance_name}.token"

    def _is_token_expired(self, token: str) -> bool:
        """Check if a token is expired.

        Args:
            token: The JWT token to check.

        Returns:
            True if the token is expired or invalid, False otherwise.
        """
        try:
            # Parse JWT token (format: header.payload.signature)
            parts = token.split(".")
            if len(parts) != 3:
                return True

            # Decode payload (second part)
            payload_b64 = parts[1]

            # Add padding if necessary
            padding = 4 - len(payload_b64) % 4
            if padding != 4:
                payload_b64 += "=" * padding

            payload_bytes = base64.urlsafe_b64decode(payload_b64)
            payload = json.loads(payload_bytes)

            # Check expiration
            if "exp" not in payload:
                return True

            exp_timestamp = payload["exp"]
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=UTC)
            now = datetime.now(UTC)

            return now >= exp_datetime

        except (ValueError, KeyError):
            # Invalid token format (json.JSONDecodeError inherits from ValueError)
            return True

    def save_token(self, instance_name: str, token: str) -> None:
        """Save an encrypted token to disk.

        Args:
            instance_name: Name of the NPM instance.
            token: The JWT token to save.
        """
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Encrypt token
        encrypted_token = self.encryptor.encrypt(token)

        # Write to cache file
        cache_file = self._get_cache_file_path(instance_name)
        cache_file.write_text(encrypted_token)

        logger.info(
            "token_saved_to_cache",
            instance_name=instance_name,
            cache_file=str(cache_file),
        )

    def load_token(self, instance_name: str) -> str | None:
        """Load and decrypt a token from disk.

        Validates token expiration before returning. Returns None if the token
        is expired, invalid, or doesn't exist.

        Args:
            instance_name: Name of the NPM instance.

        Returns:
            The decrypted JWT token if valid, None otherwise.
        """
        cache_file = self._get_cache_file_path(instance_name)

        # Check if cache file exists
        if not cache_file.exists():
            logger.debug(
                "token_cache_miss",
                instance_name=instance_name,
                reason="file_not_found",
            )
            return None

        try:
            # Read encrypted token
            encrypted_token = cache_file.read_text()

            # Decrypt token
            token = self.encryptor.decrypt(encrypted_token)

            # Validate token expiration
            if self._is_token_expired(token):
                logger.info(
                    "cached_token_expired",
                    instance_name=instance_name,
                )
                return None

            logger.debug(
                "token_loaded_from_cache",
                instance_name=instance_name,
            )
            return token

        except InvalidToken:
            logger.warning(
                "token_cache_decryption_failed",
                instance_name=instance_name,
                reason="invalid_encryption",
            )
            return None

        except ValueError:
            # json.JSONDecodeError inherits from ValueError
            logger.warning(
                "token_cache_load_failed",
                instance_name=instance_name,
                reason="invalid_token_format",
            )
            return None

    def delete_token(self, instance_name: str) -> None:
        """Delete a cached token from disk.

        Args:
            instance_name: Name of the NPM instance.
        """
        cache_file = self._get_cache_file_path(instance_name)

        if cache_file.exists():
            cache_file.unlink()
            logger.info(
                "token_deleted_from_cache",
                instance_name=instance_name,
            )
        else:
            logger.debug(
                "token_delete_skip_not_found",
                instance_name=instance_name,
            )

    def clear_all(self) -> None:
        """Clear all cached tokens from disk.

        Deletes all .token files in the cache directory.
        """
        if not self.cache_dir.exists():
            logger.debug("cache_dir_not_found_skip_clear")
            return

        # Delete all .token files
        token_files = list(self.cache_dir.glob("*.token"))

        for token_file in token_files:
            token_file.unlink()

        logger.info("all_tokens_cleared", count=len(token_files))
