"""Configuration management for Acuity CLI.

Handles credential loading with precedence:
  flags > env vars > config file (~/.config/acuity/config.json)
"""

from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

API_BASE_URL = "https://acuityscheduling.com/api/v1"
DEFAULT_TIMEZONE = "America/Chicago"
DEFAULT_OUTPUT = "json"
CONFIG_DIR = Path.home() / ".config" / "acuity"
CONFIG_FILE = CONFIG_DIR / "config.json"


@dataclass
class Config:
    """CLI configuration."""

    user_id: str
    api_key: str
    default_timezone: str = DEFAULT_TIMEZONE
    default_calendar: int | None = None
    output: str = DEFAULT_OUTPUT
    quiet: bool = False
    no_color: bool = False
    no_input: bool = False

    def validate(self) -> None:
        """Validate required fields."""
        if not self.user_id:
            raise ValueError("ACUITY_USER_ID is required")
        if not self.api_key:
            raise ValueError("ACUITY_API_KEY is required")
        if len(self.api_key) < 10:
            raise ValueError("ACUITY_API_KEY appears invalid (too short)")


def load_config_file(config_path: Path | None = None) -> dict:
    """Load config from ~/.config/acuity/config.json if it exists."""
    resolved_path = config_path or CONFIG_FILE
    if resolved_path.exists():
        try:
            with open(resolved_path) as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"Failed to load config file: {e}")
    return {}


def load_config(
    user_id: str | None = None,
    api_key: str | None = None,
    output: str | None = None,
    config_path: str | None = None,
    quiet: bool = False,
    no_color: bool = False,
    no_input: bool = False,
) -> Config:
    """Load configuration with precedence: args > env > config file.

    Args:
        user_id: Override from CLI flag
        api_key: Override from CLI flag
        output: Output format override
        config_path: Config file path override
        quiet: Suppress non-essential output
        no_color: Disable colored output
        no_input: Disable interactive prompts

    Returns:
        Config object with resolved values

    """
    # Load .env file if present
    load_dotenv()

    resolved_config_path = config_path or os.getenv("ACUITY_CONFIG")
    config_file_path = Path(resolved_config_path) if resolved_config_path else None

    # Load config file defaults
    file_config = load_config_file(config_file_path)

    # Resolve with precedence: args > env > file
    resolved_user_id = (
        user_id or os.getenv("ACUITY_USER_ID") or file_config.get("user_id", "")
    )

    resolved_api_key = (
        api_key or os.getenv("ACUITY_API_KEY") or file_config.get("api_key", "")
    )

    resolved_output = (
        output
        or os.getenv("ACUITY_OUTPUT")
        or file_config.get("output", DEFAULT_OUTPUT)
    )

    resolved_timezone = os.getenv("ACUITY_TIMEZONE") or file_config.get(
        "default_timezone", DEFAULT_TIMEZONE
    )

    resolved_calendar = file_config.get("default_calendar")

    return Config(
        user_id=resolved_user_id,
        api_key=resolved_api_key,
        default_timezone=resolved_timezone,
        default_calendar=resolved_calendar,
        output=resolved_output,
        quiet=quiet,
        no_color=no_color,
        no_input=no_input,
    )
