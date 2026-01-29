"""
Bulk operation MCP tools for Nginx Proxy Manager.

This module provides bulk operations for managing multiple NPM resources efficiently:
- renew_certificates: Bulk renewal of SSL/TLS certificates
- toggle_hosts: Bulk enable/disable proxy hosts
- delete_resources: Bulk deletion of resources with filters
- export_config: Export NPM configuration to JSON/YAML
- import_config: Import NPM configuration from JSON/YAML

All tools support:
- Concurrent batch processing with configurable batch sizes
- Dry-run mode for previewing changes
- Error resilience (continue on error)
- Detailed per-item result tracking
"""

import json
from datetime import UTC, datetime, timedelta
from typing import Any

import yaml
from mcp.types import ToolAnnotations

from npm_mcp.constants import (
    API_ACCESS_LISTS,
    API_CERTIFICATES,
    API_DEAD_HOSTS,
    API_PROXY_HOSTS,
    API_REDIRECTIONS,
    API_STREAMS,
    API_USERS,
)
from npm_mcp.models.bulk import (
    BulkOperationItemResult,
    ItemStatus,
    OperationType,
    ResourceType,
)
from npm_mcp.types import MCPContext
from npm_mcp.utils.batch import BatchProcessor, BatchProcessorConfig


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
# Helper Functions to Reduce Cognitive Complexity
# =============================================================================


def _parse_cert_expiry(expires_on_str: str, threshold_date: datetime) -> bool:
    """Check if certificate expires before threshold. Returns True if expiring."""
    try:
        expires_on = datetime.fromisoformat(expires_on_str.replace("Z", "+00:00"))
        if expires_on.tzinfo is None:
            expires_on = expires_on.replace(tzinfo=UTC)
        return expires_on < threshold_date
    except (ValueError, AttributeError, TypeError):
        return False


def _filter_expiring_certs(certificates: list[dict[str, Any]], days: int) -> list[int]:
    """Filter certificates expiring within given days. Returns list of cert IDs."""
    threshold = datetime.now(UTC) + timedelta(days=days)
    return [
        cert["id"]
        for cert in certificates
        if cert.get("expires_on") and _parse_cert_expiry(cert["expires_on"], threshold)
    ]


def _host_matches_filters(
    host: dict[str, Any],
    domain_pattern: str | None,
    enabled_only: bool | None,
) -> bool:
    """Check if host matches the given filters."""
    if domain_pattern:
        domain_names = host.get("domain_names", [])
        if not any(domain_pattern in domain for domain in domain_names):
            return False
    if enabled_only is not None:
        host_enabled = host.get("enabled", False)
        if enabled_only and not host_enabled:
            return False
        if not enabled_only and host_enabled:
            return False
    return True


def _filter_hosts(
    hosts: list[dict[str, Any]],
    domain_pattern: str | None,
    enabled_only: bool | None,
) -> list[int]:
    """Filter hosts by domain pattern and enabled status. Returns list of host IDs."""
    return [
        host["id"] for host in hosts if _host_matches_filters(host, domain_pattern, enabled_only)
    ]


def _parse_import_data(
    import_data: dict[str, Any] | None,
    import_data_json: str | None,
    import_data_yaml: str | None,
) -> dict[str, Any] | dict[str, str]:
    """Parse import data from dict, JSON, or YAML. Returns data or error dict."""
    if import_data is not None:
        return import_data
    if import_data_json:
        try:
            result: dict[str, Any] = json.loads(import_data_json)
            return result
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON format: {e!s}"}
    if import_data_yaml:
        try:
            yaml_result = yaml.safe_load(import_data_yaml)
            if not isinstance(yaml_result, dict):
                return {"error": "YAML content must be a dictionary"}
            return yaml_result
        except yaml.YAMLError as e:
            return {"error": f"Invalid YAML format: {e!s}"}
    return {"error": "At least one of import_data, import_data_json, or import_data_yaml required"}


def _filter_resources_for_deletion(
    resources: list[dict[str, Any]],
    domain_pattern: str | None,
) -> list[int]:
    """Filter resources by domain pattern and return matching IDs."""
    result = []
    for resource in resources:
        if domain_pattern:
            domain_names = resource.get("domain_names", [])
            if not domain_names:
                continue
            if not any(domain_pattern in domain for domain in domain_names):
                continue
        result.append(resource["id"])
    return result


def _get_resource_type_endpoints() -> dict[str, str]:
    """Get mapping of resource type strings to API endpoints."""
    return {
        "proxy_hosts": API_PROXY_HOSTS,
        "certificates": API_CERTIFICATES,
        "access_lists": API_ACCESS_LISTS,
        "streams": API_STREAMS,
        "redirections": API_REDIRECTIONS,
        "dead_hosts": API_DEAD_HOSTS,
        "users": API_USERS,
    }


def _get_enum_resource_endpoints() -> dict[ResourceType, str]:
    """Get mapping of ResourceType enum to API endpoints."""
    return {
        ResourceType.PROXY_HOSTS: API_PROXY_HOSTS,
        ResourceType.CERTIFICATES: API_CERTIFICATES,
        ResourceType.ACCESS_LISTS: API_ACCESS_LISTS,
        ResourceType.STREAMS: API_STREAMS,
        ResourceType.REDIRECTIONS: API_REDIRECTIONS,
        ResourceType.DEAD_HOSTS: API_DEAD_HOSTS,
        ResourceType.USERS: API_USERS,
    }


