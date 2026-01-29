"""
Stream Management MCP Tools for Nginx Proxy Manager.

This module provides 2 MCP tools for managing TCP/UDP streams:
1. npm_list_streams - List all streams with filtering
2. npm_manage_stream - Create, update, delete, enable, or disable streams

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

from typing import Any, Literal, TypeAlias

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.tools.compact import compact_stream
from npm_mcp.types import MCPContext

# Type alias
StreamResult: TypeAlias = dict[str, Any]


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
# Helper Functions
# =============================================================================


def _filter_streams_by_protocol(
    streams: list[dict[str, Any]],
    protocol: str | None,
) -> list[dict[str, Any]]:
    """Filter streams by protocol type."""
    if not protocol:
        return streams
    if protocol == "tcp":
        return [s for s in streams if s.get("tcp_forwarding", False)]
    if protocol == "udp":
        return [s for s in streams if s.get("udp_forwarding", False)]
    return streams


def _filter_enabled_streams(
    streams: list[dict[str, Any]],
    enabled_only: bool,
) -> list[dict[str, Any]]:
    """Filter streams by enabled status."""
    if not enabled_only:
        return streams
    return [s for s in streams if s.get("enabled", False)]


def _validate_port(port: int | None, param_name: str) -> StreamResult | None:
    """Validate port is in valid range. Returns error dict or None if valid."""
    if port is not None and (port < 1 or port > 65535):
        return {
            "success": False,
            "error": f"{param_name} must be between 1 and 65535, got {port}",
        }
    return None


def _validate_update_ports(
    incoming_port: int | None,
    forwarding_port: int | None,
) -> StreamResult | None:
    """Validate ports for update operation. Returns error dict or None if valid."""
    port_error = _validate_port(incoming_port, "incoming_port")
    if port_error:
        return port_error
    return _validate_port(forwarding_port, "forwarding_port")


def _validate_create_params(
    incoming_port: int | None,
    forwarding_host: str | None,
    forwarding_port: int | None,
    tcp_forwarding: bool | None,
    udp_forwarding: bool | None,
) -> StreamResult | None:
    """Validate create parameters. Returns error dict or None if valid."""
    missing_params = []
    if incoming_port is None:
        missing_params.append("incoming_port")
    if forwarding_host is None:
        missing_params.append("forwarding_host")
    if forwarding_port is None:
        missing_params.append("forwarding_port")
    if tcp_forwarding is None and udp_forwarding is None:
        missing_params.append("tcp_forwarding or udp_forwarding")

    if missing_params:
        return {
            "success": False,
            "error": f"Missing required params for create: {', '.join(missing_params)}",
        }

    # Validate port ranges
    port_error = _validate_port(incoming_port, "incoming_port")
    if port_error:
        return port_error

    port_error = _validate_port(forwarding_port, "forwarding_port")
    if port_error:
        return port_error

    return None


def _build_create_body(
    incoming_port: int,
    forwarding_host: str,
    forwarding_port: int,
    tcp_forwarding: bool | None,
    udp_forwarding: bool | None,
    certificate_id: int | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for create operation."""
    body: dict[str, Any] = {
        "incoming_port": incoming_port,
        "forwarding_host": forwarding_host,
        "forwarding_port": forwarding_port,
        "tcp_forwarding": tcp_forwarding if tcp_forwarding is not None else False,
        "udp_forwarding": udp_forwarding if udp_forwarding is not None else False,
    }

    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if meta is not None:
        body["meta"] = meta

    return body


def _build_update_body(
    incoming_port: int | None,
    forwarding_host: str | None,
    forwarding_port: int | None,
    tcp_forwarding: bool | None,
    udp_forwarding: bool | None,
    certificate_id: int | None,
    meta: dict[str, Any] | None,
) -> dict[str, Any]:
    """Build request body for update operation with only provided fields."""
    body: dict[str, Any] = {}

    if incoming_port is not None:
        body["incoming_port"] = incoming_port
    if forwarding_host is not None:
        body["forwarding_host"] = forwarding_host
    if forwarding_port is not None:
        body["forwarding_port"] = forwarding_port
    if tcp_forwarding is not None:
        body["tcp_forwarding"] = tcp_forwarding
    if udp_forwarding is not None:
        body["udp_forwarding"] = udp_forwarding
    if certificate_id is not None:
        body["certificate_id"] = certificate_id
    if meta is not None:
        body["meta"] = meta

    return body


