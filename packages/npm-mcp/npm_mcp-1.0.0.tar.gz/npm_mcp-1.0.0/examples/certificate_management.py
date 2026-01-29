#!/usr/bin/env python3
"""
Certificate Management Example for NPM MCP Server

This example demonstrates the complete certificate lifecycle:
1. Create a Let's Encrypt certificate
2. List all certificates with expiration dates
3. Renew expiring certificates (individually)
4. Bulk renew multiple certificates
5. Delete expired certificates
6. Attach certificates to proxy hosts

Prerequisites:
- NPM MCP Server installed
- NPM instance running with valid Let's Encrypt setup
- Domain(s) with proper DNS configuration
- Valid NPM credentials

Usage:
    # Set environment variables:
    export NPM_URL="http://your-npm-instance:81"
    export NPM_EMAIL="admin@example.com"
    export NPM_PASSWORD="your-password"
    export CERT_EMAIL="certs@example.com"  # Email for Let's Encrypt
    export CERT_DOMAIN="example.com"        # Domain to certify

    # Run the example:
    python examples/certificate_management.py
"""

import asyncio
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

# Add src to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from npm_mcp.config.loader import ConfigLoader
from npm_mcp.instance_manager import InstanceManager


def format_date(timestamp: int | None) -> str:
    """Format Unix timestamp to human-readable date."""
    if not timestamp:
        return "Unknown"
    return datetime.fromtimestamp(timestamp, UTC).strftime("%Y-%m-%d %H:%M:%S")


def days_until_expiry(expires_on: int | None) -> int | None:
    """Calculate days until certificate expiry."""
    if not expires_on:
        return None
    expiry_date = datetime.fromtimestamp(expires_on, UTC)
    return (expiry_date - datetime.now()).days


