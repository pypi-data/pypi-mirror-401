"""
Configuration loader and validator.
"""

import yaml
import os
from typing import Dict, Any
from pathlib import Path


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Load and validate a client configuration file.

    Args:
        config_path: Path to YAML config file

    Returns:
        Dict containing configuration
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(path, "r", encoding="utf-8") as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")

    # Resolve environment variables in config
    config = _resolve_env_vars(config)

    # Basic structure validation
    _validate_structure(config)

    return config


def _resolve_env_vars(config: Any) -> Any:
    """Recursively resolve ${VAR} environment variables."""
    if isinstance(config, dict):
        return {k: _resolve_env_vars(v) for k, v in config.items()}
    elif isinstance(config, list):
        return [_resolve_env_vars(i) for i in config]
    elif isinstance(config, str) and config.startswith("${") and config.endswith("}"):
        var_name = config[2:-1]
        env_val = os.getenv(var_name)
        if not env_val:
            # Don't fail yet, maybe the user wants to enter it manually later
            # For now, return as is or raise warning
            pass
        return env_val if env_val else config
    else:
        return config


def _validate_structure(config: Dict[str, Any]):
    """Validate required fields in config."""
    required_sections = ["client", "target", "test"]
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Config missing required section: '{section}'")

    if "platform" not in config["target"]:
        raise ValueError("Config missing 'target.platform'")

    if "connection" not in config["target"]:
        raise ValueError("Config missing 'target.connection'")
