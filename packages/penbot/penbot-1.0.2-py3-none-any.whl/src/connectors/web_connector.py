"""Web UI connector using Playwright for browser automation."""

import asyncio
from typing import Dict, Any, Optional
from datetime import datetime
from playwright.async_api import Page, Browser, BrowserContext

from src.utils.logging import get_logger
from src.utils.helpers import generate_uuid

logger = get_logger(__name__)


# Preset selectors for popular chatbots
CHATBOT_PRESETS = {
    "chatgpt": {
        "input": "textarea[placeholder*='Message']",
        "submit": "button[data-testid='send-button']",
        "response": "[data-message-author-role='assistant']:last-child",
        "new_chat": "a[href='/']",
    },
    "claude": {
        "input": "div[contenteditable='true']",
        "submit": "button[aria-label='Send Message']",
        "response": ".response-content:last-child",
        "new_chat": "button[aria-label='New chat']",
    },
    "custom": {
        # User must provide custom selectors
    },
}


class WebUITargetConnector:
    """Connector for web-based chatbots using Playwright."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize web UI connector.

        Args:
            config: Configuration dict with:
                - url: str - Target chatbot URL
                - selectors: Dict - CSS selectors or preset name
                - headless: bool - Run in headless mode (default: True)
                - timeout: int - Default timeout in ms (default: 30000)
                - wait_for_response: int - Wait time for streaming (default: 2)
        """
        self.url = config["url"]
        self.headless = config.get("headless", True)
        self.default_timeout = config.get("timeout", 30000)
        self.wait_for_response = config.get("wait_for_response", 2)

        # Get selectors (either preset or custom)
        if isinstance(config.get("selectors"), str):
            preset_name = config["selectors"]
            if preset_name not in CHATBOT_PRESETS:
                raise ValueError(f"Unknown preset: {preset_name}")
            self.selectors = CHATBOT_PRESETS[preset_name]
        else:
            self.selectors = config.get("selectors", CHATBOT_PRESETS["custom"])

        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def _ensure_browser(self) -> Page:
        """Ensure browser and page are initialized."""
        if self.page and not self.page.is_closed():
            return self.page

        logger.info("initializing_browser", url=self.url, headless=self.headless)

        # Start Playwright
        if not self.playwright:
            from playwright.async_api import async_playwright

            self.playwright = await async_playwright().start()

        # Launch browser
        if not self.browser:
            self.browser = await self.playwright.chromium.launch(
                headless=self.headless, args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

        # Create context
        if not self.context:
            self.context = await self.browser.new_context(
                viewport={"width": 1920, "height": 1080},
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            )

            # Set default timeout
            self.context.set_default_timeout(self.default_timeout)

        # Create page
        if not self.page or self.page.is_closed():
            self.page = await self.context.new_page()

            # Navigate to URL
            await self.page.goto(self.url)
            await self.page.wait_for_load_state("networkidle")

        return self.page

    async def send_message(
        self,
        message: str,
        context: Dict[str, Any],
        image_data: Optional[str] = None,
        image_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send message via web UI.

        Supports multimodal messages (text + image) if target has file upload.

        Args:
            message: Message to send
            context: Context (not used for web UI)
            image_data: Optional base64-encoded image data
            image_mime_type: Optional image MIME type

        Returns:
            Response dict with 'content' and 'metadata'
        """
        page = await self._ensure_browser()

        start_time = datetime.utcnow()

        try:
            # Wait for input to be visible
            await page.wait_for_selector(
                self.selectors["input"], state="visible", timeout=self.default_timeout
            )

            # Clear and fill input
            await page.fill(self.selectors["input"], "")
            await page.type(self.selectors["input"], message, delay=50)  # Mimic human typing

            # Click submit button
            await page.click(self.selectors["submit"])

            # Wait for response to appear
            await page.wait_for_selector(
                self.selectors["response"], state="visible", timeout=self.default_timeout
            )

            # Wait for streaming to complete
            await asyncio.sleep(self.wait_for_response)

            # Extract response text
            response_element = await page.query_selector(self.selectors["response"])
            if not response_element:
                raise Exception("Response element not found")

            response_text = await response_element.inner_text()

            # Take screenshot as evidence
            screenshot_path = f"screenshots/response_{generate_uuid()}.png"
            await page.screenshot(path=screenshot_path, full_page=False)

            end_time = datetime.utcnow()
            response_time_ms = (end_time - start_time).total_seconds() * 1000

            logger.info(
                "web_ui_message_sent",
                url=self.url,
                response_time_ms=response_time_ms,
                response_length=len(response_text),
            )

            return {
                "content": response_text,
                "metadata": {
                    "method": "web_ui",
                    "url": self.url,
                    "response_time_ms": response_time_ms,
                    "screenshot": screenshot_path,
                },
            }

        except Exception as e:
            logger.error("web_ui_message_failed", url=self.url, error=str(e), exc_info=True)
            raise Exception(f"Failed to send message via web UI: {str(e)}")

    async def reset_conversation(self) -> None:
        """Reset conversation by clicking 'New Chat' button."""
        if "new_chat" not in self.selectors:
            logger.warning("new_chat_selector_not_configured", url=self.url)
            return

        page = await self._ensure_browser()

        try:
            await page.click(self.selectors["new_chat"])
            await page.wait_for_load_state("networkidle")
            logger.info("conversation_reset_via_web_ui", url=self.url)

        except Exception as e:
            logger.warning("conversation_reset_failed", url=self.url, error=str(e))

    async def health_check(self) -> bool:
        """
        Check if web UI is accessible.

        Returns:
            True if page loads successfully
        """
        try:
            page = await self._ensure_browser()

            # Check if input is visible
            input_visible = await page.is_visible(self.selectors["input"])

            return input_visible

        except Exception as e:
            logger.warning("health_check_failed", url=self.url, error=str(e))
            return False

    async def close(self) -> None:
        """Close browser and cleanup."""
        if self.page and not self.page.is_closed():
            await self.page.close()

        if self.context:
            await self.context.close()

        if self.browser:
            await self.browser.close()

        if self.playwright:
            await self.playwright.stop()

        logger.info("web_connector_closed", url=self.url)
