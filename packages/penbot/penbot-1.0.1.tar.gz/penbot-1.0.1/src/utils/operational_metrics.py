"""
Operational Metrics Tracking System

Inspired by GTG-1002's operational tempo analysis from Anthropic's November 2025 report.
Tracks attack efficiency, agent performance, and overall campaign effectiveness.

Reference: https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf
"""

from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass
import statistics
from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class AttackMetrics:
    """Metrics for a single attack."""

    attack_id: str
    agent_name: str
    started_at: datetime
    completed_at: datetime
    success: bool
    severity: Optional[str] = None  # critical, high, medium, low, none

    @property
    def latency_seconds(self) -> float:
        """Attack latency in seconds."""
        return (self.completed_at - self.started_at).total_seconds()


@dataclass
class AgentEfficiency:
    """Efficiency metrics for a single agent."""

    agent_name: str
    total_attacks: int = 0
    successful_attacks: int = 0
    total_latency: float = 0.0
    critical_findings: int = 0
    high_findings: int = 0

    @property
    def success_rate(self) -> float:
        """Success rate as percentage (0-100)."""
        if self.total_attacks == 0:
            return 0.0
        return (self.successful_attacks / self.total_attacks) * 100

    @property
    def average_latency(self) -> float:
        """Average attack latency in seconds."""
        if self.total_attacks == 0:
            return 0.0
        return self.total_latency / self.total_attacks


