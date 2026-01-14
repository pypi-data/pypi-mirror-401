"""Canned (programmatic) response detection for automatic pivot strategy.

This module detects when a target chatbot is returning pre-programmed template
responses instead of AI-generated content, allowing the system to automatically
pivot attack strategy to avoid triggering keyword filters.
"""

import re
from hashlib import sha256
from typing import Dict, List, Any, Optional
from collections import defaultdict
from src.utils.logging import get_logger
from src.utils.text_normalization import normalize_text

logger = get_logger(__name__)


class CannedResponseDetector:
    """
    Detect programmatic/canned responses from chatbots.

    Canned responses are pre-written template messages triggered by keywords
    or patterns, bypassing AI reasoning. Detecting them allows us to:
    1. Avoid wasting attack rounds on keyword filters
    2. Identify trigger patterns to avoid in future attacks
    3. Automatically pivot to different attack strategies

    Detection Signals (language-agnostic):
    - Hash-based repetition (same normalized response ≥3 times)
    - Lightning-fast response time (<500ms) with template structure
    - Very short generic responses (<30 chars)
    - Placeholder/variable syntax ([X], {Y}, etc.)
    """

    def __init__(self, repetition_threshold: int = 3):
        """
        Initialize canned response detector.

        Args:
            repetition_threshold: Number of identical responses before flagging as canned
                                 (default: 3, meaning 3rd occurrence triggers detection)
        """
        self.repetition_threshold = repetition_threshold

        # Track response hashes per session
        self.response_hashes: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

        # Track which attacks triggered each hash
        self.trigger_map: Dict[str, List[str]] = defaultdict(list)

        # Track first occurrence timestamp per hash
        self.first_seen: Dict[str, float] = {}

    def is_canned(
        self, session_id: str, response: str, latency_ms: float, attack_query: str
    ) -> Dict[str, Any]:
        """
        Detect if a response is canned/programmatic.

        Args:
            session_id: Test session identifier
            response: Target's response text
            latency_ms: Response latency in milliseconds
            attack_query: The attack query that triggered this response

        Returns:
            Dictionary with detection results:
            {
                'is_canned': bool,
                'confidence': float (0-1),
                'reason': str,
                'trigger_hints': List[str],  # Common keywords that likely trigger this
                'hash': str,
                'occurrence_count': int
            }
        """
        # Normalize and hash response
        normalized = normalize_text(response)
        resp_hash = self._hash_response(normalized)

        # Track occurrence
        self.response_hashes[session_id][resp_hash] += 1
        occurrence_count = self.response_hashes[session_id][resp_hash]

        # Track what triggered it
        self.trigger_map[resp_hash].append(attack_query)

        # Initialize detection result
        is_canned = False
        confidence = 0.0
        reason = ""

        if occurrence_count >= self.repetition_threshold:
            is_canned = True
            confidence = min(0.95, 0.75 + (occurrence_count * 0.05))  # Caps at 0.95
            reason = f"Identical response repeated {occurrence_count} times (threshold: {self.repetition_threshold})"

            logger.warning(
                "canned_response_repetition",
                session_id=session_id,
                hash=resp_hash[:8],
                count=occurrence_count,
                confidence=confidence,
            )

        elif latency_ms < 500:
            template_score = self._calculate_template_score(normalized)

            if template_score >= 2:  # At least 2 template indicators
                is_canned = True
                confidence = 0.80 + (template_score * 0.03)  # More indicators = higher confidence
                reason = (
                    f"Fast response ({latency_ms:.0f}ms) with {template_score} template indicators"
                )

                logger.info(
                    "canned_response_fast_template",
                    session_id=session_id,
                    latency_ms=latency_ms,
                    template_score=template_score,
                    confidence=confidence,
                )

        elif len(normalized) < 30:
            generic_score = self._calculate_generic_score(normalized)

            if generic_score >= 0.6:  # 60% generic keywords
                is_canned = True
                confidence = 0.70
                reason = f"Very short ({len(normalized)} chars) highly generic response"

                logger.info(
                    "canned_response_short_generic",
                    session_id=session_id,
                    length=len(normalized),
                    generic_score=generic_score,
                )

        # Extract trigger hints if canned
        trigger_hints = []
        if is_canned and occurrence_count >= 2:
            trigger_hints = self._extract_trigger_keywords(resp_hash)

        result = {
            "is_canned": is_canned,
            "confidence": confidence,
            "reason": reason,
            "trigger_hints": trigger_hints,
            "hash": resp_hash,
            "occurrence_count": occurrence_count,
        }

        if is_canned:
            logger.warning("canned_response_detected", session_id=session_id, **result)

        return result

    def _hash_response(self, normalized_text: str) -> str:
        """Create hash of normalized response for deduplication."""
        return sha256(normalized_text.encode("utf-8")).hexdigest()[:16]

    def _calculate_template_score(self, text: str) -> int:
        """
        Calculate template-likeness score (language-agnostic).

        Returns:
            Score (0-10) based on number of template indicators found
        """
        score = 0
        text_lower = text.lower()

        # Indicator 1: Placeholder syntax
        placeholder_patterns = [
            r"\[.*?\]",  # [placeholder]
            r"\{.*?\}",  # {variable}
            r"\$\{.*?\}",  # ${var}
            r"<.*?>",  # <field>
            r"{{.*?}}",  # {{template}}
        ]
        for pattern in placeholder_patterns:
            if re.search(pattern, text):
                score += 1
                break  # Only count once

        # Indicator 2: Error code patterns
        if re.search(r"(error|code|status)[\s:]+\d+", text_lower):
            score += 1

        # Indicator 3: Form field requests (cross-language)
        form_patterns = [
            r"please\s+(provide|enter|fill|specify|submit)",
            r"enter\s+(your|the)",
            r"provide\s+(your|the)",
            r"required\s+field",
        ]
        if any(re.search(p, text_lower) for p in form_patterns):
            score += 1

        # Indicator 4: Standard apology/refusal patterns
        if re.match(r"^(sorry|apologies|unfortunately|unable|cannot|can\'t)", text_lower):
            score += 1

        # Indicator 5: URL/email templates
        if re.search(r"(https?://|www\.|@.*\.(com|org|net))", text_lower):
            score += 1

        # Indicator 6: Multiple exclamation/question marks (bot-like)
        if len(re.findall(r"[!?]{2,}", text)) >= 2:
            score += 1

        # Indicator 7: Repeated punctuation patterns
        if re.search(r"(\.{3,}|-{3,}|_{3,})", text):
            score += 1

        # Indicator 8: All caps words (ATTENTION, ERROR, etc.)
        all_caps_words = re.findall(r"\b[A-Z]{4,}\b", text)
        if len(all_caps_words) >= 2:
            score += 1

        return min(score, 10)  # Cap at 10

    def _calculate_generic_score(self, text: str) -> float:
        """
        Calculate how generic/templated a short response is.

        Returns:
            Score (0-1) indicating percentage of generic keywords
        """
        text_lower = text.lower()
        words = re.findall(r"\w+", text_lower)

        if not words:
            return 0.0

        # Generic filler words (cross-language common patterns)
        generic_keywords = [
            # English
            "sorry",
            "apologies",
            "unfortunately",
            "unable",
            "cannot",
            "can't",
            "not",
            "found",
            "invalid",
            "error",
            "please",
            "try",
            "again",
            "help",
            "assist",
            "contact",
            "support",
            # Common abbreviations
            "ok",
            "yes",
            "no",
            "thx",
            "thanks",
        ]

        generic_count = sum(1 for word in words if word in generic_keywords)

        return generic_count / len(words)

    def _extract_trigger_keywords(self, resp_hash: str) -> List[str]:
        """
        Extract common keywords from attacks that triggered the same canned response.

        Args:
            resp_hash: Response hash to analyze

        Returns:
            List of likely trigger keywords (top 5)
        """
        attacks = self.trigger_map.get(resp_hash, [])

        if len(attacks) < 2:
            return []

        from collections import Counter

        # Tokenize all attacks
        all_words = []
        for attack in attacks:
            # Extract words (3+ chars, ignore very common words)
            words = re.findall(r"\b\w{3,}\b", attack.lower())
            stopwords = {"the", "and", "for", "are", "this", "that", "with", "from", "have"}
            words = [w for w in words if w not in stopwords]
            all_words.extend(words)

        # Find words appearing in >50% of attacks
        word_counts = Counter(all_words)
        threshold = len(attacks) * 0.5

        common_words = [word for word, count in word_counts.items() if count >= threshold]

        # Sort by frequency
        common_words.sort(key=lambda w: word_counts[w], reverse=True)

        return common_words[:5]  # Top 5

    def get_statistics(self, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get detection statistics for debugging/monitoring.

        Args:
            session_id: Optional session ID to filter by

        Returns:
            Statistics dictionary
        """
        if session_id:
            hashes = self.response_hashes.get(session_id, {})
            total_responses = sum(hashes.values())
            unique_responses = len(hashes)
            canned_responses = sum(
                1 for count in hashes.values() if count >= self.repetition_threshold
            )

            return {
                "session_id": session_id,
                "total_responses": total_responses,
                "unique_responses": unique_responses,
                "canned_responses": canned_responses,
                "canned_percentage": (
                    (canned_responses / unique_responses * 100) if unique_responses else 0
                ),
            }
        else:
            # Global stats
            all_sessions = list(self.response_hashes.keys())
            return {
                "total_sessions": len(all_sessions),
                "sessions": [self.get_statistics(sid) for sid in all_sessions],
            }

    def reset_session(self, session_id: str):
        """Reset tracking for a specific session."""
        if session_id in self.response_hashes:
            del self.response_hashes[session_id]

        logger.info("canned_detector_session_reset", session_id=session_id)