def _expand_resource_types(resource_types: list[ResourceType]) -> list[ResourceType]:
    """Expand ALL to individual resource types if present."""
    if ResourceType.ALL in resource_types:
        return [
            ResourceType.PROXY_HOSTS,
            ResourceType.CERTIFICATES,
            ResourceType.ACCESS_LISTS,
            ResourceType.STREAMS,
            ResourceType.REDIRECTIONS,
            ResourceType.DEAD_HOSTS,
            ResourceType.USERS,
        ]
    return resource_types


def _determine_bulk_status(successful_count: int, failed_count: int, total_items: int) -> str:
    """Determine overall bulk operation status."""
    if total_items == 0 or failed_count == 0:
        return "completed"
    if successful_count == 0:
        return "failed"
    return "partial"


async def _fetch_resources_by_ids(
    client: Any,  # noqa: ANN401
    endpoint: str,
    resource_ids: list[int],
    continue_on_error: bool,
    logger: Any,  # noqa: ANN401
    resource_type_value: str,
) -> list[dict[str, Any]]:
    """Fetch specific resources by ID, handling errors per item."""
    resources: list[dict[str, Any]] = []
    for resource_id in resource_ids:
        try:
            resource = await client.get(f"{endpoint}/{resource_id}")
            resources.append(resource)
        except Exception as e:
            if not continue_on_error:
                raise
            logger.warning(
                "export_resource_error",
                resource_type=resource_type_value,
                resource_id=resource_id,
                error=str(e),
            )
    return resources


def _create_import_dry_run_results(
    data: dict[str, Any],
    resource_endpoints: dict[str, str],
) -> list[BulkOperationItemResult]:
    """Create preview results for dry-run import."""
    results: list[BulkOperationItemResult] = []
    item_count = 0
    for resource_type_str, resources in data.items():
        if resource_type_str not in resource_endpoints:
            continue
        for _ in resources:
            item_count += 1
            results.append(
                BulkOperationItemResult(
                    resource_id=item_count,
                    resource_type=ResourceType(resource_type_str),
                    action="preview",
                    status=ItemStatus.SKIPPED,
                    details={"message": "Dry-run mode - no data imported"},
                )
            )
    return results


async def _delete_existing_resources_for_replace(
    client: Any,  # noqa: ANN401
    endpoint: str,
    continue_on_error: bool,
    logger: Any,  # noqa: ANN401
    resource_type_str: str,
) -> None:
    """Delete existing resources as part of replace strategy."""
    existing_resources = await client.get(endpoint)
    for existing in existing_resources:
        try:
            await client.delete(f"{endpoint}/{existing['id']}")
        except Exception as e:
            logger.warning(
                "import_delete_error",
                resource_type=resource_type_str,
                resource_id=existing["id"],
                error=str(e),
            )
            if not continue_on_error:
                raise


