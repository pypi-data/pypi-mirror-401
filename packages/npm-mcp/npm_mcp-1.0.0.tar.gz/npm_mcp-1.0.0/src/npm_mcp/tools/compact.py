"""Response compaction utilities for NPM MCP Server.

This module provides functions to strip verbose/redundant fields from API responses
to reduce token usage by ~40-50%.

Usage:
    from npm_mcp.tools.compact import compact_proxy_host, compact_certificate

    # In tool responses:
    return {
        "proxy_hosts": [compact_proxy_host(h) for h in hosts],
        ...
    }
"""

from collections.abc import Callable
from typing import Any

# Essential fields to keep for each resource type
# These are the fields most useful for LLM operations and user display

ESSENTIAL_PROXY_HOST_FIELDS = frozenset(
    {
        "id",
        "domain_names",
        "forward_scheme",
        "forward_host",
        "forward_port",
        "enabled",
        "ssl_forced",
        "certificate_id",
        "access_list_id",
        "block_exploits",
        "caching_enabled",
        "websocket_support",
        "http2_support",
        "hsts_enabled",
    }
)

ESSENTIAL_CERTIFICATE_FIELDS = frozenset(
    {
        "id",
        "nice_name",
        "domain_names",
        "expires_on",
        "provider",
        "created_on",
    }
)

ESSENTIAL_ACCESS_LIST_FIELDS = frozenset(
    {
        "id",
        "name",
        "satisfy_any",
        "pass_auth",
        "items",
        "clients",
        "client_count",  # Computed field added by npm_list_access_lists
    }
)

ESSENTIAL_STREAM_FIELDS = frozenset(
    {
        "id",
        "incoming_port",
        "forwarding_host",
        "forwarding_port",
        "tcp_forwarding",
        "udp_forwarding",
        "enabled",
        "certificate_id",
    }
)

ESSENTIAL_REDIRECTION_FIELDS = frozenset(
    {
        "id",
        "domain_names",
        "forward_scheme",
        "forward_domain_name",
        "forward_http_code",
        "preserve_path",
        "enabled",
        "certificate_id",
        "ssl_forced",
    }
)

ESSENTIAL_DEAD_HOST_FIELDS = frozenset(
    {
        "id",
        "domain_names",
        "enabled",
        "certificate_id",
        "ssl_forced",
    }
)

ESSENTIAL_USER_FIELDS = frozenset(
    {
        "id",
        "name",
        "nickname",
        "email",
        "is_admin",
        "is_disabled",
        "roles",
        "created_on",
    }
)


def _compact_dict(data: dict[str, Any], essential_fields: frozenset[str]) -> dict[str, Any]:
    """Compact a dictionary by keeping only essential fields.

    Args:
        data: The dictionary to compact.
        essential_fields: Set of field names to keep.

    Returns:
        Compacted dictionary with only essential fields.
    """
    return {k: v for k, v in data.items() if k in essential_fields}


def compact_proxy_host(host: dict[str, Any]) -> dict[str, Any]:
    """Compact a proxy host response by keeping essential fields.

    Args:
        host: Full proxy host dictionary from NPM API.

    Returns:
        Compacted proxy host with only essential fields.
    """
    return _compact_dict(host, ESSENTIAL_PROXY_HOST_FIELDS)


def compact_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    """Compact a certificate response by keeping essential fields.

    Args:
        cert: Full certificate dictionary from NPM API.

    Returns:
        Compacted certificate with only essential fields.
    """
    return _compact_dict(cert, ESSENTIAL_CERTIFICATE_FIELDS)


def compact_access_list(access_list: dict[str, Any]) -> dict[str, Any]:
    """Compact an access list response by keeping essential fields.

    Args:
        access_list: Full access list dictionary from NPM API.

    Returns:
        Compacted access list with only essential fields.
    """
    result = _compact_dict(access_list, ESSENTIAL_ACCESS_LIST_FIELDS)

    # Compact nested items - only keep directive and address
    if result.get("items"):
        result["items"] = [
            {"directive": item.get("directive"), "address": item.get("address")}
            for item in result["items"]
        ]

    # Compact nested clients - only keep username (never include passwords)
    if result.get("clients"):
        result["clients"] = [{"username": client.get("username")} for client in result["clients"]]

    return result


def compact_stream(stream: dict[str, Any]) -> dict[str, Any]:
    """Compact a stream response by keeping essential fields.

    Args:
        stream: Full stream dictionary from NPM API.

    Returns:
        Compacted stream with only essential fields.
    """
    return _compact_dict(stream, ESSENTIAL_STREAM_FIELDS)


def compact_redirection(redirection: dict[str, Any]) -> dict[str, Any]:
    """Compact a redirection response by keeping essential fields.

    Args:
        redirection: Full redirection dictionary from NPM API.

    Returns:
        Compacted redirection with only essential fields.
    """
    return _compact_dict(redirection, ESSENTIAL_REDIRECTION_FIELDS)


def compact_dead_host(dead_host: dict[str, Any]) -> dict[str, Any]:
    """Compact a dead host response by keeping essential fields.

    Args:
        dead_host: Full dead host dictionary from NPM API.

    Returns:
        Compacted dead host with only essential fields.
    """
    return _compact_dict(dead_host, ESSENTIAL_DEAD_HOST_FIELDS)


def compact_user(user: dict[str, Any]) -> dict[str, Any]:
    """Compact a user response by keeping essential fields.

    Args:
        user: Full user dictionary from NPM API.

    Returns:
        Compacted user with only essential fields (never includes passwords).
    """
    return _compact_dict(user, ESSENTIAL_USER_FIELDS)


def compact_response_list(
    items: list[dict[str, Any]],
    compact_func: Callable[[dict[str, Any]], dict[str, Any]],
) -> list[dict[str, Any]]:
    """Compact a list of items using the provided compact function.

    Args:
        items: List of dictionaries to compact.
        compact_func: Function to use for compaction.

    Returns:
        List of compacted dictionaries.
    """
    return [compact_func(item) for item in items]
