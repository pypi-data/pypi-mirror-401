"""
Main CLI application logic.
"""

import argparse
import sys
import asyncio

# Version info
__version__ = "1.0.0"


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="penbot",
        description="🤖 PenBot - AI Chatbot Security Testing Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  penbot wizard                              # Interactive setup for new target
  penbot test --config configs/client.yaml   # Run security test
  penbot test --config config.yaml --quick   # Quick smoke test (3 attacks)
  penbot sessions                            # List past test sessions
  penbot agents                              # List available security agents
  penbot patterns                            # Browse attack pattern libraries
  penbot report --latest                     # Generate report for latest session
  penbot dashboard                           # Start the Mission Control dashboard

Documentation: https://gitlab.com/yan-ban/penbot
        """,
    )

    parser.add_argument("--version", action="version", version=f"PenBot v{__version__}")

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    wizard_parser = subparsers.add_parser(
        "wizard", help="Interactive setup for new target configuration"
    )

    test_parser = subparsers.add_parser("test", help="Run security test against target")
    test_parser.add_argument("--config", required=True, help="Path to client config file (YAML)")
    test_parser.add_argument(
        "--quick", action="store_true", help="Run a quick smoke test (3 attacks)"
    )
    test_parser.add_argument("--max-attacks", type=int, help="Override maximum attacks limit")
    test_parser.add_argument(
        "--agents",
        type=str,
        help="Comma-separated list of agents to use (e.g., jailbreak,encoding,rag_poisoning)",
    )
    test_parser.add_argument(
        "--phase",
        type=str,
        choices=[
            "reconnaissance",
            "trust_building",
            "boundary_testing",
            "exploitation",
            "escalation",
        ],
        help="Start at specific campaign phase",
    )
    test_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview attacks without executing (show what would be sent)",
    )
    test_parser.add_argument(
        "--output", type=str, help="Output directory for reports (default: reports/)"
    )
    test_parser.add_argument("--non-interactive", action="store_true", help="Run without prompts")
    test_parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")

    validate_parser = subparsers.add_parser(
        "validate", help="Validate target configuration and test connectivity"
    )
    validate_parser.add_argument("--config", required=True, help="Path to client config file")

    platforms_parser = subparsers.add_parser("platforms", help="List supported chatbot platforms")

    report_parser = subparsers.add_parser("report", help="Generate security assessment reports")
    report_parser.add_argument("--session", help="Session ID to report on")
    report_parser.add_argument("--latest", action="store_true", help="Report on latest session")
    report_parser.add_argument(
        "--format",
        choices=["pdf", "html", "json"],
        default="html",
        help="Output format (default: html)",
    )
    report_parser.add_argument("--output", type=str, help="Output path for the report")

    sessions_parser = subparsers.add_parser("sessions", help="Manage past test sessions")
    sessions_subparsers = sessions_parser.add_subparsers(dest="sessions_action")

    # sessions (no action) - list sessions
    sessions_parser.set_defaults(sessions_action="list")

    # sessions view <id>
    sessions_view = sessions_subparsers.add_parser("view", help="View session details")
    sessions_view.add_argument(
        "session_id", help="Session ID or index number (e.g., 1 for most recent)"
    )

    # sessions delete <id>
    sessions_delete = sessions_subparsers.add_parser("delete", help="Delete a session")
    sessions_delete.add_argument("session_id", help="Session ID or index number")
    sessions_delete.add_argument(
        "-f", "--force", action="store_true", help="Skip confirmation prompt"
    )

    # sessions export <id>
    sessions_export = sessions_subparsers.add_parser(
        "export", help="Export session to CSV or Markdown"
    )
    sessions_export.add_argument("session_id", help="Session ID or index number")
    sessions_export.add_argument(
        "--format", choices=["csv", "markdown"], default="csv", help="Export format"
    )
    sessions_export.add_argument("--output", type=str, help="Output directory")

    agents_parser = subparsers.add_parser(
        "agents", help="List and describe available security agents"
    )
    agents_subparsers = agents_parser.add_subparsers(dest="agents_action")

    # agents (no action) - list agents
    agents_parser.set_defaults(agents_action="list")

    # agents describe <id>
    agents_describe = agents_subparsers.add_parser(
        "describe", help="Show detailed agent information"
    )
    agents_describe.add_argument("agent_id", help="Agent ID (e.g., jailbreak, encoding)")

    patterns_parser = subparsers.add_parser(
        "patterns", help="Browse and search attack pattern libraries"
    )
    patterns_subparsers = patterns_parser.add_subparsers(dest="patterns_action")

    # patterns (no action) - list libraries
    patterns_parser.set_defaults(patterns_action="list")

    # patterns search <query>
    patterns_search = patterns_subparsers.add_parser("search", help="Search patterns by keyword")
    patterns_search.add_argument("query", help="Search keyword")
    patterns_search.add_argument("--limit", type=int, default=20, help="Maximum results to show")

    # patterns show <library>
    patterns_show = patterns_subparsers.add_parser("show", help="Show patterns in a library")
    patterns_show.add_argument("library", help="Library name (partial match supported)")

    # patterns view <pattern_name>
    patterns_view = patterns_subparsers.add_parser("view", help="View pattern details")
    patterns_view.add_argument("pattern_name", help="Pattern name")

    dashboard_parser = subparsers.add_parser(
        "dashboard", help="Start the Mission Control dashboard server"
    )
    dashboard_parser.add_argument(
        "--port", type=int, default=8000, help="Server port (default: 8000)"
    )
    dashboard_parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Server host (default: 0.0.0.0)"
    )
    dashboard_parser.add_argument(
        "--no-browser", action="store_true", help="Don't open browser automatically"
    )
    dashboard_parser.add_argument(
        "--status", action="store_true", help="Check if dashboard is running"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Platforms (synchronous, no imports needed)
        if args.command == "platforms":
            show_platforms()

        # Wizard
        elif args.command == "wizard":
            from src.cli.wizard import run_wizard

            asyncio.run(run_wizard(args))

        # Test
        elif args.command == "test":
            from src.cli.test_runner import run_test

            asyncio.run(run_test(args))

        # Validate
        elif args.command == "validate":
            from src.cli.validator import validate_config

            asyncio.run(validate_config(args))

        # Report
        elif args.command == "report":
            from src.cli.reporter import run_report

            asyncio.run(run_report(args))

        # Sessions
        elif args.command == "sessions":
            from src.cli.sessions import list_sessions, view_session, delete_session, export_session

            if args.sessions_action == "list" or args.sessions_action is None:
                list_sessions(args)
            elif args.sessions_action == "view":
                view_session(args)
            elif args.sessions_action == "delete":
                delete_session(args)
            elif args.sessions_action == "export":
                export_session(args)

        # Agents
        elif args.command == "agents":
            from src.cli.agents_cmd import list_agents, describe_agent

            if args.agents_action == "list" or args.agents_action is None:
                list_agents(args)
            elif args.agents_action == "describe":
                describe_agent(args)

        # Patterns
        elif args.command == "patterns":
            from src.cli.patterns import list_patterns, search_patterns, show_library, view_pattern

            if args.patterns_action == "list" or args.patterns_action is None:
                list_patterns(args)
            elif args.patterns_action == "search":
                search_patterns(args)
            elif args.patterns_action == "show":
                show_library(args)
            elif args.patterns_action == "view":
                view_pattern(args)

        # Dashboard
        elif args.command == "dashboard":
            from src.cli.dashboard_cmd import start_dashboard, check_server_status

            if hasattr(args, "status") and args.status:
                check_server_status(args)
            else:
                start_dashboard(args)

    except KeyboardInterrupt:
        print("\n⚠️  Operation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback

        if "--verbose" in sys.argv or "-v" in sys.argv:
            traceback.print_exc()
        sys.exit(1)


def show_platforms():
    """List supported platforms."""
    print("\n🤖 Supported Chatbot Platforms:\n")
    platforms = [
        ("dialogflow", "Google Dialogflow CX/ES"),
        ("rasa", "Rasa Open Source"),
        ("azure-bot", "Microsoft Azure Bot Service"),
        ("aws-lex", "Amazon Lex"),
        ("custom-rest", "Generic REST API (JSON)"),
        ("playwright", "Browser Automation (Playwright)"),
        ("moveo", "Moveo.AI (WebSocket)"),
        ("websocket", "Generic WebSocket"),
    ]

    for pid, name in platforms:
        print(f"  • {pid:<15} - {name}")
    print("\nUse 'penbot wizard' to configure a new target.\n")


if __name__ == "__main__":
    main()
