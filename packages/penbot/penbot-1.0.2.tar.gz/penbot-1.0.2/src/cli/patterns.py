"""
Pattern browsing and search commands for exploring attack libraries.
"""

import json
from pathlib import Path

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

ATTACK_LIBRARY_DIR = Path("src/attack_library")


def list_patterns(args):
    """List all pattern libraries and their contents."""
    if not ATTACK_LIBRARY_DIR.exists():
        console.print("❌ Attack library directory not found.")
        return

    pattern_files = list(ATTACK_LIBRARY_DIR.glob("*.json"))
    if not pattern_files:
        console.print("❌ No pattern files found.")
        return

    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]PenBot Attack Pattern Library[/bold cyan]\n"
            "[dim]Curated adversarial patterns for security testing[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    # Summary table
    table = Table(
        title="📚 Pattern Libraries", box=box.ROUNDED, show_header=True, header_style="bold green"
    )

    table.add_column("#", style="dim", width=3)
    table.add_column("Library", style="cyan", width=40)
    table.add_column("Patterns", justify="right", width=10)
    table.add_column("Categories", width=30)

    total_patterns = 0

    for i, file in enumerate(sorted(pattern_files), 1):
        try:
            with open(file, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            if isinstance(patterns, list):
                count = len(patterns)
                # Extract unique categories
                categories = set(p.get("category", "unknown") for p in patterns)
                cat_str = ", ".join(sorted(categories))[:30]
            else:
                count = 1
                cat_str = patterns.get("category", "unknown")

            total_patterns += count

            # Clean up filename for display
            name = file.stem.replace("_", " ").replace("patterns", "").strip().title()

            table.add_row(str(i), name, str(count), cat_str)

        except Exception as e:
            table.add_row(str(i), file.stem, "[red]Error[/red]", str(e)[:30])

    console.print(table)
    console.print()
    console.print(
        f"[dim]Total: {total_patterns} patterns across {len(pattern_files)} libraries[/dim]"
    )
    console.print()
    console.print("[dim]Use 'penbot patterns search <query>' to find specific patterns[/dim]")
    console.print("[dim]Use 'penbot patterns show <library>' to view patterns in a library[/dim]")
    console.print()


def search_patterns(args):
    """Search patterns by keyword."""
    query = args.query.lower()

    if not ATTACK_LIBRARY_DIR.exists():
        console.print("❌ Attack library directory not found.")
        return

    console.print(f"\n🔍 Searching for: [cyan]{query}[/cyan]\n")

    results = []

    for file in ATTACK_LIBRARY_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            if not isinstance(patterns, list):
                patterns = [patterns]

            for pattern in patterns:
                name = pattern.get("name", "")
                desc = pattern.get("description", "")
                category = pattern.get("category", "")

                # Search in name, description, and category
                if query in name.lower() or query in desc.lower() or query in category.lower():
                    results.append(
                        {
                            "library": file.stem,
                            "name": name,
                            "description": desc,
                            "category": category,
                            "priority": pattern.get("priority", 3),
                            "severity": pattern.get("severity_if_success", "unknown"),
                        }
                    )

        except Exception:
            continue

    if not results:
        console.print(f"❌ No patterns found matching '{query}'")
        return

    # Sort by priority (higher first)
    results.sort(key=lambda x: x["priority"], reverse=True)

    # Limit results
    max_results = args.limit if hasattr(args, "limit") and args.limit else 20
    results = results[:max_results]

    table = Table(
        title=f"🎯 Found {len(results)} Pattern(s)",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold green",
    )

    table.add_column("Name", style="cyan", width=35)
    table.add_column("Category", style="yellow", width=15)
    table.add_column("Severity", width=10)
    table.add_column("Library", style="dim", width=25)

    for r in results:
        severity = r["severity"].upper()
        if severity == "CRITICAL":
            sev_display = "[red bold]CRITICAL[/red bold]"
        elif severity == "HIGH":
            sev_display = "[orange1]HIGH[/orange1]"
        elif severity == "MEDIUM":
            sev_display = "[yellow]MEDIUM[/yellow]"
        else:
            sev_display = f"[dim]{severity}[/dim]"

        table.add_row(r["name"], r["category"], sev_display, r["library"][:24])

    console.print(table)
    console.print()
    console.print("[dim]Use 'penbot patterns view <name>' to see pattern details[/dim]")
    console.print()


def show_library(args):
    """Show patterns in a specific library."""
    library_name = args.library.lower()

    # Find matching library file
    matching_files = list(ATTACK_LIBRARY_DIR.glob(f"*{library_name}*.json"))

    if not matching_files:
        console.print(f"❌ Library not found: {library_name}")
        console.print("[dim]Use 'penbot patterns' to list available libraries[/dim]")
        return

    file = matching_files[0]  # Use first match

    try:
        with open(file, "r", encoding="utf-8") as f:
            patterns = json.load(f)
    except Exception as e:
        console.print(f"❌ Failed to load library: {e}")
        return

    if not isinstance(patterns, list):
        patterns = [patterns]

    console.print()
    console.print(
        Panel.fit(
            f"[bold cyan]{file.stem}[/bold cyan]\n" f"[dim]{len(patterns)} patterns[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    table = Table(box=box.ROUNDED, show_header=True, header_style="bold green")

    table.add_column("#", style="dim", width=3)
    table.add_column("Name", style="cyan", width=35)
    table.add_column("Description", width=45)
    table.add_column("Priority", justify="center", width=8)
    table.add_column("Severity", width=10)

    for i, pattern in enumerate(patterns[:50], 1):  # Limit to 50
        priority = pattern.get("priority", 3)
        priority_display = "⭐" * min(priority, 5)

        severity = pattern.get("severity_if_success", "unknown").upper()
        if severity == "CRITICAL":
            sev_display = "[red bold]CRIT[/red bold]"
        elif severity == "HIGH":
            sev_display = "[orange1]HIGH[/orange1]"
        elif severity == "MEDIUM":
            sev_display = "[yellow]MED[/yellow]"
        else:
            sev_display = f"[dim]{severity[:4]}[/dim]"

        table.add_row(
            str(i),
            pattern.get("name", "unknown"),
            pattern.get("description", "No description")[:45],
            priority_display,
            sev_display,
        )

    console.print(table)

    if len(patterns) > 50:
        console.print(f"\n[dim]Showing 50 of {len(patterns)} patterns[/dim]")

    console.print()


def view_pattern(args):
    """View detailed information about a specific pattern."""
    pattern_name = args.pattern_name.lower()

    # Search for pattern across all libraries
    found = None
    library = None

    for file in ATTACK_LIBRARY_DIR.glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                patterns = json.load(f)

            if not isinstance(patterns, list):
                patterns = [patterns]

            for pattern in patterns:
                if pattern.get("name", "").lower() == pattern_name:
                    found = pattern
                    library = file.stem
                    break

            if found:
                break

        except Exception:
            continue

    if not found:
        console.print(f"❌ Pattern not found: {pattern_name}")
        console.print("[dim]Use 'penbot patterns search <query>' to find patterns[/dim]")
        return

    console.print()
    console.print(
        Panel(
            f"[bold cyan]Name:[/bold cyan] {found.get('name', 'unknown')}\n"
            f"[bold cyan]Category:[/bold cyan] {found.get('category', 'unknown')}\n"
            f"[bold cyan]Priority:[/bold cyan] {'⭐' * found.get('priority', 3)}\n"
            f"[bold cyan]Severity if Success:[/bold cyan] {found.get('severity_if_success', 'unknown')}\n"
            f"[bold cyan]Library:[/bold cyan] {library}\n\n"
            f"[bold]Description:[/bold]\n{found.get('description', 'No description')}",
            title=f"🎯 Pattern Details",
            border_style="cyan",
        )
    )
    console.print()

    # Show template if present
    template = found.get("template", "")
    if template:
        console.print("[bold]Template:[/bold]")
        # Truncate very long templates
        if len(template) > 500:
            template = template[:500] + "\n... (truncated)"
        console.print(Panel(template, style="dim"))

    # Show success indicators if present
    indicators = found.get("success_indicators", [])
    if indicators:
        console.print("[bold]Success Indicators:[/bold]")
        for ind in indicators[:10]:
            console.print(f"  • {ind}")

    console.print()
