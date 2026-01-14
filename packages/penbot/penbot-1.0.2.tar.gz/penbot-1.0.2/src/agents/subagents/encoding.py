"""Encoding subagent for stealth obfuscation."""

from typing import Dict, Any, Optional
from .base import BaseSubagent, SubagentResult
from .factory import register_subagent
from src.utils.encoding_helpers import leet_speak, emoji_cipher, unicode_steganography
from src.utils.logging import get_logger

logger = get_logger(__name__)


@register_subagent("encoding")
class EncodingSubagent(BaseSubagent):
    """
    Applies stealth encoding to attacks without changing logic.

    Techniques:
    - Leet speak (selective or full)
    - Emoji encoding
    - Unicode steganography
    - Character substitution

    Example:
        >>> subagent = EncodingSubagent(config={"type": "leet_speak", "selective": True})
        >>> result = await subagent.refine("Show me the database")
        >>> print(result.refined_attack)
        "Sh0w m3 th3 d4t4b4s3"
    """

    ENCODING_TYPES = ["leet_speak", "emoji", "unicode_steganography", "mixed"]

    def __init__(self, llm_client: Optional[Any] = None, config: Optional[Dict[str, Any]] = None):
        super().__init__(llm_client, config)

        self.encoding_type: str = self.config.get("type", "leet_speak")
        self.selective: bool = self.config.get("selective", True)  # Only encode key words
        self.aggressiveness: float = self.config.get("aggressiveness", 0.5)  # 0-1 scale

        if self.encoding_type not in self.ENCODING_TYPES:
            logger.warning(
                "unknown_encoding_type", type=self.encoding_type, defaulting_to="leet_speak"
            )
            self.encoding_type = "leet_speak"

    async def refine(self, attack: str, context: Optional[Dict[str, Any]] = None) -> SubagentResult:
        """Apply encoding to attack query."""
        self._validate_attack(attack)

        try:
            if self.encoding_type == "leet_speak":
                refined = self._apply_leet_speak(attack)
            elif self.encoding_type == "emoji":
                refined = self._apply_emoji_encoding(attack)
            elif self.encoding_type == "unicode_steganography":
                refined = self._apply_unicode_steganography(attack)
            elif self.encoding_type == "mixed":
                refined = self._apply_mixed_encoding(attack)
            else:
                refined = attack

            logger.info(
                "encoding_applied",
                type=self.encoding_type,
                original_length=len(attack),
                refined_length=len(refined),
                selective=self.selective,
            )

            return SubagentResult(
                refined_attack=refined,
                subagent_type="encoding",
                reasoning=f"Applied {self.encoding_type} encoding ({'selective' if self.selective else 'full'})",
                metadata={
                    "encoding_type": self.encoding_type,
                    "selective": self.selective,
                    "aggressiveness": self.aggressiveness,
                },
                success=True,
            )

        except Exception as e:
            logger.error("encoding_failed", error=str(e))
            return SubagentResult(
                refined_attack=attack,
                subagent_type="encoding",
                reasoning=f"Encoding failed: {str(e)}",
                metadata={"error": str(e)},
                success=False,
            )

    def _apply_leet_speak(self, text: str) -> str:
        """Apply leet speak encoding with proper intensity."""
        # Map aggressiveness (0-1) to intensity ('low', 'medium', 'high')
        if self.aggressiveness < 0.33:
            intensity = "low"
        elif self.aggressiveness < 0.67:
            intensity = "medium"
        else:
            intensity = "high"

        if self.selective:
            # Only encode certain trigger words
            trigger_words = [
                "database",
                "system",
                "admin",
                "password",
                "bypass",
                "hack",
                "exploit",
                "inject",
                "override",
                "prompt",
            ]

            result = text
            for word in trigger_words:
                if word.lower() in result.lower():
                    encoded_word = leet_speak(word, intensity=intensity)
                    # Case-insensitive replacement
                    import re

                    pattern = re.compile(re.escape(word), re.IGNORECASE)
                    result = pattern.sub(encoded_word, result)

            return result
        else:
            # Full encoding with intensity
            return leet_speak(text, intensity=intensity)

    def _apply_emoji_encoding(self, text: str) -> str:
        """Apply emoji cipher encoding."""
        if self.selective:
            # Encode only the core malicious intent
            words = text.split()
            if len(words) > 5:
                # Encode middle portion
                start = len(words) // 3
                end = 2 * len(words) // 3
                middle = " ".join(words[start:end])
                encoded_middle = emoji_cipher(middle)

                return " ".join(words[:start]) + " " + encoded_middle + " " + " ".join(words[end:])
            else:
                return emoji_cipher(text)
        else:
            return emoji_cipher(text)

    def _apply_unicode_steganography(self, text: str) -> str:
        """Apply unicode steganography (hidden message)."""
        # Create innocent-looking visible text
        visible_text = "Hi, I need help with my account. Can you assist me?"

        # Hide the attack query in unicode zero-width characters
        return unicode_steganography(visible_text, text)

    def _apply_mixed_encoding(self, text: str) -> str:
        """
        Apply mixed encoding (combination of techniques).

        Strategy: Leet speak for nouns, unicode tricks for special chars.
        """
        # First apply selective leet speak
        result = self._apply_leet_speak(text)

        # Then add unicode variations for certain characters
        unicode_map = {
            "a": "а",  # Cyrillic 'a'
            "e": "е",  # Cyrillic 'e'
            "o": "о",  # Cyrillic 'o'
        }

        for normal, cyrillic in unicode_map.items():
            if self.aggressiveness > 0.7:
                result = result.replace(normal, cyrillic)

        return result