async def renew_certificates(
    ctx: MCPContext,
    cert_ids: list[int] | None = None,
    expiring_within_days: int | None = None,
    instance_name: str | None = None,
    dry_run: bool = False,
    batch_size: int = 10,
    continue_on_error: bool = True,
) -> dict[str, Any]:
    """
    Bulk renew SSL/TLS certificates.

    Renews multiple certificates concurrently with support for filtering,
    dry-run mode, and error resilience.

    Args:
        ctx: MCP context (auto-injected)
        cert_ids: List of certificate IDs to renew (optional)
        expiring_within_days: Renew certificates expiring within N days (optional)
        instance_name: Target instance name (optional, uses active instance)
        dry_run: Preview changes without executing (default: False)
        batch_size: Number of certificates to process concurrently (1-50, default: 10)
        continue_on_error: Continue processing on errors (default: True)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - operation: str - Operation type
        - result: dict - BulkOperationResult with detailed per-item results
        - error: str - Error message (if tool execution fails)

    Example:
        >>> # Renew specific certificates
        >>> result = await renew_certificates(ctx, cert_ids=[1, 2, 3])

        >>> # Renew certificates expiring within 30 days
        >>> result = await renew_certificates(ctx, expiring_within_days=30)

        >>> # Dry-run to preview changes
        >>> result = await renew_certificates(ctx, cert_ids=[1, 2], dry_run=True)
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="renew_certificates",
        instance=instance_name or "active",
        cert_ids=cert_ids,
        expiring_within_days=expiring_within_days,
        dry_run=dry_run,
    )

    try:
        # Validate parameters (None means not provided, [] is valid empty list)
        if cert_ids is None and expiring_within_days is None:
            return {
                "success": False,
                "error": "Either cert_ids or expiring_within_days must be provided",
            }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Determine which certificates to renew
        target_cert_ids: list[int] = []

        if cert_ids:
            target_cert_ids = cert_ids
        elif expiring_within_days:
            certificates = await client.get(API_CERTIFICATES)
            target_cert_ids = _filter_expiring_certs(certificates, expiring_within_days)

        # Create items list for BatchProcessor
        items = [{"id": cert_id} for cert_id in target_cert_ids]

        # Configure batch processor
        config = BatchProcessorConfig(
            batch_size=batch_size,
            continue_on_error=continue_on_error,
            dry_run=dry_run,
        )
        processor = BatchProcessor(config=config)

        # Define process function for individual certificate renewal
        async def process_cert_renewal(item: dict[str, Any]) -> BulkOperationItemResult:
            """Process a single certificate renewal."""
            cert_id = item["id"]

            try:
                # Call NPM API to renew certificate
                renewed_cert = await client.post(f"{API_CERTIFICATES}/{cert_id}/renew")

                # Create success result
                return BulkOperationItemResult(
                    resource_id=cert_id,
                    resource_type=ResourceType.CERTIFICATES,
                    action="renew",
                    status=ItemStatus.SUCCESS,
                    details={"expires_on": renewed_cert.get("expires_on")},
                )
            except Exception as e:
                # Create error result
                return BulkOperationItemResult(
                    resource_id=cert_id,
                    resource_type=ResourceType.CERTIFICATES,
                    action="renew",
                    status=ItemStatus.ERROR,
                    error=str(e),
                )

        # Process batch
        bulk_result = await processor.process_batch(
            items=items,
            process_fn=process_cert_renewal,
            operation_type=OperationType.RENEW_CERTIFICATES,
            instance_name=instance_name,
        )

        # Convert BulkOperationResult to dict for JSON serialization
        result_dict = bulk_result.model_dump()

        server_ctx.logger.info(
            "bulk_operation_complete",
            tool="renew_certificates",
            total=result_dict["total_items"],
            successful=result_dict["successful"],
            failed=result_dict["failed"],
            duration=result_dict["duration_seconds"],
        )

        return {
            "success": True,
            "operation": OperationType.RENEW_CERTIFICATES.value,
            "result": result_dict,
        }

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="renew_certificates",
            error=str(e),
        )
        return {"success": False, "error": str(e)}


async def toggle_hosts(
    ctx: MCPContext,
    action: str,
    host_ids: list[int] | None = None,
    domain_pattern: str | None = None,
    enabled_only: bool | None = None,
    instance_name: str | None = None,
    dry_run: bool = False,
    batch_size: int = 10,
    continue_on_error: bool = True,
) -> dict[str, Any]:
    """
    Bulk enable or disable proxy hosts.

    Enables or disables multiple proxy hosts concurrently with support for filtering,
    dry-run mode, and error resilience.

    Args:
        ctx: MCP context (auto-injected)
        action: Action to perform (enable|disable)
        host_ids: List of proxy host IDs to toggle (optional)
        domain_pattern: Filter by domain pattern (substring match) (optional)
        enabled_only: Only toggle enabled hosts (optional)
        instance_name: Target instance name (optional, uses active instance)
        dry_run: Preview changes without executing (default: False)
        batch_size: Number of hosts to process concurrently (1-50, default: 10)
        continue_on_error: Continue processing on errors (default: True)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - operation: str - Operation type
        - result: dict - BulkOperationResult with detailed per-item results
        - error: str - Error message (if tool execution fails)

    Example:
        >>> # Enable specific hosts
        >>> result = await toggle_hosts(ctx, action="enable", host_ids=[1, 2, 3])

        >>> # Disable all hosts matching "staging"
        >>> result = await toggle_hosts(ctx, action="disable", domain_pattern="staging")

        >>> # Dry-run to preview changes
        >>> result = await toggle_hosts(ctx, action="enable", host_ids=[1, 2], dry_run=True)
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="toggle_hosts",
        instance=instance_name or "active",
        action=action,
        host_ids=host_ids,
        domain_pattern=domain_pattern,
        enabled_only=enabled_only,
        dry_run=dry_run,
    )

    try:
        # Validate action
        if action not in ["enable", "disable"]:
            return {
                "success": False,
                "error": "action must be either enable or disable",
            }

        # Validate parameters (None means not provided, [] is valid empty list)
        if host_ids is None and domain_pattern is None and enabled_only is None:
            return {
                "success": False,
                "error": (
                    "Either host_ids or filter (domain_pattern, enabled_only) must be provided"
                ),
            }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Determine which hosts to toggle
        target_host_ids: list[int] = []

        if host_ids is not None:
            target_host_ids = host_ids
        else:
            hosts = await client.get(API_PROXY_HOSTS)
            target_host_ids = _filter_hosts(hosts, domain_pattern, enabled_only)

        # Create items list for BatchProcessor
        items = [{"id": host_id} for host_id in target_host_ids]

        # Configure batch processor
        config = BatchProcessorConfig(
            batch_size=batch_size,
            continue_on_error=continue_on_error,
            dry_run=dry_run,
        )
        processor = BatchProcessor(config=config)

        # Define process function for individual host toggle
        async def process_host_toggle(item: dict[str, Any]) -> BulkOperationItemResult:
            """Process a single host toggle."""
            host_id = item["id"]

            try:
                # Prepare update data
                enabled_value = action == "enable"
                data = {"enabled": enabled_value}

                # Call NPM API to update host
                updated_host = await client.put(
                    f"{API_PROXY_HOSTS}/{host_id}",
                    json=data,
                )

                # Create success result
                return BulkOperationItemResult(
                    resource_id=host_id,
                    resource_type=ResourceType.PROXY_HOSTS,
                    action=action,
                    status=ItemStatus.SUCCESS,
                    details={"enabled": updated_host.get("enabled")},
                )
            except Exception as e:
                # Create error result
                return BulkOperationItemResult(
                    resource_id=host_id,
                    resource_type=ResourceType.PROXY_HOSTS,
                    action=action,
                    status=ItemStatus.ERROR,
                    error=str(e),
                )

        # Process batch
        bulk_result = await processor.process_batch(
            items=items,
            process_fn=process_host_toggle,
            operation_type=OperationType.TOGGLE_HOSTS,
            instance_name=instance_name,
        )

        # Convert BulkOperationResult to dict for JSON serialization
        result_dict = bulk_result.model_dump()

        server_ctx.logger.info(
            "bulk_operation_complete",
            tool="toggle_hosts",
            action=action,
            total=result_dict["total_items"],
            successful=result_dict["successful"],
            failed=result_dict["failed"],
            duration=result_dict["duration_seconds"],
        )

        return {
            "success": True,
            "operation": OperationType.TOGGLE_HOSTS.value,
            "result": result_dict,
        }

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="toggle_hosts",
            error=str(e),
        )
        return {"success": False, "error": str(e)}


