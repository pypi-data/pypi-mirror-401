"""
Shared input models for InceptBench.

These models are used by both the API and CLI interfaces for input validation
and normalization before passing to the EvaluationService.
"""

import json
from typing import Any, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field, model_validator


class RequestMetadata(BaseModel):
    """
    Optional metadata about content generation request.

    All fields are optional. This metadata provides context about the
    intended purpose and requirements of the content.
    """

    grade: Optional[str] = Field(
        default=None,
        description="Grade level (e.g., '7', 'K', '12')"
    )
    subject: Optional[str] = Field(
        default=None,
        description="Subject area (e.g., 'mathematics', 'english')"
    )
    type: Optional[str] = Field(
        default=None,
        description="Content type (e.g., 'mcq', 'fill-in', 'article')"
    )
    difficulty: Optional[str] = Field(
        default=None,
        description="Difficulty level (e.g., 'easy', 'medium', 'hard')"
    )
    locale: Optional[str] = Field(
        default=None,
        description="Locale/language code (e.g., 'en-US', 'es-MX')"
    )
    skills: Optional[Union[dict, str]] = Field(
        default=None,
        description="Skills information (JSON object or string)"
    )
    instructions: Optional[str] = Field(
        default=None,
        description="Instructions/prompt used to generate the content"
    )

    model_config = {
        "extra": "allow"  # Allow additional fields for flexibility
    }

    def to_generation_prompt(self) -> Optional[str]:
        """
        Convert request metadata to a string for use as generation_prompt.

        Returns:
            JSON string of non-None fields, or None if all fields are None
        """
        data = self.model_dump(exclude_none=True)
        if not data:
            return None
        return json.dumps(data, indent=2)


class ContentItem(BaseModel):
    """
    Single content item for evaluation.

    The content field accepts any format - string, JSON object, or list.
    This flexibility allows the API/CLI to handle various content structures
    without imposing a rigid schema.
    """

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier. Auto-generated if not provided."
    )
    curriculum: str = Field(
        default="common_core",
        description="Curriculum to use for evaluation"
    )
    request: Optional[RequestMetadata] = Field(
        default=None,
        description="Optional metadata about the content generation request"
    )
    content: Any = Field(
        ...,
        description="Content to evaluate. Can be string, JSON object, etc."
    )

    @model_validator(mode='after')
    def validate_and_set_defaults(self) -> 'ContentItem':
        """Validate content is provided and generate ID if not provided."""
        # Validate content is not None or empty
        if self.content is None:
            raise ValueError("content is required")

        # Check for empty string
        if isinstance(self.content, str) and not self.content.strip():
            raise ValueError("content cannot be empty or just whitespace")

        # Check for empty dict/list
        if isinstance(self.content, (dict, list)) and len(self.content) == 0:
            raise ValueError("content cannot be empty")

        # Generate ID if not provided
        if self.id is None:
            self.id = str(uuid4())

        return self

    def get_content_string(self) -> str:
        """
        Convert content to string format for evaluation.

        Returns:
            String representation of content (JSON-serialized if dict/list)
        """
        if isinstance(self.content, str):
            return self.content
        return json.dumps(self.content, indent=2)

    def get_generation_prompt(self) -> Optional[str]:
        """
        Get generation prompt from request metadata.

        Returns:
            JSON string of request metadata, or None if not provided
        """
        if self.request is None:
            return None
        return self.request.to_generation_prompt()

