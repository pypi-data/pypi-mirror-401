"""
Command-line interface for educational content evaluator.

This module provides a CLI for evaluating educational content, supporting
both JSON batch input (same format as API) and raw content mode.
"""

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Optional

from ..core.input_models import ContentItem, RequestMetadata
from ..core.processor import BatchProcessor
from ..service import EvaluationService
from ..config.settings import settings
from .. import __version__


def setup_logging(verbose: bool = False):
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def get_sample_content() -> dict:
    """Get sample content.json structure."""
    return {
        "generated_content": [
            {
                "id": "example-1",
                "curriculum": "common_core",
                "request": {
                    "grade": "7",
                    "subject": "mathematics",
                    "type": "mcq",
                    "difficulty": "medium",
                    "locale": "en-US",
                    "skills": {
                        "lesson_title": "Solving Linear Equations",
                        "substandard_id": "CCSS.MATH.7.EE.A.1"
                    },
                    "instruction": "Create a linear equation problem"
                },
                "content": {
                    "question": "What is the value of x in 3x + 7 = 22?",
                    "answer": "C",
                    "options": [
                        {"key": "A", "text": "3"},
                        {"key": "B", "text": "4"},
                        {"key": "C", "text": "5"},
                        {"key": "D", "text": "6"}
                    ]
                }
            },
            {
                "id": "example-2",
                "content": "What is the capital of France?"
            }
        ]
    }


def example_command() -> int:
    """Create a sample content.json file."""
    output_path = Path("content.json")

    if output_path.exists():
        print(f"File already exists: {output_path}")
        response = input("Overwrite? [y/N]: ").strip().lower()
        if response != 'y':
            print("Aborted.")
            return 1

    sample = get_sample_content()

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sample, f, indent=2)

    print(f"Created {output_path}")
    print("\nEdit the file, then run:")
    print(f"  inceptbench evaluate {output_path}")

    return 0


def is_file_path(value: str, extensions: tuple[str, ...]) -> bool:
    """Check if value looks like a file path with given extensions."""
    if not value:
        return False
    path = Path(value)
    return path.suffix.lower() in extensions and path.exists()


def read_file_or_string(
    value: str,
    extensions: tuple[str, ...]
) -> tuple[str, bool]:
    """
    Read content from file if it's a file path, otherwise return as string.

    Args:
        value: String value or file path
        extensions: Allowed file extensions (e.g., ('.txt', '.md'))

    Returns:
        Tuple of (content, was_file)
    """
    if is_file_path(value, extensions):
        path = Path(value)
        content = path.read_text(encoding='utf-8')
        return (content, True)
    return (value, False)


