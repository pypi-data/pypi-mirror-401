"""
User Management MCP Tools for Nginx Proxy Manager.

This module provides 2 MCP tools for managing NPM users and permissions:
1. npm_list_users - List all users
2. npm_manage_user - Create, update, delete users, or change passwords

SECURITY CRITICAL:
- Passwords are NEVER logged (even in debug mode)
- Passwords are NEVER returned in responses
- All password fields are masked with "***REDACTED***"
- Password validation is performed before API calls

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

import re
from typing import Any, Literal

import structlog
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.constants import API_USERS, REDACTED
from npm_mcp.tools.compact import compact_user
from npm_mcp.types import MCPContext

# Initialize logger for this module
logger = structlog.get_logger(__name__)


def get_server_context(ctx: MCPContext) -> Any:  # noqa: ANN401  # noqa: ANN401
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP Context object

    Returns:
        ServerContext with config, instance_manager, auth_manager, logger
    """
    return ctx.request_context.lifespan_context


def _mask_sensitive_data(data: dict[str, Any]) -> dict[str, Any]:
    """
    Mask sensitive fields (passwords) in data dictionary.

    This function recursively masks password fields to prevent accidental
    logging or exposure of sensitive information.

    Args:
        data: Dictionary that may contain sensitive fields

    Returns:
        Dictionary with sensitive fields masked

    Security:
        - Masks: password, secret, current_password, new_password, old_password
        - Returns "***REDACTED***" for all password fields
    """
    masked = data.copy()
    sensitive_keys = {
        "password",
        "secret",
        "current_password",
        "new_password",
        "old_password",
        "current",
        "old",
    }

    for key in masked:
        if key.lower() in sensitive_keys:
            masked[key] = REDACTED
        elif isinstance(masked[key], dict):
            masked[key] = _mask_sensitive_data(masked[key])
        elif isinstance(masked[key], list):
            masked[key] = [
                _mask_sensitive_data(item) if isinstance(item, dict) else item
                for item in masked[key]
            ]

    return masked


