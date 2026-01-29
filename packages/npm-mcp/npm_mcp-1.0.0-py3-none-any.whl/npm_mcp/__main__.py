"""
Entry point for NPM MCP Server.

This module provides the main() function that initializes and runs the MCP server
with configurable transport options.

Transport options:
- stdio (default): Standard input/output for CLI integration
- sse: Server-Sent Events for real-time streaming
- streamable-http: Modern HTTP transport (MCP 2025-03-26 spec)

By default, only category meta-tools are loaded at startup for reduced context usage.
Use --all-tools flag to load all tools at startup (backward compatible behavior).

Usage:
    # Default (stdio transport with lazy loading)
    npm-mcp

    # SSE transport
    npm-mcp --transport sse

    # Streamable HTTP on custom port
    npm-mcp --transport streamable-http --host 0.0.0.0 --port 9000

    # Load all tools at startup
    npm-mcp --all-tools

    # Environment variables
    NPM_MCP_TRANSPORT=streamable-http NPM_MCP_PORT=8080 npm-mcp
"""

import argparse
import os


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Arguments can also be set via environment variables:
    - NPM_MCP_ALL_TOOLS: Load all tools at startup (true/1/yes)
    - NPM_MCP_TRANSPORT: Transport protocol (stdio/sse/streamable-http)
    - NPM_MCP_HOST: Host for HTTP transport (default: 127.0.0.1)
    - NPM_MCP_PORT: Port for HTTP transport (default: 8000)

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="npm-mcp",
        description="NPM MCP Server - Manage Nginx Proxy Manager via MCP protocol",
    )
    parser.add_argument(
        "--all-tools",
        action="store_true",
        default=os.environ.get("NPM_MCP_ALL_TOOLS", "").lower() in ("true", "1", "yes"),
        help="Load all tools at startup instead of lazy loading (env: NPM_MCP_ALL_TOOLS)",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default=os.environ.get("NPM_MCP_TRANSPORT", "stdio"),
        help="Transport protocol (default: stdio, env: NPM_MCP_TRANSPORT)",
    )
    parser.add_argument(
        "--host",
        default=os.environ.get("NPM_MCP_HOST", "127.0.0.1"),
        help="Host for HTTP transport (default: 127.0.0.1, env: NPM_MCP_HOST)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("NPM_MCP_PORT", "8000")),
        help="Port for HTTP transport (default: 8000, env: NPM_MCP_PORT)",
    )
    return parser.parse_args()


def main() -> int:
    """
    Initialize and run the MCP server.

    This function:
    1. Parses CLI arguments (with environment variable fallbacks)
    2. Creates the FastMCP server instance with CategoryManager
    3. Optionally enables all tool categories (if --all-tools flag is set)
    4. Runs the server with the selected transport
    5. Handles graceful shutdown on KeyboardInterrupt

    Returns:
        Exit code (0 for success).
    """
    args = parse_args()

    # Configure tool loading before creating server
    if args.all_tools:
        from npm_mcp.server import set_load_all_tools

        set_load_all_tools(True)

    try:
        # Create MCP server with CategoryManager
        # - If --all-tools: all tools registered at startup
        # - Otherwise: only category meta-tools registered (lazy loading)
        from npm_mcp.server import create_mcp_server

        server = create_mcp_server(host=args.host, port=args.port)

        # Run with selected transport (blocking call)
        server.run(transport=args.transport)
        return 0
    except KeyboardInterrupt:
        # Graceful shutdown on Ctrl+C (Unix convention: 128 + SIGINT(2) = 130)
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
