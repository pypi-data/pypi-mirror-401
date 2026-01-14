from src.cli.config_loader import load_config
from src.connectors.rest_connector import GenericRestConnector
from src.connectors.playwright_connector import PlaywrightConnector


async def validate_config(args):
    print(f"🔍 Validating config: {args.config}")
    try:
        config = load_config(args.config)
        print("✅ YAML Syntax Valid")
        print("✅ Structure Valid")

        target_config = config.get("target", {})
        connection_type = target_config.get("connection", {}).get("type")
        platform = target_config.get("platform")

        # Determine connector type
        connector = None
        if connection_type == "playwright" or platform == "playwright":
            print("ℹ️  Using Playwright Connector")
            connector = PlaywrightConnector(target_config)
        elif connection_type == "rest" or platform == "custom-rest":
            print("ℹ️  Using REST Connector")
            connector = GenericRestConnector(target_config)
        else:
            print(f"⚠️  Unknown connection type: {connection_type}. Defaulting to REST.")
            connector = GenericRestConnector(target_config)

        # Initialize if needed (Playwright needs this)
        if hasattr(connector, "initialize"):
            await connector.initialize()

        print("📡 Testing connectivity...")
        if await connector.health_check():
            print("✅ Target Reachable")
            print("✅ Connection Successful")
        else:
            print("❌ Target Unreachable")

        # Cleanup
        if hasattr(connector, "close"):
            await connector.close()

    except Exception as e:
        print(f"❌ Validation Failed: {e}")
