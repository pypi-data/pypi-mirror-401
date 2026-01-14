"""
Attack lineage tracking system.

Tracks evolutionary relationships between attacks (parent → child → grandchild).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from src.utils.logging import get_logger
import json
import os

logger = get_logger(__name__)


class AttackLineageTracker:
    """Tracks genealogy of attacks for evolutionary analysis."""

    def __init__(self, storage_dir: str = "./attack_memory"):
        self.storage_dir = storage_dir
        self.lineage_file = os.path.join(storage_dir, "attack_lineage.jsonl")

        # Ensure directory exists
        os.makedirs(storage_dir, exist_ok=True)

        logger.info("attack_lineage_tracker_initialized", storage_dir=storage_dir)

    def record_attack(
        self,
        attack_id: str,
        agent_name: str,
        attack_type: str,
        pattern: str,
        parent_attack_id: Optional[str] = None,
        generation: int = 0,
        mutation_type: Optional[str] = None,
        success: bool = False,
        severity: Optional[str] = None,
    ) -> None:
        """
        Record an attack in the lineage tree.

        Args:
            attack_id: Unique attack ID
            agent_name: Agent that generated the attack
            attack_type: Type of attack (jailbreak, encoding, etc.)
            pattern: Pattern name or description
            parent_attack_id: ID of parent attack (if evolved)
            generation: Generation number (0 = original, 1 = child, 2 = grandchild, etc.)
            mutation_type: Type of evolution ("verbalized_sampling", "crossover", "none")
            success: Whether attack found vulnerabilities
            severity: Severity of findings if successful
        """
        lineage_record = {
            "attack_id": attack_id,
            "agent_name": agent_name,
            "attack_type": attack_type,
            "pattern": pattern,
            "parent_attack_id": parent_attack_id,
            "generation": generation,
            "mutation_type": mutation_type or ("none" if generation == 0 else "unknown"),
            "is_evolved": generation > 0,
            "success": success,
            "severity": severity,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        # Append to lineage file
        try:
            with open(self.lineage_file, "a") as f:
                f.write(json.dumps(lineage_record) + "\n")

            logger.debug(
                "attack_lineage_recorded",
                attack_id=attack_id,
                generation=generation,
                parent_attack_id=parent_attack_id,
            )
        except Exception as e:
            logger.error("failed_to_record_lineage", error=str(e))

    def get_lineage_chain(self, attack_id: str) -> List[Dict[str, Any]]:
        """
        Get the full lineage chain for an attack (ancestors and descendants).

        Args:
            attack_id: Attack ID to trace

        Returns:
            List of attack records in chronological order (oldest → newest)
        """
        if not os.path.exists(self.lineage_file):
            return []

        # Load all lineage records
        all_records = []
        try:
            with open(self.lineage_file, "r") as f:
                for line in f:
                    if line.strip():
                        all_records.append(json.loads(line))
        except Exception as e:
            logger.error("failed_to_read_lineage", error=str(e))
            return []

        # Find the attack
        target_attack = next((r for r in all_records if r["attack_id"] == attack_id), None)
        if not target_attack:
            return []

        # Build ancestor chain (parent → grandparent → ...)
        ancestors = []
        current = target_attack
        while current.get("parent_attack_id"):
            parent = next(
                (r for r in all_records if r["attack_id"] == current["parent_attack_id"]), None
            )
            if not parent:
                break
            ancestors.insert(0, parent)  # Insert at start to maintain chronological order
            current = parent

        # Build descendant chain (children → grandchildren → ...)
        descendants = []

        def find_children(parent_id: str):
            children = [r for r in all_records if r.get("parent_attack_id") == parent_id]
            for child in children:
                descendants.append(child)
                find_children(child["attack_id"])  # Recursive

        find_children(attack_id)

        # Combine: ancestors → target → descendants
        full_chain = ancestors + [target_attack] + descendants

        return full_chain

    def get_successful_lineages(self) -> List[List[Dict[str, Any]]]:
        """
        Get all lineage chains that resulted in successful attacks.

        Returns:
            List of lineage chains (each chain is a list of attack records)
        """
        if not os.path.exists(self.lineage_file):
            return []

        # Load all records
        all_records = []
        try:
            with open(self.lineage_file, "r") as f:
                for line in f:
                    if line.strip():
                        all_records.append(json.loads(line))
        except Exception as e:
            logger.error("failed_to_read_lineage", error=str(e))
            return []

        # Find all successful attacks
        successful_attacks = [r for r in all_records if r.get("success")]

        # Build lineage chains for each
        lineages = []
        for attack in successful_attacks:
            chain = self.get_lineage_chain(attack["attack_id"])
            if chain and len(chain) > 1:  # Only include if it has parents/children
                lineages.append(chain)

        return lineages

    def format_lineage_tree(self, attack_id: str) -> str:
        """
        Format lineage chain as ASCII tree for console display.

        Args:
            attack_id: Attack ID to visualize

        Returns:
            Formatted tree string
        """
        chain = self.get_lineage_chain(attack_id)
        if not chain:
            return f"No lineage found for attack {attack_id}"

        lines = []
        lines.append("")
        lines.append("╔" + "═" * 78 + "╗")
        lines.append("║" + " " * 28 + "ATTACK LINEAGE" + " " * 36 + "║")
        lines.append("╚" + "═" * 78 + "╝")
        lines.append("")

        for i, record in enumerate(chain):
            is_target = record["attack_id"] == attack_id
            is_last = i == len(chain) - 1

            # Determine tree characters
            if i == 0:
                prefix = "🌱 "
                connector = ""
            else:
                indent_level = record["generation"]
                connector = "   " * (indent_level - 1) + "└─→ "
                prefix = ""

            # Success indicator
            status = ""
            if record["success"]:
                severity = record.get("severity", "unknown").upper()
                status = f"✅ {severity}"
            else:
                status = "❌ FAILED"

            # Highlight target attack
            marker = "🎯 " if is_target else ""

            # Format line
            gen_label = f"Gen {record['generation']}"
            mutation = (
                f"[{record['mutation_type']}]" if record.get("mutation_type") != "none" else ""
            )

            line = f"{connector}{prefix}{marker}{gen_label} {record['agent_name']:20s} {status:12s} {mutation}"
            lines.append(line)

            # Add pattern details
            pattern = record.get("pattern", "unknown")
            if len(pattern) > 60:
                pattern = pattern[:57] + "..."
            lines.append(f"{'   ' * (record['generation'] + 1)}Pattern: {pattern}")

            if not is_last:
                lines.append(f"{'   ' * (record['generation'] + 1)}│")

        lines.append("")

        # Summary statistics
        total_generations = max(r["generation"] for r in chain)
        successful_in_chain = sum(1 for r in chain if r["success"])

        lines.append("📊 LINEAGE STATISTICS:")
        lines.append(f"   Total Generations: {total_generations}")
        lines.append(f"   Total Attacks in Chain: {len(chain)}")
        lines.append(
            f"   Successful Attacks: {successful_in_chain}/{len(chain)} ({successful_in_chain/len(chain)*100:.1f}%)"
        )

        if total_generations > 0:
            lines.append(f"   Evolution Depth: {total_generations} generations from origin")

        lines.append("")

        return "\n".join(lines)

    def get_evolution_stats(self) -> Dict[str, Any]:
        """
        Get overall evolution statistics.

        Returns:
            Dict with evolution metrics
        """
        if not os.path.exists(self.lineage_file):
            return {
                "total_attacks": 0,
                "evolved_attacks": 0,
                "max_generation": 0,
                "successful_evolutions": 0,
            }

        all_records = []
        try:
            with open(self.lineage_file, "r") as f:
                for line in f:
                    if line.strip():
                        all_records.append(json.loads(line))
        except Exception as e:
            logger.error("failed_to_read_lineage", error=str(e))
            return {}

        evolved_attacks = [r for r in all_records if r["generation"] > 0]
        successful_evolutions = [r for r in evolved_attacks if r["success"]]

        # Mutation type breakdown
        mutation_types = {}
        for r in evolved_attacks:
            mut_type = r.get("mutation_type", "unknown")
            mutation_types[mut_type] = mutation_types.get(mut_type, 0) + 1

        return {
            "total_attacks": len(all_records),
            "original_attacks": len([r for r in all_records if r["generation"] == 0]),
            "evolved_attacks": len(evolved_attacks),
            "max_generation": max((r["generation"] for r in all_records), default=0),
            "successful_evolutions": len(successful_evolutions),
            "evolution_success_rate": (
                len(successful_evolutions) / len(evolved_attacks) if evolved_attacks else 0
            ),
            "mutation_type_breakdown": mutation_types,
            "average_generation": (
                sum(r["generation"] for r in all_records) / len(all_records) if all_records else 0
            ),
        }