async def _handle_create(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    body: dict[str, Any],
) -> StreamResult:
    """Handle stream create operation."""
    stream = await client.post("/api/nginx/streams", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_stream",
        operation="create",
        stream_id=stream.get("id"),
    )
    return {"success": True, "operation": "create", "stream": stream}


async def _handle_update(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    stream_id: int,
    body: dict[str, Any],
) -> StreamResult:
    """Handle stream update operation."""
    stream = await client.put(f"/api/nginx/streams/{stream_id}", json=body)
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_stream",
        operation="update",
        stream_id=stream_id,
    )
    return {"success": True, "operation": "update", "stream": stream}


async def _handle_delete(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    stream_id: int,
) -> StreamResult:
    """Handle stream delete operation."""
    await client.delete(f"/api/nginx/streams/{stream_id}")
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_stream",
        operation="delete",
        stream_id=stream_id,
    )
    return {"success": True, "operation": "delete", "stream_id": stream_id}


async def _handle_toggle_enabled(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    stream_id: int,
    enable: bool,
) -> StreamResult:
    """Handle stream enable/disable operation."""
    action = "enable" if enable else "disable"
    stream = await client.post(f"/api/nginx/streams/{stream_id}/{action}")
    server_ctx.logger.info(
        "tool_success",
        tool="npm_manage_stream",
        operation=action,
        stream_id=stream_id,
    )
    return {"success": True, "operation": action, "stream": stream}


# =============================================================================
# MCP Tools
# =============================================================================


