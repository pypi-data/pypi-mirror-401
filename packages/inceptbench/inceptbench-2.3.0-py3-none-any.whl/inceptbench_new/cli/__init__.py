"""
CLI module for Educational Content Evaluator.

Provides command-line interface for evaluating educational content,
supporting both JSON batch input and raw content mode.
"""

from .main import (
    main,
    example_command,
    evaluate_command,
    create_parser,
    get_sample_content,
    load_json_content,
    create_raw_content_item,
)

__all__ = [
    "main",
    "example_command",
    "evaluate_command",
    "create_parser",
    "get_sample_content",
    "load_json_content",
    "create_raw_content_item",
]

