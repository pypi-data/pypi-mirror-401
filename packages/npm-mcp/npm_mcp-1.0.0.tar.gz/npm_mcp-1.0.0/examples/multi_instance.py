#!/usr/bin/env python3
"""
Multi-Instance Management Example for NPM MCP Server

This example demonstrates managing multiple NPM instances:
1. Configure multiple instances (production, staging, development)
2. Switch between instances
3. Cross-instance comparisons and reporting
4. Sync configurations between instances
5. Failover workflows

Prerequisites:
- NPM MCP Server installed
- Multiple NPM instances running (or use the same instance with different names)
- Valid credentials for each instance

Usage:
    # Set environment variables for each instance:
    export NPM_PROD_URL="http://npm-prod:81"
    export NPM_PROD_EMAIL="admin@example.com"
    export NPM_PROD_PASSWORD="prod-password"

    export NPM_STAGING_URL="http://npm-staging:81"
    export NPM_STAGING_EMAIL="admin@example.com"
    export NPM_STAGING_PASSWORD="staging-password"

    export NPM_DEV_URL="http://npm-dev:81"
    export NPM_DEV_EMAIL="admin@example.com"
    export NPM_DEV_PASSWORD="dev-password"

    # Run the example:
    python examples/multi_instance.py
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager
from npm_mcp.models.proxy_host import ProxyHost


async def main() -> None:
    """Run the multi-instance management example."""

    print("=" * 90)
    print("NPM MCP Server - Multi-Instance Management Example")
    print("=" * 90)
    print()

    # ======================================================================
    # Part 1: Configure Multiple Instances
    # ======================================================================
    print("Part 1: Configuring Multiple Instances")
    print("-" * 90)

    # Initialize
    config = ConfigLoader.load_config()
    instance_manager = InstanceManager(config.global_settings)

    # Define instances
    instances = {
        "production": {
            "url": os.getenv("NPM_PROD_URL"),
            "email": os.getenv("NPM_PROD_EMAIL"),
            "password": os.getenv("NPM_PROD_PASSWORD"),
        },
        "staging": {
            "url": os.getenv("NPM_STAGING_URL"),
            "email": os.getenv("NPM_STAGING_EMAIL"),
            "password": os.getenv("NPM_STAGING_PASSWORD"),
        },
        "development": {
            "url": os.getenv("NPM_DEV_URL"),
            "email": os.getenv("NPM_DEV_EMAIL"),
            "password": os.getenv("NPM_DEV_PASSWORD"),
        },
    }

    # Add instances
    added_instances = []
    for name, creds in instances.items():
        if all(creds.values()):
            try:
                await instance_manager.add_instance(
                    name=name,
                    url=creds["url"],
                    username=creds["email"],
                    password=creds["password"],
                )
                added_instances.append(name)
                print(f"✓ Added instance: {name}")
                print(f"  URL: {creds['url']}")
            except Exception as e:
                print(f"✗ Failed to add {name}: {e}")
        else:
            print(f"⚠️  Skipping {name}: missing credentials")

    print()

    if not added_instances:
        print("ERROR: No instances configured!")
        print()
        print("Please set environment variables:")
        for name in instances:
            env_prefix = f"NPM_{name.upper()}"
            print(f"  {env_prefix}_URL")
            print(f"  {env_prefix}_EMAIL")
            print(f"  {env_prefix}_PASSWORD")
        sys.exit(1)

    print(f"Total instances configured: {len(added_instances)}")
    print()

    try:
        # ======================================================================
        # Part 2: Instance Status and Health Check
        # ======================================================================
        print("Part 2: Instance Status and Health Check")
        print("-" * 90)

        # Check each instance
        print(f"{'Instance':<15} {'URL':<35} {'Status':<15} {'Response Time':<15}")
        print("-" * 80)

        instance_stats = {}
        for name in added_instances:
            try:
                start_time = datetime.now()
                client = await instance_manager.get_client(name)
                # Simple health check - list proxy hosts
                await client.list_proxy_hosts()
                response_time = (datetime.now() - start_time).total_seconds()

                print(
                    f"{name:<15} {instances[name]['url']:<35} {'✓ Online':<15} {response_time:.3f}s"
                )
                instance_stats[name] = {
                    "status": "online",
                    "response_time": response_time,
                }
            except Exception as e:
                print(f"{name:<15} {instances[name]['url']:<35} {'✗ Offline':<15} {'N/A':<15}")
                instance_stats[name] = {
                    "status": "offline",
                    "error": str(e),
                }

        print()

        # ======================================================================
        # Part 3: Cross-Instance Comparison
        # ======================================================================
        print("Part 3: Cross-Instance Resource Comparison")
        print("-" * 90)

        # Collect resource counts from each instance
        resource_counts = {}

        for name in added_instances:
            if instance_stats[name]["status"] == "online":
                client = await instance_manager.get_client(name)

                try:
                    proxy_hosts = await client.list_proxy_hosts()
                    certificates = await client.list_certificates()
                    access_lists = await client.list_access_lists()

                    resource_counts[name] = {
                        "proxy_hosts": len(proxy_hosts),
                        "certificates": len(certificates),
                        "access_lists": len(access_lists),
                        "total": len(proxy_hosts) + len(certificates) + len(access_lists),
                    }
                except Exception as e:
                    print(f"✗ Failed to get resources from {name}: {e}")
                    resource_counts[name] = None

        # Display comparison table
        print(
            f"{'Instance':<15} {'Proxy Hosts':<15} {'Certificates':<15} {'Access Lists':<15} {'Total':<10}"  # noqa: E501
        )
        print("-" * 70)

        for name in added_instances:
            if resource_counts.get(name):
                counts = resource_counts[name]
                print(
                    f"{name:<15} {counts['proxy_hosts']:<15} {counts['certificates']:<15} "
                    f"{counts['access_lists']:<15} {counts['total']:<10}"
                )
            else:
                print(f"{name:<15} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<10}")

        print()

        # ======================================================================
        # Part 4: Find Configuration Differences
        # ======================================================================
        print("Part 4: Configuration Differences Between Instances")
        print("-" * 90)

        # Compare proxy hosts across instances
        all_proxy_hosts: dict[str, list[ProxyHost]] = {}

        for name in added_instances:
            if instance_stats[name]["status"] == "online":
                client = await instance_manager.get_client(name)
                try:
                    all_proxy_hosts[name] = await client.list_proxy_hosts()
                except Exception:
                    all_proxy_hosts[name] = []

        # Find domains unique to each instance
        if len(all_proxy_hosts) >= 2:
            print("Domain differences:")
            print()

            for name, hosts in all_proxy_hosts.items():
                domains = set()
                for host in hosts:
                    domains.update(host.domain_names)

                # Find domains unique to this instance
                other_instances = [n for n in all_proxy_hosts if n != name]
                other_domains = set()
                for other_name in other_instances:
                    for host in all_proxy_hosts[other_name]:
                        other_domains.update(host.domain_names)

                unique_domains = domains - other_domains

                print(f"{name}:")
                print(f"  Total domains: {len(domains)}")
                print(f"  Unique domains: {len(unique_domains)}")
                if unique_domains and len(unique_domains) <= 5:
                    for domain in list(unique_domains)[:5]:
                        print(f"    - {domain}")
                print()

        # ======================================================================
        # Part 5: Configuration Sync Workflow
        # ======================================================================
        print("Part 5: Configuration Sync Workflow")
        print("-" * 90)

        # Simulate syncing a configuration from production to staging
        if "production" in all_proxy_hosts and "staging" in all_proxy_hosts:
            print("Scenario: Sync production configuration to staging")
            print()

            prod_hosts = all_proxy_hosts["production"]
            staging_hosts = all_proxy_hosts["staging"]

            # Find hosts in production but not in staging
            prod_domains = {domain for host in prod_hosts for domain in host.domain_names}
            staging_domains = {domain for host in staging_hosts for domain in host.domain_names}

            missing_in_staging = prod_domains - staging_domains

            print(f"Production domains: {len(prod_domains)}")
            print(f"Staging domains: {len(staging_domains)}")
            print(f"Missing in staging: {len(missing_in_staging)}")
            print()

            if missing_in_staging:
                print("Domains to sync to staging:")
                for domain in list(missing_in_staging)[:5]:
                    print(f"  - {domain}")
                if len(missing_in_staging) > 5:
                    print(f"  ... and {len(missing_in_staging) - 5} more")
                print()

                print("Sync workflow:")
                print("  1. Export production configuration")
                print("  2. Filter for missing domains")
                print("  3. Import to staging instance")
                print("  4. Verify sync completed")
                print()

                print("Note: Use bulk_operations.py export/import for actual sync")
                print()

            else:
                print("✓ Staging is in sync with production")
                print()

        # ======================================================================
        # Part 6: Failover Workflow
        # ======================================================================
        print("Part 6: Failover Workflow")
        print("-" * 90)

        print("Scenario: Production instance failure")
        print()

        # Check if we have a backup instance
        online_instances = [
            name for name in added_instances if instance_stats[name]["status"] == "online"
        ]

        print(f"Online instances: {len(online_instances)}/{len(added_instances)}")
        print()

        if len(online_instances) >= 2:
            primary = online_instances[0]
            secondary = online_instances[1]

            print("Failover steps:")
            print(f"  1. Detect primary ({primary}) failure")
            print(f"  2. Validate secondary ({secondary}) is online")
            print("  3. Switch active instance to secondary")
            print("  4. Update DNS/load balancer")
            print("  5. Monitor secondary performance")
            print("  6. Restore primary when ready")
            print()

            print(f"Active instance: {primary}")
            print(f"Backup instance: {secondary}")
            print("Failover ready: ✓")
            print()

        else:
            print("⚠️  WARNING: Not enough online instances for failover")
            print("   Recommendation: Configure at least 2 instances")
            print()

        # ======================================================================
        # Part 7: Aggregated Reporting
        # ======================================================================
        print("Part 7: Aggregated Reporting Across All Instances")
        print("-" * 90)

        # Calculate totals
        total_hosts = sum(counts["proxy_hosts"] for counts in resource_counts.values() if counts)
        total_certs = sum(counts["certificates"] for counts in resource_counts.values() if counts)
        total_lists = sum(counts["access_lists"] for counts in resource_counts.values() if counts)

        print("Aggregate Statistics:")
        print(f"  Total instances: {len(added_instances)}")
        print(f"  Online instances: {len(online_instances)}")
        print(f"  Total proxy hosts: {total_hosts}")
        print(f"  Total certificates: {total_certs}")
        print(f"  Total access lists: {total_lists}")
        print()

        # Average response time
        response_times = [
            stats["response_time"]
            for stats in instance_stats.values()
            if stats["status"] == "online"
        ]
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            print(f"Average response time: {avg_response:.3f}s")
            print()

        # ======================================================================
        # Summary
        # ======================================================================
        print("=" * 90)
        print("Multi-Instance Management Summary")
        print("=" * 90)
        print()

        print("Capabilities demonstrated:")
        print("  ✓ Multiple instance configuration")
        print("  ✓ Health checking and status monitoring")
        print("  ✓ Cross-instance resource comparison")
        print("  ✓ Configuration difference detection")
        print("  ✓ Configuration sync workflows")
        print("  ✓ Failover planning")
        print("  ✓ Aggregated reporting")
        print()

        print("Best practices:")
        print("  1. Use consistent naming (production, staging, development)")
        print("  2. Tag instances by environment and region")
        print("  3. Monitor all instances for health and performance")
        print("  4. Keep staging in sync with production")
        print("  5. Test failover procedures regularly")
        print("  6. Use separate credentials per instance")
        print()

        print("Next steps:")
        print("  - Set up automated sync jobs (see automated_maintenance.py)")
        print("  - Configure monitoring and alerting")
        print("  - Document failover procedures")
        print("  - Test disaster recovery scenarios")
        print()

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        # Clean up all instances
        await instance_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())
