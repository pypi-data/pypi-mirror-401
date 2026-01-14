from pathlib import Path
from typing import Dict, Any
import yaml
import httpx
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

console = Console()


async def run_wizard(args):
    """
    Runs the interactive configuration wizard.
    """
    console.clear()
    console.print(
        Panel.fit(
            "🧙‍♂️ [bold blue]PenBot Configuration Wizard[/bold blue]\n[dim]Create a new client configuration in minutes[/dim]",
            border_style="blue",
        )
    )

    config: Dict[str, Any] = {
        "client": {},
        "target": {
            "connection": {"auth": {"type": "none"}, "headers": {}},
            "format": {"request": {}, "response": {}},
        },
        "test": {},
    }

    # --- Step 1: Client Information ---
    console.print("\n[bold]1️⃣  Client Information[/bold]")
    config["client"]["name"] = Prompt.ask("Client Name (e.g., NRG)")
    filename = config["client"]["name"].lower().replace(" ", "-") + ".yaml"
    config["client"]["contact"] = Prompt.ask("Contact Email", default="security@example.com")
    config["client"]["project_id"] = Prompt.ask(
        "Project ID", default=f"{config['client']['name'].upper()}-001"
    )

    # --- Step 2: Connection Details ---
    console.print("\n[bold]2️⃣  Connection Setup[/bold]")
    console.print("[dim]Use your browser's DevTools to find these details.[/dim]")

    conn_type = Prompt.ask("Connection Type", choices=["rest", "playwright"], default="rest")
    config["target"]["connection"]["type"] = conn_type

    endpoint = Prompt.ask("Target URL (Website URL for Playwright, API Endpoint for REST)")
    config["target"]["connection"]["endpoint"] = endpoint
    config["target"]["name"] = Prompt.ask(
        "Target Name", default=f"{config['client']['name']} Chatbot"
    )

    if conn_type == "rest":
        # --- Authentication Setup ---
        if Confirm.ask("Does the API require authentication?", default=False):
            auth_type = Prompt.ask("Auth Type", choices=["api_key", "bearer"], default="api_key")
            config["target"]["connection"]["auth"]["type"] = auth_type

            if auth_type == "api_key":
                env_var = Prompt.ask(
                    "Environment variable name for API Key", default="CHATBOT_API_KEY"
                )
                config["target"]["connection"]["auth"]["api_key_env"] = env_var
                config["target"]["connection"]["auth"]["header_name"] = Prompt.ask(
                    "Header Name", default="X-API-Key"
                )
                rprint(f"[yellow]⚠️  Make sure to export {env_var} before running tests![/yellow]")
            elif auth_type == "bearer":
                env_var = Prompt.ask("Environment variable name for Token", default="CHATBOT_TOKEN")
                config["target"]["connection"]["auth"]["token_env"] = env_var
                rprint(f"[yellow]⚠️  Make sure to export {env_var} before running tests![/yellow]")

        # REST Header setup
        if Confirm.ask("Do you need other custom headers? (e.g., User-Agent)", default=False):
            while True:
                header_str = Prompt.ask(
                    "Enter header (Format: 'Key: Value') or press Enter to finish"
                )
                if not header_str:
                    break
                if ":" in header_str:
                    key, value = header_str.split(":", 1)
                    config["target"]["connection"]["headers"][key.strip()] = value.strip()

        # --- Step 3: Request Format (REST ONLY) ---
        console.print("\n[bold]3️⃣  Request Format[/bold]")
        console.print("We need to know how to structure the JSON payload.")

        message_field = Prompt.ask(
            "Which JSON field holds the message? (e.g. 'message' or 'data.query')",
            default="message",
        )
        config["target"]["format"]["request"]["message_field"] = message_field

        # Optional: Context/Session fields
        if Confirm.ask("Does the API require a session ID field?", default=False):
            session_field = Prompt.ask("Session ID field name", default="session_id")
            config["target"]["format"]["request"]["session_field"] = session_field

    elif conn_type == "playwright":
        # Playwright Selector setup
        console.print("\n[bold]3️⃣  Browser Automation Setup[/bold]")
        console.print("We need CSS Selectors to interact with the page.")
        console.print(
            "[dim]Tip: Right-click element -> Inspect -> Right-click HTML -> Copy -> Copy Selector[/dim]"
        )

        config["target"]["selectors"] = {}
        config["target"]["selectors"]["open_chat_button"] = Prompt.ask(
            "Selector for Chat Icon (to open window)", default=".launcher-btn"
        )
        config["target"]["selectors"]["input_field"] = Prompt.ask(
            "CSS Selector for Input Box", default="div.message-input"
        )
        config["target"]["selectors"]["submit_button"] = Prompt.ask(
            "CSS Selector for Send Button (Optional - press Enter if Enter key works)", default=""
        )
        config["target"]["selectors"]["response_container"] = Prompt.ask(
            "CSS Selector for Message Bubbles (e.g., .message-bubble)",
            default="li[data-event-type='brain_message']",
        )

        config["target"]["browser"] = {"headless": True}

    # --- Step 4: Connectivity Test & Response Parsing ---
    console.print("\n[bold]4️⃣  Live Connectivity Test[/bold]")

    if Confirm.ask(f"Ready to test connection to [cyan]{endpoint}[/cyan]?", default=True):
        if conn_type == "rest":
            await test_connection_and_configure_response(config)
        elif conn_type == "playwright":
            await test_playwright_connection(config)

    # --- Step 5: Test Settings ---
    console.print("\n[bold]5️⃣  Test Settings[/bold]")
    config["test"]["max_attacks"] = int(Prompt.ask("Default Max Attacks", default="60"))
    config["test"]["phases"] = ["reconnaissance", "probing", "exploitation"]
    config["test"]["agents"] = [
        "jailbreak",
        "encoding",
        "impersonation",
        "info_disclosure",
        "output_security",
        "compliance",
        "token_soup",
        "evolutionary",
    ]

    # --- Save Configuration ---
    output_dir = Path("configs/clients")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename

    save_config(config, output_path)


