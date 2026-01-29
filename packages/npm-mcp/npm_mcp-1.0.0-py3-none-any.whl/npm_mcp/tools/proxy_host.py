"""
Proxy Host Management MCP Tools for Nginx Proxy Manager.

This module provides 3 MCP tools for managing proxy hosts:
1. npm_list_proxy_hosts - List all proxy hosts with filtering
2. npm_get_proxy_host - Get detailed proxy host information
3. npm_manage_proxy_host - Create, update, delete, enable, disable proxy hosts

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

from typing import Any, Literal, TypeAlias

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.constants import API_PROXY_HOSTS
from npm_mcp.tools.compact import compact_proxy_host
from npm_mcp.types import MCPContext

# Constants
MAX_PORT_NUMBER = 65535

# Type alias for proxy host operation results
ProxyHostResult: TypeAlias = dict[str, Any]


def get_server_context(ctx: MCPContext) -> Any:  # noqa: ANN401
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP Context object

    Returns:
        ServerContext with config, instance_manager, auth_manager, logger
    """
    return ctx.request_context.lifespan_context


# =============================================================================
# Helper Functions for Proxy Host Operations
# =============================================================================


def _validate_create_params(
    domain_names: list[str] | None,
    forward_scheme: str | None,
    forward_host: str | None,
    forward_port: int | None,
) -> ProxyHostResult | None:
    """Validate required parameters for create operation. Returns error dict or None."""
    if not domain_names:
        return {"success": False, "error": "domain_names is required for create operation"}
    if not forward_scheme:
        return {"success": False, "error": "forward_scheme is required for create operation"}
    if not forward_host:
        return {"success": False, "error": "forward_host is required for create operation"}
    if not forward_port:
        return {"success": False, "error": "forward_port is required for create operation"}
    if forward_port < 1 or forward_port > MAX_PORT_NUMBER:
        return {"success": False, "error": "forward_port must be between 1 and 65535"}
    if forward_scheme not in ["http", "https"]:
        return {"success": False, "error": "forward_scheme must be 'http' or 'https'"}
    return None