async def delete_resources(
    ctx: MCPContext,
    resource_type: ResourceType,
    resource_ids: list[int] | None = None,
    domain_pattern: str | None = None,
    instance_name: str | None = None,
    dry_run: bool = False,
    batch_size: int = 10,
    continue_on_error: bool = True,
) -> dict[str, Any]:
    """
    Bulk delete resources (proxy hosts, certificates, etc.).

    Deletes multiple resources concurrently with support for filtering,
    dry-run mode, and error resilience.

    Args:
        ctx: MCP context (auto-injected)
        resource_type: Type of resource to delete (proxy_hosts, certificates, etc.)
        resource_ids: List of resource IDs to delete (optional)
        domain_pattern: Filter by domain pattern (substring match) (optional)
        instance_name: Target instance name (optional, uses active instance)
        dry_run: Preview changes without executing (default: False)
        batch_size: Number of resources to process concurrently (1-50, default: 10)
        continue_on_error: Continue processing on errors (default: True)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - operation: str - Operation type
        - result: dict - BulkOperationResult with detailed per-item results
        - error: str - Error message (if tool execution fails)

    Example:
        >>> # Delete specific proxy hosts
        >>> result = await delete_resources(
        ...     ctx,
        ...     resource_type=ResourceType.PROXY_HOSTS,
        ...     resource_ids=[1, 2, 3]
        ... )

        >>> # Delete all hosts matching "test"
        >>> result = await delete_resources(
        ...     ctx,
        ...     resource_type=ResourceType.PROXY_HOSTS,
        ...     domain_pattern="test"
        ... )

        >>> # Dry-run to preview deletions
        >>> result = await delete_resources(
        ...     ctx,
        ...     resource_type=ResourceType.CERTIFICATES,
        ...     resource_ids=[1, 2],
        ...     dry_run=True
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="delete_resources",
        instance=instance_name or "active",
        resource_type=resource_type.value,
        resource_ids=resource_ids,
        domain_pattern=domain_pattern,
        dry_run=dry_run,
    )

    try:
        # Validate parameters (None means not provided, [] is valid empty list)
        if resource_ids is None and domain_pattern is None:
            return {
                "success": False,
                "error": "Either resource_ids or filter (domain_pattern) must be provided",
            }

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Map resource_type to API endpoints
        resource_endpoints = {
            ResourceType.PROXY_HOSTS: API_PROXY_HOSTS,
            ResourceType.CERTIFICATES: API_CERTIFICATES,
            ResourceType.ACCESS_LISTS: API_ACCESS_LISTS,
            ResourceType.STREAMS: API_STREAMS,
            ResourceType.REDIRECTIONS: API_REDIRECTIONS,
            ResourceType.DEAD_HOSTS: API_DEAD_HOSTS,
            ResourceType.USERS: API_USERS,
        }

        base_endpoint = resource_endpoints.get(resource_type)
        if not base_endpoint:
            return {
                "success": False,
                "error": f"Unsupported resource_type: {resource_type.value}",
            }

        # Determine which resources to delete
        if resource_ids is not None:
            target_resource_ids = resource_ids
        else:
            # Fetch all resources and filter by domain pattern
            resources = await client.get(base_endpoint)
            target_resource_ids = _filter_resources_for_deletion(resources, domain_pattern)

        # Create items list for BatchProcessor
        items = [{"id": resource_id} for resource_id in target_resource_ids]

        # Configure batch processor
        config = BatchProcessorConfig(
            batch_size=batch_size,
            continue_on_error=continue_on_error,
            dry_run=dry_run,
        )
        processor = BatchProcessor(config=config)

        # Define process function for individual resource deletion
        async def process_resource_deletion(item: dict[str, Any]) -> BulkOperationItemResult:
            """Process a single resource deletion."""
            resource_id = item["id"]

            try:
                # Call NPM API to delete resource
                await client.delete(f"{base_endpoint}/{resource_id}")

                # Create success result
                return BulkOperationItemResult(
                    resource_id=resource_id,
                    resource_type=resource_type,
                    action="delete",
                    status=ItemStatus.SUCCESS,
                )
            except Exception as e:
                # Create error result
                return BulkOperationItemResult(
                    resource_id=resource_id,
                    resource_type=resource_type,
                    action="delete",
                    status=ItemStatus.ERROR,
                    error=str(e),
                )

        # Process batch
        bulk_result = await processor.process_batch(
            items=items,
            process_fn=process_resource_deletion,
            operation_type=OperationType.DELETE_RESOURCES,
            instance_name=instance_name,
        )

        # Convert BulkOperationResult to dict for JSON serialization
        result_dict = bulk_result.model_dump()

        server_ctx.logger.info(
            "bulk_operation_complete",
            tool="delete_resources",
            resource_type=resource_type.value,
            total=result_dict["total_items"],
            successful=result_dict["successful"],
            failed=result_dict["failed"],
            duration=result_dict["duration_seconds"],
        )

        return {
            "success": True,
            "operation": OperationType.DELETE_RESOURCES.value,
            "result": result_dict,
        }

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="delete_resources",
            error=str(e),
        )
        return {"success": False, "error": str(e)}


def _create_export_dry_run_results(
    resource_types: list[ResourceType],
) -> list[BulkOperationItemResult]:
    """Create preview results for dry-run export."""
    return [
        BulkOperationItemResult(
            resource_id=0,
            resource_type=rt,
            action="preview",
            status=ItemStatus.SKIPPED,
            details={"message": "Dry-run mode - no data exported"},
        )
        for rt in resource_types
    ]


async def _export_single_resource_type(
    client: Any,  # noqa: ANN401
    resource_type: ResourceType,
    endpoint: str,
    resource_ids: list[int] | None,
    continue_on_error: bool,
    logger: Any,  # noqa: ANN401
) -> tuple[BulkOperationItemResult, list[Any] | None]:
    """Export a single resource type. Returns (result, data) tuple."""
    try:
        if resource_ids:
            resources = await _fetch_resources_by_ids(
                client, endpoint, resource_ids, continue_on_error, logger, resource_type.value
            )
        else:
            resources = await client.get(endpoint)

        result = BulkOperationItemResult(
            resource_id=len(resources),
            resource_type=resource_type,
            action="export",
            status=ItemStatus.SUCCESS,
            details={"count": len(resources)},
        )
        return result, resources
    except Exception as e:
        result = BulkOperationItemResult(
            resource_id=0,
            resource_type=resource_type,
            action="export",
            status=ItemStatus.ERROR,
            error=str(e),
        )
        return result, None


async def _process_export_resources(
    client: Any,  # noqa: ANN401
    resource_types: list[ResourceType],
    resource_endpoints: dict[ResourceType, str],
    resource_ids: list[int] | None,
    continue_on_error: bool,
    logger: Any,  # noqa: ANN401
) -> tuple[list[BulkOperationItemResult], dict[str, Any], int, int]:
    """Process export for all resource types.

    Returns:
        Tuple of (results, export_data, success_count, fail_count).
    """
    results: list[BulkOperationItemResult] = []
    export_data: dict[str, Any] = {}
    successful_count = 0
    failed_count = 0

    for resource_type in resource_types:
        endpoint = resource_endpoints.get(resource_type)
        if not endpoint:
            results.append(
                BulkOperationItemResult(
                    resource_id=0,
                    resource_type=resource_type,
                    action="export",
                    status=ItemStatus.ERROR,
                    error=f"Unsupported resource type: {resource_type.value}",
                )
            )
            failed_count += 1
            continue

        result, resources = await _export_single_resource_type(
            client, resource_type, endpoint, resource_ids, continue_on_error, logger
        )
        results.append(result)

        if resources is not None:
            export_data[resource_type.value] = resources
            successful_count += 1
        else:
            failed_count += 1
            if not continue_on_error:
                break

    return results, export_data, successful_count, failed_count


async def export_config(
    ctx: MCPContext,
    resource_types: list[ResourceType] | None = None,
    resource_ids: list[int] | None = None,
    format: str = "json",
    instance_name: str | None = None,
    dry_run: bool = False,
    continue_on_error: bool = True,
) -> dict[str, Any]:
    """
    Export NPM configuration to JSON or YAML format.

    Exports configuration data for selected resource types, with support for
    filtering by resource IDs, dry-run mode, and error resilience.

    Args:
        ctx: MCP context (auto-injected)
        resource_types: List of resource types to export (required)
        resource_ids: List of specific resource IDs to export (optional)
        format: Output format (json|yaml) (default: json)
        instance_name: Target instance name (optional, uses active instance)
        dry_run: Preview changes without executing (default: False)
        continue_on_error: Continue processing on errors (default: True)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - operation: str - Operation type
        - result: dict - BulkOperationResult with detailed per-item results
        - export_data: dict - Exported configuration data (if format=json)
        - export_data_yaml: str - Exported configuration as YAML string (if format=yaml)
        - metadata: dict - Export metadata (timestamp, version, etc.)
        - format: str - Output format used
        - error: str - Error message (if tool execution fails)

    Example:
        >>> # Export all resources as JSON
        >>> result = await export_config(
        ...     ctx,
        ...     resource_types=[ResourceType.ALL],
        ...     format="json"
        ... )

        >>> # Export specific proxy hosts as YAML
        >>> result = await export_config(
        ...     ctx,
        ...     resource_types=[ResourceType.PROXY_HOSTS],
        ...     resource_ids=[1, 2, 3],
        ...     format="yaml"
        ... )

        >>> # Dry-run to preview export
        >>> result = await export_config(
        ...     ctx,
        ...     resource_types=[ResourceType.PROXY_HOSTS],
        ...     dry_run=True
        ... )
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="export_config",
        instance=instance_name or "active",
        resource_types=[rt.value for rt in resource_types] if resource_types else [],
        format=format,
        dry_run=dry_run,
    )

    try:
        # Validate parameters
        if not resource_types:
            return {
                "success": False,
                "error": "resource_types parameter is required",
            }

        if format not in ["json", "yaml"]:
            return {
                "success": False,
                "error": f"Invalid format '{format}'. Must be 'json' or 'yaml'",
            }

        # Start timing
        start_time = datetime.now(UTC)

        # Expand ResourceType.ALL and get endpoint mappings
        resource_types_to_export = _expand_resource_types(resource_types)
        resource_endpoints = _get_enum_resource_endpoints()

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Process export (dry-run or actual)
        if dry_run:
            results = _create_export_dry_run_results(resource_types_to_export)
            export_data: dict[str, Any] = {}
            successful_count = 0
            failed_count = 0
        else:
            results, export_data, successful_count, failed_count = await _process_export_resources(
                client,
                resource_types_to_export,
                resource_endpoints,
                resource_ids,
                continue_on_error,
                server_ctx.logger,
            )

        # Calculate duration
        end_time = datetime.now(UTC)
        duration = (end_time - start_time).total_seconds()

        # Determine overall status
        total_items = len(results)
        status = _determine_bulk_status(successful_count, failed_count, total_items)

        # Create BulkOperationResult
        from npm_mcp.models.bulk import BulkOperationResult

        bulk_result = BulkOperationResult(
            operation=OperationType.EXPORT_CONFIG,
            status=status,
            total_items=total_items,
            successful=successful_count,
            failed=failed_count,
            dry_run=dry_run,
            results=results,
            duration_seconds=duration,
            instance_name=instance_name,
        )

        # Create metadata
        metadata = {
            "exported_at": datetime.now(UTC).isoformat(),
            "resource_types": [rt.value for rt in resource_types_to_export],
            "format": format,
            "instance_name": instance_name or "active",
        }

        # Convert to dict for JSON serialization
        result_dict = bulk_result.model_dump()

        # Prepare response
        response: dict[str, Any] = {
            "success": True,
            "operation": OperationType.EXPORT_CONFIG.value,
            "result": result_dict,
            "format": format,
            "metadata": metadata,
        }

        # Add export data in requested format
        if format == "json":
            response["export_data"] = export_data
        elif format == "yaml":
            response["export_data"] = export_data  # Also include dict version
            response["export_data_yaml"] = yaml.dump(
                export_data,
                default_flow_style=False,
                sort_keys=False,
            )

        server_ctx.logger.info(
            "bulk_operation_complete",
            tool="export_config",
            total=total_items,
            successful=successful_count,
            failed=failed_count,
            duration=duration,
        )

        return response

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="export_config",
            error=str(e),
        )
        return {"success": False, "error": str(e)}


