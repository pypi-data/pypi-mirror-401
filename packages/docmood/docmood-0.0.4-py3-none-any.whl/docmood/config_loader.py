from __future__ import annotations

import configparser
import sys
from pathlib import Path
from typing import Optional

from .config import DocmoodConfig
from .mood import DocstringMood

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None  # type: ignore[assignment]


# Configuration file names
CONFIG_FILE_PYPROJECT = "pyproject.toml"
CONFIG_FILE_INI = "docmood.ini"

# Configuration sources
CONFIG_SOURCE_PYPROJECT = "pyproject.toml"
CONFIG_SOURCE_INI = "docmood.ini"
CONFIG_SOURCE_DEFAULTS = "defaults"

# Configuration keys
CONFIG_SECTION_TOOL = "tool"
CONFIG_SECTION_DOCMOOD = "docmood"
CONFIG_KEY_MOOD = "mood"
CONFIG_KEY_ALLOW_UNKNOWN = "allow_unknown"
CONFIG_KEY_SKIP_DIRS = "skip_dirs"

# Mood values
MOOD_VALUE_IMPERATIVE = "imperative"
MOOD_VALUE_THIRD_PERSON = "third_person"
MOOD_VALUE_THIRD_PERSON_ALT = "third-person"

# Default configuration values
DEFAULT_ALLOW_UNKNOWN = True


def load_config(root: Path) -> DocmoodConfig:
    """
    Load configuration from project root.

    Searches for configuration in the following order:
    1. pyproject.toml with [tool.docmood] section
    2. docmood.ini file
    3. Default configuration

    Args:
        root: The root directory to search for configuration files.

    Returns:
        A DocmoodConfig instance with loaded settings.
    """
    # Try pyproject.toml first
    pyproject_path = root / CONFIG_FILE_PYPROJECT
    if pyproject_path.exists():
        config = _load_from_pyproject(pyproject_path)
        if config is not None:
            return config

    # Try docmood.ini
    ini_path = root / CONFIG_FILE_INI
    if ini_path.exists():
        config = _load_from_ini(ini_path)
        if config is not None:
            return config

    # Default to imperative mood with allow_unknown=True and no additional skip_dirs
    return DocmoodConfig(
        expected_mood=DocstringMood.IMPERATIVE,
        allow_unknown=DEFAULT_ALLOW_UNKNOWN,
        additional_skip_dirs=None,
        config_source=CONFIG_SOURCE_DEFAULTS,
    )


def _load_from_pyproject(path: Path) -> Optional[DocmoodConfig]:
    """Load configuration from pyproject.toml file."""
    if tomllib is None:
        return None

    try:
        with open(path, "rb") as f:
            data = tomllib.load(f)

        tool_config = data.get(CONFIG_SECTION_TOOL, {}).get(CONFIG_SECTION_DOCMOOD, {})
        if not tool_config:
            return None

        mood_str = tool_config.get(CONFIG_KEY_MOOD, "").lower()
        allow_unknown = tool_config.get(CONFIG_KEY_ALLOW_UNKNOWN, DEFAULT_ALLOW_UNKNOWN)
        additional_skip_dirs = tool_config.get(CONFIG_KEY_SKIP_DIRS, None)

        return _parse_mood_config(
            mood_str, allow_unknown, additional_skip_dirs, CONFIG_SOURCE_PYPROJECT
        )

    except (OSError, ValueError, KeyError):
        return None


def _load_from_ini(path: Path) -> Optional[DocmoodConfig]:
    """Load configuration from docmood.ini file."""
    try:
        parser = configparser.ConfigParser()
        parser.read(path)

        if not parser.has_section(CONFIG_SECTION_DOCMOOD):
            return None

        mood_str = parser.get(CONFIG_SECTION_DOCMOOD, CONFIG_KEY_MOOD, fallback="").lower()
        allow_unknown = parser.getboolean(
            CONFIG_SECTION_DOCMOOD, CONFIG_KEY_ALLOW_UNKNOWN, fallback=DEFAULT_ALLOW_UNKNOWN
        )

        # Parse skip_dirs as comma-separated list (additional dirs to skip)
        skip_dirs_str = parser.get(CONFIG_SECTION_DOCMOOD, CONFIG_KEY_SKIP_DIRS, fallback="")
        additional_skip_dirs = None
        if skip_dirs_str:
            additional_skip_dirs = [d.strip() for d in skip_dirs_str.split(",") if d.strip()]

        return _parse_mood_config(
            mood_str, allow_unknown, additional_skip_dirs, CONFIG_SOURCE_INI
        )

    except (OSError, configparser.Error):
        return None


def _parse_mood_config(
    mood_str: str,
    allow_unknown: bool = DEFAULT_ALLOW_UNKNOWN,
    additional_skip_dirs: Optional[list[str]] = None,
    config_source: str = CONFIG_SOURCE_DEFAULTS,
) -> Optional[DocmoodConfig]:
    """Parse mood string to DocstringMood enum."""
    mood_mapping = {
        MOOD_VALUE_IMPERATIVE: DocstringMood.IMPERATIVE,
        MOOD_VALUE_THIRD_PERSON: DocstringMood.THIRD_PERSON,
        MOOD_VALUE_THIRD_PERSON_ALT: DocstringMood.THIRD_PERSON,
    }

    mood = mood_mapping.get(mood_str)
    if mood is None:
        return None

    return DocmoodConfig(
        expected_mood=mood,
        allow_unknown=allow_unknown,
        additional_skip_dirs=additional_skip_dirs,
        config_source=config_source,
    )
