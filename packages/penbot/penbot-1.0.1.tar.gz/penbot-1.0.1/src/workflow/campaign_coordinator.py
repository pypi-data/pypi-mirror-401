"""
Campaign Coordination Node

Integrates AttackCampaignPlanner with the workflow graph.
"""

from typing import Dict, Any
from src.utils.logging import get_logger
from src.campaign.planner import AttackCampaignPlanner

logger = get_logger(__name__)

# Global campaign planner instance (persists across node calls)
_campaign_planner: Dict[str, AttackCampaignPlanner] = {}


def get_campaign_planner(session_id: str) -> AttackCampaignPlanner:
    """
    Get or create campaign planner for a session.

    Args:
        session_id: Test session ID

    Returns:
        AttackCampaignPlanner instance for this session
    """
    if session_id not in _campaign_planner:
        _campaign_planner[session_id] = AttackCampaignPlanner()
        logger.info(
            "campaign_planner_created", session_id=session_id, initial_phase="reconnaissance"
        )
    return _campaign_planner[session_id]


def update_campaign_phase(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update campaign phase based on recent results.

    This node runs after each attack/response cycle to:
    1. Evaluate if the attempt met phase objectives
    2. Determine if should advance to next phase
    3. Update state with current campaign phase

    Args:
        state: Current PenTestState

    Returns:
        State updates (campaign phase info)
    """
    session_id = state["test_session_id"]
    planner = get_campaign_planner(session_id)

    # Get recent results
    conversation_history = state.get("conversation_history", [])
    findings = state.get("security_findings", [])
    target_responses = state.get("target_responses", [])

    # Evaluate if last attempt was successful for phase objectives
    success = planner.evaluate_phase_success(
        conversation_history=conversation_history,
        findings=findings,
        target_responses=target_responses,
    )

    # Record attempt
    planner.record_attempt(success=success, findings=findings)

    # Check if should advance phase
    if planner.should_advance_phase():
        new_phase = planner.advance_phase()
        logger.info(
            "campaign_phase_advanced",
            session_id=session_id,
            new_phase=new_phase.value,
            previous_phase_attempts=state.get("campaign_phase_attempts", 0),
            previous_phase_successes=state.get("campaign_phase_successes", 0),
        )

    # Get current phase context
    planner.get_phase_context()

    # Update state
    return {
        "campaign_phase": planner.get_current_phase().value,
        "campaign_phase_attempts": planner.phase_attempts,
        "campaign_phase_successes": planner.phase_successes,
        "campaign_history": planner.phase_history.copy(),
    }


def get_campaign_instructions(state: Dict[str, Any]) -> str:
    """
    Get campaign instructions for agents based on current phase.

    Args:
        state: Current PenTestState

    Returns:
        Instructions string for agents
    """
    session_id = state["test_session_id"]
    planner = get_campaign_planner(session_id)

    return planner.get_phase_instructions()


def get_campaign_context_for_agents(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get full campaign context for agent coordination.

    Args:
        state: Current PenTestState

    Returns:
        Dictionary with campaign context
    """
    session_id = state["test_session_id"]
    planner = get_campaign_planner(session_id)

    phase_context = planner.get_phase_context()
    campaign_summary = planner.get_campaign_summary()

    return {
        "current_phase": phase_context["phase"],
        "phase_description": phase_context["description"],
        "phase_instructions": phase_context["instructions"],
        "phase_success_criteria": phase_context["success_criteria"],
        "phase_progress": {
            "attempts": phase_context["attempts"],
            "successes": phase_context["successes"],
            "max_attempts": phase_context["max_attempts"],
            "success_rate": phase_context["successes"] / max(phase_context["attempts"], 1),
        },
        "campaign_summary": campaign_summary,
    }


def cleanup_campaign_planner(session_id: str) -> None:
    """
    Clean up campaign planner after test completion.

    Args:
        session_id: Test session ID
    """
    if session_id in _campaign_planner:
        planner = _campaign_planner[session_id]
        summary = planner.get_campaign_summary()

        logger.info("campaign_completed", session_id=session_id, **summary)

        del _campaign_planner[session_id]
