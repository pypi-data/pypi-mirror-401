"""State management for penetration testing workflow."""

from typing import TypedDict, Annotated, List, Literal, Optional
import operator
from datetime import datetime, timezone
from src.utils.helpers import generate_uuid


class AttackAttempt(TypedDict):
    """Single attack attempt record."""

    attack_id: str
    agent_name: str
    attack_type: Literal["social_engineering", "prompt_injection", "encoding", "jailbreak"]
    query: str
    timestamp: datetime
    parent_attack_id: Optional[str]  # For tracking attack chains
    metadata: dict  # Additional attack-specific metadata

    # Image attack support (NEW)
    image_data: Optional[str]  # Base64-encoded image
    image_mime_type: Optional[str]  # "image/png", "image/jpeg"
    image_attack_type: Optional[str]  # "text_in_image_bypass", "visual_social_engineering", etc.
    image_metadata: Optional[dict]  # Image generation details


class TargetResponse(TypedDict):
    """Response from target chatbot."""

    response_id: str
    attack_id: str
    content: str
    timestamp: datetime
    metadata: dict  # Response time, tokens, screenshots, etc.


class SecurityFinding(TypedDict):
    """Security vulnerability discovered."""

    finding_id: str
    severity: Literal["critical", "high", "medium", "low", "info"]
    category: Literal[
        # LLM01: Prompt Injection
        "policy_violation",
        "jailbreak_success",
        "instruction_override",
        # LLM07: System Prompt Leakage
        "system_prompt_disclosure",
        "trigger_word_disclosure",
        "decision_framework_disclosure",
        "scope_definition_disclosure",
        "system_command_acceptance",
        # LLM02: Sensitive Information Disclosure
        "data_leakage",
        "pii_exposure",
        # LLM04: Data and Model Poisoning
        "backdoor_trigger_activation",
        "behavior_inconsistency",
        "hidden_instruction_following",
        "output_bias_poisoning",
        # LLM05: Improper Output Handling
        "unsafe_content",
        # LLM06: Excessive Agency (NEW)
        "excessive_agency",
        "unauthorized_function_call",
        "authorization_bypass",
        "dangerous_action_acceptance",
        "function_disclosure",
        # LLM07: System Prompt Leakage
        "system_prompt_leak",
        # LLM08: Vector and Embedding Weaknesses (NEW)
        "vector_cross_tenant_leak",
        "vector_injection_success",
        "embedding_inversion",
        "unauthorized_vector_access",
        "rag_poisoning_indicator",
        # LLM09: Misinformation
        "misinformation",
        "hallucination",
        # LLM10: Unbounded Consumption (NEW)
        "missing_rate_limits",
        "excessive_input_acceptance",
        "large_input_acceptance",
        "model_extraction_risk",
        "context_window_overflow",
        # Structured Content Disclosures (NEW)
        "categorization_framework_disclosure",
        "json_structure_disclosure",
        "operational_procedure_disclosure",
        "architecture_table_disclosure",
        "code_implementation_disclosure",
        "configuration_disclosure",
        # General
        "rate_limiting",
        "invalid_response",
    ]
    description: str
    attack_id: str
    evidence: str
    confidence: float  # 0-1


