"""
Google Gemini adapter for the LLM abstraction layer.

This module provides an adapter for Google's Gemini models
that implements the LLMInterface.

Includes retry logic with exponential backoff for transient errors
(timeouts, rate limits, empty responses).

Retry configuration: 3 retries with 4s exponential backoff.
"""

import asyncio
import base64
import json
import logging
import random
from typing import List, Optional, Type, Union

from google import genai
from google.genai import types
from pydantic import BaseModel

from inceptbench_new.llm.base import LLMImage, LLMInterface, LLMMessage
from inceptbench_new.utils.failure_tracker import AttemptError, FailureTracker

logger = logging.getLogger(__name__)

# Retry configuration: 3 retries with 4s exponential backoff
GEMINI_MAX_RETRIES = 3
GEMINI_BASE_DELAY = 4.0


class GeminiAdapter(LLMInterface):
    """
    Adapter for Google Gemini API.
    
    This adapter handles all Gemini-specific details:
    - Authentication and API client setup
    - Request/response format conversion
    - Structured output via response schemas
    - Vision input handling
    - Error handling and retries
    """
    
    def __init__(
        self,
        model: str,
        api_key: str,
        timeout: float = 60.0,
        temperature: float = 0.0,
        max_tokens: int = 16384
    ):
        """
        Initialize Gemini adapter.
        
        Args:
            model: Model identifier (e.g., "gemini-3-pro-preview")
            api_key: Google AI API key
            timeout: Request timeout in seconds
            temperature: Sampling temperature (0.0 = deterministic)
            max_tokens: Maximum tokens in response
        """
        super().__init__(
            model=model,
            api_key=api_key,
            timeout=timeout,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.client = genai.Client(api_key=self.api_key)
        logger.debug(f"Gemini adapter initialized: {self.model}")
    
    async def generate_text(
        self,
        messages: List[LLMMessage],
        **kwargs
    ) -> str:
        """
        Generate plain text using Gemini API.
        
        Includes retry logic with exponential backoff for transient errors.
        
        Args:
            messages: Conversation messages
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Generated text string
        """
        # Extract system instruction if present
        system_instruction = next(
            (msg.content for msg in messages if msg.role == "system"),
            None
        )
        
        # Build contents from non-system messages
        contents = []
        for msg in messages:
            if msg.role != "system":
                role = "user" if msg.role == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.content)]
                ))
        
        last_error = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(GEMINI_MAX_RETRIES + 1):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=kwargs.get("temperature", self.temperature),
                        max_output_tokens=kwargs.get("max_tokens", self.max_tokens)
                    )
                )
                
                # Check for None response
                if response is None or response.text is None:
                    raise ValueError("Gemini returned empty response")
                
                # Record recovery if this wasn't the first attempt
                if attempt > 0:
                    FailureTracker.record_recovered(
                        component="gemini_adapter.generate_text",
                        message=f"Succeeded on attempt {attempt + 1}/{GEMINI_MAX_RETRIES + 1}",
                        context={"model": self.model},
                        attempt_errors=attempt_errors if attempt_errors else None
                    )
                
                return response.text.strip()
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Record this attempt's error
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
                
                # Check if error is retryable
                is_retryable = any(keyword in error_str for keyword in [
                    "timeout", "rate", "quota", "429", "503", "500",
                    "overloaded", "empty response", "none"
                ])
                
                if is_retryable and attempt < GEMINI_MAX_RETRIES:
                    delay = GEMINI_BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Gemini text generation error (attempt {attempt + 1}/"
                        f"{GEMINI_MAX_RETRIES + 1}): {e}. Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Gemini text generation failed after all retries: {e}")
                    FailureTracker.record_exhausted(
                        component="gemini_adapter.generate_text",
                        error_message=str(e),
                        context={"model": self.model, "attempts": attempt + 1},
                        attempt_errors=attempt_errors
                    )
                    raise
        
        # Should not reach here, but just in case
        raise last_error

    async def generate_structured(
        self,
        messages: List[LLMMessage],
        response_schema: Type[BaseModel],
        **kwargs
    ) -> BaseModel:
        """
        Generate structured output using Gemini's native JSON mode.
        
        Includes retry logic with exponential backoff for transient errors.
        
        Args:
            messages: Conversation messages
            response_schema: Pydantic model class for output structure
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Instance of response_schema with model output
        """
        # Extract system instruction if present
        system_instruction = next(
            (msg.content for msg in messages if msg.role == "system"),
            None
        )
        
        # Build contents from non-system messages
        contents = []
        for msg in messages:
            if msg.role != "system":
                role = "user" if msg.role == "user" else "model"
                contents.append(types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.content)]
                ))
        
        last_error = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(GEMINI_MAX_RETRIES + 1):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=kwargs.get("temperature", self.temperature),
                        max_output_tokens=kwargs.get("max_tokens", self.max_tokens),
                        response_mime_type="application/json",
                        response_schema=response_schema
                    )
                )
                
                # Check for None response
                if response is None or response.text is None:
                    raise ValueError("Gemini returned empty response (None)")
                
                # Parse the JSON response into the schema
                parsed_data = json.loads(response.text)
                
                # Record recovery if this wasn't the first attempt
                if attempt > 0:
                    FailureTracker.record_recovered(
                        component="gemini_adapter.generate_structured",
                        message=f"Succeeded on attempt {attempt + 1}/{GEMINI_MAX_RETRIES + 1}",
                        context={"model": self.model, "schema": response_schema.__name__},
                        attempt_errors=attempt_errors if attempt_errors else None
                    )
                
                return response_schema(**parsed_data)
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Record this attempt's error
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
                
                # Check if error is retryable
                is_retryable = any(keyword in error_str for keyword in [
                    "timeout", "rate", "quota", "429", "503", "500",
                    "overloaded", "empty response", "none", "nonetype"
                ])
                
                if is_retryable and attempt < GEMINI_MAX_RETRIES:
                    delay = GEMINI_BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Gemini structured output error (attempt {attempt + 1}/"
                        f"{GEMINI_MAX_RETRIES + 1}): {e}. Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"Gemini structured output generation failed for "
                        f"{response_schema.__name__} after all retries: {e}"
                    )
                    FailureTracker.record_exhausted(
                        component="gemini_adapter.generate_structured",
                        error_message=str(e),
                        context={"model": self.model, "schema": response_schema.__name__, "attempts": attempt + 1},
                        attempt_errors=attempt_errors
                    )
                    raise
        
        # Should not reach here, but just in case
        raise last_error

    async def generate_with_vision(
        self,
        messages: List[LLMMessage],
        images: List[LLMImage],
        response_schema: Optional[Type[BaseModel]] = None,
        **kwargs
    ) -> Union[str, BaseModel]:
        """
        Generate response with image inputs (Gemini vision).
        
        Handles both plain text and structured output with vision.
        Images can be provided as URLs or base64-encoded data.
        Includes retry logic with exponential backoff for transient errors.
        
        Args:
            messages: Conversation messages
            images: List of images to analyze
            response_schema: Optional schema for structured output
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Text string if no schema, otherwise instance of response_schema
        """
        if not self.supports_vision:
            raise NotImplementedError(
                f"Model {self.model} does not support vision inputs"
            )
        
        # Extract system instruction if present
        system_instruction = next(
            (msg.content for msg in messages if msg.role == "system"),
            None
        )
        
        # Build parts list with text and images
        parts = []
        
        # Add text from user messages
        for msg in messages:
            if msg.role == "user":
                parts.append(types.Part.from_text(text=msg.content))
        
        # Add images
        for img in images:
            if img.url:
                # Gemini can handle URLs directly
                parts.append(types.Part.from_uri(
                    file_uri=img.url,
                    mime_type=img.media_type or "image/png"
                ))
            elif img.base64_data:
                # For base64, use inline data
                image_bytes = base64.b64decode(img.base64_data)
                parts.append(types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=img.media_type or "image/png"
                ))
        
        # Build content with all parts
        contents = [types.Content(role="user", parts=parts)]
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=kwargs.get("temperature", self.temperature),
            max_output_tokens=kwargs.get("max_tokens", self.max_tokens)
        )
        
        if response_schema:
            config.response_mime_type = "application/json"
            config.response_schema = response_schema
        
        last_error = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(GEMINI_MAX_RETRIES + 1):
            try:
                response = await self.client.aio.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
                
                # Check for None response
                if response is None or response.text is None:
                    raise ValueError("Gemini returned empty response (None)")
                
                # Record recovery if this wasn't the first attempt
                if attempt > 0:
                    FailureTracker.record_recovered(
                        component="gemini_adapter.generate_with_vision",
                        message=f"Succeeded on attempt {attempt + 1}/{GEMINI_MAX_RETRIES + 1}",
                        context={"model": self.model, "image_count": len(images)},
                        attempt_errors=attempt_errors if attempt_errors else None
                    )
                
                if response_schema:
                    parsed_data = json.loads(response.text)
                    return response_schema(**parsed_data)
                else:
                    return response.text.strip()
                    
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Record this attempt's error
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
                
                # Check if error is retryable
                is_retryable = any(keyword in error_str for keyword in [
                    "timeout", "rate", "quota", "429", "503", "500",
                    "overloaded", "empty response", "none", "nonetype"
                ])
                
                if is_retryable and attempt < GEMINI_MAX_RETRIES:
                    delay = GEMINI_BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Gemini vision error (attempt {attempt + 1}/"
                        f"{GEMINI_MAX_RETRIES + 1}): {e}. Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    logger.error(f"Gemini vision generation failed after all retries: {e}")
                    FailureTracker.record_exhausted(
                        component="gemini_adapter.generate_with_vision",
                        error_message=str(e),
                        context={"model": self.model, "image_count": len(images), "attempts": attempt + 1},
                        attempt_errors=attempt_errors
                    )
                    raise
        
        # Should not reach here, but just in case
        raise last_error

    @property
    def supports_vision(self) -> bool:
        """Check if this model supports vision inputs."""
        # Most Gemini models support vision
        return "gemini" in self.model.lower()
    
    @property
    def supports_structured_output(self) -> bool:
        """Check if this model supports native structured output."""
        # Gemini supports JSON mode with response schemas
        return True