class OperationalMetrics:
    """
    Track attack efficiency and operational tempo.

    Inspired by GTG-1002's operational capabilities:
    - "Peak activity: thousands of requests, multiple operations per second"
    - "AI executed 80-90% of tactical work independently"

    Metrics tracked:
    - Attacks per minute
    - Average attack latency
    - Per-agent efficiency
    - Think-MCP utilization
    - Overall efficiency score
    """

    def __init__(self):
        self.session_start: Optional[datetime] = None
        self.session_end: Optional[datetime] = None

        # Attack tracking
        self.attack_history: List[AttackMetrics] = []
        self.agent_metrics: Dict[str, AgentEfficiency] = {}

        # Think-MCP tracking
        self.think_mcp_operations: int = 0
        self.think_mcp_consensus: int = 0
        self.think_mcp_validation: int = 0
        self.think_mcp_learning: int = 0

        # Tavily tracking
        self.tavily_searches: int = 0
        self.tavily_results: int = 0

        # Subagent tracking
        self.subagent_refinements: int = 0

        logger.info("operational_metrics_initialized")

    def start_session(self):
        """Mark session start."""
        self.session_start = datetime.utcnow()
        logger.info("metrics_session_started", timestamp=self.session_start.isoformat())

    def end_session(self):
        """Mark session end."""
        self.session_end = datetime.utcnow()
        logger.info(
            "metrics_session_ended",
            timestamp=self.session_end.isoformat(),
            duration_seconds=self.session_duration_seconds,
        )

    @property
    def session_duration_seconds(self) -> float:
        """Total session duration in seconds."""
        if not self.session_start:
            return 0.0
        end = self.session_end or datetime.utcnow()
        return (end - self.session_start).total_seconds()

    @property
    def session_duration_minutes(self) -> float:
        """Total session duration in minutes."""
        return self.session_duration_seconds / 60.0

    def record_attack(
        self,
        attack_id: str,
        agent_name: str,
        started_at: datetime,
        completed_at: datetime,
        success: bool,
        severity: Optional[str] = None,
    ):
        """Record a completed attack."""
        metrics = AttackMetrics(
            attack_id=attack_id,
            agent_name=agent_name,
            started_at=started_at,
            completed_at=completed_at,
            success=success,
            severity=severity,
        )

        self.attack_history.append(metrics)

        # Update agent metrics
        if agent_name not in self.agent_metrics:
            self.agent_metrics[agent_name] = AgentEfficiency(agent_name=agent_name)

        agent = self.agent_metrics[agent_name]
        agent.total_attacks += 1
        agent.total_latency += metrics.latency_seconds

        if success:
            agent.successful_attacks += 1

        if severity == "critical":
            agent.critical_findings += 1
        elif severity == "high":
            agent.high_findings += 1

        logger.info(
            "attack_recorded",
            attack_id=attack_id,
            agent=agent_name,
            latency=metrics.latency_seconds,
            success=success,
        )

    def record_think_mcp_operation(self, operation_type: str):
        """
        Record Think-MCP usage.

        Args:
            operation_type: 'consensus', 'validation', 'learning'
        """
        self.think_mcp_operations += 1

        if operation_type == "consensus":
            self.think_mcp_consensus += 1
        elif operation_type == "validation":
            self.think_mcp_validation += 1
        elif operation_type == "learning":
            self.think_mcp_learning += 1

        logger.info("think_mcp_operation_recorded", operation_type=operation_type)

    def record_tavily_search(self, results_count: int):
        """Record Tavily reconnaissance search."""
        self.tavily_searches += 1
        self.tavily_results += results_count
        logger.info("tavily_search_recorded", results_count=results_count)

    def record_subagent_refinement(self):
        """Record subagent refinement operation."""
        self.subagent_refinements += 1

    @property
    def total_attacks(self) -> int:
        """Total number of attacks executed."""
        return len(self.attack_history)

    @property
    def successful_attacks(self) -> int:
        """Number of successful attacks (found vulnerabilities)."""
        return sum(1 for a in self.attack_history if a.success)

    @property
    def attacks_per_minute(self) -> float:
        """Average attacks per minute."""
        if self.session_duration_minutes == 0:
            return 0.0
        return self.total_attacks / self.session_duration_minutes

    @property
    def requests_per_second(self) -> float:
        """
        Approximate requests per second.

        GTG-1002 achieved "multiple operations per second" at peak.
        We estimate: 1 attack = ~10-15 requests (voting, consensus, validation, etc.)
        """
        if self.session_duration_seconds == 0:
            return 0.0

        # Rough estimate of total requests
        total_requests = (
            self.total_attacks * 10  # Each attack ~10 LLM calls
            + self.think_mcp_operations * 2  # Each Think-MCP ~2 calls
            + self.tavily_searches * 1  # Each Tavily search ~1 call
        )

        return total_requests / self.session_duration_seconds

    @property
    def average_attack_latency(self) -> float:
        """Average attack latency in seconds."""
        if not self.attack_history:
            return 0.0
        return statistics.mean(a.latency_seconds for a in self.attack_history)

    @property
    def median_attack_latency(self) -> float:
        """Median attack latency in seconds."""
        if not self.attack_history:
            return 0.0
        return statistics.median(a.latency_seconds for a in self.attack_history)

    @property
    def overall_success_rate(self) -> float:
        """Overall success rate as percentage (0-100)."""
        if self.total_attacks == 0:
            return 0.0
        return (self.successful_attacks / self.total_attacks) * 100

    @property
    def critical_findings(self) -> int:
        """Total critical findings across all agents."""
        return sum(agent.critical_findings for agent in self.agent_metrics.values())

    @property
    def high_findings(self) -> int:
        """Total high findings across all agents."""
        return sum(agent.high_findings for agent in self.agent_metrics.values())

    @property
    def think_mcp_utilization(self) -> float:
        """
        Think-MCP utilization as percentage (0-100).

        Measures: What % of attacks used Think-MCP features?
        (consensus + validation + learning)
        """
        if self.total_attacks == 0:
            return 0.0

        # Each attack can have up to 3 Think-MCP operations
        max_possible = self.total_attacks * 3
        actual = self.think_mcp_operations

        return min(100.0, (actual / max_possible) * 100)

    @property
    def tempo_score(self) -> float:
        """
        Operational tempo score (0-100).

        Measures how fast attacks are executed.
        Baseline: 1 attack per minute = 50 points
        """
        apm = self.attacks_per_minute

        if apm == 0:
            return 0.0

        # Scoring curve: 1 APM = 50, 5 APM = 100
        score = min(100.0, (apm / 5.0) * 100)
        return score

    @property
    def coordination_score(self) -> float:
        """
        Agent coordination efficiency (0-100).

        Measures how well agents work together:
        - Multiple agents contributing
        - Consistent success rates
        - Balanced workload
        """
        if not self.agent_metrics:
            return 0.0

        # Factor 1: Number of agents (more = better coordination)
        agent_diversity = min(1.0, len(self.agent_metrics) / 5.0) * 40

        # Factor 2: Success rate consistency (low variance = better)
        success_rates = [a.success_rate for a in self.agent_metrics.values() if a.total_attacks > 0]
        if success_rates:
            variance = statistics.variance(success_rates) if len(success_rates) > 1 else 0
            consistency = max(0, 30 - (variance / 100))  # Lower variance = higher score
        else:
            consistency = 0

        # Factor 3: Workload balance (even distribution = better)
        attack_counts = [a.total_attacks for a in self.agent_metrics.values()]
        if attack_counts and len(attack_counts) > 1:
            workload_variance = statistics.variance(attack_counts)
            balance = max(0, 30 - (workload_variance / 10))
        else:
            balance = 0

        return agent_diversity + consistency + balance

    def calculate_efficiency_score(self) -> float:
        """
        Overall campaign efficiency score (0-100).

        Weighted combination of:
        - Success rate (40%)
        - Operational tempo (30%)
        - Agent coordination (20%)
        - Think-MCP utilization (10%)
        """
        weights = {"success": 0.40, "tempo": 0.30, "coordination": 0.20, "think_mcp": 0.10}

        score = (
            self.overall_success_rate * weights["success"]
            + self.tempo_score * weights["tempo"]
            + self.coordination_score * weights["coordination"]
            + self.think_mcp_utilization * weights["think_mcp"]
        )

        return round(score, 2)

    def get_summary(self) -> Dict:
        """Get complete metrics summary."""
        return {
            "session": {
                "duration_seconds": self.session_duration_seconds,
                "duration_minutes": round(self.session_duration_minutes, 2),
                "started_at": self.session_start.isoformat() if self.session_start else None,
                "ended_at": self.session_end.isoformat() if self.session_end else None,
            },
            "attacks": {
                "total": self.total_attacks,
                "successful": self.successful_attacks,
                "success_rate": round(self.overall_success_rate, 2),
                "attacks_per_minute": round(self.attacks_per_minute, 2),
                "requests_per_second": round(self.requests_per_second, 2),
                "average_latency": round(self.average_attack_latency, 2),
                "median_latency": round(self.median_attack_latency, 2),
            },
            "findings": {"critical": self.critical_findings, "high": self.high_findings},
            "agents": {
                agent_name: {
                    "total_attacks": agent.total_attacks,
                    "success_rate": round(agent.success_rate, 2),
                    "average_latency": round(agent.average_latency, 2),
                    "critical_findings": agent.critical_findings,
                    "high_findings": agent.high_findings,
                }
                for agent_name, agent in self.agent_metrics.items()
            },
            "think_mcp": {
                "total_operations": self.think_mcp_operations,
                "consensus": self.think_mcp_consensus,
                "validation": self.think_mcp_validation,
                "learning": self.think_mcp_learning,
                "utilization": round(self.think_mcp_utilization, 2),
            },
            "tavily": {"searches": self.tavily_searches, "results": self.tavily_results},
            "deep_agents": {"subagent_refinements": self.subagent_refinements},
            "scores": {
                "efficiency": self.calculate_efficiency_score(),
                "tempo": round(self.tempo_score, 2),
                "coordination": round(self.coordination_score, 2),
                "success_rate": round(self.overall_success_rate, 2),
                "think_mcp_utilization": round(self.think_mcp_utilization, 2),
            },
        }

    def format_report(self) -> str:
        """Format metrics as human-readable report."""
        summary = self.get_summary()

        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     📊 OPERATIONAL METRICS REPORT                            ║
