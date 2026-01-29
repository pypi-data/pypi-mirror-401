"""
Redirection and Dead Host Management MCP Tools for Nginx Proxy Manager.

This module provides 4 MCP tools for managing URL redirections and dead hosts:
1. npm_list_redirections - List all redirections with filtering
2. npm_manage_redirection - Create, update, or delete redirections
3. npm_list_dead_hosts - List all dead hosts with filtering
4. npm_manage_dead_host - Create, update, or delete dead hosts

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

from typing import Any, Literal, TypeAlias

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.tools.compact import compact_dead_host, compact_redirection
from npm_mcp.types import MCPContext

# Type aliases
RedirectionResult: TypeAlias = dict[str, Any]
DeadHostResult: TypeAlias = dict[str, Any]

# Valid HTTP redirect codes
VALID_HTTP_CODES = {301, 302, 307, 308}


def get_server_context(ctx: MCPContext) -> Any:  # noqa: ANN401  # noqa: ANN401
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP Context object

    Returns:
        ServerContext with config, instance_manager, auth_manager, logger
    """
    return ctx.request_context.lifespan_context


# =============================================================================
# Redirection Helper Functions
# =============================================================================


def _validate_redir_create_params(
    domain_names: list[str] | None,
    forward_scheme: str | None,
    forward_domain_name: str | None,
    forward_http_code: int | None,
) -> RedirectionResult | None:
    """Validate create parameters. Returns error dict or None if valid."""
    missing_params = []
    if domain_names is None or len(domain_names) == 0:
        missing_params.append("domain_names")
    if forward_scheme is None:
        missing_params.append("forward_scheme")
    if forward_domain_name is None:
        missing_params.append("forward_domain_name")

    if missing_params:
        return {
            "success": False,
            "error": f"Missing required params for create: {', '.join(missing_params)}",
        }

    if forward_http_code is not None and forward_http_code not in VALID_HTTP_CODES:
        return {
            "success": False,
            "error": f"forward_http_code must be one of {VALID_HTTP_CODES}",
        }

    return None


def _build_redir_create_body(
    domain_names: list[str],
    forward_scheme: str,
    forward_domain_name: str,
    forward_http_code: int | None,
    preserve_path: bool,
    ssl_forced: bool,
    hsts_enabled: bool,
    hsts_subdomains: bool,
    http2_support: bool,
    block_exploits: bool,
    certificate_id: int | None,
    advanced_config: str | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for create operation."""
    body: dict[str, Any] = {
        "domain_names": domain_names,
        "forward_scheme": forward_scheme,
        "forward_domain_name": forward_domain_name,
        "forward_http_code": forward_http_code if forward_http_code is not None else 301,
        "preserve_path": preserve_path,
        "ssl_forced": ssl_forced,
        "hsts_enabled": hsts_enabled,
        "hsts_subdomains": hsts_subdomains,
        "http2_support": http2_support,
        "block_exploits": block_exploits,
    }

    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if advanced_config is not None:
        body["advanced_config"] = advanced_config
    if meta is not None:
        body["meta"] = meta

    return body


def _build_redir_update_body(
    domain_names: list[str] | None,
    forward_scheme: str | None,
    forward_domain_name: str | None,
    forward_http_code: int | None,
    preserve_path: bool | None,
    certificate_id: int | None,
    ssl_forced: bool | None,
    hsts_enabled: bool | None,
    hsts_subdomains: bool | None,
    http2_support: bool | None,
    block_exploits: bool | None,
    advanced_config: str | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for update operation with only provided fields."""
    body: dict[str, Any] = {}

    if domain_names is not None:
        body["domain_names"] = domain_names
    if forward_scheme is not None:
        body["forward_scheme"] = forward_scheme
    if forward_domain_name is not None:
        body["forward_domain_name"] = forward_domain_name
    if forward_http_code is not None:
        body["forward_http_code"] = forward_http_code
    if preserve_path is not None:
        body["preserve_path"] = preserve_path
    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if ssl_forced is not None:
        body["ssl_forced"] = ssl_forced
    if hsts_enabled is not None:
        body["hsts_enabled"] = hsts_enabled
    if hsts_subdomains is not None:
        body["hsts_subdomains"] = hsts_subdomains
    if http2_support is not None:
        body["http2_support"] = http2_support
    if block_exploits is not None:
        body["block_exploits"] = block_exploits
    if advanced_config is not None:
        body["advanced_config"] = advanced_config
    if meta is not None:
        body["meta"] = meta

    return body


async def _handle_redir_create(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    body: dict[str, Any],
) -> RedirectionResult:
    """Handle redirection create operation."""
    redirection = await client.post("/api/nginx/redirection-hosts", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_redirection",
        operation="create",
        redirect_id=redirection.get("id"),
    )
    return {"success": True, "operation": "create", "redirection": redirection}


async def _handle_redir_update(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    redirect_id: int,
    body: dict[str, Any],
) -> RedirectionResult:
    """Handle redirection update operation."""
    redirection = await client.put(f"/api/nginx/redirection-hosts/{redirect_id}", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_redirection",
        operation="update",
        redirect_id=redirect_id,
    )
    return {"success": True, "operation": "update", "redirection": redirection}


async def _handle_redir_delete(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    redirect_id: int,
) -> RedirectionResult:
    """Handle redirection delete operation."""
    await client.delete(f"/api/nginx/redirection-hosts/{redirect_id}")
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_redirection",
        operation="delete",
        redirect_id=redirect_id,
    )
    return {"success": True, "operation": "delete", "redirect_id": redirect_id}


