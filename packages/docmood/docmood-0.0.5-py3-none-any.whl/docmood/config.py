from __future__ import annotations

from typing import Optional

from .mood import DocstringMood


_DEFAULT_SKIP_DIRS = [
    ".git",
    ".hg",
    ".svn",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    "__pycache__",
    "build",
    "dist",
    "site-packages",
    "venv",
    ".venv",
]


class DocmoodConfig:  # pylint: disable=too-few-public-methods
    """Configuration for docmood tool."""

    def __init__(
        self,
        expected_mood: DocstringMood,
        allow_unknown: bool = True,
        additional_skip_dirs: Optional[list[str]] = None,
        config_source: str = "defaults",
    ) -> None:
        """
        Create a configuration instance.

        Args:
            expected_mood: The expected mood for all docstrings.
            allow_unknown: Whether to treat unknown mood as passed (default: True).
            additional_skip_dirs: Additional directory names to skip (added to defaults).
            config_source: Where the config was loaded from (for display).
        """
        self.expected_mood = expected_mood
        self.allow_unknown = allow_unknown
        self.config_source = config_source
        # Combine default skip dirs with additional ones
        self.skip_dirs = list(_DEFAULT_SKIP_DIRS)
        if additional_skip_dirs:
            self.skip_dirs.extend(additional_skip_dirs)

    def __str__(self):
        return (f"expected_mood: {self.expected_mood.value}, "
                f"allow_unknown: {self.allow_unknown}, "
                f"config_source: {self.config_source}")
