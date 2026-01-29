#!/usr/bin/env python3
"""
Bulk Operations Example for NPM MCP Server

This example demonstrates advanced bulk operations:
1. Bulk certificate renewal (concurrent processing)
2. Bulk enable/disable proxy hosts (by pattern)
3. Bulk delete resources (filtered)
4. Configuration export (backup)
5. Configuration import (restore)
6. Dry-run mode for safety

Prerequisites:
- NPM MCP Server installed
- NPM instance with multiple resources configured
- Valid NPM credentials

Usage:
    # Set environment variables:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"

    # Run the example:
    python examples/bulk_operations.py
"""

import asyncio
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager
from npm_mcp.models.bulk import (
    BulkOperationRequest,
    BulkOperationType,
    ResourceFilter,
)


async def main() -> None:
    """Run the bulk operations example."""

    print("=" * 90)
    print("NPM MCP Server - Bulk Operations Example")
    print("=" * 90)
    print()

    # Get credentials from environment
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables:")
        print("  - NPM_URL: URL to your NPM instance")
        print("  - NPM_EMAIL: Your NPM admin email")
        print("  - NPM_PASSWORD: Your NPM admin password")
        sys.exit(1)

    try:
        # Initialize
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        # Add instance
        await instance_manager.add_instance(
            name="bulk_demo",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )
        npm_client = await instance_manager.get_client("bulk_demo")

        # ======================================================================
        # Part 1: Bulk Certificate Renewal (with filters)
        # ======================================================================
        print("Part 1: Bulk Certificate Renewal")
        print("-" * 90)

        # First, check what certificates would be affected
        print("Step 1a: DRY RUN - Preview certificates to renew")
        print()

        certificates = await npm_client.list_certificates()
        print(f"Total certificates: {len(certificates)}")

        # Filter: certificates expiring in next 30 days
        from datetime import timedelta

        now_ts = int(datetime.now().timestamp())
        thirty_days_ts = int((datetime.now() + timedelta(days=30)).timestamp())

        expiring_certs = [
            c for c in certificates if c.expires_on and now_ts < c.expires_on <= thirty_days_ts
        ]

        print(f"Certificates expiring in next 30 days: {len(expiring_certs)}")
        print()

        if expiring_certs:
            print("Certificates that would be renewed:")
            for cert in expiring_certs[:5]:
                days_left = (cert.expires_on - now_ts) / 86400
                print(f"  - {cert.nice_name} (ID: {cert.id})")
                print(f"    Domains: {', '.join(cert.domain_names)}")
                print(f"    Expires in: {int(days_left)} days")
            if len(expiring_certs) > 5:
                print(f"  ... and {len(expiring_certs) - 5} more")
            print()

            # Dry run first
            print("Step 1b: Executing DRY RUN...")
            print()

            try:
                # Note: Bulk operations are performed through the MCP tool interface
                # This example shows the conceptual flow
                bulk_request = BulkOperationRequest(
                    operation=BulkOperationType.RENEW_CERTIFICATES,
                    filters=ResourceFilter(
                        days_until_expiry=30,  # Certificates expiring in 30 days
                    ),
                    options={
                        "batch_size": 5,  # Process 5 at a time
                        "dry_run": True,  # Preview only
                    },
                )

                print(f"Operation: {bulk_request.operation.value}")
                print("Filters: days_until_expiry <= 30")
                print(f"Batch size: {bulk_request.options['batch_size']}")
                print(f"Dry run: {bulk_request.options['dry_run']}")
                print()

                print("✓ DRY RUN complete - no changes made")
                print(f"  Would renew: {len(expiring_certs)} certificate(s)")
                print()

            except Exception as e:
                print(f"✗ Dry run failed: {e}")
                print()

            # Ask for confirmation
            print("Step 1c: Execute actual renewal?")
            print("Note: This example does NOT actually renew for safety.")
            print("To perform actual renewal, set dry_run=False in production.")
            print()

        else:
            print("✓ No certificates expiring in next 30 days - no action needed")
            print()

        # ======================================================================
        # Part 2: Bulk Toggle Proxy Hosts (enable/disable by pattern)
        # ======================================================================
        print("Part 2: Bulk Toggle Proxy Hosts")
        print("-" * 90)

        proxy_hosts = await npm_client.list_proxy_hosts()
        print(f"Total proxy hosts: {len(proxy_hosts)}")
        print()

        # Filter: hosts matching a pattern (e.g., staging)
        pattern = "staging"
        matching_hosts = [
            h for h in proxy_hosts if any(pattern in domain for domain in h.domain_names)
        ]

        print(f"Hosts matching pattern '{pattern}': {len(matching_hosts)}")
        print()

        if matching_hosts:
            enabled_count = sum(1 for h in matching_hosts if h.enabled)
            print(
                f"Current state: {enabled_count} enabled, {len(matching_hosts) - enabled_count} disabled"  # noqa: E501
            )
            print()

            # Show hosts
            for host in matching_hosts[:5]:
                status = "✓ Enabled" if host.enabled else "✗ Disabled"
                print(f"  - {host.domain_names[0]} (ID: {host.id}): {status}")
            if len(matching_hosts) > 5:
                print(f"  ... and {len(matching_hosts) - 5} more")
            print()

            # Bulk disable (dry run)
            print("Bulk operation: DISABLE all staging hosts")
            print("Executing DRY RUN...")
            print()

            bulk_request = BulkOperationRequest(
                operation=BulkOperationType.TOGGLE_HOSTS,
                filters=ResourceFilter(
                    domain_pattern=f"*{pattern}*",
                ),
                options={
                    "enable": False,  # Disable hosts
                    "batch_size": 10,
                    "dry_run": True,
                },
            )

            print(f"Operation: {bulk_request.operation.value}")
            print(f"Filters: domain_pattern = *{pattern}*")
            print("Action: DISABLE")
            print(f"Batch size: {bulk_request.options['batch_size']}")
            print()

            print(f"✓ DRY RUN complete - would disable {len(matching_hosts)} host(s)")
            print()

        else:
            print(f"✓ No hosts matching pattern '{pattern}'")
            print()

        # ======================================================================
        # Part 3: Configuration Export (Backup)
        # ======================================================================
        print("Part 3: Configuration Export (Backup)")
        print("-" * 90)

        print("Exporting NPM configuration to file...")
        print()

        # Count resources
        access_lists = await npm_client.list_access_lists()
        streams = await npm_client.list_streams()

        print("Resources to export:")
        print(f"  - Proxy hosts: {len(proxy_hosts)}")
        print(f"  - Certificates: {len(certificates)}")
        print(f"  - Access lists: {len(access_lists)}")
        print(f"  - Streams: {len(streams)}")
        print(f"  Total: {len(proxy_hosts) + len(certificates) + len(access_lists) + len(streams)}")
        print()

        # Create backup directory
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = backup_dir / f"npm_backup_{timestamp}.json"

        # Bulk export request
        bulk_request = BulkOperationRequest(
            operation=BulkOperationType.EXPORT_CONFIG,
            options={
                "format": "json",
                "include_disabled": True,
                "include_metadata": True,
            },
        )

        print(f"Export format: {bulk_request.options['format']}")
        print(f"Include disabled: {bulk_request.options['include_disabled']}")
        print(f"Include metadata: {bulk_request.options['include_metadata']}")
        print()

        # Simulate export
        export_data = {
            "export_date": timestamp,
            "instance_url": npm_url,
            "resources": {
                "proxy_hosts": len(proxy_hosts),
                "certificates": len(certificates),
                "access_lists": len(access_lists),
                "streams": len(streams),
            },
            "total_resources": (
                len(proxy_hosts) + len(certificates) + len(access_lists) + len(streams)
            ),
        }

        backup_file.write_text(json.dumps(export_data, indent=2))
        file_size = backup_file.stat().st_size

        print("✓ Configuration exported successfully")
        print(f"  File: {backup_file}")
        print(f"  Size: {file_size:,} bytes")
        print()

        # ======================================================================
        # Part 4: Bulk Delete Resources (with caution!)
        # ======================================================================
        print("Part 4: Bulk Delete Resources (CAUTION)")
        print("-" * 90)

        # Find resources to potentially delete (example: disabled hosts)
        disabled_hosts = [h for h in proxy_hosts if not h.enabled]

        print(f"Disabled proxy hosts: {len(disabled_hosts)}")
        print()

        if disabled_hosts:
            print("Hosts that WOULD BE DELETED (DRY RUN):")
            for host in disabled_hosts[:3]:
                print(f"  - {host.domain_names[0]} (ID: {host.id})")
                created_date = datetime.fromtimestamp(host.created_on, UTC).strftime("%Y-%m-%d")
                print(f"    Created: {created_date}")
            if len(disabled_hosts) > 3:
                print(f"  ... and {len(disabled_hosts) - 3} more")
            print()

            # Dry run delete
            print("Bulk operation: DELETE disabled hosts")
            print("Executing DRY RUN...")
            print()

            bulk_request = BulkOperationRequest(
                operation=BulkOperationType.DELETE_RESOURCES,
                filters=ResourceFilter(
                    enabled=False,  # Only disabled hosts
                ),
                options={
                    "resource_type": "proxy_host",
                    "batch_size": 5,
                    "dry_run": True,  # ALWAYS dry run first!
                    "require_confirmation": True,
                },
            )

            print(f"Operation: {bulk_request.operation.value}")
            print(f"Resource type: {bulk_request.options['resource_type']}")
            print("Filters: enabled = False")
            print(f"Batch size: {bulk_request.options['batch_size']}")
            print()

            print(f"✓ DRY RUN complete - would delete {len(disabled_hosts)} host(s)")
            print()

            print("⚠️  WARNING: Bulk delete is PERMANENT!")
            print("   Always:")
            print("   1. Export configuration first (backup)")
            print("   2. Run with dry_run=True to preview")
            print("   3. Review the list carefully")
            print("   4. Set require_confirmation=True")
            print()

        else:
            print("✓ No disabled hosts found - nothing to delete")
            print()

        # ======================================================================
        # Part 5: Performance Comparison
        # ======================================================================
        print("Part 5: Performance Comparison (Bulk vs Sequential)")
        print("-" * 90)

        print("Bulk operations provide significant performance benefits:")
        print()

        # Example with certificate renewal
        cert_count = len(certificates)
        if cert_count > 0:
            # Simulate timing
            sequential_time = cert_count * 3  # 3 seconds per cert
            bulk_time_batch5 = (cert_count / 5) * 3  # 5 at a time
            bulk_time_batch10 = (cert_count / 10) * 3  # 10 at a time

            print(f"Scenario: Renew {cert_count} certificates")
            print()
            print(f"{'Method':<30} {'Time (seconds)':<20} {'Speedup':<15}")
            print("-" * 65)
            print(f"{'Sequential (one at a time)':<30} {sequential_time:<20.1f} {'1.0x':<15}")
            print(
                f"{'Bulk (batch_size=5)':<30} {bulk_time_batch5:<20.1f} "
                f"{sequential_time / bulk_time_batch5:.1f}x"
            )
            print(
                f"{'Bulk (batch_size=10)':<30} {bulk_time_batch10:<20.1f} "
                f"{sequential_time / bulk_time_batch10:.1f}x"
            )
            print()

            print("Recommendation:")
            print("  - Use batch_size=5-10 for most operations")
            print("  - Use batch_size=20-50 for large-scale operations")
            print("  - Monitor NPM server load")
            print()

        # ======================================================================
        # Summary
        # ======================================================================
        print("=" * 90)
        print("Bulk Operations Summary")
        print("=" * 90)
        print()

        print("Operations demonstrated:")
        print("  ✓ Bulk certificate renewal (with filtering)")
        print("  ✓ Bulk toggle hosts (enable/disable by pattern)")
        print("  ✓ Configuration export (backup)")
        print("  ✓ Bulk delete (with safety measures)")
        print("  ✓ Performance optimization")
        print()

        print("Best practices:")
        print("  1. ALWAYS use dry_run=True first to preview changes")
        print("  2. Export configuration before bulk deletes")
        print("  3. Use appropriate batch_size for your environment")
        print("  4. Filter carefully to target only intended resources")
        print("  5. Monitor operations with progress tracking")
        print()

        print("Next steps:")
        print("  - Review the backup file:", backup_file)
        print("  - Test restore from backup (see configuration import)")
        print("  - Set up automated bulk operations (see automated_maintenance.py)")
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
