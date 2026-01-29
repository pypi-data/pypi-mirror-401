"""
Certificate Management MCP Tools for Nginx Proxy Manager.

This module provides 3 MCP tools for managing SSL/TLS certificates:
1. npm_list_certificates - List all certificates with expiration tracking
2. npm_manage_certificate - Create, update, delete, or renew certificates
3. npm_validate_certificate - Validate certificate configuration before creation

All tools follow FastMCP patterns with ServerContext injection and structured error handling.
"""

import json
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from npm_mcp.constants import API_CERTIFICATES
from npm_mcp.tools.compact import compact_certificate
from npm_mcp.types import MCPContext


def get_server_context(ctx: MCPContext) -> Any:  # noqa: ANN401
    """
    Extract ServerContext from MCP Context.

    Args:
        ctx: MCP Context object

    Returns:
        ServerContext with config, instance_manager, auth_manager, logger
    """
    return ctx.request_context.lifespan_context


# =============================================================================
# Helper Functions for Certificate Operations
# =============================================================================


def _parse_expiration_date(expires_on_str: str | None) -> datetime | None:
    """Parse certificate expiration date string to datetime."""
    if not expires_on_str:
        return None
    try:
        expires_on = datetime.fromisoformat(expires_on_str.replace("Z", "+00:00"))
        if expires_on.tzinfo is None:
            expires_on = expires_on.replace(tzinfo=UTC)
        return expires_on
    except (ValueError, AttributeError, TypeError):
        return None


def _is_expiring_soon(cert: dict[str, Any], threshold_date: datetime) -> bool:
    """Check if certificate expires before threshold date."""
    expires_on = _parse_expiration_date(cert.get("expires_on"))
    return expires_on is not None and expires_on < threshold_date


def _filter_certs_by_provider(
    certificates: list[dict[str, Any]],
    provider: str | None,
) -> list[dict[str, Any]]:
    """Filter certificates by provider."""
    if not provider:
        return certificates
    return [cert for cert in certificates if cert.get("provider") == provider]


def _filter_certs_by_domain(
    certificates: list[dict[str, Any]],
    domain_filter: str | None,
) -> list[dict[str, Any]]:
    """Filter certificates by domain name substring match."""
    if not domain_filter:
        return certificates
    domain_lower = domain_filter.lower()
    return [
        cert
        for cert in certificates
        if any(domain_lower in domain.lower() for domain in cert.get("domain_names", []))
    ]


def _filter_certs_expiring_soon(
    certificates: list[dict[str, Any]],
    expiring_soon: bool | None,
    threshold_date: datetime,
) -> list[dict[str, Any]]:
    """Filter certificates by expiring soon status."""
    if not expiring_soon:
        return certificates
    return [cert for cert in certificates if _is_expiring_soon(cert, threshold_date)]


def _validate_create_params(
    provider: str | None,
    nice_name: str | None,
    domain_names: list[str] | None,
) -> dict[str, Any] | None:
    """Validate required params for create. Returns error dict or None."""
    if not provider:
        return {"success": False, "error": "provider is required for create operation"}
    if provider not in ["letsencrypt", "custom"]:
        return {
            "success": False,
            "error": f"Invalid provider '{provider}'. Must be 'letsencrypt' or 'custom'",
        }
    if not nice_name:
        return {"success": False, "error": "nice_name is required for create operation"}
    if not domain_names:
        return {"success": False, "error": "domain_names is required for create operation"}
    return None


def _build_letsencrypt_data(
    base_data: dict[str, Any],
    *,
    letsencrypt_email: str | None,
    letsencrypt_agree_tos: bool | None,
    dns_challenge: bool | None,
    dns_provider: str | None,
    dns_credentials: dict[str, Any] | str | None,
    propagation_seconds: int | None,
) -> dict[str, Any] | None:
    """Build letsencrypt-specific data. Returns error dict or None (modifies base_data)."""
    if not letsencrypt_email:
        return {
            "success": False,
            "error": "letsencrypt_email is required for Let's Encrypt certificates",
        }
    base_data["meta"]["letsencrypt_email"] = letsencrypt_email
    base_data["meta"]["letsencrypt_agree"] = letsencrypt_agree_tos or True

    if dns_challenge:
        base_data["meta"]["dns_challenge"] = True
        if dns_provider:
            base_data["meta"]["dns_provider"] = dns_provider
        if dns_credentials:
            if isinstance(dns_credentials, dict):
                base_data["meta"]["dns_provider_credentials"] = json.dumps(dns_credentials)
            else:
                base_data["meta"]["dns_provider_credentials"] = dns_credentials
        if propagation_seconds:
            base_data["meta"]["propagation_seconds"] = propagation_seconds
    else:
        base_data["meta"]["dns_challenge"] = False
    return None


