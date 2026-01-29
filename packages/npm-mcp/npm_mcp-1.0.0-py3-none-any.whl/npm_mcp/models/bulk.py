"""
Bulk operation Pydantic models for Nginx Proxy Manager MCP Server.

This module defines models for bulk operations including:
- BulkOperationFilters: Filter criteria for resource selection
- BulkOperationItemResult: Result for individual item in bulk operation
- BulkOperationResult: Complete bulk operation result with all items
- OperationType, ResourceType, ItemStatus: Enums for type safety
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class OperationType(str, Enum):
    """Supported bulk operation types."""

    RENEW_CERTIFICATES = "renew_certificates"
    TOGGLE_HOSTS = "toggle_hosts"
    DELETE_RESOURCES = "delete_resources"
    EXPORT_CONFIG = "export_config"
    IMPORT_CONFIG = "import_config"


class ResourceType(str, Enum):
    """Supported resource types for bulk operations."""

    PROXY_HOSTS = "proxy_hosts"
    CERTIFICATES = "certificates"
    ACCESS_LISTS = "access_lists"
    STREAMS = "streams"
    REDIRECTIONS = "redirections"
    DEAD_HOSTS = "dead_hosts"
    USERS = "users"
    ALL = "all"


class ItemStatus(str, Enum):
    """Status of individual item in bulk operation."""

    SUCCESS = "success"
    ERROR = "error"
    SKIPPED = "skipped"


class BulkOperationFilters(BaseModel):
    """
    Filter criteria for selecting resources in bulk operations.

    Filters allow query-based resource selection instead of explicit ID lists.
    Multiple filters can be combined using AND logic.

    Attributes:
        domain_pattern: Regex pattern for domain name matching
        enabled_only: Only select enabled resources
        expiring_within_days: Select certificates expiring within N days (> 0)
        created_after: ISO 8601 date string, select resources created after this date
        tags: List of tags to match (all must be present)

    Example:
        >>> # Filter staging hosts
        >>> filters = BulkOperationFilters(
        ...     domain_pattern=r".*\\.staging\\..*",
        ...     enabled_only=True
        ... )

        >>> # Filter expiring certificates
        >>> filters = BulkOperationFilters(expiring_within_days=30)

        >>> # Complex filter
        >>> filters = BulkOperationFilters(
        ...     domain_pattern=r"^api\\..*",
        ...     enabled_only=True,
        ...     created_after="2024-01-01T00:00:00Z",
        ...     tags=["production", "critical"]
        ... )
    """

    domain_pattern: str | None = Field(
        default=None,
        description="Regex pattern for domain name matching",
    )
    enabled_only: bool | None = Field(
        default=None,
        description="Only select enabled resources",
    )
    expiring_within_days: int | None = Field(
        default=None,
        description="Select certificates expiring within N days (must be positive)",
        gt=0,
    )
    created_after: str | None = Field(
        default=None,
        description="ISO 8601 date, select resources created after this date",
    )
    tags: list[str] | None = Field(
        default=None,
        description="List of tags to match",
    )

    @field_validator("expiring_within_days")
    @classmethod
    def validate_expiring_within_days(cls, v: int | None) -> int | None:
        """Validate that expiring_within_days is positive."""
        if v is not None and v <= 0:
            msg = "expiring_within_days must be positive"
            raise ValueError(msg)
        return v

    @field_validator("created_after")
    @classmethod
    def validate_created_after(cls, v: str | None) -> str | None:
        """Validate that created_after is a valid ISO 8601 date."""
        if v is not None:
            try:
                # Attempt to parse the date to validate format
                datetime.fromisoformat(v.replace("Z", "+00:00"))
            except (ValueError, AttributeError) as e:
                msg = f"created_after must be a valid ISO 8601 date: {e}"
                raise ValueError(msg) from e
        return v


class BulkOperationItemResult(BaseModel):
    """
    Result for a single item in a bulk operation.

    Represents the outcome of processing one resource in a bulk operation,
    including success, error, or skipped status.

    Attributes:
        resource_id: ID of the resource that was processed
        resource_type: Type of resource (proxy_host, certificate, etc.)
        action: Action performed (enable, disable, renew, delete, etc.)
        status: Outcome status (success, error, skipped)
        details: Additional details about the operation (optional)
        error: Error message if status is ERROR (optional)

    Example:
        >>> # Successful renewal
        >>> result = BulkOperationItemResult(
        ...     resource_id=1,
        ...     resource_type=ResourceType.CERTIFICATE,
        ...     action="renew",
        ...     status=ItemStatus.SUCCESS,
        ...     details={"expires_on": "2026-01-15T00:00:00Z"}
        ... )

        >>> # Failed operation
        >>> result = BulkOperationItemResult(
        ...     resource_id=2,
        ...     resource_type=ResourceType.CERTIFICATE,
        ...     action="renew",
        ...     status=ItemStatus.ERROR,
        ...     error="DNS validation failed"
        ... )
    """

    resource_id: int = Field(
        description="ID of the resource that was processed",
    )
    resource_type: ResourceType = Field(
        description="Type of resource (proxy_host, certificate, etc.)",
    )
    action: str = Field(
        description="Action performed (enable, disable, renew, delete, etc.)",
    )
    status: ItemStatus = Field(
        description="Outcome status (success, error, skipped)",
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Additional details about the operation",
    )
    error: str | None = Field(
        default=None,
        description="Error message if status is ERROR",
    )


class BulkOperationResult(BaseModel):
    """
    Complete result of a bulk operation.

    Contains summary statistics and detailed per-item results for a bulk operation.
    Includes validation to ensure counts match actual results.

    Attributes:
        operation: Type of bulk operation performed
        status: Overall operation status (completed, failed, etc.)
        total_items: Total number of items processed
        successful: Number of items that succeeded
        failed: Number of items that failed
        dry_run: Whether this was a dry-run (preview only)
        results: List of per-item results
        duration_seconds: Time taken to complete operation
        instance_name: NPM instance name (optional)

    Example:
        >>> results = [
        ...     BulkOperationItemResult(
        ...         resource_id=1,
        ...         resource_type=ResourceType.CERTIFICATE,
        ...         action="renew",
        ...         status=ItemStatus.SUCCESS,
        ...     ),
        ...     BulkOperationItemResult(
        ...         resource_id=2,
        ...         resource_type=ResourceType.CERTIFICATE,
        ...         action="renew",
        ...         status=ItemStatus.ERROR,
        ...         error="Failed",
        ...     ),
        ... ]
        >>> bulk_result = BulkOperationResult(
        ...     operation=OperationType.RENEW_CERTIFICATES,
        ...     status="completed",
        ...     total_items=2,
        ...     successful=1,
        ...     failed=1,
        ...     dry_run=False,
        ...     results=results,
        ...     duration_seconds=5.3,
        ... )
    """

    operation: OperationType = Field(
        description="Type of bulk operation performed",
    )
    status: str = Field(
        description="Overall operation status (completed, failed, etc.)",
    )
    total_items: int = Field(
        description="Total number of items processed",
        ge=0,
    )
    successful: int = Field(
        description="Number of items that succeeded",
        ge=0,
    )
    failed: int = Field(
        description="Number of items that failed",
        ge=0,
    )
    dry_run: bool = Field(
        description="Whether this was a dry-run (preview only)",
    )
    results: list[BulkOperationItemResult] = Field(
        description="List of per-item results",
    )
    duration_seconds: float = Field(
        description="Time taken to complete operation",
        ge=0.0,
    )
    instance_name: str | None = Field(
        default=None,
        description="NPM instance name",
    )

    @field_validator("duration_seconds")
    @classmethod
    def validate_duration(cls, v: float) -> float:
        """Validate that duration is non-negative."""
        if v < 0:
            msg = "duration_seconds must be non-negative"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_counts(self) -> "BulkOperationResult":
        """
        Validate that counts match the actual results.

        Ensures:
        - total_items matches length of results list
        - successful count matches number of SUCCESS items
        - failed count matches number of ERROR items
        """
        # Validate total_items
        if self.total_items != len(self.results):
            msg = (
                f"total_items ({self.total_items}) must match "
                f"length of results list ({len(self.results)})"
            )
            raise ValueError(msg)

        # Count actual successes and failures
        actual_successful = sum(1 for item in self.results if item.status == ItemStatus.SUCCESS)
        actual_failed = sum(1 for item in self.results if item.status == ItemStatus.ERROR)

        # Validate successful count
        if self.successful != actual_successful:
            msg = (
                f"successful count ({self.successful}) does not match "
                f"actual SUCCESS items ({actual_successful})"
            )
            raise ValueError(msg)

        # Validate failed count
        if self.failed != actual_failed:
            msg = (
                f"failed count ({self.failed}) does not match actual ERROR items ({actual_failed})"
            )
            raise ValueError(msg)

        return self
