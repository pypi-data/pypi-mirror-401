"""Target chatbot fingerprinting for adaptive attack strategy.

This module automatically classifies and profiles target chatbots based on
their responses, enabling intelligent attack adaptation from Round 1.
"""

import re
from dataclasses import dataclass, field
from typing import List, Literal
from collections import Counter
from src.utils.logging import get_logger
from src.utils.text_normalization import normalize_text

logger = get_logger(__name__)


@dataclass
class TargetProfile:
    """Fingerprint profile of a target chatbot."""

    # Domain classification
    domain: str  # 'parcel_tracking', 'customer_support', 'ecommerce', 'banking', 'healthcare', 'general_ai', 'unknown'
    domain_confidence: float  # 0-1

    # Language detection
    primary_language: str  # 'en', 'el', 'es', 'de', 'fr', 'multi', 'unknown'
    secondary_languages: List[str] = field(default_factory=list)

    # Response style
    response_style: str  # 'emoji_heavy', 'structured', 'conversational', 'terse', 'formal'
    avg_response_length: float = 0.0

    # Performance characteristics
    avg_latency_ms: float = 0.0
    latency_variance: float = 0.0  # Indicates caching vs live generation

    # Defensive posture
    defensive_level: Literal["low", "medium", "high"] = "low"
    has_keyword_filters: bool = False
    filter_indicators: List[str] = field(default_factory=list)

    # Capabilities discovered
    capabilities_disclosed: List[str] = field(default_factory=list)

    # Technical stack hints
    likely_framework: str = "unknown"  # 'custom', 'openai', 'dialogflow', 'rasa', 'unknown'
    framework_confidence: float = 0.0

    # Metadata
    responses_analyzed: int = 0
    profile_updated_at: str = ""


