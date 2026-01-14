"""Base class for vulnerability detectors."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from src.utils.logging import get_logger
from src.utils.text_normalization import normalize_text, get_normalization_stats

logger = get_logger(__name__)


class VulnerabilityDetector(ABC):
    """
    Base class for vulnerability detectors.

    Each detector analyzes target responses for specific types of vulnerabilities.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize detector.

        Args:
            config: Detector-specific configuration
        """
        self.config = config or {}
        self.name = self.__class__.__name__.replace("Detector", "").lower()

        logger.info("detector_initialized", detector=self.name)

    @abstractmethod
    async def analyze(
        self, attack: Dict[str, Any], response: Dict[str, Any], context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Analyze response for vulnerabilities.

        Args:
            attack: Attack attempt that was sent
            response: Target's response
            context: Additional context (target info, conversation history, etc.)

        Returns:
            List of SecurityFinding dicts
        """

    def _normalize_content(self, content: str) -> str:
        """
        Normalize text content to prevent evasion.

        Applies unicode normalization, homoglyph replacement,
        zero-width character removal, and bidi stripping.

        Args:
            content: Raw content to normalize

        Returns:
            Normalized content ready for pattern matching
        """
        original_length = len(content)
        normalized = normalize_text(content, aggressive=True)

        # Log if significant obfuscation detected
        if len(normalized) < original_length * 0.9:
            stats = get_normalization_stats(content, normalized)
            if stats["total_changes"] > 5:
                logger.warning(
                    "obfuscation_detected",
                    detector=self.name,
                    total_changes=stats["total_changes"],
                    stats=stats,
                )

        return normalized

    def _create_finding(
        self,
        attack_id: str,
        severity: str,
        category: str,
        description: str,
        evidence: str,
        confidence: float,
        raw_evidence: str = None,
        conversation_context: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a security finding dict with evidence pack.

        Args:
            attack_id: ID of the attack that triggered this finding
            severity: Severity level (critical, high, medium, low, info)
            category: Finding category
            description: Human-readable description
            evidence: Processed evidence from response
            confidence: Confidence score (0-1)
            raw_evidence: Optional raw evidence before normalization
            conversation_context: Optional conversation history slice

        Returns:
            SecurityFinding dict with full evidence pack
        """
        from src.utils.helpers import generate_uuid
        from datetime import datetime, timezone

        finding = {
            "finding_id": generate_uuid(),
            "severity": severity,
            "category": category,
            "description": description,
            "attack_id": attack_id,
            "evidence": evidence,
            "confidence": confidence,
            "detected_at": datetime.now(timezone.utc).isoformat(),
            "detector": self.name,
        }

        # Add evidence pack for better reproducibility
        evidence_pack = {}

        if raw_evidence and raw_evidence != evidence:
            evidence_pack["raw_evidence"] = raw_evidence
            evidence_pack["normalized_evidence"] = evidence

        if conversation_context:
            # Include last 3 turns for context
            evidence_pack["conversation_context"] = conversation_context[-3:]

        if evidence_pack:
            finding["evidence_pack"] = evidence_pack

        return finding
