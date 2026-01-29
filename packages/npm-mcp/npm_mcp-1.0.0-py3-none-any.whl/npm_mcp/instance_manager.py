"""
Instance Manager for multi-instance NPM management.

This module provides:
- NPM client connection pooling and reuse
- Instance selection (active instance context)
- Dynamic instance management (add/remove)
- Connection testing and validation
- Resource cleanup on shutdown

The InstanceManager is a key component of the MCP server, providing efficient
management of multiple NPM instances with connection pooling to minimize
HTTP overhead.

Usage:
    from npm_mcp.instance_manager import InstanceManager
    from npm_mcp.config.models import Config
    from npm_mcp.auth.manager import AuthManager

    config = load_config()
    auth_manager = AuthManager(config)
    instance_manager = InstanceManager(config, auth_manager)

    # Get client for specific instance
    client = await instance_manager.get_client("prod")

    # Select active instance
    instance_manager.select_instance("staging")

    # Get client for active instance
    client = await instance_manager.get_client()

    # Cleanup on shutdown
    await instance_manager.cleanup()
"""

import asyncio
import time
from typing import Any

import structlog

from npm_mcp.auth.manager import AuthManager
from npm_mcp.client.npm_client import NPMClient
from npm_mcp.config.models import Config, InstanceConfig

logger = structlog.get_logger(__name__)


