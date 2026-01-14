"""
PenBot Professional Console Dashboard
Powered by Rich
"""

from datetime import datetime
from typing import Dict, List, Any

from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.console import Console
from rich.text import Text
from rich.columns import Columns
from rich.console import Group
from rich import box


class PenBotDashboard:
    def __init__(self):
        self.console = Console()
        self.layout = Layout()

        # State
        self.start_time = datetime.now()
        self.current_round = 0
        self.max_rounds = 0
        self.phase = "INITIALIZING"
        self.target_name = "Unknown"

        self.agents: Dict[str, Dict[str, Any]] = {}
        self.findings = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        self.logs: List[Text] = []
        self.max_logs = 50  # Keep last 50 logs in view

        # Initialize layout
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3),
        )

        self.layout["main"].split_row(Layout(name="left", ratio=2), Layout(name="right", ratio=1))

        self.layout["right"].split(
            Layout(name="intelligence", size=10),
            Layout(name="agents", ratio=1),
            Layout(name="findings", size=10),
        )

    def start(self):
        """Start the live dashboard context."""
        return Live(self.layout, refresh_per_second=4, screen=True)

    def render_header(self) -> Panel:
        """Render the top header."""
        elapsed = datetime.now() - self.start_time
        grid = Table.grid(expand=True)
        grid.add_column(justify="left", ratio=1)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right", ratio=1)

        grid.add_row(
            "🤖 [bold cyan]PenBot v2.0[/] [dim]Professional Console[/]",
            f"🎯 Target: [bold yellow]{self.target_name}[/]",
            f"⏱️ Runtime: [bold]{str(elapsed).split('.')[0]}[/]",
        )
        return Panel(grid, style="white on blue")

    def render_logs(self) -> Panel:
        """Render the scrolling log panel."""
        return Panel(
            Group(*self.logs[-self.max_logs :]),
            title="📜 [bold]Live Operation Log[/]",
            border_style="cyan",
            padding=(0, 1),
        )

    def render_intelligence(self) -> Panel:
        """Render campaign intelligence metrics."""
        table = Table(box=None, expand=True)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", justify="right", style="bold white")

        table.add_row("Phase", f"[magenta]{self.phase}[/]")
        table.add_row("Round", f"{self.current_round}/{self.max_rounds}")

        # Calculate success rate if data available
        total_vulns = sum(self.findings.values())
        rate = f"{(total_vulns/self.current_round)*100:.1f}%" if self.current_round > 0 else "0%"
        table.add_row("Hit Rate", rate)

        return Panel(table, title="🧠 [bold]Campaign Intel[/]", border_style="magenta")

    def render_agents(self) -> Panel:
        """Render active agent status."""
        table = Table(box=box.SIMPLE_HEAD, expand=True)
        table.add_column("Agent", style="cyan")
        table.add_column("Conf", justify="right", width=6)
        table.add_column("Status", justify="center", width=10)

        for name, data in self.agents.items():
            # Shorten name
            short_name = name.replace("_agent", "").replace("Agent", "").title()

            conf = f"{data.get('confidence', 0.0):.2f}"

            status = data.get("status", "Idle")
            status_style = "dim"
            if status == "Thinking":
                status_style = "bold yellow"
            if status == "Voting":
                status_style = "bold blue"
            if status == "WINNER":
                status_style = "bold green"

            table.add_row(short_name, conf, f"[{status_style}]{status}[/]")

        return Panel(table, title="🕵️ [bold]Active Agents[/]", border_style="blue")

    def render_findings(self) -> Panel:
        """Render findings summary."""
        grid = Columns(expand=True)

        def make_stat(label, count, color):
            return Panel(
                f"[bold {color}]{count}[/]",
                title=f"[{color}]{label}[/]",
                border_style=color,
                height=5,
            )

        return Panel(
            Columns(
                [
                    make_stat("CRIT", self.findings["CRITICAL"], "red"),
                    make_stat("HIGH", self.findings["HIGH"], "orange1"),
                    make_stat("MED", self.findings["MEDIUM"], "yellow"),
                    make_stat("LOW", self.findings["LOW"], "blue"),
                ]
            ),
            title="🛡️ [bold]Findings[/]",
            border_style="green",
        )

    def render_footer(self) -> Panel:
        """Render the footer."""
        return Panel(
            Text("Press Ctrl+C to stop • Logs saved to test_logs/", justify="center", style="dim"),
            style="white on black",
        )

    def update(self):
        """Update the layout with new data."""
        self.layout["header"].update(self.render_header())
        self.layout["left"].update(self.render_logs())
        self.layout["intelligence"].update(self.render_intelligence())
        self.layout["agents"].update(self.render_agents())
        self.layout["findings"].update(self.render_findings())
        self.layout["footer"].update(self.render_footer())

    # --- Public API ---

    def init_campaign(self, target_name: str, max_rounds: int):
        self.target_name = target_name
        self.max_rounds = max_rounds
        self.update()

    def set_phase(self, phase: str):
        self.phase = phase
        self.log(f"🔄 Campaign Phase Switched: [bold magenta]{phase}[/]")
        self.update()

    def set_round(self, round_num: int):
        self.current_round = round_num
        self.update()

    def update_agent(self, name: str, status: str, confidence: float = 0.0):
        if name not in self.agents:
            self.agents[name] = {}
        self.agents[name]["status"] = status
        if confidence > 0:
            self.agents[name]["confidence"] = confidence
        self.update()

    def add_finding(self, severity: str):
        sev = severity.upper()
        if sev in self.findings:
            self.findings[sev] += 1
            self.log(f"🚨 [bold red]NEW FINDING DETECTED: {sev}[/]")
        self.update()

    def log(self, message: str, level: str = "INFO"):
        """Add a log message to the scrolling panel."""
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Style based on level/content
        style = "white"
        if "ERROR" in level or "Error" in message:
            style = "red"
        elif "WARNING" in level:
            style = "yellow"
        elif "SUCCESS" in message or "WINNER" in message:
            style = "green"
        elif "Attack Sent" in message:
            style = "cyan"
        elif "Response" in message:
            style = "dim"

        # Check for specific keywords to highlight
        formatted_msg = message
        if "🏆 WINNER" in message:
            formatted_msg = f"[bold green]{message}[/]"
        elif "Attack Lineage" in message:
            formatted_msg = f"[bold blue]{message}[/]"

        text = Text.from_markup(f"[{timestamp}] {formatted_msg}", style=style)
        self.logs.append(text)
        self.update()


# Global instance for easy import
dashboard = PenBotDashboard()
