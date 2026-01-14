"""
Base Connector Interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseConnector(ABC):
    """Abstract base class for all chatbot connectors."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize connector with configuration.

        Args:
            config: 'target' section of the YAML config
        """
        self.config = config
        self.name = config.get("name", "Unknown Target")
        self.connection_config = config.get("connection", {})

    @abstractmethod
    async def initialize(self) -> None:
        """Perform handshake, login, or session creation."""

    @abstractmethod
    async def send_message(
        self,
        message: str,
        context: Optional[Dict] = None,
        image_data: Optional[str] = None,
        image_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send a message to the target.

        Args:
            message: Text content
            context: Conversation context
            image_data: Base64 encoded image (optional)
            image_mime_type: MIME type of the image (optional)

        Returns:
            Dict containing:
            - content: str (The bot's response text)
            - metadata: dict (Raw response, latency, headers)
        """

    @abstractmethod
    async def close(self) -> None:
        """Clean up resources (close session, browser, socket)."""

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        mime_type: str = "application/octet-stream",
        context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to the target system (for RAG testing).

        Args:
            file_content: File bytes
            filename: Name of the file
            mime_type: MIME type (e.g., application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document)
            context: Additional context (e.g., folder, tags)

        Returns:
            Dict containing:
            - success: bool
            - file_id: str (if applicable)
            - message: str (response from server)
            - metadata: dict (upload details)

        Raises:
            NotImplementedError: If connector doesn't support file uploads
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support file uploads. "
            "Implement upload_file() method to enable RAG document poisoning tests."
        )

    async def health_check(self) -> bool:
        """Check if target is reachable."""
        try:
            await self.initialize()
            return True
        except Exception:
            return False


# Backward compatibility alias for existing code
TargetConnector = BaseConnector
