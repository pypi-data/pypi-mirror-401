"""
Main entry point for the inceptbench_new CLI.

This allows running the CLI with:
    python -m inceptbench_new evaluate ...
    python -m inceptbench_new example

Instead of:
    python -m inceptbench_new.cli.main evaluate ...
"""

import sys
from .cli import main as cli_main


if __name__ == "__main__":
    sys.exit(cli_main())

