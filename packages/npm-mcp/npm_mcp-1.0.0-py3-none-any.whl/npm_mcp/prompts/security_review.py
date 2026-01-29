"""Security review prompts for NPM MCP Server.

Provides guided workflows for:
- Security auditing of access lists and configurations
- Setting up IP-based access controls
"""

from typing import Any

from mcp.server.fastmcp import FastMCP


def register_security_prompts(mcp: FastMCP[Any]) -> None:
    """Register security-related prompts with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.prompt(
        name="npm_security_audit",
        description="Review access lists and check for security misconfigurations",
    )
    def security_audit_prompt(
        instance_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for security auditing.

        Args:
            instance_name: Optional instance name to audit.

        Returns:
            List of prompt messages guiding the security audit process.
        """
        instance_text = f' on instance "{instance_name}"' if instance_name else ""
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me perform a security audit{instance_text}.

Steps to follow:

1. **Review Access Lists**
   Use npm_list_access_lists to get all configured access lists
   Check for:
   - Empty access lists (no rules defined)
   - Access lists allowing "all" without authentication
   - Unused access lists

2. **Review Proxy Hosts Security**
   Use npm_list_proxy_hosts to get all proxy hosts
   For each proxy host, check:
   - block_exploits is enabled
   - SSL is properly configured (force_ssl=true when certificate is present)
   - Access list is applied if needed
   - HSTS is enabled for sensitive domains

3. **Review Certificate Status**
   Use npm_list_certificates with expiring_soon=true
   Flag any certificates that:
   - Are expired or expiring within 7 days
   - Use weak encryption (if detectable)

4. **Review System Settings**
   Use npm_get_system_settings
   Check for:
   - Default Let's Encrypt email configured
   - Any security-related settings

5. **Summary Report**
   Provide a summary with:
   - Critical issues (immediate action required)
   - Warnings (should be addressed soon)
   - Recommendations (best practices)

Please proceed with these steps.""",
                },
            }
        ]

    @mcp.prompt(
        name="access_list_setup",
        description="Guide creating IP-based access controls",
    )
    def access_list_setup_prompt(
        name: str,
        allowed_ips: str,
        require_auth: str = "false",
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for setting up access lists.

        Args:
            name: Name for the access list.
            allowed_ips: Comma-separated list of allowed IPs/CIDRs.
            require_auth: Whether to require HTTP Basic Auth (default: false).

        Returns:
            List of prompt messages guiding the access list setup.
        """
        ip_list = [ip.strip() for ip in allowed_ips.split(",")]
        ip_rules = ", ".join([f'{{"directive": "allow", "address": "{ip}"}}' for ip in ip_list])

        auth_section = ""
        if require_auth.lower() == "true":
            auth_section = """

4. **Add HTTP Basic Auth users** (since require_auth=true)
   Use npm_manage_access_list with operation="update" to add clients:
   - list_id: <id from step 2>
   - clients: [{{"username": "user1", "password": "secure_password"}}]
   Note: Use strong passwords and consider using a password manager"""

        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me set up an access list named "{name}" \
to restrict access to specific IPs.

Steps to follow:

1. **Create the access list**
   Use npm_manage_access_list with:
   - operation: "create"
   - name: "{name}"
   - satisfy_any: false (require ALL conditions to match)
   - items: [{ip_rules}, {{"directive": "deny", "address": "all"}}]

2. **Verify the access list was created**
   Use npm_list_access_lists to confirm the new list exists

3. **Apply to proxy hosts**
   For each proxy host that should be protected:
   Use npm_manage_proxy_host with:
   - operation: "update"
   - host_id: <target host id>
   - access_list_id: <id from step 1>{auth_section}

5. **Test the configuration**
   - Try accessing protected hosts from an allowed IP (should work)
   - Try accessing from a non-allowed IP (should be blocked)

Please proceed with these steps.""",
                },
            }
        ]
