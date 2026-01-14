"""Configuration management for Synphony MCP server"""

import json
import os
from pathlib import Path
from typing import Optional


CONFIG_DIR = Path.home() / ".synphony"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """Load configuration from file or environment variables"""

    # Try loading from config file first
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = json.load(f)
            return {
                "api_key": config.get("api_key"),
                "api_base_url": config.get("api_base_url", "https://dev.synphony.co/api/cli")
            }

    # Fallback to environment variables
    api_key = os.getenv("SYNPHONY_API_KEY")
    if not api_key:
        raise ValueError(
            f"No API key found. Either:\n"
            f"1. Create {CONFIG_FILE} with your API key, or\n"
            f"2. Set SYNPHONY_API_KEY environment variable"
        )

    return {
        "api_key": api_key,
        "api_base_url": os.getenv("SYNPHONY_API_BASE_URL", "https://dev.synphony.co/api/cli")
    }


def save_config(api_key: str, api_base_url: str = "https://dev.synphony.co/api/cli"):
    """Save configuration to file"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    config = {
        "api_key": api_key,
        "api_base_url": api_base_url
    }

    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
