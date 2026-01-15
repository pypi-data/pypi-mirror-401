from __future__ import annotations

from .analyzer import CheckResult
from .config import DocmoodConfig
from .mood import DocstringMood


def print_results(config: DocmoodConfig, result: CheckResult) -> None:
    """
    Print check results.

    Args:
        config: The configuration used for checking.
        result: The check result to print.
    """
    # Print warnings for unknown mood docstrings
    unknown_items = [
        item for item in result.items if item.detected_mood == DocstringMood.UNKNOWN
    ]

    if unknown_items:
        unknown_count = len(unknown_items)
        plural = "s" if unknown_count != 1 else ""
        # print(f"\n⚠ Warning: Found {unknown_count} docstring{plural} with unknown mood:")
        for item in unknown_items:
            print(f"[docmood] warning: {item.relative_path}:{item.line_number} "
                  f"docstring mood could not be determined.")
        if config.allow_unknown:
            print("These are counted as passed because unknown moods are allowed by configuration.")
        print()

    # Print statistics
    if result.total_count == 0:
        print("[docmood] No docstrings found.")
    elif result.failed_count == 0:
        plural = "s" if result.total_count != 1 else ""
        print(f"[docmood] Found {result.total_count} method doc{plural}, all passed!")
    else:
        percentage = result.passed_count / result.total_count * 100
        mood_name = config.expected_mood.value.replace("_", " ")

        print("\nFailed docstrings:")
        for item in result.items:
            if not item.passed:
                mood_display = item.detected_mood.value.replace("_", " ")
                print(f"  {item.relative_path}:{item.line_number} "
                      f"(detected: {mood_display}, expected: {mood_name})")
        print("=" * 40)
        plural = "s" if result.total_count != 1 else ""
        print(f"[docmood] Found {result.total_count} doc{plural}: "
              f"{result.passed_count}/{result.total_count} passed ({percentage:.0f}%)")