async def _import_single_resource_type(
    client: Any,  # noqa: ANN401
    resource_type: ResourceType,
    endpoint: str,
    resources: list[dict[str, Any]],
    batch_size: int,
    continue_on_error: bool,
    strategy: str,
    logger: Any,  # noqa: ANN401
    instance_name: str | None,
) -> tuple[list[BulkOperationItemResult], int, int]:
    """Import resources for a single resource type. Returns (results, success_count, fail_count)."""
    # Handle replace strategy: delete existing resources first
    if strategy == "replace":
        try:
            await _delete_existing_resources_for_replace(
                client, endpoint, continue_on_error, logger, resource_type.value
            )
        except Exception as e:
            logger.error(
                "import_replace_fetch_error", resource_type=resource_type.value, error=str(e)
            )
            if not continue_on_error:
                raise

    # Configure batch processor
    items = [{"data": resource} for resource in resources]
    config = BatchProcessorConfig(
        batch_size=batch_size, continue_on_error=continue_on_error, dry_run=False
    )
    processor = BatchProcessor(config=config)

    # Define process function for individual resource import
    async def process_resource_import(
        item: dict[str, Any],
        *,
        _endpoint: str = endpoint,
        _resource_type: ResourceType = resource_type,
    ) -> BulkOperationItemResult:
        """Process a single resource import."""
        resource_data = item["data"]
        try:
            created_resource = await client.post(_endpoint, json=resource_data)
            return BulkOperationItemResult(
                resource_id=created_resource.get("id", 0),
                resource_type=_resource_type,
                action="import",
                status=ItemStatus.SUCCESS,
                details={"created_id": created_resource.get("id")},
            )
        except Exception as e:
            return BulkOperationItemResult(
                resource_id=0,
                resource_type=_resource_type,
                action="import",
                status=ItemStatus.ERROR,
                error=str(e),
            )

    # Process batch
    bulk_result = await processor.process_batch(
        items=items,
        process_fn=process_resource_import,
        operation_type=OperationType.IMPORT_CONFIG,
        instance_name=instance_name,
    )

    return list(bulk_result.results), bulk_result.successful, bulk_result.failed