def _build_create_payload(
    domain_names: list[str],
    forward_scheme: str,
    forward_host: str,
    forward_port: int,
    *,
    certificate_id: int | None = None,
    force_ssl: bool | None = None,
    hsts_enabled: bool | None = None,
    hsts_subdomains: bool | None = None,
    http2_support: bool | None = None,
    websocket_support: bool | None = None,
    block_exploits: bool | None = None,
    caching_enabled: bool | None = None,
    access_list_id: int | None = None,
    advanced_config: str | None = None,
    locations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build request payload for create operation."""
    payload: dict[str, Any] = {
        "domain_names": domain_names,
        "forward_scheme": forward_scheme,
        "forward_host": forward_host,
        "forward_port": forward_port,
    }

    # Map of parameter names to payload keys
    optional_fields = [
        (certificate_id, "certificate_id"),
        (force_ssl, "ssl_forced"),
        (hsts_enabled, "hsts_enabled"),
        (hsts_subdomains, "hsts_subdomains"),
        (http2_support, "http2_support"),
        (websocket_support, "allow_websocket_upgrade"),
        (block_exploits, "block_exploits"),
        (caching_enabled, "caching_enabled"),
        (access_list_id, "access_list_id"),
        (advanced_config, "advanced_config"),
        (locations, "locations"),
    ]

    for value, key in optional_fields:
        if value is not None:
            payload[key] = value

    return payload


def _validate_update_params(
    forward_scheme: str | None,
    forward_port: int | None,
) -> ProxyHostResult | None:
    """Validate optional parameters for update operation. Returns error dict or None."""
    if forward_scheme is not None and forward_scheme not in ["http", "https"]:
        return {"success": False, "error": "forward_scheme must be 'http' or 'https'"}
    if forward_port is not None and (forward_port < 1 or forward_port > MAX_PORT_NUMBER):
        return {"success": False, "error": "forward_port must be between 1 and 65535"}
    return None


def _build_update_payload(
    current_host: dict[str, Any],
    *,
    domain_names: list[str] | None = None,
    forward_scheme: str | None = None,
    forward_host: str | None = None,
    forward_port: int | None = None,
    certificate_id: int | None = None,
    force_ssl: bool | None = None,
    hsts_enabled: bool | None = None,
    hsts_subdomains: bool | None = None,
    http2_support: bool | None = None,
    websocket_support: bool | None = None,
    block_exploits: bool | None = None,
    caching_enabled: bool | None = None,
    access_list_id: int | None = None,
    advanced_config: str | None = None,
    locations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Build request payload for update operation, merging with current host data."""
    # Start with current values (exclude read-only fields)
    payload: dict[str, Any] = {
        "domain_names": current_host.get("domain_names"),
        "forward_scheme": current_host.get("forward_scheme"),
        "forward_host": current_host.get("forward_host"),
        "forward_port": current_host.get("forward_port"),
        "certificate_id": current_host.get("certificate_id"),
        "ssl_forced": current_host.get("ssl_forced"),
        "hsts_enabled": current_host.get("hsts_enabled"),
        "hsts_subdomains": current_host.get("hsts_subdomains"),
        "http2_support": current_host.get("http2_support"),
        "allow_websocket_upgrade": current_host.get("allow_websocket_upgrade"),
        "block_exploits": current_host.get("block_exploits"),
        "caching_enabled": current_host.get("caching_enabled"),
        "access_list_id": current_host.get("access_list_id"),
        "advanced_config": current_host.get("advanced_config"),
        "enabled": current_host.get("enabled"),
    }

    if current_host.get("locations") is not None:
        payload["locations"] = current_host.get("locations")

    # Apply updates - map of (new_value, payload_key) pairs
    updates = [
        (domain_names, "domain_names"),
        (forward_scheme, "forward_scheme"),
        (forward_host, "forward_host"),
        (forward_port, "forward_port"),
        (certificate_id, "certificate_id"),
        (force_ssl, "ssl_forced"),
        (hsts_enabled, "hsts_enabled"),
        (hsts_subdomains, "hsts_subdomains"),
        (http2_support, "http2_support"),
        (websocket_support, "allow_websocket_upgrade"),
        (block_exploits, "block_exploits"),
        (caching_enabled, "caching_enabled"),
        (access_list_id, "access_list_id"),
        (advanced_config, "advanced_config"),
        (locations, "locations"),
    ]

    for value, key in updates:
        if value is not None:
            payload[key] = value

    return payload


async def _handle_create(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    *,
    domain_names: list[str] | None,
    forward_scheme: str | None,
    forward_host: str | None,
    forward_port: int | None,
    certificate_id: int | None,
    force_ssl: bool | None,
    hsts_enabled: bool | None,
    hsts_subdomains: bool | None,
    http2_support: bool | None,
    websocket_support: bool | None,
    block_exploits: bool | None,
    caching_enabled: bool | None,
    access_list_id: int | None,
    advanced_config: str | None,
    locations: list[dict[str, Any]] | None,
) -> ProxyHostResult:
    """Handle create operation for proxy host."""
    # Validate parameters
    validation_error = _validate_create_params(
        domain_names, forward_scheme, forward_host, forward_port
    )
    if validation_error:
        return validation_error

    # Build and send request (params validated, so we can assert non-None)
    payload = _build_create_payload(
        domain_names,  # type: ignore[arg-type]
        forward_scheme,  # type: ignore[arg-type]
        forward_host,  # type: ignore[arg-type]
        forward_port,  # type: ignore[arg-type]
        certificate_id=certificate_id,
        force_ssl=force_ssl,
        hsts_enabled=hsts_enabled,
        hsts_subdomains=hsts_subdomains,
        http2_support=http2_support,
        websocket_support=websocket_support,
        block_exploits=block_exploits,
        caching_enabled=caching_enabled,
        access_list_id=access_list_id,
        advanced_config=advanced_config,
        locations=locations,
    )

    raw_response = await client.post(API_PROXY_HOSTS, json=payload)
    response = raw_response.json()

    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_proxy_host",
        operation="create",
        host_id=response.get("id"),
    )

    return {"success": True, "operation": "create", "proxy_host": response}