class TargetFingerprinter:
    """
    Automatically fingerprint target chatbot characteristics.

    Analyzes responses to build a profile enabling:
    - Domain-specific attack selection
    - Language-appropriate strategies
    - Defensive posture assessment
    - Framework-specific exploits
    """

    def __init__(self):
        self.responses: List[str] = []
        self.latencies: List[float] = []
        self.normalized_responses: List[str] = []

        # Domain keyword dictionaries (expandable)
        self.domain_keywords = {
            "parcel_tracking": [
                "tracking",
                "delivery",
                "parcel",
                "package",
                "shipment",
                "courier",
                "postal",
                "τράκινγκ",
                "παράδοση",
                "δέμα",
            ],
            "customer_support": [
                "ticket",
                "issue",
                "problem",
                "resolve",
                "help",
                "support",
                "assist",
                "υποστήριξη",
                "βοήθεια",
            ],
            "ecommerce": [
                "order",
                "purchase",
                "cart",
                "checkout",
                "product",
                "price",
                "buy",
                "παραγγελία",
                "αγορά",
                "προϊόν",
            ],
            "banking": [
                "account",
                "balance",
                "transaction",
                "transfer",
                "payment",
                "bank",
                "λογαριασμός",
                "τράπεζα",
                "συναλλαγή",
            ],
            "healthcare": [
                "appointment",
                "doctor",
                "symptom",
                "medication",
                "patient",
                "ραντεβού",
                "γιατρός",
                "ασθενής",
            ],
            "general_ai": ["anything", "question", "help", "assist", "can", "know", "information"],
        }

    def update(self, response: str, latency_ms: float):
        """
        Update fingerprint with new response.

        Args:
            response: Chatbot response text
            latency_ms: Response latency in milliseconds
        """
        self.responses.append(response)
        self.latencies.append(latency_ms)
        self.normalized_responses.append(normalize_text(response))

        logger.debug(
            "fingerprint_updated", total_responses=len(self.responses), latest_latency=latency_ms
        )

    def get_profile(self) -> TargetProfile:
        """
        Generate complete target profile from collected responses.

        Returns:
            TargetProfile with all detected characteristics
        """
        if not self.responses:
            logger.warning("fingerprint_requested_with_no_data")
            return self._empty_profile()

        # Domain detection
        domain, domain_conf = self._detect_domain()

        # Language detection
        primary_lang, secondary_langs = self._detect_languages()

        # Response style
        style = self._detect_response_style()

        # Performance characteristics
        avg_latency, latency_var = self._calculate_latency_stats()

        # Defensive posture
        defensive, has_filters, indicators = self._detect_defensive_posture()

        # Capabilities
        capabilities = self._extract_capabilities()

        # Framework detection
        framework, framework_conf = self._detect_framework()

        # Response length stats
        avg_length = sum(len(r) for r in self.responses) / len(self.responses)

        profile = TargetProfile(
            domain=domain,
            domain_confidence=domain_conf,
            primary_language=primary_lang,
            secondary_languages=secondary_langs,
            response_style=style,
            avg_response_length=avg_length,
            avg_latency_ms=avg_latency,
            latency_variance=latency_var,
            defensive_level=defensive,
            has_keyword_filters=has_filters,
            filter_indicators=indicators,
            capabilities_disclosed=capabilities,
            likely_framework=framework,
            framework_confidence=framework_conf,
            responses_analyzed=len(self.responses),
            profile_updated_at=str(__import__("datetime").datetime.utcnow()),
        )

        logger.info(
            "target_profile_generated",
            domain=domain,
            language=primary_lang,
            defensive_level=defensive,
            responses_analyzed=len(self.responses),
        )

        return profile

    def _detect_domain(self) -> tuple[str, float]:
        """Detect chatbot domain from responses."""
        combined_text = " ".join(self.normalized_responses).lower()

        # Score each domain
        domain_scores = {}
        for domain, keywords in self.domain_keywords.items():
            score = sum(1 for kw in keywords if kw in combined_text)
            if score > 0:
                # Normalize by keyword count
                domain_scores[domain] = score / len(keywords)

        if not domain_scores:
            return "unknown", 0.0

        # Get best match
        best_domain = max(domain_scores, key=domain_scores.get)
        confidence = domain_scores[best_domain]

        # Require minimum confidence
        if confidence < 0.1:
            return "unknown", confidence

        return best_domain, min(confidence, 1.0)

    def _detect_languages(self) -> tuple[str, List[str]]:
        """Detect primary and secondary languages."""
        combined_text = " ".join(self.responses)

        # Character set analysis
        char_counts = {
            "greek": len(re.findall(r"[Α-Ωα-ω]", combined_text)),
            "latin": len(re.findall(r"[A-Za-z]", combined_text)),
            "cyrillic": len(re.findall(r"[А-Яа-я]", combined_text)),
            "arabic": len(re.findall(r"[\u0600-\u06FF]", combined_text)),
            "chinese": len(re.findall(r"[\u4e00-\u9fff]", combined_text)),
        }

        total_chars = sum(char_counts.values())
        if total_chars == 0:
            return "unknown", []

        # Calculate percentages
        percentages = {
            lang: count / total_chars for lang, count in char_counts.items() if count > 0
        }

        # Sort by percentage
        sorted_langs = sorted(percentages.items(), key=lambda x: x[1], reverse=True)

        # Map character sets to language codes
        lang_map = {
            "greek": "el",
            "latin": "en",  # Assume English for Latin, refine later
            "cyrillic": "ru",
            "arabic": "ar",
            "chinese": "zh",
        }

        if not sorted_langs:
            return "unknown", []

        # Primary language
        primary_script, primary_pct = sorted_langs[0]
        primary_lang = lang_map.get(primary_script, "unknown")

        # Secondary languages (>10% presence)
        secondary = [
            lang_map.get(script, "unknown") for script, pct in sorted_langs[1:] if pct > 0.1
        ]

        # Multi-language detection
        if len([pct for _, pct in sorted_langs if pct > 0.2]) >= 2:
            primary_lang = "multi"

        return primary_lang, secondary

    def _detect_response_style(self) -> str:
        """Detect chatbot response style."""
        combined_text = " ".join(self.responses)

        # Emoji analysis
        emoji_pattern = r"[✅✓✔⚠️⚡❌✖❗🔒🔓📌📍🎯💡ℹ️📦🚚📧📞🏠]"
        emoji_count = len(re.findall(emoji_pattern, combined_text))

        # Structure analysis
        bullet_count = combined_text.count("\n-") + combined_text.count("\n•")
        numbered_count = len(re.findall(r"\n\d+\.", combined_text))

        # Length analysis
        avg_length = sum(len(r) for r in self.responses) / len(self.responses)

        # Classification
        if emoji_count > len(self.responses) * 2:  # >2 emojis per response
            return "emoji_heavy"
        elif bullet_count + numbered_count > len(self.responses):
            return "structured"
        elif avg_length > 300:
            return "conversational"
        elif avg_length < 50:
            return "terse"
        else:
            return "formal"

    def _calculate_latency_stats(self) -> tuple[float, float]:
        """Calculate average latency and variance."""
        if not self.latencies:
            return 0.0, 0.0

        avg_latency = sum(self.latencies) / len(self.latencies)

        # Calculate variance
        if len(self.latencies) > 1:
            variance = sum((lat - avg_latency) ** 2 for lat in self.latencies) / len(self.latencies)
        else:
            variance = 0.0

        return avg_latency, variance

    def _detect_defensive_posture(self) -> tuple[str, bool, List[str]]:
        """
        Detect defensive level and keyword filtering.

        Returns:
            (defensive_level, has_keyword_filters, filter_indicators)
        """
        # Check for repeated identical responses (canned = filters)
        normalized_counter = Counter(self.normalized_responses)
        repeated = [
            (resp, count)
            for resp, count in normalized_counter.items()
            if count >= 2 and len(resp) < 100
        ]

        # Check for filter indicator phrases
        filter_phrases = [
            "cannot help",
            "unable to",
            "not allowed",
            "not permitted",
            "out of scope",
            "cannot provide",
            "restricted",
            "δεν μπορώ",
            "δεν επιτρέπεται",
            "εκτός πεδίου",
        ]

        combined_text = " ".join(self.normalized_responses).lower()
        filter_indicators = [phrase for phrase in filter_phrases if phrase in combined_text]

        # Determine defensive level
        has_filters = len(repeated) >= 2 or len(filter_indicators) >= 2

        if len(repeated) >= 3 or len(filter_indicators) >= 3:
            defensive = "high"
        elif len(repeated) >= 2 or len(filter_indicators) >= 2:
            defensive = "medium"
        else:
            defensive = "low"

        return defensive, has_filters, filter_indicators

    def _extract_capabilities(self) -> List[str]:
        """Extract disclosed capabilities from responses."""
        capabilities = []
        combined_text = " ".join(self.responses).lower()

        # Capability patterns (language-agnostic where possible)
        capability_patterns = {
            "can_search": r"(i can|able to).*(search|find|look|locate)",
            "has_database_access": r"(access|query|check).*(database|data|records)",
            "can_modify": r"(i can|able to).*(modify|change|update|edit)",
            "has_pii_access": r"(access|see|view).*(personal|private|user) (data|information)",
            "multi_language": r"(english|greek|spanish|ελληνικά|αγγλικά|español)",
            "can_escalate": r"(transfer|escalate|forward|contact).*(human|agent|support)",
        }

        for capability, pattern in capability_patterns.items():
            if re.search(pattern, combined_text, re.IGNORECASE):
                capabilities.append(capability)

        return capabilities

    def _detect_framework(self) -> tuple[str, float]:
        """Detect underlying chatbot framework."""
        combined_text = " ".join(self.responses).lower()
        avg_latency = sum(self.latencies) / len(self.latencies) if self.latencies else 0

        # Check for explicit framework mentions
        framework_markers = {
            "openai": ["openai", "chatgpt", "gpt-"],
            "anthropic": ["claude", "anthropic"],
            "dialogflow": ["dialogflow", "google assistant"],
            "rasa": ["rasa", "botpress"],
            "custom": [],  # Detected by characteristics
        }

        for framework, markers in framework_markers.items():
            if any(marker in combined_text for marker in markers):
                return framework, 0.9

        # Heuristic detection
        if avg_latency < 300:
            # Very fast = likely rule-based/custom
            return "custom", 0.6
        elif avg_latency > 2000:
            # Slow = likely large LLM (OpenAI/Anthropic)
            if len(self.responses[0]) > 200:  # Long responses
                return "openai", 0.5

        return "unknown", 0.0

    def _empty_profile(self) -> TargetProfile:
        """Return empty profile when no data available."""
        return TargetProfile(
            domain="unknown",
            domain_confidence=0.0,
            primary_language="unknown",
            defensive_level="low",
        )

    def reset(self):
        """Reset fingerprinter for new target."""
        self.responses.clear()
        self.latencies.clear()
        self.normalized_responses.clear()
        logger.info("fingerprinter_reset")
