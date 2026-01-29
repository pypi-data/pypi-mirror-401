"""Bulk operations prompts for NPM MCP Server.

Provides guided workflows for:
- Exporting full NPM configuration
- Importing configuration to a new instance
"""

from typing import Any

from mcp.server.fastmcp import FastMCP


def register_bulk_prompts(mcp: FastMCP[Any]) -> None:
    """Register bulk operation prompts with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.prompt(
        name="bulk_export",
        description="Guide exporting full NPM configuration for backup or migration",
    )
    def bulk_export_prompt(
        instance_name: str | None = None,
        format: str = "json",
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for exporting NPM configuration.

        Args:
            instance_name: Optional instance name to export from.
            format: Export format - json or yaml (default: json).

        Returns:
            List of prompt messages guiding the export process.
        """
        instance_text = f' from instance "{instance_name}"' if instance_name else ""
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me export the full NPM configuration{instance_text} \
for backup or migration.

Steps to follow:

1. **Preview what will be exported**
   First, let's see what resources exist:
   - Use npm_list_proxy_hosts to count proxy hosts
   - Use npm_list_certificates to count certificates
   - Use npm_list_access_lists to count access lists
   - Use npm_list_streams to count TCP/UDP streams
   - Use npm_list_redirections to count redirections
   - Use npm_list_dead_hosts to count dead hosts

2. **Export the configuration**
   Use npm_bulk_operations with:
   - operation: "export_config"
   - resource_types: ["all"] or specify individual types:
     ["proxy_hosts", "certificates", "access_lists",
      "streams", "redirections", "dead_hosts"]
   - format: "{format}"
   {f'- instance_name: "{instance_name}"' if instance_name else ""}

3. **Review the exported data**
   The export will include:
   - All proxy host configurations
   - Certificate metadata (not private keys for custom certs)
   - Access list rules and clients
   - Stream configurations
   - Redirection rules
   - Dead host entries

4. **Save the configuration**
   The exported {format.upper()} can be:
   - Stored as a backup
   - Used for migration to another instance
   - Version controlled in git
   - Used to recreate the configuration

Note: Custom certificate private keys are NOT exported for security.
You'll need to re-upload custom certificates after import.

Please proceed with these steps.""",
                },
            }
        ]

    @mcp.prompt(
        name="bulk_import",
        description="Guide importing configuration to a new NPM instance",
    )
    def bulk_import_prompt(
        instance_name: str | None = None,
        strategy: str = "merge",
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for importing NPM configuration.

        Args:
            instance_name: Optional target instance name.
            strategy: Import strategy - merge or replace (default: merge).

        Returns:
            List of prompt messages guiding the import process.
        """
        instance_text = f' to instance "{instance_name}"' if instance_name else ""
        strategy_explanation = (
            "merge existing configurations (add new, update matching)"
            if strategy == "merge"
            else "replace existing configurations (delete all, then import)"
        )
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me import NPM configuration{instance_text}.

Import Strategy: {strategy} - {strategy_explanation}

Steps to follow:

1. **Prepare the configuration data**
   You should have configuration data from a previous export in JSON or YAML format.
   Provide the configuration data for import.

2. **Preview the import (dry run)**
   Use npm_bulk_operations with:
   - operation: "import_config"
   - import_data: <your configuration dict>
   - strategy: "{strategy}"
   - dry_run: true
   {f'- instance_name: "{instance_name}"' if instance_name else ""}

   Review what will be created/updated/skipped.

3. **Execute the import**
   If the dry run looks correct, run again without dry_run:
   Use npm_bulk_operations with:
   - operation: "import_config"
   - import_data: <your configuration dict>
   - strategy: "{strategy}"
   - dry_run: false
   - continue_on_error: true (to import as much as possible)
   {f'- instance_name: "{instance_name}"' if instance_name else ""}

4. **Verify the import**
   - Use npm_list_proxy_hosts to verify proxy hosts
   - Use npm_list_certificates to verify certificates
   - Use npm_list_access_lists to verify access lists

5. **Post-import tasks**
   - Re-issue Let's Encrypt certificates (they may need HTTP validation on new instance)
   - Re-upload custom certificate private keys
   - Test critical proxy hosts
   - Update DNS if instance IP has changed

Please provide your configuration data and proceed with these steps.""",
                },
            }
        ]
