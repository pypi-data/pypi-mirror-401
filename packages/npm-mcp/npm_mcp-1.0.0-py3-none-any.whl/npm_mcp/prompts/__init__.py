"""MCP Prompts for NPM MCP Server.

This module provides pre-built conversation starters that guide LLMs
on how to use tools for common NPM management workflows.

Prompts are registered with the MCP server and can be invoked by clients
to get structured guidance for specific tasks.
"""

from typing import Any

from mcp.server.fastmcp import FastMCP

from npm_mcp.prompts.bulk_operations import register_bulk_prompts
from npm_mcp.prompts.certificate_management import register_certificate_prompts
from npm_mcp.prompts.proxy_setup import register_proxy_prompts
from npm_mcp.prompts.security_review import register_security_prompts


def register_all_prompts(mcp: FastMCP[Any]) -> None:
    """Register all MCP prompts with the server.

    Args:
        mcp: FastMCP server instance.
    """
    register_proxy_prompts(mcp)
    register_certificate_prompts(mcp)
    register_security_prompts(mcp)
    register_bulk_prompts(mcp)