async def _handle_update(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    host_id: int,
    *,
    domain_names: list[str] | None,
    forward_scheme: str | None,
    forward_host: str | None,
    forward_port: int | None,
    certificate_id: int | None,
    force_ssl: bool | None,
    hsts_enabled: bool | None,
    hsts_subdomains: bool | None,
    http2_support: bool | None,
    websocket_support: bool | None,
    block_exploits: bool | None,
    caching_enabled: bool | None,
    access_list_id: int | None,
    advanced_config: str | None,
    locations: list[dict[str, Any]] | None,
) -> ProxyHostResult:
    """Handle update operation for proxy host."""
    # Validate optional parameters
    validation_error = _validate_update_params(forward_scheme, forward_port)
    if validation_error:
        return validation_error

    # Fetch current host data
    raw_current = await client.get(f"{API_PROXY_HOSTS}/{host_id}")
    current_host = raw_current.json()

    # Build and send request
    payload = _build_update_payload(
        current_host,
        domain_names=domain_names,
        forward_scheme=forward_scheme,
        forward_host=forward_host,
        forward_port=forward_port,
        certificate_id=certificate_id,
        force_ssl=force_ssl,
        hsts_enabled=hsts_enabled,
        hsts_subdomains=hsts_subdomains,
        http2_support=http2_support,
        websocket_support=websocket_support,
        block_exploits=block_exploits,
        caching_enabled=caching_enabled,
        access_list_id=access_list_id,
        advanced_config=advanced_config,
        locations=locations,
    )

    raw_response = await client.put(f"{API_PROXY_HOSTS}/{host_id}", json=payload)
    response = raw_response.json()

    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_proxy_host",
        operation="update",
        host_id=host_id,
    )

    return {"success": True, "operation": "update", "proxy_host": response}


async def _handle_delete(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    host_id: int,
) -> ProxyHostResult:
    """Handle delete operation for proxy host."""
    await client.delete(f"{API_PROXY_HOSTS}/{host_id}")

    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_proxy_host",
        operation="delete",
        host_id=host_id,
    )

    return {
        "success": True,
        "operation": "delete",
        "message": f"Proxy host {host_id} deleted successfully",
    }


async def _handle_toggle_enabled(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    host_id: int,
    *,
    enable: bool,
) -> ProxyHostResult:
    """Handle enable/disable operation for proxy host."""
    operation = "enable" if enable else "disable"

    raw_current = await client.get(f"{API_PROXY_HOSTS}/{host_id}")
    current_host = raw_current.json()
    current_host["enabled"] = enable
    raw_response = await client.put(f"{API_PROXY_HOSTS}/{host_id}", json=current_host)
    response = raw_response.json()

    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_proxy_host",
        operation=operation,
        host_id=host_id,
    )

    return {"success": True, "operation": operation, "proxy_host": response}


# =============================================================================
# MCP Tools
# =============================================================================