║                   Inspired by GTG-1002 Tempo Analysis                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

SESSION OVERVIEW:
  • Duration: {summary['session']['duration_minutes']:.1f} minutes ({summary['session']['duration_seconds']:.0f}s)
  • Total Attacks: {summary['attacks']['total']}
  • Successful Attacks: {summary['attacks']['successful']} ({summary['attacks']['success_rate']:.1f}%)

OPERATIONAL TEMPO:
  • Attacks per Minute: {summary['attacks']['attacks_per_minute']:.2f}
  • Requests per Second: {summary['attacks']['requests_per_second']:.2f}
  • Average Attack Latency: {summary['attacks']['average_latency']:.1f}s
  • Median Attack Latency: {summary['attacks']['median_latency']:.1f}s

FINDINGS DETECTED:
  • Critical: {summary['findings']['critical']}
  • High: {summary['findings']['high']}

AGENT EFFICIENCY:
"""

        for agent_name, agent_data in summary["agents"].items():
            report += f"  • {agent_name}:\n"
            report += f"    - Attacks: {agent_data['total_attacks']}\n"
            report += f"    - Success Rate: {agent_data['success_rate']:.1f}%\n"
            report += f"    - Avg Latency: {agent_data['average_latency']:.1f}s\n"
            report += f"    - Critical/High: {agent_data['critical_findings']}/{agent_data['high_findings']}\n"

        report += f"""