async def import_config(
    ctx: MCPContext,
    import_data: dict[str, Any] | None = None,
    import_data_json: str | None = None,
    import_data_yaml: str | None = None,
    strategy: str = "merge",
    instance_name: str | None = None,
    dry_run: bool = False,
    batch_size: int = 10,
    continue_on_error: bool = True,
) -> dict[str, Any]:
    """
    Import NPM configuration from JSON or YAML data.

    Imports configuration data with support for merge or replace strategies,
    dry-run mode, and error resilience.

    Args:
        ctx: MCP context (auto-injected)
        import_data: Configuration data as dict (optional)
        import_data_json: Configuration data as JSON string (optional)
        import_data_yaml: Configuration data as YAML string (optional)
        strategy: Import strategy (merge|replace) (default: merge)
        instance_name: Target instance name (optional, uses active instance)
        dry_run: Preview changes without executing (default: False)
        batch_size: Number of resources to process concurrently (1-50, default: 10)
        continue_on_error: Continue processing on errors (default: True)

    Returns:
        Dictionary with:
        - success: bool - Tool execution success
        - operation: str - Operation type
        - result: dict - BulkOperationResult with detailed per-item results
        - error: str - Error message (if tool execution fails)

    Example:
        >>> # Import with merge strategy (add/update)
        >>> data = {"proxy_hosts": [{"domain_names": ["app.com"], "forward_host": "localhost"}]}
        >>> result = await import_config(ctx, import_data=data, strategy="merge")

        >>> # Import from JSON string
        >>> json_str = '{"proxy_hosts": [...]}'
        >>> result = await import_config(ctx, import_data_json=json_str, strategy="merge")

        >>> # Import with replace strategy (delete all then import)
        >>> result = await import_config(ctx, import_data=data, strategy="replace")
    """
    server_ctx = get_server_context(ctx)
    server_ctx.logger.info(
        "tool_operation",
        tool="import_config",
        instance=instance_name or "active",
        strategy=strategy,
        dry_run=dry_run,
    )

    try:
        # Validate strategy
        if strategy not in ["merge", "replace"]:
            return {
                "success": False,
                "error": f"Invalid strategy '{strategy}'. Must be 'merge' or 'replace'",
            }

        # Parse import data from provided format
        data = _parse_import_data(import_data, import_data_json, import_data_yaml)
        if "error" in data:
            return {"success": False, "error": data["error"]}

        # Start timing
        start_time = datetime.now(UTC)

        # Get NPM client for the instance
        client = await server_ctx.instance_manager.get_client(instance_name)

        # Map resource types to API endpoints
        resource_endpoints = _get_resource_type_endpoints()

        # Initialize results
        results: list[BulkOperationItemResult] = []
        successful_count = 0
        failed_count = 0

        # Handle dry-run mode
        if dry_run:
            results = _create_import_dry_run_results(data, resource_endpoints)
        else:
            # Process each resource type using helper
            for resource_type_str, resources in data.items():
                if resource_type_str not in resource_endpoints:
                    server_ctx.logger.warning(
                        "import_unsupported_resource_type", resource_type=resource_type_str
                    )
                    continue

                endpoint = resource_endpoints[resource_type_str]
                resource_type = ResourceType(resource_type_str)

                # Ensure resources is a list (type narrowing)
                if not isinstance(resources, list):
                    server_ctx.logger.warning(
                        "import_invalid_resource_format", resource_type=resource_type_str
                    )
                    continue

                type_results, type_success, type_fail = await _import_single_resource_type(
                    client,
                    resource_type,
                    endpoint,
                    resources,
                    batch_size,
                    continue_on_error,
                    strategy,
                    server_ctx.logger,
                    instance_name,
                )

                results.extend(type_results)
                successful_count += type_success
                failed_count += type_fail

        # Calculate duration
        end_time = datetime.now(UTC)
        duration = (end_time - start_time).total_seconds()

        # Determine overall status
        total_items = len(results)
        status = _determine_bulk_status(successful_count, failed_count, total_items)

        # Create BulkOperationResult
        from npm_mcp.models.bulk import BulkOperationResult

        bulk_result_final = BulkOperationResult(
            operation=OperationType.IMPORT_CONFIG,
            status=status,
            total_items=total_items,
            successful=successful_count,
            failed=failed_count,
            dry_run=dry_run,
            results=results,
            duration_seconds=duration,
            instance_name=instance_name,
        )

        # Convert to dict for JSON serialization
        result_dict = bulk_result_final.model_dump()

        server_ctx.logger.info(
            "bulk_operation_complete",
            tool="import_config",
            strategy=strategy,
            total=total_items,
            successful=successful_count,
            failed=failed_count,
            duration=duration,
        )

        return {
            "success": True,
            "operation": OperationType.IMPORT_CONFIG.value,
            "result": result_dict,
        }

    except Exception as e:
        server_ctx.logger.error(
            "tool_error",
            tool="import_config",
            error=str(e),
        )
        return {"success": False, "error": str(e)}


