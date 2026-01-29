"""Tool category definitions and meta-tools for hierarchical tool management.

This module provides category-based lazy loading of tools to reduce context
window consumption. Instead of loading all 28 tools at startup, only 3
meta-tools are exposed initially. Users can enable specific categories
on-demand.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import structlog
from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

if TYPE_CHECKING:
    from collections.abc import Callable

logger = structlog.get_logger()

# Error message constant to avoid duplication
_MANAGER_NOT_INITIALIZED_ERROR = "Category manager not initialized"


@dataclass
class CategoryDefinition:
    """Definition of a tool category."""

    name: str
    description: str
    tool_names: list[str]
    register_func: Callable[[FastMCP[Any]], None]


# Category definitions with their tools
CATEGORY_DEFINITIONS: dict[str, CategoryDefinition] = {}


def _define_categories() -> None:
    """Define all tool categories.

    This is called lazily to avoid circular imports.
    """
    if CATEGORY_DEFINITIONS:
        return  # Already defined

    from npm_mcp.tools.access_list import register_access_list_tools
    from npm_mcp.tools.bulk import register_bulk_tools
    from npm_mcp.tools.certificate import register_certificate_tools
    from npm_mcp.tools.instance import register_instance_tools
    from npm_mcp.tools.proxy_host import register_proxy_host_tools
    from npm_mcp.tools.redirection import register_redirection_tools
    from npm_mcp.tools.stream import register_stream_tools
    from npm_mcp.tools.system import register_system_tools
    from npm_mcp.tools.user import register_user_tools

    CATEGORY_DEFINITIONS.update(
        {
            "instance": CategoryDefinition(
                name="instance",
                description="Instance management: configure NPM server connections",
                tool_names=[
                    "npm_list_instances",
                    "npm_manage_instance",
                    "npm_get_instance",
                    "npm_select_instance",
                    "npm_set_default_instance",
                    "npm_update_instance_credentials",
                    "npm_validate_instance_config",
                ],
                register_func=register_instance_tools,
            ),
            "proxy_host": CategoryDefinition(
                name="proxy_host",
                description="Proxy hosts: manage reverse proxy configurations",
                tool_names=[
                    "npm_list_proxy_hosts",
                    "npm_get_proxy_host",
                    "npm_manage_proxy_host",
                ],
                register_func=register_proxy_host_tools,
            ),
            "certificate": CategoryDefinition(
                name="certificate",
                description="SSL certificates: manage Let's Encrypt and custom certificates",
                tool_names=[
                    "npm_list_certificates",
                    "npm_manage_certificate",
                    "npm_validate_certificate",
                ],
                register_func=register_certificate_tools,
            ),
            "access_list": CategoryDefinition(
                name="access_list",
                description="Access lists: IP-based access control and HTTP Basic Auth",
                tool_names=[
                    "npm_list_access_lists",
                    "npm_manage_access_list",
                ],
                register_func=register_access_list_tools,
            ),
            "stream": CategoryDefinition(
                name="stream",
                description="Streams: TCP/UDP port forwarding",
                tool_names=[
                    "npm_list_streams",
                    "npm_manage_stream",
                ],
                register_func=register_stream_tools,
            ),
            "redirection": CategoryDefinition(
                name="redirection",
                description="Redirections and dead hosts: URL redirects and 404 handlers",
                tool_names=[
                    "npm_list_redirections",
                    "npm_manage_redirection",
                    "npm_list_dead_hosts",
                    "npm_manage_dead_host",
                ],
                register_func=register_redirection_tools,
            ),
            "user": CategoryDefinition(
                name="user",
                description="Users: manage NPM user accounts",
                tool_names=[
                    "npm_list_users",
                    "npm_manage_user",
                ],
                register_func=register_user_tools,
            ),
            "system": CategoryDefinition(
                name="system",
                description="System: settings, audit logs, and host reports",
                tool_names=[
                    "npm_get_system_settings",
                    "npm_update_system_settings",
                    "npm_get_audit_logs",
                    "npm_get_host_reports",
                ],
                register_func=register_system_tools,
            ),
            "bulk": CategoryDefinition(
                name="bulk",
                description="Bulk operations: batch processing, export/import configurations",
                tool_names=[
                    "npm_bulk_operations",
                ],
                register_func=register_bulk_tools,
            ),
        }
    )


class CategoryManager:
    """Manages tool categories with lazy loading support."""

    def __init__(self, server: FastMCP[Any]) -> None:
        """Initialize the category manager.

        Args:
            server: The FastMCP server instance.
        """
        self._server = server
        self._enabled_categories: set[str] = set()
        _define_categories()

    def list_categories(self) -> list[dict[str, Any]]:
        """List all available categories.

        Returns:
            List of category information dictionaries.
        """
        return [
            {
                "name": cat.name,
                "description": cat.description,
                "tool_count": len(cat.tool_names),
                "tools": cat.tool_names,
                "enabled": cat.name in self._enabled_categories,
            }
            for cat in CATEGORY_DEFINITIONS.values()
        ]

    def enable_category(self, name: str) -> dict[str, Any]:
        """Enable a category and register its tools.

        Args:
            name: Category name to enable.

        Returns:
            Result dictionary with enabled tools.

        Raises:
            ValueError: If category doesn't exist.
        """
        if name not in CATEGORY_DEFINITIONS:
            available = ", ".join(CATEGORY_DEFINITIONS.keys())
            msg = f"Category '{name}' not found. Available: {available}"
            raise ValueError(msg)

        category = CATEGORY_DEFINITIONS[name]

        if name in self._enabled_categories:
            return {
                "success": True,
                "category": name,
                "already_enabled": True,
                "tools": category.tool_names,
            }

        # Register the tools
        category.register_func(self._server)
        self._enabled_categories.add(name)

        logger.info(
            "category_enabled",
            category=name,
            tools=category.tool_names,
        )

        return {
            "success": True,
            "category": name,
            "already_enabled": False,
            "tools": category.tool_names,
            "message": f"Enabled {len(category.tool_names)} tools from '{name}' category",
        }

    def disable_category(self, name: str) -> dict[str, Any]:
        """Mark a category as disabled.

        Note: FastMCP doesn't support unregistering tools at runtime.
        This marks the category as disabled but tools remain available
        until server restart.

        Args:
            name: Category name to disable.

        Returns:
            Result dictionary.

        Raises:
            ValueError: If category doesn't exist.
        """
        if name not in CATEGORY_DEFINITIONS:
            available = ", ".join(CATEGORY_DEFINITIONS.keys())
            msg = f"Category '{name}' not found. Available: {available}"
            raise ValueError(msg)

        if name not in self._enabled_categories:
            return {
                "success": True,
                "category": name,
                "was_enabled": False,
                "message": f"Category '{name}' was not enabled",
            }

        self._enabled_categories.discard(name)

        logger.info("category_disabled", category=name)

        return {
            "success": True,
            "category": name,
            "was_enabled": True,
            "message": (
                f"Category '{name}' marked as disabled. "
                "Note: Tools remain registered until server restart."
            ),
        }

    def enable_all(self) -> dict[str, Any]:
        """Enable all categories.

        Returns:
            Result dictionary with all enabled tools.
        """
        all_tools: list[str] = []
        for name in CATEGORY_DEFINITIONS:
            if name not in self._enabled_categories:
                result = self.enable_category(name)
                all_tools.extend(result.get("tools", []))

        return {
            "success": True,
            "enabled_categories": list(CATEGORY_DEFINITIONS.keys()),
            "total_tools": len(all_tools),
        }

    def get_enabled_categories(self) -> list[str]:
        """Get list of enabled category names."""
        return list(self._enabled_categories)

    @property
    def total_tool_count(self) -> int:
        """Get total number of tools across all categories."""
        return sum(len(cat.tool_names) for cat in CATEGORY_DEFINITIONS.values())


# Global category manager instance (set by server initialization)
_category_manager: CategoryManager | None = None


def get_category_manager() -> CategoryManager | None:
    """Get the global category manager instance."""
    return _category_manager


def set_category_manager(manager: CategoryManager | None) -> None:
    """Set the global category manager instance."""
    global _category_manager  # noqa: PLW0603
    _category_manager = manager


# Meta-tools for category management


def npm_list_categories(
    ctx: Context[Any, Any],
) -> dict[str, Any]:
    """List available tool categories with descriptions.

    Use this to discover what NPM capabilities are available.
    Enable specific categories with npm_enable_category to access their tools.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - categories: list - Available categories with descriptions and tool counts
        - total_tools: int - Total number of tools across all categories
        - enabled_count: int - Number of currently enabled categories
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    categories = manager.list_categories()
    enabled = [c for c in categories if c["enabled"]]

    return {
        "success": True,
        "categories": categories,
        "total_tools": manager.total_tool_count,
        "enabled_count": len(enabled),
    }


