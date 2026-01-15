from __future__ import annotations

from enum import Enum

from .imperative_indicators import IMPERATIVE_INDICATORS
from .third_person_indicators import THIRD_PERSON_INDICATORS


class DocstringMood(Enum):
    """Represents the grammatical mood of a docstring."""

    IMPERATIVE = "imperative"
    THIRD_PERSON = "third_person"
    UNKNOWN = "unknown"


def detect_docstring_mood(docstring: str) -> DocstringMood:  # pylint: disable=too-many-return-statements
    """
    Detect the grammatical mood of a docstring.

    Analyzes the first sentence to determine if it uses imperative mood
    (e.g., "Return the value") or third-person mood (e.g., "Returns the value").

    Args:
        docstring: The docstring text to analyze.

    Returns:
        The detected mood: IMPERATIVE, THIRD_PERSON, or UNKNOWN.
    """
    if not docstring:
        return DocstringMood.UNKNOWN

    # Get first non-empty line and normalize
    lines = [line.strip() for line in docstring.strip().split("\n")]
    first_line = next((line for line in lines if line), "")

    if not first_line:
        return DocstringMood.UNKNOWN

    # Remove common punctuation
    first_line_clean = first_line.rstrip(".!?").strip()
    if not first_line_clean:
        return DocstringMood.UNKNOWN

    # Get words and skip articles
    words = first_line_clean.split()
    if not words:
        return DocstringMood.UNKNOWN

    # Skip articles at the beginning (A, An, The)
    articles = {"a", "an", "the"}
    start_index = 0
    if words[0].lower() in articles and len(words) > 1:
        start_index = 1

    first_word = words[start_index].lower()

    if first_word in THIRD_PERSON_INDICATORS:
        return DocstringMood.THIRD_PERSON
    if first_word in IMPERATIVE_INDICATORS:
        return DocstringMood.IMPERATIVE

    # Fallback: check if first word ends with 's' (likely third person)
    if first_word.endswith("s") and len(first_word) > 2:
        return DocstringMood.THIRD_PERSON

    return DocstringMood.UNKNOWN