def load_json_content(file_path: Path) -> list[ContentItem]:
    """
    Load content items from a JSON file.

    Supports two formats:
    1. {"generated_content": [...]}
    2. [...]  (direct array)

    Args:
        file_path: Path to JSON file

    Returns:
        List of ContentItem objects

    Raises:
        ValueError: If JSON is invalid or has wrong structure
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Handle both formats
    if isinstance(data, dict):
        if 'generated_content' not in data:
            raise ValueError(
                "JSON must have 'generated_content' array or be an array"
            )
        items_data = data['generated_content']
    elif isinstance(data, list):
        items_data = data
    else:
        raise ValueError("JSON must be an object or array")

    if not items_data:
        raise ValueError("No content items found in JSON")

    if len(items_data) > 100:
        raise ValueError("Maximum 100 items allowed per file")

    # Convert to ContentItem objects
    items = []
    for i, item_data in enumerate(items_data):
        try:
            item = ContentItem(**item_data)
            items.append(item)
        except Exception as e:
            raise ValueError(f"Invalid item at index {i}: {e}")

    return items


def create_raw_content_item(
    content: str,
    curriculum: str,
    generation_prompt: Optional[str]
) -> ContentItem:
    """
    Create a ContentItem from raw content.

    Args:
        content: Raw content string
        curriculum: Curriculum to use
        generation_prompt: Optional generation prompt

    Returns:
        ContentItem object
    """
    request = None
    if generation_prompt:
        request = RequestMetadata(instructions=generation_prompt)

    return ContentItem(
        content=content,
        curriculum=curriculum,
        request=request
    )


def build_summary(result_dict: dict, name: str = "content") -> dict:
    """
    Build a summary of evaluations including nested subcontent.

    Args:
        result_dict: The evaluation result dictionary
        name: Name/identifier for this content piece

    Returns:
        Dictionary with content names and their scores
    """
    summary = {}

    overall = result_dict.get('overall', {})
    summary[name] = {
        "overall_score": overall.get('score'),
        "overall_rating": result_dict.get('overall_rating')
    }

    # Add nested subcontent evaluations recursively
    subcontent = result_dict.get('subcontent_evaluations')
    if subcontent:
        for i, sub_eval in enumerate(subcontent, 1):
            content_type = sub_eval.get('content_type', 'item')
            sub_name = f"{name}/{content_type}_{i}"
            sub_summary = build_summary(sub_eval, sub_name)
            summary.update(sub_summary)

    return dict(sorted(summary.items()))


def print_categorized_failures(failure_summary: dict, verbose: bool):
    """
    Print categorized failure summary.
    
    Categories:
    - CRASHED: Process halted, remaining items not evaluated
    - ABORTED: Item had unhandled error, couldn't complete
    - EXHAUSTED: All retry attempts failed for an operation  
    - RECOVERED: Succeeded after retry (informational)
    """
    crashed = failure_summary.get('crashed')
    aborted = failure_summary.get('aborted', [])
    exhausted = failure_summary.get('exhausted', [])
    recovered = failure_summary.get('recovered', [])
    
    # Check if there's anything to show
    has_issues = crashed or aborted or exhausted or recovered
    if not has_issues:
        return
    
    print("\n" + "=" * 70)
    print("⚠️  ISSUES DURING EVALUATION")
    print("=" * 70)
    
    # CRASHED: Process halted (most severe)
    if crashed:
        print("\n💀 CRASHED (process halted):")
        print(f"   Error: {crashed.get('error', 'Unknown error')}")
        items_not_eval = crashed.get('items_not_evaluated', [])
        if items_not_eval:
            count = crashed.get('items_not_evaluated_count', len(items_not_eval))
            print(f"   Items not evaluated ({count}): {', '.join(items_not_eval[:5])}")
            if count > 5:
                print(f"   ... and {count - 5} more")
    
    # ABORTED: Items that couldn't be evaluated due to unhandled errors
    if aborted:
        print(f"\n❌ ABORTED ({len(aborted)} item(s) - unhandled error, no result):")
        for i, f in enumerate(aborted, 1):
            content_id = f.get('context', {}).get('content_id', 'unknown')
            error = f.get('error', 'No error message')
            print(f"\n  [{i}] Content: {content_id}")
            print(f"      Error: {error[:300]}{'...' if len(error) > 300 else ''}")
    
    # EXHAUSTED: Operations where all retry attempts failed
    if exhausted:
        by_component = failure_summary.get('exhausted_by_component', {})
        print(f"\n🔴 EXHAUSTED ({len(exhausted)} operation(s) - all retries failed):")
        if by_component:
            print(f"   By component: {json.dumps(by_component)}")
        
        for i, f in enumerate(exhausted, 1):
            content_id = f.get('context', {}).get('content_id', 'unknown')
            component = f.get('component', 'unknown')
            error = f.get('error', 'No error message')
            attempts = f.get('context', {}).get('attempts', '?')
            attempt_errors = f.get('attempt_errors', [])
            
            print(f"\n  [{i}] Content: {content_id}")
            print(f"      Component: {component}")
            print(f"      Attempts: {attempts}")
            
            # Show all attempt errors if available
            if attempt_errors and len(attempt_errors) > 1:
                print("      Errors by attempt:")
                for ae in attempt_errors:
                    attempt_num = ae.get('attempt', '?')
                    attempt_err = ae.get('error', 'No error message')
                    # Truncate long errors
                    truncated = attempt_err[:200] + '...' if len(attempt_err) > 200 else attempt_err
                    print(f"        [{attempt_num}] {truncated}")
            else:
                # Single attempt or no detailed errors - show final error
                print(f"      Error: {error[:200]}{'...' if len(error) > 200 else ''}")
            
            # Show additional context if verbose
            if verbose:
                context = f.get('context', {})
                other_context = {k: v for k, v in context.items() 
                                if k not in ('content_id', 'attempts')}
                if other_context:
                    print(f"      Context: {json.dumps(other_context)}")
    
    # RECOVERED: Operations that succeeded after retry (less detail)
    if recovered:
        print(f"\n🟡 RECOVERED ({len(recovered)} operation(s) - succeeded after retry):")
        for f in recovered:
            content_id = f.get('context', {}).get('content_id', 'unknown')
            component = f.get('component', 'unknown')
            message = f.get('error', '')  # Actually contains recovery message
            print(f"   - {content_id}: {component} ({message})")
            
            # Show what errors happened before recovery if verbose
            if verbose:
                attempt_errors = f.get('attempt_errors', [])
                if attempt_errors:
                    for ae in attempt_errors:
                        attempt_num = ae.get('attempt', '?')
                        attempt_err = ae.get('error', 'No error message')
                        truncated = attempt_err[:150] + '...' if len(attempt_err) > 150 else attempt_err
                        print(f"     └─ Attempt {attempt_num} failed: {truncated}")


def print_evaluation_summary(
    evaluations: dict,
    verbose: bool
):
    """Print evaluation summary to console (successful evaluations only)."""
    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)

    for item_id, result in evaluations.items():
        content_type = result.get('content_type', 'unknown')
        overall_score = result.get('overall', {}).get('score', 0)
        overall_rating = result.get('overall_rating', 'N/A')

        print(f"\n[{item_id}]")
        print(f"  Type: {content_type}")
        print(f"  Overall Score: {overall_score:.2f}")
        print(f"  Rating: {overall_rating}")

        # Show subcontent count if present
        subcontent = result.get('subcontent_evaluations')
        if subcontent:
            print(f"  Nested Items: {len(subcontent)}")

        if verbose:
            # Show all metrics
            print("  Metrics:")
            for key, value in result.items():
                if isinstance(value, dict) and 'score' in value:
                    print(f"    {key}: {value['score']:.2f}")

    print("\n" + "=" * 70)


async def run_evaluation(
    items: list[ContentItem],
    output_file: Optional[Path],
    verbose: bool,
    full: bool = False
) -> int:
    """
    Run evaluation on content items.

    Args:
        items: List of ContentItem to evaluate
        output_file: Optional file to save results
        verbose: Whether to show verbose output
        full: Whether to output complete JSON evaluation results

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        service = EvaluationService()
        processor = BatchProcessor(service=service)

        total = len(items)
        print(f"\nEvaluating {total} item(s)...")

        # Progress tracking
        if total > 1:
            try:
                from tqdm import tqdm
                pbar = tqdm(total=total, desc="Evaluating", unit="item")

                def on_progress(completed: int, total: int):
                    pbar.n = completed
                    pbar.refresh()

                result = await processor.process_batch(items, on_progress)
                pbar.close()
            except ImportError:
                # tqdm not available, simple progress
                print("Processing... (install tqdm for progress bar)")
                result = await processor.process_batch(items)
        else:
            result = await processor.process_batch(items)

        # Build output (failures are shown separately, not in JSON)
        output_data = {
            "success_count": result.success_count,
            "failure_count": result.failure_count,
            "evaluations": result.evaluations,
            "failed_items": [
                {"item_id": fi.item_id, "error": fi.error}
                for fi in result.failed_items
            ] if result.failed_items else None,
            "inceptbench_version": __version__
        }

        # Get failure summary for display (includes ABORTED items from failed_items)
        failure_summary = processor.service.get_failure_summary() if hasattr(processor, 'service') else None

        # Save to file if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=2)
            print(f"\nResults saved to: {output_file}")

        # Output order: 1) Full JSON, 2) Failure summary, 3) Overall score summary

        # 1) Print full JSON if --full is specified
        if full:
            print("\n" + "=" * 70)
            print("FULL JSON OUTPUT")
            print("=" * 70)
            print(json.dumps(output_data, indent=2))

        # 2) Print failure summary (categorized)
        if failure_summary:
            print_categorized_failures(failure_summary, verbose)

        # 3) Print overall score summary
        print_evaluation_summary(
            result.evaluations,
            verbose
        )

        # Return success if at least one evaluation succeeded
        return 0 if result.success_count > 0 else 1

    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        if verbose:
            import traceback
            traceback.print_exc()
        return 1