def npm_enable_category(
    ctx: Context[Any, Any],
    category: str,
) -> dict[str, Any]:
    """Enable tools in a category, making them available for use.

    After enabling, the category's tools will appear in the available tools list.

    Args:
        category: Category name (instance, project, issue, quality, metrics, rules, task)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - category: str - Category that was enabled
        - tools: list - List of newly available tool names
        - message: str - Status message
        - error: str - Error message (if success is False)
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    try:
        return manager.enable_category(category)
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }


def npm_disable_category(
    ctx: Context[Any, Any],
    category: str,
) -> dict[str, Any]:
    """Disable tools in a category to reduce context usage.

    Note: Due to MCP protocol limitations, tools remain registered until
    server restart. This primarily serves as a signal for future sessions.

    Args:
        category: Category name to disable.

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - category: str - Category that was disabled
        - message: str - Status message
        - error: str - Error message (if success is False)
    """
    manager = get_category_manager()
    if manager is None:
        return {
            "success": False,
            "error": _MANAGER_NOT_INITIALIZED_ERROR,
        }

    try:
        return manager.disable_category(category)
    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
        }


def register_category_tools(mcp: FastMCP[Any]) -> None:
    """Register the category meta-tools with the MCP server.

    These tools are always available regardless of --all-tools flag.
    """
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_categories
    )
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(npm_enable_category)
    mcp.tool(annotations=ToolAnnotations(idempotentHint=True))(npm_disable_category)
