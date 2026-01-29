"""System & Reporting MCP Tools for Nginx Proxy Manager.

This module implements 4 MCP tools for system configuration and operational reporting:

1. npm_get_system_settings - Get current system settings
2. npm_update_system_settings - Update system settings
3. npm_get_audit_logs - Retrieve audit logs with filtering
4. npm_get_host_reports - Get performance reports for hosts

All tools support multi-instance management via the instance_name parameter.

Usage:
    These tools are automatically registered with the FastMCP server during
    initialization and can be invoked by LLMs through the MCP protocol.

Example:
    # Get system settings
    >>> result = await npm_get_system_settings(ctx=context)
    >>> print(result["settings"]["letsencrypt_email"])

    # Update settings
    >>> result = await npm_update_system_settings(
    ...     settings={"letsencrypt_email": "admin@example.com"},
    ...     ctx=context
    ... )

    # Get audit logs with filtering
    >>> result = await npm_get_audit_logs(
    ...     start_date="2025-10-01T00:00:00Z",
    ...     user_id=1,
    ...     action_filter="proxy",
    ...     ctx=context
    ... )

    # Get host performance reports
    >>> result = await npm_get_host_reports(
    ...     time_range="24h",
    ...     host_ids=[42, 43],
    ...     ctx=context
    ... )
"""

from datetime import datetime
from typing import Any

import httpx
import structlog
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.client.npm_client import NPMClient
from npm_mcp.server import ServerContext
from npm_mcp.types import MCPContext

# Module logger
logger = structlog.get_logger(__name__)


# Helper Functions


