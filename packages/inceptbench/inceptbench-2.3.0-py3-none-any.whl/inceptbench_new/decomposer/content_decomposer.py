"""
Content decomposer for hierarchical educational content.

This module provides the ContentDecomposer class which uses LLM-based analysis
to identify and extract nested content structures (e.g., questions within quizzes,
quizzes within reading passages).
"""

import asyncio
import logging
import random
import time
from pathlib import Path
from typing import Optional

from inceptbench_new.llm import LLMFactory, LLMMessage
from inceptbench_new.models import ContentNode, ContentTree, ContentType, DecompositionResult
from inceptbench_new.core.input_models import RequestMetadata

logger = logging.getLogger(__name__)

# Retry configuration: 3 retries with 4s exponential backoff
DECOMPOSER_MAX_RETRIES = 3
DECOMPOSER_BASE_DELAY = 4.0


class ContentDecomposer:
    """
    Decomposes educational content into hierarchical tree structure.
    
    Uses content-type-specific decomposition prompts to identify nested
    components. For example:
    - Quiz → individual questions
    - Reading passage → quizzes and/or questions
    
    The decomposition logic is driven by prompts in src/prompts/<content_type>/decomposition.txt
    If no decomposition prompt exists, the content is treated as a leaf node.
    """
    
    def __init__(self):
        """Initialize the content decomposer."""
        self.llm = LLMFactory.create("decomposer")
    
    def _get_decomposition_prompt_path(self, content_type: ContentType) -> Optional[Path]:
        """
        Get the path to the decomposition prompt for a content type.
        
        Args:
            content_type: Type of content to decompose
            
        Returns:
            Path to decomposition prompt, or None if decomposition not supported
        """
        # Map content type to directory name
        type_map = {
            ContentType.QUESTION: "question",
            ContentType.QUIZ: "quiz",
            ContentType.FICTION_READING: "fiction_reading",
            ContentType.NONFICTION_READING: "nonfiction_reading",
            ContentType.ARTICLE: "article",
            ContentType.OTHER: "other",
        }
        
        dir_name = type_map.get(content_type)
        if not dir_name:
            return None
        
        prompt_path = Path(__file__).parent.parent / "prompts" / dir_name / "decomposition.txt"
        
        # Only return path if file exists
        return prompt_path if prompt_path.exists() else None
    
    def _load_decomposition_prompt(self, content_type: ContentType) -> Optional[str]:
        """
        Load the decomposition prompt for a content type.
        
        Args:
            content_type: Type of content to decompose
            
        Returns:
            Decomposition prompt text, or None if decomposition not supported
        """
        prompt_path = self._get_decomposition_prompt_path(content_type)
        
        if prompt_path is None:
            logger.debug(f"No decomposition prompt for {content_type.value}")
            return None
        
        try:
            with open(prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Error loading decomposition prompt for {content_type.value}: {e}")
            return None
    
    async def _call_decomposer_llm(
        self, 
        content: str, 
        prompt: str,
        request_metadata: Optional[RequestMetadata] = None
    ) -> DecompositionResult:
        """
        Call LLM to decompose content into components.
        
        Includes retry logic with exponential backoff for transient failures.
        
        Args:
            content: Content to decompose
            prompt: Decomposition prompt (content-type-specific)
            request_metadata: Optional structured metadata about the request
            
        Returns:
            DecompositionResult with extracted children
        """
        # Inject structural hints from metadata if available (from upstream)
        system_prompt = prompt
        if request_metadata and request_metadata.instructions:
            # Add instructions as a hint for expected structure
            # We use instructions because they often contain "Create 5 questions" etc.
            system_prompt += (
                f"\n\n## GENERATION INSTRUCTIONS\n"
                f"The user provided the following instructions for creating this content:\n"
                f"\"{request_metadata.instructions}\"\n"
                f"Use these instructions as a hint for the expected structure (e.g., number of questions), "
                f"but strictly decompose the ACTUAL content provided below."
            )
        
        last_error = None
        
        for attempt in range(DECOMPOSER_MAX_RETRIES + 1):
            try:
                result = await self.llm.generate_structured(
                    messages=[
                        LLMMessage(role="system", content=system_prompt),
                        LLMMessage(role="user", content=f"Analyze this content:\n\n{content}")
                    ],
                    response_schema=DecompositionResult
                )
                if attempt > 0:
                    from ..utils.failure_tracker import FailureTracker
                    FailureTracker.record_recovered(
                        component="decomposer",
                        message=f"Succeeded on attempt {attempt + 1}/{DECOMPOSER_MAX_RETRIES + 1}",
                        context={}
                    )
                    logger.info(f"Decomposer succeeded on attempt {attempt + 1}")
                return result
                
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                
                # Check if this is a retryable error (timeout, rate limit, etc.)
                is_retryable = (
                    "timeout" in error_str or
                    "rate" in error_str or
                    "throttl" in error_str or
                    "503" in error_str or
                    "502" in error_str or
                    "overloaded" in error_str
                )
                
                if is_retryable and attempt < DECOMPOSER_MAX_RETRIES:
                    delay = DECOMPOSER_BASE_DELAY * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(
                        f"Decomposer LLM call failed (attempt {attempt + 1}/{DECOMPOSER_MAX_RETRIES + 1}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )
                    await asyncio.sleep(delay)
                else:
                    # Not retryable or out of retries
                    logger.error(f"Error calling decomposer LLM: {e}")
                    from ..utils.failure_tracker import FailureTracker
                    FailureTracker.record_exhausted(
                        component="decomposer",
                        error_message=str(e),
                        context={"attempts": attempt + 1}
                    )
                    # On error, treat as leaf node
                    return DecompositionResult(has_children=False, children=[])
        
        # Should not reach here, but just in case
        from ..utils.failure_tracker import FailureTracker
        FailureTracker.record_exhausted(
            component="decomposer",
            error_message=str(last_error) if last_error else "Unknown error",
            context={"attempts": DECOMPOSER_MAX_RETRIES + 1}
        )
        logger.error(f"Decomposer failed after {DECOMPOSER_MAX_RETRIES + 1} attempts: {last_error}")
        return DecompositionResult(has_children=False, children=[])
    
    async def decompose(
        self, 
        content: str, 
        content_type: ContentType,
        request_metadata: Optional[RequestMetadata] = None
    ) -> ContentTree:
        """
        Decompose content into hierarchical tree structure.
        
        This method recursively decomposes content, identifying nested components
        and building a tree structure. The root content is stored once in the
        ContentTree to avoid duplication across all nodes.
        
        Args:
            content: The content to decompose
            content_type: The type of this content
            request_metadata: Optional structured metadata about the request
            
        Returns:
            ContentTree with root_content and decomposed node structure
        """
        logger.info(f"Decomposing {content_type.value} content ({len(content)} chars)")
        
        # Decompose into node structure
        root_node = await self._decompose_node(content, content_type, request_metadata)
        
        # Wrap in ContentTree to store root_content once
        return ContentTree(
            root_content=content,
            root_node=root_node
        )
    
    async def _decompose_node(
        self,
        content: str,
        content_type: ContentType,
        request_metadata: Optional[RequestMetadata] = None
    ) -> ContentNode:
        """
        Internal method to recursively decompose a content node.
        
        This builds the tree structure without storing root_content in each node.
        
        Args:
            content: The content to decompose for this node
            content_type: The type of this content
            request_metadata: Optional structured metadata about the request
            
        Returns:
            ContentNode with children (if any)
        """

        start_time = time.time()

        # Load decomposition prompt for this content type
        decomposition_prompt = self._load_decomposition_prompt(content_type)
        
        # If no decomposition prompt, treat as leaf node
        if decomposition_prompt is None:
            logger.debug(f"No decomposition for {content_type.value}, treating as leaf")
            return ContentNode(
                type=content_type,
                extracted_content=content,
                children=[]
            )
        
        # Call LLM to extract structure
        try:
            decomposition_result = await self._call_decomposer_llm(
                content, 
                decomposition_prompt, 
                request_metadata
            )
        except Exception as e:
            logger.error(
                f"Decomposition failed after {time.time() - start_time:.2f}s for {content_type.value}: {e}"
            )
            # Fallback to leaf node on error
            return ContentNode(
                type=content_type,
                extracted_content=content,
                children=[]
            )
        
        # If no children found, return leaf node
        if not decomposition_result.has_children or not decomposition_result.children:
            logger.debug(
                f"No children found in {content_type.value} after {time.time() - start_time:.2f}s"
            )
            return ContentNode(
                type=content_type,
                extracted_content=content,
                children=[]
            )
        
        # Recursively decompose children
        child_nodes = []
        for extracted_child in decomposition_result.children:
            logger.info(
                f"Decomposing child: {extracted_child.type.value} "
                f"after {time.time() - start_time:.2f}s"
                f"({len(extracted_child.extracted_content)} chars)"
            )
            
            # Recursively decompose this child
            # Note: We don't pass request_metadata to recursive calls because structural hints
            # (like "Create 5 questions") usually apply to the top level, not nested sub-components.
            # Passing it down might confuse the LLM for sub-components.
            child_node = await self._decompose_node(
                content=extracted_child.extracted_content,
                content_type=extracted_child.type,
                request_metadata=None  # Intentionally not passing metadata to children
            )
            
            child_nodes.append(child_node)
        
        # Create parent node with children
        parent_node = ContentNode(
            type=content_type,
            extracted_content=content,
            children=child_nodes
        )
        
        logger.info(
            f"Decomposed {content_type.value} into {len(child_nodes)} "
            f"children in {time.time() - start_time:.2f}s "
            f"(depth: {parent_node.get_depth()}, total nodes: {parent_node.count_nodes()})"
        )
        
        return parent_node