async def _handle_delete_resources_operation(
    ctx: MCPContext,
    resource_type: str | None,
    resource_ids: list[int] | None,
    domain_pattern: str | None,
    instance_name: str | None,
    dry_run: bool,
    batch_size: int,
    continue_on_error: bool,
) -> dict[str, Any]:
    """Handle delete_resources operation with validation."""
    if not resource_type:
        return {
            "success": False,
            "error": "resource_type parameter required for delete_resources operation",
        }
    try:
        rt = ResourceType(resource_type)
    except ValueError:
        return {"success": False, "error": f"Invalid resource_type: {resource_type}"}
    return await delete_resources(
        ctx=ctx,
        resource_type=rt,
        resource_ids=resource_ids,
        domain_pattern=domain_pattern,
        instance_name=instance_name,
        dry_run=dry_run,
        batch_size=batch_size,
        continue_on_error=continue_on_error,
    )


async def _handle_export_config_operation(
    ctx: MCPContext,
    resource_types: list[str] | None,
    resource_ids: list[int] | None,
    format: str,
    instance_name: str | None,
    dry_run: bool,
    continue_on_error: bool,
) -> dict[str, Any]:
    """Handle export_config operation with validation."""
    if not resource_types:
        return {
            "success": False,
            "error": "resource_types parameter required for export_config operation",
        }
    try:
        rt_enums = [ResourceType(rt) for rt in resource_types]
    except ValueError as e:
        return {"success": False, "error": f"Invalid resource_type: {e!s}"}
    return await export_config(
        ctx=ctx,
        resource_types=rt_enums,
        resource_ids=resource_ids,
        format=format,
        instance_name=instance_name,
        dry_run=dry_run,
        continue_on_error=continue_on_error,
    )


