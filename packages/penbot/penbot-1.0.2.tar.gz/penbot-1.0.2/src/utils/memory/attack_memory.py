"""Attack memory store for cross-agent knowledge sharing."""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from src.utils.logging import get_logger

logger = get_logger(__name__)


class SuccessfulAttackRecord(BaseModel):
    """Record of a successful attack for learning."""

    attack_id: str = Field(..., description="Unique attack ID")
    timestamp: str = Field(..., description="ISO timestamp")
    attack_type: str = Field(..., description="Type of attack (jailbreak, encoding, etc.)")
    pattern: str = Field(default="", description="Pattern name used")
    query: str = Field(..., description="Attack query that worked")
    target_response: str = Field(..., description="Target's response")
    findings: List[Dict[str, Any]] = Field(default_factory=list, description="Security findings")
    success_indicators: List[str] = Field(
        default_factory=list, description="What made this successful"
    )
    target_domain: Optional[str] = Field(None, description="Target's domain if known")


class DeclinePattern(BaseModel):
    """Record of a target's decline/refusal pattern."""

    pattern_id: str = Field(..., description="Hash of decline text")
    decline_text: str = Field(..., description="The decline message text")
    triggers: List[str] = Field(
        default_factory=list, description="Words/phrases that triggered this"
    )
    frequency: int = Field(default=1, description="How many times seen")
    last_seen: str = Field(..., description="ISO timestamp of last occurrence")
    target_name: Optional[str] = Field(None, description="Target that uses this pattern")


