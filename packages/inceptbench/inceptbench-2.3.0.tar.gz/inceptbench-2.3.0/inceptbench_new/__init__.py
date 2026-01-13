"""
InceptBench - Educational Content Evaluator.

A comprehensive system for evaluating educational content using LLM-based analysis.
Supports hierarchical content evaluation, curriculum alignment, and multi-modal assessment.

Usage:
    # Programmatic
    from inceptbench_new import EvaluationService
    
    service = EvaluationService()
    result = await service.evaluate("What is 2+2?", curriculum="common_core")
    
    # CLI
    python -m inceptbench_new evaluate content.json
    
    # API
    uvicorn inceptbench_new.api.main:app

See README.md for full documentation.
"""

__version__ = "2.3.0"

# Main service
from .service import EvaluationService

# Core models for building input
from .core.input_models import ContentItem, RequestMetadata

# Batch processor for custom integrations
from .core.processor import BatchProcessor, BatchResult, FailedItem

__all__ = [
    # Version
    "__version__",
    # Main service
    "EvaluationService",
    # Input models
    "ContentItem",
    "RequestMetadata",
    # Batch processing
    "BatchProcessor",
    "BatchResult",
    "FailedItem",
]