def evaluate_command(args: argparse.Namespace) -> int:
    """Handle the evaluate command."""
    # Validate mutual exclusivity
    has_json = args.content_json is not None
    has_raw = args.raw is not None

    if not has_json and not has_raw:
        print("Error: Either content_json or --raw is required", file=sys.stderr)
        print("Usage: inceptbench evaluate <content.json>")
        print("   or: inceptbench evaluate --raw <content>")
        print("   or: inceptbench evaluate --raw <folder>")
        return 1

    # Validate --curriculum and --generation-prompt only with --raw
    if has_json:
        if args.curriculum != settings.DEFAULT_CURRICULUM:
            print(
                "Error: --curriculum is only valid with --raw",
                file=sys.stderr
            )
            return 1
        if args.generation_prompt:
            print(
                "Error: --generation-prompt is only valid with --raw",
                file=sys.stderr
            )
            return 1

    # Load content items
    try:
        if has_json:
            # JSON file mode - check if it's a folder
            json_path = Path(args.content_json)

            if not json_path.exists():
                print(f"Error: File not found: {json_path}", file=sys.stderr)
                return 1

            if json_path.is_dir():
                # Folder mode - evaluate all files in folder
                return _evaluate_folder(
                    json_path, args.output, args.verbose,
                    getattr(args, 'full', False), args.max_threads
                )

            if json_path.suffix.lower() != '.json':
                print(
                    f"Error: Expected .json file, got: {json_path.suffix}",
                    file=sys.stderr
                )
                print("For raw content, use: --raw <content>")
                return 1

            items = load_json_content(json_path)
            print(f"Loaded {len(items)} item(s) from {json_path}")

        else:
            # Raw content mode
            raw_value = args.raw
            extensions = ('.txt', '.md', '.html', '.json')

            # Check if it's a folder
            raw_path = Path(raw_value)
            if raw_path.is_dir():
                # Folder mode - evaluate all files in folder
                return _evaluate_folder(
                    raw_path, args.output, args.verbose,
                    getattr(args, 'full', False), args.max_threads
                )

            # Check if it's a file
            if raw_path.exists():
                if raw_path.suffix.lower() not in extensions:
                    print(
                        f"Error: Expected .txt, .md, .html, or .json file, "
                        f"got: {raw_path.suffix}",
                        file=sys.stderr
                    )
                    return 1
                content = raw_path.read_text(encoding='utf-8')
                print(f"Loaded content from {raw_path}")
            else:
                # Treat as string content
                content = raw_value

            if not content.strip():
                print("Error: Content cannot be empty", file=sys.stderr)
                return 1

            # Handle generation prompt (string or file)
            generation_prompt = None
            if args.generation_prompt:
                prompt_path = Path(args.generation_prompt)
                if prompt_path.exists():
                    prompt_extensions = ('.txt', '.md')
                    if prompt_path.suffix.lower() not in prompt_extensions:
                        print(
                            f"Error: Expected .txt or .md file for prompt, "
                            f"got: {prompt_path.suffix}",
                            file=sys.stderr
                        )
                        return 1
                    generation_prompt = prompt_path.read_text(encoding='utf-8')
                    print(f"Loaded prompt from {prompt_path}")
                else:
                    generation_prompt = args.generation_prompt

            items = [create_raw_content_item(
                content=content,
                curriculum=args.curriculum,
                generation_prompt=generation_prompt
            )]

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error loading content: {e}", file=sys.stderr)
        return 1

    # Run evaluation
    setup_logging(args.verbose)
    return asyncio.run(run_evaluation(
        items=items,
        output_file=args.output,
        verbose=args.verbose,
        full=getattr(args, 'full', False)
    ))