def _get_server_context(ctx: MCPContext) -> ServerContext:
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP context from tool invocation

    Returns:
        ServerContext instance

    Raises:
        RuntimeError: If ServerContext is not available
    """
    server_ctx = ctx.request_context.lifespan_context
    if not isinstance(server_ctx, ServerContext):
        msg = "ServerContext not available in lifespan_context"
        raise RuntimeError(msg)
    return server_ctx


async def _get_instance_client(ctx: MCPContext, instance_name: str | None = None) -> NPMClient:
    """
    Get NPM client for specified instance or active instance.

    Args:
        ctx: MCP context
        instance_name: Optional instance name, uses active if not specified

    Returns:
        NPM client for the instance

    Raises:
        ValueError: If instance not found
    """
    server_ctx = _get_server_context(ctx)
    return await server_ctx.instance_manager.get_client(instance_name)


def _build_audit_log_params(
    start_date: str | None,
    end_date: str | None,
    user_id: int | None,
    action_filter: str | None,
    page: int | None,
    limit: int | None,
) -> dict[str, Any]:
    """Build query parameters for audit log request."""
    params: dict[str, Any] = {}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if user_id is not None:
        params["user_id"] = user_id
    if action_filter:
        params["action_filter"] = action_filter
    if page is not None:
        params["page"] = page
    if limit is not None:
        params["limit"] = limit
    return params


def _process_audit_log_response(audit_logs: Any) -> dict[str, Any]:  # noqa: ANN401
    """Process audit log API response into standard format."""
    if isinstance(audit_logs, list):
        return {"success": True, "audit_logs": audit_logs, "total": len(audit_logs)}

    result = {
        "success": True,
        "audit_logs": audit_logs.get("logs", audit_logs),
        "total": audit_logs.get("total", len(audit_logs.get("logs", []))),
    }
    if "page" in audit_logs:
        result["page"] = audit_logs["page"]
    if "pages" in audit_logs:
        result["pages"] = audit_logs["pages"]
    return result


def _validate_time_range(time_range: str) -> bool:
    """
    Validate time range is one of the allowed values.

    Args:
        time_range: Time range string to validate

    Returns:
        True if valid

    Raises:
        ValueError: If time range is invalid
    """
    valid_ranges = {"1h", "24h", "7d", "30d"}
    if time_range not in valid_ranges:
        msg = f"Invalid time_range: {time_range}. Must be one of {valid_ranges}"
        raise ValueError(msg)
    return True


def _validate_iso_date(date_str: str) -> bool:
    """
    Validate ISO 8601 date format.

    Args:
        date_str: Date string to validate

    Returns:
        True if valid

    Raises:
        ValueError: If date format is invalid
    """
    try:
        datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return True
    except (ValueError, AttributeError) as e:
        msg = (
            f"Invalid date format: {date_str}. Expected ISO 8601 format "
            "(e.g., 2025-10-26T10:00:00Z)"
        )
        raise ValueError(msg) from e


# Tool Implementations


async def npm_get_system_settings(
    ctx: MCPContext,
    instance_name: str | None = None,
) -> dict[str, Any]:
    """
    Get current system settings from NPM instance.

    Retrieves global system configuration including Let's Encrypt settings,
    default feature flags, and system-wide preferences.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target NPM instance (optional, uses active instance)

    Returns:
        Dict containing:
            - success: bool - Operation success status
            - settings: dict - System settings object
            - error: str - Error message (only if success=False)

    Example:
        >>> result = await npm_get_system_settings(ctx=context)
        >>> print(result["settings"]["letsencrypt_email"])
        "admin@example.com"
    """
    logger.info(
        "tool.get_system_settings.start",
        instance_name=instance_name or "active",
    )

    try:
        # Get NPM client
        client = await _get_instance_client(ctx, instance_name)

        # Fetch settings from NPM API
        response = await client.get("/api/settings")
        settings = response.json()

        logger.info(
            "tool.get_system_settings.success",
            instance_name=instance_name or "active",
        )

        return {
            "success": True,
            "settings": settings,
        }

    except ValueError as e:
        # Instance not found
        error_msg = str(e)
        logger.error(
            "tool.get_system_settings.error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except httpx.HTTPStatusError as e:
        # API error
        response_text = e.response.text if hasattr(e.response, "text") else str(e)
        error_msg = f"HTTP {e.response.status_code}: {response_text}"
        logger.error(
            "tool.get_system_settings.http_error",
            error=error_msg,
            status_code=e.response.status_code,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error: {e!s}"
        logger.error(
            "tool.get_system_settings.unexpected_error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }


async def npm_update_system_settings(
    ctx: MCPContext,
    settings: dict[str, Any],
    instance_name: str | None = None,
) -> dict[str, Any]:
    """
    Update system settings in NPM instance.

    Updates global system configuration. Only the provided settings are updated,
    others remain unchanged.

    Args:
        ctx: MCP context (auto-injected)
        settings: Dict of settings to update (key-value pairs)
        instance_name: Target NPM instance (optional, uses active instance)

    Returns:
        Dict containing:
            - success: bool - Operation success status
            - updated_settings: dict - Updated settings object
            - error: str - Error message (only if success=False)

    Example:
        >>> result = await npm_update_system_settings(
        ...     settings={"letsencrypt_email": "newemail@example.com"},
        ...     ctx=context
        ... )
        >>> print(result["updated_settings"]["letsencrypt_email"])
        "newemail@example.com"
    """
    logger.info(
        "tool.update_system_settings.start",
        instance_name=instance_name or "active",
        settings_keys=list(settings.keys()) if settings else [],
    )

    try:
        # Validate settings is not empty
        if not settings:
            msg = "Settings dictionary cannot be empty"
            raise ValueError(msg)

        # Get NPM client
        client = await _get_instance_client(ctx, instance_name)

        # Update settings via NPM API
        updated_settings = await client.put("/api/settings", json=settings)

        logger.info(
            "tool.update_system_settings.success",
            instance_name=instance_name or "active",
            updated_keys=list(settings.keys()),
        )

        return {
            "success": True,
            "updated_settings": updated_settings,
        }

    except ValueError as e:
        # Validation error or instance not found
        error_msg = str(e)
        logger.error(
            "tool.update_system_settings.error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except httpx.HTTPStatusError as e:
        # API error
        response_text = e.response.text if hasattr(e.response, "text") else str(e)
        error_msg = f"HTTP {e.response.status_code}: {response_text}"
        logger.error(
            "tool.update_system_settings.http_error",
            error=error_msg,
            status_code=e.response.status_code,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error: {e!s}"
        logger.error(
            "tool.update_system_settings.unexpected_error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }


async def npm_get_audit_logs(
    ctx: MCPContext,
    instance_name: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    user_id: int | None = None,
    action_filter: str | None = None,
    page: int | None = None,
    limit: int | None = None,
) -> dict[str, Any]:
    """
    Retrieve audit logs from NPM instance with optional filtering.

    Fetches audit logs with support for date range, user, and action filtering,
    as well as pagination for large result sets.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target NPM instance (optional, uses active instance)
        start_date: Filter start date in ISO 8601 format (optional)
        end_date: Filter end date in ISO 8601 format (optional)
        user_id: Filter by user ID (optional)
        action_filter: Filter by action keyword (optional)
        page: Page number for pagination (optional)
        limit: Results per page (optional)

    Returns:
        Dict containing:
            - success: bool - Operation success status
            - audit_logs: list - Array of audit log entries
            - total: int - Total number of logs
            - page: int - Current page (if paginated)
            - pages: int - Total pages (if paginated)
            - error: str - Error message (only if success=False)

    Example:
        >>> result = await npm_get_audit_logs(
        ...     start_date="2025-10-01T00:00:00Z",
        ...     user_id=1,
        ...     action_filter="proxy",
        ...     ctx=context
        ... )
        >>> print(f"Found {result['total']} audit logs")
    """
    logger.info(
        "tool.get_audit_logs.start",
        instance_name=instance_name or "active",
        filters={
            "start_date": start_date,
            "end_date": end_date,
            "user_id": user_id,
            "action_filter": action_filter,
            "page": page,
            "limit": limit,
        },
    )

    try:
        if start_date:
            _validate_iso_date(start_date)
        if end_date:
            _validate_iso_date(end_date)

        client = await _get_instance_client(ctx, instance_name)
        params = _build_audit_log_params(start_date, end_date, user_id, action_filter, page, limit)
        response = await client.get("/api/audit-log", params=params)
        result = _process_audit_log_response(response.json())

        logger.info(
            "tool.get_audit_logs.success",
            instance_name=instance_name or "active",
            total_logs=result["total"],
        )
        return result

    except ValueError as e:
        # Validation error or instance not found
        error_msg = str(e)
        logger.error(
            "tool.get_audit_logs.error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except httpx.HTTPStatusError as e:
        # API error
        response_text = e.response.text if hasattr(e.response, "text") else str(e)
        error_msg = f"HTTP {e.response.status_code}: {response_text}"
        logger.error(
            "tool.get_audit_logs.http_error",
            error=error_msg,
            status_code=e.response.status_code,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error: {e!s}"
        logger.error(
            "tool.get_audit_logs.unexpected_error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }


async def npm_get_host_reports(
    ctx: MCPContext,
    instance_name: str | None = None,
    time_range: str = "24h",
    host_ids: list[int] | None = None,
    metrics: list[str] | None = None,
) -> dict[str, Any]:
    """
    Get performance reports for hosts from NPM instance.

    Retrieves performance metrics for proxy hosts including requests, bandwidth,
    response times, and error rates.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target NPM instance (optional, uses active instance)
        time_range: Time range for report (1h|24h|7d|30d), default: 24h
        host_ids: List of host IDs to filter (optional, all hosts if not specified)
        metrics: List of specific metrics to include (optional, all metrics if not specified)

    Returns:
        Dict containing:
            - success: bool - Operation success status
            - report: dict - Report object with host metrics
            - error: str - Error message (only if success=False)

    Example:
        >>> result = await npm_get_host_reports(
        ...     time_range="7d",
        ...     host_ids=[42, 43],
        ...     ctx=context
        ... )
        >>> for host in result["report"]["hosts"]:
        ...     print(f"{host['domain_names']}: {host['metrics']['total_requests']} requests")
    """
    logger.info(
        "tool.get_host_reports.start",
        instance_name=instance_name or "active",
        time_range=time_range,
        host_ids=host_ids,
        metrics=metrics,
    )

    try:
        # Validate time_range
        _validate_time_range(time_range)

        # Get NPM client
        client = await _get_instance_client(ctx, instance_name)

        # Build query parameters
        params: dict[str, Any] = {"time_range": time_range}
        if host_ids is not None:
            params["host_ids"] = host_ids
        if metrics is not None:
            params["metrics"] = metrics

        # Fetch reports from NPM API
        response = await client.get("/api/reports/hosts", params=params)
        report = response.json()

        logger.info(
            "tool.get_host_reports.success",
            instance_name=instance_name or "active",
            time_range=time_range,
            host_count=len(report.get("hosts", [])),
        )

        return {
            "success": True,
            "report": report,
        }

    except ValueError as e:
        # Validation error or instance not found
        error_msg = str(e)
        logger.error(
            "tool.get_host_reports.error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except httpx.HTTPStatusError as e:
        # API error
        response_text = e.response.text if hasattr(e.response, "text") else str(e)
        error_msg = f"HTTP {e.response.status_code}: {response_text}"
        logger.error(
            "tool.get_host_reports.http_error",
            error=error_msg,
            status_code=e.response.status_code,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }

    except Exception as e:
        # Unexpected error
        error_msg = f"Unexpected error: {e!s}"
        logger.error(
            "tool.get_host_reports.unexpected_error",
            error=error_msg,
            instance_name=instance_name or "active",
        )
        return {
            "success": False,
            "error": error_msg,
        }


# Tool Registration


def register_system_tools(mcp: FastMCP) -> None:
    """
    Register all system & reporting tools with the FastMCP server.

    This function is called during server initialization to register all 4
    system and reporting tools with the MCP server.

    Args:
        mcp: FastMCP server instance

    Example:
        >>> from mcp.server.fastmcp import FastMCP
        >>> server = FastMCP("npm-mcp")
        >>> register_system_tools(server)
    """
    # npm_get_system_settings (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_get_system_settings
    )

    # npm_update_system_settings (destructive - modifies system settings)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_update_system_settings)

    # npm_get_audit_logs (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_get_audit_logs
    )

    # npm_get_host_reports (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_get_host_reports
    )

    logger.info("system_tools.registered", tool_count=4)
