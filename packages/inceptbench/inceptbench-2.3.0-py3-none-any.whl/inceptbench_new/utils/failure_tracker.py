"""
Failure tracking utility for inceptbench_new.

This module provides a centralized way to track and categorize failures that occur
during evaluation. It distinguishes between four types of failures:

1. CRASHED - A catastrophic failure that stopped the entire evaluation process.
            No more items could be evaluated after this point.

2. ABORTED - An item had an unhandled error that prevented retrying that item,
            but other items could continue being evaluated.

3. EXHAUSTED - An operation's retry loop ran all attempts but all failed.
              The item may still have a partial result or no result.

4. RECOVERED - An operation had transient failures but eventually succeeded on retry.
              The item has a valid result.

Request Isolation:
    The FailureTracker uses contextvars for request-isolated storage. Each async
    context (e.g., each web request) gets its own isolated failure log. This prevents
    one request from seeing or clearing another request's failure data.

Usage:
    from inceptbench_new.utils.failure_tracker import FailureTracker, FailureCategory
    
    # Initialize tracker for this request context
    FailureTracker.init_context()
    
    # Record different types of failures
    FailureTracker.record_exhausted("gemini_adapter", "Timeout after 3 retries", {...})
    FailureTracker.record_recovered("openai_adapter", "Succeeded on attempt 2/3", {...})
    FailureTracker.record_aborted("item_123", "KeyError in classifier", {...})
    FailureTracker.record_crashed("OutOfMemoryError", ["item_5", "item_6", ...])
    
    # Get categorized summary
    summary = FailureTracker.get_summary()
    
    # Clear at end of request (optional, context cleanup handles this)
    FailureTracker.clear()
"""

import contextvars
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# =============================================================================
# Context Variables for Request Isolation
# =============================================================================
# Each async context (web request, CLI invocation) gets its own isolated storage.
# This prevents concurrent requests from interfering with each other's failure logs.

# Current content ID being evaluated (for associating failures with content items)
_current_content_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar(
    'current_content_id', default=None
)

# Failure records for the current context
_failures_var: contextvars.ContextVar[List["FailureRecord"]] = contextvars.ContextVar(
    'failures', default=None  # type: ignore  # Will be initialized via init_context()
)

# Crash record for the current context
_crash_var: contextvars.ContextVar[Optional["CrashRecord"]] = contextvars.ContextVar(
    'crash', default=None
)


class FailureCategory(str, Enum):
    """Categories of failures during evaluation."""
    CRASHED = "crashed"      # Process halted, remaining items not evaluated
    ABORTED = "aborted"      # Item had unhandled error, couldn't retry
    EXHAUSTED = "exhausted"  # All retry attempts failed
    RECOVERED = "recovered"  # Succeeded after retry (for informational purposes)


@dataclass
class AttemptError:
    """Record of a single retry attempt error."""
    attempt: int  # 1-indexed attempt number
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "attempt": self.attempt,
            "error": self.error_message[:500] if len(self.error_message) > 500 else self.error_message,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class FailureRecord:
    """Record of a single failure or recovery."""
    category: FailureCategory
    component: str  # Which component (e.g., "gemini_adapter", "classifier")
    error_message: str  # The final error message or recovery info
    timestamp: datetime = field(default_factory=datetime.now)
    context: Optional[Dict[str, Any]] = None  # Additional context
    attempt_errors: Optional[List[AttemptError]] = None  # All errors from retry attempts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "category": self.category.value,
            "component": self.component,
            "error": self.error_message,
            "timestamp": self.timestamp.isoformat()
        }
        if self.context:
            # Truncate context values to avoid huge outputs
            truncated_context = {}
            for key, value in self.context.items():
                if isinstance(value, str) and len(value) > 200:
                    truncated_context[key] = value[:200] + "..."
                else:
                    truncated_context[key] = value
            result["context"] = truncated_context
        if self.attempt_errors:
            result["attempt_errors"] = [ae.to_dict() for ae in self.attempt_errors]
        return result


