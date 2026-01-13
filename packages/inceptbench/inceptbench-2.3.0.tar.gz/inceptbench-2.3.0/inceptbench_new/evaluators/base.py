"""
Base evaluator class for educational content evaluation.

This module defines the abstract base class that all content-type-specific
evaluators must extend.
"""

import asyncio
import logging
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from inceptbench_new.config import settings
from inceptbench_new.models import BaseEvaluationResult
from inceptbench_new.core.input_models import RequestMetadata
from inceptbench_new.tools.api_client import get_async_openai_client
from inceptbench_new.tools.curriculum_search import get_curriculum_context
from inceptbench_new.tools.image_utils import extract_image_urls, prepare_images_for_api
from inceptbench_new.tools.image_analyzer import analyze_images, format_analysis_for_prompt
from inceptbench_new.tools.object_counter import count_objects_in_images, format_count_data_for_prompt
from inceptbench_new.utils.failure_tracker import AttemptError, FailureTracker

logger = logging.getLogger(__name__)


class BaseEvaluator(ABC):
    """
    Abstract base class for all content evaluators.
    
    Provides common functionality for:
    - Loading prompts from files
    - Getting curriculum context
    - Getting object count context for images
    - Structuring evaluation calls
    
    Subclasses must implement:
    - _load_prompt(): Load evaluator-specific prompt
    - evaluate(): Perform the evaluation
    - _get_result_model(): Return the Pydantic model for results
    """
    
    def __init__(self, model: Optional[str] = None):
        """
        Initialize the evaluator.
        
        Args:
            model: Model to use for evaluation (defaults to settings.EVALUATION_MODEL)
        """
        self.model = model or settings.EVALUATION_MODEL
        self.prompt_template = self._load_prompt()
        
    @abstractmethod
    def _load_prompt(self) -> str:
        """
        Load the evaluator-specific prompt from file.
        
        Returns:
            Prompt template string
            
        Raises:
            RuntimeError: If prompt file cannot be loaded
        """
        pass
    
    async def evaluate(
        self, 
        content: str, 
        curriculum: str = "common_core",
        full_context: Optional[str] = None,
        subcontent_results: Optional[List[BaseEvaluationResult]] = None,
        request_metadata: Optional[RequestMetadata] = None,
        analyzed_image_urls: Optional[set] = None
    ) -> BaseEvaluationResult:
        """
        Evaluate the content and return structured results.
        
        This is the default implementation that handles the common evaluation flow:
        1. Get programmatic analysis context (if any)
        2. Get curriculum context
        3. Get object count context (skipping already-analyzed images)
        4. Get generation_prompt context from request_metadata (for AI-generated content)
        5. Add full_context if provided (for hierarchical content)
        6. Add subcontent_results if provided (for parent content)
        7. Build system prompt with all contexts
        8. Call LLM evaluator
        9. Return results
        
        Subclasses can override this method for custom behavior, or just override
        _get_programmatic_context() to add custom analyses.
        
        Args:
            content: The educational content to evaluate (specific node content)
            curriculum: Curriculum to use for evaluation (default: "common_core")
            full_context: Complete root content for contextual evaluation (optional)
            subcontent_results: Results from evaluating nested content (optional)
            request_metadata: Optional structured metadata about the content generation request
            analyzed_image_urls: Set of image URLs already analyzed in subcontent (optional)
            
        Returns:
            Evaluation results specific to the content type
            
        Raises:
            RuntimeError: If evaluation fails
        """
        start_time = time.time()
        content_type_name = self._get_result_model().__name__.replace("EvaluationResult", "").lower()
        logger.info(f"Evaluating {content_type_name}...")
        
        # Track which images to skip (already analyzed in subcontent)
        skip_images = analyzed_image_urls or set()
        if skip_images:
            logger.info(f"Skipping {len(skip_images)} image(s) already analyzed in subcontent")
        
        try:
            # Gather context in parallel (no dependencies between these calls)
            (
                programmatic_context, 
                curriculum_context, 
                object_count_context,
                image_analysis_context
            ) = await asyncio.gather(
                self._get_programmatic_context(content),
                self._get_curriculum_context(content, curriculum, request_metadata),
                self._get_object_count_context(content, skip_images=skip_images),
                self._get_image_analysis_context(content, skip_images=skip_images)
            )

            # Get generation prompt context if provided (sync, no IO)
            # We derive this from request_metadata
            generation_prompt_context = ""
            if request_metadata:
                prompt_text = request_metadata.to_generation_prompt()
                generation_prompt_context = self._format_generation_prompt_context(prompt_text)
            
            # Build complete system prompt (contexts are prepended to prompt template)
            system_prompt = self.prompt_template
            
            # Add hierarchical context (if provided)
            if full_context and full_context != content:
                context_note = (
                    "\n\n## FULL CONTEXT\n\n"
                    "This content is part of a larger educational resource. "
                    "The complete context is provided below for reference:\n\n"
                    f"{full_context}\n\n"
                    "---\n\n"
                    "You are evaluating the SPECIFIC content provided in the user message, "
                    "but you should consider how it relates to and fits within the full context above."
                )
                system_prompt = context_note + "\n\n" + system_prompt
            
            # Add subcontent evaluation results (if provided)
            if subcontent_results:
                subcontent_context = self._format_subcontent_results(subcontent_results)
                system_prompt = subcontent_context + "\n\n" + system_prompt
            
            # Add standard contexts
            if programmatic_context:
                system_prompt = programmatic_context + "\n\n" + system_prompt
            if object_count_context:
                system_prompt = object_count_context + "\n\n" + system_prompt
            if image_analysis_context:
                system_prompt = image_analysis_context + "\n\n" + system_prompt
            if curriculum_context:
                system_prompt = curriculum_context + "\n\n" + system_prompt
            if generation_prompt_context:
                system_prompt = generation_prompt_context + "\n\n" + system_prompt
            
            # Call LLM evaluator
            result_model = self._get_result_model()
            result = await self._call_llm_evaluator(
                content=content,
                system_prompt=system_prompt,
                result_model=result_model
            )
            
            logger.info(
                f"{content_type_name.capitalize()} evaluation complete in {time.time() - start_time:.2f}s. "
                f"Overall: {result.overall.score:.2f}"
            )
            return result
            
        except Exception as e:
            logger.error(f"Error evaluating {content_type_name}: {e}")
            raise RuntimeError(f"{content_type_name.capitalize()} evaluation failed: {e}")
    
    @abstractmethod
    def _get_result_model(self) -> type[BaseEvaluationResult]:
        """
        Return the Pydantic model class for this evaluator's results.
        
        Returns:
            Pydantic model class (e.g., QuestionEvaluationResult)
        """
        pass
    
    async def _get_programmatic_context(self, content: str) -> str:
        """
        Hook for subclasses to add programmatic analysis context.
        
        Override this method to perform programmatic analyses (e.g., chi-square
        test for answer balance in quizzes) and return formatted context to
        prepend to the system prompt.
        
        Args:
            content: The educational content
            
        Returns:
            Formatted programmatic analysis context string (empty by default)
        """
        return ""
    
    def _compute_child_aggregation_stats(
        self, 
        subcontent_results: List[BaseEvaluationResult]
    ) -> Dict:
        """
        Compute aggregation statistics from child evaluation results.
        
        These statistics are used by parent evaluators as authoritative data
        for metrics that depend on child outcomes.
        
        Args:
            subcontent_results: List of evaluation results from subcontent
            
        Returns:
            Dictionary containing:
            - n_children: Total number of children
            - mean_child: Mean of child overall scores
            - min_child: Minimum of child overall scores
            - max_child: Maximum of child overall scores
            - factual_accuracy_failures: Count of children with factual_accuracy = 0.0
            - educational_accuracy_failures: Count of children with educational_accuracy = 0.0
            - educational_accuracy_failure_pct: Percentage of children failing educational_accuracy
            - metric_pass_rates: Dict mapping metric names to pass rates (proportion with score 1.0)
        """
        if not subcontent_results:
            return {}
        
        n = len(subcontent_results)
        overall_scores = [r.overall.score for r in subcontent_results]
        
        # Core statistics
        stats = {
            "n_children": n,
            "mean_child": sum(overall_scores) / n,
            "min_child": min(overall_scores),
            "max_child": max(overall_scores),
        }
        
        # Critical metric failures
        factual_failures = sum(1 for r in subcontent_results if r.factual_accuracy.score == 0.0)
        educational_failures = sum(1 for r in subcontent_results if r.educational_accuracy.score == 0.0)
        
        stats["factual_accuracy_failures"] = factual_failures
        stats["educational_accuracy_failures"] = educational_failures
        stats["educational_accuracy_failure_pct"] = (educational_failures / n) * 100
        
        # Compute pass rates for common metrics across all children
        # We check which metrics exist on the results and compute pass rates
        metric_pass_rates = {}
        
        # Metrics that might be shared between parent and child evaluations
        potential_shared_metrics = [
            "factual_accuracy",
            "educational_accuracy", 
            "localization_quality",
            "stimulus_quality",
        ]
        
        for metric_name in potential_shared_metrics:
            scores = []
            for r in subcontent_results:
                metric_result = getattr(r, metric_name, None)
                if metric_result is not None and hasattr(metric_result, 'score'):
                    scores.append(metric_result.score)
            
            if scores:
                pass_count = sum(1 for s in scores if s == 1.0)
                metric_pass_rates[metric_name] = {
                    "pass_count": pass_count,
                    "total": len(scores),
                    "pass_rate": pass_count / len(scores)
                }
        
        stats["metric_pass_rates"] = metric_pass_rates
        
        return stats
    
    def _format_subcontent_results(self, subcontent_results: List[BaseEvaluationResult]) -> str:
        """
        Format subcontent evaluation results for inclusion in parent evaluation prompt.
        
        This provides the parent evaluator with context about how its nested
        components were evaluated, including computed aggregation statistics
        that should be used as authoritative data.
        
        Args:
            subcontent_results: List of evaluation results from subcontent
            
        Returns:
            Formatted string describing subcontent evaluations
        """
        if not subcontent_results:
            return ""
        
        # Compute aggregation statistics
        stats = self._compute_child_aggregation_stats(subcontent_results)
        
        lines = [
            "\n\n## NESTED CONTENT EVALUATIONS\n",
            f"This content contains {stats['n_children']} nested component(s) that have been evaluated.",
        ]
        
        # Add computed statistics section (AUTHORITATIVE)
        lines.append("\n### COMPUTED AGGREGATION STATISTICS (AUTHORITATIVE - USE THESE EXACTLY)")
        lines.append("")
        lines.append("The following statistics have been pre-computed from child evaluations.")
        lines.append("**You MUST use these values exactly** when applying aggregation rules.")
        lines.append("")
        lines.append(f"- **mean_child**: {stats['mean_child']:.3f}")
        lines.append(f"- **min_child**: {stats['min_child']:.3f}")
        lines.append(f"- **max_child**: {stats['max_child']:.3f}")
        lines.append("")
        lines.append(f"- **factual_accuracy failures**: {stats['factual_accuracy_failures']} of {stats['n_children']} children")
        lines.append(f"- **educational_accuracy failures**: {stats['educational_accuracy_failures']} of {stats['n_children']} children ({stats['educational_accuracy_failure_pct']:.1f}%)")
        
        # Add metric pass rates
        if stats.get("metric_pass_rates"):
            lines.append("")
            lines.append("**Metric pass rates across children:**")
            for metric_name, rate_info in stats["metric_pass_rates"].items():
                pct = rate_info["pass_rate"] * 100
                passes_threshold = "✓ passes 80%" if rate_info["pass_rate"] >= 0.80 else "✗ below 80%"
                lines.append(f"- {metric_name}: {rate_info['pass_count']}/{rate_info['total']} passing ({pct:.0f}%) {passes_threshold}")
        
        # Add individual component details
        lines.append("\n### Individual Component Scores\n")
        
        for i, subcontent_result in enumerate(subcontent_results, 1):
            content_type = subcontent_result.content_type
            overall_score = subcontent_result.overall.score
            
            lines.append(f"**Component {i}: {content_type}**")
            lines.append(f"- Overall Score: {overall_score:.2f}")
            lines.append(f"- Factual Accuracy: {subcontent_result.factual_accuracy.score:.1f}")
            lines.append(f"- Educational Accuracy: {subcontent_result.educational_accuracy.score:.1f}")
            
            # Add key insights from overall reasoning (first sentence)
            reasoning_preview = subcontent_result.overall.reasoning.split('.')[0] + "."
            lines.append(f"- Summary: {reasoning_preview}")
            lines.append("")
        
        lines.append(
            "**Use the computed statistics above** when determining parent-level metric scores. "
            "Do NOT recalculate these values - use them as provided."
        )
        
        return "\n".join(lines)
    
    async def _get_curriculum_context(
        self, 
        content: str, 
        curriculum: str,
        request_metadata: Optional[RequestMetadata] = None
    ) -> str:
        """
        Get curriculum context for the content.
        
        Extracts explicit curriculum standards if present, or searches
        based on content. Returns formatted context string.
        
        Args:
            content: The educational content
            curriculum: Curriculum name
            request_metadata: Optional metadata about the request (prioritized for search)
            
        Returns:
            Formatted curriculum context string (may be empty)
        """
        try:
            return await get_curriculum_context(content, curriculum, request_metadata)
        except Exception as e:
            logger.warning(f"Error getting curriculum context: {e}")
            return ""
    
    async def _get_object_count_context(self, content: str, skip_images: set = None) -> str:
        """
        Get object count context if images are present in the content.
        
        Extracts image URLs, counts objects in images, and returns
        formatted context string. Skips images that have already been
        analyzed in subcontent evaluations.
        
        Args:
            content: The educational content
            skip_images: Set of image URLs to skip (already analyzed in subcontent)
            
        Returns:
            Formatted object count context string (may be empty)
        """
        try:
            image_urls = extract_image_urls(content)
            if not image_urls:
                return ""
            
            # Filter out images already analyzed in subcontent
            if skip_images:
                original_count = len(image_urls)
                image_urls = [url for url in image_urls if url not in skip_images]
                if original_count != len(image_urls):
                    logger.info(
                        f"Filtered {original_count - len(image_urls)} image(s) already analyzed in subcontent"
                    )
            
            if not image_urls:
                logger.info("All images already analyzed in subcontent, skipping object counting")
                return ""
            
            logger.info(f"Found {len(image_urls)} image(s) in content, counting objects...")
            count_result = await count_objects_in_images(image_urls)
            object_count_context = format_count_data_for_prompt(count_result)
            logger.info("Object count context generated")
            return object_count_context
            
        except Exception as e:
            logger.warning(f"Error getting object count context: {e}")
            return ""
    
    async def _get_image_analysis_context(self, content: str, skip_images: set = None) -> str:
        """
        Get image analysis context if images are present in the content.
        
        Analyzes geometric properties, angles, shapes, and spatial relationships
        in images. This provides authoritative ground truth for geometry questions
        and other visual content verification. Skips images that have already been
        analyzed in subcontent evaluations.
        
        Args:
            content: The educational content
            skip_images: Set of image URLs to skip (already analyzed in subcontent)
            
        Returns:
            Formatted image analysis context string (may be empty)
        """
        try:
            image_urls = extract_image_urls(content)
            if not image_urls:
                return ""
            
            # Filter out images already analyzed in subcontent
            if skip_images:
                original_count = len(image_urls)
                image_urls = [url for url in image_urls if url not in skip_images]
                if original_count != len(image_urls):
                    logger.info(
                        f"Filtered {original_count - len(image_urls)} image(s) already analyzed in subcontent"
                    )
            
            if not image_urls:
                logger.info("All images already analyzed in subcontent, skipping image analysis")
                return ""
            
            logger.info(f"Found {len(image_urls)} image(s) in content, analyzing visual properties...")
            analysis_result = await analyze_images(image_urls)
            image_analysis_context = format_analysis_for_prompt(analysis_result)
            logger.info("Image analysis context generated")
            return image_analysis_context
            
        except Exception as e:
            logger.warning(f"Error getting image analysis context: {e}")
            return ""
    
    def _format_generation_prompt_context(self, generation_prompt: Optional[str]) -> str:
        """
        Format the generation prompt context for inclusion in the system prompt.
        
        The generation prompt represents the instructions used to create AI-generated
        content. When present, it helps the evaluator understand the intended purpose
        and goals of the content, which is especially relevant for metrics like
        educational_accuracy and curriculum_alignment.
        
        Args:
            generation_prompt: The prompt used to generate the content (optional)
            
        Returns:
            Formatted generation prompt context string (empty if no prompt provided)
        """
        if not generation_prompt or not generation_prompt.strip():
            return ""
        
        return (
            "## GENERATION PROMPT\n\n"
            "The content you are evaluating was AI-generated using the following prompt. "
            "Use this prompt as an expression of the intended purpose, goals, and requirements "
            "for the content. When assessing metrics such as educational_accuracy, "
            "curriculum_alignment, or any other metrics where understanding the intended "
            "purpose is relevant, consider whether the content successfully fulfills the "
            "requirements expressed in this generation prompt:\n\n"
            f"{generation_prompt.strip()}\n\n"
            "---"
        )
    
    def _load_prompt_from_file(self, prompt_file_path: Path) -> str:
        """
        Helper method to load prompt from a file path.
        
        Args:
            prompt_file_path: Path to the prompt file
            
        Returns:
            Prompt content as string
            
        Raises:
            RuntimeError: If file cannot be loaded
        """
        try:
            with open(prompt_file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading prompt from {prompt_file_path}: {e}")
            raise RuntimeError(f"Could not load prompt: {e}")
    
    async def _call_llm_evaluator(
        self,
        content: str,
        system_prompt: str,
        result_model: type[BaseEvaluationResult],
        max_retries: int = 3
    ) -> BaseEvaluationResult:
        """
        Helper method to call LLM for evaluation with structured output.
        
        Includes retry logic with exponential backoff for parsing failures.
        
        Args:
            content: The content to evaluate
            system_prompt: The complete system prompt (including context)
            result_model: Pydantic model for structured output
            max_retries: Maximum number of retry attempts (default: 3)
            
        Returns:
            Evaluation result
            
        Raises:
            RuntimeError: If LLM call fails after all retries
        """
        import json
        import random
        
        client = get_async_openai_client(timeout=settings.DEFAULT_TIMEOUT)
        
        # Build user content with images if present
        user_content = [
            {"type": "input_text", "text": f"Please evaluate this content:\n\n{content}"}
        ]
        
        # Add images if present
        image_urls = extract_image_urls(content)
        if image_urls:
            logger.info(f"Adding {len(image_urls)} image(s) to evaluation")
            image_content = prepare_images_for_api(image_urls)
            user_content.extend(image_content)
        
        last_error = None
        attempt_errors: List[AttemptError] = []
        
        for attempt in range(max_retries + 1):
            try:
                # Call LLM with structured output
                response = await client.responses.parse(
                    model=self.model,
                    input=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    text_format=result_model
                )
                
                # Extract the evaluation from the structured response
                for output_item in response.output:
                    if output_item.type == "message":
                        for content_item in output_item.content:
                            if content_item.type == "output_text":
                                # Check if parsing succeeded
                                if hasattr(content_item, "parsed") and content_item.parsed is not None:
                                    if attempt > 0:
                                        FailureTracker.record_recovered(
                                            component="evaluator._call_llm_evaluator",
                                            message=f"Succeeded on attempt {attempt + 1}/{max_retries + 1}",
                                            context={"model": self.model},
                                            attempt_errors=attempt_errors if attempt_errors else None
                                        )
                                        logger.info(f"Successfully parsed response on attempt {attempt + 1}")
                                    return content_item.parsed
                                
                                # Parsing failed - try to manually parse from raw text
                                raw_text = getattr(content_item, "text", None)
                                if raw_text:
                                    try:
                                        raw_json = json.loads(raw_text)
                                        # Try to validate with Pydantic
                                        result = result_model.model_validate(raw_json)
                                        logger.info(f"Manually parsed response on attempt {attempt + 1}")
                                        return result
                                    except json.JSONDecodeError as json_error:
                                        logger.warning(f"Raw response is not valid JSON: {json_error}")
                                    except Exception as validation_error:
                                        logger.warning(f"Pydantic validation error: {validation_error}")
                
                # Check if response only has "reasoning" output (common failure mode)
                response_types = [item.type for item in response.output]
                if response_types == ["reasoning"]:
                    error_msg = "LLM returned reasoning output but no structured evaluation"
                    logger.warning(
                        f"LLM returned only reasoning output without structured response "
                        f"(attempt {attempt + 1}/{max_retries + 1})"
                    )
                    last_error = RuntimeError(error_msg)
                    attempt_errors.append(AttemptError(
                        attempt=attempt + 1,
                        error_message=error_msg
                    ))
                else:
                    # Log response structure for debugging
                    error_msg = f"Could not parse evaluation results from LLM response (structure: {response_types})"
                    logger.warning(f"Unexpected response structure: {response_types} (attempt {attempt + 1})")
                    for output_item in response.output:
                        if output_item.type == "message":
                            logger.warning(f"Message content types: {[c.type for c in output_item.content]}")
                    last_error = RuntimeError(error_msg)
                    attempt_errors.append(AttemptError(
                        attempt=attempt + 1,
                        error_message=error_msg
                    ))
                
            except Exception as e:
                logger.warning(f"LLM call failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                last_error = e
                attempt_errors.append(AttemptError(
                    attempt=attempt + 1,
                    error_message=str(e)
                ))
            
            # Retry with exponential backoff (4s base delay) if not the last attempt
            if attempt < max_retries:
                delay = 4.0 * (2 ** attempt) + random.uniform(0, 1)
                logger.info(f"Retrying in {delay:.1f}s...")
                await asyncio.sleep(delay)
        
        # All retries exhausted - record as EXHAUSTED
        FailureTracker.record_exhausted(
            component="evaluator._call_llm_evaluator",
            error_message=str(last_error) if last_error else "Unknown error",
            context={"model": self.model, "result_model": result_model.__name__, "attempts": max_retries + 1},
            attempt_errors=attempt_errors
        )
        logger.error(f"Failed to get valid LLM response after {max_retries + 1} attempts")
        raise RuntimeError(f"Evaluation failed after {max_retries + 1} attempts: {last_error}")
