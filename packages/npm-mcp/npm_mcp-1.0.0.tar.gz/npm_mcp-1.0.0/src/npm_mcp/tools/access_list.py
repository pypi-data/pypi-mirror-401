"""
Access List Management MCP Tools for Nginx Proxy Manager.

This module provides 2 MCP tools for managing IP-based access control:
1. npm_list_access_lists - List all access lists
2. npm_manage_access_list - Create, update, or delete access lists

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

from typing import Any, Literal, TypeAlias

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.tools.compact import compact_access_list
from npm_mcp.types import MCPContext

# Type alias
AccessListResult: TypeAlias = dict[str, Any]


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
# Helper Functions
# =============================================================================


def _validate_create_params(
    name: str | None,
    items: list[dict[str, str]] | None,
) -> AccessListResult | None:
    """Validate create parameters. Returns error dict or None if valid."""
    if not name:
        return {"success": False, "error": "name is required for create operation"}

    if items:
        for item in items:
            directive = item.get("directive")
            if directive not in ["allow", "deny"]:
                return {
                    "success": False,
                    "error": f"Invalid directive '{directive}'. Must be 'allow' or 'deny'",
                }

    return None


def _build_create_data(
    name: str,
    satisfy_any: bool | None,
    pass_auth: bool | None,
    items: list[dict[str, str]] | None,
    clients: list[dict[str, str]] | None,
) -> dict[str, Any]:
    """Build data for create operation."""
    return {
        "name": name,
        "satisfy_any": satisfy_any if satisfy_any is not None else False,
        "pass_auth": pass_auth if pass_auth is not None else False,
        "items": items if items is not None else [],
        "clients": clients if clients is not None else [],
        "meta": {},
    }


def _build_update_data(
    name: str | None,
    satisfy_any: bool | None,
    pass_auth: bool | None,
    items: list[dict[str, str]] | None,
    clients: list[dict[str, str]] | None,
) -> dict[str, Any]:
    """Build data for update operation with only provided fields."""
    data: dict[str, Any] = {}
    if name is not None:
        data["name"] = name
    if satisfy_any is not None:
        data["satisfy_any"] = satisfy_any
    if pass_auth is not None:
        data["pass_auth"] = pass_auth
    if items is not None:
        data["items"] = items
    if clients is not None:
        data["clients"] = clients
    return data


async def _handle_create(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    data: dict[str, Any],
) -> AccessListResult:
    """Handle access list create operation."""
    response = await client.post("/api/nginx/access-lists", json=data)
    server_ctx.logger.info("access_list_created", list_id=response.get("id"))
    return {"success": True, "operation": "create", "access_list": response}


async def _handle_update(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    list_id: int,
    data: dict[str, Any],
) -> AccessListResult:
    """Handle access list update operation."""
    response = await client.put(f"/api/nginx/access-lists/{list_id}", json=data)
    server_ctx.logger.info("access_list_updated", list_id=list_id)
    return {"success": True, "operation": "update", "access_list": response}


async def _handle_delete(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    list_id: int,
) -> AccessListResult:
    """Handle access list delete operation."""
    await client.delete(f"/api/nginx/access-lists/{list_id}")
    server_ctx.logger.info("access_list_deleted", list_id=list_id)
    return {"success": True, "operation": "delete", "list_id": list_id}


# =============================================================================
# MCP Tools
# =============================================================================


async def npm_list_access_lists(
    ctx: MCPContext,
    instance_name: str | None = None,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all access lists for IP-based access control.

    This tool retrieves all configured access lists from the NPM instance,
    including IP rules and HTTP Basic Authentication clients.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - access_lists: list - Array of access list objects
        - total: int - Total number of access lists
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_access_lists(ctx)
        >>> print(f"Found {result['total']} access lists")
        >>> for access_list in result['access_lists']:
        ...     print(f"  - {access_list['name']}: {access_list['client_count']} clients")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_access_lists",
        instance=instance_name or "active",
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all access lists from NPM API
        response = await client.get("/api/nginx/access-lists")

        # Ensure response is a list
        access_lists = response if isinstance(response, list) else []

        # Add client_count to each access list for convenience
        for access_list in access_lists:
            clients = access_list.get("clients", [])
            access_list["client_count"] = len(clients)

        total = len(access_lists)

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_access_lists",
            total=total,
        )

        # Apply compaction if requested (default: True)
        result_lists = [compact_access_list(a) for a in access_lists] if compact else access_lists

        return {
            "success": True,
            "access_lists": result_lists,
            "total": total,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_access_lists", error=str(e))
        return {"success": False, "error": str(e)}


async def npm_manage_access_list(
    ctx: MCPContext,
    operation: Literal["create", "update", "delete"],
    instance_name: str | None = None,
    list_id: int | None = None,
    name: str | None = None,
    satisfy_any: bool | None = None,
    pass_auth: bool | None = None,
    items: list[dict[str, str]] | None = None,
    clients: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """
    Create, update, or delete access lists for IP-based access control and HTTP Basic Auth.

    This tool provides comprehensive access list management including:
    - IP-based access control (allow/deny directives with CIDR notation)
    - HTTP Basic Authentication
    - IPv4 and IPv6 support
    - Satisfy any (OR) or satisfy all (AND) logic

    Args:
        ctx: MCP context (auto-injected)
        operation: Operation to perform (create|update|delete)
        instance_name: Target instance name (optional, uses active instance)
        list_id: Access list ID (required for update/delete)
        name: Human-readable access list name (required for create)
        satisfy_any: Whether to satisfy any rule (OR) or all rules (AND) (optional, default: False)
        pass_auth: Whether to pass authentication to backend (optional, default: False)
        items: List of IP access rules with directive and address (optional)
               Example: [{"directive": "allow", "address": "192.168.1.0/24"}]
        clients: List of HTTP Basic Auth users (optional)
                 Example: [{"username": "admin", "password": "secure_pass"}]

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - access_list: dict - Access list details (for create/update)
        - list_id: int - Access list ID (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create IP-based access list
        >>> result = await npm_manage_access_list(
        ...     ctx,
        ...     operation="create",
        ...     name="Office Network",
        ...     items=[
        ...         {"directive": "allow", "address": "192.168.1.0/24"},
        ...         {"directive": "deny", "address": "all"},
        ...     ],
        ... )
        >>> # Create access list with HTTP Basic Auth
        >>> result = await npm_manage_access_list(
        ...     ctx,
        ...     operation="create",
        ...     name="Protected Area",
        ...     satisfy_any=False,
        ...     items=[{"directive": "allow", "address": "all"}],
        ...     clients=[{"username": "admin", "password": "secure_password"}],
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_access_list",
        operation=operation,
        instance=instance_name or "active",
        list_id=list_id,
    )

    try:
        # Validate operation
        valid_operations = {"create", "update", "delete"}
        if operation not in valid_operations:
            return {
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be: {', '.join(valid_operations)}",
            }

        # Validate parameters based on operation
        if operation == "create":
            validation_error = _validate_create_params(name, items)
            if validation_error:
                return validation_error

        elif operation in ("update", "delete"):
            if not list_id:
                return {
                    "success": False,
                    "error": f"list_id is required for {operation} operation",
                }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        if operation == "create":
            data = _build_create_data(name, satisfy_any, pass_auth, items, clients)  # type: ignore[arg-type]
            return await _handle_create(client, server_ctx, data)

        # list_id validated above for update/delete
        assert list_id is not None  # nosec B101 - type narrowing after validation

        if operation == "update":
            data = _build_update_data(name, satisfy_any, pass_auth, items, clients)
            return await _handle_update(client, server_ctx, list_id, data)

        # operation == "delete"
        return await _handle_delete(client, server_ctx, list_id)

    except Exception as e:
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_access_list", operation=operation, error=str(e)
        )
        return {"success": False, "error": str(e)}


def register_access_list_tools(mcp: FastMCP) -> None:
    """
    Register all access list management tools with the FastMCP server.

    This function registers 2 access list tools:
    - npm_list_access_lists
    - npm_manage_access_list

    Args:
        mcp: FastMCP server instance
    """
    # npm_list_access_lists (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_access_lists
    )

    # npm_manage_access_list (destructive - creates, updates, deletes)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_access_list)