async def npm_list_proxy_hosts(
    ctx: MCPContext,
    instance_name: str | None = None,
    domain_filter: str | None = None,
    enabled_only: bool | None = False,
    page: int | None = 1,
    limit: int | None = 50,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all proxy hosts with optional filtering.

    This tool retrieves all proxy hosts from the NPM instance and supports
    filtering by domain name, enabled status, and pagination.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        domain_filter: Filter by domain name (optional, substring match)
        enabled_only: Show only enabled hosts (optional, default: False)
        page: Page number for pagination (optional, default: 1)
        limit: Results per page (optional, default: 50)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - proxy_hosts: list - Array of proxy host objects
        - total: int - Total number of matching hosts
        - page: int - Current page number
        - limit: int - Results per page
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_proxy_hosts(ctx, enabled_only=True)
        >>> print(f"Found {result['total']} enabled proxy hosts")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_proxy_hosts",
        instance=instance_name or "active",
        filters={
            "domain_filter": domain_filter,
            "enabled_only": enabled_only,
            "page": page,
            "limit": limit,
        },
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all proxy hosts from NPM API
        raw_response = await client.get(API_PROXY_HOSTS)
        response = raw_response.json()

        # Apply filters
        proxy_hosts = response if isinstance(response, list) else []

        # Filter by domain name if specified
        if domain_filter:
            proxy_hosts = [
                host
                for host in proxy_hosts
                if any(
                    domain_filter.lower() in domain.lower()
                    for domain in host.get("domain_names", [])
                )
            ]

        # Filter by enabled status if specified
        if enabled_only:
            proxy_hosts = [host for host in proxy_hosts if host.get("enabled", False)]

        # Calculate pagination (simplified - would use API pagination in production)
        total = len(proxy_hosts)
        page_num = page if page is not None else 1
        limit_num = limit if limit is not None else 50
        start_idx = (page_num - 1) * limit_num
        end_idx = start_idx + limit_num
        paginated_hosts = proxy_hosts[start_idx:end_idx]

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_proxy_hosts",
            total=total,
            returned=len(paginated_hosts),
        )

        # Apply compaction if requested (default: True)
        result_hosts = (
            [compact_proxy_host(h) for h in paginated_hosts] if compact else paginated_hosts
        )

        return {
            "success": True,
            "proxy_hosts": result_hosts,
            "total": total,
            "page": page_num,
            "limit": limit_num,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_proxy_hosts", error=str(e))
        return {"success": False, "error": str(e)}


async def npm_get_proxy_host(
    ctx: MCPContext,
    host_id: int | None = None,
    domain_name: str | None = None,
    instance_name: str | None = None,
) -> dict[str, Any]:
    """
    Get detailed information about a specific proxy host.

    This tool retrieves complete details for a proxy host, including SSL configuration,
    access lists, location-based routing, and advanced settings. You can specify
    either host_id or domain_name (at least one is required).

    Args:
        ctx: MCP context (auto-injected)
        host_id: Proxy host ID (optional, required if domain_name not provided)
        domain_name: Domain name to search for (optional, required if host_id not provided)
        instance_name: Target instance name (optional, uses active instance if not specified)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - proxy_host: dict - Complete proxy host details
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_get_proxy_host(ctx, host_id=42)
        >>> print(f"Host: {result['proxy_host']['domain_names']}")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_get_proxy_host",
        instance=instance_name or "active",
        host_id=host_id,
        domain_name=domain_name,
    )

    try:
        # Validate parameters
        if not host_id and not domain_name:
            return {
                "success": False,
                "error": "Either host_id or domain_name must be provided",
            }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch proxy host details
        if host_id:
            # Get by ID
            raw_response = await client.get(f"{API_PROXY_HOSTS}/{host_id}")
            proxy_host = raw_response.json()
        else:
            # Get by domain name - fetch all hosts and filter
            raw_all_hosts = await client.get(API_PROXY_HOSTS)
            all_hosts = raw_all_hosts.json()
            domain_lower = domain_name.lower() if domain_name else ""
            matching_hosts = [
                host
                for host in all_hosts
                if domain_lower in [d.lower() for d in host.get("domain_names", [])]
            ]

            if not matching_hosts:
                return {
                    "success": False,
                    "error": f"Proxy host not found with domain name '{domain_name}'",
                }

            proxy_host = matching_hosts[0]

        server_ctx.logger.info(
            "tool_success",
            tool="npm_get_proxy_host",
            host_id=proxy_host.get("id"),
            domains=proxy_host.get("domain_names"),
        )

        return {"success": True, "proxy_host": proxy_host}

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_get_proxy_host", error=str(e))
        return {"success": False, "error": str(e)}


async def npm_manage_proxy_host(
    operation: Literal["create", "update", "delete", "enable", "disable"],
    ctx: MCPContext,
    host_id: int | None = None,
    instance_name: str | None = None,
    # Domain and forwarding configuration
    domain_names: list[str] | None = None,
    forward_scheme: str | None = None,
    forward_host: str | None = None,
    forward_port: int | None = None,
    # SSL/TLS configuration
    certificate_id: int | None = None,
    force_ssl: bool | None = None,
    hsts_enabled: bool | None = None,
    hsts_subdomains: bool | None = None,
    # Feature flags
    http2_support: bool | None = None,
    websocket_support: bool | None = None,
    block_exploits: bool | None = None,
    caching_enabled: bool | None = None,
    # Access control
    access_list_id: int | None = None,
    # Advanced configuration
    advanced_config: str | None = None,
    # Location-based routing
    locations: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """
    Create, update, delete, enable, or disable proxy hosts.

    This is a multi-operation tool that handles all CRUD operations for proxy hosts.
    Different operations require different parameters:

    - create: requires domain_names, forward_scheme, forward_host, forward_port
    - update: requires host_id, optional fields to update
    - delete: requires host_id
    - enable: requires host_id
    - disable: requires host_id

    Args:
        operation: Operation type (create, update, delete, enable, disable)
        ctx: MCP context (auto-injected)
        host_id: Proxy host ID (required for update/delete/enable/disable)
        instance_name: Target instance name (optional)
        domain_names: List of domain names (required for create, optional for update)
        forward_scheme: Forwarding protocol - http or https (required for create)
        forward_host: Target host IP or hostname (required for create)
        forward_port: Target port 1-65535 (required for create)
        certificate_id: SSL certificate ID (optional)
        force_ssl: Force HTTPS redirect (optional)
        hsts_enabled: Enable HSTS header (optional)
        hsts_subdomains: Include subdomains in HSTS (optional)
        http2_support: Enable HTTP/2 (optional)
        websocket_support: Allow WebSocket upgrades (optional)
        block_exploits: Block common exploits (optional)
        caching_enabled: Enable caching (optional)
        access_list_id: Apply access list (optional)
        advanced_config: Custom Nginx config (optional)
        locations: Location-based routing rules (optional)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - proxy_host: dict - Proxy host details (for create/update/enable/disable)
        - message: str - Success message (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create a proxy host
        >>> result = await npm_manage_proxy_host(
        ...     operation="create",
        ...     ctx=ctx,
        ...     domain_names=["api.example.com"],
        ...     forward_scheme="http",
        ...     forward_host="192.168.1.100",
        ...     forward_port=3000,
        ... )

        >>> # Update SSL settings
        >>> result = await npm_manage_proxy_host(
        ...     operation="update",
        ...     ctx=ctx,
        ...     host_id=42,
        ...     certificate_id=5,
        ...     force_ssl=True,
        ... )

        >>> # Disable a proxy host
        >>> result = await npm_manage_proxy_host(
        ...     operation="disable",
        ...     ctx=ctx,
        ...     host_id=42,
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_proxy_host",
        operation=operation,
        instance=instance_name or "active",
        host_id=host_id,
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Route to appropriate handler based on operation
        if operation == "create":
            return await _handle_create(
                client,
                server_ctx,
                domain_names=domain_names,
                forward_scheme=forward_scheme,
                forward_host=forward_host,
                forward_port=forward_port,
                certificate_id=certificate_id,
                force_ssl=force_ssl,
                hsts_enabled=hsts_enabled,
                hsts_subdomains=hsts_subdomains,
                http2_support=http2_support,
                websocket_support=websocket_support,
                block_exploits=block_exploits,
                caching_enabled=caching_enabled,
                access_list_id=access_list_id,
                advanced_config=advanced_config,
                locations=locations,
            )

        # Operations requiring host_id
        if not host_id:
            return {
                "success": False,
                "error": f"host_id is required for {operation} operation",
            }

        if operation == "update":
            return await _handle_update(
                client,
                server_ctx,
                host_id,
                domain_names=domain_names,
                forward_scheme=forward_scheme,
                forward_host=forward_host,
                forward_port=forward_port,
                certificate_id=certificate_id,
                force_ssl=force_ssl,
                hsts_enabled=hsts_enabled,
                hsts_subdomains=hsts_subdomains,
                http2_support=http2_support,
                websocket_support=websocket_support,
                block_exploits=block_exploits,
                caching_enabled=caching_enabled,
                access_list_id=access_list_id,
                advanced_config=advanced_config,
                locations=locations,
            )

        if operation == "delete":
            return await _handle_delete(client, server_ctx, host_id)

        if operation == "enable":
            return await _handle_toggle_enabled(client, server_ctx, host_id, enable=True)

        # operation == "disable"
        return await _handle_toggle_enabled(client, server_ctx, host_id, enable=False)

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="npm_manage_proxy_host",
            operation=operation,
            error=str(e),
        )
        return {"success": False, "error": str(e)}


def register_proxy_host_tools(mcp: FastMCP) -> None:
    """
    Register all 3 proxy host management tools with FastMCP server.

    Args:
        mcp: FastMCP server instance

    Tools registered:
        1. npm_list_proxy_hosts - List all proxy hosts with filtering
        2. npm_get_proxy_host - Get detailed proxy host information
        3. npm_manage_proxy_host - Create, update, delete, enable, disable proxy hosts
    """
    # npm_list_proxy_hosts (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_proxy_hosts
    )

    # npm_get_proxy_host (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_get_proxy_host
    )

    # npm_manage_proxy_host (destructive - creates, updates, deletes)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_proxy_host)
