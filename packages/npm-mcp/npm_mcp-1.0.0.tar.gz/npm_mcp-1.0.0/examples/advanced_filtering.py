#!/usr/bin/env python3
"""
Advanced Filtering Example for NPM MCP Server

This example demonstrates advanced filtering and query techniques:
1. Domain pattern matching (wildcards, regex)
2. Expiration-based filtering (certificates)
3. Status-based filtering (enabled/disabled)
4. Complex filter combinations (AND/OR logic)
5. Resource relationship queries

Prerequisites:
- NPM MCP Server installed
- NPM instance with various resources configured
- Valid NPM credentials

Usage:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"

    python examples/advanced_filtering.py
"""

import asyncio
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager
from npm_mcp.models.certificate import Certificate
from npm_mcp.models.proxy_host import ProxyHost


def match_pattern(text: str, pattern: str) -> bool:
    """
    Match text against a pattern with wildcard support.

    Patterns:
    - * : matches any characters
    - ? : matches single character
    - literal: exact match
    """
    # Convert wildcard pattern to regex
    regex_pattern = pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".")
    return bool(re.match(f"^{regex_pattern}$", text, re.IGNORECASE))


def filter_by_domain_pattern(hosts: list[ProxyHost], pattern: str) -> list[ProxyHost]:
    """Filter proxy hosts by domain pattern."""
    return [
        host
        for host in hosts
        if any(match_pattern(domain, pattern) for domain in host.domain_names)
    ]


def filter_by_expiration(certificates: list[Certificate], days: int) -> list[Certificate]:
    """Filter certificates expiring within specified days."""
    cutoff_ts = int((datetime.now() + timedelta(days=days)).timestamp())
    now_ts = int(datetime.now().timestamp())

    return [
        cert for cert in certificates if cert.expires_on and now_ts < cert.expires_on <= cutoff_ts
    ]


