"""
Type aliases and common types for npm_mcp.

This module provides type aliases for framework types that require
type parameters but where we don't need to be specific.
"""

from typing import Any

from mcp.server.fastmcp import Context as _Context

# Type alias for MCP Context that avoids needing to specify type parameters
# throughout the codebase. The MCP SDK Context is
# Context[ServerSessionT, LifespanContextT, RequestT] but for our purposes
# we don't need to be specific about these.
MCPContext = _Context[Any, Any, Any]
