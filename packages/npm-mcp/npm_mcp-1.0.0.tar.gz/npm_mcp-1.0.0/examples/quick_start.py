#!/usr/bin/env python3
"""
Quick Start Example for NPM MCP Server

This minimal example demonstrates the basic workflow:
1. Add an NPM instance
2. List existing proxy hosts
3. Create a simple proxy host
4. Enable SSL certificate

Prerequisites:
- NPM MCP Server installed (pip install npm-mcp-server)
- NPM instance running and accessible
- Valid NPM credentials

Usage:
    # Set environment variables first:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"

    # Run the example:
    python examples/quick_start.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager


async def main() -> None:
    """Run the quick start example."""

    print("=" * 70)
    print("NPM MCP Server - Quick Start Example")
    print("=" * 70)
    print()

    # Get credentials from environment
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables:")
        print("  - NPM_URL: URL to your NPM instance (e.g., http://localhost:81)")
        print("  - NPM_EMAIL: Your NPM admin email")
        print("  - NPM_PASSWORD: Your NPM admin password")
        print()
        print("Example:")
        print('  export NPM_URL="http://localhost:81"')
        print('  export NPM_EMAIL="admin@example.com"')
        print('  export NPM_PASSWORD="your-password"')
        sys.exit(1)

    try:
        # Initialize configuration and instance manager
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        print("Step 1: Adding NPM instance")
        print("-" * 70)

        # Add NPM instance
        await instance_manager.add_instance(
            name="quickstart",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )
        print(f"✓ Instance 'quickstart' added: {npm_url}")
        print()

        # Get the NPM client
        npm_client = await instance_manager.get_client("quickstart")

        print("Step 2: Listing existing proxy hosts")
        print("-" * 70)

        # List proxy hosts
        hosts = await npm_client.list_proxy_hosts()
        print(f"✓ Found {len(hosts)} existing proxy host(s)")

        if hosts:
            for host in hosts[:3]:  # Show first 3
                print(f"  - {host.domain_names[0]} → {host.forward_host}:{host.forward_port}")
            if len(hosts) > 3:
                print(f"  ... and {len(hosts) - 3} more")
        else:
            print("  (No proxy hosts configured yet)")
        print()

        print("Step 3: Creating a simple proxy host")
        print("-" * 70)

        # Check if example host already exists
        example_domain = "example.local"
        existing = [h for h in hosts if example_domain in h.domain_names]

        if existing:
            print(f"✓ Proxy host for '{example_domain}' already exists (ID: {existing[0].id})")
            proxy_host_id = existing[0].id
        else:
            # Create a new proxy host
            proxy_host = await npm_client.create_proxy_host(
                domain_names=[example_domain],
                forward_scheme="http",
                forward_host="192.168.1.100",
                forward_port=8080,
                block_exploits=True,
                allow_websocket_upgrade=False,
                http2_support=False,
                cache_assets=False,
            )
            proxy_host_id = proxy_host.id
            print(f"✓ Created proxy host '{example_domain}' (ID: {proxy_host_id})")
            print("  Forwarding to: http://192.168.1.100:8080")
        print()

        print("Step 4: SSL Certificate Status")
        print("-" * 70)

        # List certificates
        certificates = await npm_client.list_certificates()
        print(f"✓ Found {len(certificates)} SSL certificate(s)")

        if certificates:
            for cert in certificates[:3]:  # Show first 3
                status = "Valid" if not cert.expires_on else "Expiring"
                print(f"  - {cert.nice_name}: {status}")
                print(f"    Domains: {', '.join(cert.domain_names)}")
        else:
            print("  (No SSL certificates configured yet)")
            print()
            print("  To enable SSL, you would:")
            print("  1. Create a Let's Encrypt certificate")
            print("  2. Attach it to your proxy host")
            print("  3. Force SSL redirection")
        print()

        print("=" * 70)
        print("Quick Start Complete!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  - Explore certificate_management.py for SSL setup")
        print("  - Check bulk_operations.py for batch processing")
        print("  - See multi_instance.py for managing multiple NPM servers")
        print()

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up
        await instance_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())