class AttackMemoryStore:
    """
    File-based attack memory store for cross-agent knowledge sharing.

    Inspired by Deep Agents' file system backend pattern.
    Stores:
    - Successful attacks (learn what works)
    - Decline patterns (learn target's refusal behaviors)
    - Attack effectiveness metrics

    Example:
        >>> memory = AttackMemoryStore(base_dir="./attack_memory")
        >>> await memory.record_successful_attack(
        ...     attack_data={"query": "...", "type": "jailbreak"},
        ...     target_response="Sure, here's the information...",
        ...     findings=[{...}]
        ... )
        >>> similar = await memory.get_similar_successful_attacks("jailbreak", "parcel_tracking")
    """

    def __init__(self, base_dir: str = "./attack_memory"):
        """
        Initialize attack memory store.

        Args:
            base_dir: Base directory for storing memory files
        """
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

        # File paths
        self.successful_attacks_file = self.base_dir / "successful_attacks.jsonl"
        self.decline_patterns_file = self.base_dir / "decline_patterns.json"
        self.metrics_file = self.base_dir / "metrics.json"

        # Ensure files exist
        self.successful_attacks_file.touch(exist_ok=True)
        if not self.decline_patterns_file.exists():
            self.decline_patterns_file.write_text("{}")
        if not self.metrics_file.exists():
            self.metrics_file.write_text("{}")

        logger.info("attack_memory_store_initialized", base_dir=str(self.base_dir))

    async def record_successful_attack(
        self,
        attack_data: Dict[str, Any],
        target_response: str,
        findings: List[Dict[str, Any]],
        target_domain: Optional[str] = None,
    ) -> None:
        """
        Record a successful attack for future learning.

        Args:
            attack_data: Dict with attack details (query, type, pattern, etc.)
            target_response: Target's response to the attack
            findings: List of security findings discovered
            target_domain: Optional domain of the target
        """
        try:
            # Extract success indicators from findings
            success_indicators = []
            for finding in findings:
                if finding.get("severity") in ["critical", "high"]:
                    success_indicators.append(
                        f"{finding.get('category', 'unknown')}: {finding.get('description', '')[:50]}"
                    )

            # Create record
            record = SuccessfulAttackRecord(
                attack_id=attack_data.get("attack_id", self._generate_id()),
                timestamp=datetime.utcnow().isoformat(),
                attack_type=attack_data.get("type", "unknown"),
                pattern=attack_data.get("pattern", ""),
                query=attack_data.get("query", ""),
                target_response=target_response[:500],  # Truncate for storage
                findings=findings,
                success_indicators=success_indicators,
                target_domain=target_domain,
            )

            # Append to JSONL file
            with self.successful_attacks_file.open("a") as f:
                f.write(record.model_dump_json() + "\n")

            logger.info(
                "successful_attack_recorded",
                attack_id=record.attack_id,
                attack_type=record.attack_type,
                pattern=record.pattern,
                indicators_count=len(success_indicators),
            )

        except Exception as e:
            logger.error("failed_to_record_successful_attack", error=str(e))

    async def get_similar_successful_attacks(
        self, attack_type: Optional[str] = None, target_domain: Optional[str] = None, limit: int = 5
    ) -> List[SuccessfulAttackRecord]:
        """
        Retrieve similar past successful attacks for learning.

        Args:
            attack_type: Filter by attack type (jailbreak, encoding, etc.)
            target_domain: Filter by target domain
            limit: Maximum number of records to return

        Returns:
            List of successful attack records
        """
        try:
            all_records = []

            # Read JSONL file
            if self.successful_attacks_file.exists():
                with self.successful_attacks_file.open("r") as f:
                    for line in f:
                        if line.strip():
                            record_dict = json.loads(line)
                            record = SuccessfulAttackRecord(**record_dict)

                            # Filter by criteria
                            if attack_type and record.attack_type != attack_type:
                                continue
                            if target_domain and record.target_domain != target_domain:
                                continue

                            all_records.append(record)

            # Return most recent matches
            all_records.sort(key=lambda r: r.timestamp, reverse=True)
            results = all_records[:limit]

            logger.info(
                "similar_attacks_retrieved",
                count=len(results),
                attack_type=attack_type,
                target_domain=target_domain,
            )

            return results

        except Exception as e:
            logger.error("failed_to_get_similar_attacks", error=str(e))
            return []

    async def record_decline_pattern(
        self, decline_text: str, triggers: List[str], target_name: Optional[str] = None
    ) -> None:
        """
        Record a target's decline/refusal pattern.

        Args:
            decline_text: The decline message text
            triggers: Words/phrases that likely triggered this decline
            target_name: Optional name of target
        """
        try:
            # Generate pattern ID from text hash
            pattern_id = hashlib.sha256(decline_text.encode()).hexdigest()[:12]

            # Load existing patterns
            patterns = json.loads(self.decline_patterns_file.read_text())

            # Update or create pattern
            if pattern_id in patterns:
                # Update existing
                patterns[pattern_id]["frequency"] += 1
                patterns[pattern_id]["last_seen"] = datetime.utcnow().isoformat()
                # Merge triggers
                existing_triggers = set(patterns[pattern_id]["triggers"])
                existing_triggers.update(triggers)
                patterns[pattern_id]["triggers"] = list(existing_triggers)
            else:
                # Create new
                patterns[pattern_id] = DeclinePattern(
                    pattern_id=pattern_id,
                    decline_text=decline_text,
                    triggers=triggers,
                    frequency=1,
                    last_seen=datetime.utcnow().isoformat(),
                    target_name=target_name,
                ).model_dump()

            # Save patterns
            self.decline_patterns_file.write_text(json.dumps(patterns, indent=2))

            logger.info(
                "decline_pattern_recorded",
                pattern_id=pattern_id,
                frequency=patterns[pattern_id]["frequency"],
                triggers_count=len(patterns[pattern_id]["triggers"]),
            )

        except Exception as e:
            logger.error("failed_to_record_decline_pattern", error=str(e))

    async def get_decline_patterns(
        self, target_name: Optional[str] = None, min_frequency: int = 2
    ) -> List[DeclinePattern]:
        """
        Get known decline patterns for a target.

        Args:
            target_name: Optional target name to filter by
            min_frequency: Minimum frequency to include pattern

        Returns:
            List of decline patterns
        """
        try:
            patterns_dict = json.loads(self.decline_patterns_file.read_text())

            results = []
            for pattern_data in patterns_dict.values():
                pattern = DeclinePattern(**pattern_data)

                # Filter by criteria
                if target_name and pattern.target_name != target_name:
                    continue
                if pattern.frequency < min_frequency:
                    continue

                results.append(pattern)

            # Sort by frequency (most common first)
            results.sort(key=lambda p: p.frequency, reverse=True)

            logger.info("decline_patterns_retrieved", count=len(results), target_name=target_name)

            return results

        except Exception as e:
            logger.error("failed_to_get_decline_patterns", error=str(e))
            return []

    async def get_attack_effectiveness_metrics(
        self, attack_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get effectiveness metrics for attack types.

        Args:
            attack_type: Optional filter by attack type

        Returns:
            Dict with metrics (success rate, avg findings, etc.)
        """
        try:
            # Read all successful attacks
            all_records = []
            if self.successful_attacks_file.exists():
                with self.successful_attacks_file.open("r") as f:
                    for line in f:
                        if line.strip():
                            record_dict = json.loads(line)
                            record = SuccessfulAttackRecord(**record_dict)

                            if attack_type and record.attack_type != attack_type:
                                continue

                            all_records.append(record)

            if not all_records:
                return {"total_successes": 0, "attack_type": attack_type or "all"}

            # Calculate metrics
            total_findings = sum(len(r.findings) for r in all_records)
            critical_findings = sum(
                1 for r in all_records for f in r.findings if f.get("severity") == "critical"
            )

            # Group by pattern
            pattern_counts = {}
            for r in all_records:
                pattern = r.pattern or "unknown"
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

            metrics = {
                "total_successes": len(all_records),
                "attack_type": attack_type or "all",
                "avg_findings_per_attack": round(total_findings / len(all_records), 2),
                "critical_findings": critical_findings,
                "most_effective_pattern": max(pattern_counts, key=pattern_counts.get),
                "pattern_distribution": pattern_counts,
            }

            logger.info("attack_effectiveness_metrics_calculated", metrics=metrics)
            return metrics

        except Exception as e:
            logger.error("failed_to_get_effectiveness_metrics", error=str(e))
            return {}

    async def clear_all(self) -> None:
        """Clear all stored memory (for testing/reset)."""
        try:
            # Clear files
            self.successful_attacks_file.write_text("")
            self.decline_patterns_file.write_text("{}")
            self.metrics_file.write_text("{}")

            logger.info("attack_memory_cleared")
        except Exception as e:
            logger.error("failed_to_clear_memory", error=str(e))

    def _generate_id(self) -> str:
        """Generate a unique ID."""
        import uuid

        return str(uuid.uuid4())