@dataclass
class CrashRecord:
    """Record of a process-level crash."""
    error_message: str
    timestamp: datetime = field(default_factory=datetime.now)
    items_not_evaluated: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "category": FailureCategory.CRASHED.value,
            "error": self.error_message,
            "timestamp": self.timestamp.isoformat(),
            "items_not_evaluated": self.items_not_evaluated,
            "items_not_evaluated_count": len(self.items_not_evaluated)
        }


class FailureTracker:
    """
    Request-isolated tracker for failures across the evaluation pipeline.
    
    Uses contextvars for storage, ensuring each async context (web request,
    CLI invocation) has its own isolated failure logs. This prevents one
    request from seeing or clearing another request's data.
    
    Tracks four categories of failures:
    - CRASHED: Process stopped, remaining items not evaluated
    - ABORTED: Item failed with unhandled error, no retries possible
    - EXHAUSTED: All retry attempts failed for an operation
    - RECOVERED: Operation succeeded after retry (informational)
    
    Usage:
        # At start of request/evaluation:
        FailureTracker.init_context()
        
        # During evaluation:
        FailureTracker.set_current_content("item_123")
        FailureTracker.record_exhausted(...)
        
        # At end of request:
        summary = FailureTracker.get_summary()
        FailureTracker.clear()  # Optional, context cleanup handles this
    """
    
    @classmethod
    def init_context(cls) -> None:
        """
        Initialize the failure tracker for the current async context.
        
        Call this at the start of each request/evaluation to ensure
        the context has its own isolated failure storage.
        """
        _failures_var.set([])
        _crash_var.set(None)
        _current_content_id_var.set(None)
    
    @classmethod
    def _get_failures(cls) -> List[FailureRecord]:
        """Get the failures list for the current context, initializing if needed."""
        failures = _failures_var.get()
        if failures is None:
            # Auto-initialize if not explicitly initialized
            failures = []
            _failures_var.set(failures)
        return failures
    
    @classmethod
    def _get_crash(cls) -> Optional[CrashRecord]:
        """Get the crash record for the current context."""
        return _crash_var.get()
    
    @classmethod
    def set_current_content(cls, content_id: Optional[str]) -> None:
        """
        Set the current content being evaluated for this async context.
        
        All failures recorded after this call will include this content_id
        until it's changed or cleared. Uses contextvars for async-safety,
        so each concurrent task gets its own content_id.
        """
        _current_content_id_var.set(content_id)
    
    @classmethod
    def get_current_content(cls) -> Optional[str]:
        """Get the current content ID for this async context."""
        return _current_content_id_var.get()
    
    @classmethod
    def _add_content_to_context(cls, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Add current content ID to context dict."""
        full_context = context.copy() if context else {}
        current_content_id = _current_content_id_var.get()
        if current_content_id:
            full_context["content_id"] = current_content_id
        return full_context
    
    @classmethod
    def record_crashed(
        cls,
        error_message: str,
        items_not_evaluated: Optional[List[str]] = None
    ) -> None:
        """
        Record a process-level crash that stopped all evaluation.
        
        Args:
            error_message: Description of what crashed
            items_not_evaluated: List of item IDs that couldn't be evaluated
        """
        crash = CrashRecord(
            error_message=str(error_message)[:500],
            items_not_evaluated=items_not_evaluated or []
        )
        _crash_var.set(crash)
        logger.error(f"CRASHED: {error_message[:200]}")
    
    @classmethod
    def record_aborted(
        cls,
        content_id: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Record an item that was aborted due to an unhandled error.
        
        Args:
            content_id: ID of the content item that was aborted
            error_message: The error message
            context: Optional additional context
        """
        full_context = context.copy() if context else {}
        full_context["content_id"] = content_id
        
        record = FailureRecord(
            category=FailureCategory.ABORTED,
            component="evaluation",
            error_message=str(error_message)[:500],
            context=full_context
        )
        cls._get_failures().append(record)
        logger.warning(f"ABORTED [{content_id}]: {error_message[:100]}...")
    
    @classmethod
    def record_exhausted(
        cls,
        component: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None,
        attempt_errors: Optional[List[AttemptError]] = None
    ) -> None:
        """
        Record an operation where all retry attempts failed.
        
        Args:
            component: Name of the component (e.g., "gemini_adapter.generate_with_vision")
            error_message: The last error message
            context: Optional additional context (attempts, model, etc.)
            attempt_errors: Optional list of errors from each retry attempt
        """
        full_context = cls._add_content_to_context(context)
        current_content_id = _current_content_id_var.get()
        
        record = FailureRecord(
            category=FailureCategory.EXHAUSTED,
            component=component,
            error_message=str(error_message)[:500],
            context=full_context if full_context else None,
            attempt_errors=attempt_errors
        )
        cls._get_failures().append(record)
        content_info = f" [{current_content_id}]" if current_content_id else ""
        logger.warning(f"EXHAUSTED{content_info} in {component}: {error_message[:100]}...")
    
    @classmethod
    def record_recovered(
        cls,
        component: str,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        attempt_errors: Optional[List[AttemptError]] = None
    ) -> None:
        """
        Record an operation that succeeded after retry.
        
        Args:
            component: Name of the component
            message: Recovery info (e.g., "Succeeded on attempt 2/3")
            context: Optional additional context
            attempt_errors: Optional list of errors from failed attempts before recovery
        """
        full_context = cls._add_content_to_context(context)
        current_content_id = _current_content_id_var.get()
        
        record = FailureRecord(
            category=FailureCategory.RECOVERED,
            component=component,
            error_message=message,
            context=full_context if full_context else None,
            attempt_errors=attempt_errors
        )
        cls._get_failures().append(record)
        content_info = f" [{current_content_id}]" if current_content_id else ""
        logger.debug(f"RECOVERED{content_info} in {component}: {message}")
    
    @classmethod
    def record(
        cls,
        component: str,
        error_message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Legacy method - records as EXHAUSTED for backwards compatibility.
        
        Use record_exhausted(), record_recovered(), etc. for explicit categorization.
        """
        cls.record_exhausted(component, error_message, context)
    
    @classmethod
    def get_failures_by_category(cls, category: FailureCategory) -> List[Dict[str, Any]]:
        """Get all failures of a specific category."""
        return [f.to_dict() for f in cls._get_failures() if f.category == category]
    
    @classmethod
    def has_failures(cls) -> bool:
        """Check if any failures (excluding RECOVERED) have been recorded."""
        if cls._get_crash():
            return True
        return any(f.category != FailureCategory.RECOVERED for f in cls._get_failures())
    
    @classmethod
    def has_any_issues(cls) -> bool:
        """Check if any issues (including RECOVERED) have been recorded."""
        return cls._get_crash() is not None or len(cls._get_failures()) > 0
    
    @classmethod
    def clear(cls) -> None:
        """
        Clear all recorded failures for the current context.
        
        Call at the start of each evaluation to reset state.
        This only affects the current async context's data.
        """
        _failures_var.set([])
        _crash_var.set(None)
        # Note: Don't reset the content_id contextvar here as it may be
        # set/cleared independently by the code that calls set_current_content()
    
    @classmethod
    def get_summary(cls) -> Optional[Dict[str, Any]]:
        """
        Get a categorized summary of all failures and recoveries.
        
        Returns:
            None if no issues, otherwise a dict with categorized failures
        """
        failures = cls._get_failures()
        crash = cls._get_crash()
        
        if not failures and not crash:
            return None
        
        # Categorize failures
        crashed = crash.to_dict() if crash else None
        aborted = [f.to_dict() for f in failures 
                   if f.category == FailureCategory.ABORTED]
        exhausted = [f.to_dict() for f in failures 
                     if f.category == FailureCategory.EXHAUSTED]
        recovered = [f.to_dict() for f in failures 
                     if f.category == FailureCategory.RECOVERED]
        
        # Count by component for exhausted failures
        exhausted_by_component: Dict[str, int] = {}
        for f in failures:
            if f.category == FailureCategory.EXHAUSTED:
                exhausted_by_component[f.component] = \
                    exhausted_by_component.get(f.component, 0) + 1
        
        return {
            "crashed": crashed,
            "aborted": aborted,
            "aborted_count": len(aborted),
            "exhausted": exhausted,
            "exhausted_count": len(exhausted),
            "exhausted_by_component": exhausted_by_component,
            "recovered": recovered,
            "recovered_count": len(recovered)
        }
