"""Authentication manager for NPM MCP Server.

This module provides JWT token-based authentication for NPM instances:
- Token generation via NPM API
- Token parsing and validation
- Token expiration detection
- In-memory token caching
- Optional disk token caching (encrypted)
- Multi-instance token management

Usage:
    from npm_mcp.auth.manager import AuthManager
    from npm_mcp.auth.token_cache import TokenCache

    # Without disk caching (memory-only)
    auth_manager = AuthManager(config)
    token = await auth_manager.get_valid_token("production")

    # With disk caching
    token_cache = TokenCache(cache_dir=Path.home() / ".npm-mcp" / "tokens", encryptor=encryptor)
    auth_manager = AuthManager(config, token_cache=token_cache)
    token = await auth_manager.get_valid_token("production")
"""

import base64
import json
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

import httpx
import structlog

from npm_mcp.config.models import Config, InstanceConfig

if TYPE_CHECKING:
    from npm_mcp.auth.token_cache import TokenCache

logger = structlog.get_logger(__name__)

# JWT token constants
JWT_PARTS_COUNT = 3  # JWT format: header.payload.signature
BASE64_PADDING_MODULO = 4  # Base64 requires padding to be a multiple of 4


class AuthManager:
    """Manages authentication for NPM instances.

    Handles JWT token generation, validation, caching, and expiration checking
    for all configured NPM instances.

    Attributes:
        config: The complete NPM MCP configuration.
        _token_cache: In-memory cache of JWT tokens by instance name.
        _token_cache_disk: Optional disk-based token cache for persistence.
    """

    def __init__(self, config: Config, token_cache: "TokenCache | None" = None) -> None:
        """Initialize the authentication manager.

        Args:
            config: Complete NPM MCP configuration containing instances and settings.
            token_cache: Optional TokenCache for encrypted disk-based token persistence.
                        If None, tokens are only cached in memory.
        """
        self.config = config
        self._token_cache: dict[str, str] = {}
        self._token_cache_disk = token_cache

        # Load tokens from disk cache if available
        if self._token_cache_disk is not None:
            self._load_tokens_from_disk()

        logger.info(
            "auth_manager_initialized",
            num_instances=len(config.instances),
            disk_cache_enabled=token_cache is not None,
        )

    def _load_tokens_from_disk(self) -> None:
        """Load all valid tokens from disk cache into memory.

        Iterates through all configured instances and attempts to load
        their cached tokens from disk. Only valid (non-expired) tokens
        are loaded into memory.
        """
        if self._token_cache_disk is None:
            return

        for instance in self.config.instances:
            token = self._token_cache_disk.load_token(instance.name)
            if token is not None:
                # Token is valid and not expired (verified by TokenCache)
                self._token_cache[instance.name] = token
                logger.debug(
                    "token_loaded_from_disk_to_memory",
                    instance_name=instance.name,
                )

    def _parse_token(self, token: str) -> dict[str, Any]:
        """Parse a JWT token and extract the payload.

        Args:
            token: The JWT token string in format: header.payload.signature

        Returns:
            Dictionary containing the token payload with claims.

        Raises:
            ValueError: If token format is invalid or cannot be decoded.
        """
        try:
            # JWT format: header.payload.signature
            parts = token.split(".")
            if len(parts) != JWT_PARTS_COUNT:
                msg = f"Invalid JWT token format: expected {JWT_PARTS_COUNT} parts"
                raise ValueError(msg)

            # Decode payload (second part)
            payload_b64 = parts[1]

            # Add padding if necessary for base64 decoding
            padding = BASE64_PADDING_MODULO - len(payload_b64) % BASE64_PADDING_MODULO
            if padding != BASE64_PADDING_MODULO:
                payload_b64 += "=" * padding

            payload_bytes = base64.urlsafe_b64decode(payload_b64)
            payload: dict[str, Any] = json.loads(payload_bytes)

            logger.debug("token_parsed", has_exp="exp" in payload, has_email="email" in payload)
            return payload

        except ValueError as e:
            # json.JSONDecodeError inherits from ValueError
            logger.error("token_parse_failed", error=str(e))
            msg = f"Invalid JWT token: {e}"
            raise ValueError(msg) from e

    def is_token_expired(self, token: str) -> bool:
        """Check if a JWT token is expired.

        Args:
            token: The JWT token to check.

        Returns:
            True if the token is expired, False otherwise.

        Raises:
            ValueError: If token is invalid or missing expiration claim.
        """
        try:
            payload = self._parse_token(token)

            if "exp" not in payload:
                msg = "Token missing expiration claim"
                raise ValueError(msg)

            exp_timestamp = payload["exp"]
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=UTC)
            now = datetime.now(UTC)

            is_expired = now >= exp_datetime

            logger.debug(
                "token_expiration_checked",
                is_expired=is_expired,
                expires_at=exp_datetime.isoformat(),
            )

            return is_expired

        except (ValueError, KeyError) as e:
            logger.error("token_expiration_check_failed", error=str(e))
            raise

    def is_token_expiring_soon(self, token: str, buffer_minutes: int = 5) -> bool:
        """Check if a token will expire soon.

        Args:
            token: The JWT token to check.
            buffer_minutes: Number of minutes to consider as "expiring soon".

        Returns:
            True if token expires within buffer_minutes, False otherwise.

        Raises:
            ValueError: If token is invalid or missing expiration claim.
        """
        try:
            payload = self._parse_token(token)

            if "exp" not in payload:
                msg = "Token missing expiration claim"
                raise ValueError(msg)

            exp_timestamp = payload["exp"]
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=UTC)
            now = datetime.now(UTC)

            # Check if token expires within the buffer period
            buffer_delta = timedelta(minutes=buffer_minutes)
            is_expiring_soon = exp_datetime <= now + buffer_delta

            logger.debug(
                "token_expiring_soon_checked",
                is_expiring_soon=is_expiring_soon,
                buffer_minutes=buffer_minutes,
                expires_at=exp_datetime.isoformat(),
            )

            return is_expiring_soon

        except (ValueError, KeyError) as e:
            logger.error("token_expiring_soon_check_failed", error=str(e))
            raise

    def _has_credentials(self, instance: InstanceConfig) -> bool:
        """Check if an instance has authentication credentials configured.

        Args:
            instance: The instance configuration to check.

        Returns:
            True if the instance has credentials (username/password or api_token).
        """
        has_username_password = instance.username is not None and instance.password is not None
        has_api_token = instance.api_token is not None

        return has_username_password or has_api_token

    def _get_instance_by_name(self, instance_name: str) -> InstanceConfig:
        """Get instance configuration by name.

        Args:
            instance_name: Name of the instance to find.

        Returns:
            The instance configuration.

        Raises:
            ValueError: If instance not found.
        """
        for instance in self.config.instances:
            if instance.name == instance_name:
                return instance

        msg = f"Instance '{instance_name}' not found in configuration"
        raise ValueError(msg)

    async def authenticate(self, instance_name: str) -> str:
        """Authenticate with NPM instance and get JWT token.

        Makes a POST request to /api/tokens with credentials and returns
        the JWT token from the response.

        Args:
            instance_name: Name of the instance to authenticate with.

        Returns:
            JWT token string.

        Raises:
            ValueError: If instance not found or credentials missing.
            httpx.HTTPStatusError: If authentication fails (401, 500, etc.).
            httpx.ConnectError: If connection to NPM instance fails.
            httpx.TimeoutException: If request times out.
            KeyError: If response doesn't contain expected 'token' field.
        """
        # Get instance configuration
        instance = self._get_instance_by_name(instance_name)

        # Validate credentials
        if not self._has_credentials(instance):
            logger.error(
                "authentication_failed_no_credentials",
                instance_name=instance_name,
            )
            msg = (
                f"No credentials configured for instance '{instance_name}'. "
                "Please provide username/password or api_token."
            )
            raise ValueError(msg)

        # If instance has pre-configured API token, skip authentication
        if instance.api_token:
            logger.info(
                "using_preconfigured_token",
                instance_name=instance_name,
            )
            # Cache and return the pre-configured token
            self._token_cache[instance_name] = instance.api_token
            return instance.api_token

        # Build authentication URL
        scheme = "https" if instance.use_https else "http"
        url = f"{scheme}://{instance.host}:{instance.port}/api/tokens"

        # Prepare authentication request
        auth_data = {
            "identity": instance.username,
            "secret": instance.password,
        }

        logger.info(
            "authenticating",
            instance_name=instance_name,
            url=url,
            username=instance.username,
        )

        # Make authentication request
        async with httpx.AsyncClient(
            timeout=self.config.settings.default_timeout,
            verify=instance.verify_ssl,
        ) as client:
            try:
                response = await client.post(url, json=auth_data)

                # Raise exception for HTTP errors
                response.raise_for_status()

                # Parse response
                response_data = response.json()
                token: str = response_data["token"]

                # Cache token in memory
                self._token_cache[instance_name] = token

                # Cache token to disk if disk cache is enabled
                if self._token_cache_disk is not None:
                    self._token_cache_disk.save_token(instance_name, token)

                logger.info(
                    "authentication_successful",
                    instance_name=instance_name,
                    token_length=len(token),
                )

                return token

            except httpx.HTTPStatusError as e:
                logger.error(
                    "authentication_http_error",
                    instance_name=instance_name,
                    status_code=e.response.status_code,
                    error=str(e),
                )
                raise

            except httpx.ConnectError as e:
                logger.error(
                    "authentication_connection_error",
                    instance_name=instance_name,
                    url=url,
                    error=str(e),
                )
                raise

            except httpx.TimeoutException as e:
                logger.error(
                    "authentication_timeout",
                    instance_name=instance_name,
                    url=url,
                    error=str(e),
                )
                raise

            except KeyError as e:
                logger.error(
                    "authentication_invalid_response",
                    instance_name=instance_name,
                    error=f"Response missing '{e}' field",
                )
                raise

    async def get_valid_token(self, instance_name: str) -> str:
        """Get a valid JWT token for an instance.

        Returns a cached token if available and not expired, otherwise
        authenticates and returns a new token. Checks both memory cache
        and disk cache (if enabled) before authenticating.

        Args:
            instance_name: Name of the instance.

        Returns:
            Valid JWT token string.

        Raises:
            ValueError: If instance not found or credentials missing.
            httpx exceptions: If authentication fails.
        """
        # Check if we have a cached token in memory
        if instance_name in self._token_cache:
            cached_token = self._token_cache[instance_name]

            try:
                # Check if cached token is still valid
                if not self.is_token_expired(cached_token):
                    logger.debug(
                        "using_cached_token",
                        instance_name=instance_name,
                    )
                    return cached_token
                logger.info(
                    "cached_token_expired",
                    instance_name=instance_name,
                )
            except ValueError:
                # Invalid token format, remove from cache
                logger.warning(
                    "cached_token_invalid",
                    instance_name=instance_name,
                )
                del self._token_cache[instance_name]

        # Check disk cache if available
        if self._token_cache_disk is not None:
            disk_token = self._token_cache_disk.load_token(instance_name)
            if disk_token is not None:
                # Token is valid (TokenCache validates expiration)
                # Load into memory cache
                self._token_cache[instance_name] = disk_token
                logger.debug(
                    "using_disk_cached_token",
                    instance_name=instance_name,
                )
                return disk_token

        # No valid cached token, authenticate
        logger.info(
            "no_valid_cached_token_authenticating",
            instance_name=instance_name,
        )
        return await self.authenticate(instance_name)

    async def get_valid_token_with_refresh(
        self, instance_name: str, buffer_minutes: int = 5
    ) -> str:
        """Get a valid JWT token with proactive refresh.

        Similar to get_valid_token(), but proactively refreshes tokens that
        are expiring soon (within buffer_minutes). This prevents token
        expiration during long-running operations.

        Args:
            instance_name: Name of the instance.
            buffer_minutes: Number of minutes before expiration to trigger
                          proactive refresh. Default is 5 minutes.

        Returns:
            Valid JWT token string.

        Raises:
            ValueError: If instance not found or credentials missing.
            httpx exceptions: If authentication fails.
        """
        # First, get a valid token (from cache or authenticate)
        token = await self.get_valid_token(instance_name)

        # Check if token is expiring soon
        try:
            if self.is_token_expiring_soon(token, buffer_minutes=buffer_minutes):
                logger.info(
                    "token_expiring_soon_refreshing",
                    instance_name=instance_name,
                    buffer_minutes=buffer_minutes,
                )
                # Refresh the token by re-authenticating
                token = await self.authenticate(instance_name)
        except ValueError:
            # Token is invalid, get_valid_token should have handled it
            # but just in case, re-authenticate
            logger.warning(
                "invalid_token_during_refresh_check",
                instance_name=instance_name,
            )
            token = await self.authenticate(instance_name)

        return token

    def cleanup(self) -> None:
        """Clean up authentication manager resources.

        Performs cleanup tasks:
        - Flushes in-memory token cache
        - Saves valid tokens to disk cache (if enabled)
        - Closes any open connections

        This method should be called during server shutdown to ensure
        tokens are properly persisted.
        """
        logger.info("auth_manager_cleanup_started")

        # Save valid tokens to disk if disk cache is enabled
        if self._token_cache_disk is not None:
            for instance_name, token in self._token_cache.items():
                try:
                    # Only save non-expired tokens
                    if not self.is_token_expired(token):
                        self._token_cache_disk.save_token(instance_name, token)
                        logger.debug(
                            "token_saved_to_disk",
                            instance_name=instance_name,
                        )
                except ValueError:
                    # Invalid token format - skip
                    logger.warning(
                        "invalid_token_skipped_during_cleanup",
                        instance_name=instance_name,
                    )

        # Clear in-memory cache
        self._token_cache.clear()
        logger.info("auth_manager_cleanup_completed")
