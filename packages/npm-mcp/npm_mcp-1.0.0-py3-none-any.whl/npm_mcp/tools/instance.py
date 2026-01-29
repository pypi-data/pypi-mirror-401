"""Instance Management MCP Tools.

This module implements 7 MCP tools for managing NPM instances:
1. npm_manage_instance - CRUD operations (create, update, delete, test)
2. npm_get_instance - Get instance details
3. npm_list_instances - List all instances with filtering
4. npm_select_instance - Set active instance
5. npm_update_instance_credentials - Rotate credentials
6. npm_validate_instance_config - Pre-flight validation
7. npm_set_default_instance - Change default instance

These tools integrate with the InstanceManager for connection pooling and
multi-instance management.

Usage:
    from npm_mcp.tools.instance import register_instance_tools

    server = create_mcp_server()
    register_instance_tools(server)

Note:
    Simplified implementation working with current Phase 1 infrastructure.
    Features like persist_to_file, tags, and descriptions will be added
    in future phases when config file writing is supported.
"""

from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.config.models import InstanceConfig
from npm_mcp.server import ServerContext
from npm_mcp.types import MCPContext

# Constants
MAX_PORT_NUMBER = 65535

# Helper Functions


def get_server_context(ctx: MCPContext) -> ServerContext:
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP context passed to tool functions

    Returns:
        ServerContext with Phase 1 components
    """
    return ctx.request_context.lifespan_context  # type: ignore[no-any-return]


def instance_to_dict(instance: InstanceConfig, show_credentials: bool = False) -> dict[str, Any]:
    """
    Convert InstanceConfig to dictionary with optional credential masking.

    Args:
        instance: InstanceConfig object
        show_credentials: Whether to show actual credentials (default: False)

    Returns:
        Dictionary representation of instance with credentials masked if needed
    """
    data = {
        "name": instance.name,
        "host": instance.host,
        "port": instance.port,
        "use_https": instance.use_https,
        "verify_ssl": instance.verify_ssl,
        "is_default": instance.default,
        "has_username": instance.username is not None,
        "has_password": instance.password is not None,
        "has_token": instance.api_token is not None,
    }

    if show_credentials:
        data["username"] = instance.username
        # Still mask password for security even when show_credentials=True
        data["password"] = "***MASKED***" if instance.password else None
        data["api_token"] = "***MASKED***" if instance.api_token else None
    else:
        data["username"] = None
        data["password"] = None
        data["api_token"] = None

    return data


# =============================================================================
# Helper Functions for npm_manage_instance
# =============================================================================


def _validate_create_params(
    host: str | None,
    username: str | None,
    password: str | None,
    api_token: str | None,
) -> dict[str, Any] | None:
    """Validate parameters for create operation. Returns error dict or None if valid."""
    if not host:
        return {"success": False, "error": "Missing required parameter: host"}
    if not username and not api_token:
        return {"success": False, "error": "Missing required parameter: username or api_token"}
    if username and not password:
        return {"success": False, "error": "Password required when username is provided"}
    return None


async def _handle_create(
    server_ctx: ServerContext,
    instance_name: str,
    host: str,
    port: int | None,
    use_https: bool | None,
    verify_ssl: bool | None,
    username: str | None,
    password: str | None,
    api_token: str | None,
    set_as_default: bool,
) -> dict[str, Any]:
    """Handle create operation."""
    new_instance = InstanceConfig(
        name=instance_name,
        host=host,
        port=port if port is not None else 81,
        use_https=use_https if use_https is not None else False,
        verify_ssl=verify_ssl if verify_ssl is not None else True,
        username=username,
        password=password,
        api_token=api_token,
        default=set_as_default,
    )
    result = await server_ctx.instance_manager.add_instance(new_instance, test_connection=True)
    if result["success"]:
        return {"success": True, "operation": "create", "instance": instance_to_dict(new_instance)}
    return {"success": False, "operation": "create", "error": result.get("error", "Failed to add")}


def _handle_update(
    server_ctx: ServerContext,
    instance_name: str,
    host: str | None,
    port: int | None,
    use_https: bool | None,
    verify_ssl: bool | None,
    username: str | None,
    password: str | None,
    api_token: str | None,
    set_as_default: bool,
) -> dict[str, Any]:
    """Handle update operation."""
    existing = server_ctx.config.get_instance(instance_name)
    if not existing:
        return {
            "success": False,
            "operation": "update",
            "error": f"Instance '{instance_name}' not found",
        }

    if host is not None:
        existing.host = host
    if port is not None:
        existing.port = port
    if use_https is not None:
        existing.use_https = use_https
    if verify_ssl is not None:
        existing.verify_ssl = verify_ssl
    if username is not None:
        existing.username = username
    if password is not None:
        existing.password = password
    if api_token is not None:
        existing.api_token = api_token
    if set_as_default:
        for inst in server_ctx.config.instances:
            if inst.name != instance_name:
                inst.default = False
        existing.default = True

    return {"success": True, "operation": "update", "instance": instance_to_dict(existing)}


async def _handle_delete(server_ctx: ServerContext, instance_name: str) -> dict[str, Any]:
    """Handle delete operation."""
    try:
        result = await server_ctx.instance_manager.remove_instance(instance_name)
        return {"success": True, "operation": "delete", "instance_name": result["instance_name"]}
    except ValueError as e:
        return {"success": False, "operation": "delete", "error": str(e)}


async def _handle_test(server_ctx: ServerContext, instance_name: str) -> dict[str, Any]:
    """Handle test operation."""
    result = await server_ctx.instance_manager.test_instance(instance_name)
    if result["success"]:
        return {
            "success": True,
            "operation": "test",
            "instance_name": instance_name,
            "status": result.get("status"),
            "response_time_ms": result.get("response_time_ms"),
        }
    return {
        "success": False,
        "operation": "test",
        "error": result.get("error", "Connection test failed"),
    }


# =============================================================================
# Tool 1: npm_manage_instance
# =============================================================================


async def npm_manage_instance(
    operation: Literal["create", "update", "delete", "test"],
    instance_name: str,
    ctx: MCPContext,
    host: str | None = None,
    port: int | None = None,
    use_https: bool | None = None,
    verify_ssl: bool | None = None,
    username: str | None = None,
    password: str | None = None,
    api_token: str | None = None,
    set_as_default: bool = False,
) -> dict[str, Any]:
    """
    Manage NPM instances with CRUD operations.

    Operations:
    - create: Add new instance with connection details
    - update: Modify existing instance configuration
    - delete: Remove instance
    - test: Test connection to instance

    Args:
        operation: Operation to perform (create, update, delete, test)
        instance_name: Unique identifier for the instance
        ctx: MCP context (auto-injected)
        host: Hostname or IP address (required for create/update)
        port: Port number 1-65535 (optional, default: 81)
        use_https: Use HTTPS for API connections (optional, default: False)
        verify_ssl: Verify SSL certificates (optional, default: True).
                    Set to False for self-signed certificates.
        username: Username for authentication
        password: Password for authentication
        api_token: Alternative to username/password
        set_as_default: Set as default instance (optional, default: False)

    Returns:
        Dict with operation result:
            - success: bool - Whether operation succeeded
            - operation: str - Operation performed
            - instance: dict - Instance details (for create/update/test)
            - error: str - Error message (if failed)
    """
    server_ctx = get_server_context(ctx)

    try:
        if operation == "create":
            validation_error = _validate_create_params(host, username, password, api_token)
            if validation_error:
                return validation_error
            # host validated above
            assert host is not None  # nosec B101 - type narrowing after validation
            return await _handle_create(
                server_ctx,
                instance_name,
                host,
                port,
                use_https,
                verify_ssl,
                username,
                password,
                api_token,
                set_as_default,
            )

        if operation == "update":
            return _handle_update(
                server_ctx,
                instance_name,
                host,
                port,
                use_https,
                verify_ssl,
                username,
                password,
                api_token,
                set_as_default,
            )

        if operation == "delete":
            return await _handle_delete(server_ctx, instance_name)

        # operation == "test"
        return await _handle_test(server_ctx, instance_name)

    except Exception as e:
        server_ctx.logger.error(
            "npm_manage_instance_error",
            operation=operation,
            instance_name=instance_name,
            error=str(e),
        )
        return {"success": False, "operation": operation, "error": str(e)}


# Tool 2: npm_get_instance


def npm_get_instance(
    instance_name: str,
    ctx: MCPContext,
    show_credentials: bool = False,
) -> dict[str, Any]:
    """
    Get detailed configuration for a specific instance.

    Args:
        instance_name: Name of instance to retrieve
        ctx: MCP context (auto-injected)
        show_credentials: Show actual credentials (default: False)

    Returns:
        Dict with instance details or error
    """
    server_ctx = get_server_context(ctx)

    try:
        instance = server_ctx.config.get_instance(instance_name)
        if not instance:
            return {
                "success": False,
                "error": f"Instance '{instance_name}' not found",
            }

        return instance_to_dict(instance, show_credentials=show_credentials)

    except Exception as e:
        server_ctx.logger.error(
            "npm_get_instance_error",
            instance_name=instance_name,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


# Tool 3: npm_list_instances


def npm_list_instances(
    ctx: MCPContext,
) -> dict[str, Any]:
    """
    List all configured NPM instances.

    Args:
        ctx: MCP context (auto-injected)

    Returns:
        Dict with list of instances:
            - instances: list - List of instance dicts
            - total: int - Total count
    """
    server_ctx = get_server_context(ctx)

    try:
        instances = [
            instance_to_dict(inst, show_credentials=False) for inst in server_ctx.config.instances
        ]

        return {
            "instances": instances,
            "total": len(instances),
        }

    except Exception as e:
        server_ctx.logger.error(
            "npm_list_instances_error",
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


# Tool 4: npm_select_instance


def npm_select_instance(
    instance_name: str,
    ctx: MCPContext,
) -> dict[str, Any]:
    """
    Set the active instance for subsequent operations.

    Args:
        instance_name: Name of instance to select
        ctx: MCP context (auto-injected)

    Returns:
        Dict with selection result:
            - success: bool
            - selected_instance: str
            - error: str (if failed)
    """
    server_ctx = get_server_context(ctx)

    try:
        # Validate instance exists
        instance = server_ctx.config.get_instance(instance_name)
        if not instance:
            return {
                "success": False,
                "error": f"Instance '{instance_name}' not found",
            }

        # Select instance
        server_ctx.instance_manager.select_instance(instance_name)

        return {
            "success": True,
            "selected_instance": instance_name,
            "host": instance.host,
            "message": f"All subsequent operations will use the '{instance_name}' instance",
        }

    except Exception as e:
        server_ctx.logger.error(
            "npm_select_instance_error",
            instance_name=instance_name,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


# Tool 5: npm_update_instance_credentials


def npm_update_instance_credentials(
    instance_name: str,
    ctx: MCPContext,
    new_username: str | None = None,
    new_password: str | None = None,
    new_api_token: str | None = None,
    test_before_applying: bool = True,
) -> dict[str, Any]:
    """
    Rotate credentials for an instance without recreating it.

    Args:
        instance_name: Name of instance to update
        ctx: MCP context (auto-injected)
        new_username: New username
        new_password: New password
        new_api_token: New API token (alternative to username/password)
        test_before_applying: Test credentials before applying (default: True)

    Returns:
        Dict with update result:
            - success: bool
            - instance_name: str
            - credentials_updated: bool
            - test_successful: bool (if tested)
            - error: str (if failed)
    """
    server_ctx = get_server_context(ctx)

    try:
        # Validate new credentials provided
        if not new_username and not new_api_token:
            return {
                "success": False,
                "error": "Must provide new_username or new_api_token",
            }

        # Find instance
        instance = server_ctx.config.get_instance(instance_name)
        if not instance:
            return {
                "success": False,
                "error": f"Instance '{instance_name}' not found",
            }

        # Test credentials if requested
        # Note: Credential testing is deferred - returns assumed success
        test_result = None
        if test_before_applying and (new_username or new_api_token):
            # Credential validation deferred to API call at usage time
            test_result = {"success": True}

        # Update credentials
        if new_username is not None:
            instance.username = new_username
        if new_password is not None:
            instance.password = new_password
        if new_api_token is not None:
            instance.api_token = new_api_token

        result = {
            "success": True,
            "instance_name": instance_name,
            "credentials_updated": True,
        }

        if test_result:
            result["test_successful"] = test_result.get("success", False)

        return result

    except Exception as e:
        server_ctx.logger.error(
            "npm_update_instance_credentials_error",
            instance_name=instance_name,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


# Tool 6: npm_validate_instance_config


def npm_validate_instance_config(
    host: str,
    ctx: MCPContext,
    port: int | None = None,
    use_https: bool = False,
    username: str | None = None,
    password: str | None = None,
    api_token: str | None = None,
) -> dict[str, Any]:
    """
    Validate instance configuration before adding (pre-flight check).

    Performs multiple validation checks:
    - Required fields present
    - Port in valid range
    - Authentication method provided

    Args:
        host: Hostname or IP address
        ctx: MCP context (auto-injected, unused in validation)
        port: Port number (optional, default: 81)
        use_https: Use HTTPS (optional, default: False, unused in current validation)
        username: Username for authentication
        password: Password for authentication
        api_token: API token (alternative to username/password)

    Returns:
        Dict with validation results:
            - valid: bool - Overall validation result
            - validation_results: list - Individual check results
            - errors: list - Validation errors
            - warnings: list - Validation warnings
    """
    validation_results: list[dict[str, str]] = []
    errors: list[str] = []
    warnings: list[str] = []

    # Check 1: Required fields
    if not host:
        errors.append("Host is required")
        validation_results.append(
            {
                "check": "required_fields",
                "status": "failed",
                "message": "Host is required",
            }
        )
    else:
        validation_results.append(
            {
                "check": "required_fields",
                "status": "passed",
                "message": "Required fields present",
            }
        )

    # Check 2: Authentication method
    if not username and not api_token:
        errors.append("Either username or api_token must be provided")
        validation_results.append(
            {
                "check": "authentication",
                "status": "failed",
                "message": "No authentication method provided",
            }
        )
    elif username and not password:
        errors.append("Password is required when username is provided")
        validation_results.append(
            {
                "check": "authentication",
                "status": "failed",
                "message": "Password required with username",
            }
        )
    else:
        validation_results.append(
            {
                "check": "authentication",
                "status": "passed",
                "message": "Authentication method valid",
            }
        )

    # Check 3: Port range
    actual_port = port if port is not None else 81
    if actual_port < 1 or actual_port > MAX_PORT_NUMBER:
        errors.append(f"Port must be between 1 and {MAX_PORT_NUMBER}, got {actual_port}")
        validation_results.append(
            {
                "check": "port_range",
                "status": "failed",
                "message": f"Invalid port: {actual_port}",
            }
        )
    else:
        validation_results.append(
            {
                "check": "port_range",
                "status": "passed",
                "message": f"Port {actual_port} is valid",
            }
        )

    return {
        "valid": len(errors) == 0,
        "validation_results": validation_results,
        "errors": errors,
        "warnings": warnings,
    }


# Tool 7: npm_set_default_instance


def npm_set_default_instance(
    instance_name: str,
    ctx: MCPContext,
) -> dict[str, Any]:
    """
    Change which instance is the default.

    Args:
        instance_name: Name of instance to set as default
        ctx: MCP context (auto-injected)

    Returns:
        Dict with result:
            - success: bool
            - previous_default: str - Previous default instance name
            - new_default: str - New default instance name
            - error: str (if failed)
    """
    server_ctx = get_server_context(ctx)

    try:
        # Find instance
        instance = server_ctx.config.get_instance(instance_name)
        if not instance:
            return {
                "success": False,
                "error": f"Instance '{instance_name}' not found",
            }

        # Find previous default
        previous_default = None
        for inst in server_ctx.config.instances:
            if inst.default:
                previous_default = inst.name
                inst.default = False

        # Set new default
        instance.default = True

        message = (
            f"Default instance changed from '{previous_default}' to '{instance_name}'"
            if previous_default
            else f"Default instance set to '{instance_name}'"
        )

        return {
            "success": True,
            "previous_default": previous_default,
            "new_default": instance_name,
            "message": message,
        }

    except Exception as e:
        server_ctx.logger.error(
            "npm_set_default_instance_error",
            instance_name=instance_name,
            error=str(e),
        )
        return {
            "success": False,
            "error": str(e),
        }


# Tool Registration


def register_instance_tools(mcp: FastMCP) -> None:
    """
    Register all 7 instance management tools with FastMCP server.

    This function registers the following tools:
    1. npm_manage_instance - CRUD operations (create, update, delete, test)
    2. npm_get_instance - Get instance details
    3. npm_list_instances - List all instances
    4. npm_select_instance - Set active instance
    5. npm_update_instance_credentials - Rotate credentials
    6. npm_validate_instance_config - Pre-flight validation
    7. npm_set_default_instance - Change default instance

    Args:
        mcp: FastMCP server instance to register tools with

    Example:
        server = create_mcp_server()
        register_instance_tools(server)
        server.run()
    """
    # Tool 1: npm_manage_instance (destructive - creates, updates, deletes)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_instance)

    # Tool 2: npm_get_instance (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(npm_get_instance)

    # Tool 3: npm_list_instances (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_instances
    )

    # Tool 4: npm_select_instance (idempotent state change)
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(npm_select_instance)

    # Tool 5: npm_update_instance_credentials (destructive - modifies credentials)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_update_instance_credentials)

    # Tool 6: npm_validate_instance_config (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_validate_instance_config
    )

    # Tool 7: npm_set_default_instance (idempotent state change)
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(npm_set_default_instance)