def register_bulk_tools(server: Any) -> None:  # noqa: ANN401
    """
    Register bulk operation MCP tools with the FastMCP server.

    Registers the following tools:
    - npm_bulk_operations: Unified tool for all bulk operations (5 operations)

    Args:
        server: FastMCP server instance

    Example:
        >>> from npm_mcp.server import create_mcp_server
        >>> from npm_mcp.tools.bulk import register_bulk_tools
        >>>
        >>> server = create_mcp_server()
        >>> register_bulk_tools(server)
        >>> server.run(transport="stdio")
    """

    # Register unified bulk operations tool (destructive - performs batch modifications)
    @server.tool(annotations=ToolAnnotations(destructiveHint=True))  # type: ignore[untyped-decorator]
    async def npm_bulk_operations(
        ctx: MCPContext,
        operation: str,
        # Renew certificates parameters
        cert_ids: list[int] | None = None,
        expiring_within_days: int | None = None,
        # Toggle hosts parameters
        action: str | None = None,
        host_ids: list[int] | None = None,
        domain_pattern: str | None = None,
        enabled_only: bool | None = None,
        # Delete resources parameters
        resource_type: str | None = None,
        resource_ids: list[int] | None = None,
        # Export config parameters
        resource_types: list[str] | None = None,
        format: str = "json",
        # Import config parameters
        import_data: dict[str, Any] | None = None,
        import_data_json: str | None = None,
        import_data_yaml: str | None = None,
        strategy: str = "merge",
        # Common parameters
        instance_name: str | None = None,
        dry_run: bool = False,
        batch_size: int = 10,
        continue_on_error: bool = True,
    ) -> dict[str, Any]:
        """
        Unified bulk operations tool for Nginx Proxy Manager.

        Supports 5 bulk operations:
        1. renew_certificates: Bulk renewal of SSL/TLS certificates
        2. toggle_hosts: Bulk enable/disable proxy hosts
        3. delete_resources: Bulk deletion of resources
        4. export_config: Export NPM configuration to JSON/YAML
        5. import_config: Import NPM configuration from JSON/YAML

        Args:
            operation: Operation type (renew_certificates|toggle_hosts|
                delete_resources|export_config|import_config)

            # Renew certificates parameters:
            cert_ids: List of certificate IDs to renew (optional)
            expiring_within_days: Renew certificates expiring within N days (optional)

            # Toggle hosts parameters:
            action: Action to perform (enable|disable) (required for toggle_hosts)
            host_ids: List of proxy host IDs to toggle (optional)
            domain_pattern: Filter by domain pattern (substring match) (optional)
            enabled_only: Only toggle enabled hosts (optional)

            # Delete resources parameters:
            resource_type: Type of resource to delete (proxy_hosts, certificates, etc.)
            resource_ids: List of resource IDs to delete (optional)
            domain_pattern: Filter by domain pattern (substring match) (optional)

            # Export config parameters:
            resource_types: List of resource types to export (required for export_config)
            format: Output format (json|yaml) (default: json)

            # Import config parameters:
            import_data: Configuration data as dict (optional)
            import_data_json: Configuration data as JSON string (optional)
            import_data_yaml: Configuration data as YAML string (optional)
            strategy: Import strategy (merge|replace) (default: merge)

            # Common parameters:
            instance_name: Target instance name (optional, uses active instance)
            dry_run: Preview changes without executing (default: False)
            batch_size: Number of items to process concurrently (1-50, default: 10)
            continue_on_error: Continue processing on errors (default: True)

        Returns:
            Dictionary with operation results including success status, bulk result details,
            and export/import data when applicable

        Example:
            >>> # Renew certificates expiring within 30 days
            >>> result = npm_bulk_operations(
            ...     operation="renew_certificates",
            ...     expiring_within_days=30,
            ...     dry_run=True
            ... )

            >>> # Export all configuration
            >>> result = npm_bulk_operations(
            ...     operation="export_config",
            ...     resource_types=["all"],
            ...     format="json"
            ... )
        """
        # Context is injected automatically by FastMCP

        # Route to appropriate operation
        if operation == "renew_certificates":
            return await renew_certificates(
                ctx=ctx,
                cert_ids=cert_ids,
                expiring_within_days=expiring_within_days,
                instance_name=instance_name,
                dry_run=dry_run,
                batch_size=batch_size,
                continue_on_error=continue_on_error,
            )
        if operation == "toggle_hosts":
            if not action:
                return {
                    "success": False,
                    "error": "action parameter required for toggle_hosts operation",
                }
            return await toggle_hosts(
                ctx=ctx,
                action=action,
                host_ids=host_ids,
                domain_pattern=domain_pattern,
                enabled_only=enabled_only,
                instance_name=instance_name,
                dry_run=dry_run,
                batch_size=batch_size,
                continue_on_error=continue_on_error,
            )
        if operation == "delete_resources":
            return await _handle_delete_resources_operation(
                ctx,
                resource_type,
                resource_ids,
                domain_pattern,
                instance_name,
                dry_run,
                batch_size,
                continue_on_error,
            )
        if operation == "export_config":
            return await _handle_export_config_operation(
                ctx, resource_types, resource_ids, format, instance_name, dry_run, continue_on_error
            )
        if operation == "import_config":
            return await import_config(
                ctx=ctx,
                import_data=import_data,
                import_data_json=import_data_json,
                import_data_yaml=import_data_yaml,
                strategy=strategy,
                instance_name=instance_name,
                dry_run=dry_run,
                batch_size=batch_size,
                continue_on_error=continue_on_error,
            )
        return {
            "success": False,
            "error": (
                f"Unknown operation: {operation}. "
                "Must be one of: renew_certificates, toggle_hosts, "
                "delete_resources, export_config, import_config"
            ),
        }
