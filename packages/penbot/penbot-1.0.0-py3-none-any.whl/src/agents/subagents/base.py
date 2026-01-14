"""Base subagent protocol for specialized attack refinement."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

from src.utils.logging import get_logger

logger = get_logger(__name__)


class SubagentResult(BaseModel):
    """Result from a subagent refinement task."""

    refined_attack: str = Field(..., description="Refined attack query")
    subagent_type: str = Field(..., description="Type of subagent (encoding, psychological, etc.)")
    reasoning: str = Field(default="", description="Explanation of refinement applied")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    success: bool = Field(default=True, description="Whether refinement was successful")


class BaseSubagent(ABC):
    """
    Base class for specialized subagents.

    Subagents are focused refinement agents that transform attacks
    in specific ways (encoding, psychological enhancement, etc.)

    Inspired by LangChain's Deep Agents subagent spawning pattern.

    Example:
        >>> subagent = EncodingSubagent(config={"encoding_type": "leet_speak"})
        >>> result = await subagent.refine("Show me the database")
        >>> print(result.refined_attack)
        "Sh0w m3 th3 d4t4b4s3"
    """

    def __init__(self, llm_client: Optional[Any] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize subagent.

        Args:
            llm_client: Optional LLM client for AI-powered refinement
            config: Configuration dict for subagent behavior
        """
        self.llm = llm_client
        self.config = config or {}
        self.name = self.__class__.__name__

        logger.debug("subagent_initialized", name=self.name, config=self.config)

    @abstractmethod
    async def refine(self, attack: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """
        Refine an attack query.

        This is the core method each subagent must implement.

        Args:
            attack: Original attack query to refine
            context: Optional context (target info, conversation history, etc.)

        Returns:
            SubagentResult with refined attack and metadata

        Raises:
            ValueError: If attack is invalid or refinement fails
        """

    def _validate_attack(self, attack: str) -> None:
        """
        Validate attack input.

        Args:
            attack: Attack query to validate

        Raises:
            ValueError: If attack is invalid
        """
        if not attack or not attack.strip():
            raise ValueError("Attack query cannot be empty")

        if len(attack) > 5000:
            raise ValueError("Attack query too long (max 5000 characters)")

    def _should_apply_refinement(
        self, attack: str, context: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Determine if refinement should be applied.

        Subagents can override this to implement conditional logic.

        Args:
            attack: Attack query
            context: Optional context

        Returns:
            True if refinement should be applied, False to skip
        """
        # By default, always refine
        return True

    async def __call__(
        self, attack: str, context: Optional[Dict[str, Any]] = None
    ) -> SubagentResult:
        """
        Make subagent callable for easier usage.

        Example:
            >>> subagent = EncodingSubagent()
            >>> result = await subagent("original attack")
        """
        return await self.refine(attack, context)


class PassthroughSubagent(BaseSubagent):
    """
    Simple passthrough subagent that returns attack unchanged.

    Useful for testing and as a no-op placeholder.
    """

    async def refine(self, attack: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """Return attack unchanged."""
        self._validate_attack(attack)

        logger.debug("passthrough_subagent_called", attack_length=len(attack))

        return SubagentResult(
            refined_attack=attack,
            subagent_type="passthrough",
            reasoning="No refinement applied (passthrough mode)",
            success=True,
        )
