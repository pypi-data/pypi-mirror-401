"""
Multi-Turn Attack Graph Module

Models adversarial conversations as a directed graph where:
- Nodes = Conversation states (partial successes, context changes)
- Edges = Attack attempts with success/failure conditions
- Paths = Complete attack chains leading to vulnerabilities

This enables:
1. Dynamic path planning based on target responses
2. Backtracking when attacks fail
3. Learning optimal attack sequences
4. Identifying multiple paths to same vulnerability

Research Contribution: First graph-based attack planning for LLM security testing.
Target Venues: IEEE S&P, ACM CCS, NeurIPS (AI safety track)
"""

import json
import hashlib
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict
import heapq

from src.utils.logging import get_logger

logger = get_logger(__name__)


class NodeType(str, Enum):
    """Types of nodes in the attack graph."""

    INITIAL = "initial"  # Starting state
    PROBE = "probe"  # Information gathering state
    PARTIAL_SUCCESS = "partial"  # Some progress made
    JAILBREAK = "jailbreak"  # Safety bypass achieved
    EXPLOIT = "exploit"  # Active exploitation
    GOAL = "goal"  # Attack objective achieved
    DEAD_END = "dead_end"  # No further progress possible
    BACKTRACK = "backtrack"  # Need to try alternative path


class EdgeOutcome(str, Enum):
    """Possible outcomes of an attack edge."""

    SUCCESS = "success"  # Attack achieved its goal
    PARTIAL = "partial"  # Some progress but not complete
    BLOCKED = "blocked"  # Target blocked the attack
    DETECTED = "detected"  # Attack was detected/flagged
    ERROR = "error"  # Technical error occurred
    TIMEOUT = "timeout"  # Response timed out


@dataclass
class AttackNode:
    """
    A node in the attack graph representing a conversation state.

    Attributes:
        node_id: Unique identifier
        node_type: Type of this node
        state_hash: Hash of conversation state for deduplication
        conversation_context: Summary of conversation so far
        partial_success_indicators: What progress has been made
        available_attacks: Attack vectors available from this state
        visit_count: How many times this node has been visited
        success_rate: Historical success rate from this node
        created_at: When this node was created
        metadata: Additional node metadata
    """

    node_id: str
    node_type: NodeType
    state_hash: str
    conversation_context: Dict[str, Any] = field(default_factory=dict)
    partial_success_indicators: List[str] = field(default_factory=list)
    available_attacks: List[str] = field(default_factory=list)
    visit_count: int = 0
    success_rate: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type.value,
            "state_hash": self.state_hash,
            "conversation_context": self.conversation_context,
            "partial_success_indicators": self.partial_success_indicators,
            "available_attacks": self.available_attacks,
            "visit_count": self.visit_count,
            "success_rate": self.success_rate,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class AttackEdge:
    """
    An edge in the attack graph representing an attack attempt.

    Attributes:
        edge_id: Unique identifier
        source_node: Starting node ID
        target_node: Destination node ID
        attack_type: Type of attack (jailbreak, encoding, etc.)
        attack_pattern: Specific pattern used
        attack_query: The actual attack query
        outcome: Result of the attack
        response_summary: Brief summary of target response
        confidence: Confidence in this edge's effectiveness
        traversal_count: How many times this edge has been traversed
        success_count: How many times traversal led to success
        created_at: When this edge was created
        metadata: Additional edge metadata
    """

    edge_id: str
    source_node: str
    target_node: str
    attack_type: str
    attack_pattern: str
    attack_query: str
    outcome: EdgeOutcome
    response_summary: str = ""
    confidence: float = 0.5
    traversal_count: int = 0
    success_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """Calculate success rate for this edge."""
        if self.traversal_count == 0:
            return 0.0
        return self.success_count / self.traversal_count

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "edge_id": self.edge_id,
            "source_node": self.source_node,
            "target_node": self.target_node,
            "attack_type": self.attack_type,
            "attack_pattern": self.attack_pattern,
            "attack_query": self.attack_query,
            "outcome": self.outcome.value,
            "response_summary": self.response_summary,
            "confidence": self.confidence,
            "traversal_count": self.traversal_count,
            "success_count": self.success_count,
            "success_rate": self.success_rate,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata,
        }