class InstanceManager:
    """
    Manages NPM instances and their connections.

    The InstanceManager handles:
    - Connection pooling for NPM clients (one client per instance)
    - Client caching and reuse to minimize HTTP overhead
    - Active instance selection for session-wide context
    - Dynamic instance addition and removal
    - Connection testing and validation
    - Graceful cleanup of all connections

    Attributes:
        config: Application configuration with instance definitions
        auth_manager: Authentication manager for token handling
        _clients: Cache of NPM clients by instance name
        _active_instance: Name of currently selected instance
        _client_lock: Asyncio lock for thread-safe client creation
    """

    def __init__(self, config: Config, auth_manager: AuthManager) -> None:
        """
        Initialize Instance Manager.

        Args:
            config: Application configuration with instance definitions
            auth_manager: Authentication manager for JWT tokens
        """
        self.config = config
        self.auth_manager = auth_manager
        self._clients: dict[str, NPMClient] = {}
        self._active_instance: str | None = None
        self._client_lock = asyncio.Lock()

        logger.info(
            "instance_manager_initialized",
            instance_count=len(config.instances),
            instances=[instance.name for instance in config.instances],
        )

    async def get_client(self, instance_name: str | None = None) -> NPMClient:
        """
        Get NPM client for specified instance or active instance.

        This method implements connection pooling by caching NPMClient instances.
        If a client for the requested instance already exists, it is returned.
        Otherwise, a new client is created, cached, and returned.

        Instance selection logic:
        1. If instance_name is provided, use that instance
        2. Else if active instance is set, use active instance
        3. Else use default instance from config

        Args:
            instance_name: Target instance name (optional, uses active instance)

        Returns:
            NPM client for the specified instance

        Raises:
            ValueError: If instance not found in configuration
        """
        # Determine which instance to use
        target_instance_name = self._resolve_instance_name(instance_name)

        # Get instance config
        instance_config = self.config.get_instance(target_instance_name)
        if instance_config is None:
            msg = f"Instance '{target_instance_name}' not found in configuration"
            logger.error("instance_not_found", instance_name=target_instance_name)
            raise ValueError(msg)

        # Check if client is already cached
        if target_instance_name in self._clients:
            logger.debug(
                "reusing_cached_client",
                instance_name=target_instance_name,
            )
            return self._clients[target_instance_name]

        # Create new client (with lock to prevent race conditions)
        async with self._client_lock:
            # Double-check after acquiring lock (another coroutine may have created it)
            if target_instance_name in self._clients:
                return self._clients[target_instance_name]

            logger.info(
                "creating_new_npm_client",
                instance_name=target_instance_name,
                host=instance_config.host,
                port=instance_config.port,
            )

            # Create and cache the client
            client = NPMClient(instance_config, self.auth_manager)
            self._clients[target_instance_name] = client

            logger.info(
                "npm_client_created",
                instance_name=target_instance_name,
                cached_clients_count=len(self._clients),
            )

            return client

    def _resolve_instance_name(self, instance_name: str | None) -> str:
        """
        Resolve instance name using selection logic.

        Selection logic:
        1. If instance_name is provided, use it
        2. Else if active instance is set, use active instance
        3. Else use default instance from config

        Args:
            instance_name: Requested instance name (optional)

        Returns:
            Resolved instance name

        Raises:
            ValueError: If no instance can be resolved
        """
        if instance_name is not None:
            return instance_name

        if self._active_instance is not None:
            return self._active_instance

        # Use default instance
        default_instance = self.config.get_default_instance()
        if default_instance is None:
            msg = "No instance specified and no default instance configured"
            raise ValueError(msg)

        return default_instance.name

    def select_instance(self, instance_name: str) -> None:
        """
        Set the active instance for subsequent operations.

        The active instance is used by get_client() when no specific instance
        is requested. This provides a session-wide context for instance selection.

        Args:
            instance_name: Name of instance to set as active

        Raises:
            ValueError: If instance not found in configuration
        """
        # Validate instance exists
        instance_config = self.config.get_instance(instance_name)
        if instance_config is None:
            msg = f"Instance '{instance_name}' not found in configuration"
            logger.error("select_instance_not_found", instance_name=instance_name)
            raise ValueError(msg)

        self._active_instance = instance_name
        logger.info("active_instance_selected", instance_name=instance_name)

    def get_active_instance(self) -> str | None:
        """
        Get the name of the currently active instance.

        Returns:
            Name of active instance, or None if no instance is active
        """
        return self._active_instance

    async def add_instance(
        self,
        instance_config: InstanceConfig,
        test_connection: bool = True,
    ) -> dict[str, Any]:
        """
        Add a new NPM instance to the configuration.

        Optionally tests the connection before adding the instance.
        If connection test fails, the instance is not added.

        Args:
            instance_config: Configuration for the new instance
            test_connection: Whether to test connection before adding (default: True)

        Returns:
            Dictionary with operation result:
                - success: bool - Whether operation succeeded
                - instance_name: str - Name of the instance
                - error: str (optional) - Error message if failed

        Raises:
            ValueError: If instance with same name already exists
        """
        # Check for duplicate names
        existing = self.config.get_instance(instance_config.name)
        if existing is not None:
            msg = f"Instance '{instance_config.name}' already exists"
            logger.error("add_instance_duplicate", instance_name=instance_config.name)
            raise ValueError(msg)

        # Test connection if requested
        if test_connection:
            logger.info(
                "testing_new_instance_connection",
                instance_name=instance_config.name,
            )

            # Create temporary client for testing
            temp_client = NPMClient(instance_config, self.auth_manager)
            try:
                # Try to get settings endpoint to verify connection
                await temp_client.get("/api/settings")
                logger.info(
                    "new_instance_connection_successful",
                    instance_name=instance_config.name,
                )
            except Exception as e:
                logger.error(
                    "new_instance_connection_failed",
                    instance_name=instance_config.name,
                    error=str(e),
                )
                # Close the temp client
                await temp_client.close()
                return {
                    "success": False,
                    "instance_name": instance_config.name,
                    "error": f"Connection test failed: {e}",
                }
            finally:
                # Always close temp client (if not already closed)
                try:
                    await temp_client.close()
                except Exception as e:
                    # Client may already be closed, log at debug level
                    logger.debug(
                        "temp_client_close_failed",
                        instance_name=instance_config.name,
                        error=str(e),
                    )

        # Add instance to config
        self.config.instances.append(instance_config)

        logger.info(
            "instance_added",
            instance_name=instance_config.name,
            total_instances=len(self.config.instances),
        )

        return {
            "success": True,
            "instance_name": instance_config.name,
        }

    async def remove_instance(self, instance_name: str) -> dict[str, Any]:
        """
        Remove an NPM instance from the configuration.

        Closes any cached client for the instance and removes it from config.
        If the instance being removed is the active instance, clears active instance.

        Args:
            instance_name: Name of instance to remove

        Returns:
            Dictionary with operation result:
                - success: bool - Whether operation succeeded
                - instance_name: str - Name of the removed instance

        Raises:
            ValueError: If instance not found or trying to remove last instance
        """
        # Validate instance exists
        instance_config = self.config.get_instance(instance_name)
        if instance_config is None:
            msg = f"Instance '{instance_name}' not found in configuration"
            logger.error("remove_instance_not_found", instance_name=instance_name)
            raise ValueError(msg)

        # Prevent removing the last instance
        if len(self.config.instances) == 1:
            msg = "Cannot remove last instance. At least one instance required."
            logger.error("remove_last_instance_attempted", instance_name=instance_name)
            raise ValueError(msg)

        # Close cached client if exists
        if instance_name in self._clients:
            logger.info(
                "closing_client_for_removed_instance",
                instance_name=instance_name,
            )
            try:
                await self._clients[instance_name].close()
            except Exception as e:
                logger.warning(
                    "error_closing_client",
                    instance_name=instance_name,
                    error=str(e),
                )

            # Remove from cache
            del self._clients[instance_name]

        # Clear active instance if removing the active instance
        if self._active_instance == instance_name:
            logger.info(
                "clearing_active_instance",
                instance_name=instance_name,
            )
            self._active_instance = None

        # Remove from config
        self.config.instances.remove(instance_config)

        logger.info(
            "instance_removed",
            instance_name=instance_name,
            remaining_instances=len(self.config.instances),
        )

        return {
            "success": True,
            "instance_name": instance_name,
        }

    async def test_instance(self, instance_name: str) -> dict[str, Any]:
        """
        Test connection to an NPM instance.

        Creates a temporary client, attempts to connect, and measures response time.
        Does not cache the client - this is purely for testing.

        Args:
            instance_name: Name of instance to test

        Returns:
            Dictionary with test results:
                - success: bool - Whether connection succeeded
                - instance_name: str - Name of the tested instance
                - status: str (optional) - Status from NPM API
                - response_time_ms: float (optional) - Response time in milliseconds
                - error: str (optional) - Error message if failed

        Raises:
            ValueError: If instance not found
        """
        # Validate instance exists
        instance_config = self.config.get_instance(instance_name)
        if instance_config is None:
            msg = f"Instance '{instance_name}' not found in configuration"
            logger.error("test_instance_not_found", instance_name=instance_name)
            raise ValueError(msg)

        logger.info("testing_instance_connection", instance_name=instance_name)

        # Create temporary client
        temp_client = NPMClient(instance_config, self.auth_manager)

        try:
            # Measure response time
            start_time = time.perf_counter()

            # Try to get settings endpoint
            response = await temp_client.get("/api/settings")

            end_time = time.perf_counter()
            response_time_ms = (end_time - start_time) * 1000

            # Parse response (validate it's valid JSON)
            _ = response.json()

            logger.info(
                "instance_connection_successful",
                instance_name=instance_name,
                response_time_ms=response_time_ms,
            )

            return {
                "success": True,
                "instance_name": instance_name,
                "status": "online",
                "response_time_ms": response_time_ms,
            }

        except Exception as e:
            logger.error(
                "instance_connection_failed",
                instance_name=instance_name,
                error=str(e),
            )

            return {
                "success": False,
                "instance_name": instance_name,
                "error": str(e),
            }

        finally:
            # Always close the temp client
            try:
                await temp_client.close()
            except Exception as e:
                # Client may already be closed, log at debug level
                logger.debug(
                    "temp_client_close_failed",
                    instance_name=instance_name,
                    error=str(e),
                )

    async def cleanup(self) -> None:
        """
        Cleanup all HTTP connections.

        Closes all cached NPM client connections and clears the cache.
        Called during server shutdown to ensure graceful cleanup.

        This method is safe to call multiple times and handles errors
        during client close gracefully.
        """
        logger.info(
            "cleaning_up_instance_manager",
            cached_clients_count=len(self._clients),
        )

        # Close all cached clients (copy dict to avoid modification during iteration)
        clients_copy = dict(self._clients)
        for instance_name, client in clients_copy.items():
            try:
                logger.debug("closing_client", instance_name=instance_name)
                await client.close()
            except Exception as e:
                logger.warning(
                    "error_closing_client_during_cleanup",
                    instance_name=instance_name,
                    error=str(e),
                )

        # Clear the cache
        self._clients.clear()

        logger.info("instance_manager_cleanup_complete")
