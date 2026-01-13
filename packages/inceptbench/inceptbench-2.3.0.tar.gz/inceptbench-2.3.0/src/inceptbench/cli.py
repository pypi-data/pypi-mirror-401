"""CLI for Incept Eval"""
import click
import json
import sys
import os
from pathlib import Path
import requests


def get_api_key(api_key=None):
    """Get API key - now optional since we run locally"""
    if api_key:
        return api_key
    if os.getenv('INCEPT_API_KEY'):
        return os.getenv('INCEPT_API_KEY')
    config_file = Path.home() / '.incept' / 'config'
    if config_file.exists():
        try:
            with open(config_file) as f:
                return json.load(f).get('api_key')
        except Exception:
            pass
    # API key is now optional - we run locally
    return None


@click.group()
@click.version_option(version='2.3.0')
def cli():
    """Incept Eval - Evaluate educational questions via Incept API

    \b
    CLI tool for evaluating educational questions with comprehensive
    assessment including DI compliance, answer verification, and
    specialized evaluators for math, reading, and image content.

    \b
    Commands:
      evaluate    Evaluate questions from a JSON file or raw content
      benchmark   Process many questions in parallel (high throughput)
      example     Generate sample input JSON file
      help        Show detailed help and usage examples

    \b
    Quick Start:
      1. Generate a sample file:
         $ inceptbench example

      2. Evaluate using the JSON file:
         $ inceptbench evaluate content.json

      3. Evaluate raw content:
         $ inceptbench evaluate --raw "What is 2+2?"

    \b
    For detailed help, run: inceptbench help
    """
    pass


@cli.command()
@click.argument('content_json', type=click.Path(), required=False)
@click.option('--raw', 'raw_content', metavar='CONTENT',
              help='Raw content: string or path to .txt/.md file')
@click.option('--curriculum', default='common_core',
              help='Curriculum for evaluation (default: common_core)')
@click.option('--generation-prompt', 'gen_prompt', metavar='TEXT',
              help='Generation prompt: string or path to .txt/.md file')
@click.option('--output', '-o', type=click.Path(),
              help='Save results to file (overwrites)')
@click.option('--verbose', '-v', is_flag=True,
              help='Show verbose output and debug logging')
@click.option('--full', '-f', is_flag=True,
              help='Output complete JSON evaluation results')
@click.option('--max-threads', type=int, default=10,
              help='Maximum number of parallel evaluation threads (default: 10)')
@click.option('--legacy', is_flag=True,
              help='Use legacy evaluator (deprecated)')
@click.option('--append', '-a', type=click.Path(),
              help='(Legacy only) Append results to file')
@click.option('--api-key', '-k', envvar='INCEPT_API_KEY',
              help='(Legacy only) API key for authentication')
@click.option('--api-url', default='https://uae-poc.inceptapi.com',
              help='(Legacy only) API endpoint URL')
@click.option('--timeout', '-t', type=int, default=600,
              help='(Legacy only) Request timeout in seconds')
@click.option('--subject', '-s',
              type=click.Choice(['math', 'ela', 'science', 'social-studies',
                                'history', 'general'], case_sensitive=False),
              help='(Legacy only) Subject area for automatic evaluator selection')
@click.option('--grade', '-g',
              help='(Legacy only) Grade level (e.g., "K", "3", "6-8", "9-12")')
@click.option('--type', 'content_type',
              type=click.Choice(['mcq', 'fill-in', 'short-answer', 'essay',
                                'text-content', 'passage', 'article'],
                               case_sensitive=False),
              help='(Legacy only) Content type for automatic evaluator selection')
@click.option('--advanced', is_flag=True, hidden=True,
              help='DEPRECATED: Use folder path without --legacy instead')
