"""Factory for creating target connectors."""

from typing import Dict, Any, Literal
from .base import TargetConnector
from .api_connector import APITargetConnector
from .web_connector import WebUITargetConnector


def create_connector(
    target_type: Literal["api", "web_ui"], config: Dict[str, Any]
) -> TargetConnector:
    """
    Create appropriate connector based on target type.

    Args:
        target_type: Type of target ("api" or "web_ui")
        config: Configuration dict for the connector

    Returns:
        Initialized connector instance

    Raises:
        ValueError: If target_type is unknown

    Example:
        >>> # API connector
        >>> connector = create_connector("api", {
        ...     "endpoint": "http://localhost:5000/chat",
        ...     "api_key": "sk-..."
        ... })

        >>> # Web UI connector
        >>> connector = create_connector("web_ui", {
        ...     "url": "https://chatbot.example.com",
        ...     "selectors": "chatgpt"  # Or custom selectors dict
        ... })
    """
    if target_type == "api":
        return APITargetConnector(config)
    elif target_type == "web_ui":
        return WebUITargetConnector(config)
    else:
        raise ValueError(f"Unknown target type: {target_type}")