def _validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if email format is valid, False otherwise
    """
    # Basic email validation pattern
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def _remove_sensitive_fields(response: dict[str, Any]) -> dict[str, Any]:
    """Remove password/secret fields from response."""
    return {k: v for k, v in response.items() if k not in {"password", "secret"}}


def _validate_create_user_params(
    name: str | None,
    email: str | None,
    password: str | None,
) -> dict[str, Any] | None:
    """Validate create user parameters. Returns error dict or None if valid."""
    if not name or not email or not password:
        return {
            "success": False,
            "error": "Missing required fields for create: name, email, password",
        }
    if not _validate_email(email):
        return {"success": False, "error": f"Invalid email format: {email}"}
    return None


def _sanitize_error_message(
    error_msg: str,
    password: str | None,
    current_password: str | None,
    new_password: str | None,
) -> str:
    """Remove any passwords that might appear in error message."""
    if password and password in error_msg:
        error_msg = error_msg.replace(password, REDACTED)
    if current_password and current_password in error_msg:
        error_msg = error_msg.replace(current_password, REDACTED)
    if new_password and new_password in error_msg:
        error_msg = error_msg.replace(new_password, REDACTED)
    return error_msg


async def _handle_create_user(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    *,
    name: str,
    email: str,
    password: str,
    is_admin: bool,
    is_disabled: bool,
) -> dict[str, Any]:
    """Handle user create operation."""
    request_body: dict[str, Any] = {
        "email": email,
        "name": name,
        "secret": password,
        "is_disabled": is_disabled,
    }
    if is_admin:
        request_body["roles"] = ["admin"]

    masked_body = _mask_sensitive_data(request_body)
    server_ctx.logger.debug("api_request", endpoint=API_USERS, method="POST", body=masked_body)

    response = await client.post(API_USERS, json=request_body)
    safe_response = _remove_sensitive_fields(response)

    server_ctx.logger.info(
        "tool_success", tool="npm_manage_user", operation="create", user_id=response.get("id")
    )
    return {"success": True, "operation": "create", "user": safe_response}


async def _handle_update_user(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    user_id: int,
    *,
    name: str | None,
    email: str | None,
    is_admin: bool | None,
    is_disabled: bool | None,
) -> dict[str, Any]:
    """Handle user update operation."""
    request_body: dict[str, Any] = {}
    if name is not None:
        request_body["name"] = name
    if email is not None:
        request_body["email"] = email
    if is_disabled is not None:
        request_body["is_disabled"] = is_disabled
    if is_admin is not None:
        request_body["roles"] = ["admin"] if is_admin else []

    response = await client.put(f"{API_USERS}/{user_id}", json=request_body)
    safe_response = _remove_sensitive_fields(response)

    server_ctx.logger.info(
        "tool_success", tool="npm_manage_user", operation="update", user_id=user_id
    )
    return {"success": True, "operation": "update", "user": safe_response}


async def _handle_delete_user(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    user_id: int,
) -> dict[str, Any]:
    """Handle user delete operation."""
    await client.delete(f"{API_USERS}/{user_id}")

    server_ctx.logger.info(
        "tool_success", tool="npm_manage_user", operation="delete", user_id=user_id
    )
    return {"success": True, "operation": "delete", "message": "User deleted successfully"}


async def _handle_change_password(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    user_id: int,
    current_password: str,
    new_password: str,
) -> dict[str, Any]:
    """Handle user password change operation."""
    request_body = {"type": "password", "current": current_password, "secret": new_password}

    server_ctx.logger.debug(
        "api_request",
        endpoint=f"{API_USERS}/{user_id}",
        method="PUT",
        body={"type": "password", "current": REDACTED, "secret": REDACTED},
    )

    await client.put(f"{API_USERS}/{user_id}", json=request_body)

    server_ctx.logger.info(
        "tool_success", tool="npm_manage_user", operation="change_password", user_id=user_id
    )
    return {
        "success": True,
        "operation": "change_password",
        "message": "Password changed successfully",
    }


# =============================================================================
# MCP Tools
# =============================================================================


async def npm_list_users(
    ctx: MCPContext,
    instance_name: str | None = None,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all NPM users.

    This tool retrieves all user accounts from the NPM instance.
    Passwords are never included in the response.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - users: list - Array of user objects (without passwords)
        - total: int - Total number of users
        - error: str - Error message (if success is False)

    Security:
        - Password fields are never included in responses
        - Only returns user metadata (id, email, name, roles, etc.)

    Example:
        >>> result = await npm_list_users(ctx)
        >>> print(f"Found {result['total']} users")
        >>> for user in result['users']:
        ...     print(f"  {user['name']} ({user['email']}) - Admin: {user.get('is_admin', False)}")

        >>> # List users from specific instance
        >>> result = await npm_list_users(ctx, instance_name="production")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_users",
        instance=instance_name or "active",
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all users from NPM API
        response = await client.get(API_USERS)

        # Ensure response is a list
        users = response if isinstance(response, list) else []

        # Remove any password fields from response (security)
        safe_users = []
        for user in users:
            safe_user = {k: v for k, v in user.items() if k not in {"password", "secret"}}
            safe_users.append(safe_user)

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_users",
            total_users=len(safe_users),
        )

        # Apply compaction if requested (default: True)
        result_users = [compact_user(u) for u in safe_users] if compact else safe_users

        return {
            "success": True,
            "users": result_users,
            "total": len(safe_users),
        }

    except ValueError as e:
        # Instance not found
        error_msg = f"Failed to list users: {e!s}"
        server_ctx.logger.error(
            "tool_error",
            tool="npm_list_users",
            error=error_msg,
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except Exception as e:
        # Generic error handling
        error_msg = f"Failed to list users: {type(e).__name__}: {e!s}"
        server_ctx.logger.error(
            "tool_error",
            tool="npm_list_users",
            error=error_msg,
        )
        return {
            "success": False,
            "error": error_msg,
        }


async def npm_manage_user(
    operation: Literal["create", "update", "delete", "change_password"],
    ctx: MCPContext,
    instance_name: str | None = None,
    user_id: int | None = None,
    name: str | None = None,
    email: str | None = None,
    password: str | None = None,
    current_password: str | None = None,
    new_password: str | None = None,
    is_admin: bool = False,
    is_disabled: bool = False,
) -> dict[str, Any]:
    """
    Create, update, delete users, or change passwords in NPM.

    This tool provides comprehensive user management operations.
    All password operations are secured and passwords are never logged or returned.

    Args:
        operation: Operation to perform (create|update|delete|change_password)
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance)
        user_id: User ID (required for update/delete/change_password)
        name: User's full name (required for create)
        email: User's email address (required for create)
        password: User's password (required for create)
        current_password: Current password (required for change_password)
        new_password: New password (required for change_password)
        is_admin: Whether user is an admin (optional, default: False)
        is_disabled: Whether user account is disabled (optional, default: False)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation that was performed
        - user: dict - User object (for create/update)
        - message: str - Success message (for delete/change_password)
        - error: str - Error message (if success is False)

    Security:
        - Passwords are NEVER logged
        - Passwords are NEVER returned in responses
        - Email format is validated
        - Admin role requires explicit is_admin=True

    Examples:
        >>> # Create a user
        >>> result = await npm_manage_user(
        ...     operation="create",
        ...     name="John Doe",
        ...     email="john@example.com",
        ...     password="securepassword123",
        ...     ctx=ctx
        ... )

        >>> # Create an admin user
        >>> result = await npm_manage_user(
        ...     operation="create",
        ...     name="Admin User",
        ...     email="admin@example.com",
        ...     password="adminpass",
        ...     is_admin=True,
        ...     ctx=ctx
        ... )

        >>> # Update user name
        >>> result = await npm_manage_user(
        ...     operation="update",
        ...     user_id=5,
        ...     name="John Smith",
        ...     ctx=ctx
        ... )

        >>> # Change password
        >>> result = await npm_manage_user(
        ...     operation="change_password",
        ...     user_id=5,
        ...     current_password="oldpass",
        ...     new_password="newpass123",
        ...     ctx=ctx
        ... )

        >>> # Delete user
        >>> result = await npm_manage_user(
        ...     operation="delete",
        ...     user_id=5,
        ...     ctx=ctx
        ... )
    """
    server_ctx = get_server_context(ctx)

    # Log operation WITHOUT sensitive data
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_user",
        operation=operation,
        instance=instance_name or "active",
        user_id=user_id,
        email=email,
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Route to appropriate handler based on operation
        if operation == "create":
            validation_error = _validate_create_user_params(name, email, password)
            if validation_error:
                return validation_error
            # Type assertions - validated above
            assert name is not None  # nosec B101 - type narrowing after validation
            assert email is not None  # nosec B101 - type narrowing after validation
            assert password is not None  # nosec B101 - type narrowing after validation
            return await _handle_create_user(
                client,
                server_ctx,
                name=name,
                email=email,
                password=password,
                is_admin=is_admin,
                is_disabled=is_disabled,
            )

        # Operations requiring user_id
        if user_id is None:
            return {"success": False, "error": f"Missing required field for {operation}: user_id"}

        if operation == "update":
            if email is not None and not _validate_email(email):
                return {"success": False, "error": f"Invalid email format: {email}"}
            return await _handle_update_user(
                client,
                server_ctx,
                user_id,
                name=name,
                email=email,
                is_admin=is_admin,
                is_disabled=is_disabled,
            )

        if operation == "delete":
            return await _handle_delete_user(client, server_ctx, user_id)

        # operation == "change_password"
        if not current_password or not new_password:
            return {
                "success": False,
                "error": "change_password requires: current_password, new_password",
            }
        return await _handle_change_password(
            client, server_ctx, user_id, current_password, new_password
        )

    except ValueError as e:
        error_msg = f"Failed to {operation} user: {e!s}"
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_user", operation=operation, error=error_msg
        )
        return {"success": False, "error": error_msg}

    except Exception as e:
        error_msg = f"Failed to {operation} user: {type(e).__name__}: {e!s}"
        error_msg = _sanitize_error_message(error_msg, password, current_password, new_password)
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_user", operation=operation, error=error_msg
        )
        return {"success": False, "error": error_msg}


def register_user_tools(mcp: FastMCP) -> None:
    """
    Register all user management tools with FastMCP server.

    Args:
        mcp: FastMCP server instance
    """
    # npm_list_users (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(npm_list_users)

    # npm_manage_user (destructive - creates, updates, deletes, changes passwords)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_user)
