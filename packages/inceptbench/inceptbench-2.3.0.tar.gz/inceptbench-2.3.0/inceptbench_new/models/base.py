"""
Base models for educational content evaluation.

This module defines the core Pydantic models used across all evaluators,
including metric results, evaluation results, and content types.
"""

from abc import ABC
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_serializer

from inceptbench_new.config.tier_scoring import calculate_weighted_score


class ContentType(str, Enum):
    """Types of educational content that can be evaluated."""
    QUESTION = "question"
    QUIZ = "quiz"
    FICTION_READING = "fiction_reading"
    NONFICTION_READING = "nonfiction_reading"
    ARTICLE = "article"
    OTHER = "other"


class OverallRating(str, Enum):
    """
    Qualitative rating corresponding to the overall assessment score.
    
    Thresholds:
    - SUPERIOR: score >= 0.99 (exceeds typical high-quality content)
    - ACCEPTABLE: score >= 0.85 and < 0.99 (comparable to typical high-quality content)
    - INFERIOR: score < 0.85 (falls short of expected quality)
    """
    SUPERIOR = "SUPERIOR"
    ACCEPTABLE = "ACCEPTABLE"
    INFERIOR = "INFERIOR"


class MetricResult(BaseModel):
    """
    Result for a single evaluation metric.
    
    Attributes:
        score: Float in [0.0, 1.0]. Binary metrics are 0.0 or 1.0.
               Only 'overall' can have intermediate values.
        internal_reasoning: Detailed step-by-step analysis for consistency (not for human readers).
        reasoning: Clean, human-readable explanation for the score given.
        suggested_improvements: Suggestions for improvement (null if score = 1.0).
    """
    score: float = Field(..., ge=0.0, le=1.0, description="Score between 0.0 and 1.0")
    internal_reasoning: Optional[str] = Field(
        None,
        description="Detailed step-by-step analysis (internal use, helps ensure consistency)"
    )
    reasoning: str = Field(..., min_length=1, description="Clean, human-readable explanation for the score")
    suggested_improvements: Optional[str] = Field(
        None, 
        description="Suggestions for improvement (provide if score < 1.0, null if score = 1.0)"
    )
    
    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class BaseEvaluationResult(BaseModel, ABC):
    """
    Abstract base class for all evaluation results.
    
    All evaluation results must include:
    - content_type: Type of content evaluated
    - overall: Overall assessment (continuous metric)
    - factual_accuracy: Factual correctness (binary)
    - educational_accuracy: Educational intent fulfillment (binary)
    - localization_quality: Cultural/linguistic appropriateness (binary)

    Subclasses add content-type-specific metrics.
    """
    
    model_config = ConfigDict(
        # Serialize using actual runtime type, not annotated type
        # This ensures subcontent_evaluations include all subclass fields
        use_enum_values=True,
    )
    
    content_type: str = Field(..., description="Type of content evaluated")
    overall: MetricResult = Field(..., description="Overall assessment (continuous)")
    factual_accuracy: MetricResult = Field(
        ..., 
        description="Factual correctness (binary)"
    )
    educational_accuracy: MetricResult = Field(
        ..., 
        description="Educational intent fulfillment (binary)"
    )
    localization_quality: MetricResult = Field(
        ...,
        description="Cultural and linguistic appropriateness for target audience (binary)"
    )

    # Hierarchical content support
    subcontent_evaluations: Optional[List['BaseEvaluationResult']] = Field(
        None,
        description="Evaluation results for nested content (e.g., questions within a quiz)"
    )

    @field_validator('factual_accuracy', 'educational_accuracy', 'localization_quality')
    @classmethod
    def validate_binary_metric(cls, v: MetricResult) -> MetricResult:
        """Ensure binary metrics have scores of exactly 0.0 or 1.0."""
        if v.score not in (0.0, 1.0):
            raise ValueError(
                f"Binary metrics must have score of 0.0 or 1.0, got {v.score}"
            )
        return v
    
    @model_serializer(mode='wrap')
    def _serialize_model(self, serializer: Any) -> dict:
        """
        Custom serializer to control field ordering in output.
        
        Output order:
        1. content_type
        2. overall_rating (qualitative rating)
        3. overall (detailed assessment)
        4. All other metrics (in their defined order)
        5. subcontent_evaluations (at the end, if present)
        """
        # Get default serialization
        data = serializer(self)
        
        # Build reordered output
        ordered = {}
        
        # 1. content_type first
        if 'content_type' in data:
            ordered['content_type'] = data.pop('content_type')
        
        # 2. overall_rating second
        if 'overall_rating' in data:
            ordered['overall_rating'] = data.pop('overall_rating')
        
        # 3. overall third
        if 'overall' in data:
            ordered['overall'] = data.pop('overall')
        
        # 4. Remove subcontent_evaluations temporarily to add at the end
        subcontent = data.pop('subcontent_evaluations', None)
        
        # 5. Add all remaining metrics (except weighted_score which we skip)
        for key, value in data.items():
            if key != 'weighted_score':  # Skip weighted_score - it's confusing
                ordered[key] = value
        
        # 6. Add subcontent_evaluations at the end
        if subcontent is not None:
            # Serialize each subcontent item with all its fields
            subcontent_serialized = [
                item.model_dump(mode='python') if hasattr(item, 'model_dump')
                else item
                for item in self.subcontent_evaluations
            ] if self.subcontent_evaluations else None
            ordered['subcontent_evaluations'] = subcontent_serialized
        else:
            ordered['subcontent_evaluations'] = None
        
        return ordered
    
    def _get_metric_scores(self) -> Dict[str, float]:
        """Extract all metric scores from this result."""
        scores = {}
        for field_name in type(self).model_fields:
            if field_name in ('content_type', 'subcontent_evaluations', 'overall'):
                continue
            value = getattr(self, field_name, None)
            if isinstance(value, MetricResult):
                scores[field_name] = value.score
        return scores

    @computed_field
    @property
    def weighted_score(self) -> float:
        """
        Tier-weighted score based on metric importance.

        Critical metrics (factual_accuracy, educational_accuracy) are weighted 2x.
        Important metrics (curriculum_alignment, clarity, etc.) are weighted 1.5x.
        Enhancement metrics (localization, engagement, etc.) are weighted 1x.
        """
        scores = self._get_metric_scores()
        result = calculate_weighted_score(scores)
        return round(result, 4) if result is not None else 0.0

    @computed_field
    @property
    def overall_rating(self) -> OverallRating:
        """
        Qualitative rating derived from the overall assessment score.
        
        Returns:
            OverallRating.SUPERIOR if score >= 0.99
            OverallRating.ACCEPTABLE if score >= 0.85 and < 0.99
            OverallRating.INFERIOR if score < 0.85
        """
        score = self.overall.score
        if score >= 0.99:
            return OverallRating.SUPERIOR
        elif score >= 0.85:
            return OverallRating.ACCEPTABLE
        else:
            return OverallRating.INFERIOR

    def to_json(self) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(indent=2)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return self.model_dump()


class EvaluationRequest(BaseModel):
    """
    Request model for content evaluation.
    
    Attributes:
        content: The educational content to evaluate (any string, may contain image URLs)
        curriculum: Curriculum to use for evaluation (defaults to "common_core")
        generation_prompt: Optional prompt used to generate the content (for AI-generated content)
    """
    content: str = Field(..., min_length=1, description="Content to evaluate")
    curriculum: str = Field(
        "common_core", 
        description="Curriculum for evaluation"
    )
    generation_prompt: Optional[str] = Field(
        None,
        description="Optional prompt used to generate the content (useful for evaluating AI-generated content)"
    )
    
    @field_validator('content')
    @classmethod
    def validate_content_not_empty(cls, v: str) -> str:
        """Ensure content is not just whitespace."""
        if not v.strip():
            raise ValueError("Content cannot be empty or just whitespace")
        return v

