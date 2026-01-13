"""
Content classifier for educational materials.

This module provides a classifier that uses LLM to determine the type of
educational content (question, quiz, reading passage, etc.).
"""

import logging
import time
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

from inceptbench_new.llm import LLMFactory, LLMMessage
from inceptbench_new.models import ContentType
from inceptbench_new.core.input_models import RequestMetadata

logger = logging.getLogger(__name__)


class ContentClassificationResult(BaseModel):
    """Result from content classification."""
    content_type: ContentType
    confidence: str  # high, medium, low
    explanation: str


class ContentClassifier:
    """
    Classifies educational content into predefined types.
    
    Uses LLM with structured output to classify content as question, quiz,
    fiction reading, nonfiction reading, or other.
    """
    
    def __init__(self):
        """Initialize the content classifier."""
        self.llm = LLMFactory.create("classifier")
        self.base_system_prompt = self._load_prompt()
        
    def _load_prompt(self) -> str:
        """Load the classifier prompt from file."""
        prompt_path = Path(__file__).parent.parent / "prompts" / "classifier.txt"
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading classifier prompt: {e}")
            raise RuntimeError(f"Could not load classifier prompt: {e}")
    
    async def classify(
        self, 
        content: str,
        request_metadata: Optional[RequestMetadata] = None
    ) -> ContentType:
        """
        Classify the content type.
        
        Args:
            content: The educational content to classify
            request_metadata: Optional metadata about the content generation request
            
        Returns:
            ContentType enum value indicating the classified type
            
        Raises:
            RuntimeError: If classification fails
        """
        start_time = time.time()
        logger.info("Classifying content type...")
        
        try:
            # Construct system prompt with optional hint
            system_prompt = self.base_system_prompt
            
            if request_metadata and request_metadata.type:
                logger.info(f"Using requested type hint: {request_metadata.type}")
                system_prompt += (
                    f"\n\n## USER INTENT\n"
                    f"The user explicitly requested content of type: '{request_metadata.type}'. "
                    f"Please consider this intended type when classifying the actual content, "
                    f"but verify that the content actually matches this type."
                )
            
            result = await self.llm.generate_structured(
                messages=[
                    LLMMessage(role="system", content=system_prompt),
                    LLMMessage(role="user", content=content)
                ],
                response_schema=ContentClassificationResult
            )
            
            logger.info(
                f"Classification completed in {time.time() - start_time:.2f}s: "
                f"{result.content_type.value} (confidence: {result.confidence})"
            )
            logger.debug(f"Classification explanation: {result.explanation}")
            return result.content_type
            
        except Exception as e:
            logger.error(f"Error classifying content: {str(e)}")
            # Record failure and default to OTHER
            from ..utils.failure_tracker import FailureTracker
            FailureTracker.record_exhausted(
                component="classifier",
                error_message=str(e),
                context={"defaulted_to": "OTHER"}
            )
            logger.info(
                f"Classification failed after {time.time() - start_time:.2f}s, "
                f"defaulting to OTHER"
            )
            return ContentType.OTHER
