"""
Voting visualization and explanation system.

Provides detailed breakdowns of why agents won/lost voting rounds.
"""

from typing import List, Dict, Any
from src.utils.logging import get_logger

logger = get_logger(__name__)


class VotingExplainer:
    """Explains voting outcomes with detailed reasoning."""

    @staticmethod
    def explain_vote_outcome(
        winner: Dict[str, Any], all_votes: List[Dict[str, Any]], phase: str, current_attempt: int
    ) -> Dict[str, Any]:
        """
        Generate detailed explanation of why a specific agent won.

        Args:
            winner: The winning vote dictionary
            all_votes: All votes cast in this round
            phase: Current campaign phase
            current_attempt: Round number

        Returns:
            Dict with detailed explanation components
        """
        winner_agent = winner["vote"].agent_name
        winner_score = winner["score"]

        # Sort all votes by score for comparison
        sorted_votes = sorted(all_votes, key=lambda x: x["score"], reverse=True)

        # Calculate score gaps
        if len(sorted_votes) > 1:
            second_place = sorted_votes[1]
            score_gap = winner_score - second_place["score"]
            score_gap_pct = (score_gap / winner_score * 100) if winner_score > 0 else 0
        else:
            second_place = None
            score_gap = 0
            score_gap_pct = 0

        # Identify win factors
        win_factors = []

        # Factor 1: Base score (priority × confidence)
        base_score = winner["vote"].priority * winner["vote"].confidence
        if base_score == winner_score:
            win_factors.append(
                {
                    "factor": "base_score",
                    "description": f"Strong base score (priority={winner['vote'].priority}, confidence={winner['vote'].confidence:.2f})",
                    "contribution": base_score,
                }
            )

        # Factor 2: Phase boost
        if "phase_boost" in winner:
            boost_value = winner["phase_boost"]
            if boost_value != 1.0:
                boost_contribution = base_score * (boost_value - 1.0)
                win_factors.append(
                    {
                        "factor": "phase_boost",
                        "description": f"{phase.upper()} phase boost (×{boost_value:.2f})",
                        "contribution": boost_contribution,
                    }
                )

        # Factor 3: Diversity penalty (if avoided)
        # This would require tracking if penalty was applied to others

        # Factor 4: Historical success (if confidence adjusted)
        if hasattr(winner["vote"], "metadata") and winner["vote"].metadata:
            if "historical_success_rate" in winner["vote"].metadata:
                success_rate = winner["vote"].metadata["historical_success_rate"]
                win_factors.append(
                    {
                        "factor": "historical_success",
                        "description": f"Agent's historical success rate: {success_rate:.1%}",
                        "contribution": None,  # Already in confidence
                    }
                )

        # Build explanation
        explanation = {
            "round": current_attempt,
            "phase": phase,
            "winner": {
                "agent": winner_agent,
                "pattern": _extract_pattern_name(winner["vote"]),
                "final_score": winner_score,
                "base_score": base_score,
                "priority": winner["vote"].priority,
                "confidence": winner["vote"].confidence,
                "reasoning": winner["vote"].reasoning,
            },
            "competition": {
                "second_place": second_place["vote"].agent_name if second_place else None,
                "second_score": second_place["score"] if second_place else 0,
                "score_gap": score_gap,
                "score_gap_pct": score_gap_pct,
                "margin": (
                    "landslide"
                    if score_gap_pct > 30
                    else (
                        "comfortable"
                        if score_gap_pct > 15
                        else "narrow" if score_gap_pct > 5 else "tie-breaker"
                    )
                ),
            },
            "win_factors": win_factors,
            "all_scores": [
                {
                    "agent": v["vote"].agent_name,
                    "score": v["score"],
                    "pattern": _extract_pattern_name(v["vote"]),
                }
                for v in sorted_votes
            ],
        }

        logger.info(
            "voting_outcome_explained",
            winner=winner_agent,
            margin=explanation["competition"]["margin"],
            win_factors=[f["factor"] for f in win_factors],
        )

        return explanation

    @staticmethod
    def format_explanation_console(explanation: Dict[str, Any]) -> str:
        """
        Format explanation for console display.

        Args:
            explanation: Explanation dict from explain_vote_outcome

        Returns:
            Formatted string for console output
        """
        lines = []
        lines.append("")
        lines.append("╔" + "═" * 78 + "╗")
        lines.append("║" + " " * 25 + "VOTING EXPLANATION" + " " * 35 + "║")
        lines.append("╚" + "═" * 78 + "╝")
        lines.append("")

        winner = explanation["winner"]
        comp = explanation["competition"]

        # Winner section
        lines.append(f"🏆 WINNER: {winner['agent']}")
        lines.append(f"   Pattern: {winner['pattern']}")
        lines.append(f"   Final Score: {winner['final_score']:.2f}")
        lines.append("")

        # Score breakdown
        lines.append("📊 SCORE BREAKDOWN:")
        lines.append(
            f"   Base Score: {winner['base_score']:.2f} (priority={winner['priority']}, confidence={winner['confidence']:.2f})"
        )

        for factor in explanation["win_factors"]:
            if factor["contribution"] is not None:
                lines.append(f"   + {factor['description']}: +{factor['contribution']:.2f}")
            else:
                lines.append(f"   • {factor['description']}")

        lines.append(f"   = Final: {winner['final_score']:.2f}")
        lines.append("")

        # Competition
        lines.append("🥈 COMPETITION:")
        if comp["second_place"]:
            lines.append(
                f"   2nd Place: {comp['second_place']} (score: {comp['second_score']:.2f})"
            )
            lines.append(
                f"   Margin: {comp['margin'].upper()} ({comp['score_gap']:.2f} points, {comp['score_gap_pct']:.1f}%)"
            )
        else:
            lines.append("   No competition (only one valid vote)")
        lines.append("")

        # All scores
        lines.append("📋 ALL VOTES:")
        for i, vote in enumerate(explanation["all_scores"], 1):
            marker = "🏆" if i == 1 else f"{i}."
            lines.append(
                f"   {marker} {vote['agent']:30s} {vote['score']:6.2f}  ({vote['pattern']})"
            )

        lines.append("")
        lines.append("💡 WHY THIS AGENT WON:")
        lines.append(f"   {winner['reasoning'][:400]}")
        if len(winner["reasoning"]) > 400:
            lines.append("   ...")
        lines.append("")

        return "\n".join(lines)


def _extract_pattern_name(vote) -> str:
    """Extract pattern name from vote for display."""
    proposed_attack = vote.proposed_attack

    # Try different locations where pattern might be stored
    pattern = (
        proposed_attack.get("pattern")
        or proposed_attack.get("encoding_method")
        or proposed_attack.get("metadata", {}).get("pattern", "unknown")
    )

    # Truncate if too long
    if isinstance(pattern, str) and len(pattern) > 60:
        return pattern[:57] + "..."

    return str(pattern)