def evaluate(content_json, raw_content, curriculum, gen_prompt, output,
             verbose, full, max_threads, legacy, append, api_key, api_url,
             timeout, subject, grade, content_type, advanced):
    """Evaluate educational content with comprehensive assessment

    By default, uses the new evaluation system. Use --legacy for the
    deprecated legacy evaluator.

    \b
    Input (mutually exclusive - choose one):
      content_json              JSON file or FOLDER with content to evaluate
      --raw CONTENT             Raw content: string, file path, or FOLDER path

    \b
    Supported file types:
      .json                     JSON file with API format
      .txt, .md, .html          Raw content files

    \b
    Raw mode options (only valid with --raw for single files):
      --curriculum CURRICULUM   Curriculum for evaluation (default: common_core)
      --generation-prompt TEXT  Generation prompt: string or .txt/.md file

    \b
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

        # Save results to file
        inceptbench evaluate content.json -o results.json

        # Use legacy evaluator (deprecated)
        inceptbench evaluate questions.json --legacy --subject math
    """
    # Check for deprecated --advanced flag
    if advanced:
        click.echo(
            "❌ Error: The --advanced flag has been removed.\n\n"
            "To evaluate a folder of files, use the new evaluator (default):\n"
            "  inceptbench evaluate ./my_folder/\n"
            "  inceptbench evaluate --raw ./my_folder/\n\n"
            "The legacy evaluator (--legacy) does not support folder input.\n"
            "Remove --legacy and --advanced to use the new evaluator.",
            err=True
        )
        sys.exit(1)

    # Route to new or legacy evaluator
    if legacy:
        # Run legacy evaluator
        _evaluate_legacy(
            input_file=content_json,
            output=output,
            append=append,
            api_key=api_key,
            api_url=api_url,
            timeout=timeout,
            verbose=verbose,
            full=full,
            subject=subject,
            grade=grade,
            content_type=content_type,
            max_threads=max_threads
        )
    else:
        # Delegate to new CLI
        _evaluate_new(
            content_json=content_json,
            raw_content=raw_content,
            curriculum=curriculum,
            gen_prompt=gen_prompt,
            output=output,
            verbose=verbose,
            full=full,
            max_threads=max_threads
        )


def _evaluate_new(content_json, raw_content, curriculum, gen_prompt,
                  output, verbose, full=False, max_threads=10):
    """Delegate to the new inceptbench_new CLI."""
    import argparse

    # Build args for new CLI
    args = argparse.Namespace(
        command='evaluate',
        content_json=content_json,
        raw=raw_content,
        curriculum=curriculum,
        generation_prompt=gen_prompt,
        output=Path(output) if output else None,
        verbose=verbose,
        full=full,
        max_threads=max_threads
    )

    # Import and run new CLI
    from inceptbench_new.cli.main import main as new_cli_main
    sys.exit(new_cli_main(args))


