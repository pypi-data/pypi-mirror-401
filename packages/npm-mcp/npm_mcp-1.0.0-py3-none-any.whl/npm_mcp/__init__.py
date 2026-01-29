"""
Nginx Proxy Manager MCP Server

A comprehensive Model Context Protocol (MCP) server that enables Large Language Models
to manage Nginx Proxy Manager instances through natural language interactions.

This package provides:
- 28 semantic tools for NPM management
- Multi-instance support with secure credential handling
- Full CRUD operations for all NPM resources
- Production-ready authentication and error handling

Supports multiple transport protocols:
- stdio (default): Standard input/output for CLI integration
- sse: Server-Sent Events for real-time streaming
- streamable-http: Modern HTTP transport (MCP 2025-03-26 spec)
"""

import sys

import structlog

__version__ = "1.0.0"
__author__ = "Wade Woolwine"
__email__ = "wade.woolwine@gmail.com"

# Configure structlog to write to stderr (required for HTTP transport)
# stdout is reserved for JSON-RPC protocol messages in MCP
structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.dev.ConsoleRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.WriteLoggerFactory(file=sys.stderr),
    cache_logger_on_first_use=True,
)