async def test_playwright_connection(config: Dict[str, Any]):
    """
    Tests the Playwright connection by launching a browser and typing a message.
    """
    from src.connectors.playwright_connector import PlaywrightConnector

    rprint(f"[dim]Launching browser...[/dim]")
    connector = PlaywrightConnector(config["target"])

    try:
        success = await connector.initialize()
        if not success:
            rprint("[bold red]❌ Could not launch browser or navigate to URL.[/bold red]")
            return

        rprint(f"[bold green]✅ Browser launched & navigated![/bold green]")

        if Confirm.ask("Send 'Hello' test message?", default=True):
            response = await connector.send_message("Hello")
            rprint(Panel(response["content"], title="Bot Response"))

            if "[Error" in response["content"] or "[Timeout" in response["content"]:
                rprint("[yellow]⚠️  Interaction failed. Check your CSS selectors.[/yellow]")
            else:
                rprint("[bold green]✅ Full interaction successful![/bold green]")

    except Exception as e:
        rprint(f"[bold red]❌ Playwright Error: {e}[/bold red]")
    finally:
        await connector.close()


async def test_connection_and_configure_response(config: Dict[str, Any]):
    """
    Sends a test request and helps the user identify the response field.
    """
    endpoint = config["target"]["connection"]["endpoint"]
    headers = config["target"]["connection"].get("headers", {})
    msg_field = config["target"]["format"]["request"]["message_field"]

    # Build simple payload
    payload = {msg_field: "Hello"}

    # Add session ID if configured
    if "session_field" in config["target"]["format"]["request"]:
        payload[config["target"]["format"]["request"]["session_field"]] = "test_wizard_session"

    # Handle nested fields if message_field contains dots
    if "." in msg_field:
        payload = {}
        parts = msg_field.split(".")
        current = payload
        for part in parts[:-1]:
            current[part] = {}
            current = current[part]
        current[parts[-1]] = "Hello"

    console.print(f"[dim]Sending payload: {payload}[/dim]")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(endpoint, json=payload, headers=headers)

            if response.status_code >= 400:
                rprint(f"[bold red]❌ Request failed with status {response.status_code}[/bold red]")
                rprint(f"Response: {response.text}")
                if not Confirm.ask("Continue anyway?", default=False):
                    return
            else:
                rprint(
                    f"[bold green]✅ Connection Successful! (Status {response.status_code})[/bold green]"
                )

                try:
                    json_response = response.json()
                    console.print(
                        Panel(
                            Syntax(str(json_response), "json", theme="monokai"),
                            title="Server Response",
                        )
                    )

                    # Heuristic: Try to find "Hello" or common response fields
                    suggested_path = suggest_response_path(json_response)

                    rprint(f"\nWe need to extract the bot's text from this JSON.")
                    if suggested_path:
                        rprint(f"Suggested JSONPath: [cyan]{suggested_path}[/cyan]")
                        path = Prompt.ask("Enter JSONPath to response text", default=suggested_path)
                    else:
                        path = Prompt.ask(
                            "Enter JSONPath to response text (e.g., 'response.text' or '0.content')"
                        )

                    config["target"]["format"]["response"]["message_field"] = path

                except Exception as e:
                    rprint(f"[yellow]⚠️ Could not parse JSON response: {e}[/yellow]")
                    config["target"]["format"]["response"]["message_field"] = Prompt.ask(
                        "Enter JSONPath manually"
                    )

    except Exception as e:
        rprint(f"[bold red]❌ Connection Error: {e}[/bold red]")


def suggest_response_path(data: Any, parent_path: str = "") -> str:
    """Recursive helper to find a likely string field in the response."""
    if isinstance(data, dict):
        for k, v in data.items():
            current_path = f"{parent_path}.{k}" if parent_path else k
            if isinstance(v, str) and len(v) > 0:
                # Prioritize keys that look like message content
                if k in ["text", "message", "content", "reply", "answer", "bot_response"]:
                    return current_path
            elif isinstance(v, (dict, list)):
                found = suggest_response_path(v, current_path)
                if found:
                    return found
    elif isinstance(data, list):
        if len(data) > 0:
            return suggest_response_path(data[0], f"{parent_path}.0" if parent_path else "0")
    return ""


def save_config(config: Dict[str, Any], path: Path):
    """Saves the configuration to a YAML file."""

    # Custom dump to look nicer
    class NoAliasDumper(yaml.SafeDumper):
        def ignore_aliases(self, data):
            return True

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, Dumper=NoAliasDumper, default_flow_style=False, sort_keys=False)

    console.print(f"\n[bold green]✅ Configuration saved to: {path}[/bold green]")
    console.print(f"Run test with: [cyan]penbot test --config {path} --quick[/cyan]")