class AttackGraph:
    """
    Directed graph representing multi-turn attack possibilities.

    The graph grows dynamically as attacks are attempted:
    - New nodes are created when novel conversation states are reached
    - Edges are created/updated based on attack attempts and outcomes
    - Historical data influences future path selection

    Path Planning Strategy:
    1. Start from current node
    2. Use UCB1 (Upper Confidence Bound) to balance exploration/exploitation
    3. Prefer paths with high historical success
    4. Backtrack when dead ends are reached
    5. Learn from failed paths to avoid them in future
    """

    def __init__(self):
        """Initialize the attack graph."""
        self.nodes: Dict[str, AttackNode] = {}
        self.edges: Dict[str, AttackEdge] = {}

        # Adjacency lists for efficient traversal
        self.outgoing: Dict[str, List[str]] = defaultdict(list)  # node_id -> edge_ids
        self.incoming: Dict[str, List[str]] = defaultdict(list)  # node_id -> edge_ids

        # State hash to node mapping for deduplication
        self.state_to_node: Dict[str, str] = {}

        # Current position in the graph
        self.current_node_id: Optional[str] = None

        # Path history for this session
        self.traversal_history: List[str] = []  # edge_ids in order

        # Goal nodes reached
        self.goals_reached: List[str] = []

        # Create initial node
        self._create_initial_node()

        logger.info("attack_graph_initialized")

    def _create_initial_node(self):
        """Create the initial starting node."""
        import uuid

        node_id = f"node_{uuid.uuid4().hex[:8]}"
        state_hash = self._compute_state_hash({})

        initial_node = AttackNode(
            node_id=node_id,
            node_type=NodeType.INITIAL,
            state_hash=state_hash,
            conversation_context={},
            available_attacks=[
                "jailbreak",
                "encoding",
                "impersonation",
                "rag_poisoning",
                "tool_exploit",
                "token_soup",
            ],
        )

        self.nodes[node_id] = initial_node
        self.state_to_node[state_hash] = node_id
        self.current_node_id = node_id

    def _compute_state_hash(self, context: Dict[str, Any]) -> str:
        """Compute a hash of the conversation state for deduplication."""
        # Extract key features that define the state
        key_features = {
            "message_count": len(context.get("messages", [])),
            "partial_successes": sorted(context.get("partial_successes", [])),
            "blocked_attacks": sorted(context.get("blocked_attacks", [])),
            "last_response_type": context.get("last_response_type", ""),
        }

        # Hash the features
        content = json.dumps(key_features, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def get_current_node(self) -> Optional[AttackNode]:
        """Get the current node in the graph."""
        if self.current_node_id:
            return self.nodes.get(self.current_node_id)
        return None

    def add_attack_result(
        self,
        attack_type: str,
        attack_pattern: str,
        attack_query: str,
        response: str,
        outcome: EdgeOutcome,
        new_context: Dict[str, Any],
        partial_successes: List[str] = None,
        is_goal_reached: bool = False,
    ) -> Tuple[AttackNode, AttackEdge]:
        """
        Add an attack result to the graph, creating new nodes/edges as needed.

        Args:
            attack_type: Type of attack attempted
            attack_pattern: Specific pattern used
            attack_query: The attack query sent
            response: Target's response (summarized)
            outcome: Result of the attack
            new_context: Updated conversation context
            partial_successes: Any partial successes achieved
            is_goal_reached: Whether this attack achieved the goal

        Returns:
            Tuple of (new_node, edge)
        """
        import uuid

        source_node = self.current_node_id
        if not source_node:
            raise ValueError("No current node set")

        # Compute state hash for new state
        new_state_hash = self._compute_state_hash(new_context)

        # Check if this state already exists
        if new_state_hash in self.state_to_node:
            target_node_id = self.state_to_node[new_state_hash]
            target_node = self.nodes[target_node_id]
            target_node.visit_count += 1
        else:
            # Create new node
            target_node_id = f"node_{uuid.uuid4().hex[:8]}"

            # Determine node type
            if is_goal_reached:
                node_type = NodeType.GOAL
            elif outcome == EdgeOutcome.BLOCKED:
                node_type = NodeType.DEAD_END
            elif partial_successes:
                node_type = NodeType.PARTIAL_SUCCESS
            elif outcome == EdgeOutcome.SUCCESS:
                node_type = NodeType.JAILBREAK
            else:
                node_type = NodeType.PROBE

            target_node = AttackNode(
                node_id=target_node_id,
                node_type=node_type,
                state_hash=new_state_hash,
                conversation_context=new_context,
                partial_success_indicators=partial_successes or [],
                visit_count=1,
            )

            self.nodes[target_node_id] = target_node
            self.state_to_node[new_state_hash] = target_node_id

        # Create edge
        edge_id = f"edge_{uuid.uuid4().hex[:8]}"
        edge = AttackEdge(
            edge_id=edge_id,
            source_node=source_node,
            target_node=target_node_id,
            attack_type=attack_type,
            attack_pattern=attack_pattern,
            attack_query=attack_query,
            outcome=outcome,
            response_summary=response[:200] if len(response) > 200 else response,
            traversal_count=1,
            success_count=1 if outcome in [EdgeOutcome.SUCCESS, EdgeOutcome.PARTIAL] else 0,
        )

        self.edges[edge_id] = edge
        self.outgoing[source_node].append(edge_id)
        self.incoming[target_node_id].append(edge_id)

        # Update traversal history
        self.traversal_history.append(edge_id)

        # Update current position
        self.current_node_id = target_node_id

        # Track goals
        if is_goal_reached:
            self.goals_reached.append(target_node_id)

        logger.info(
            "attack_result_added",
            source_node=source_node,
            target_node=target_node_id,
            outcome=outcome.value,
            is_goal=is_goal_reached,
        )

        return target_node, edge

    def select_next_attack(
        self, available_agents: List[str], exploration_weight: float = 1.414
    ) -> Dict[str, Any]:
        """
        Select the next attack using UCB1 algorithm.

        UCB1 balances:
        - Exploitation: Choose attacks with high historical success
        - Exploration: Try less-explored attacks to discover new paths

        Args:
            available_agents: List of available attack agents
            exploration_weight: Controls exploration vs exploitation (√2 is optimal)

        Returns:
            Dictionary with recommended attack details
        """
        import math

        current_node = self.get_current_node()
        if not current_node:
            return {"agent": available_agents[0], "reason": "no_current_node"}

        # Get outgoing edges from current node
        outgoing_edge_ids = self.outgoing.get(self.current_node_id, [])

        # If no previous attacks from this state, explore randomly
        if not outgoing_edge_ids:
            return {
                "agent": available_agents[0],
                "reason": "unexplored_state",
                "node_type": current_node.node_type.value,
            }

        # Calculate UCB1 scores for each agent type
        total_visits = sum(self.edges[eid].traversal_count for eid in outgoing_edge_ids)

        agent_scores: Dict[str, float] = {}

        for agent in available_agents:
            # Find edges for this agent type
            agent_edges = [
                self.edges[eid] for eid in outgoing_edge_ids if self.edges[eid].attack_type == agent
            ]

            if not agent_edges:
                # Unexplored agent - high exploration bonus
                agent_scores[agent] = float("inf")
            else:
                # Calculate average success rate
                total_success = sum(e.success_count for e in agent_edges)
                total_traversals = sum(e.traversal_count for e in agent_edges)

                if total_traversals == 0:
                    agent_scores[agent] = float("inf")
                else:
                    # UCB1 formula: mean + c * sqrt(ln(total) / agent_count)
                    mean_success = total_success / total_traversals
                    exploration_bonus = exploration_weight * math.sqrt(
                        math.log(total_visits + 1) / total_traversals
                    )
                    agent_scores[agent] = mean_success + exploration_bonus

        # Select agent with highest UCB1 score
        best_agent = max(agent_scores.items(), key=lambda x: x[1])

        # Find best edge for this agent (if exists)
        best_edge = None
        best_pattern = None

        for eid in outgoing_edge_ids:
            edge = self.edges[eid]
            if edge.attack_type == best_agent[0]:
                if best_edge is None or edge.success_rate > best_edge.success_rate:
                    best_edge = edge
                    best_pattern = edge.attack_pattern

        return {
            "agent": best_agent[0],
            "ucb_score": best_agent[1] if best_agent[1] != float("inf") else 999.0,
            "suggested_pattern": best_pattern,
            "reason": "ucb1_selection",
            "all_scores": {k: v if v != float("inf") else 999.0 for k, v in agent_scores.items()},
        }

    def backtrack(self, steps: int = 1) -> Optional[str]:
        """
        Backtrack to a previous node in the graph.

        Args:
            steps: Number of steps to backtrack

        Returns:
            New current node ID or None if can't backtrack
        """
        if len(self.traversal_history) < steps:
            logger.warning(
                "cannot_backtrack", requested=steps, available=len(self.traversal_history)
            )
            return None

        # Remove last N edges from history
        for _ in range(steps):
            if self.traversal_history:
                edge_id = self.traversal_history.pop()
                edge = self.edges.get(edge_id)
                if edge:
                    self.current_node_id = edge.source_node

        logger.info("backtracked", steps=steps, current_node=self.current_node_id)
        return self.current_node_id

    def find_path_to_goal(
        self, goal_type: NodeType = NodeType.GOAL, max_depth: int = 10
    ) -> List[str]:
        """
        Find shortest path from current node to any goal node.

        Uses Dijkstra's algorithm with edge success rate as weight.

        Args:
            goal_type: Type of goal node to find
            max_depth: Maximum search depth

        Returns:
            List of edge IDs forming the path, or empty if no path
        """
        if not self.current_node_id:
            return []

        # Priority queue: (cost, node_id, path_so_far)
        pq = [(0.0, self.current_node_id, [])]
        visited = set()

        while pq:
            cost, node_id, path = heapq.heappop(pq)

            if node_id in visited:
                continue
            visited.add(node_id)

            # Check if this is a goal
            node = self.nodes.get(node_id)
            if node and node.node_type == goal_type:
                return path

            # Check depth limit
            if len(path) >= max_depth:
                continue

            # Explore outgoing edges
            for edge_id in self.outgoing.get(node_id, []):
                edge = self.edges.get(edge_id)
                if not edge:
                    continue

                target = edge.target_node
                if target in visited:
                    continue

                # Cost = 1 - success_rate (lower is better)
                edge_cost = 1.0 - edge.success_rate
                new_cost = cost + edge_cost

                heapq.heappush(pq, (new_cost, target, path + [edge_id]))

        return []  # No path found

    def get_attack_chain(self, goal_node_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get the attack chain leading to current position or specified goal.

        Returns:
            List of attack details in order
        """
        target_node = goal_node_id or self.current_node_id
        if not target_node:
            return []

        # Reconstruct path by following incoming edges
        chain = []
        current = target_node
        visited = set()

        while current:
            if current in visited:
                break
            visited.add(current)

            incoming_edges = self.incoming.get(current, [])
            if not incoming_edges:
                break

            # Take the most recent edge (last in list)
            edge_id = incoming_edges[-1]
            edge = self.edges.get(edge_id)
            if edge:
                chain.append(edge.to_dict())
                current = edge.source_node
            else:
                break

        # Reverse to get chronological order
        chain.reverse()
        return chain

    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        node_types = defaultdict(int)
        for node in self.nodes.values():
            node_types[node.node_type.value] += 1

        outcome_counts = defaultdict(int)
        for edge in self.edges.values():
            outcome_counts[edge.outcome.value] += 1

        total_traversals = sum(e.traversal_count for e in self.edges.values())
        total_successes = sum(e.success_count for e in self.edges.values())

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "node_types": dict(node_types),
            "edge_outcomes": dict(outcome_counts),
            "goals_reached": len(self.goals_reached),
            "current_path_length": len(self.traversal_history),
            "overall_success_rate": (
                total_successes / total_traversals if total_traversals > 0 else 0.0
            ),
            "exploration_coverage": len(self.nodes) / max(len(self.edges), 1),
        }

    def export_to_dict(self) -> Dict[str, Any]:
        """Export the graph to a dictionary for serialization."""
        return {
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "edges": {eid: edge.to_dict() for eid, edge in self.edges.items()},
            "outgoing": dict(self.outgoing),
            "incoming": dict(self.incoming),
            "current_node_id": self.current_node_id,
            "traversal_history": self.traversal_history,
            "goals_reached": self.goals_reached,
            "statistics": self.get_statistics(),
        }

    def visualize_ascii(self, max_nodes: int = 10) -> str:
        """
        Generate ASCII visualization of the graph.

        Returns:
            ASCII art representation of the graph
        """
        lines = ["Attack Graph Visualization", "=" * 40]

        # Show current position
        lines.append(f"Current Node: {self.current_node_id}")
        lines.append(f"Path Length: {len(self.traversal_history)}")
        lines.append("")

        # Show nodes by type
        for node_type in NodeType:
            type_nodes = [n for n in self.nodes.values() if n.node_type == node_type]
            if type_nodes:
                lines.append(f"[{node_type.value.upper()}] ({len(type_nodes)} nodes)")
                for node in type_nodes[:max_nodes]:
                    marker = "→" if node.node_id == self.current_node_id else " "
                    lines.append(f"  {marker} {node.node_id[:12]} (visits: {node.visit_count})")

        lines.append("")
        lines.append(f"Total Edges: {len(self.edges)}")
        lines.append(f"Goals Reached: {len(self.goals_reached)}")

        return "\n".join(lines)


class AttackPathPlanner:
    """
    Strategic path planner for multi-turn attacks.

    Uses the attack graph to plan optimal attack sequences,
    considering historical success rates and exploration needs.
    """

    def __init__(self, graph: AttackGraph):
        """Initialize the path planner."""
        self.graph = graph

        # Attack type priorities (can be adjusted)
        self.attack_priorities = {
            "jailbreak": 5,
            "encoding": 4,
            "impersonation": 4,
            "rag_poisoning": 3,
            "tool_exploit": 3,
            "token_soup": 2,
        }

    def plan_next_turn(
        self,
        available_agents: List[str],
        target_info: Dict[str, Any] = None,
        phase: str = "exploitation",
    ) -> Dict[str, Any]:
        """
        Plan the next attack turn.

        Args:
            available_agents: List of available agent types
            target_info: Information about the target
            phase: Current campaign phase

        Returns:
            Attack plan with recommended agent, pattern, and reasoning
        """
        current_node = self.graph.get_current_node()
        if not current_node:
            return {"error": "no_current_state"}

        # Get UCB1 recommendation
        ucb_recommendation = self.graph.select_next_attack(available_agents)

        # Check for known paths to goals
        known_path = self.graph.find_path_to_goal()

        # Consider node type
        if current_node.node_type == NodeType.DEAD_END:
            # Need to backtrack
            return {
                "action": "backtrack",
                "reason": "current_state_is_dead_end",
                "recommended_steps": 1,
            }

        if current_node.node_type == NodeType.PARTIAL_SUCCESS:
            # Build on success - recommend related attacks
            return {
                "action": "attack",
                "agent": ucb_recommendation["agent"],
                "pattern": ucb_recommendation.get("suggested_pattern"),
                "reason": "building_on_partial_success",
                "partial_indicators": current_node.partial_success_indicators,
                "ucb_scores": ucb_recommendation.get("all_scores", {}),
            }

        if known_path:
            # Follow known successful path
            first_edge_id = known_path[0]
            edge = self.graph.edges.get(first_edge_id)
            if edge:
                return {
                    "action": "attack",
                    "agent": edge.attack_type,
                    "pattern": edge.attack_pattern,
                    "reason": "following_known_successful_path",
                    "path_length": len(known_path),
                    "expected_success_rate": edge.success_rate,
                }

        # Default to UCB1 recommendation
        return {
            "action": "attack",
            "agent": ucb_recommendation["agent"],
            "pattern": ucb_recommendation.get("suggested_pattern"),
            "reason": ucb_recommendation["reason"],
            "ucb_scores": ucb_recommendation.get("all_scores", {}),
        }

    def analyze_failed_paths(self) -> List[Dict[str, Any]]:
        """
        Analyze paths that led to dead ends.

        Returns:
            List of failed path analyses with recommendations
        """
        analyses = []

        dead_end_nodes = [n for n in self.graph.nodes.values() if n.node_type == NodeType.DEAD_END]

        for node in dead_end_nodes:
            # Get path to this dead end
            path = []
            for edge_id in self.graph.incoming.get(node.node_id, []):
                edge = self.graph.edges.get(edge_id)
                if edge:
                    path.append(
                        {
                            "attack_type": edge.attack_type,
                            "pattern": edge.attack_pattern,
                            "outcome": edge.outcome.value,
                        }
                    )

            analyses.append(
                {
                    "dead_end_node": node.node_id,
                    "path_to_failure": path,
                    "recommendation": self._generate_failure_recommendation(path),
                }
            )

        return analyses

    def _generate_failure_recommendation(self, path: List[Dict[str, Any]]) -> str:
        """Generate recommendation based on failed path."""
        if not path:
            return "No path data available"

        last_attack = path[-1]
        attack_type = last_attack.get("attack_type", "unknown")

        recommendations = {
            "jailbreak": "Try encoding-based bypass or social engineering approach",
            "encoding": "Try different encoding method or combine with jailbreak",
            "impersonation": "Escalate authority level or try technical approach",
            "rag_poisoning": "Try different injection method or chunk boundary exploit",
            "tool_exploit": "Try different tool or argument injection technique",
        }

        return recommendations.get(attack_type, "Try alternative attack vector")