async def npm_list_streams(
    ctx: MCPContext,
    instance_name: str | None = None,
    enabled_only: bool = False,
    protocol: Literal["tcp", "udp"] | None = None,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all TCP/UDP streams with optional filtering.

    This tool retrieves all configured streams from the NPM instance,
    with options to filter by enabled status and protocol type.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        enabled_only: Only show enabled streams (default: False)
        protocol: Filter by protocol - 'tcp' or 'udp' (optional)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - streams: list - Array of stream objects (filtered if requested)
        - total: int - Total number of streams before filtering
        - enabled_count: int - Number of enabled streams in result
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_streams(ctx)
        >>> print(f"Found {result['total']} streams")
        >>> for stream in result['streams']:
        ...     print(f"  Port {stream['incoming_port']} -> "
        ...           f"{stream['forwarding_host']}:{stream['forwarding_port']}")

        >>> # Filter by TCP protocol only
        >>> result = await npm_list_streams(ctx, protocol="tcp")

        >>> # Filter by enabled streams only
        >>> result = await npm_list_streams(ctx, enabled_only=True)
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_streams",
        instance=instance_name or "active",
        enabled_only=enabled_only,
        protocol=protocol,
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all streams from NPM API
        response = await client.get("/api/nginx/streams")

        # Ensure response is a list
        streams = response if isinstance(response, list) else []

        # Store total before filtering
        total = len(streams)

        # Apply filters using helpers
        streams = _filter_streams_by_protocol(streams, protocol)
        streams = _filter_enabled_streams(streams, enabled_only)

        # Count enabled streams in final result
        enabled_count = sum(1 for s in streams if s.get("enabled", False))

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_streams",
            total=total,
            filtered_count=len(streams),
            enabled_count=enabled_count,
        )

        # Apply compaction if requested (default: True)
        result_streams = [compact_stream(s) for s in streams] if compact else streams

        return {
            "success": True,
            "streams": result_streams,
            "total": total,
            "enabled_count": enabled_count,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_streams", error=str(e))
        return {"success": False, "error": str(e)}


async def npm_manage_stream(
    ctx: MCPContext,
    operation: Literal["create", "update", "delete", "enable", "disable"],
    instance_name: str | None = None,
    stream_id: int | None = None,
    incoming_port: int | None = None,
    forwarding_host: str | None = None,
    forwarding_port: int | None = None,
    tcp_forwarding: bool | None = None,
    udp_forwarding: bool | None = None,
    certificate_id: int | None = None,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Create, update, delete, enable, or disable TCP/UDP streams.

    This tool provides full CRUD operations for stream management, including
    TCP/UDP port forwarding and optional SSL termination.

    Args:
        ctx: MCP context (auto-injected)
        operation: Operation to perform (create, update, delete, enable, disable)
        instance_name: Target instance name (optional, uses active instance)
        stream_id: Stream ID (required for update/delete/enable/disable)
        incoming_port: Port to listen on (1-65535, required for create)
        forwarding_host: Target host IP/hostname (required for create)
        forwarding_port: Target port (1-65535, required for create)
        tcp_forwarding: Enable TCP forwarding (required for create)
        udp_forwarding: Enable UDP forwarding (required for create)
        certificate_id: SSL certificate ID for SSL termination (optional)
        meta: Additional metadata (optional)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - stream: dict - Stream object (for create/update/enable/disable)
        - stream_id: int - Stream ID (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create a TCP stream for MySQL
        >>> result = await npm_manage_stream(
        ...     ctx,
        ...     operation="create",
        ...     incoming_port=3306,
        ...     forwarding_host="192.168.1.50",
        ...     forwarding_port=3306,
        ...     tcp_forwarding=True,
        ...     udp_forwarding=False,
        ... )

        >>> # Update stream to add UDP
        >>> result = await npm_manage_stream(
        ...     ctx,
        ...     operation="update",
        ...     stream_id=10,
        ...     udp_forwarding=True,
        ... )

        >>> # Disable stream
        >>> result = await npm_manage_stream(
        ...     ctx,
        ...     operation="disable",
        ...     stream_id=10,
        ... )

        >>> # Delete stream
        >>> result = await npm_manage_stream(
        ...     ctx,
        ...     operation="delete",
        ...     stream_id=10,
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_stream",
        operation=operation,
        instance=instance_name or "active",
        stream_id=stream_id,
    )

    # Validate operation
    valid_operations = {"create", "update", "delete", "enable", "disable"}
    if operation not in valid_operations:
        error_msg = f"Invalid operation: {operation}. Must be: {', '.join(valid_operations)}"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    # Validate parameters based on operation
    if operation in {"update", "delete", "enable", "disable"} and stream_id is None:
        error_msg = f"stream_id is required for {operation} operation"
        server_ctx.logger.error("tool_validation_error", error=error_msg)
        return {"success": False, "error": error_msg}

    if operation == "create":
        validation_error = _validate_create_params(
            incoming_port, forwarding_host, forwarding_port, tcp_forwarding, udp_forwarding
        )
        if validation_error:
            server_ctx.logger.error("tool_validation_error", error=validation_error["error"])
            return validation_error

    # Validate port ranges for update operation
    if operation == "update":
        port_error = _validate_update_ports(incoming_port, forwarding_port)
        if port_error:
            server_ctx.logger.error("tool_validation_error", error=port_error["error"])
            return port_error

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        if operation == "create":
            body = _build_create_body(
                incoming_port,  # type: ignore[arg-type]
                forwarding_host,  # type: ignore[arg-type]
                forwarding_port,  # type: ignore[arg-type]
                tcp_forwarding,
                udp_forwarding,
                certificate_id,
                meta,
            )
            return await _handle_create(client, server_ctx, body)

        # stream_id validated above for update/delete/enable/disable
        assert stream_id is not None  # nosec B101 - type narrowing after validation

        if operation == "update":
            body = _build_update_body(
                incoming_port,
                forwarding_host,
                forwarding_port,
                tcp_forwarding,
                udp_forwarding,
                certificate_id,
                meta,
            )
            return await _handle_update(client, server_ctx, stream_id, body)

        if operation == "delete":
            return await _handle_delete(client, server_ctx, stream_id)

        # operation == "enable" or "disable"
        return await _handle_toggle_enabled(client, server_ctx, stream_id, operation == "enable")

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="npm_manage_stream",
            operation=operation,
            error=str(e),
        )
        return {"success": False, "error": str(e)}


def register_stream_tools(server: FastMCP) -> None:
    """
    Register stream management tools with FastMCP server.

    Args:
        server: FastMCP server instance
    """
    # npm_list_streams (read-only, idempotent)
    server.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_streams
    )

    # npm_manage_stream (destructive - creates, updates, deletes, enables, disables)
    server.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_stream)