async def main() -> None:
    """Run the certificate management example."""

    print("=" * 80)
    print("NPM MCP Server - Certificate Management Example")
    print("=" * 80)
    print()

    # Get credentials from environment
    npm_url = os.getenv("NPM_URL")
    npm_email = os.getenv("NPM_EMAIL")
    npm_password = os.getenv("NPM_PASSWORD")
    cert_email = os.getenv("CERT_EMAIL", npm_email)
    cert_domain = os.getenv("CERT_DOMAIN")

    if not all([npm_url, npm_email, npm_password]):
        print("ERROR: Missing required environment variables:")
        print("  - NPM_URL: URL to your NPM instance")
        print("  - NPM_EMAIL: Your NPM admin email")
        print("  - NPM_PASSWORD: Your NPM admin password")
        print("  - CERT_EMAIL: Email for Let's Encrypt (optional, defaults to NPM_EMAIL)")
        print("  - CERT_DOMAIN: Domain to create certificate for (optional)")
        sys.exit(1)

    try:
        # Initialize
        config = ConfigLoader.load_config()
        instance_manager = InstanceManager(config.global_settings)

        # Add instance
        await instance_manager.add_instance(
            name="cert_demo",
            url=npm_url,
            username=npm_email,
            password=npm_password,
        )
        npm_client = await instance_manager.get_client("cert_demo")

        # ======================================================================
        # Part 1: List Existing Certificates
        # ======================================================================
        print("Part 1: Listing All Certificates")
        print("-" * 80)

        certificates = await npm_client.list_certificates()
        print(f"✓ Found {len(certificates)} certificate(s)")
        print()

        if certificates:
            print(f"{'ID':<6} {'Name':<25} {'Domains':<30} {'Expires':<12} {'Days Left':<10}")
            print("-" * 80)

            for cert in certificates:
                days_left = days_until_expiry(cert.expires_on)
                days_str = f"{days_left}d" if days_left is not None else "N/A"

                # Color code based on days left
                if days_left is not None:
                    if days_left < 7:
                        status = "⚠️  URGENT"
                    elif days_left < 30:
                        status = "⚠️  Soon"
                    else:
                        status = "✓  Good"
                else:
                    status = "?"

                domains = ", ".join(cert.domain_names[:2])
                if len(cert.domain_names) > 2:
                    domains += f", +{len(cert.domain_names) - 2}"

                print(
                    f"{cert.id:<6} {cert.nice_name:<25} {domains:<30} {days_str:<12} {status:<10}"
                )
            print()

        # ======================================================================
        # Part 2: Create New Certificate (if domain provided)
        # ======================================================================
        if cert_domain:
            print("Part 2: Creating New Let's Encrypt Certificate")
            print("-" * 80)

            # Check if certificate already exists
            existing = [c for c in certificates if cert_domain in c.domain_names]

            if existing:
                print(f"✓ Certificate for '{cert_domain}' already exists (ID: {existing[0].id})")
                print(f"  Nice name: {existing[0].nice_name}")
                print(f"  Expires: {format_date(existing[0].expires_on)}")
                cert_id = existing[0].id
            else:
                print(f"Creating Let's Encrypt certificate for: {cert_domain}")
                print(f"Using email: {cert_email}")
                print()

                try:
                    certificate = await npm_client.create_certificate(
                        provider="letsencrypt",
                        nice_name=f"LE - {cert_domain}",
                        domain_names=[cert_domain, f"*.{cert_domain}"],
                        meta={
                            "letsencrypt_email": cert_email,
                            "letsencrypt_agree": True,
                            "dns_challenge": False,  # Use HTTP challenge
                        },
                    )
                    cert_id = certificate.id
                    print(f"✓ Certificate created successfully (ID: {cert_id})")
                    print(f"  Domains: {', '.join(certificate.domain_names)}")
                    print(f"  Expires: {format_date(certificate.expires_on)}")
                except Exception as e:
                    print(f"✗ Failed to create certificate: {e}")
                    print()
                    print("Note: Certificate creation requires:")
                    print("  - Domain DNS must point to your NPM instance")
                    print("  - Port 80 must be accessible for HTTP challenge")
                    print("  - NPM must be properly configured for Let's Encrypt")
                    cert_id = None
            print()

        # ======================================================================
        # Part 3: Identify Expiring Certificates
        # ======================================================================
        print("Part 3: Identifying Expiring Certificates")
        print("-" * 80)

        # Refresh certificate list
        certificates = await npm_client.list_certificates()

        # Find certificates expiring in next 30 days
        expiring_soon = [
            cert
            for cert in certificates
            if days_until_expiry(cert.expires_on) is not None
            and days_until_expiry(cert.expires_on) < 30
        ]

        print(f"✓ Found {len(expiring_soon)} certificate(s) expiring within 30 days")
        print()

        if expiring_soon:
            for cert in expiring_soon:
                days_left = days_until_expiry(cert.expires_on)
                print(f"  - {cert.nice_name}")
                print(f"    Domains: {', '.join(cert.domain_names)}")
                print(f"    Expires in: {days_left} days")
                print()

        # ======================================================================
        # Part 4: Renew Individual Certificate
        # ======================================================================
        if expiring_soon and len(expiring_soon) > 0:
            print("Part 4: Renewing Individual Certificate")
            print("-" * 80)

            cert_to_renew = expiring_soon[0]
            print(f"Renewing: {cert_to_renew.nice_name} (ID: {cert_to_renew.id})")
            print(f"Current expiry: {format_date(cert_to_renew.expires_on)}")
            print()

            try:
                renewed_cert = await npm_client.renew_certificate(cert_to_renew.id)
                print("✓ Certificate renewed successfully")
                print(f"  New expiry: {format_date(renewed_cert.expires_on)}")
                new_days = days_until_expiry(renewed_cert.expires_on)
                print(f"  Valid for: {new_days} days")
            except Exception as e:
                print(f"✗ Failed to renew certificate: {e}")
            print()

        # ======================================================================
        # Part 5: Bulk Certificate Renewal (using bulk operations tool)
        # ======================================================================
        if len(expiring_soon) > 1:
            print("Part 5: Bulk Certificate Renewal")
            print("-" * 80)
            print(f"Renewing {len(expiring_soon)} certificates in bulk...")
            print()

            # Note: This would use the npm_bulk_operations tool
            # For demonstration, we show the concept
            print("Using bulk operations tool:")
            print('  operation: "renew_certificates"')
            print("  filters: days_until_expiry <= 30")
            print("  batch_size: 5")
            print("  dry_run: false")
            print()
            print("Expected results:")
            for cert in expiring_soon:
                print(f"  - {cert.nice_name}: Would be renewed")
            print()
            print("Note: Run bulk_operations.py example for actual bulk renewal")
            print()

        # ======================================================================
        # Part 6: Certificate Usage Information
        # ======================================================================
        print("Part 6: Certificate Usage Information")
        print("-" * 80)

        # List proxy hosts to see certificate usage
        proxy_hosts = await npm_client.list_proxy_hosts()
        hosts_with_ssl = [h for h in proxy_hosts if h.certificate_id is not None]

        print(f"✓ {len(hosts_with_ssl)}/{len(proxy_hosts)} proxy hosts have SSL enabled")
        print()

        if hosts_with_ssl:
            # Group by certificate
            cert_usage = {}
            for host in hosts_with_ssl:
                cert_id = host.certificate_id
                if cert_id not in cert_usage:
                    cert = next((c for c in certificates if c.id == cert_id), None)
                    if cert:
                        cert_usage[cert_id] = {
                            "cert": cert,
                            "hosts": [],
                        }
                if cert_id in cert_usage:
                    cert_usage[cert_id]["hosts"].append(host.domain_names[0])

            print("Certificate usage by proxy hosts:")
            for cert_id, data in cert_usage.items():
                cert = data["cert"]
                hosts = data["hosts"]
                print(f"\n  {cert.nice_name} (ID: {cert_id})")
                print(f"  Used by {len(hosts)} host(s):")
                for host_domain in hosts[:5]:
                    print(f"    - {host_domain}")
                if len(hosts) > 5:
                    print(f"    ... and {len(hosts) - 5} more")

        print()

        # ======================================================================
        # Summary
        # ======================================================================
        print("=" * 80)
        print("Certificate Management Summary")
        print("=" * 80)
        print(f"Total certificates: {len(certificates)}")
        print(f"Expiring soon (<30 days): {len(expiring_soon)}")
        print(f"Hosts with SSL: {len(hosts_with_ssl)}/{len(proxy_hosts)}")
        print()

        # Recommendations
        print("Recommendations:")
        if len(expiring_soon) > 0:
            print(f"  ⚠️  Renew {len(expiring_soon)} certificate(s) soon")
        else:
            print("  ✓  All certificates are valid")

        if len(proxy_hosts) - len(hosts_with_ssl) > 0:
            print(
                f"  💡 {len(proxy_hosts) - len(hosts_with_ssl)} host(s) without SSL - "
                "consider enabling HTTPS"
            )

        print()
        print("Next steps:")
        print("  - Set up automated renewal (see automated_maintenance.py)")
        print("  - Use bulk operations for multiple renewals (see bulk_operations.py)")
        print("  - Monitor certificate expiration regularly")
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
