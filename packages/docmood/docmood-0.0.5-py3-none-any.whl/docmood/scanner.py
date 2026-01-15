from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .mood import DocstringMood, detect_docstring_mood
from .scan import scan_project


@dataclass
class DocstringInfo:
    """Information about a discovered docstring with detected mood."""

    relative_path: str
    line_number: int
    docstring: str
    detected_mood: DocstringMood


def scan_and_detect_moods(root: Path, skip_dirs: list[str]) -> list[DocstringInfo]:
    """
    Scan project and detect mood for each docstring.

    Args:
        root: Root directory of the project to scan.
        skip_dirs: List of directory names to skip during scanning.

    Returns:
        List of DocstringInfo with detected moods.
    """
    doc_items = scan_project(root, skip_dirs=skip_dirs)
    results: list[DocstringInfo] = []

    for item in doc_items:
        relative_path = os.path.relpath(item.path, start=root)
        detected_mood = detect_docstring_mood(item.doc)

        results.append(
            DocstringInfo(
                relative_path=relative_path,
                line_number=item.doc_lineno,
                docstring=item.doc,
                detected_mood=detected_mood,
            )
        )

    return results
