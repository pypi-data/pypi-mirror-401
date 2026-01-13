"""
Batch processor for educational content evaluation.

This module provides the BatchProcessor class that handles parallel
evaluation of multiple content items with optional progress tracking.
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from .input_models import ContentItem
from ..utils.failure_tracker import FailureTracker

logger = logging.getLogger(__name__)

# Default max concurrent evaluations (configurable via env var)
DEFAULT_MAX_CONCURRENT = int(os.getenv("MAX_CONCURRENT_EVALUATIONS", "10"))


@dataclass
class FailedItem:
    """Information about a failed evaluation item."""
    item_id: str
    error: str


@dataclass
class BatchResult:
    """Result of batch evaluation."""
    evaluations: dict[str, Any] = field(default_factory=dict)
    failed_items: list[FailedItem] = field(default_factory=list)

    @property
    def success_count(self) -> int:
        """Number of successful evaluations."""
        return len(self.evaluations)

    @property
    def failure_count(self) -> int:
        """Number of failed evaluations."""
        return len(self.failed_items)

    @property
    def total_count(self) -> int:
        """Total number of items processed."""
        return self.success_count + self.failure_count


class BatchProcessor:
    """
    Processor for batch evaluation of content items.

    Handles parallel processing with concurrency control and optional
    progress callbacks for CLI progress bars.
    """

    def __init__(
        self,
        service: Any,  # EvaluationService - using Any to avoid circular import
        max_concurrent: int = DEFAULT_MAX_CONCURRENT
    ):
        """
        Initialize the batch processor.

        Args:
            service: EvaluationService instance
            max_concurrent: Maximum number of concurrent evaluations
        """
        self.service = service
        self.max_concurrent = max_concurrent

    async def process_batch(
        self,
        items: list[ContentItem],
        on_progress: Optional[Callable[[int, int], None]] = None
    ) -> BatchResult:
        """
        Process multiple content items in parallel.

        Args:
            items: List of ContentItem to evaluate
            on_progress: Optional callback(completed, total) called after
                         each item completes. Useful for progress bars.

        Returns:
            BatchResult containing evaluations dict and failed_items list
        """
        if not items:
            return BatchResult()

        total = len(items)
        completed = 0
        lock = asyncio.Lock()

        logger.info(
            f"Processing {total} items (max concurrent: {self.max_concurrent})"
        )

        # Semaphore for concurrency control
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def process_item(
            item: ContentItem
        ) -> tuple[str, Optional[dict], Optional[str]]:
            """Process a single item with semaphore control."""
            nonlocal completed

            async with semaphore:
                try:
                    # Set current content ID for failure tracking
                    FailureTracker.set_current_content(item.id)

                    # Get content as string
                    content_str = item.get_content_string()

                    # Perform evaluation
                    result = await self.service.evaluate(
                        content=content_str,
                        curriculum=item.curriculum,
                        request_metadata=item.request
                    )

                    # Convert result to dict
                    result_dict = result.model_dump()

                    logger.debug(
                        f"Item {item.id} evaluated. "
                        f"Type: {result_dict.get('content_type', 'unknown')}, "
                        f"Score: {result_dict.get('overall', {}).get('score', 0):.2f}"
                    )

                    return (item.id, result_dict, None)

                except Exception as e:
                    logger.error(f"Item {item.id} failed: {e}")
                    # Record as ABORTED - item had unhandled error, couldn't complete
                    FailureTracker.record_aborted(
                        content_id=item.id,
                        error_message=str(e),
                        context={"curriculum": item.curriculum}
                    )
                    return (item.id, None, str(e))

                finally:
                    # Clear content context for failure tracking
                    FailureTracker.set_current_content(None)
                    
                    # Update progress
                    async with lock:
                        completed += 1
                        if on_progress:
                            on_progress(completed, total)

        # Create and run all tasks
        tasks = [process_item(item) for item in items]
        results = await asyncio.gather(*tasks)

        # Build result
        batch_result = BatchResult()
        for item_id, result_dict, error in results:
            if error:
                batch_result.failed_items.append(
                    FailedItem(item_id=item_id, error=error)
                )
            else:
                batch_result.evaluations[item_id] = result_dict

        logger.info(
            f"Batch complete. Success: {batch_result.success_count}, "
            f"Failed: {batch_result.failure_count}"
        )

        return batch_result

    async def process_single(
        self,
        item: ContentItem
    ) -> tuple[dict, Optional[str]]:
        """
        Process a single content item.

        Convenience method for single-item evaluation.

        Args:
            item: ContentItem to evaluate

        Returns:
            Tuple of (result_dict, error_message)
            If successful, error_message is None.
            If failed, result_dict is empty dict.
        """
        result = await self.process_batch([item])

        if result.failed_items:
            return ({}, result.failed_items[0].error)

        return (result.evaluations.get(item.id, {}), None)