def _evaluate_legacy(input_file, output, append, api_key, api_url,
                     timeout, verbose, full, subject, grade,
                     content_type, max_threads):
    """Run the legacy evaluator."""
    try:
        click.echo(
            "⚠️  Warning: Legacy evaluator is deprecated. "
            "Remove --legacy flag to use the new evaluator.",
            err=True
        )

        if not input_file:
            click.echo(
                "❌ Error: Legacy mode requires an input file",
                err=True
            )
            sys.exit(1)

        if not Path(input_file).exists():
            click.echo(f"❌ Error: File not found: {input_file}", err=True)
            sys.exit(1)

        api_key = get_api_key(api_key)

        # Standard mode (structured JSON input)
        if verbose:
            click.echo(f"📂 Loading: {input_file}")

        with open(input_file) as f:
            data = json.load(f)

        # Add verbose flag and routing parameters to the data
        data['verbose'] = full
        if subject:
            data['subject'] = subject
        if grade:
            data['grade'] = grade
        if content_type:
            data['type'] = content_type
        data['use_new_evaluator'] = False
        data['max_threads'] = max_threads

        # Import here to avoid loading orchestrator for non-evaluation commands
        from .client import InceptClient
        client = InceptClient(api_key, api_url, timeout=timeout)
        result = client.evaluate_dict(data)

        # Extract debug info (soft failures) - separate from main output
        soft_failures = result.pop('_debug_soft_failures', None)

        # Always output full results - pretty only controls formatting
        json_output = json.dumps(result, indent=2, ensure_ascii=False)

        # Build evaluation summary for display
        def build_evaluation_summary(result_data):
            """Build a summary of scores and ratings (sorted by key)."""
            summary = {}
            evaluations = result_data.get('evaluations', {})
            for name, eval_data in evaluations.items():
                # Handle inceptbench_new_evaluation format
                if 'inceptbench_new_evaluation' in eval_data:
                    new_eval = eval_data['inceptbench_new_evaluation']
                    if 'error' not in new_eval:
                        summary[name] = {
                            "overall_score": new_eval.get(
                                'overall', {}
                            ).get('score'),
                            "overall_rating": new_eval.get('overall_rating')
                        }
                # Handle legacy format with 'score' field
                elif 'score' in eval_data:
                    summary[name] = {
                        "overall_score": eval_data.get('score'),
                        "overall_rating": None
                    }
            return dict(sorted(summary.items()))

        # Handle output options
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            if verbose:
                click.echo(f"✅ Saved to: {output}")
        elif append:
            existing_data = []
            if Path(append).exists():
                try:
                    with open(append, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                        if not isinstance(existing_data, list):
                            existing_data = [existing_data]
                except json.JSONDecodeError:
                    if verbose:
                        click.echo(
                            "⚠️  File exists but is invalid JSON, "
                            "creating new file"
                        )
                    existing_data = []

            existing_data.append(result)

            with open(append, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, indent=2, ensure_ascii=False)

            if verbose:
                click.echo(
                    f"✅ Appended to: {append} "
                    f"(total: {len(existing_data)} evaluations)"
                )
        else:
            click.echo(json_output)

        # Print soft failures (internal debugging info) if any occurred
        if soft_failures:
            click.echo("\n" + "=" * 80)
            click.echo("⚠️  SOFT FAILURES (Internal Debugging Info)")
            click.echo("=" * 80)
            click.echo(f"Total failures: {soft_failures.get('total_failures', 0)}")
            click.echo(f"Failures by component: {json.dumps(soft_failures.get('failures_by_component', {}))}")
            click.echo("\nDetails:")
            click.echo(json.dumps(soft_failures.get('failures', []), indent=2))

        # Print evaluation summary at the end
        if 'evaluations' in result:
            summary = build_evaluation_summary(result)
            if summary:
                click.echo("\n" + "=" * 80)
                click.echo("EVALUATION SUMMARY")
                click.echo("=" * 80)
                click.echo(json.dumps(summary, indent=4))

    except requests.HTTPError as e:
        click.echo(f"❌ API Error: {e.response.status_code}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(),
              help='Save results to file')
@click.option('--workers', '-w', type=int, default=100,
              help='Number of parallel workers (default: 100)')
@click.option('--verbose', '-v', is_flag=True,
              help='Show progress messages')
@click.option('--subject', '-s',
              type=click.Choice(['math', 'ela', 'science', 'social-studies',
                                'history', 'general'], case_sensitive=False),
              help='Subject area for automatic evaluator selection')
@click.option('--grade', '-g',
              help='Grade level (e.g., "K", "3", "6-8", "9-12")')
@click.option('--type', 'content_type',
              type=click.Choice(['mcq', 'fill-in', 'short-answer', 'essay',
                                'text-content', 'passage', 'article'],
                               case_sensitive=False),
              help='Content type for automatic evaluator selection')
def benchmark(input_file, output, workers, verbose, subject, grade,
              content_type):
    """Benchmark mode: Process many questions in parallel (LEGACY)

    Note: This command uses the legacy evaluator. For new evaluations,
    use 'inceptbench evaluate content.json' which processes items in
    parallel by default.

    Example:
        inceptbench benchmark questions.json --workers 100 -o results.json
    """
    try:
        click.echo(
            "⚠️  Warning: benchmark command uses legacy evaluator. "
            "Use 'inceptbench evaluate' for new evaluations.",
            err=True
        )

        if verbose:
            click.echo(f"📂 Loading: {input_file}")

        with open(input_file) as f:
            data = json.load(f)

        # Add routing parameters to the data
        if subject:
            data['subject'] = subject
        if grade:
            data['grade'] = grade
        if content_type:
            data['type'] = content_type
        data['use_new_evaluator'] = False
        data['max_threads'] = workers

        # Import here to avoid loading evaluator for non-benchmark commands
        from .client import InceptClient
        client = InceptClient()

        # Use benchmark mode
        if verbose:
            questions = data.get('generated_questions', [])
            click.echo(
                f"🚀 Benchmark mode: {len(questions)} questions "
                f"with {workers} workers"
            )

        result = client.benchmark(data, max_workers=workers)

        # Format output
        json_output = json.dumps(result, indent=2, ensure_ascii=False)

        # Handle output
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(json_output)
            if verbose:
                click.echo(f"✅ Saved to: {output}")
                click.echo(
                    f"📊 Results: {result['successful']}/"
                    f"{result['total_questions']} successful"
                )
                click.echo(
                    f"⏱️  Time: {result['evaluation_time_seconds']:.2f}s"
                )
                click.echo(f"📈 Avg Score: {result['avg_score']:.3f}")
                if result['failed_ids']:
                    click.echo(
                        f"❌ Failed IDs: {', '.join(result['failed_ids'])}"
                    )
        else:
            click.echo(json_output)

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def configure():
    """Save API key to config file (LEGACY)

    Note: API key configuration is only needed for legacy evaluator.
    The new evaluator uses environment variables directly.
    """
    api_key = click.prompt("Enter your API key")
    try:
        config_dir = Path.home() / '.incept'
        config_dir.mkdir(exist_ok=True)
        config_file = config_dir / 'config'

        with open(config_file, 'w') as f:
            json.dump({'api_key': api_key}, f)

        config_file.chmod(0o600)
        click.echo(f"✅ API key saved to {config_file}")
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)


