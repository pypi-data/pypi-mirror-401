"""Certificate management prompts for NPM MCP Server.

Provides guided workflows for:
- Auditing certificates for expiration
- Setting up Let's Encrypt certificates
"""

from typing import Any

from mcp.server.fastmcp import FastMCP


def register_certificate_prompts(mcp: FastMCP[Any]) -> None:
    """Register certificate-related prompts with the MCP server.

    Args:
        mcp: FastMCP server instance.
    """

    @mcp.prompt(
        name="certificate_audit",
        description="Audit certificates for expiration and guide renewal",
    )
    def certificate_audit_prompt(
        days_threshold: str = "30",
        instance_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for auditing certificates.

        Args:
            days_threshold: Days threshold for expiring soon (default: 30).
            instance_name: Optional instance name to audit.

        Returns:
            List of prompt messages guiding the audit process.
        """
        instance_text = f' on instance "{instance_name}"' if instance_name else ""
        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me audit SSL certificates{instance_text} \
and identify any that need renewal.

Steps to follow:
1. Use npm_list_certificates with expiring_soon=true and days_threshold={days_threshold}
2. For each certificate expiring soon:
   - Check if it's a Let's Encrypt certificate (can be auto-renewed)
   - Check if it's a custom certificate (needs manual replacement)
3. For Let's Encrypt certificates expiring soon:
   - Use npm_manage_certificate with operation="renew" and cert_id=<id>
   - Or use npm_bulk_operations with operation="renew_certificates" for batch renewal
4. For custom certificates:
   - List the certificates that need manual replacement
   - Provide guidance on updating them with npm_manage_certificate operation="update"
5. Summarize:
   - Total certificates checked
   - Certificates renewed successfully
   - Certificates requiring manual attention

Please proceed with these steps.""",
                },
            }
        ]

    @mcp.prompt(
        name="ssl_setup",
        description="Guide setting up Let's Encrypt SSL certificates",
    )
    def ssl_setup_prompt(
        domain: str,
        email: str,
        use_dns_challenge: str = "false",
        dns_provider: str | None = None,
    ) -> list[dict[str, Any]]:
        """Create a guided workflow for SSL certificate setup.

        Args:
            domain: Domain name for the certificate.
            email: Email address for Let's Encrypt registration.
            use_dns_challenge: Whether to use DNS challenge (default: false).
            dns_provider: DNS provider for DNS challenge (optional).

        Returns:
            List of prompt messages guiding the SSL setup process.
        """
        is_wildcard = domain.startswith("*.")

        if is_wildcard or use_dns_challenge.lower() == "true":
            reason = (
                "this is a wildcard certificate" if is_wildcard else "you requested DNS challenge"
            )
            challenge_text = f"""
Since {reason}, we'll use DNS validation:
- dns_challenge: true
- dns_provider: "{dns_provider or "cloudflare"}" (or your provider)
- You'll need to provide dns_credentials with your API key"""
        else:
            challenge_text = """
Using HTTP validation (default for non-wildcard certificates):
- Ensure the domain points to this NPM instance
- Ensure port 80 is accessible from the internet"""

        return [
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"""Help me set up a Let's Encrypt SSL certificate for {domain}.

Steps to follow:
1. First, validate the certificate configuration:
   Use npm_validate_certificate with:
   - provider: "letsencrypt"
   - domain_names: ["{domain}"]
   - letsencrypt_email: "{email}"

2. If validation passes, create the certificate:
   Use npm_manage_certificate with:
   - operation: "create"
   - provider: "letsencrypt"
   - nice_name: "{domain} SSL"
   - domain_names: ["{domain}"]
   - letsencrypt_email: "{email}"
   - letsencrypt_agree_tos: true
{challenge_text}

3. Verify the certificate was created:
   Use npm_list_certificates with domain_filter="{domain}"

4. The certificate can now be attached to proxy hosts using its certificate_id.

Please proceed with these steps.""",
                },
            }
        ]
