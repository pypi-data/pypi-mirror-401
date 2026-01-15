from __future__ import annotations

from .analyzer import CheckResult


def get_exit_code(result: CheckResult) -> int:
    """
    Determine exit code based on check results.

    Args:
        result: The check result.

    Returns:
        0 if all passed, 1 if any failed.
    """
    return 1 if result.failed_count > 0 else 0
