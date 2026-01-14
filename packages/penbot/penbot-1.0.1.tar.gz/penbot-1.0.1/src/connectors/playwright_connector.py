import asyncio
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from playwright.async_api import async_playwright

from src.connectors.base import BaseConnector
from src.utils.logging import get_logger

logger = get_logger(__name__)


class PlaywrightConnector(BaseConnector):
    """
    A universal connector that uses Browser Automation (Playwright) to interact with chatbots.
    It simulates a real user typing in the chat window.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        # Access endpoint from connection config provided by BaseConnector
        self.url = self.connection_config.get("endpoint")
        self.selectors = config.get("selectors", {})
        self.browser_config = config.get("browser", {})

        # State
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.last_message_count = 0

    async def initialize(self) -> bool:
        """Launches the browser and navigates to the target."""
        try:
            logger.info("playwright_initializing", target=self.name, url=self.url)
            self.playwright = await async_playwright().start()

            headless = self.browser_config.get("headless", True)
            self.browser = await self.playwright.chromium.launch(headless=headless)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()

            await self.page.goto(self.url)

            # Optional: Accept Cookies
            cookie_selector = self.selectors.get("cookie_button")
            if cookie_selector:
                try:
                    logger.info("playwright_checking_cookies", selector=cookie_selector)
                    # Try main page (cookies usually on main page)
                    # Use a short timeout
                    try:
                        cookie_btn = self.page.locator(cookie_selector).first
                        if await cookie_btn.is_visible(timeout=5000):
                            await cookie_btn.click()
                            logger.info("playwright_cookies_accepted")
                            await asyncio.sleep(1)
                    except Exception:
                        pass  # No cookie banner found, ignore
                except Exception as e:
                    logger.warning("playwright_cookie_error", error=str(e))

            # Optional: Click to open chat window
            open_selector = self.selectors.get("open_chat_button")
            if open_selector:
                try:
                    logger.info("playwright_opening_chat", selector=open_selector)
                    # Try main page then frames
                    open_btn = await self._get_locator(open_selector)
                    await open_btn.click()
                    await asyncio.sleep(2)  # Wait for animation
                except Exception as e:
                    logger.warning("playwright_failed_to_open_chat", error=str(e))

            # Wait for the chat input to be visible to confirm load
            input_selector = self.selectors.get("input_field")
            if input_selector:
                try:
                    await self.page.wait_for_selector(input_selector, timeout=15000)
                except Exception:
                    logger.warning(
                        "playwright_input_not_found_immediately", selector=input_selector
                    )

            # Initial message count (to distinguish new replies later)
            self.last_message_count = await self._count_messages()

            logger.info("playwright_initialized", target=self.name)
            return True
        except Exception as e:
            logger.error("playwright_init_failed", error=str(e))
            return False

    async def _get_locator(self, selector: str, timeout: int = 10000):
        """
        Helper to find an element, checking both the main page AND iframes.
        Retries scanning frames until timeout.
        """
        start_time = datetime.now()

        while (datetime.now() - start_time).total_seconds() * 1000 < timeout:
            # 1. Try main page
            loc = self.page.locator(selector)
            if await loc.count() > 0 and await loc.first.is_visible():
                return loc.first

            # 2. Try all frames
            # logger.debug("playwright_scanning_frames", frame_count=len(self.page.frames))
            for frame in self.page.frames:
                try:
                    loc = frame.locator(selector)
                    if await loc.count() > 0 and await loc.first.is_visible():
                        logger.info(
                            "playwright_found_in_frame", selector=selector, frame_url=frame.url
                        )
                        return loc.first
                except Exception:
                    continue

            # Wait a bit before retrying (frames might be loading)
            await asyncio.sleep(0.5)

        # 3. Fallback (will likely fail if we got here)
        logger.warning("playwright_selector_not_found_anywhere", selector=selector)
        return self.page.locator(selector)

    async def send_message(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        image_data: Optional[str] = None,
        image_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Types message into the browser and waits for a reply."""
        if not self.page:
            await self.initialize()

        if image_data:
            logger.warning("playwright_image_not_supported_yet")

        input_selector = self.selectors.get("input_field")
        submit_selector = self.selectors.get("submit_button")
        self.selectors.get("response_container")

        try:
            # 1. Type Message
            input_el = await self._get_locator(input_selector)
            await input_el.fill(message)

            # 2. Send (Click button or Press Enter)
            if submit_selector:
                submit_el = await self._get_locator(submit_selector)
                await submit_el.click()
            else:
                await input_el.press("Enter")

            # 3. Wait for Response
            # Strategy: Wait for the number of message bubbles to increase
            timeout = self.config.get("timeout", 30000)
            new_reply = await self._wait_for_new_message(timeout)

            return {
                "content": new_reply,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "metadata": {"source": "playwright"},
            }

        except Exception as e:
            logger.error("playwright_interaction_error", error=str(e))
            return {"content": "[Error: Browser interaction failed]", "metadata": {"error": str(e)}}

    async def receive_message(self) -> Dict[str, Any]:
        """Not used in request-response flow, handled inside send_message."""

    async def health_check(self) -> bool:
        """Checks if the page is open and input is interactive."""
        try:
            if not self.page:
                return False

            input_selector = self.selectors.get("input_field", "body")
            el = await self._get_locator(input_selector)
            return await el.is_visible()
        except Exception:
            return False

    async def close(self) -> None:
        """Closes the browser."""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        logger.info("playwright_closed")

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        mime_type: str = "application/octet-stream",
        context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file via browser automation (for RAG testing).

        Args:
            file_content: File bytes
            filename: Name of the file
            mime_type: MIME type
            context: Additional context

        Returns:
            Dict with upload result
        """
        # Check if file upload selector is configured
        upload_selector = self.selectors.get("file_upload_input")
        if not upload_selector:
            logger.warning(
                "file_upload_not_configured",
                message="Set 'selectors.file_upload_input' in config for file uploads",
            )
            raise NotImplementedError(
                "File upload not configured. Add 'file_upload_input' selector to config."
            )

        try:
            import tempfile
            import os

            # Write file to temporary location (Playwright needs a file path)
            with tempfile.NamedTemporaryFile(
                mode="wb", delete=False, suffix=f"_{filename}"
            ) as temp_file:
                temp_file.write(file_content)
                temp_path = temp_file.name

            logger.info("file_upload_starting", filename=filename, size=len(file_content))

            # Find file input element
            file_input = await self._get_locator(upload_selector, timeout=10000)

            # Upload file
            await file_input.set_input_files(temp_path)

            # Wait for upload to complete (check for success indicators)
            await asyncio.sleep(2)  # Basic wait

            # Optional: Click upload submit button if configured
            upload_submit = self.selectors.get("file_upload_submit")
            if upload_submit:
                submit_btn = await self._get_locator(upload_submit, timeout=5000)
                await submit_btn.click()
                await asyncio.sleep(2)

            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass

            logger.info("file_uploaded", filename=filename)

            return {
                "success": True,
                "file_id": None,  # Browser automation doesn't return file IDs
                "message": "File uploaded successfully via browser automation",
                "metadata": {
                    "filename": filename,
                    "size": len(file_content),
                    "mime_type": mime_type,
                    "method": "playwright",
                },
            }

        except Exception as e:
            logger.error("file_upload_failed", filename=filename, error=str(e))
            return {
                "success": False,
                "message": f"Upload failed: {str(e)}",
                "metadata": {"error": str(e)},
            }

    async def _count_messages(self) -> int:
        """Counts current message bubbles."""
        selector = self.selectors.get("response_container")
        if not selector:
            return 0

        # We need to count all matches across all frames potentially
        # But typically all messages are in one container.
        # We'll reuse the locator logic to find the container first?
        # Actually, _get_locator returns the FIRST match.
        # For counting, we probably want the count of that specific locator.

        try:
            # Use the frame-aware locator logic to find where messages live
            # This is a bit tricky because selector might be ".message" which exists multiple times
            # We assume all messages are in the SAME frame as the input usually.

            # Simplified: Just scan frames and sum up? Or find the main chat frame.
            # Let's try to find the frame that has the input box, and count messages there.

            # For now, iterate and return first non-zero count
            for frame in self.page.frames:
                count = await frame.locator(selector).count()
                if count > 0:
                    return count

            return await self.page.locator(selector).count()
        except Exception:
            return 0

    async def _wait_for_new_message(self, timeout_ms: int) -> str:
        """
        Waits for a new message bubble to appear and returns its text.
        Handles streaming responses by waiting for text stability.
        """
        selector = self.selectors.get("response_container")
        if not selector:
            return ""

        start_time = datetime.now()

        # Find the active frame first
        active_frame = self.page
        for frame in self.page.frames:
            if await frame.locator(self.selectors.get("input_field")).count() > 0:
                active_frame = frame
                break

        # Polling loop to find NEW message
        target_element = None
        while (datetime.now() - start_time).total_seconds() * 1000 < timeout_ms:
            try:
                current_count = await active_frame.locator(selector).count()
                if current_count > self.last_message_count:
                    # New message found!
                    target_element = active_frame.locator(selector).last
                    self.last_message_count = current_count
                    break
            except Exception:
                pass
            await asyncio.sleep(0.5)

        if not target_element:
            return "[Timeout: No reply received]"

        # Wait for streaming to finish (Text stability check)
        # We check every 500ms. If text doesn't change for 1.5 seconds, we assume it's done.
        last_text = ""
        stable_start = datetime.now()

        # Give it up to 30 more seconds for streaming to complete
        stream_timeout = 30000
        stream_start = datetime.now()

        while (datetime.now() - stream_start).total_seconds() * 1000 < stream_timeout:
            try:
                current_text = await target_element.inner_text()
                if current_text == last_text and current_text.strip():
                    # Text hasn't changed. How long has it been stable?
                    if (datetime.now() - stable_start).total_seconds() > 1.5:
                        return current_text
                else:
                    # Text changed (streaming), reset stability timer
                    last_text = current_text
                    stable_start = datetime.now()

                await asyncio.sleep(0.5)
            except Exception:
                break  # Element might have disappeared

        return last_text  # Return whatever we have if timeout hits