@cli.command()
def help():
    """Show detailed help and usage examples"""
    help_text = """
╔═══════════════════════════════════════════════════════════════════╗
║                    INCEPT-EVAL CLI HELP                           ║
║                      Version 2.1.0                                ║
╚═══════════════════════════════════════════════════════════════════╝

OVERVIEW:
  InceptBench is a comprehensive evaluation framework for educational
  content. It evaluates content across 11+ quality dimensions including
  accuracy, curriculum alignment, clarity, and misconception detection.

INSTALLATION:
  pip install inceptbench

COMMANDS:

  1. example - Generate sample input file
     Usage: inceptbench example

     Creates a sample content.json file in the current directory that
     you can edit and use with the evaluate command.

     Example:
       inceptbench example

  2. evaluate - Evaluate content
     Usage: inceptbench evaluate [OPTIONS] [CONTENT_JSON]

     Input (mutually exclusive - choose one):
       content_json              JSON file or FOLDER with content
       --raw CONTENT             Raw content: string, file, or FOLDER

     Supported file types:
       .json                     JSON file with API format
       .txt, .md, .html          Raw content files

     Raw mode options (only valid with --raw for single files):
       --curriculum CURRICULUM   Curriculum for evaluation (default: common_core)
       --generation-prompt TEXT  Generation prompt: string or .txt/.md file

     Common options:
       -o, --output FILE         Save results to JSON file
       -v, --verbose             Show verbose output and debug logging
       --legacy                  Use legacy evaluator (deprecated)

     Examples:
       # Evaluate using JSON file (batch mode)
       inceptbench evaluate content.json

       # Evaluate raw content (single item)
       inceptbench evaluate --raw "What is 2+2?"
       inceptbench evaluate --raw question.txt --curriculum ngss
       inceptbench evaluate --raw content.md --generation-prompt prompt.txt

       # Evaluate all files in a folder (with parallelism)
       inceptbench evaluate ./my_content/
       inceptbench evaluate --raw ./my_articles/
       inceptbench evaluate ./my_content/ --max-threads 20

       # Save results to file
       inceptbench evaluate content.json -o results.json

  3. benchmark - High-throughput parallel evaluation (LEGACY)
     Usage: inceptbench benchmark INPUT_FILE [OPTIONS]

     Note: This uses the legacy evaluator. The new 'evaluate' command
     processes items in parallel by default.

INPUT FILE FORMAT (JSON):

  The JSON file should match the API input format:

  {
    "generated_content": [
      {
        "id": "q1",              // Optional: auto-generated if omitted
        "curriculum": "common_core",  // Optional: defaults to common_core
        "request": {            // Optional: metadata about generation
          "grade": "7",
          "subject": "mathematics",
          "instructions": "Create a math question"
        },
        "content": "What is 2 + 2?"  // Required: string or JSON
      }
    ]
  }

  Or just the array:
  [{"content": "..."}, {"content": "..."}]

  Use 'inceptbench example' to generate a complete sample file.

OUTPUT FORMAT:

  The response includes:
  - success_count: Number of successful evaluations
  - failure_count: Number of failed evaluations
  - evaluations: Per-item results with scores and reasoning
  - failed_items: List of items that failed (if any)

  Each evaluation contains:
  - content_type: Detected type (question, quiz, article, etc.)
  - overall: Score and reasoning
  - factual_accuracy: Accuracy score
  - educational_accuracy: Educational value score
  - curriculum_alignment: Alignment with specified curriculum
  - (and more dimension-specific scores)

QUICK START:

  # 1. Generate sample file
  inceptbench example

  # 2. Edit the file to add your content

  # 3. Run evaluation
  inceptbench evaluate content.json -v

  # 4. Save results
  inceptbench evaluate content.json -o results.json

For more information, visit: https://github.com/incept-ai/inceptbench
"""
    click.echo(help_text)


@cli.command()
@click.option('--output', '-o', type=click.Path(), default=None,
              help='Save to file (default: content.json)')
def example(output):
    """Generate sample input file

    Creates a sample content.json file that you can edit and use with
    the evaluate command. The file demonstrates the API input format.
    """
    # Use new CLI's example command
    from inceptbench_new.cli.main import example_command
    result = example_command()
    sys.exit(result)


if __name__ == '__main__':
    cli()
