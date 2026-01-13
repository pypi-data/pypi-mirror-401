"""
Anthropic Claude adapter for the LLM abstraction layer.

This module provides an adapter for Anthropic's Claude models
that implements the LLMInterface. Supports both AWS Bedrock
and direct Anthropic API, with automatic fallback.

Environment Variables:
    USE_BEDROCK: Set to "true" to use Bedrock, "false" for direct API (default: "true")
    AWS_PROFILE: AWS profile name for Bedrock (default: None, uses instance role)
    AWS_REGION: AWS region for Bedrock (default: "us-east-1")
    ANTHROPIC_API_KEY: API key for direct Anthropic API fallback
    BEDROCK_MAX_RETRIES: Maximum retry attempts for throttling errors (default: 5)
    BEDROCK_BASE_DELAY: Base delay in seconds for exponential backoff (default: 2.0)
"""

import asyncio
import json
import logging
import os
import random
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel

from inceptbench_new.llm.base import LLMImage, LLMInterface, LLMMessage
from inceptbench_new.utils.failure_tracker import AttemptError, FailureTracker

logger = logging.getLogger(__name__)


# Model ID mapping: Direct API model names → Bedrock inference profile IDs
BEDROCK_MODEL_MAPPINGS = {
    # Claude Sonnet 4.5
    "claude-sonnet-4-5": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "claude-sonnet-4-5-20250929": "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    
    # Claude Sonnet 4
    "claude-sonnet-4": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    "claude-sonnet-4-20250514": "us.anthropic.claude-sonnet-4-20250514-v1:0",
    
    # Claude 3.5 Sonnet
    "claude-3-5-sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "claude-3-5-sonnet-20241022": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
}


class BedrockAnthropicResponse:
    """
    Mock response object that matches the structure of Anthropic's response.
    This allows the unified client to be a drop-in replacement for Bedrock responses.
    """
    
    def __init__(self, response_data: Dict[str, Any]):
        self.id = response_data.get("id")
        self.type = response_data.get("type")
        self.role = response_data.get("role")
        self.model = response_data.get("model")
        self.stop_reason = response_data.get("stop_reason")
        self.stop_sequence = response_data.get("stop_sequence")
        self.usage = response_data.get("usage", {})
        
        # Parse content blocks
        self.content = []
        for content_item in response_data.get("content", []):
            content_block = BedrockContentBlock(content_item)
            self.content.append(content_block)


class BedrockContentBlock:
    """Represents a content block in the Bedrock response (text or tool_use)."""
    
    def __init__(self, content_data: Dict[str, Any]):
        self.type = content_data.get("type")
        
        if self.type == "text":
            self.text = content_data.get("text")
        elif self.type == "tool_use":
            self.id = content_data.get("id")
            self.name = content_data.get("name")
            self.input = content_data.get("input", {})


