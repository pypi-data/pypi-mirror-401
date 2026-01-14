import json
from pathlib import Path
from datetime import datetime
import sys

# Add the project root to sys.path for imports
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.reporting.detailed_report_generator import DetailedReportGenerator
from src.reporting.owasp_compliance import OWASPComplianceReport
from rich.console import Console

console = Console()


async def run_report(args):
    """
    Generate a penetration test report.
    """
    session_id = args.session
    if args.latest:
        # Find the latest session file
        sessions_dir = Path("sessions")
        if not sessions_dir.exists():
            console.print("❌ No sessions directory found. Run a test first.")
            return

        files = list(sessions_dir.glob("*.json"))
        if not files:
            console.print("❌ No session files found.")
            return

        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        session_id = latest_file.stem
        console.print(f"📄 Using latest session: [cyan]{session_id}[/cyan]")

    if not session_id:
        console.print("❌ Please specify a session ID or use --latest")
        return

    file_path = Path("sessions") / f"{session_id}.json"
    if not file_path.exists():
        console.print(f"❌ Session file not found: {file_path}")
        return

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            session_data = json.load(f)
    except Exception as e:
        console.print(f"❌ Failed to load session data: {e}")
        return

    console.print(
        f"📊 Generating [bold]{args.format.upper()}[/bold] report for session: {session_id}"
    )

    # Prepare data for reporting
    findings = session_data.get("security_findings", [])
    target_name = session_data.get("target_name", "Unknown Target")

    started_at_str = session_data.get("started_at")
    completed_at_str = session_data.get("completed_at")

    # Parse dates if they are strings
    started_at = datetime.fromisoformat(started_at_str) if started_at_str else datetime.utcnow()
    if isinstance(completed_at_str, str):
        completed_at = datetime.fromisoformat(completed_at_str)
    else:
        completed_at = datetime.utcnow()

    # Generate OWASP Report content
    owasp_reporter = OWASPComplianceReport()
    owasp_report = owasp_reporter.generate_report(
        findings=findings,
        test_session_id=session_id,
        target_name=target_name,
        started_at=started_at,
        completed_at=completed_at,
    )

    # Generate Detailed Findings content
    detailed_generator = DetailedReportGenerator()
    detailed_findings = []
    for finding in findings:
        detailed_findings.append(detailed_generator.generate_report(finding))

    if args.format == "json":
        output_data = {
            "owasp_report": owasp_report,
            "detailed_findings": detailed_findings,
            "raw_session": session_data,
        }
        output_file = Path("reports") / f"report_{session_id}.json"
        output_file.parent.mkdir(exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2)
        console.print(f"✅ JSON report saved to: [green]{output_file}[/green]")

    elif args.format == "html":
        generate_html_report(session_id, owasp_report, detailed_findings, session_data)

    elif args.format == "pdf":
        console.print("⚠️  PDF generation requires 'weasyprint'. Generating HTML instead...")
        generate_html_report(session_id, owasp_report, detailed_findings, session_data)


