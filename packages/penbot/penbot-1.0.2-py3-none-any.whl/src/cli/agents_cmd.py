"""
Agent management commands for listing and describing available security agents.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

# Agent registry with metadata
# This is the single source of truth for agent information in the CLI
# Pattern counts updated to reflect actual loaded patterns from attack library
AGENT_REGISTRY = {
    "jailbreak": {
        "class": "JailbreakAgent",
        "module": "src.agents.jailbreak",
        "description": "Prompt injection and jailbreak attempts (DAN, system override, etc.)",
        "owasp": "LLM01: Prompt Injection",
        "patterns": "694 patterns",  # 560 basic + 41 libertas + 25 ultra + 23 advanced + 16 research + 8 specialized + 21 latest
        "priority": "High",
        "category": "Prompt Engineering",
    },
    "encoding": {
        "class": "EncodingAgent",
        "module": "src.agents.encoding",
        "description": "Encoding-based attacks (leet speak, Base64, ROT13, Unicode tricks)",
        "owasp": "LLM01: Prompt Injection",
        "patterns": "154 encoding methods",  # From encoding_methods.json
        "priority": "Medium",
        "category": "Prompt Engineering",
    },
    "info_disclosure": {
        "class": "InfoDisclosureAgent",
        "module": "src.agents.info_disclosure",
        "description": "Tests for PII extraction, credential harvesting, metadata leakage",
        "owasp": "LLM06: Sensitive Info Disclosure",
        "patterns": "10+ patterns",
        "priority": "High",
        "category": "Data Security",
    },
    "output_security": {
        "class": "OutputSecurityAgent",
        "module": "src.agents.output_security",
        "description": "Tests for XSS, SQL injection, command injection in outputs",
        "owasp": "LLM02: Insecure Output Handling",
        "patterns": "10+ patterns",
        "priority": "High",
        "category": "Output Security",
    },
    "impersonation": {
        "class": "ImpersonationAgent",
        "module": "src.agents.impersonation",
        "description": "Social engineering via authority figure impersonation",
        "owasp": "LLM01: Prompt Injection",
        "patterns": "285+ patterns",  # From social_engineering.json
        "priority": "Medium",
        "category": "Social Engineering",
    },
    "compliance": {
        "class": "ComplianceAgent",
        "module": "src.agents.compliance",
        "description": "Industry-specific compliance testing (HIPAA, PCI-DSS, GDPR)",
        "owasp": "Multiple (LLM06, LLM02)",
        "patterns": "12 patterns across 8 industries",
        "priority": "Medium",
        "category": "Compliance",
    },
    "token_soup": {
        "class": "TokenSoupAgent",
        "module": "src.agents.token_soup",
        "description": "Machine-only dialect attacks (system logs, pseudocode, kernel traces)",
        "owasp": "LLM01: Prompt Injection",
        "patterns": "5 dialect categories (dynamic)",
        "priority": "Medium",
        "category": "Prompt Engineering",
    },
    "evolutionary": {
        "class": "EvolutionaryAgent",
        "module": "src.agents.evolutionary.agent",
        "description": "Genetic algorithm-based attack evolution (breeds from successful attacks)",
        "owasp": "Multiple",
        "patterns": "Dynamic (evolves from history)",
        "priority": "High",
        "category": "Adaptive",
    },
    # ✨ NEW: December 2025 - Specialized Agents
    "rag_poisoning": {
        "class": "RAGPoisoningAgent",
        "module": "src.agents.rag_poisoning",
        "description": "RAG document poisoning (indirect injection, chunk boundary exploitation, citation manipulation)",
        "owasp": "LLM03: Training Data Poisoning, LLM06: Sensitive Info Disclosure",
        "patterns": "20 RAG-specific patterns",
        "priority": "High",
        "category": "RAG & Retrieval",
    },
    "tool_exploit": {
        "class": "ToolExploitAgent",
        "module": "src.agents.tool_exploit",
        "description": "Tool/function exploitation (argument injection, privilege escalation, sandbox escape)",
        "owasp": "LLM07: Insecure Plugin Design, LLM08: Excessive Agency",
        "patterns": "20 tool attack patterns",
        "priority": "High",
        "category": "Agentic AI",
    },
}


def list_agents(args):
    """List all available security testing agents."""
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]PenBot Security Agents[/bold cyan]\n"
            "[dim]Multi-agent adversarial testing framework[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    # Group by category
    categories = {}
    for agent_id, info in AGENT_REGISTRY.items():
        cat = info["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((agent_id, info))

    for category, agents in categories.items():
        table = Table(
            title=f"[bold]{category}[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold green",
        )

        table.add_column("Agent ID", style="cyan", width=18)
        table.add_column("Description", width=50)
        table.add_column("OWASP", style="yellow", width=25)
        table.add_column("Patterns", style="dim", width=15)

        for agent_id, info in agents:
            table.add_row(agent_id, info["description"], info["owasp"], info["patterns"])

        console.print(table)
        console.print()

    console.print(f"[dim]Total: {len(AGENT_REGISTRY)} agents available[/dim]")
    console.print()
    console.print(
        "[dim]Use with: penbot test --config <file> --agents jailbreak,encoding,rag_poisoning[/dim]"
    )
    console.print("[dim italic]New in Dec 2025: rag_poisoning, tool_exploit[/dim italic]")
    console.print()


def describe_agent(args):
    """Show detailed information about a specific agent."""
    import logging
    import sys
    from io import StringIO

    agent_id = args.agent_id.lower()

    if agent_id not in AGENT_REGISTRY:
        console.print(f"❌ Unknown agent: {agent_id}")
        console.print(f"[dim]Available agents: {', '.join(AGENT_REGISTRY.keys())}[/dim]")
        return

    info = AGENT_REGISTRY[agent_id]

    # Try to get actual pattern count (suppress all output during load)
    actual_pattern_count = None
    try:
        # Suppress stdout/stderr during agent initialization to hide structlog output
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

        # Also suppress root logger
        old_level = logging.root.level
        logging.root.setLevel(logging.CRITICAL)

        try:
            if agent_id == "jailbreak":
                from src.agents.jailbreak import JailbreakAgent

                agent = JailbreakAgent(llm_client=None, config={})
                patterns = agent.get_attack_patterns()
                actual_pattern_count = len(patterns)
            elif agent_id == "encoding":
                from src.agents.encoding import EncodingAgent

                agent = EncodingAgent(llm_client=None, config={})
                patterns = agent.get_attack_patterns()
                actual_pattern_count = len(patterns)
            elif agent_id == "impersonation":
                from src.agents.impersonation import ImpersonationAgent

                agent = ImpersonationAgent(llm_client=None, config={})
                patterns = agent.get_attack_patterns()
                actual_pattern_count = len(patterns)
            elif agent_id == "rag_poisoning":
                from src.agents.rag_poisoning import RAGPoisoningAgent

                agent = RAGPoisoningAgent(llm_client=None, config={})
                patterns = agent.get_attack_patterns()
                actual_pattern_count = len(patterns)
            elif agent_id == "tool_exploit":
                from src.agents.tool_exploit import ToolExploitAgent

                agent = ToolExploitAgent(llm_client=None, config={})
                patterns = agent.get_attack_patterns()
                actual_pattern_count = len(patterns)
        finally:
            # Restore stdout/stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            logging.root.setLevel(old_level)

    except Exception:
        pass  # Silent fail if can't load patterns

    # Use actual count if available, otherwise use registry value
    patterns_display = (
        f"{actual_pattern_count} patterns" if actual_pattern_count else info["patterns"]
    )

    console.print()
    console.print(
        Panel(
            f"[bold cyan]Agent ID:[/bold cyan] {agent_id}\n"
            f"[bold cyan]Class:[/bold cyan] {info['class']}\n"
            f"[bold cyan]Module:[/bold cyan] {info['module']}\n"
            f"[bold cyan]Category:[/bold cyan] {info['category']}\n"
            f"[bold cyan]Priority:[/bold cyan] {info['priority']}\n\n"
            f"[bold]Description:[/bold]\n{info['description']}\n\n"
            f"[bold]OWASP Coverage:[/bold] {info['owasp']}\n"
            f"[bold]Attack Patterns:[/bold] {patterns_display}",
            title=f"🤖 {info['class']}",
            border_style="cyan",
        )
    )
    console.print()


def get_agent_ids() -> list:
    """Return list of valid agent IDs for validation."""
    return list(AGENT_REGISTRY.keys())


def validate_agent_list(agents_str: str) -> tuple:
    """
    Validate a comma-separated list of agent IDs.

    Returns:
        Tuple of (valid_agents, invalid_agents)
    """
    if not agents_str:
        return [], []

    requested = [a.strip().lower() for a in agents_str.split(",")]
    valid = [a for a in requested if a in AGENT_REGISTRY]
    invalid = [a for a in requested if a not in AGENT_REGISTRY]

    return valid, invalid
