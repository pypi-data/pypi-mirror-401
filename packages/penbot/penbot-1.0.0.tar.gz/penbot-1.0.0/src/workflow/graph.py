"""LangGraph workflow construction for penetration testing."""

from typing import Literal, Optional
from langgraph.graph import StateGraph, START, END

from .state import PenTestState
from .nodes import (
    reconnaissance_search,
    coordinate_agents,
    generate_attack,
    execute_attack,
    analyze_response,
    summarize_if_needed,
    calculate_score,
    generate_report,
)
from src.utils.logging import get_logger

logger = get_logger(__name__)


def route_after_analysis(
    state: PenTestState,
) -> Literal["critical_finding", "continue_testing", "complete"]:
    """
    Route workflow after response analysis.

    Determines whether to:
    - Stop for critical finding review
    - Continue testing
    - Complete the test

    Args:
        state: Current test state

    Returns:
        Next node to execute
    """
    findings = state["security_findings"]

    # Check for critical findings (could implement human-in-the-loop here)
    critical_findings = [f for f in findings if f["severity"] == "critical"]
    if critical_findings and state["current_attempt"] >= 3:
        # If we have critical findings and done at least 3 attempts, we can stop
        logger.info(
            "critical_findings_detected",
            test_session_id=state["test_session_id"],
            critical_count=len(critical_findings),
        )
        return "complete"

    # Check if we've reached max attempts
    if state["current_attempt"] >= state["max_attempts"]:
        logger.info(
            "max_attempts_reached",
            test_session_id=state["test_session_id"],
            attempts=state["current_attempt"],
        )
        return "complete"

    # Continue testing
    return "continue_testing"


def create_pentest_workflow(checkpoint_db: Optional[str] = "pentest_sessions.db") -> StateGraph:
    """
    Create and compile the penetration testing workflow.

    The workflow orchestrates:
    1. Agent coordination - Agents vote on next attack
    2. Attack generation - Generate attack payload
    3. Attack execution - Send to target chatbot
    4. Response analysis - Detect vulnerabilities
    5. Decision point - Continue or complete?
    6. Report generation - Final report

    Args:
        checkpoint_db: Path to SQLite database for checkpointing

    Returns:
        Compiled LangGraph workflow

    Example:
        >>> app = create_pentest_workflow()
        >>> initial_state = create_initial_state(...)
        >>> config = {"configurable": {"thread_id": "test-123"}}
        >>> result = await app.ainvoke(initial_state, config)
    """
    logger.info("creating_pentest_workflow", checkpoint_db=checkpoint_db)

    # Create workflow
    workflow = StateGraph(PenTestState)

    # Add nodes
    workflow.add_node(
        "reconnaissance_search", reconnaissance_search
    )  # Tavily pre-test intelligence gathering
    workflow.add_node("coordinate_agents", coordinate_agents)
    workflow.add_node("generate_attack", generate_attack)
    workflow.add_node("execute_attack", execute_attack)
    workflow.add_node("analyze_response", analyze_response)
    workflow.add_node(
        "summarize_if_needed", summarize_if_needed
    )  # Auto-summarize long conversations
    workflow.add_node("calculate_score", calculate_score)
    workflow.add_node("generate_report", generate_report)

    # Build graph structure
    workflow.add_edge(START, "reconnaissance_search")  # Start with Tavily reconnaissance
    workflow.add_edge("reconnaissance_search", "coordinate_agents")  # Then begin attack loop
    workflow.add_edge("coordinate_agents", "generate_attack")
    workflow.add_edge("generate_attack", "execute_attack")
    workflow.add_edge("execute_attack", "analyze_response")
    workflow.add_edge("analyze_response", "summarize_if_needed")  # Summarize before scoring
    workflow.add_edge("summarize_if_needed", "calculate_score")

    # Conditional routing after analysis
    workflow.add_conditional_edges(
        "calculate_score",
        route_after_analysis,
        {
            "critical_finding": "generate_report",
            "continue_testing": "coordinate_agents",  # Loop back
            "complete": "generate_report",
        },
    )

    workflow.add_edge("generate_report", END)

    # Compile workflow with checkpointing (enabled by default for resumability)
    if checkpoint_db:
        try:
            # Try to import and use checkpointer if available
            from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
            import os

            # Ensure checkpoint directory exists
            checkpoint_dir = (
                os.path.dirname(checkpoint_db) if os.path.dirname(checkpoint_db) else "."
            )
            os.makedirs(checkpoint_dir, exist_ok=True)

            checkpointer = AsyncSqliteSaver.from_conn_string(checkpoint_db)
            app = workflow.compile(checkpointer=checkpointer)
            logger.info(
                "pentest_workflow_created_with_checkpoint",
                checkpoint_db=checkpoint_db,
                checkpoint_enabled=True,
            )
        except ImportError:
            logger.warning("checkpoint_not_available_compiling_without_checkpoint")
            app = workflow.compile()
    else:
        app = workflow.compile()
        logger.info("pentest_workflow_created_without_checkpoint", checkpoint_enabled=False)

    return app
