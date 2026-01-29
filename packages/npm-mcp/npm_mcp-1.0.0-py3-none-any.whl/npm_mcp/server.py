"""
MCP Server Core.

This module implements the FastMCP server with lifespan management for integrating
Phase 1 components (config, auth, HTTP client, models) with the MCP protocol.

Key components:
- ServerContext: Dataclass holding Phase 1 components shared across tools
- create_server_lifespan: Factory function for async lifespan context manager
- create_mcp_server: Factory function for FastMCP server instance
- CategoryManager integration for lazy tool loading

Usage:
    from npm_mcp.server import create_mcp_server

    server = create_mcp_server()
    # Run with MCP transport (stdio, SSE, etc.)
"""

from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any

from mcp.server.fastmcp import FastMCP

from npm_mcp.auth.manager import AuthManager
from npm_mcp.config.loader import load_config
from npm_mcp.config.models import Config
from npm_mcp.instance_manager import InstanceManager
from npm_mcp.utils.logging import setup_logging

# Global flag to track if all tools should be loaded at startup
_load_all_tools: bool = False


def set_load_all_tools(value: bool) -> None:
    """Set the flag to load all tools at startup.

    When True, all tool categories are enabled at startup (backward compatible).
    When False, only category meta-tools are loaded (lazy loading).

    Args:
        value: Whether to load all tools at startup.
    """
    global _load_all_tools  # noqa: PLW0603
    _load_all_tools = value


def get_load_all_tools() -> bool:
    """Get the current value of the load all tools flag."""
    return _load_all_tools


@dataclass
class ServerContext:
    """
    Application context with Phase 1 components.

    This context is created during server lifespan startup and made available
    to all MCP tools via Context injection.

    Attributes:
        config: Loaded configuration with instance details
        auth_manager: JWT token manager for NPM authentication
        instance_manager: Multi-instance connection manager
        logger: Structured logger instance
        active_instance: Name of currently selected instance (optional)
    """

    config: Config
    auth_manager: AuthManager
    instance_manager: InstanceManager
    logger: Any
    active_instance: str | None = None


def create_server_lifespan() -> Callable[[FastMCP], AsyncIterator[ServerContext]]:
    """
    Create async lifespan function for FastMCP server.

    The lifespan function manages initialization and cleanup of Phase 1 components:

    Startup:
        1. Set up structured logging
        2. Load configuration (YAML/env)
        3. Initialize AuthManager
        4. Initialize InstanceManager
        5. Pre-authenticate default instance

    Shutdown:
        1. Cleanup InstanceManager (close HTTP connections)
        2. Cleanup AuthManager (flush token cache)

    Returns:
        Async context manager function that yields ServerContext

    Example:
        @asynccontextmanager
        async def lifespan(server: FastMCP) -> AsyncIterator[ServerContext]:
            # Startup
            logger = setup_logging()
            logger.info("MCP server starting up")
            config = await load_config()
            auth_manager = AuthManager(config)
            instance_manager = InstanceManager(config, auth_manager)

            # Pre-authenticate default instance
            default = config.get_default_instance()
            if default:
                await auth_manager.get_valid_token(default.name)

            context = ServerContext(
                config=config,
                auth_manager=auth_manager,
                instance_manager=instance_manager,
                logger=logger
            )

            try:
                yield context
            finally:
                # Shutdown
                logger.info("MCP server shutting down")
                await instance_manager.cleanup()
                auth_manager.cleanup()
    """

    @asynccontextmanager
    async def server_lifespan(_server: FastMCP) -> AsyncIterator[ServerContext]:
        """
        Initialize Phase 1 components on startup, cleanup on shutdown.

        Args:
            _server: FastMCP server instance (unused, required by protocol)

        Yields:
            ServerContext with initialized Phase 1 components
        """
        # Startup
        logger = setup_logging()
        logger.info("MCP server starting up")

        # Load configuration
        config = load_config()

        # Initialize Phase 1 components
        auth_manager = AuthManager(config)
        instance_manager = InstanceManager(config, auth_manager)

        # Pre-authenticate default instance if configured (non-blocking)
        default_instance = config.get_default_instance()
        if default_instance:
            try:
                await auth_manager.get_valid_token(default_instance.name)
            except Exception as e:
                # Log warning but don't crash - authentication will be retried when tools are called
                logger.warning(
                    "failed_to_authenticate_default_instance_during_startup",
                    instance_name=default_instance.name,
                    error=str(e),
                    message="Authentication will be retried when tools are invoked",
                )

        # Create server context
        context = ServerContext(
            config=config,
            auth_manager=auth_manager,
            instance_manager=instance_manager,
            logger=logger,
        )

        try:
            yield context
        finally:
            # Shutdown
            logger.info("MCP server shutting down")
            await instance_manager.cleanup()
            auth_manager.cleanup()

    return server_lifespan  # type: ignore[return-value]


def create_mcp_server(
    host: str = "127.0.0.1",
    port: int = 8000,
) -> FastMCP:
    """
    Create and configure FastMCP server instance.

    Creates a FastMCP server with:
    - Name: "npm-mcp"
    - Version: Imported from package
    - Lifespan: Phase 1 component initialization/cleanup
    - CategoryManager for lazy tool loading
    - Configurable host/port for HTTP transports

    Args:
        host: Bind address for HTTP transports (ignored for stdio). Default: 127.0.0.1
        port: Port for HTTP transports (ignored for stdio). Default: 8000

    Returns:
        Configured FastMCP server instance ready for tool registration

    Example:
        # Default (stdio transport)
        server = create_mcp_server()

        # HTTP transport on custom port
        server = create_mcp_server(host="0.0.0.0", port=9000)

        @server.tool()
        async def npm_list_instances(
            ctx: Context[ServerSession, ServerContext]
        ) -> dict:
            # Access Phase 1 components via context
            server_ctx = ctx.request_context.lifespan_context
            instances = server_ctx.config.instances
            return {"instances": [i.name for i in instances]}
    """
    # Import here to avoid circular imports
    from npm_mcp.prompts import register_all_prompts
    from npm_mcp.tools.categories import (
        CategoryManager,
        register_category_tools,
        set_category_manager,
    )

    # Create lifespan function
    lifespan_fn = create_server_lifespan()

    # Create FastMCP server with lifespan
    # host/port are only used when running with HTTP transports (sse, streamable-http)
    server = FastMCP(
        name="npm-mcp",
        instructions=(
            "NPM MCP Server - Manage Nginx Proxy Manager instances through "
            "natural language. Supports multi-instance management, proxy hosts, "
            "SSL certificates, access lists, and more."
        ),
        lifespan=lifespan_fn,  # type: ignore[arg-type]
        host=host,
        port=port,
    )

    # Initialize category manager for lazy tool loading
    category_manager = CategoryManager(server)
    set_category_manager(category_manager)

    # Register category meta-tools (always available)
    register_category_tools(server)

    # Register MCP prompts
    register_all_prompts(server)

    # If --all-tools flag was set, enable all categories at startup
    if _load_all_tools:
        category_manager.enable_all()

    return server