# =============================================================================
# Dead Host Helper Functions
# =============================================================================


def _build_dead_host_create_body(
    domain_names: list[str],
    ssl_forced: bool,
    hsts_enabled: bool,
    hsts_subdomains: bool,
    http2_support: bool,
    certificate_id: int | None,
    advanced_config: str | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for dead host create operation."""
    body: dict[str, Any] = {
        "domain_names": domain_names,
        "ssl_forced": ssl_forced,
        "hsts_enabled": hsts_enabled,
        "hsts_subdomains": hsts_subdomains,
        "http2_support": http2_support,
    }

    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if advanced_config is not None:
        body["advanced_config"] = advanced_config
    if meta is not None:
        body["meta"] = meta

    return body


def _build_dead_host_update_body(
    domain_names: list[str] | None,
    certificate_id: int | None,
    ssl_forced: bool | None,
    hsts_enabled: bool | None,
    hsts_subdomains: bool | None,
    http2_support: bool | None,
    advanced_config: str | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for dead host update operation."""
    body: dict[str, Any] = {}

    if domain_names is not None:
        body["domain_names"] = domain_names
    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if ssl_forced is not None:
        body["ssl_forced"] = ssl_forced
    if hsts_enabled is not None:
        body["hsts_enabled"] = hsts_enabled
    if hsts_subdomains is not None:
        body["hsts_subdomains"] = hsts_subdomains
    if http2_support is not None:
        body["http2_support"] = http2_support
    if advanced_config is not None:
        body["advanced_config"] = advanced_config
    if meta is not None:
        body["meta"] = meta

    return body


async def _handle_dead_host_create(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    body: dict[str, Any],
) -> DeadHostResult:
    """Handle dead host create operation."""
    dead_host = await client.post("/api/nginx/dead-hosts", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_dead_host",
        operation="create",
        host_id=dead_host.get("id"),
    )
    return {"success": True, "operation": "create", "dead_host": dead_host}


async def _handle_dead_host_update(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    host_id: int,
    body: dict[str, Any],
) -> DeadHostResult:
    """Handle dead host update operation."""
    dead_host = await client.put(f"/api/nginx/dead-hosts/{host_id}", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_dead_host",
        operation="update",
        host_id=host_id,
    )
    return {"success": True, "operation": "update", "dead_host": dead_host}


async def _handle_dead_host_delete(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    host_id: int,
) -> DeadHostResult:
    """Handle dead host delete operation."""
    await client.delete(f"/api/nginx/dead-hosts/{host_id}")
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_dead_host",
        operation="delete",
        host_id=host_id,
    )
    return {"success": True, "operation": "delete", "host_id": host_id}


# =============================================================================
# Redirection Tools
# =============================================================================


