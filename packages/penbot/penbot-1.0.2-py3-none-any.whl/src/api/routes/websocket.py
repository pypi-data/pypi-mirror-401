"""WebSocket endpoints for real-time penetration test streaming."""

from typing import Dict, Any
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi import Body
from pydantic import BaseModel
from datetime import datetime, timezone

from src.utils.logging import get_logger
from src.utils.metrics import increment_ws_connections, decrement_ws_connections

# from src.workflow.graph import app as workflow_app  # Uncomment when workflow is ready

logger = get_logger(__name__)

router = APIRouter(tags=["websocket"])


class ConnectionManager:
    """Manage active WebSocket connections."""

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept and register a WebSocket connection."""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        increment_ws_connections()  # Prometheus metric
        logger.info("websocket_connected", session_id=session_id)

    def disconnect(self, session_id: str):
        """Remove a WebSocket connection."""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            decrement_ws_connections()  # Prometheus metric
            logger.info("websocket_disconnected", session_id=session_id)

    async def send_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """Send event to a specific session's WebSocket."""
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_json(
                    {
                        "type": event_type,
                        "data": data,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                )
            except Exception as e:
                logger.error("websocket_send_failed", session_id=session_id, error=str(e))
                self.disconnect(session_id)


manager = ConnectionManager()


@router.websocket("/pentest/{session_id}")
async def pentest_stream(websocket: WebSocket, session_id: str):
    """
    Stream penetration test progress via WebSocket.

    Events sent:
    - test_started: Test initialization
    - attack_generated: New attack created
    - attack_sent: Attack sent to target
    - response_received: Response from target
    - finding_detected: Security finding identified
    - agent_consultation: Agent coordination event
    - test_complete: Test finished
    - error_occurred: Error during test

    Args:
        websocket: WebSocket connection
        session_id: Unique test session identifier
    """
    await manager.connect(websocket, session_id)

    try:
        # Send initial connection confirmation
        await manager.send_event(
            session_id, "connected", {"message": "WebSocket connected", "session_id": session_id}
        )

        # Keep connection alive and listen for client messages
        while True:
            # Receive any client messages (e.g., stop command)
            data = await websocket.receive_json()

            if data.get("command") == "stop":
                logger.info("stop_command_received", session_id=session_id)
                await manager.send_event(
                    session_id, "test_stopped", {"message": "Test stopped by user"}
                )
                break

            elif data.get("command") == "ping":
                await manager.send_event(session_id, "pong", {"message": "alive"})

    except WebSocketDisconnect:
        logger.info("websocket_client_disconnected", session_id=session_id)
    except Exception as e:
        logger.error("websocket_error", session_id=session_id, error=str(e))
        try:
            await manager.send_event(session_id, "error_occurred", {"error": str(e)})
        except Exception:
            pass
    finally:
        manager.disconnect(session_id)


async def stream_test_event(session_id: str, event_type: str, data: Dict[str, Any]):
    """
    Helper function to send events to a specific session.

    Can be called from workflow nodes to push real-time updates.

    Args:
        session_id: Test session ID
        event_type: Type of event (attack_generated, finding_detected, etc.)
        data: Event data
    """
    await manager.send_event(session_id, event_type, data)


class PublishEvent(BaseModel):
    """Schema for publishing an event to a WebSocket session."""

    type: str
    data: Dict[str, Any]


@router.post("/publish/{session_id}")
async def publish_event(session_id: str, event: PublishEvent):
    """
    Accept events over HTTP and forward to connected WebSocket clients.
    This allows external scripts/processes (e.g., test_orchestrated.py)
    to publish live updates without being in the same process as the API server.
    """
    await manager.send_event(session_id, event.type, event.data)
    return {"ok": True}


_attack_graphs: Dict[str, Dict[str, Any]] = {}


class AttackGraphNode(BaseModel):
    """Node in the attack graph for visualization."""

    id: str
    label: str
    type: str  # initial, probe, partial, jailbreak, exploit, goal, dead_end
    visit_count: int = 0
    success_rate: float = 0.0
    color: str = "#666666"


class AttackGraphEdge(BaseModel):
    """Edge in the attack graph for visualization."""

    from_id: str
    to_id: str
    label: str
    attack_type: str
    agent: str
    outcome: str  # success, partial, blocked
    reward: float = 0.0
    color: str = "#444444"


class AttackGraphData(BaseModel):
    """Complete attack graph data for visualization."""

    nodes: list
    edges: list
    stats: Dict[str, Any]


@router.get("/graph/{session_id}")
async def get_attack_graph(session_id: str):
    """
    Get the attack graph visualization data for a session.

    Returns nodes and edges formatted for vis.js network visualization.
    """
    if session_id not in _attack_graphs:
        return AttackGraphData(
            nodes=[], edges=[], stats={"total_nodes": 0, "total_edges": 0, "max_depth": 0}
        )

    return _attack_graphs[session_id]


@router.post("/graph/{session_id}/update")
async def update_attack_graph(session_id: str, graph_data: Dict[str, Any] = Body(...)):
    """
    Update the attack graph for a session (called from test runner).

    Converts AttackGraph internal format to vis.js visualization format.
    """
    nodes = []
    edges = []

    # Color mapping for node types
    node_colors = {
        "initial": "#00D4FF",  # Cyan - starting point
        "probe": "#888888",  # Gray - information gathering
        "partial": "#FFB86C",  # Orange - partial success
        "jailbreak": "#FF79C6",  # Pink - safety bypass
        "exploit": "#FF5555",  # Red - exploitation
        "goal": "#50FA7B",  # Green - objective achieved
        "dead_end": "#6272A4",  # Dark gray - no progress
        "backtrack": "#BD93F9",  # Purple - trying alternatives
    }

    # Edge colors based on outcome
    edge_colors = {
        "success": "#50FA7B",  # Green
        "partial": "#FFB86C",  # Orange
        "blocked": "#FF5555",  # Red
        "detected": "#FF79C6",  # Pink
        "error": "#6272A4",  # Gray
        "timeout": "#888888",  # Light gray
    }

    # Process nodes
    raw_nodes = graph_data.get("nodes", [])
    for node in raw_nodes:
        node_type = node.get("type", "probe")
        nodes.append(
            {
                "id": node["id"],
                "label": f"{node.get('label', node['id'][:8])}\n({node.get('visit_count', 0)} visits)",
                "type": node_type,
                "color": {
                    "background": node_colors.get(node_type, "#666666"),
                    "border": "#ffffff",
                    "highlight": {
                        "background": "#ffffff",
                        "border": node_colors.get(node_type, "#666666"),
                    },
                },
                "shape": "dot" if node_type != "goal" else "star",
                "size": 15 + (node.get("visit_count", 0) * 2),
                "title": f"Type: {node_type}\nVisits: {node.get('visit_count', 0)}\nSuccess Rate: {node.get('success_rate', 0):.1%}",
            }
        )

    # Process edges
    raw_edges = graph_data.get("edges", [])
    for edge in raw_edges:
        outcome = edge.get("outcome", "partial")
        edges.append(
            {
                "from": edge["from"],
                "to": edge["to"],
                "label": edge.get("attack_type", "attack")[:15],
                "color": edge_colors.get(outcome, "#444444"),
                "arrows": "to",
                "width": 1 + (edge.get("reward", 0) * 2),
                "title": f"Agent: {edge.get('agent', 'unknown')}\nPattern: {edge.get('pattern', 'unknown')}\nOutcome: {outcome}\nReward: {edge.get('reward', 0):.2f}",
                "smooth": {"type": "curvedCW", "roundness": 0.2},
            }
        )

    # Calculate stats
    stats = {
        "total_nodes": len(nodes),
        "total_edges": len(edges),
        "success_edges": len([e for e in raw_edges if e.get("outcome") == "success"]),
        "goal_nodes": len([n for n in raw_nodes if n.get("type") == "goal"]),
        "dead_ends": len([n for n in raw_nodes if n.get("type") == "dead_end"]),
    }

    # Store
    _attack_graphs[session_id] = AttackGraphData(nodes=nodes, edges=edges, stats=stats)

    # Also push to WebSocket for real-time updates
    await manager.send_event(
        session_id, "attack_graph_updated", {"nodes": nodes, "edges": edges, "stats": stats}
    )

    return {"ok": True, "stats": stats}


# Example of how to integrate with workflow:
# In workflow nodes, call:
# await stream_test_event(
#     state["test_session_id"],
#     "attack_generated",
#     {
#         "pattern": attack["pattern"],
#         "query_preview": attack["query"][:100],
#         "reasoning": attack["reasoning"]
#     }
# )
