"""API routes for report generation and session replay."""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from typing import Dict, Any
from pathlib import Path
import json

from src.reporting.owasp_compliance import OWASPComplianceReport
from src.reporting.detailed_report_generator import DetailedReportGenerator

router = APIRouter(prefix="/api/v1/reports", tags=["reports"])

# Sessions directory
SESSIONS_DIR = Path("sessions")

# In-memory storage for test results (for demo purposes)
# In production, this should be stored in a database
test_results_cache: Dict[str, Dict[str, Any]] = {}

# In-memory storage for findings (needed for detailed reports)
findings_cache: Dict[str, Dict[str, Any]] = {}


@router.post("/cache/{session_id}")
async def cache_test_results(session_id: str, results: Dict[str, Any]):
    """
    Cache test results for a session.

    This endpoint is called by test_orchestrated.py to store results
    for later report generation.
    """
    test_results_cache[session_id] = results
    return {"status": "cached", "session_id": session_id}


@router.get("/owasp/{session_id}")
async def get_owasp_report(session_id: str):
    """
    Generate OWASP LLM Top 10 2025 compliance report for a test session.

    Args:
        session_id: The test session ID

    Returns:
        Complete OWASP compliance report
    """
    # Check if we have results for this session
    if session_id not in test_results_cache:
        raise HTTPException(
            status_code=404,
            detail=f"No test results found for session {session_id}. "
            "Make sure the test has completed and results were cached.",
        )

    results = test_results_cache[session_id]

    # Extract necessary data
    findings = results.get("security_findings", [])
    target_name = results.get("target_name", "Unknown Target")
    started_at_str = results.get("started_at")
    completed_at_str = results.get("completed_at")

    # Parse timestamps
    if isinstance(started_at_str, str):
        started_at = datetime.fromisoformat(started_at_str.replace("Z", "+00:00"))
    else:
        started_at = started_at_str or datetime.now(timezone.utc)

    if isinstance(completed_at_str, str):
        completed_at = datetime.fromisoformat(completed_at_str.replace("Z", "+00:00"))
    else:
        completed_at = completed_at_str or datetime.now(timezone.utc)

    # Generate OWASP compliance report
    reporter = OWASPComplianceReport()

    report = reporter.generate_report(
        findings=findings,
        test_session_id=session_id,
        target_name=target_name,
        started_at=started_at,
        completed_at=completed_at,
    )

    return report


@router.delete("/cache/{session_id}")
async def clear_cached_results(session_id: str):
    """Clear cached test results for a session."""
    if session_id in test_results_cache:
        del test_results_cache[session_id]
        return {"status": "cleared", "session_id": session_id}
    else:
        raise HTTPException(
            status_code=404, detail=f"No cached results found for session {session_id}"
        )


@router.get("/cache")
async def list_cached_sessions():
    """List all cached test sessions."""
    return {"sessions": list(test_results_cache.keys()), "count": len(test_results_cache)}


@router.post("/findings/cache")
async def cache_finding(finding: Dict[str, Any]):
    """
    Cache a finding for detailed report generation.

    This is called when streaming findings to the dashboard.
    """
    finding_id = finding.get("finding_id")
    if finding_id:
        findings_cache[finding_id] = finding
        return {"status": "cached", "finding_id": finding_id}
    else:
        raise HTTPException(status_code=400, detail="Missing finding_id")


@router.get("/findings/{finding_id}/detailed-report")
async def get_detailed_report(finding_id: str):
    """
    Generate detailed security report for a specific finding.

    Args:
        finding_id: The unique finding ID

    Returns:
        Comprehensive detailed report with exploitation scenarios,
        remediation steps, code examples, and OWASP mapping
    """
    # Check if we have this finding cached
    if finding_id not in findings_cache:
        raise HTTPException(
            status_code=404,
            detail=f"Finding {finding_id} not found. Make sure the finding was cached.",
        )

    finding = findings_cache[finding_id]

    # Generate detailed report
    generator = DetailedReportGenerator()
    report = generator.generate_report(finding)

    return report