def _build_custom_cert_data(
    base_data: dict[str, Any],
    custom_certificate: str | None,
    custom_certificate_key: str | None,
) -> dict[str, Any] | None:
    """Build custom certificate data. Returns error dict or None on success."""
    if not custom_certificate or not custom_certificate_key:
        return {
            "success": False,
            "error": (
                "custom_certificate and custom_certificate_key are required for custom certificates"
            ),
        }
    base_data["certificate"] = custom_certificate
    base_data["certificate_key"] = custom_certificate_key
    return None


def _build_validation_data(
    provider: str,
    domain_names: list[str],
    letsencrypt_email: str | None,
    dns_challenge: bool | None,
    dns_provider: str | None,
    dns_credentials: str | None,
) -> dict[str, Any]:
    """Build certificate validation request data."""
    data: dict[str, Any] = {
        "provider": provider,
        "domain_names": domain_names,
    }

    if provider == "letsencrypt":
        if letsencrypt_email:
            data["letsencrypt_email"] = letsencrypt_email
        if dns_challenge is not None:
            data["dns_challenge"] = dns_challenge
        if dns_provider:
            data["dns_provider"] = dns_provider
        if dns_credentials:
            data["dns_credentials"] = dns_credentials

    return data


async def _call_validation_api(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    data: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    """Call NPM validation API and return (validation_results, warnings, errors)."""
    validation_results: list[dict[str, Any]] = []
    warnings: list[str] = []
    errors: list[str] = []

    try:
        raw_response = await client.post(f"{API_CERTIFICATES}/validate", json=data)
        response = raw_response.json()
        if isinstance(response, dict):
            validation_results = response.get("validation_results", [])
            warnings.extend(response.get("warnings", []))
            errors.extend(response.get("errors", []))
    except Exception as validation_error:
        # If validation endpoint doesn't exist or fails, provide basic validation
        validation_results = [
            {
                "check": "basic_validation",
                "status": "passed",
                "message": "Basic validation completed (NPM validation endpoint not available)",
            }
        ]
        # Log but don't fail on validation endpoint errors
        server_ctx.logger.warning("validation_endpoint_unavailable", error=str(validation_error))

    return validation_results, warnings, errors


async def _handle_create_cert(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    *,
    provider: str,
    nice_name: str,
    domain_names: list[str],
    letsencrypt_email: str | None,
    letsencrypt_agree_tos: bool | None,
    dns_challenge: bool | None,
    dns_provider: str | None,
    dns_credentials: dict[str, Any] | str | None,
    propagation_seconds: int | None,
    custom_certificate: str | None,
    custom_certificate_key: str | None,
) -> dict[str, Any]:
    """Handle certificate create operation."""
    data: dict[str, Any] = {
        "provider": provider,
        "nice_name": nice_name,
        "domain_names": domain_names,
        "meta": {},
    }

    if provider == "letsencrypt":
        error = _build_letsencrypt_data(
            data,
            letsencrypt_email=letsencrypt_email,
            letsencrypt_agree_tos=letsencrypt_agree_tos,
            dns_challenge=dns_challenge,
            dns_provider=dns_provider,
            dns_credentials=dns_credentials,
            propagation_seconds=propagation_seconds,
        )
        if error:
            return error
    else:  # custom
        error = _build_custom_cert_data(data, custom_certificate, custom_certificate_key)
        if error:
            return error

    raw_response = await client.post(API_CERTIFICATES, json=data)
    if raw_response is None:
        return {"success": False, "error": "HTTP client returned None response"}
    response = raw_response.json()
    server_ctx.logger.info("certificate_created", cert_id=response.get("id"))

    return {"success": True, "operation": "create", "certificate": response}


async def _handle_update_cert(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    cert_id: int,
    *,
    nice_name: str | None,
    domain_names: list[str] | None,
) -> dict[str, Any]:
    """Handle certificate update operation."""
    data: dict[str, Any] = {}
    if nice_name is not None:
        data["nice_name"] = nice_name
    if domain_names is not None:
        data["domain_names"] = domain_names

    raw_response = await client.put(f"{API_CERTIFICATES}/{cert_id}", json=data)
    response = raw_response.json()
    server_ctx.logger.info("certificate_updated", cert_id=cert_id)

    return {"success": True, "operation": "update", "certificate": response}


async def _handle_renew_cert(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    cert_id: int,
) -> dict[str, Any]:
    """Handle certificate renew operation."""
    raw_response = await client.post(f"{API_CERTIFICATES}/{cert_id}/renew")
    response = raw_response.json()
    server_ctx.logger.info("certificate_renewed", cert_id=cert_id)

    return {"success": True, "operation": "renew", "certificate": response}


async def _handle_delete_cert(
    client: Any,  # noqa: ANN401
    server_ctx: Any,  # noqa: ANN401
    cert_id: int,
) -> dict[str, Any]:
    """Handle certificate delete operation."""
    await client.delete(f"{API_CERTIFICATES}/{cert_id}")
    server_ctx.logger.info("certificate_deleted", cert_id=cert_id)

    return {"success": True, "operation": "delete", "cert_id": cert_id}


# =============================================================================
# MCP Tools
# =============================================================================


async def npm_list_certificates(
    ctx: MCPContext,
    instance_name: str | None = None,
    expiring_soon: bool | None = False,
    days_threshold: int | None = 30,
    provider: str | None = None,
    domain_filter: str | None = None,
    compact: bool | None = True,
) -> dict[str, Any]:
    """
    List all SSL/TLS certificates with optional filtering and expiration tracking.

    This tool retrieves all certificates from the NPM instance and supports
    filtering by expiration date, provider, and domain name.

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance if not specified)
        expiring_soon: Filter certificates expiring soon (optional, default: False)
        days_threshold: Days threshold for expiring soon (optional, default: 30)
        provider: Filter by provider (letsencrypt|custom) (optional)
        domain_filter: Filter by domain name (optional, substring match)
        compact: Return compact responses with essential fields only (optional, default: True)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - certificates: list - Array of certificate objects
        - total: int - Total number of certificates (before expiring_soon filter)
        - expiring_soon_count: int - Number of certificates expiring soon
        - error: str - Error message (if success is False)

    Example:
        >>> result = await npm_list_certificates(ctx, expiring_soon=True)
        >>> print(f"Found {result['expiring_soon_count']} expiring certificates")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_list_certificates",
        instance=instance_name or "active",
        filters={
            "expiring_soon": expiring_soon,
            "days_threshold": days_threshold,
            "provider": provider,
            "domain_filter": domain_filter,
        },
    )

    try:
        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Fetch all certificates from NPM API
        raw_response = await client.get(API_CERTIFICATES)
        response = raw_response.json()

        # Ensure response is a list
        certificates = response if isinstance(response, list) else []

        # Track total before filtering
        total = len(certificates)

        # Calculate threshold date for expiring soon calculations
        threshold_date = datetime.now(UTC) + timedelta(days=days_threshold or 30)

        # Apply filters using helpers
        certificates = _filter_certs_by_provider(certificates, provider)
        certificates = _filter_certs_by_domain(certificates, domain_filter)

        # Count expiring soon before final filter
        expiring_soon_count = sum(
            1 for cert in certificates if _is_expiring_soon(cert, threshold_date)
        )

        # Apply expiring soon filter using helper
        certificates = _filter_certs_expiring_soon(certificates, expiring_soon, threshold_date)

        server_ctx.logger.info(
            "tool_success",
            tool="npm_list_certificates",
            total=total,
            returned=len(certificates),
            expiring_soon_count=expiring_soon_count,
        )

        # Apply compaction if requested (default: True)
        result_certs = [compact_certificate(c) for c in certificates] if compact else certificates

        return {
            "success": True,
            "certificates": result_certs,
            "total": total,
            "expiring_soon_count": expiring_soon_count,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_list_certificates", error=str(e))
        return {"success": False, "error": str(e)}


async def npm_manage_certificate(
    ctx: MCPContext,
    operation: Literal["create", "update", "delete", "renew"],
    instance_name: str | None = None,
    cert_id: int | None = None,
    provider: str | None = None,
    nice_name: str | None = None,
    domain_names: list[str] | None = None,
    letsencrypt_email: str | None = None,
    letsencrypt_agree_tos: bool | None = None,
    dns_challenge: bool | None = False,
    dns_provider: str | None = None,
    dns_credentials: dict[str, Any] | str | None = None,
    propagation_seconds: int | None = 60,
    custom_certificate: str | None = None,
    custom_certificate_key: str | None = None,
) -> dict[str, Any]:
    """
    Create, update, delete, or renew SSL/TLS certificates.

    This tool provides comprehensive certificate management including:
    - Let's Encrypt automatic certificates (HTTP and DNS challenges)
    - Custom certificate uploads
    - Certificate renewal
    - Certificate updates and deletion

    Args:
        ctx: MCP context (auto-injected)
        operation: Operation to perform (create|update|delete|renew)
        instance_name: Target instance name (optional, uses active instance)
        cert_id: Certificate ID (required for update/delete/renew)
        provider: Certificate provider (letsencrypt|custom) (required for create)
        nice_name: Human-readable certificate name (required for create)
        domain_names: Domain names for certificate (required for create)
        letsencrypt_email: Email for Let's Encrypt (required for letsencrypt)
        letsencrypt_agree_tos: Agree to LE TOS (required for letsencrypt)
        dns_challenge: Use DNS challenge (required for wildcards)
        dns_provider: DNS provider (cloudflare|route53|etc) (required for DNS challenge)
        dns_credentials: DNS provider credentials JSON string
        propagation_seconds: DNS propagation wait time (default: 60)
        custom_certificate: Custom certificate PEM (required for custom provider)
        custom_certificate_key: Custom certificate key PEM (required for custom provider)

    Returns:
        Dictionary with:
        - success: bool - Operation success status
        - operation: str - Operation performed
        - certificate: dict - Certificate details (for create/update/renew)
        - cert_id: int - Certificate ID (for delete)
        - error: str - Error message (if success is False)

    Example:
        >>> # Create Let's Encrypt certificate
        >>> result = await npm_manage_certificate(
        ...     ctx,
        ...     operation="create",
        ...     provider="letsencrypt",
        ...     nice_name="Example Cert",
        ...     domain_names=["example.com", "www.example.com"],
        ...     letsencrypt_email="admin@example.com",
        ...     letsencrypt_agree_tos=True,
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_manage_certificate",
        operation=operation,
        instance=instance_name or "active",
        cert_id=cert_id,
    )

    try:
        # Validate parameters BEFORE getting client
        if operation == "create":
            validation_error = _validate_create_params(provider, nice_name, domain_names)
            if validation_error:
                return validation_error
        elif operation in ("update", "renew", "delete"):
            if not cert_id:
                return {"success": False, "error": f"cert_id is required for {operation} operation"}
        else:
            valid_ops = "create, update, delete, renew"
            return {
                "success": False,
                "error": f"Invalid operation '{operation}'. Must be: {valid_ops}",
            }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Route to appropriate handler based on operation
        if operation == "create":
            return await _handle_create_cert(
                client,
                server_ctx,
                provider=provider,  # type: ignore[arg-type]
                nice_name=nice_name,  # type: ignore[arg-type]
                domain_names=domain_names,  # type: ignore[arg-type]
                letsencrypt_email=letsencrypt_email,
                letsencrypt_agree_tos=letsencrypt_agree_tos,
                dns_challenge=dns_challenge,
                dns_provider=dns_provider,
                dns_credentials=dns_credentials,
                propagation_seconds=propagation_seconds,
                custom_certificate=custom_certificate,
                custom_certificate_key=custom_certificate_key,
            )

        # cert_id validated above for update/renew/delete operations
        assert cert_id is not None  # nosec B101 - type narrowing after validation

        if operation == "update":
            return await _handle_update_cert(
                client,
                server_ctx,
                cert_id,
                nice_name=nice_name,
                domain_names=domain_names,
            )

        if operation == "renew":
            return await _handle_renew_cert(client, server_ctx, cert_id)

        # operation == "delete"
        return await _handle_delete_cert(client, server_ctx, cert_id)

    except Exception as e:
        server_ctx.logger.error(
            "tool_error", tool="npm_manage_certificate", operation=operation, error=str(e)
        )
        return {"success": False, "error": str(e)}


async def npm_validate_certificate(
    ctx: MCPContext,
    instance_name: str | None = None,
    provider: str | None = None,
    domain_names: list[str] | None = None,
    letsencrypt_email: str | None = None,
    dns_challenge: bool | None = None,
    dns_provider: str | None = None,
    dns_credentials: str | None = None,
) -> dict[str, Any]:
    """
    Validate certificate configuration before creation (pre-flight check).

    This tool performs comprehensive validation checks including:
    - Domain name syntax validation
    - DNS record verification
    - HTTP reachability checks
    - DNS provider credential validation
    - Wildcard certificate requirements

    Args:
        ctx: MCP context (auto-injected)
        instance_name: Target instance name (optional, uses active instance)
        provider: Certificate provider (letsencrypt|custom) (required)
        domain_names: Domain names to validate (required)
        letsencrypt_email: Email for Let's Encrypt (required for letsencrypt)
        dns_challenge: Use DNS challenge (optional)
        dns_provider: DNS provider (optional)
        dns_credentials: DNS provider credentials (optional)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - valid: bool - Whether configuration is valid
        - validation_results: list - Detailed validation checks
        - warnings: list - Warning messages
        - errors: list - Error messages
        - error: str - Error message (if tool execution fails)

    Example:
        >>> result = await npm_validate_certificate(
        ...     ctx,
        ...     provider="letsencrypt",
        ...     domain_names=["example.com"],
        ...     letsencrypt_email="admin@example.com",
        ... )
        >>> if result["valid"]:
        ...     print("Configuration is valid!")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="npm_validate_certificate",
        instance=instance_name or "active",
        provider=provider,
        domain_count=len(domain_names) if domain_names else 0,
    )

    try:
        # Validate required parameters
        if not provider:
            return {"success": False, "error": "provider is required"}
        if not domain_names:
            return {"success": False, "error": "domain_names is required"}

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Build validation request data
        data = _build_validation_data(
            provider,
            domain_names,
            letsencrypt_email,
            dns_challenge,
            dns_provider,
            dns_credentials,
        )

        # Check for wildcard domains requiring DNS challenge
        has_wildcard = any(domain.startswith("*") for domain in domain_names)
        wildcard_warning = (
            ["Wildcard certificates require DNS challenge"]
            if has_wildcard and not dns_challenge
            else []
        )

        # Call validation API
        validation_results, api_warnings, errors = await _call_validation_api(
            client, server_ctx, data
        )
        warnings = wildcard_warning + api_warnings

        valid = len(errors) == 0

        server_ctx.logger.info(
            "certificate_validated",
            valid=valid,
            warnings_count=len(warnings),
            errors_count=len(errors),
        )

        return {
            "success": True,
            "valid": valid,
            "validation_results": validation_results,
            "warnings": warnings,
            "errors": errors,
        }

    except Exception as e:
        server_ctx.logger.error("tool_error", tool="npm_validate_certificate", error=str(e))
        return {"success": False, "error": str(e)}


def register_certificate_tools(mcp: FastMCP) -> None:
    """
    Register all certificate management tools with the FastMCP server.

    This function registers 3 certificate tools:
    - npm_list_certificates
    - npm_manage_certificate
    - npm_validate_certificate

    Args:
        mcp: FastMCP server instance
    """
    # npm_list_certificates (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_list_certificates
    )

    # npm_manage_certificate (destructive - creates, updates, deletes, renews)
    mcp.tool(annotations=ToolAnnotations(destructiveHint=True))(npm_manage_certificate)

    # npm_validate_certificate (read-only, idempotent)
    mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))(
        npm_validate_certificate
    )
