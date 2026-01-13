"""
Curriculum standards search functionality.

This module provides tools for searching curriculum standards via the InceptAPI.
"""

import logging
import time
import json
from typing import Optional, Tuple

import httpx

from inceptbench_new.config import settings
from inceptbench_new.core.input_models import RequestMetadata

logger = logging.getLogger(__name__)


def _is_meaningful(value) -> bool:
    """
    Check if a value has meaningful content (not empty/null/garbage).
    
    Args:
        value: Any value to check
        
    Returns:
        True if the value appears to have meaningful content
    """
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def _skills_to_query(skills, metadata: Optional[RequestMetadata] = None) -> str:
    """
    Convert a skills field to a search query string.
    
    Extracts relevant information from various skills formats and builds
    a query string for RAG search.
    
    Args:
        skills: The skills field (dict, string, or list)
        metadata: Optional metadata for additional context (grade, subject)
        
    Returns:
        Search query string
    """
    parts = []
    
    if isinstance(skills, dict):
        # Extract relevant fields - prioritize ID and name
        for key in ["id", "standard_id", "standardId", "code", "standard_code", 
                    "name", "title", "description", "skill"]:
            if key in skills and skills[key]:
                parts.append(str(skills[key]))
        
        # If no specific fields found, use JSON dump
        if not parts:
            parts.append(json.dumps(skills))
            
    elif isinstance(skills, str):
        parts.append(skills)
        
    elif isinstance(skills, list):
        for item in skills:
            if isinstance(item, dict):
                # Extract ID/name from each item
                for key in ["id", "standard_id", "name"]:
                    if key in item and item[key]:
                        parts.append(str(item[key]))
                        break
                else:
                    parts.append(json.dumps(item))
            elif item:
                parts.append(str(item))
    
    # Add grade/subject context if available
    if metadata:
        if metadata.grade:
            parts.append(f"Grade {metadata.grade}")
        if metadata.subject:
            parts.append(metadata.subject)
    
    return " ".join(parts)


def _determine_curriculum_confidence(
    content: str,
    request_metadata: Optional[RequestMetadata] = None
) -> Tuple[str, str, str]:
    """
    Determine the confidence level for curriculum targeting and build the search query.
    
    Confidence levels:
    - GUARANTEED: Explicit skills metadata was provided - standards should be strictly enforced
    - HARD: Generation prompt was provided - standards should be enforced
    - SOFT: Only content available - standards are inferred, be conservative
    
    Args:
        content: The educational content
        request_metadata: Optional metadata about the content generation request
        
    Returns:
        Tuple of (confidence_level, search_query, source_description)
    """
    if request_metadata:
        # Priority 1: Explicit skills metadata
        if request_metadata.skills and _is_meaningful(request_metadata.skills):
            search_query = _skills_to_query(request_metadata.skills, request_metadata)
            return ("GUARANTEED", search_query, "explicit skills metadata")
        
        # Priority 2: Generation prompt (instructions field)
        if request_metadata.instructions and _is_meaningful(request_metadata.instructions):
            # Build query from instructions + any available context
            query_parts = []
            if request_metadata.grade:
                query_parts.append(f"Grade {request_metadata.grade}")
            if request_metadata.subject:
                query_parts.append(request_metadata.subject)
            query_parts.append(request_metadata.instructions)
            search_query = " ".join(query_parts)
            return ("HARD", search_query, "generation prompt")
    
    # Priority 3: Fallback to content inference
    # Add any available context from metadata
    if request_metadata:
        context_parts = []
        if request_metadata.grade:
            context_parts.append(f"Grade {request_metadata.grade}")
        if request_metadata.subject:
            context_parts.append(request_metadata.subject)
        
        if context_parts:
            search_query = f"{' '.join(context_parts)}\n\n{content}"
            return ("SOFT", search_query, "content with grade/subject context")
    
    return ("SOFT", content, "content inference")


def _format_curriculum_context(
    results: str,
    confidence: str,
    source: str
) -> str:
    """
    Format curriculum search results with confidence level information.
    
    Args:
        results: The raw curriculum search results
        confidence: The confidence level (GUARANTEED, HARD, SOFT)
        source: Description of the source used for the search
        
    Returns:
        Formatted curriculum context string
    """
    return f"""## CURRICULUM CONTEXT
Confidence: {confidence}
Source: {source}

{results}"""


async def get_curriculum_context(
    content: str, 
    curriculum: str = "common_core",
    request_metadata: Optional[RequestMetadata] = None
) -> str:
    """
    Get curriculum context by calling the InceptAPI curriculum search endpoint.
    
    The API handles all complexity including:
    - Content preparation and cleaning
    - Extracting explicit curriculum standards from content
    - Vector store search across curriculum databases
    - Deduplication of results
    
    The returned context includes a confidence level indicator:
    - GUARANTEED: Explicit skills metadata was provided
    - HARD: Generation prompt was provided
    - SOFT: Standards inferred from content only
    
    Args:
        content: The educational content to analyze
        curriculum: Curriculum name (default: "common_core")
        request_metadata: Optional metadata about the content generation request
        
    Returns:
        Formatted curriculum context string with confidence level, or empty string if none found
    """
    start_time = time.time()
    
    try:
        # Determine confidence level and build optimal search query
        confidence, search_query, source = _determine_curriculum_confidence(
            content, request_metadata
        )
        
        logger.info(
            f"Searching {curriculum} curriculum standards. "
            f"Confidence: {confidence}, Source: {source}, "
            f"Query length: {len(search_query)}"
        )
        
        # Call the InceptAPI curriculum search endpoint
        async with httpx.AsyncClient(timeout=settings.CURRICULUM_SEARCH_TIMEOUT) as client:
            headers = {}
            if settings.INCEPT_API_KEY:
                headers["Authorization"] = f"Bearer {settings.INCEPT_API_KEY}"
            
            response = await client.post(
                f"{settings.INCEPTAPI_BASE_URL}/curriculum-search",
                json={
                    "prompt": search_query,
                    "curriculum_name": curriculum
                },
                headers=headers
            )
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", "")
            
            if results:
                logger.info(
                    f"Curriculum standards search completed in {time.time() - start_time:.2f}s. "
                    f"Confidence: {confidence}"
                )
                return _format_curriculum_context(results, confidence, source)
            else:
                logger.warning(f"No curriculum standards found after {time.time() - start_time:.2f}s")
                return ""
                
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from curriculum API after {time.time() - start_time:.2f}s: "
                    f"{e.response.status_code} - {e.response.text}")
        return ""
    except Exception as e:
        logger.warning(f"Could not retrieve curriculum context after {time.time() - start_time:.2f}s: {e}")
        return ""
