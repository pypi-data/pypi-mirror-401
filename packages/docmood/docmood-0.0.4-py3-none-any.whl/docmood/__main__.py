from __future__ import annotations

import argparse
from pathlib import Path

from .analyzer import analyze_docstrings
from .config_loader import load_config
from .exit_code import get_exit_code
from .print_config import print_config
from .print_results import print_results
from .scanner import scan_and_detect_moods


def main() -> None:
    """Main entry point for the docmood package."""
    parser = argparse.ArgumentParser(prog="docmood")
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project directory to scan (default: current directory).",
    )
    args = parser.parse_args()

    root = Path(args.path).resolve()

    # Load configuration
    config = load_config(root)

    # Print configuration
    print_config(config)

    # Scan and detect moods for all docstrings
    docstrings = scan_and_detect_moods(root, config.skip_dirs)

    # Analyze docstrings against configuration rules
    result = analyze_docstrings(docstrings, config)

    # Determine exit code
    exit_code = get_exit_code(result)

    # Print results
    print_results(config, result)

    # Exit with appropriate code
    if exit_code != 0:
        raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
