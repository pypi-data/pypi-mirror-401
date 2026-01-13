"""
API request and response models.

Defines Pydantic models for API input validation and response formatting.
Uses shared input models from core module.
"""

from typing import Any, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

# Import shared models from core
from ..core.input_models import ContentItem, RequestMetadata

# Re-export for convenience
__all__ = [
    "ContentItem",
    "RequestMetadata",
    "EvaluationRequest",
    "EvaluationResponse",
    "FailedItem",
    "HealthResponse",
    "CurriculumsResponse",
    "ErrorResponse",
]


class EvaluationRequest(BaseModel):
    """
    Request model for content evaluation endpoint.
    
    Uses a single array-based format. Each item in the array is evaluated
    independently and in parallel.
    """

    generated_content: list[ContentItem] = Field(
        ...,
        description="Array of content items to evaluate (1-100 items)",
        min_length=1,
        max_length=100
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "generated_content": [
                        {
                            "content": "What is the capital of France?"
                        }
                    ]
                },
                {
                    "generated_content": [
                        {
                            "id": "q1",
                            "curriculum": "common_core",
                            "request": {
                                "grade": "7",
                                "subject": "mathematics",
                                "type": "mcq",
                                "difficulty": "medium",
                                "locale": "en-US",
                                "skills": {
                                    "lesson_title": "Solving Linear Equations",
                                    "substandard_id": "CCSS.MATH.7.EE.A.1",
                                    "substandard_description": "Solve linear equations in one variable"
                                },
                                "instruction": "Create a linear equation problem"
                            },
                            "content": {
                                "question": "What is the value of x in 3x + 7 = 22?",
                                "answer": "C",
                                "answer_explanation": "Subtract 7 from both sides: 3x = 15, then divide by 3: x = 5",
                                "answer_options": [
                                    {"key": "A", "text": "3"},
                                    {"key": "B", "text": "4"},
                                    {"key": "C", "text": "5"},
                                    {"key": "D", "text": "6"}
                                ]
                            }
                        }
                    ]
                },
                {
                    "generated_content": [
                        {
                            "content": "Solve: 2x + 5 = 15",
                            "request": {"grade": "6", "subject": "math"}
                            },
                        {
                            "content": "What is photosynthesis?",
                            "curriculum": "ngss"
                        }
                    ]
                }
            ]
        }
    }


# Response Models

class FailedItem(BaseModel):
    """Information about a failed evaluation item."""
    
    item_id: str = Field(..., description="ID of the failed item")
    error: str = Field(..., description="Error message")


class EvaluationResponse(BaseModel):
    """
    Response model for evaluation endpoints.

    The evaluations dict contains pass-through results from the evaluation
    service. No schema is enforced on individual evaluation results.
    """
    
    request_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique request identifier"
    )
    evaluations: dict[str, Any] = Field(
        ...,
        description="Evaluations keyed by item ID (pass-through from service)"
    )
    evaluation_time_seconds: float = Field(
        ...,
        description="Total evaluation time in seconds"
    )
    inceptbench_version: str = Field(
        ...,
        description="InceptBench version"
    )
    failed_items: Optional[list[FailedItem]] = Field(
        default=None,
        description="Items that failed evaluation (null if all succeeded)"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "request_id": "550e8400-e29b-41d4-a716-446655440000",
                    "evaluations": {
                        "q1": {
                                "content_type": "question",
                                "overall": {
                                    "score": 0.9,
                                "reasoning": "Strong question.",
                                "suggested_improvements": None
                                },
                                "factual_accuracy": {
                                    "score": 1.0,
                                "reasoning": "Accurate.",
                                    "suggested_improvements": None
                                },
                                "weighted_score": 0.8387
                        }
                    },
                    "evaluation_time_seconds": 12.34,
                    "inceptbench_version": "x.y.z",
                    "failed_items": None
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(..., description="Service health status")
    version: str = Field(..., description="API version")
    service: str = Field(..., description="Service name")


class CurriculumsResponse(BaseModel):
    """Response model for curriculum listing endpoint."""
    
    curriculums: list[str] = Field(..., description="Available curriculums")
    default: str = Field(..., description="Default curriculum")


class ErrorResponse(BaseModel):
    """Response model for error responses."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
