from __future__ import annotations

from .config import DocmoodConfig


def print_config(config: DocmoodConfig) -> None:
    """
    Print configuration information.

    Args:
        config: The loaded configuration.
    """
    print(f"[docmood] Configuration loaded from: {config.config_source}")
    print(f"[docmood] {config}")