def _evaluate_folder(
    folder_path: Path,
    output_file: Optional[Path],
    verbose: bool,
    full: bool = False,
    max_threads: int = 10
) -> int:
    """
    Evaluate all files in a folder.

    Args:
        folder_path: Path to folder containing content files
        output_file: Optional file to save results
        verbose: Whether to show verbose output
        full: Whether to output complete JSON evaluation results
        max_threads: Maximum number of parallel evaluations

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    setup_logging(verbose)

    # Collect files to evaluate
    valid_extensions = {'.txt', '.md', '.html', '.json'}
    files_to_evaluate = [
        f for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() in valid_extensions
    ]

    if not files_to_evaluate:
        print(f"Error: No valid files found in {folder_path}", file=sys.stderr)
        print(f"Supported extensions: {', '.join(sorted(valid_extensions))}")
        return 1

    print(f"Found {len(files_to_evaluate)} file(s) in {folder_path}")
    print(f"Using {max_threads} parallel thread(s)")

    # Run evaluation
    return asyncio.run(_run_folder_evaluation(
        files=files_to_evaluate,
        output_file=output_file,
        verbose=verbose,
        full=full,
        max_threads=max_threads
    ))


async def _run_folder_evaluation(
    files: list[Path],
    output_file: Optional[Path],
    verbose: bool,
    full: bool = False,
    max_threads: int = 10
) -> int:
    """
    Run evaluation on all files in a folder with parallel processing.

    Args:
        files: List of file paths to evaluate
        output_file: Optional file to save results
        verbose: Whether to show verbose output
        full: Whether to output complete JSON evaluation results
        max_threads: Maximum number of parallel evaluations

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    from ..utils.failure_tracker import FailureTracker

    service = EvaluationService()

    # Progress tracking
    try:
        from tqdm import tqdm
        pbar = tqdm(total=len(files), desc="Evaluating Files", unit="file")
        use_pbar = True
    except ImportError:
        print(f"Processing {len(files)} file(s)...")
        use_pbar = False
        pbar = None

    # Semaphore for controlling concurrency
    semaphore = asyncio.Semaphore(max_threads)

    async def evaluate_file(file_path: Path):
        """Evaluate a single file with semaphore control."""
        async with semaphore:
            try:
                # Set current content for failure tracking
                FailureTracker.set_current_content(file_path.name)

                # Read file content
                content = file_path.read_text(encoding='utf-8')

                if verbose:
                    logging.info(f"Evaluating: {file_path.name}")

                # Evaluate
                result = await service.evaluate(content=content)

                if use_pbar:
                    pbar.update(1)

                return file_path.name, result.to_dict(), None

            except Exception as e:
                logging.error(f"Failed to evaluate {file_path.name}: {e}")
                # Record as ABORTED - file had unhandled error, couldn't complete
                FailureTracker.record_aborted(
                    content_id=file_path.name,
                    error_message=str(e)
                )
                if use_pbar:
                    pbar.update(1)
                return file_path.name, None, str(e)

            finally:
                FailureTracker.set_current_content(None)

    # Run all evaluations in parallel (controlled by semaphore)
    tasks = [evaluate_file(f) for f in files]
    results = await asyncio.gather(*tasks)

    if use_pbar:
        pbar.close()

    # Separate successful and failed evaluations
    evaluations = {}
    failed_items = []
    for filename, result, error in results:
        if error is None:
            evaluations[filename] = result
        else:
            failed_items.append({
                "item_id": filename,
                "error": error
            })

    # Build output (failures are shown separately, not in JSON)
    output_data = {
        "success_count": len(evaluations),
        "failure_count": len(failed_items),
        "evaluations": evaluations
    }

    # Get failure summary for display (includes ABORTED items)
    failure_summary = service.get_failure_summary()

    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
        print(f"\nResults saved to: {output_file}")

    # Output order: 1) Full JSON, 2) Failure summary, 3) Overall score summary

    # 1) Print full JSON if --full is specified
    if full:
        print("\n" + "=" * 70)
        print("FULL JSON OUTPUT")
        print("=" * 70)
        print(json.dumps(output_data, indent=2))

    # 2) Print failure summary (categorized)
    if failure_summary:
        print_categorized_failures(failure_summary, verbose)

    # 3) Print overall score summary
    print("\n" + "=" * 70)
    print("EVALUATION RESULTS")
    print("=" * 70)

    for name, result in evaluations.items():
        content_type = result.get('content_type', 'unknown')
        overall_score = result.get('overall', {}).get('score', 0)

        print(f"\n[{name}]")
        print(f"  Type: {content_type}")
        print(f"  Overall Score: {overall_score:.2f}")

        subcontent = result.get('subcontent_evaluations')
        if subcontent:
            print(f"  Nested Items: {len(subcontent)}")

    print("=" * 70)

    return 0 if len(evaluations) > 0 else 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="inceptbench",
        description="Educational Content Evaluator CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Version flag
    parser.add_argument(
        "-V", "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        title="commands",
        description="Available commands"
    )

    # Example command
    subparsers.add_parser(
        "example",
        help="Create a sample content.json file",
        description="Create a sample content.json file in the current directory"
    )

    # Evaluate command
    eval_parser = subparsers.add_parser(
        "evaluate",
        help="Evaluate educational content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="Evaluate educational content quality",
        epilog="""
Input (mutually exclusive - choose one):
  content_json              JSON file or FOLDER with content to evaluate
  --raw CONTENT             Raw content: string, file path, or FOLDER path

Supported file types:
  .json                     JSON file with API format
  .txt, .md, .html          Raw content files

Raw mode options (only valid with --raw for single files):
  --curriculum CURRICULUM   Curriculum for evaluation (default: common_core)
  --generation-prompt TEXT  Generation prompt: string or path to .txt/.md file

Examples:
  # Create a sample content.json to get started
  inceptbench example
  
  # Evaluate using JSON file (batch mode)
  inceptbench evaluate content.json
  
  # Evaluate raw content (single item)
  inceptbench evaluate --raw "What is 2+2?"
  inceptbench evaluate --raw question.txt --curriculum ngss
  inceptbench evaluate --raw content.md --generation-prompt prompt.txt

  # Evaluate all files in a folder (with parallelism)
  inceptbench evaluate ./my_content/
  inceptbench evaluate --raw ./my_articles/
  inceptbench evaluate ./my_content/ -o results.json
  inceptbench evaluate ./my_content/ --max-threads 20

JSON Format (same as API):
  {"generated_content": [{"content": "...", "curriculum": "...", "request": {...}}]}
  
  Or just the array:
  [{"content": "..."}, {"content": "..."}]

Note: Use 'inceptbench example' to generate a sample content.json file.
        """
    )

    # Positional argument for JSON file (optional)
    eval_parser.add_argument(
        "content_json",
        nargs="?",
        help="JSON file with content to evaluate"
    )

    # Raw content flag
    eval_parser.add_argument(
        "--raw",
        metavar="CONTENT",
        help="Raw content: string or path to .txt/.md file"
    )

    # Raw mode options
    eval_parser.add_argument(
        "--curriculum",
        default=settings.DEFAULT_CURRICULUM,
        help=f"Curriculum for evaluation (default: {settings.DEFAULT_CURRICULUM})"
    )
    eval_parser.add_argument(
        "--generation-prompt",
        metavar="TEXT",
        help="Generation prompt: string or path to .txt/.md file"
    )

    # Common options
    eval_parser.add_argument(
        "-o", "--output",
        type=Path,
        metavar="FILE",
        help="Save results to JSON file"
    )
    eval_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show verbose output and debug logging"
    )
    eval_parser.add_argument(
        "-f", "--full",
        action="store_true",
        help="Output complete JSON evaluation results"
    )
    eval_parser.add_argument(
        "--max-threads",
        type=int,
        default=10,
        metavar="N",
        help="Maximum parallel evaluations for folder mode (default: 10)"
    )

    return parser


def main(args: Optional[argparse.Namespace] = None) -> int:
    """
    Main CLI entry point.

    Args:
        args: Pre-parsed arguments (for use when called from legacy wrapper)

    Returns:
        Exit code
    """
    if args is None:
        parser = create_parser()
        args = parser.parse_args()

    if args.command is None:
        parser = create_parser()
        parser.print_help()
        return 0

    if args.command == "example":
        return example_command()
    elif args.command == "evaluate":
        return evaluate_command(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