@router.get("/sessions")
async def list_sessions():
    """
    List all saved test sessions available for replay.

    Returns:
        List of sessions with metadata (id, target, date, attack count, finding count)
    """
    sessions = []

    if not SESSIONS_DIR.exists():
        return {"sessions": [], "count": 0}

    for session_file in SESSIONS_DIR.glob("*.json"):
        try:
            with open(session_file, "r") as f:
                data = json.load(f)

            sessions.append(
                {
                    "session_id": data.get("test_session_id", session_file.stem),
                    "target_name": data.get("target_name", "Unknown"),
                    "started_at": data.get("started_at"),
                    "completed_at": data.get("completed_at"),
                    "attack_count": len(data.get("attack_attempts", [])),
                    "finding_count": len(data.get("security_findings", [])),
                    "status": data.get("test_status", "unknown"),
                    "max_attempts": data.get("max_attempts", 0),
                    "current_attempt": data.get("current_attempt", 0),
                }
            )
        except Exception:
            # Skip invalid files
            continue

    # Sort by date (newest first)
    sessions.sort(key=lambda x: x.get("started_at", ""), reverse=True)

    return {"sessions": sessions, "count": len(sessions)}


@router.get("/sessions/{session_id}")
async def get_session(session_id: str):
    """
    Get full session data for replay.

    Args:
        session_id: The session ID to load

    Returns:
        Complete session data including all attacks and responses
    """
    session_file = SESSIONS_DIR / f"{session_id}.json"

    if not session_file.exists():
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    try:
        with open(session_file, "r") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading session: {str(e)}")


@router.get("/sessions/{session_id}/chain")
async def get_attack_chain(session_id: str):
    """
    Get attack chain formatted for step-by-step replay.

    Returns each attack with its corresponding response and any findings,
    in a format optimized for the replay UI.
    """
    session_file = SESSIONS_DIR / f"{session_id}.json"

    if not session_file.exists():
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")

    try:
        with open(session_file, "r") as f:
            data = json.load(f)

        attacks = data.get("attack_attempts", [])
        responses = data.get("target_responses", [])
        findings = data.get("security_findings", [])

        # Build response lookup by attack_id
        response_map = {r.get("attack_id"): r for r in responses}

        # Build findings lookup by attack_id
        findings_map = {}
        for f in findings:
            attack_id = f.get("attack_id")
            if attack_id:
                if attack_id not in findings_map:
                    findings_map[attack_id] = []
                findings_map[attack_id].append(f)

        # Build chain
        chain = []
        for i, attack in enumerate(attacks):
            attack_id = attack.get("attack_id")
            response = response_map.get(attack_id, {})
            attack_findings = findings_map.get(attack_id, [])

            # Determine outcome
            if attack_findings:
                severities = [f.get("severity") for f in attack_findings]
                if "critical" in severities:
                    outcome = "critical"
                elif "high" in severities:
                    outcome = "high"
                elif "medium" in severities:
                    outcome = "medium"
                else:
                    outcome = "low"
            else:
                # Check if response indicates refusal
                content = response.get("content", "").lower()
                refusal_markers = ["cannot", "sorry", "i can't", "unable to", "policy", "not able"]
                if any(m in content for m in refusal_markers):
                    outcome = "blocked"
                else:
                    outcome = "neutral"

            chain.append(
                {
                    "step": i + 1,
                    "attack_id": attack_id,
                    "agent": attack.get("agent_name", "unknown"),
                    "attack_type": attack.get("attack_type", "unknown"),
                    "pattern": attack.get(
                        "pattern", attack.get("metadata", {}).get("pattern", "unknown")
                    ),
                    "query": attack.get("query", ""),
                    "timestamp": attack.get("timestamp"),
                    "response": response.get("content", "No response recorded"),
                    "response_timestamp": response.get("timestamp"),
                    "findings": attack_findings,
                    "finding_count": len(attack_findings),
                    "outcome": outcome,
                    "metadata": attack.get("metadata", {}),
                }
            )

        return {
            "session_id": session_id,
            "target_name": data.get("target_name", "Unknown"),
            "started_at": data.get("started_at"),
            "completed_at": data.get("completed_at"),
            "total_steps": len(chain),
            "total_findings": len(findings),
            "chain": chain,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error building attack chain: {str(e)}")


@router.get("/sessions/{session_id}/step/{step_num}")
async def get_chain_step(session_id: str, step_num: int):
    """
    Get a single step in the attack chain for replay.

    Useful for stepping through attacks one at a time.
    """
    chain_data = await get_attack_chain(session_id)
    chain = chain_data.get("chain", [])

    if step_num < 1 or step_num > len(chain):
        raise HTTPException(
            status_code=404, detail=f"Step {step_num} not found. Valid range: 1-{len(chain)}"
        )

    step = chain[step_num - 1]
    step["total_steps"] = len(chain)
    step["has_prev"] = step_num > 1
    step["has_next"] = step_num < len(chain)

    return step