class PenTestState(TypedDict):
    """State for penetration testing workflow."""

    # Target configuration
    target_id: str
    target_name: str
    target_type: Literal["api", "web_ui"]
    target_config: dict  # API endpoint/URL and credentials

    # Test configuration
    test_session_id: str
    attack_group: Literal["social_engineering", "prompt_engineering"]
    max_attempts: int
    current_attempt: int

    # Attack history (reducers for accumulation)
    attack_attempts: Annotated[List[AttackAttempt], operator.add]
    target_responses: Annotated[List[TargetResponse], operator.add]
    security_findings: Annotated[List[SecurityFinding], operator.add]

    # Current context
    conversation_history: List[dict]  # For maintaining context with target
    last_response: str
    agent_consultation: dict  # Agent discussion/voting results

    # Canned response detection & pivot strategy
    canned_detector: Optional[object]  # CannedResponseDetector instance
    pivot_required: bool  # Flag to trigger pivot strategy
    avoid_keywords: List[str]  # Keywords to avoid in next attacks
    last_canned_hash: Optional[str]  # Hash of last canned response

    # Target fingerprinting
    target_fingerprinter: Optional[object]  # TargetFingerprinter instance
    target_profile: Optional[dict]  # Detected target characteristics

    # Attack memory & learning (Feature 2)
    attack_memory: Optional[object]  # AttackMemoryStore instance for cross-agent knowledge sharing

    # Attack graph (multi-turn planning)
    attack_graph: Optional[object]  # AttackGraph instance for strategic path planning
    attack_graph_enabled: bool  # Whether to use graph-based attack planning
    current_graph_node_id: Optional[str]  # Current position in attack graph

    # Campaign planning
    campaign_phase: str  # Current phase: reconnaissance, trust_building, etc.
    campaign_phase_attempts: int  # Attempts in current phase
    campaign_phase_successes: int  # Successes in current phase
    campaign_history: List[dict]  # History of completed phases

    # Test results
    vulnerability_score: float  # 0-100, calculated from findings
    test_status: Literal["running", "completed", "failed", "stopped"]

    # Metadata
    started_at: datetime
    completed_at: Optional[datetime]
    error: Optional[str]


def create_initial_state(
    target_name: str,
    target_type: Literal["api", "web_ui"],
    target_config: dict,
    attack_group: Literal["social_engineering", "prompt_engineering"],
    max_attempts: int = 10,
) -> PenTestState:
    """
    Create initial state for a penetration test.

    Args:
        target_name: Human-readable name for target
        target_type: Type of target (api or web_ui)
        target_config: Configuration for connecting to target
        attack_group: Which group of attacks to use
        max_attempts: Maximum number of attack attempts

    Returns:
        Initial PenTestState

    Example:
        >>> state = create_initial_state(
        ...     target_name="My Chatbot",
        ...     target_type="api",
        ...     target_config={"endpoint": "http://localhost:5000/chat"},
        ...     attack_group="prompt_engineering",
        ...     max_attempts=5
        ... )
    """
    return PenTestState(
        # Target configuration
        target_id=generate_uuid(),
        target_name=target_name,
        target_type=target_type,
        target_config=target_config,
        # Test configuration
        test_session_id=generate_uuid(),
        attack_group=attack_group,
        max_attempts=max_attempts,
        current_attempt=0,
        # Initialize empty history
        attack_attempts=[],
        target_responses=[],
        security_findings=[],
        # Initialize empty context
        conversation_history=[],
        last_response="",
        agent_consultation={},
        # Initialize canned response detection
        canned_detector=None,
        pivot_required=False,
        avoid_keywords=[],
        last_canned_hash=None,
        # Initialize target fingerprinting
        target_fingerprinter=None,
        target_profile=None,
        # Initialize attack memory
        attack_memory=None,  # Will be initialized on first use
        # Initialize attack graph
        attack_graph=None,  # Will be initialized if graph-based planning is enabled
        attack_graph_enabled=False,  # Disabled by default, enable via config
        current_graph_node_id=None,
        # Initialize campaign planning
        campaign_phase="reconnaissance",
        campaign_phase_attempts=0,
        campaign_phase_successes=0,
        campaign_history=[],
        # Initialize results
        vulnerability_score=0.0,
        test_status="running",
        # Set timestamps
        started_at=datetime.now(timezone.utc),
        completed_at=None,
        error=None,
    )


def get_last_attack(state: PenTestState) -> Optional[AttackAttempt]:
    """Get the most recent attack attempt."""
    if state["attack_attempts"]:
        return state["attack_attempts"][-1]
    return None


def get_last_response(state: PenTestState) -> Optional[TargetResponse]:
    """Get the most recent target response."""
    if state["target_responses"]:
        return state["target_responses"][-1]
    return None


def count_findings_by_severity(state: PenTestState, severity: str) -> int:
    """Count findings of a specific severity level."""
    return len([f for f in state["security_findings"] if f["severity"] == severity])
