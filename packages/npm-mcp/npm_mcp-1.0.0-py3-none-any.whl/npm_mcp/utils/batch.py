"""
Batch processing utility for bulk operations.

Provides concurrent batch processing with configurable batch sizes,
error resilience, dry-run simulation, and progress tracking.
"""

import asyncio
import time
from collections.abc import Awaitable, Callable
from typing import Any

from pydantic import BaseModel, Field, field_validator

from npm_mcp.models.bulk import (
    BulkOperationItemResult,
    BulkOperationResult,
    ItemStatus,
    OperationType,
    ResourceType,
)

# Constants
MAX_BATCH_SIZE = 50
MIN_BATCH_SIZE = 1


class BatchProcessorConfig(BaseModel):
    """
    Configuration for batch processor.

    Attributes:
        batch_size: Number of items to process concurrently (1-50)
        continue_on_error: Continue processing on errors (default: True)
        dry_run: Preview changes without executing (default: False)

    Example:
        >>> config = BatchProcessorConfig(batch_size=10, continue_on_error=True)
        >>> config.batch_size
        10
    """

    batch_size: int = Field(
        default=10,
        description=f"Number of items to process concurrently ({MIN_BATCH_SIZE}-{MAX_BATCH_SIZE})",
        ge=MIN_BATCH_SIZE,
        le=MAX_BATCH_SIZE,
    )
    continue_on_error: bool = Field(
        default=True,
        description="Continue processing on errors",
    )
    dry_run: bool = Field(
        default=False,
        description="Preview changes without executing",
    )

    @field_validator("batch_size")
    @classmethod
    def validate_batch_size(cls, v: int) -> int:
        """Validate that batch_size is within allowed range."""
        if v < MIN_BATCH_SIZE or v > MAX_BATCH_SIZE:
            msg = f"batch_size must be between {MIN_BATCH_SIZE} and {MAX_BATCH_SIZE}"
            raise ValueError(msg)
        return v


class BatchProcessor:
    """
    Batch processor for concurrent bulk operations.

    Processes items in configurable batch sizes using asyncio.gather(),
    with error resilience, dry-run simulation, and progress tracking.

    Example:
        >>> config = BatchProcessorConfig(batch_size=10)
        >>> processor = BatchProcessor(config=config)
        >>> results = await processor.process_batch(
        ...     items=[{"id": 1}, {"id": 2}],
        ...     process_fn=my_async_function,
        ...     operation_type=OperationType.TOGGLE_HOSTS
        ... )
    """

    def __init__(self, config: BatchProcessorConfig) -> None:
        """
        Initialize batch processor.

        Args:
            config: Batch processor configuration
        """
        self.config = config

    async def process_batch(
        self,
        items: list[dict[str, Any]],
        process_fn: Callable[[dict[str, Any]], Awaitable[BulkOperationItemResult]],
        operation_type: OperationType,
        instance_name: str | None = None,
    ) -> BulkOperationResult:
        """
        Process items in batches concurrently.

        Args:
            items: List of items to process
            process_fn: Async function to process each item
            operation_type: Type of bulk operation
            instance_name: Optional NPM instance name

        Returns:
            BulkOperationResult with detailed per-item results

        Raises:
            Exception: If continue_on_error=False and an error occurs
        """
        start_time = time.time()
        results: list[BulkOperationItemResult] = []

        # Handle empty items list
        if not items:
            return BulkOperationResult(
                operation=operation_type,
                status="completed",
                total_items=0,
                successful=0,
                failed=0,
                dry_run=self.config.dry_run,
                results=[],
                duration_seconds=0.0,
                instance_name=instance_name,
            )

        # Handle dry-run mode
        if self.config.dry_run:
            results = self._simulate_dry_run(items)
        else:
            # Process items in batches
            results = await self._process_items_in_batches(items, process_fn)

        # Calculate duration
        duration_seconds = time.time() - start_time

        # Aggregate results
        successful = sum(1 for r in results if r.status == ItemStatus.SUCCESS)
        failed = sum(1 for r in results if r.status == ItemStatus.ERROR)

        return BulkOperationResult(
            operation=operation_type,
            status="completed" if failed == 0 else "partial",
            total_items=len(items),
            successful=successful,
            failed=failed,
            dry_run=self.config.dry_run,
            results=results,
            duration_seconds=duration_seconds,
            instance_name=instance_name,
        )

    async def _process_items_in_batches(
        self,
        items: list[dict[str, Any]],
        process_fn: Callable[[dict[str, Any]], Awaitable[BulkOperationItemResult]],
    ) -> list[BulkOperationItemResult]:
        """
        Process items in batches using asyncio.gather().

        Args:
            items: List of items to process
            process_fn: Async function to process each item

        Returns:
            List of BulkOperationItemResult for all items

        Raises:
            Exception: If continue_on_error=False and an error occurs
        """
        all_results: list[BulkOperationItemResult] = []

        # Process items in batches of batch_size
        for batch_start in range(0, len(items), self.config.batch_size):
            batch_end = min(batch_start + self.config.batch_size, len(items))
            batch_items = items[batch_start:batch_end]

            # Process batch concurrently
            batch_results = await self._process_batch_concurrent(batch_items, process_fn)
            all_results.extend(batch_results)

        return all_results

    async def _process_batch_concurrent(
        self,
        batch_items: list[dict[str, Any]],
        process_fn: Callable[[dict[str, Any]], Awaitable[BulkOperationItemResult]],
    ) -> list[BulkOperationItemResult]:
        """
        Process a single batch of items concurrently.

        Args:
            batch_items: Items in this batch
            process_fn: Async function to process each item

        Returns:
            List of results for this batch

        Raises:
            Exception: If continue_on_error=False and an error occurs
        """
        if self.config.continue_on_error:
            # Create tasks for all items
            tasks = [self._process_item_safe(item, process_fn) for item in batch_items]
            # Execute concurrently
            return await asyncio.gather(*tasks)
        # Fail fast mode - don't catch exceptions
        tasks = [process_fn(item) for item in batch_items]  # type: ignore[misc]
        return await asyncio.gather(*tasks)

    async def _process_item_safe(
        self,
        item: dict[str, Any],
        process_fn: Callable[[dict[str, Any]], Awaitable[BulkOperationItemResult]],
    ) -> BulkOperationItemResult:
        """
        Process a single item with error handling.

        Args:
            item: Item to process
            process_fn: Async function to process the item

        Returns:
            BulkOperationItemResult (success or error)
        """
        try:
            return await process_fn(item)
        except Exception as e:
            # Extract resource_id from item if available
            resource_id = item.get("id", 0)

            # Create error result with minimal required fields
            return BulkOperationItemResult(
                resource_id=resource_id,
                resource_type=ResourceType.PROXY_HOSTS,  # Default type
                action="process",
                status=ItemStatus.ERROR,
                error=str(e),
            )

    def _simulate_dry_run(self, items: list[dict[str, Any]]) -> list[BulkOperationItemResult]:
        """
        Simulate dry-run mode by creating SKIPPED results.

        Args:
            items: Items to simulate

        Returns:
            List of SKIPPED results for all items
        """
        results: list[BulkOperationItemResult] = []

        for item in items:
            resource_id = item.get("id", 0)
            result = BulkOperationItemResult(
                resource_id=resource_id,
                resource_type=ResourceType.PROXY_HOSTS,  # Default type for dry-run
                action="preview",
                status=ItemStatus.SKIPPED,
                details={"dry_run": True, "item": item},
            )
            results.append(result)

        return results