THINK-MCP UTILIZATION:
  • Total Operations: {summary['think_mcp']['total_operations']}
  • Consensus: {summary['think_mcp']['consensus']}
  • Validation: {summary['think_mcp']['validation']}
  • Learning: {summary['think_mcp']['learning']}
  • Utilization Rate: {summary['think_mcp']['utilization']:.1f}%

TAVILY RECONNAISSANCE:
  • Searches: {summary['tavily']['searches']}
  • Results Retrieved: {summary['tavily']['results']}

DEEP AGENTS:
  • Subagent Refinements: {summary['deep_agents']['subagent_refinements']}

╔══════════════════════════════════════════════════════════════════════════════╗
║                        EFFICIENCY SCORES                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

  Overall Efficiency: {summary['scores']['efficiency']:.1f}/100

  Component Breakdown:
    • Success Rate:          {summary['scores']['success_rate']:.1f}/100 (40% weight)
    • Operational Tempo:     {summary['scores']['tempo']:.1f}/100 (30% weight)
    • Agent Coordination:    {summary['scores']['coordination']:.1f}/100 (20% weight)
    • Think-MCP Utilization: {summary['scores']['think_mcp_utilization']:.1f}/100 (10% weight)

╔══════════════════════════════════════════════════════════════════════════════╗
║                   COMPARISON TO GTG-1002 CAPABILITIES                        ║
╚══════════════════════════════════════════════════════════════════════════════╝

  GTG-1002 (Malicious):
    • Peak RPS: "Multiple operations per second" (unthrottled)
    • AI Autonomy: 80-90%
    • Human Oversight: 10-20%
    • Safeguards: NONE

  PenBot (Ethical):
    • Current RPS: {summary['attacks']['requests_per_second']:.2f}
    • AI Autonomy: ~{100 - summary['think_mcp']['utilization']:.0f}% (autonomous)
    • Human Oversight: ~{summary['think_mcp']['utilization']:.0f}% (Think-MCP gates)
    • Safeguards: Authorization gates, validation, logging

Reference: https://assets.anthropic.com/m/ec212e6566a0d47/original/Disrupting-the-first-reported-AI-orchestrated-cyber-espionage-campaign.pdf
"""

        return report


# Global instance for easy access
_metrics_instance: Optional[OperationalMetrics] = None


def get_metrics() -> OperationalMetrics:
    """Get global metrics instance."""
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = OperationalMetrics()
    return _metrics_instance


def reset_metrics():
    """Reset global metrics instance."""
    global _metrics_instance
    _metrics_instance = OperationalMetrics()
