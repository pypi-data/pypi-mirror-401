#!/usr/bin/env python3
"""
Automated Maintenance Example for NPM MCP Server

This example demonstrates automated maintenance tasks:
1. Scheduled certificate renewal (cron-like)
2. Weekly configuration backup
3. Host health monitoring
4. Alerting on failures
5. Automated cleanup of old resources
6. Report generation

Prerequisites:
- NPM MCP Server installed
- NPM instance with resources configured
- Valid NPM credentials
- Optional: SMTP server for email alerts

Usage:
    # Set environment variables:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"
    export SMTP_HOST="smtp.gmail.com"  # Optional
    export SMTP_PORT="587"              # Optional
    export ALERT_EMAIL="alerts@example.com"  # Optional

    # Run once:
    python examples/automated_maintenance.py --once

    # Run as daemon (continuous monitoring):
    python examples/automated_maintenance.py --daemon

    # Or use as a cron job:
    # 0 2 * * * cd /path/to/npm_mcp && python examples/automated_maintenance.py --once
"""

import argparse
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager


class MaintenanceTask:
    """Base class for maintenance tasks."""

    def __init__(self, name: str, schedule: str) -> None:
        self.name = name
        self.schedule = schedule
        self.last_run: datetime | None = None

    async def run(self) -> dict:
        """Execute the task and return results."""
        raise NotImplementedError


class CertificateRenewalTask(MaintenanceTask):
    """Automatically renew expiring certificates."""

    def __init__(self, npm_client, days_threshold: int = 30) -> None:
        super().__init__("Certificate Renewal", "daily")
        self.npm_client = npm_client
        self.days_threshold = days_threshold

    async def run(self) -> dict:
        """Check and renew expiring certificates."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running: {self.name}")

        try:
            # Get all certificates
            certificates = await self.npm_client.list_certificates()

            # Find expiring certificates
            now_ts = int(datetime.now().timestamp())
            threshold_ts = int((datetime.now() + timedelta(days=self.days_threshold)).timestamp())

            expiring = [
                cert
                for cert in certificates
                if cert.expires_on and now_ts < cert.expires_on <= threshold_ts
            ]

            results = {
                "success": True,
                "total_certs": len(certificates),
                "expiring_certs": len(expiring),
                "renewed": [],
                "failed": [],
            }

            # Renew each expiring certificate
            for cert in expiring:
                try:
                    print(f"  Renewing: {cert.nice_name} (ID: {cert.id})")
                    renewed = await self.npm_client.renew_certificate(cert.id)
                    results["renewed"].append(
                        {"id": cert.id, "name": cert.nice_name, "new_expiry": renewed.expires_on}
                    )
                    print("    ✓ Renewed successfully")
                except Exception as e:
                    print(f"    ✗ Failed: {e}")
                    results["failed"].append(
                        {"id": cert.id, "name": cert.nice_name, "error": str(e)}
                    )

            self.last_run = datetime.now()
            print(
                f"  Summary: {len(results['renewed'])} renewed, {len(results['failed'])} failed\n"
            )

            return results

        except Exception as e:
            print(f"  ✗ Task failed: {e}\n")
            return {"success": False, "error": str(e)}


class BackupTask(MaintenanceTask):
    """Backup NPM configuration."""

    def __init__(self, npm_client, backup_dir: Path) -> None:
        super().__init__("Configuration Backup", "weekly")
        self.npm_client = npm_client
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(exist_ok=True)

    async def run(self) -> dict:
        """Create configuration backup."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running: {self.name}")

        try:
            # Get all resources
            proxy_hosts = await self.npm_client.list_proxy_hosts()
            certificates = await self.npm_client.list_certificates()
            access_lists = await self.npm_client.list_access_lists()
            streams = await self.npm_client.list_streams()

            # Create backup data
            backup_data = {
                "backup_date": datetime.now().isoformat(),
                "resources": {
                    "proxy_hosts": [host.model_dump() for host in proxy_hosts],
                    "certificates": [cert.model_dump() for cert in certificates],
                    "access_lists": [alist.model_dump() for alist in access_lists],
                    "streams": [stream.model_dump() for stream in streams],
                },
                "counts": {
                    "proxy_hosts": len(proxy_hosts),
                    "certificates": len(certificates),
                    "access_lists": len(access_lists),
                    "streams": len(streams),
                },
            }

            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"npm_backup_{timestamp}.json"

            backup_file.write_text(json.dumps(backup_data, indent=2))
            file_size = backup_file.stat().st_size

            # Clean up old backups (keep last 30)
            all_backups = sorted(self.backup_dir.glob("npm_backup_*.json"))
            if len(all_backups) > 30:
                for old_backup in all_backups[:-30]:
                    old_backup.unlink()
                    print(f"  Deleted old backup: {old_backup.name}")

            self.last_run = datetime.now()

            results = {
                "success": True,
                "file": str(backup_file),
                "size": file_size,
                "resources": backup_data["counts"],
            }

            print(f"  ✓ Backup created: {backup_file.name}")
            print(f"  Size: {file_size:,} bytes")
            print(f"  Resources: {sum(backup_data['counts'].values())} total\n")

            return results

        except Exception as e:
            print(f"  ✗ Task failed: {e}\n")
            return {"success": False, "error": str(e)}


