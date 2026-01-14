"""
Session management commands for viewing and managing test sessions.
"""

import json
from pathlib import Path
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

SESSIONS_DIR = Path("sessions")


def list_sessions(args):
    """List all available sessions."""
    if not SESSIONS_DIR.exists():
        console.print("❌ No sessions directory found. Run a test first.")
        return

    files = list(SESSIONS_DIR.glob("*.json"))
    if not files:
        console.print("❌ No session files found.")
        return

    # Sort by modification time (most recent first)
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

    # Build table
    table = Table(
        title="📋 PenBot Test Sessions", box=box.ROUNDED, header_style="bold cyan", show_lines=True
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Session ID", style="green", width=38)
    table.add_column("Target", style="yellow", width=25)
    table.add_column("Attacks", justify="right", width=8)
    table.add_column("Findings", justify="right", width=8)
    table.add_column("Status", width=10)
    table.add_column("Date", width=18)

    for i, file in enumerate(files, 1):
        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

            session_id = file.stem
            target_name = data.get("target_name", "Unknown")[:24]
            attacks = len(data.get("attack_attempts", []))
            findings = len(data.get("security_findings", []))
            status = data.get("test_status", "unknown")

            # Parse date
            started_at = data.get("started_at", "")
            if started_at:
                try:
                    dt = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
                    date_str = dt.strftime("%Y-%m-%d %H:%M")
                except Exception:
                    date_str = started_at[:16]
            else:
                date_str = "Unknown"

            # Color status
            if status == "completed":
                status_display = "[green]✅ Done[/green]"
            elif status == "stopped":
                status_display = "[yellow]⚠️ Stopped[/yellow]"
            elif status == "running":
                status_display = "[blue]🔄 Running[/blue]"
            else:
                status_display = f"[dim]{status}[/dim]"

            # Color findings by severity
            if findings > 0:
                findings_display = f"[red bold]{findings}[/red bold]"
            else:
                findings_display = f"[dim]{findings}[/dim]"

            table.add_row(
                str(i),
                session_id[:36] + "..." if len(session_id) > 36 else session_id,
                target_name,
                str(attacks),
                findings_display,
                status_display,
                date_str,
            )

        except Exception:
            table.add_row(
                str(i),
                file.stem[:36],
                "[red]Error loading[/red]",
                "-",
                "-",
                "[red]Error[/red]",
                "-",
            )

    console.print()
    console.print(table)
    console.print()
    console.print(
        f"[dim]Total: {len(files)} session(s) | Use 'penbot sessions view <id>' to see details[/dim]"
    )
    console.print()


def view_session(args):
    """View detailed session information."""
    session_id = args.session_id

    # Handle index-based lookup (e.g., "1" for most recent)
    if session_id.isdigit():
        files = sorted(SESSIONS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        idx = int(session_id) - 1
        if 0 <= idx < len(files):
            session_id = files[idx].stem
        else:
            console.print(
                f"❌ Session #{session_id} not found. Use 'penbot sessions' to list available sessions."
            )
            return

    file_path = SESSIONS_DIR / f"{session_id}.json"

    if not file_path.exists():
        console.print(f"❌ Session not found: {session_id}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"❌ Failed to load session: {e}")
        return

    # Build detailed view
    console.print()
    console.print(
        Panel(
            f"[bold cyan]Session:[/bold cyan] {session_id}\n"
            f"[bold cyan]Target:[/bold cyan] {data.get('target_name', 'Unknown')}\n"
            f"[bold cyan]Status:[/bold cyan] {data.get('test_status', 'unknown')}\n"
            f"[bold cyan]Started:[/bold cyan] {data.get('started_at', 'Unknown')}\n"
            f"[bold cyan]Completed:[/bold cyan] {data.get('completed_at', 'N/A')}",
            title="📊 Session Overview",
            border_style="cyan",
        )
    )

    # Summary stats
    attacks = data.get("attack_attempts", [])
    findings = data.get("security_findings", [])

    stats_table = Table(box=box.SIMPLE)
    stats_table.add_column("Metric", style="bold")
    stats_table.add_column("Value", justify="right")

    stats_table.add_row("Total Attacks", str(len(attacks)))
    stats_table.add_row("Total Findings", str(len(findings)))
    stats_table.add_row("Campaign Phase", data.get("campaign_phase", "N/A"))
    stats_table.add_row("Attack Group", data.get("attack_group", "N/A"))

    # Count findings by severity
    critical = len([f for f in findings if f.get("severity") == "critical"])
    high = len([f for f in findings if f.get("severity") == "high"])
    medium = len([f for f in findings if f.get("severity") == "medium"])
    low = len([f for f in findings if f.get("severity") == "low"])

    if critical:
        stats_table.add_row("🚨 Critical", f"[red bold]{critical}[/red bold]")
    if high:
        stats_table.add_row("⚠️  High", f"[orange1 bold]{high}[/orange1 bold]")
    if medium:
        stats_table.add_row("📋 Medium", f"[yellow]{medium}[/yellow]")
    if low:
        stats_table.add_row("ℹ️  Low", f"[dim]{low}[/dim]")

    console.print(stats_table)
    console.print()

    # Show findings if any
    if findings:
        console.print("[bold]🔍 Security Findings:[/bold]")
        console.print()

        for i, finding in enumerate(findings, 1):
            severity = finding.get("severity", "unknown").upper()
            if severity == "CRITICAL":
                sev_style = "[red bold]🚨 CRITICAL[/red bold]"
            elif severity == "HIGH":
                sev_style = "[orange1 bold]⚠️  HIGH[/orange1 bold]"
            elif severity == "MEDIUM":
                sev_style = "[yellow]📋 MEDIUM[/yellow]"
            else:
                sev_style = f"[dim]ℹ️  {severity}[/dim]"

            console.print(f"  {i}. {sev_style} | [cyan]{finding.get('category', 'unknown')}[/cyan]")
            console.print(f"     {finding.get('description', 'No description')[:100]}")
            console.print()
    else:
        console.print("[green]✅ No vulnerabilities found in this session.[/green]")

    console.print()
    console.print(
        f"[dim]Use 'penbot report --session {session_id}' to generate a full report[/dim]"
    )
    console.print()


def delete_session(args):
    """Delete a session file."""
    session_id = args.session_id

    # Handle index-based lookup
    if session_id.isdigit():
        files = sorted(SESSIONS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        idx = int(session_id) - 1
        if 0 <= idx < len(files):
            session_id = files[idx].stem
        else:
            console.print(f"❌ Session #{session_id} not found.")
            return

    file_path = SESSIONS_DIR / f"{session_id}.json"

    if not file_path.exists():
        console.print(f"❌ Session not found: {session_id}")
        return

    if not args.force:
        # Confirm deletion
        from rich.prompt import Confirm

        if not Confirm.ask(f"Delete session [cyan]{session_id}[/cyan]?"):
            console.print("Cancelled.")
            return

    try:
        file_path.unlink()
        console.print(f"✅ Session deleted: {session_id}")

        # Also try to delete corresponding report if it exists
        report_path = Path("reports") / f"report_{session_id}.html"
        if report_path.exists():
            report_path.unlink()
            console.print(f"✅ Report also deleted: {report_path.name}")

    except Exception as e:
        console.print(f"❌ Failed to delete session: {e}")


def export_session(args):
    """Export session data to different formats."""
    session_id = args.session_id
    output_format = args.format

    # Handle index-based lookup
    if session_id.isdigit():
        files = sorted(SESSIONS_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
        idx = int(session_id) - 1
        if 0 <= idx < len(files):
            session_id = files[idx].stem
        else:
            console.print(f"❌ Session #{session_id} not found.")
            return

    file_path = SESSIONS_DIR / f"{session_id}.json"

    if not file_path.exists():
        console.print(f"❌ Session not found: {session_id}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        console.print(f"❌ Failed to load session: {e}")
        return

    output_dir = Path(args.output) if args.output else Path("exports")
    output_dir.mkdir(exist_ok=True)

    if output_format == "csv":
        _export_csv(data, session_id, output_dir)
    elif output_format == "markdown":
        _export_markdown(data, session_id, output_dir)
    else:
        console.print(f"❌ Unknown format: {output_format}")


def _export_csv(data: dict, session_id: str, output_dir: Path):
    """Export findings to CSV."""
    import csv

    findings = data.get("security_findings", [])
    if not findings:
        console.print("⚠️  No findings to export.")
        return

    output_file = output_dir / f"{session_id}_findings.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Severity", "Category", "Description", "Confidence", "Evidence"])

        for finding in findings:
            writer.writerow(
                [
                    finding.get("severity", ""),
                    finding.get("category", ""),
                    finding.get("description", ""),
                    finding.get("confidence", ""),
                    finding.get("evidence", "")[:200],  # Truncate evidence
                ]
            )

    console.print(f"✅ Exported to: [green]{output_file}[/green]")


def _export_markdown(data: dict, session_id: str, output_dir: Path):
    """Export session summary to Markdown."""
    findings = data.get("security_findings", [])
    attacks = data.get("attack_attempts", [])

    output_file = output_dir / f"{session_id}_summary.md"

    lines = [
        f"# PenBot Security Assessment",
        f"",
        f"**Session ID:** `{session_id}`",
        f"**Target:** {data.get('target_name', 'Unknown')}",
        f"**Date:** {data.get('started_at', 'Unknown')[:10]}",
        f"**Status:** {data.get('test_status', 'unknown')}",
        f"",
        f"## Summary",
        f"",
        f"- **Total Attacks:** {len(attacks)}",
        f"- **Findings:** {len(findings)}",
        f"",
    ]

    if findings:
        lines.append("## Findings")
        lines.append("")

        for i, finding in enumerate(findings, 1):
            lines.append(
                f"### {i}. [{finding.get('severity', 'unknown').upper()}] {finding.get('category', 'Unknown')}"
            )
            lines.append("")
            lines.append(f"{finding.get('description', 'No description')}")
            lines.append("")
            if finding.get("evidence"):
                lines.append(f"**Evidence:** `{finding.get('evidence', '')[:150]}...`")
                lines.append("")
    else:
        lines.append("## Findings")
        lines.append("")
        lines.append("✅ No vulnerabilities detected.")

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    console.print(f"✅ Exported to: [green]{output_file}[/green]")
