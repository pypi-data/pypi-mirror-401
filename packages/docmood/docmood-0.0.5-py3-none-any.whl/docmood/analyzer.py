from __future__ import annotations

from dataclasses import dataclass

from .config import DocmoodConfig
from .mood import DocstringMood
from .scanner import DocstringInfo


@dataclass
class DocstringResult:
    """Result for a single docstring check."""

    relative_path: str
    line_number: int
    docstring: str
    detected_mood: DocstringMood
    passed: bool


@dataclass
class CheckResult:
    """Result of checking docstrings in a project."""

    items: list[DocstringResult]
    total_count: int
    passed_count: int
    failed_count: int


def analyze_docstrings(
    docstrings: list[DocstringInfo], config: DocmoodConfig
) -> CheckResult:
    """
    Analyze docstrings against configuration rules.

    Args:
        docstrings: List of docstrings with detected moods.
        config: Configuration with expected mood and rules.

    Returns:
        CheckResult with pass/fail analysis for each docstring.
    """
    results: list[DocstringResult] = []

    for doc_info in docstrings:
        # Determine if this docstring passed
        if doc_info.detected_mood == config.expected_mood:
            passed = True
        elif doc_info.detected_mood == DocstringMood.UNKNOWN and config.allow_unknown:
            passed = True
        else:
            passed = False

        results.append(
            DocstringResult(
                relative_path=doc_info.relative_path,
                line_number=doc_info.line_number,
                docstring=doc_info.docstring,
                detected_mood=doc_info.detected_mood,
                passed=passed,
            )
        )

    total = len(results)
    passed_count = sum(1 for r in results if r.passed)
    failed_count = total - passed_count

    return CheckResult(
        items=results,
        total_count=total,
        passed_count=passed_count,
        failed_count=failed_count,
    )