class ClaudeAdapter(LLMInterface):
    """
    Adapter for Anthropic Claude API with AWS Bedrock support.
    
    This adapter handles all Claude-specific details:
    - AWS Bedrock integration with automatic fallback to direct API
    - Authentication and API client setup
    - Request/response format conversion
    - Structured output via tool calling
    - Vision input handling
    - Error handling and retries
    
    Claude uses a tool calling mechanism to generate structured output,
    which is abstracted away by this adapter.
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
        Initialize Claude adapter with Bedrock support.
        
        Args:
            model: Model identifier (e.g., "claude-sonnet-4-5")
            api_key: Anthropic API key (used for direct API fallback)
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
        
        # Determine whether to use Bedrock
        # Default to TRUE - use Bedrock by default for higher rate limits
        use_bedrock_env = os.getenv("USE_BEDROCK", "true").lower()
        self.use_bedrock = use_bedrock_env in ("true", "1", "yes")
        
        # AWS configuration
        self.aws_profile = os.getenv("AWS_PROFILE") or None
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        
        # Initialize clients lazily
        self._bedrock_client = None
        self._anthropic_client = None
        
        # Validate Bedrock availability if enabled
        if self.use_bedrock:
            try:
                self._get_bedrock_client()
                logger.info(
                    f"Claude adapter initialized with Bedrock: {self.model}, "
                    f"region={self.aws_region}"
                )
            except Exception as e:
                logger.warning(
                    f"Bedrock client initialization failed: {e}. "
                    f"Falling back to direct API."
                )
                self.use_bedrock = False
        
        if not self.use_bedrock:
            logger.info(f"Claude adapter initialized with direct API: {self.model}")
    
    def _get_bedrock_client(self):
        """Get or create boto3 Bedrock runtime client."""
        if self._bedrock_client is None:
            try:
                import boto3
                
                # For EC2 instances with IAM roles, don't specify profile_name
                # This allows boto3 to use instance role credentials automatically
                session_kwargs = {"region_name": self.aws_region}
                if self.aws_profile:  # Only set profile if explicitly provided
                    session_kwargs["profile_name"] = self.aws_profile
                
                session = boto3.Session(**session_kwargs)
                self._bedrock_client = session.client('bedrock-runtime')
                
                profile_info = f"profile={self.aws_profile}" if self.aws_profile else "instance role"
                logger.debug(
                    f"Initialized Bedrock client using {profile_info}, region={self.aws_region}"
                )
            except ImportError as e:
                logger.error(f"Failed to import boto3: {e}. Install with: pip install boto3")
                raise
            except Exception as e:
                logger.error(
                    f"Failed to initialize Bedrock client: {e}. "
                    f"Check AWS credentials and region configuration."
                )
                raise
        return self._bedrock_client
    
    def _get_anthropic_client(self):
        """Get or create direct Anthropic client."""
        if self._anthropic_client is None:
            try:
                from anthropic import AsyncAnthropic
                
                if not self.api_key:
                    raise ValueError(
                        "No API key found for Claude direct API. "
                        "Set ANTHROPIC_API_KEY environment variable."
                    )
                self._anthropic_client = AsyncAnthropic(
                    api_key=self.api_key,
                    timeout=self.timeout
                )
                logger.debug("Initialized direct Anthropic client")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
                raise
        return self._anthropic_client
    
    def _map_model_to_bedrock(self, model: str) -> str:
        """
        Map direct API model name to Bedrock inference profile ID.
        
        Args:
            model: Model name from direct API (e.g., "claude-sonnet-4-5")
            
        Returns:
            Bedrock inference profile ID
        """
        # If already a Bedrock inference profile ID, return as-is
        if model.startswith("us.") or model.startswith("global."):
            return model
        
        # Try exact match
        if model in BEDROCK_MODEL_MAPPINGS:
            return BEDROCK_MODEL_MAPPINGS[model]
        
        # Try prefix match
        for key, value in BEDROCK_MODEL_MAPPINGS.items():
            if model.startswith(key):
                logger.debug(f"Mapped model '{model}' to Bedrock profile '{value}'")
                return value
        
        # Default to Claude Sonnet 4.5 if no match
        logger.warning(
            f"No Bedrock mapping found for model '{model}', defaulting to Claude Sonnet 4.5"
        )
        return BEDROCK_MODEL_MAPPINGS["claude-sonnet-4-5"]
    
    async def _invoke_bedrock(
        self,
        system_content: Optional[str],
        user_messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Dict] = None,
        **kwargs
    ) -> BedrockAnthropicResponse:
        """
        Invoke model via AWS Bedrock with retry logic for throttling.
        
        Uses asyncio.to_thread() to make boto3's synchronous calls async.
        Implements exponential backoff with jitter for throttling errors.
        """
        bedrock_client = self._get_bedrock_client()
        
        # Map model ID to Bedrock inference profile
        bedrock_model_id = self._map_model_to_bedrock(self.model)
        
        # Build request body (Bedrock uses same format as Anthropic API)
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "messages": user_messages,
        }
        
        if system_content:
            request_body["system"] = system_content
        if tools:
            request_body["tools"] = tools
        if tool_choice:
            request_body["tool_choice"] = tool_choice
        
        temperature = kwargs.get("temperature", self.temperature)
        if temperature is not None:
            request_body["temperature"] = temperature
        
        logger.debug(
            f"Bedrock request: model={bedrock_model_id}, "
            f"max_tokens={request_body['max_tokens']}, messages_count={len(user_messages)}"
        )
        
        # Retry configuration
        max_retries = int(os.getenv("BEDROCK_MAX_RETRIES", "5"))
        base_delay = float(os.getenv("BEDROCK_BASE_DELAY", "2.0"))
        
        last_exception = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(max_retries + 1):
            try:
                # Invoke model via Bedrock (synchronous boto3 call in thread pool)
                response = await asyncio.to_thread(
                    bedrock_client.invoke_model,
                    modelId=bedrock_model_id,
                    body=json.dumps(request_body)
                )
                
                # Parse response
                response_body = json.loads(response['body'].read())
                
                logger.debug(
                    f"Bedrock response received: model={bedrock_model_id}, "
                    f"tokens_used={response_body.get('usage', {})}"
                )
                
                # Record recovery if this wasn't the first attempt
                if attempt > 0:
                    FailureTracker.record_recovered(
                        component="claude_adapter.bedrock",
                        message=f"Succeeded on attempt {attempt + 1}/{max_retries + 1}",
                        context={"model": self.model, "bedrock_model_id": bedrock_model_id},
                        attempt_errors=attempt_errors if attempt_errors else None
                    )
                
                return BedrockAnthropicResponse(response_body)
                
            except Exception as e:
                last_exception = e
                error_name = type(e).__name__
                
                # Record this attempt's error
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
                
                # Check if this is a throttling/rate limit error
                is_throttling = (
                    "ThrottlingException" in error_name or
                    "ThrottlingException" in str(e) or
                    "Too many tokens" in str(e) or
                    "rate" in str(e).lower() or
                    "throttl" in str(e).lower()
                )
                
                if is_throttling and attempt < max_retries:
                    # Exponential backoff with jitter
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Bedrock throttling (attempt {attempt + 1}/{max_retries + 1}): "
                        f"{error_name}: {e}. Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    # Not a throttling error or out of retries
                    if is_throttling:
                        logger.error(
                            f"Bedrock throttling persists after {max_retries + 1} attempts. "
                            f"Consider reducing concurrency or increasing BEDROCK_BASE_DELAY."
                        )
                        FailureTracker.record_exhausted(
                            component="claude_adapter.bedrock",
                            error_message=f"Bedrock throttling after {max_retries + 1} retries: {e}",
                            context={"model": self.model, "bedrock_model_id": bedrock_model_id, "attempts": attempt + 1},
                            attempt_errors=attempt_errors
                        )
                    raise
        
        # Should not reach here, but just in case
        raise last_exception
    
    async def _invoke_direct(
        self,
        system_content: Optional[str],
        user_messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Dict] = None,
        **kwargs
    ) -> Any:
        """
        Invoke model via direct Anthropic API.
        
        Includes retry logic with 3 retries and 4s exponential backoff
        for transient errors (rate limits, timeouts, server errors).
        
        Returns the native Anthropic response object.
        """
        anthropic_client = self._get_anthropic_client()
        
        logger.debug(
            f"Direct API request: model={self.model}, "
            f"max_tokens={kwargs.get('max_tokens', self.max_tokens)}, "
            f"messages_count={len(user_messages)}"
        )
        
        # Build kwargs for Anthropic API
        api_kwargs = {
            "model": self.model,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens),
            "messages": user_messages,
        }
        
        if system_content:
            api_kwargs["system"] = system_content
        if tools:
            api_kwargs["tools"] = tools
        if tool_choice:
            api_kwargs["tool_choice"] = tool_choice
        
        temperature = kwargs.get("temperature", self.temperature)
        if temperature is not None:
            api_kwargs["temperature"] = temperature
        
        # Retry configuration: 3 retries with 4s exponential backoff
        max_retries = 3
        base_delay = 4.0
        last_exception = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(max_retries + 1):
            try:
                response = await anthropic_client.messages.create(**api_kwargs)
                
                # Record recovery if this wasn't the first attempt
                if attempt > 0:
                    FailureTracker.record_recovered(
                        component="claude_adapter.direct",
                        message=f"Succeeded on attempt {attempt + 1}/{max_retries + 1}",
                        context={"model": self.model},
                        attempt_errors=attempt_errors if attempt_errors else None
                    )
                
                logger.debug(
                    f"Direct API response received: model={self.model}, "
                    f"tokens_used={response.usage if hasattr(response, 'usage') else 'unknown'}"
                )
                
                return response
                
            except Exception as e:
                last_exception = e
                error_str = str(e).lower()
                
                # Record this attempt's error
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
                
                # Check if error is retryable
                is_retryable = any(keyword in error_str for keyword in [
                    "timeout", "timed out", "rate", "429", "503", "500",
                    "overloaded", "server error", "connection"
                ])
                
                if is_retryable and attempt < max_retries:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Claude direct API error (attempt {attempt + 1}/"
                        f"{max_retries + 1}): {e}. Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    if is_retryable:
                        FailureTracker.record_exhausted(
                            component="claude_adapter.direct",
                            error_message=str(e),
                            context={"model": self.model, "attempts": attempt + 1},
                            attempt_errors=attempt_errors
                        )
                    raise
        
        # Should not reach here, but just in case
        raise last_exception
    
    async def _create_message(
        self,
        system_content: Optional[str],
        user_messages: List[Dict],
        tools: Optional[List[Dict]] = None,
        tool_choice: Optional[Dict] = None,
        **kwargs
    ) -> Any:
        """
        Create a message using the configured provider with automatic fallback.
        """
        # Try Bedrock first if enabled
        if self.use_bedrock:
            try:
                logger.debug(f"Attempting Bedrock invocation for model={self.model}")
                response = await self._invoke_bedrock(
                    system_content=system_content,
                    user_messages=user_messages,
                    tools=tools,
                    tool_choice=tool_choice,
                    **kwargs
                )
                logger.debug(f"✓ Bedrock invocation successful for model={self.model}")
                return response
                
            except Exception as e:
                logger.warning(
                    f"Bedrock invocation failed for model={self.model}, "
                    f"falling back to direct API: {type(e).__name__}: {e}"
                )
                # Fall through to direct API
        
        # Use direct API (either as primary or fallback)
        logger.debug(
            f"Using direct Anthropic API for model={self.model} "
            f"(bedrock_enabled={self.use_bedrock})"
        )
        response = await self._invoke_direct(
            system_content=system_content,
            user_messages=user_messages,
            tools=tools,
            tool_choice=tool_choice,
            **kwargs
        )
        logger.debug(f"✓ Direct API invocation successful for model={self.model}")
        return response
    
    def _prepare_messages(self, messages: List[LLMMessage]) -> tuple[Optional[str], list[dict]]:
        """
        Prepare messages for Claude API.
        
        Claude requires system messages to be separate from the messages array.
        
        Args:
            messages: Standard LLM messages
            
        Returns:
            Tuple of (system_content, user_messages)
        """
        # Extract system message if present
        system_content = next(
            (msg.content for msg in messages if msg.role == "system"),
            None
        )
        
        # Build user messages (Claude doesn't accept system in messages array)
        user_messages = [
            msg.to_dict()
            for msg in messages
            if msg.role != "system"
        ]
        
        return system_content, user_messages
    
    async def generate_text(
        self,
        messages: List[LLMMessage],
        **kwargs
    ) -> str:
        """
        Generate plain text using Claude messages API.
        
        Args:
            messages: Conversation messages
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Generated text string
        """
        system_content, user_messages = self._prepare_messages(messages)
        
        try:
            response = await self._create_message(
                system_content=system_content,
                user_messages=user_messages,
                **kwargs
            )
            
            # Extract text from response
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Claude text generation failed: {e}")
            FailureTracker.record_exhausted(
                component="claude_adapter.generate_text",
                error_message=str(e),
                context={"model": self.model}
            )
            raise
    
    async def generate_structured(
        self,
        messages: List[LLMMessage],
        response_schema: Type[BaseModel],
        **kwargs
    ) -> BaseModel:
        """
        Generate structured output using Claude tool calling.
        
        Claude doesn't have native structured output, but we can use
        tool calling to achieve the same result. We define a tool with
        the schema as its input schema, and force Claude to use it.
        
        Args:
            messages: Conversation messages
            response_schema: Pydantic model class for output structure
            **kwargs: Override temperature, max_tokens, etc.
            
        Returns:
            Instance of response_schema with model output
        """
        system_content, user_messages = self._prepare_messages(messages)
        
        # Define tool from schema
        tool = {
            "name": "structured_output",
            "description": (
                f"Return structured output matching the {response_schema.__name__} schema"
            ),
            "input_schema": response_schema.model_json_schema()
        }
        
        try:
            response = await self._create_message(
                system_content=system_content,
                user_messages=user_messages,
                tools=[tool],
                tool_choice={"type": "tool", "name": "structured_output"},
                **kwargs
            )
            
            # Extract tool use from response
            for content_block in response.content:
                if (content_block.type == "tool_use" and 
                    content_block.name == "structured_output"):
                    return response_schema(**content_block.input)
            
            raise ValueError("No structured output found in Claude response")
            
        except Exception as e:
            logger.error(
                f"Claude structured output generation failed for "
                f"{response_schema.__name__}: {e}"
            )
            FailureTracker.record_exhausted(
                component="claude_adapter.generate_structured",
                error_message=str(e),
                context={"model": self.model, "schema": response_schema.__name__}
            )
            raise
    
    async def generate_with_vision(
        self,
        messages: List[LLMMessage],
        images: List[LLMImage],
        response_schema: Optional[Type[BaseModel]] = None,
        **kwargs
    ) -> Union[str, BaseModel]:
        """
        Generate response with image inputs (Claude vision).
        
        Handles both plain text and structured output with vision.
        Images can be provided as URLs or base64-encoded data.
        
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
        
        system_content, user_messages_base = self._prepare_messages(messages)
        
        # Build content array with text and images
        content = []
        
        # Add text from user messages
        for msg in messages:
            if msg.role == "user":
                content.append({"type": "text", "text": msg.content})
        
        # Add images to content
        for img in images:
            if img.url:
                # Note: Claude API expects base64 for images, but we'll pass URL
                # and let the adapter handle downloading if needed
                content.append({
                    "type": "image",
                    "source": {"type": "url", "url": img.url}
                })
            elif img.base64_data:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": img.media_type,
                        "data": img.base64_data
                    }
                })
        
        # Build user messages with combined content
        user_messages = [{"role": "user", "content": content}]
        
        try:
            if response_schema:
                # Structured output with vision using tool calling
                tool = {
                    "name": "structured_output",
                    "description": (
                        f"Return structured output matching the {response_schema.__name__} schema"
                    ),
                    "input_schema": response_schema.model_json_schema()
                }
                
                response = await self._create_message(
                    system_content=system_content,
                    user_messages=user_messages,
                    tools=[tool],
                    tool_choice={"type": "tool", "name": "structured_output"},
                    **kwargs
                )
                
                for content_block in response.content:
                    if (content_block.type == "tool_use" and 
                        content_block.name == "structured_output"):
                        return response_schema(**content_block.input)
                
                raise ValueError("No structured output found in vision response")
            else:
                # Plain text with vision
                response = await self._create_message(
                    system_content=system_content,
                    user_messages=user_messages,
                    **kwargs
                )
                
                return response.content[0].text.strip()
                
        except Exception as e:
            logger.error(f"Claude vision generation failed: {e}")
            FailureTracker.record_exhausted(
                component="claude_adapter.generate_with_vision",
                error_message=str(e),
                context={"model": self.model, "image_count": len(images)}
            )
            raise
    
    @property
    def supports_vision(self) -> bool:
        """Check if this model supports vision inputs."""
        # Most Claude models support vision
        return "claude" in self.model.lower()
    
    @property
    def supports_structured_output(self) -> bool:
        """Check if this model supports native structured output."""
        # Claude uses tool calling for structured output
        return True