class HealthCheckTask(MaintenanceTask):
    """Monitor NPM instance health."""

    def __init__(self, npm_client) -> None:
        super().__init__("Health Check", "hourly")
        self.npm_client = npm_client

    async def run(self) -> dict:
        """Check NPM instance health."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running: {self.name}")

        try:
            start_time = datetime.now()

            # Test basic connectivity
            proxy_hosts = await self.npm_client.list_proxy_hosts()

            response_time = (datetime.now() - start_time).total_seconds()

            # Check for issues
            issues = []

            # Check for disabled hosts
            disabled_count = sum(1 for h in proxy_hosts if not h.enabled)
            if disabled_count > 0:
                issues.append(f"{disabled_count} disabled hosts")

            # Check for hosts without SSL
            no_ssl_count = sum(1 for h in proxy_hosts if h.certificate_id is None and h.enabled)
            if no_ssl_count > 0:
                issues.append(f"{no_ssl_count} enabled hosts without SSL")

            self.last_run = datetime.now()

            results = {
                "success": True,
                "response_time": response_time,
                "proxy_hosts": len(proxy_hosts),
                "issues": issues,
                "healthy": len(issues) == 0,
            }

            if results["healthy"]:
                print("  ✓ Instance healthy")
            else:
                print("  ⚠️  Issues found:")
                for issue in issues:
                    print(f"    - {issue}")

            print(f"  Response time: {response_time:.3f}s\n")

            return results

        except Exception as e:
            print(f"  ✗ Health check failed: {e}\n")
            return {"success": False, "error": str(e), "healthy": False}


class CleanupTask(MaintenanceTask):
    """Clean up old or unused resources."""

    def __init__(self, npm_client) -> None:
        super().__init__("Resource Cleanup", "weekly")
        self.npm_client = npm_client

    async def run(self) -> dict:
        """Clean up unused resources."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running: {self.name}")

        try:
            # Get all resources
            proxy_hosts = await self.npm_client.list_proxy_hosts()
            certificates = await self.npm_client.list_certificates()

            # Find unused certificates
            cert_ids_in_use = {h.certificate_id for h in proxy_hosts if h.certificate_id}
            unused_certs = [c for c in certificates if c.id not in cert_ids_in_use]

            # Find expired certificates
            now_ts = int(datetime.now().timestamp())
            expired_certs = [c for c in unused_certs if c.expires_on and c.expires_on < now_ts]

            results = {
                "success": True,
                "unused_certs": len(unused_certs),
                "expired_certs": len(expired_certs),
                "deleted": [],
            }

            # Delete expired, unused certificates (dry run for safety)
            for cert in expired_certs[:5]:  # Limit to 5 for safety
                print(f"  Would delete expired cert: {cert.nice_name} (ID: {cert.id})")
                # await self.npm_client.delete_certificate(cert.id)  # Uncomment to actually delete
                results["deleted"].append({"id": cert.id, "name": cert.nice_name})

            self.last_run = datetime.now()

            print(f"  Summary: {len(unused_certs)} unused, {len(expired_certs)} expired")
            print("  Note: Cleanup is in DRY RUN mode by default\n")

            return results

        except Exception as e:
            print(f"  ✗ Task failed: {e}\n")
            return {"success": False, "error": str(e)}


