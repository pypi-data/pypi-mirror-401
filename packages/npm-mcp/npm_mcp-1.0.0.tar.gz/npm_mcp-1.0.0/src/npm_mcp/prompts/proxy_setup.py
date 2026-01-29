"""Proxy setup prompts for NPM MCP Server.

Provides guided workflows for:
- Creating new proxy hosts with SSL certificates
- Migrating proxy configurations between instances
"""

from typing import Any

from mcp.server.fastmcp import FastMCP


def register_proxy_prompts(mcp: FastMCP[Any]) -> None:
    """Register proxy-related prompts with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.prompt(
        name="setup_proxy",
        description="Guide creating a new proxy host with SSL certificate",
    )
    def setup_proxy_prompt(
        domain: str,
        backend_host: str,
        backend_port: str = "80",
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for setting up a proxy host.

        Args:
            domain: The domain name for the proxy host.
            backend_host: The backend server hostname or IP.
            backend_port: The backend server port (default: 80).

        Returns:
            List of prompt messages guiding the setup process.
        """
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me set up a proxy host for {domain}.

Steps to follow:
1. First, use npm_list_certificates to check for existing certificates for {domain}
2. If no certificate exists, use npm_manage_certificate to create a Let's Encrypt certificate:
   - operation: "create"
   - provider: "letsencrypt"
   - domain_names: ["{domain}"]
   - nice_name: "{domain} SSL"
   - letsencrypt_agree_tos: true
3. Use npm_manage_proxy_host to create the proxy:
   - operation: "create"
   - domain_names: ["{domain}"]
   - forward_scheme: "http"
   - forward_host: "{backend_host}"
   - forward_port: {backend_port}
   - certificate_id: (from step 2)
   - force_ssl: true
   - websocket_support: true
   - block_exploits: true
4. Verify the setup with npm_get_proxy_host

Please proceed with these steps.""",
                },
            }
        ]

    @mcp.prompt(
        name="migrate_proxy",
        description="Guide migrating proxy configurations between NPM instances",
    )
    def migrate_proxy_prompt(
        source_instance: str,
        target_instance: str,
        domain_pattern: str | None = None,
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for migrating proxy configs.

        Args:
            source_instance: Name of the source NPM instance.
            target_instance: Name of the target NPM instance.
            domain_pattern: Optional pattern to filter domains to migrate.

        Returns:
            List of prompt messages guiding the migration process.
        """
        filter_text = f' matching "{domain_pattern}"' if domain_pattern else ""
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me migrate proxy configurations \
from {source_instance} to {target_instance}{filter_text}.

Steps to follow:
1. Use npm_list_proxy_hosts on instance "{source_instance}" to get all proxy hosts{filter_text}
2. Use npm_bulk_operations with operation="export_config" on "{source_instance}" to export:
   - resource_types: ["proxy_hosts", "certificates"]
   - format: "json"
3. Review the exported configuration for any instance-specific settings that need adjustment
4. Use npm_bulk_operations with operation="import_config" on "{target_instance}" to import:
   - strategy: "merge" (to preserve existing configs) or "replace" (to overwrite)
5. Use npm_list_proxy_hosts on "{target_instance}" to verify the migration
6. Test a few key proxy hosts to ensure they're working correctly

Note: Certificates may need to be re-issued on the target instance if they use HTTP validation.

Please proceed with these steps.""",
                },
            }
        ]