async def npm_list_redirections(
    ctx: MCPContext,
    instance_name: str | None = None,
    enabled_only: bool = False,
    http_code: int | None = None,
    with_certificate: bool = False,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all URL redirections with optional filtering.

    This tool retrieves all configured redirections from the NPM instance,
    with options to filter by enabled status, HTTP status code, and SSL certificate.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        enabled_only: Only show enabled redirections (default: False)
        http_code: Filter by HTTP status code - 301, 302, 307, or 308 (optional)
        with_certificate: Only show redirections with SSL certificates (default: False)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - redirections: list - Array of redirection objects (filtered if requested)
        - total: int - Total number of redirections before filtering
        - enabled_count: int - Number of enabled redirections in result
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_redirections(ctx)
        >>> print(f"Found {result['total']} redirections")
        >>> for redir in result['redirections']:
        ...     print(f"  {redir['domain_names']} -> {redir['forward_domain_name']} "
        ...           f"({redir['forward_http_code']})")

        >>> # Filter by HTTP 301 only
        >>> result = await npm_list_redirections(ctx, http_code=301)

        >>> # Filter by enabled redirections with SSL
        >>> result = await npm_list_redirections(ctx, enabled_only=True, with_certificate=True)
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_redirections",
        instance=instance_name or "active",
        enabled_only=enabled_only,
        http_code=http_code,
        with_certificate=with_certificate,
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all redirections from NPM API
        response = await client.get("/api/nginx/redirection-hosts")

        # Ensure response is a list
        redirections = response if isinstance(response, list) else []

        # Store total before filtering
        total = len(redirections)

        # Apply http_code filter if specified
        if http_code is not None:
            redirections = [r for r in redirections if r.get("forward_http_code") == http_code]

        # Apply with_certificate filter if specified
        if with_certificate:
            redirections = [r for r in redirections if r.get("certificate_id") is not None]

        # Apply enabled_only filter if specified
        if enabled_only:
            redirections = [r for r in redirections if r.get("enabled", False)]

        # Count enabled redirections in filtered result
        enabled_count = sum(1 for r in redirections if r.get("enabled", False))

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_redirections",
            total=total,
            filtered=len(redirections),
            enabled_count=enabled_count,
        )

        # Apply compaction if requested (default: True)
        result_redirections = (
            [compact_redirection(r) for r in redirections] if compact else redirections
        )

        return {
            "success": True,
            "redirections": result_redirections,
            "total": total,
            "enabled_count": enabled_count,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_redirections", error=str(e))
        raise


async def npm_manage_redirection(
    ctx: MCPContext,
    operation: Literal["create", "update", "delete"],
    instance_name: str | None = None,
    redirect_id: int | None = None,
    domain_names: list[str] | None = None,
    forward_scheme: Literal["http", "https", "$scheme"] | None = None,
    forward_domain_name: str | None = None,
    forward_http_code: int | None = None,
    preserve_path: bool = True,
    certificate_id: int | None = None,
    ssl_forced: bool = False,
    hsts_enabled: bool = False,
    hsts_subdomains: bool = False,
    http2_support: bool = False,
    block_exploits: bool = True,
    advanced_config: str | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create, update, or delete URL redirections.

    This tool provides full CRUD operations for redirection management, including
    HTTP status code configuration and optional SSL termination.

    Args:
        ctx: MCP context (auto-injected)
        operation: Operation to perform (create, update, delete)
        instance_name: Target instance name (optional, uses active instance)
        redirect_id: Redirection ID (required for update/delete)
        domain_names: Source domain names (required for create)
        forward_scheme: Target scheme - 'http', 'https', or '$scheme' (required for create)
        forward_domain_name: Target domain name (required for create)
        forward_http_code: HTTP redirect code - 301, 302, 307, or 308 (default: 301)
        preserve_path: Whether to preserve URL path in redirect (default: True)
        certificate_id: SSL certificate ID (optional)
        ssl_forced: Force SSL redirect HTTP to HTTPS (default: False)
        hsts_enabled: Enable HTTP Strict Transport Security (default: False)
        hsts_subdomains: Include subdomains in HSTS (default: False)
        http2_support: Enable HTTP/2 support (default: False)
        block_exploits: Block common exploits (default: True)
        advanced_config: Custom Nginx configuration (optional)
        meta: Additional metadata (optional)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - redirection: dict - Redirection object (for create/update)
        - redirect_id: int - Redirection ID (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create a 301 redirect from old to new domain
        >>> result = await npm_manage_redirection(
        ...     ctx,
        ...     operation="create",
        ...     domain_names=["old.example.com"],
        ...     forward_scheme="https",
        ...     forward_domain_name="new.example.com",
        ...     forward_http_code=301,
        ...     preserve_path=True,
        ... )

        >>> # Update to 302 temporary redirect
        >>> result = await npm_manage_redirection(
        ...     ctx,
        ...     operation="update",
        ...     redirect_id=10,
        ...     forward_http_code=302,
        ... )

        >>> # Delete redirection
        >>> result = await npm_manage_redirection(
        ...     ctx,
        ...     operation="delete",
        ...     redirect_id=10,
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_redirection",
        operation=operation,
        instance=instance_name or "active",
        redirect_id=redirect_id,
    )

    # Validate operation
    valid_operations = {"create", "update", "delete"}
    if operation not in valid_operations:
        error_msg = f"Invalid operation: {operation}. Must be: {', '.join(valid_operations)}"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    # Validate parameters based on operation
    if operation in {"update", "delete"} and redirect_id is None:
        error_msg = f"redirect_id is required for {operation} operation"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    if operation == "create":
        validation_error = _validate_redir_create_params(
            domain_names, forward_scheme, forward_domain_name, forward_http_code
        )
        if validation_error:
            server_ctx.logger.error("tool_validation_error", error=validation_error["error"])
            return validation_error

    # Validate HTTP code for update operation
    if operation == "update" and forward_http_code is not None:
        if forward_http_code not in VALID_HTTP_CODES:
            error_msg = f"forward_http_code must be one of {VALID_HTTP_CODES}"
            server_ctx.logger.error("tool_validation_error", error=error_msg)
            return {"success": False, "error": error_msg}

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        if operation == "create":
            body = _build_redir_create_body(
                domain_names,  # type: ignore[arg-type]
                forward_scheme,  # type: ignore[arg-type]
                forward_domain_name,  # type: ignore[arg-type]
                forward_http_code,
                preserve_path,
                ssl_forced,
                hsts_enabled,
                hsts_subdomains,
                http2_support,
                block_exploits,
                certificate_id,
                advanced_config,
                meta,
            )
            return await _handle_redir_create(client, server_ctx, body)

        # redirect_id validated above for update/delete
        assert redirect_id is not None  # nosec B101 - type narrowing after validation

        if operation == "update":
            body = _build_redir_update_body(
                domain_names,
                forward_scheme,
                forward_domain_name,
                forward_http_code,
                preserve_path,
                certificate_id,
                ssl_forced,
                hsts_enabled,
                hsts_subdomains,
                http2_support,
                block_exploits,
                advanced_config,
                meta,
            )
            return await _handle_redir_update(client, server_ctx, redirect_id, body)

        # operation == "delete"
        return await _handle_redir_delete(client, server_ctx, redirect_id)

    except Exception as e:
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_redirection", operation=operation, error=str(e)
        )
        raise


# =============================================================================
# Dead Host Tools
# =============================================================================


async def npm_list_dead_hosts(
    ctx: MCPContext,
    instance_name: str | None = None,
    enabled_only: bool = False,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all dead hosts (404 handlers) with optional filtering.

    This tool retrieves all configured dead hosts from the NPM instance,
    with options to filter by enabled status.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        enabled_only: Only show enabled dead hosts (default: False)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - dead_hosts: list - Array of dead host objects (filtered if requested)
        - total: int - Total number of dead hosts before filtering
        - enabled_count: int - Number of enabled dead hosts in result
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_dead_hosts(ctx)
        >>> print(f"Found {result['total']} dead hosts")
        >>> for host in result['dead_hosts']:
        ...     print(f"  {host['domain_names']} - 404 handler")

        >>> # Filter by enabled only
        >>> result = await npm_list_dead_hosts(ctx, enabled_only=True)
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_dead_hosts",
        instance=instance_name or "active",
        enabled_only=enabled_only,
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all dead hosts from NPM API
        response = await client.get("/api/nginx/dead-hosts")

        # Ensure response is a list
        dead_hosts = response if isinstance(response, list) else []

        # Store total before filtering
        total = len(dead_hosts)

        # Apply enabled_only filter if specified
        if enabled_only:
            dead_hosts = [h for h in dead_hosts if h.get("enabled", False)]

        # Count enabled dead hosts in filtered result
        enabled_count = sum(1 for h in dead_hosts if h.get("enabled", False))

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_dead_hosts",
            total=total,
            filtered=len(dead_hosts),
            enabled_count=enabled_count,
        )

        # Apply compaction if requested (default: True)
        result_dead_hosts = [compact_dead_host(h) for h in dead_hosts] if compact else dead_hosts

        return {
            "success": True,
            "dead_hosts": result_dead_hosts,
            "total": total,
            "enabled_count": enabled_count,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_dead_hosts", error=str(e))
        raise


async def npm_manage_dead_host(
    ctx: MCPContext,
    operation: Literal["create", "update", "delete"],
    instance_name: str | None = None,
    host_id: int | None = None,
    domain_names: list[str] | None = None,
    certificate_id: int | None = None,
    ssl_forced: bool = False,
    hsts_enabled: bool = False,
    hsts_subdomains: bool = False,
    http2_support: bool = False,
    advanced_config: str | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create, update, or delete dead hosts (404 handlers).

    This tool provides full CRUD operations for dead host management, including
    optional SSL termination for catch-all domains.

    Args:
        ctx: MCP context (auto-injected)
        operation: Operation to perform (create, update, delete)
        instance_name: Target instance name (optional, uses active instance)
        host_id: Dead host ID (required for update/delete)
        domain_names: Domain names for 404 handler (required for create)
        certificate_id: SSL certificate ID (optional)
        ssl_forced: Force SSL redirect HTTP to HTTPS (default: False)
        hsts_enabled: Enable HTTP Strict Transport Security (default: False)
        hsts_subdomains: Include subdomains in HSTS (default: False)
        http2_support: Enable HTTP/2 support (default: False)
        advanced_config: Custom Nginx configuration (optional)
        meta: Additional metadata (optional)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - dead_host: dict - Dead host object (for create/update)
        - host_id: int - Dead host ID (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create a 404 handler for unused subdomains
        >>> result = await npm_manage_dead_host(
        ...     ctx,
        ...     operation="create",
        ...     domain_names=["*.unused.example.com"],
        ... )

        >>> # Update to add SSL certificate
        >>> result = await npm_manage_dead_host(
        ...     ctx,
        ...     operation="update",
        ...     host_id=15,
        ...     certificate_id=5,
        ...     ssl_forced=True,
        ... )

        >>> # Delete dead host
        >>> result = await npm_manage_dead_host(
        ...     ctx,
        ...     operation="delete",
        ...     host_id=15,
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_dead_host",
        operation=operation,
        instance=instance_name or "active",
        host_id=host_id,
    )

    # Validate operation
    valid_operations = {"create", "update", "delete"}
    if operation not in valid_operations:
        error_msg = f"Invalid operation: {operation}. Must be: {', '.join(valid_operations)}"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    # Validate parameters based on operation
    if operation in {"update", "delete"} and host_id is None:
        error_msg = f"host_id is required for {operation} operation"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    if operation == "create":
        if domain_names is None or len(domain_names) == 0:
            error_msg = "domain_names is required for create operation"
            server_ctx.logger.error("tool_validation_error", error=error_msg)
            return {"success": False, "error": error_msg}

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        if operation == "create":
            body = _build_dead_host_create_body(
                domain_names,  # type: ignore[arg-type]
                ssl_forced,
                hsts_enabled,
                hsts_subdomains,
                http2_support,
                certificate_id,
                advanced_config,
                meta,
            )
            return await _handle_dead_host_create(client, server_ctx, body)

        # host_id validated above for update/delete
        assert host_id is not None  # nosec B101 - type narrowing after validation

        if operation == "update":
            body = _build_dead_host_update_body(
                domain_names,
                certificate_id,
                ssl_forced,
                hsts_enabled,
                hsts_subdomains,
                http2_support,
                advanced_config,
                meta,
            )
            return await _handle_dead_host_update(client, server_ctx, host_id, body)

        # operation == "delete"
        return await _handle_dead_host_delete(client, server_ctx, host_id)

    except Exception as e:
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_dead_host", operation=operation, error=str(e)
        )
        raise


def register_redirection_tools(mcp: FastMCP) -> None:
    """
    Register all redirection and dead host tools with FastMCP server.

    Args:
        mcp: FastMCP server instance
    """
    # npm_list_redirections (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_redirections
    )

    # npm_manage_redirection (destructive - creates, updates, deletes)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_redirection)

    # npm_list_dead_hosts (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_dead_hosts
    )

    # npm_manage_dead_host (destructive - creates, updates, deletes)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_dead_host)