async def main() -> None:
    """Run the advanced filtering example."""

    print("=" * 90)
    print("NPM MCP Server - Advanced Filtering Example")
    print("=" * 90)
    print()

    # Get credentials
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables")
        sys.exit(1)

    try:
        # Initialize
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        await instance_manager.add_instance(
            name="filter_demo",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )
        npm_client = await instance_manager.get_client("filter_demo")

        # Load data
        all_hosts = await npm_client.list_proxy_hosts()
        all_certs = await npm_client.list_certificates()
        all_lists = await npm_client.list_access_lists()

        print("Loaded resources:")
        print(f"  - Proxy hosts: {len(all_hosts)}")
        print(f"  - Certificates: {len(all_certs)}")
        print(f"  - Access lists: {len(all_lists)}")
        print()

        # ======================================================================
        # Part 1: Domain Pattern Matching
        # ======================================================================
        print("Part 1: Domain Pattern Matching")
        print("-" * 90)

        # Example patterns
        patterns = [
            "*.example.com",  # All subdomains of example.com
            "api.*",  # All API-related domains
            "*staging*",  # All staging environments
            "app?.example.com",  # app1, app2, etc.
        ]

        for pattern in patterns:
            matched = filter_by_domain_pattern(all_hosts, pattern)
            print(f"Pattern: {pattern}")
            print(f"  Matches: {len(matched)}")

            if matched:
                for host in matched[:3]:
                    print(f"    - {host.domain_names[0]}")
                if len(matched) > 3:
                    print(f"    ... and {len(matched) - 3} more")
            print()

        # ======================================================================
        # Part 2: Expiration-Based Filtering (Certificates)
        # ======================================================================
        print("Part 2: Expiration-Based Filtering")
        print("-" * 90)

        # Different expiration windows
        windows = [7, 14, 30, 60, 90]

        for days in windows:
            expiring = filter_by_expiration(all_certs, days)
            print(f"Certificates expiring in next {days} days: {len(expiring)}")

            if expiring:
                for cert in expiring[:2]:
                    expires_on = cert.expires_on
                    if expires_on:
                        days_left = (expires_on - int(datetime.now().timestamp())) / 86400
                        print(f"  - {cert.nice_name}: {int(days_left)} days left")

        print()

        # ======================================================================
        # Part 3: Status-Based Filtering
        # ======================================================================
        print("Part 3: Status-Based Filtering")
        print("-" * 90)

        # Enabled vs disabled hosts
        enabled_hosts = [h for h in all_hosts if h.enabled]
        disabled_hosts = [h for h in all_hosts if not h.enabled]

        print(f"Enabled hosts: {len(enabled_hosts)}")
        print(f"Disabled hosts: {len(disabled_hosts)}")
        print()

        # SSL vs non-SSL hosts
        ssl_hosts = [h for h in all_hosts if h.certificate_id is not None]
        non_ssl_hosts = [h for h in all_hosts if h.certificate_id is None]

        print(f"Hosts with SSL: {len(ssl_hosts)}")
        print(f"Hosts without SSL: {len(non_ssl_hosts)}")
        print()

        # Block exploits enabled
        secure_hosts = [h for h in all_hosts if h.block_exploits]
        print(f"Hosts with exploit blocking: {len(secure_hosts)}")
        print()

        # ======================================================================
        # Part 4: Complex Filter Combinations
        # ======================================================================
        print("Part 4: Complex Filter Combinations")
        print("-" * 90)

        # Example 1: Production hosts with SSL
        prod_ssl_hosts = [
            h
            for h in all_hosts
            if h.certificate_id is not None and any("prod" in domain for domain in h.domain_names)
        ]

        print(f"Production hosts with SSL: {len(prod_ssl_hosts)}")
        for host in prod_ssl_hosts[:3]:
            print(f"  - {host.domain_names[0]}")
        print()

        # Example 2: Staging hosts without SSL
        staging_no_ssl = [
            h
            for h in all_hosts
            if h.certificate_id is None and any("staging" in domain for domain in h.domain_names)
        ]

        print(f"Staging hosts WITHOUT SSL: {len(staging_no_ssl)}")
        for host in staging_no_ssl[:3]:
            print(f"  - {host.domain_names[0]}")
        print()

        # Example 3: Disabled API hosts
        disabled_api_hosts = [
            h
            for h in all_hosts
            if not h.enabled and any("api" in domain for domain in h.domain_names)
        ]

        print(f"Disabled API hosts: {len(disabled_api_hosts)}")
        for host in disabled_api_hosts[:3]:
            print(f"  - {host.domain_names[0]}")
        print()

        # Example 4: Expiring certs on enabled hosts
        expiring_on_enabled = []
        expiring_7days = filter_by_expiration(all_certs, 7)

        for cert in expiring_7days:
            # Find hosts using this cert
            hosts_with_cert = [h for h in all_hosts if h.certificate_id == cert.id and h.enabled]
            if hosts_with_cert:
                expiring_on_enabled.append((cert, hosts_with_cert))

        print(f"Expiring certs (7 days) on ENABLED hosts: {len(expiring_on_enabled)}")
        for cert, hosts in expiring_on_enabled[:3]:
            print(f"  - {cert.nice_name}: {len(hosts)} host(s)")
        print()

        # ======================================================================
        # Part 5: Resource Relationship Queries
        # ======================================================================
        print("Part 5: Resource Relationship Queries")
        print("-" * 90)

        # Find certificates with no hosts
        cert_ids_in_use = {h.certificate_id for h in all_hosts if h.certificate_id}
        unused_certs = [c for c in all_certs if c.id not in cert_ids_in_use]

        print(f"Unused certificates: {len(unused_certs)}")
        for cert in unused_certs[:5]:
            print(f"  - {cert.nice_name} (ID: {cert.id})")
        print()

        # Find hosts with specific access list
        if all_lists:
            access_list_id = all_lists[0].id
            hosts_with_list = [h for h in all_hosts if access_list_id in (h.access_list_id or [])]

            print(f"Hosts using access list '{all_lists[0].name}': {len(hosts_with_list)}")
            for host in hosts_with_list[:3]:
                print(f"  - {host.domain_names[0]}")
            print()

        # Find hosts forwarding to specific backend
        backend_port = 8080
        backend_hosts = [h for h in all_hosts if h.forward_port == backend_port]

        print(f"Hosts forwarding to port {backend_port}: {len(backend_hosts)}")
        for host in backend_hosts[:3]:
            print(f"  - {host.domain_names[0]} → {host.forward_host}:{host.forward_port}")
        print()

        # ======================================================================
        # Part 6: Advanced Search Queries
        # ======================================================================
        print("Part 6: Advanced Search Queries")
        print("-" * 90)

        # Query 1: Find all resources related to a domain
        search_domain = "example.com" if all_hosts else "test.com"
        print(f"Searching for resources related to: {search_domain}")
        print()

        # Hosts
        related_hosts = [
            h for h in all_hosts if any(search_domain in domain for domain in h.domain_names)
        ]
        print(f"  Related proxy hosts: {len(related_hosts)}")

        # Certificates
        related_certs = [
            c for c in all_certs if any(search_domain in domain for domain in c.domain_names)
        ]
        print(f"  Related certificates: {len(related_certs)}")
        print()

        # Query 2: Find security gaps
        print("Security Analysis:")
        print()

        # Hosts without exploit blocking
        no_exploit_block = [h for h in all_hosts if not h.block_exploits and h.enabled]
        print(f"  ⚠️  Enabled hosts without exploit blocking: {len(no_exploit_block)}")

        # Enabled hosts without SSL
        enabled_no_ssl = [h for h in all_hosts if h.enabled and h.certificate_id is None]
        print(f"  ⚠️  Enabled hosts without SSL: {len(enabled_no_ssl)}")

        # Hosts without access lists
        no_access_list = [h for h in all_hosts if h.enabled and not h.access_list_id]
        print(f"  💡 Enabled hosts without access lists: {len(no_access_list)}")
        print()

        # ======================================================================
        # Part 7: Custom Filter Functions
        # ======================================================================
        print("Part 7: Custom Filter Examples")
        print("-" * 90)

        # Custom filter: High-traffic hosts (cache assets enabled)
        high_traffic_hosts = [h for h in all_hosts if h.cache_assets]
        print(f"High-traffic hosts (cache enabled): {len(high_traffic_hosts)}")

        # Custom filter: WebSocket-enabled hosts
        websocket_hosts = [h for h in all_hosts if h.allow_websocket_upgrade]
        print(f"WebSocket-enabled hosts: {len(websocket_hosts)}")

        # Custom filter: HTTP/2 hosts
        http2_hosts = [h for h in all_hosts if h.http2_support]
        print(f"HTTP/2-enabled hosts: {len(http2_hosts)}")

        # Custom filter: Hosts created in last 7 days
        week_ago_ts = int((datetime.now() - timedelta(days=7)).timestamp())
        recent_hosts = [h for h in all_hosts if h.created_on >= week_ago_ts]
        print(f"Hosts created in last 7 days: {len(recent_hosts)}")
        print()

        # ======================================================================
        # Summary
        # ======================================================================
        print("=" * 90)
        print("Advanced Filtering Summary")
        print("=" * 90)
        print()

        print("Filtering techniques demonstrated:")
        print("  ✓ Domain pattern matching (wildcards)")
        print("  ✓ Expiration-based filtering")
        print("  ✓ Status-based filtering (enabled/SSL/security)")
        print("  ✓ Complex filter combinations (AND/OR)")
        print("  ✓ Resource relationship queries")
        print("  ✓ Advanced search queries")
        print("  ✓ Custom filter functions")
        print()

        print("Use cases:")
        print("  - Find all hosts matching a pattern for bulk operations")
        print("  - Identify certificates needing renewal")
        print("  - Audit security configuration")
        print("  - Clean up unused resources")
        print("  - Generate compliance reports")
        print()

        print("Next steps:")
        print("  - Apply filters in bulk operations (bulk_operations.py)")
        print("  - Create automated reports (automated_maintenance.py)")
        print("  - Build custom dashboards")
        print()

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await instance_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())