def generate_html_report(session_id, owasp_report, detailed_findings, session_data):
    """Generate a standalone HTML report matching the main dashboard style."""

    # OWASP category names for proper display
    owasp_names = {
        "LLM01": "Prompt Injection",
        "LLM02": "Sensitive Information Disclosure",
        "LLM03": "Supply Chain",
        "LLM04": "Data and Model Poisoning",
        "LLM05": "Improper Output Handling",
        "LLM06": "Excessive Agency",
        "LLM07": "System Prompt Leakage",
        "LLM08": "Vector and Embedding Weaknesses",
        "LLM09": "Misinformation",
        "LLM10": "Unbounded Consumption",
    }

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>PenBot Security Report - {session_data.get('target_name')}</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-dark: #0a0a0f;
                --bg-card: #12121a;
                --border-color: #1e1e2e;
                --text-primary: #e0e0e0;
                --text-secondary: #888;
                --accent-cyan: #00D4FF;
                --accent-red: #ff4444;
                --accent-green: #00ff88;
                --accent-orange: #f59e0b;
                --severity-critical: #ff2d55;
                --severity-high: #ff6b35;
                --severity-medium: #f59e0b;
                --severity-low: #00ff88;
            }}
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            body {{
                font-family: 'JetBrains Mono', monospace;
                background-color: var(--bg-dark);
                color: var(--text-primary);
                line-height: 1.6;
                padding: 0;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }}
            .header {{
                background: linear-gradient(135deg, var(--bg-card) 0%, #1a1a2e 100%);
                padding: 1rem 1rem;
                border-bottom: 1px solid var(--border-color);
                margin-bottom: 1.5rem;
            }}
            .logo-container {{
                display: flex;
                align-items: center;
                gap: 0.75rem;
                margin-bottom: 0.5rem;
            }}
            .logo-img {{
                height: 70px;
                width: auto;
            }}
            .logo-text {{
                font-size: 1.6rem;
                font-weight: 700;
                color: var(--accent-cyan);
                text-shadow: 0 0 20px rgba(0, 212, 255, 0.3);
            }}
            h1 {{
                font-size: 1.2rem;
                color: var(--text-primary);
                margin: 0.25rem 0;
            }}
            .meta-info {{
                font-size: 0.75rem;
                color: var(--text-secondary);
            }}
            .card {{
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1.5rem;
            }}
            h2 {{
                font-size: 1.2rem;
                color: var(--accent-cyan);
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 1px solid var(--border-color);
            }}
            h3 {{ margin-top: 0; color: var(--text-primary); }}
            h4 {{
                color: var(--text-secondary);
                font-size: 0.9rem;
                margin: 1rem 0 0.5rem 0;
            }}
            .severity-badge {{
                padding: 0.25rem 0.75rem;
                border-radius: 4px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
            }}
            .severity-critical {{ background-color: var(--severity-critical); color: #000; }}
            .severity-high {{ background-color: var(--severity-high); color: #000; }}
            .severity-medium {{ background-color: var(--severity-medium); color: #000; }}
            .severity-low {{ background-color: var(--severity-low); color: #000; }}
            .severity-info {{ background-color: var(--accent-cyan); color: #000; }}
            .metric-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
                gap: 1rem;
                margin-bottom: 1.5rem;
            }}
            .metric {{
                text-align: center;
                padding: 1.25rem;
                background: rgba(0, 212, 255, 0.05);
                border: 1px solid var(--border-color);
                border-radius: 8px;
            }}
            .metric-value {{
                font-size: 2rem;
                font-weight: bold;
                color: var(--accent-cyan);
            }}
            .metric-value.risk-critical {{ color: var(--severity-critical); }}
            .metric-value.risk-high {{ color: var(--severity-high); }}
            .metric-value.risk-medium {{ color: var(--severity-medium); }}
            .metric-value.risk-low {{ color: var(--severity-low); }}
            .metric-label {{
                font-size: 0.8rem;
                color: var(--text-secondary);
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin-top: 0.25rem;
            }}
            .owasp-table {{
                width: 100%;
                border-collapse: collapse;
            }}
            .owasp-table th {{
                text-align: left;
                padding: 0.75rem;
                border-bottom: 2px solid var(--border-color);
                color: var(--text-secondary);
                font-size: 0.8rem;
                text-transform: uppercase;
            }}
            .owasp-table td {{
                padding: 0.75rem;
                border-bottom: 1px solid var(--border-color);
            }}
            .owasp-table tr:hover {{
                background: rgba(0, 212, 255, 0.05);
            }}
            .status-pass {{ color: var(--accent-green); }}
            .status-fail {{ color: var(--accent-red); }}
            .status-warn {{ color: var(--accent-orange); }}
            .finding-card {{
                background-color: var(--bg-card);
                border: 1px solid var(--border-color);
                border-radius: 8px;
                padding: 1.5rem;
                margin-bottom: 1rem;
                border-left: 4px solid var(--accent-cyan);
            }}
            .finding-card.critical {{ border-left-color: var(--severity-critical); }}
            .finding-card.high {{ border-left-color: var(--severity-high); }}
            .finding-card.medium {{ border-left-color: var(--severity-medium); }}
            .finding-card.low {{ border-left-color: var(--severity-low); }}
            .finding-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
            }}
            ul {{
                margin: 0.5rem 0;
                padding-left: 1.5rem;
            }}
            li {{
                margin: 0.3rem 0;
                color: var(--text-secondary);
            }}
            p {{
                color: var(--text-secondary);
                margin: 0.5rem 0;
            }}
            .assessment-text {{
                font-size: 0.95rem;
                line-height: 1.7;
                color: var(--text-primary);
            }}
            @media print {{
                body {{ background: white; color: #1a1a1a; }}
                .card {{ border: 1px solid #ddd; }}
                .metric-value {{ color: #2563eb; }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="container">
                <div class="logo-container">
                    <img src="../frontend/images/PenBot_2.png" alt="PenBot Logo" class="logo-img" onerror="this.style.display='none'">
                    <span class="logo-text">PenBot Security Report</span>
                </div>
                <h1>{session_data.get('target_name')}</h1>
                <p class="meta-info">Session ID: {session_id} | Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
        </div>

        <div class="container">
            <div class="card">
                <h2>Executive Summary</h2>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-value">{round(owasp_report['executive_summary']['compliance_score'], 1)}</div>
                        <div class="metric-label">Compliance Score</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value risk-{owasp_report['executive_summary']['risk_level'].lower()}">{owasp_report['executive_summary']['risk_level']}</div>
                        <div class="metric-label">Risk Level</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{len(detailed_findings)}</div>
                        <div class="metric-label">Total Findings</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{owasp_report['executive_summary']['critical_findings']}</div>
                        <div class="metric-label">Critical Issues</div>
                    </div>
                </div>
                <p class="assessment-text">{owasp_report['executive_summary']['overall_assessment']}</p>
            </div>

            <div class="card">
                <h2>OWASP LLM Top 10 2025 Compliance</h2>
                <table class="owasp-table">
                    <thead>
                        <tr>
                            <th>Category</th>
                            <th>Score</th>
                            <th>Findings</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    # Add OWASP rows with proper names
    for cat_id, score in owasp_report["compliance_score"]["category_scores"].items():
        findings_count = len(owasp_report["owasp_category_mapping"].get(cat_id, []))

        # Determine status class
        if score == 100:
            status_class = "status-pass"
        elif score < 70:
            status_class = "status-fail"
        else:
            status_class = "status-warn"

        # Get proper OWASP name
        cat_name = owasp_names.get(cat_id, cat_id)

        # Round score to 1 decimal place
        rounded_score = round(score, 1)

        html_content += f"""
                        <tr>
                            <td><strong>{cat_id}</strong>: {cat_name}</td>
                            <td class="{status_class}" style="font-weight: bold;">{rounded_score}%</td>
                            <td>{findings_count}</td>
                        </tr>
        """

    html_content += """
                    </tbody>
                </table>
            </div>

            <h2 style="color: var(--accent-cyan); margin: 2rem 0 1rem 0;">Detailed Findings</h2>
    """

    if not detailed_findings:
        html_content += """
            <div class="card">
                <p style="text-align: center; color: var(--text-secondary);">No security findings detected. The system appears well-protected against tested attack vectors.</p>
            </div>
        """
    else:
        for i, finding in enumerate(detailed_findings, 1):
            severity = finding["summary"]["severity"].lower()
            html_content += f"""
                <div class="finding-card {severity}">
                    <div class="finding-header">
                        <h3>{i}. {finding['summary']['title']}</h3>
                        <span class="severity-badge severity-{severity}">{finding['summary']['severity']}</span>
                    </div>
                    <p><strong>Category:</strong> {finding['summary']['category']}</p>
                    <p>{finding['summary']['description']}</p>

                    <h4>Exploitation Scenario</h4>
                    <p><strong>Business Impact:</strong></p>
                    <ul>
                        {''.join(f'<li>{item}</li>' for item in finding['exploitation_scenario']['business_impact'])}
                    </ul>

                    <h4>Remediation</h4>
                    <p><strong>Priority:</strong> {finding['remediation_steps']['priority']['level']} ({finding['remediation_steps']['priority']['timeframe']})</p>
                    <ul>
                        {''.join(f'<li>{item}</li>' for item in finding['remediation_steps']['immediate_actions'])}
                    </ul>
                </div>
            """

    html_content += """
        </div>
    </body>
    </html>
    """

    output_file = Path("reports") / f"report_{session_id}.html"
    output_file.parent.mkdir(exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    console.print(f"[green]HTML report saved to:[/green] [bold]{output_file}[/bold]")
