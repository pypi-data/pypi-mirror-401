"""
Dashboard server command for launching the PenBot UI.
"""

import subprocess
import sys
import webbrowser
from pathlib import Path
from time import sleep

from rich.console import Console
from rich.panel import Panel

console = Console()


def start_dashboard(args):
    """Start the PenBot dashboard server."""
    port = args.port if hasattr(args, "port") and args.port else 8000
    host = args.host if hasattr(args, "host") and args.host else "0.0.0.0"
    open_browser = not (hasattr(args, "no_browser") and args.no_browser)

    console.print()
    console.print(
        Panel.fit(
            "[bold cyan]PenBot Mission Control[/bold cyan]\n"
            "[dim]Real-time security testing dashboard[/dim]",
            border_style="cyan",
        )
    )
    console.print()

    console.print(f"🚀 Starting dashboard server on [cyan]http://{host}:{port}[/cyan]")
    console.print()

    # Check if frontend files exist
    frontend_dir = Path("frontend")
    dashboard_html = frontend_dir / "dashboard.html"

    if not dashboard_html.exists():
        console.print(f"[yellow]⚠️  Dashboard HTML not found at {dashboard_html}[/yellow]")
        console.print(
            "[dim]The API server will still start, but you may need to serve the frontend separately.[/dim]"
        )
    else:
        console.print(f"📂 Frontend: [green]{dashboard_html}[/green]")

    console.print()
    console.print("📡 [bold]Endpoints:[/bold]")
    console.print(f"   • API Docs:    http://localhost:{port}/docs")
    console.print(f"   • Health:      http://localhost:{port}/health")
    console.print(f"   • WebSocket:   ws://localhost:{port}/api/v1/ws/pentest/<session_id>")
    console.print(f"   • Dashboard:   file://{dashboard_html.absolute()}")
    console.print()
    console.print("[dim]Press Ctrl+C to stop the server[/dim]")
    console.print()

    # Open browser if requested
    if open_browser and dashboard_html.exists():
        console.print("🌐 Opening dashboard in browser...")
        sleep(1)  # Give server a moment to start
        try:
            webbrowser.open(f"file://{dashboard_html.absolute()}")
        except Exception as e:
            console.print(f"[yellow]⚠️  Could not open browser: {e}[/yellow]")

    # Start uvicorn server
    try:
        # Use subprocess to run uvicorn so we can handle keyboard interrupt cleanly
        cmd = [
            sys.executable,
            "-m",
            "uvicorn",
            "src.api.main:app",
            "--host",
            host,
            "--port",
            str(port),
            "--reload",
        ]

        console.print(f"[dim]Running: {' '.join(cmd)}[/dim]")
        console.print()

        # Run interactively so user sees logs
        subprocess.run(cmd)

    except KeyboardInterrupt:
        console.print("\n⚠️  Dashboard server stopped")
    except FileNotFoundError:
        console.print("❌ Could not find uvicorn. Install with: pip install uvicorn")
    except Exception as e:
        console.print(f"❌ Failed to start server: {e}")


def check_server_status(args):
    """Check if the dashboard server is running."""
    import httpx

    port = args.port if hasattr(args, "port") and args.port else 8000

    try:
        response = httpx.get(f"http://localhost:{port}/health", timeout=2.0)
        if response.status_code == 200:
            data = response.json()
            console.print(f"✅ Dashboard server is [green]running[/green] on port {port}")
            console.print(f"   Environment: {data.get('environment', 'unknown')}")
        else:
            console.print(f"⚠️  Server responded with status {response.status_code}")
    except httpx.ConnectError:
        console.print(f"❌ Dashboard server is [red]not running[/red] on port {port}")
        console.print(f"[dim]Start with: penbot dashboard[/dim]")
    except Exception as e:
        console.print(f"❌ Could not check server status: {e}")