async def send_alert(subject: str, message: str) -> None:
    """Send alert email (placeholder)."""
    print(f"\n📧 ALERT: {subject}")
    print(f"   {message}\n")

    # TODO: Implement actual email sending with SMTP
    # smtp_host = os.getenv("SMTP_HOST")
    # if smtp_host:
    #     # Send email using smtplib
    #     pass


async def run_maintenance_cycle(instance_manager, instance_name: str) -> None:
    """Run one complete maintenance cycle."""
    print("=" * 90)
    print(f"NPM Maintenance Cycle - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 90)
    print()

    try:
        # Get NPM client
        npm_client = await instance_manager.get_client(instance_name)

        # Define backup directory
        backup_dir = Path("backups")

        # Create tasks
        tasks = [
            HealthCheckTask(npm_client),
            CertificateRenewalTask(npm_client, days_threshold=30),
            BackupTask(npm_client, backup_dir),
            CleanupTask(npm_client),
        ]

        # Run each task
        all_results = {}
        for task in tasks:
            results = await task.run()
            all_results[task.name] = results

            # Send alert on failure
            if not results.get("success", False):
                await send_alert(
                    f"Task Failed: {task.name}", f"Error: {results.get('error', 'Unknown')}"
                )

            # Send alert on health issues
            if task.name == "Health Check" and not results.get("healthy", True):
                issues = results.get("issues", [])
                await send_alert("Health Issues Detected", "\n".join(f"- {i}" for i in issues))

        # Summary
        print("=" * 90)
        print("Maintenance Cycle Summary")
        print("=" * 90)
        print()

        for task_name, results in all_results.items():
            status = "✓" if results.get("success", False) else "✗"
            print(f"{status} {task_name}")

        print()

    except Exception as e:
        print(f"ERROR: Maintenance cycle failed: {e}")
        import traceback

        traceback.print_exc()


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="NPM Automated Maintenance")
    parser.add_argument("--once", action="store_true", help="Run once and exit (for cron jobs)")
    parser.add_argument("--daemon", action="store_true", help="Run continuously as a daemon")
    parser.add_argument(
        "--interval", type=int, default=3600, help="Interval in seconds (default: 3600)"
    )

    args = parser.parse_args()

    # Get credentials
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables")
        print("  - NPM_URL")
        print("  - NPM_EMAIL")
        print("  - NPM_PASSWORD")
        sys.exit(1)

    try:
        # Initialize
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        await instance_manager.add_instance(
            name="maintenance",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )

        if args.daemon:
            # Run continuously
            print("Starting maintenance daemon...")
            print(f"Interval: {args.interval} seconds")
            print("Press Ctrl+C to stop")
            print()

            while True:
                await run_maintenance_cycle(instance_manager, "maintenance")

                print(f"Sleeping for {args.interval} seconds...")
                print()
                await asyncio.sleep(args.interval)

        else:
            # Run once
            await run_maintenance_cycle(instance_manager, "maintenance")

    except KeyboardInterrupt:
        print("\nMaintenance daemon stopped by user")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await instance_manager.close_all()


if __name__ == "__main__":
    asyncio.run(main())
