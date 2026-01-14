"""
Test runner for executing security tests via CLI.
"""

import asyncio
import sys
from pathlib import Path

# Add root directory to path to import test_orchestrated
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from src.cli.config_loader import load_config
from src.connectors.rest_connector import GenericRestConnector
from src.connectors.playwright_connector import PlaywrightConnector

console = Console()


async def run_test(args):
    """
    Execute full orchestrated test using configuration.

    Enhanced with:
    - --agents: Select specific agents
    - --dry-run: Preview without executing
    - --output: Specify report output
    - --phase: Start at specific phase
    - --verbose: Detailed output
    """
    verbose = getattr(args, "verbose", False)

    # ═══════════════════════════════════════════════════════════════════════════
    # Load Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]PenBot Security Testing Framework[/bold cyan]\n"
            "[dim]Multi-agent adversarial testing for AI chatbots[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    console.print(f"📂 Loading config: [cyan]{args.config}[/cyan]")

    try:
        config = load_config(args.config)
    except FileNotFoundError:
        console.print(f"[red]❌ Config file not found: {args.config}[/red]")
        return
    except Exception as e:
        console.print(f"[red]❌ Failed to load config: {e}[/red]")
        return

    target_name = config["target"]["name"]
    console.print(f"✅ Target: [green]{target_name}[/green]")

    # ═══════════════════════════════════════════════════════════════════════════
    # Agent Selection
    # ═══════════════════════════════════════════════════════════════════════════
    if args.agents:
        from src.cli.agents_cmd import validate_agent_list

        valid_agents, invalid_agents = validate_agent_list(args.agents)

        if invalid_agents:
            console.print(f"[yellow]⚠️  Unknown agents: {', '.join(invalid_agents)}[/yellow]")

        if not valid_agents:
            console.print("[red]❌ No valid agents specified[/red]")
            console.print("[dim]Use 'penbot agents' to see available agents[/dim]")
            return

        # Override config with selected agents
        config["test"]["agents"] = valid_agents
        console.print(f"🤖 Agents: [cyan]{', '.join(valid_agents)}[/cyan]")
    else:
        agents_in_config = config["test"].get("agents", [])
        console.print(
            f"🤖 Agents: [cyan]{', '.join(agents_in_config) if agents_in_config else 'All available'}[/cyan]"
        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Determine Attack Count
    # ═══════════════════════════════════════════════════════════════════════════
    max_attacks = args.max_attacks
    if not max_attacks:
        max_attacks = config["test"].get("max_attacks", 30)

    if args.quick:
        max_attacks = 3
        console.print(f"⚡ Quick mode: [yellow]{max_attacks} attacks[/yellow]")
    else:
        console.print(f"🎯 Max Attacks: [cyan]{max_attacks}[/cyan]")

    # ═══════════════════════════════════════════════════════════════════════════
    # Campaign Phase
    # ═══════════════════════════════════════════════════════════════════════════
    start_phase = getattr(args, "phase", None)
    if start_phase:
        console.print(f"📍 Starting Phase: [cyan]{start_phase}[/cyan]")

    # ═══════════════════════════════════════════════════════════════════════════
    # Output Configuration
    # ═══════════════════════════════════════════════════════════════════════════
    output_dir = Path(args.output) if getattr(args, "output", None) else Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(f"📄 Reports: [cyan]{output_dir}[/cyan]")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════════
    # Dry Run Mode
    # ═══════════════════════════════════════════════════════════════════════════
    if getattr(args, "dry_run", False):
        await _dry_run(config, max_attacks)
        return

    # ═══════════════════════════════════════════════════════════════════════════
    # Initialize Connector
    # ═══════════════════════════════════════════════════════════════════════════
    conn_type = config["target"]["connection"].get("type", "rest")

    if conn_type == "playwright":
        console.print("🌐 Using Playwright browser automation")
        connector = PlaywrightConnector(config["target"])
    elif config["target"]["platform"] == "custom-rest" or conn_type == "rest":
        console.print("🔌 Using REST API connector")
        connector = GenericRestConnector(config["target"])
    else:
        console.print(
            f"[yellow]⚠️  Platform '{config['target']['platform']}' not yet supported.[/yellow]"
        )
        console.print("   Falling back to GenericRestConnector...")
        connector = GenericRestConnector(config["target"])

    # Initialize connector
    with console.status("[bold green]Initializing connector...") as status:
        await connector.initialize()

    console.print("✅ Connector initialized")
    console.print()

    # ═══════════════════════════════════════════════════════════════════════════
    # Test Configuration Summary
    # ═══════════════════════════════════════════════════════════════════════════
    summary_table = Table(box=box.ROUNDED, show_header=False, title="📋 Test Configuration")
    summary_table.add_column("Setting", style="bold")
    summary_table.add_column("Value", style="cyan")

    summary_table.add_row("Target", target_name)
    summary_table.add_row("Platform", config["target"].get("platform", "unknown"))
    summary_table.add_row("Max Attacks", str(max_attacks))
    summary_table.add_row("Agents", str(len(config["test"].get("agents", []))) + " active")
    if start_phase:
        summary_table.add_row("Start Phase", start_phase)

    console.print(summary_table)
    console.print()

    # ═══════════════════════════════════════════════════════════════════════════
    # Execute Campaign
    # ═══════════════════════════════════════════════════════════════════════════

    # Import the actual orchestration function
    from test_orchestrated import run_orchestrated_test

    console.print("🚀 [bold green]Starting orchestrated campaign...[/bold green]")
    console.print()

    try:
        await run_orchestrated_test(
            target_config=config["target"], connector=connector, max_attacks=max_attacks
        )
        console.print()
        console.print("[bold green]✅ Campaign completed successfully.[/bold green]")

    except (KeyboardInterrupt, asyncio.CancelledError):
        console.print()
        console.print("[yellow]⚠️  Campaign interrupted by user.[/yellow]")
    except Exception as e:
        console.print()
        console.print(f"[red]❌ Campaign failed: {e}[/red]")
        if verbose:
            import traceback

            traceback.print_exc()
    finally:
        await connector.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # Post-Test Summary
    # ═══════════════════════════════════════════════════════════════════════════
    console.print()
    console.print("[dim]Use 'penbot sessions' to view past sessions[/dim]")
    console.print("[dim]Use 'penbot report --latest' to generate a report[/dim]")


async def _dry_run(config: dict, max_attacks: int):
    """
    Preview what would be tested without actually executing.

    Shows:
    - Target configuration
    - Active agents
    - Sample attack patterns
    """
    console.print()
    console.print(
        Panel.fit(
            "[bold yellow]🔍 DRY RUN MODE[/bold yellow]\n"
            "[dim]Preview only - no attacks will be executed[/dim]",
            border_style="yellow",
        )
    )
    console.print()

    # Show target info
    target = config["target"]
    console.print("[bold]Target Configuration:[/bold]")
    console.print(f"  • Name: {target.get('name', 'Unknown')}")
    console.print(f"  • Platform: {target.get('platform', 'Unknown')}")
    console.print(f"  • Endpoint: {target.get('connection', {}).get('endpoint', 'Unknown')}")
    console.print()

    # Show agents
    agents = config["test"].get("agents", [])
    console.print("[bold]Active Agents:[/bold]")

    if agents:
        from src.cli.agents_cmd import AGENT_REGISTRY

        for agent_id in agents:
            if agent_id in AGENT_REGISTRY:
                info = AGENT_REGISTRY[agent_id]
                console.print(f"  • [cyan]{agent_id}[/cyan] - {info['description'][:50]}...")
            else:
                console.print(f"  • [cyan]{agent_id}[/cyan]")
    else:
        console.print("  [dim]All available agents will be used[/dim]")

    console.print()

    # Show sample patterns
    console.print("[bold]Sample Attack Patterns:[/bold]")
    console.print()

    try:
        from src.agents.jailbreak import JailbreakAgent

        agent = JailbreakAgent(llm_client=None, config={})
        patterns = agent.get_attack_patterns()[:5]  # First 5

        for i, pattern in enumerate(patterns, 1):
            name = pattern.get("name", "unknown")
            desc = pattern.get("description", "No description")[:60]
            severity = pattern.get("severity_if_success", "unknown")
            console.print(f"  {i}. [cyan]{name}[/cyan]")
            console.print(f"     {desc}")
            console.print(f"     Severity: {severity}")
            console.print()

    except Exception as e:
        console.print(f"  [dim]Could not load patterns: {e}[/dim]")

    # Estimated duration
    avg_time_per_attack = 5  # seconds
    total_time = max_attacks * avg_time_per_attack
    minutes = total_time // 60
    seconds = total_time % 60

    console.print()
    console.print(
        f"[bold]Estimated Duration:[/bold] ~{minutes}m {seconds}s for {max_attacks} attacks"
    )
    console.print()
    console.print("[dim]To execute, run without --dry-run flag[/dim]")
