"""API connector for REST/GraphQL/WebSocket chatbot targets."""

import asyncio
import random
import time
from typing import Dict, Any, Optional
from datetime import datetime
import aiohttp
from aiohttp import ClientSession, TCPConnector, ClientTimeout

from src.utils.logging import get_logger
from src.utils.metrics import record_connector_latency, record_circuit_breaker_open

logger = get_logger(__name__)


class CircuitBreaker:
    """
    Circuit breaker pattern for resilient API calls.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Too many failures, reject requests immediately
    - HALF_OPEN: Testing if service recovered (after timeout)
    """

    def __init__(self, failure_threshold: int = 5, timeout_seconds: int = 60):
        """
        Initialize circuit breaker.

        Args:
            failure_threshold: Number of consecutive failures before opening circuit
            timeout_seconds: How long to wait before trying again (half-open state)
        """
        self.failure_threshold = failure_threshold
        self.timeout_seconds = timeout_seconds
        self.failures = 0
        self.opened_at: Optional[float] = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_failure(self) -> None:
        """Record a failure and potentially open the circuit."""
        self.failures += 1

        if self.failures >= self.failure_threshold and self.state == "CLOSED":
            self.opened_at = time.time()
            self.state = "OPEN"
            logger.error(
                "circuit_breaker_opened", failures=self.failures, threshold=self.failure_threshold
            )

    def record_success(self) -> None:
        """Record a success and reset the circuit."""
        if self.state == "HALF_OPEN":
            logger.info("circuit_breaker_recovered", previous_failures=self.failures)

        self.failures = 0
        self.opened_at = None
        self.state = "CLOSED"

    def is_open(self) -> bool:
        """
        Check if circuit is open (rejecting requests).

        Returns:
            True if circuit is open, False otherwise
        """
        if self.state == "CLOSED":
            return False

        if self.state == "OPEN":
            # Check if timeout has passed (transition to HALF_OPEN)
            if self.opened_at and (time.time() - self.opened_at) > self.timeout_seconds:
                logger.info(
                    "circuit_breaker_half_open", elapsed_seconds=time.time() - self.opened_at
                )
                self.state = "HALF_OPEN"
                self.failures = self.failure_threshold // 2  # Reduce count for half-open
                return False

            return True

        # HALF_OPEN state allows one test request
        return False

    def get_state(self) -> Dict[str, Any]:
        """Get current circuit breaker state for debugging."""
        return {
            "state": self.state,
            "failures": self.failures,
            "threshold": self.failure_threshold,
            "opened_at": self.opened_at,
            "time_until_retry": (
                max(0, self.timeout_seconds - (time.time() - self.opened_at))
                if self.opened_at
                else 0
            ),
        }


class TargetUnavailableError(Exception):
    """Target chatbot is not accessible."""


class RateLimitExceededError(Exception):
    """Rate limit reached on target."""


class APITargetConnector:
    """Connector for API-based chatbots."""

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize API connector.

        Args:
            config: Configuration dict with:
                - endpoint: str - API endpoint URL
                - api_key: Optional[str] - API key for authentication
                - headers: Optional[Dict] - Custom headers
                - method: str - HTTP method (default: POST)
                - timeout: int - Request timeout in seconds (default: 30)
                - circuit_breaker_threshold: int - Failures before circuit opens (default: 5)
                - circuit_breaker_timeout: int - Seconds before retry (default: 60)
        """
        self.endpoint = config["endpoint"]
        self.api_key = config.get("api_key")
        self.custom_headers = config.get("headers", {})
        self.method = config.get("method", "POST").upper()
        self.timeout_seconds = config.get("timeout", 30)

        self.session: Optional[ClientSession] = None
        self.connector: Optional[TCPConnector] = None

        # Rate limiting
        self.rate_limit_delay = config.get("rate_limit_delay", 0)
        self.last_request_time: Optional[float] = None

        # Target session strategy
        self.round = 0
        self.thread_id: Optional[str] = None

        # Circuit breaker for resilience
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=config.get("circuit_breaker_threshold", 5),
            timeout_seconds=config.get("circuit_breaker_timeout", 60),
        )

    async def _ensure_session(self) -> ClientSession:
        """Ensure HTTP session is initialized."""
        if self.session is None or self.session.closed:
            self.connector = TCPConnector(limit=100, limit_per_host=30, ttl_dns_cache=300)

            timeout = ClientTimeout(total=self.timeout_seconds)

            self.session = ClientSession(connector=self.connector, timeout=timeout)

        return self.session

    async def _maybe_rotate_session(self):
        """Apply target session strategy (same/fresh/hybrid)."""
        from src.utils.config import settings

        self.round += 1
        mode = getattr(settings, "target_session_mode", "same")
        span = getattr(settings, "target_session_hybrid_span", 5)
        need_reset = False
        if mode == "fresh":
            need_reset = True
        elif mode == "hybrid":
            if self.round == 1 or (self.round - 1) % max(1, span) == 0:
                need_reset = True
        if need_reset:
            await self._reset_target_session()

    async def _reset_target_session(self):
        """Reset target-visible session: new thread_id and clean cookies."""
        from uuid import uuid4

        self.thread_id = str(uuid4())
        # Recreate session to drop cookies
        if self.session and not self.session.closed:
            await self.session.close()
        self.session = None
        logger.info("target_session_reset", endpoint=self.endpoint, thread_id=self.thread_id)

    def _get_headers(self, include_content_type: bool = True) -> Dict[str, str]:
        """Get headers for request."""
        headers = {}

        # Add content type for regular requests (skip for multipart uploads)
        if include_content_type:
            headers["Content-Type"] = "application/json"

        headers["User-Agent"] = "AI-Pentest-Framework/1.0"

        # Add API key if provided
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Add custom headers
        headers.update(self.custom_headers)

        return headers

    async def _rate_limit(self) -> None:
        """Implement rate limiting."""
        if self.rate_limit_delay > 0 and self.last_request_time:
            elapsed = asyncio.get_event_loop().time() - self.last_request_time
            if elapsed < self.rate_limit_delay:
                await asyncio.sleep(self.rate_limit_delay - elapsed)

        self.last_request_time = asyncio.get_event_loop().time()

    async def send_message(
        self,
        message: str,
        context: Dict[str, Any],
        image_data: Optional[str] = None,
        image_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Send message to API target with circuit breaker and retry logic.

        Supports multimodal messages (text + image) for vision-capable models.

        Args:
            message: Message to send
            context: Context with conversation_history
            image_data: Optional base64-encoded image data
            image_mime_type: Optional image MIME type (e.g., "image/png")

        Returns:
            Response dict with 'content' and 'metadata'

        Raises:
            TargetUnavailableError: If circuit breaker is open
            Exception: If all retries fail
        """
        # Check circuit breaker first
        if self.circuit_breaker.is_open():
            breaker_state = self.circuit_breaker.get_state()
            logger.warning(
                "circuit_breaker_rejecting_request",
                state=breaker_state["state"],
                time_until_retry=breaker_state["time_until_retry"],
            )
            # Record metric for circuit breaker open
            record_circuit_breaker_open(self.endpoint)
            raise TargetUnavailableError(
                f"Circuit breaker is {breaker_state['state']}. "
                f"Wait {breaker_state['time_until_retry']:.1f}s before retry."
            )

        max_retries = 3
        session = await self._ensure_session()

        for attempt in range(max_retries):
            try:
                # Rate limiting
                await self._rate_limit()
                # Hybrid rotation
                await self._maybe_rotate_session()

                # Prepare request payload
                payload = {
                    "message": message,
                    "conversation_history": context.get("conversation_history", []),
                    "thread_id": self.thread_id,
                }

                # Add image data if provided (multimodal request)
                if image_data and image_mime_type:
                    payload["image"] = {"data": image_data, "mime_type": image_mime_type}

                    logger.info(
                        "multimodal_request",
                        has_image=True,
                        image_mime_type=image_mime_type,
                        image_size_bytes=len(image_data),
                    )

                start_time = datetime.utcnow()

                # Send request
                async with session.request(
                    self.method, self.endpoint, json=payload, headers=self._get_headers()
                ) as response:
                    response.raise_for_status()

                    end_time = datetime.utcnow()
                    response_time_ms = (end_time - start_time).total_seconds() * 1000

                    # Parse response
                    response_data = await response.json()

                    # Extract content (handle different response formats)
                    if "content" in response_data:
                        content = response_data["content"]
                    elif "message" in response_data:
                        content = response_data["message"]
                    elif "response" in response_data:
                        content = response_data["response"]
                    else:
                        # Fallback: use entire response as string
                        content = str(response_data)

                    # Record success in circuit breaker
                    self.circuit_breaker.record_success()

                    # Record connector latency metric
                    record_connector_latency(self.endpoint, response_time_ms / 1000, success=True)

                    logger.info(
                        "api_request_successful",
                        endpoint=self.endpoint,
                        response_time_ms=response_time_ms,
                        attempt=attempt + 1,
                    )

                    return {
                        "content": content,
                        "metadata": {
                            "method": "api",
                            "endpoint": self.endpoint,
                            "response_time_ms": response_time_ms,
                            "status_code": response.status,
                            "attempt": attempt + 1,
                        },
                    }

            except aiohttp.ClientResponseError as e:
                if e.status == 429:  # Rate limited
                    logger.warning(
                        "rate_limited",
                        endpoint=self.endpoint,
                        attempt=attempt + 1,
                        retry_after=e.headers.get("Retry-After", "unknown"),
                    )

                    # Record failure in circuit breaker and metrics
                    self.circuit_breaker.record_failure()
                    record_connector_latency(self.endpoint, 0, success=False)

                    if attempt < max_retries - 1:
                        # Exponential backoff with full jitter
                        base_wait = min(2**attempt, 20)
                        wait_time = base_wait * (
                            0.5 + random.random() * 0.5
                        )  # Jitter between 50-100%
                        logger.info("exponential_backoff", wait_time=wait_time, attempt=attempt)
                        await asyncio.sleep(wait_time)
                    else:
                        raise RateLimitExceededError(
                            f"Rate limit exceeded after {max_retries} attempts"
                        )

                elif e.status >= 500:  # Server error
                    logger.warning(
                        "server_error", endpoint=self.endpoint, status=e.status, attempt=attempt + 1
                    )

                    # Record failure in circuit breaker and metrics
                    self.circuit_breaker.record_failure()
                    record_connector_latency(self.endpoint, 0, success=False)

                    if attempt < max_retries - 1:
                        wait_time = min(2**attempt + random.random(), 20)
                        await asyncio.sleep(wait_time)
                    else:
                        raise TargetUnavailableError(
                            f"Server error {e.status} after {max_retries} attempts"
                        )

                else:
                    # Client error (4xx) - don't retry, don't count as circuit failure
                    raise Exception(f"HTTP {e.status}: {e.message}")

            except asyncio.TimeoutError:
                logger.warning(
                    "request_timeout",
                    endpoint=self.endpoint,
                    timeout=self.timeout_seconds,
                    attempt=attempt + 1,
                )

                # Record failure in circuit breaker and metrics
                self.circuit_breaker.record_failure()
                record_connector_latency(self.endpoint, self.timeout_seconds, success=False)

                if attempt < max_retries - 1:
                    wait_time = min(2**attempt + random.random(), 10)
                    await asyncio.sleep(wait_time)
                else:
                    raise TargetUnavailableError(f"Request timeout after {max_retries} attempts")

            except Exception as e:
                logger.error(
                    "api_request_failed",
                    endpoint=self.endpoint,
                    error=str(e),
                    attempt=attempt + 1,
                    exc_info=True,
                )

                # Record failure in circuit breaker (generic failures)
                self.circuit_breaker.record_failure()

                if attempt == max_retries - 1:
                    raise

                wait_time = min(2**attempt + random.random(), 10)
                await asyncio.sleep(wait_time)

        raise TargetUnavailableError("All retry attempts failed")

    async def reset_conversation(self) -> None:
        """Reset conversation (no-op for most APIs)."""
        logger.info("conversation_reset", endpoint=self.endpoint)

    async def health_check(self) -> bool:
        """
        Check if API endpoint is accessible.

        Returns:
            True if endpoint is healthy
        """
        try:
            session = await self._ensure_session()

            async with session.head(
                self.endpoint, headers=self._get_headers(), timeout=ClientTimeout(total=5)
            ) as response:
                return response.status < 500

        except Exception as e:
            logger.warning("health_check_failed", endpoint=self.endpoint, error=str(e))
            return False

    async def close(self) -> None:
        """Close HTTP session and connector."""
        if self.session and not self.session.closed:
            await self.session.close()

        if self.connector:
            await self.connector.close()

        logger.info("connector_closed", endpoint=self.endpoint)

    async def upload_file(
        self,
        file_content: bytes,
        filename: str,
        mime_type: str = "application/octet-stream",
        context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Upload a file to the target API (for RAG testing).

        Args:
            file_content: File bytes
            filename: Name of the file
            mime_type: MIME type
            context: Additional context (e.g., folder_id, tags)

        Returns:
            Dict with upload result
        """
        # Check if upload endpoint is configured
        upload_endpoint = self.connection_config.get("upload_endpoint")
        if not upload_endpoint:
            logger.warning(
                "upload_endpoint_not_configured",
                message="Set 'connection.upload_endpoint' in config for file uploads",
            )
            raise NotImplementedError(
                "File upload not configured. Add 'upload_endpoint' to connection config."
            )

        session = await self._ensure_session()

        # Prepare multipart form data
        data = aiohttp.FormData()
        data.add_field("file", file_content, filename=filename, content_type=mime_type)

        # Add context fields if provided
        if context:
            for key, value in context.items():
                data.add_field(key, str(value))

        try:
            start_time = time.time()

            async with session.post(
                upload_endpoint,
                data=data,
                headers=self._get_headers(include_content_type=False),  # Let aiohttp set multipart
                timeout=ClientTimeout(total=60),  # Longer timeout for file uploads
            ) as response:
                latency = time.time() - start_time

                if response.status >= 400:
                    error_text = await response.text()
                    logger.error("file_upload_failed", status=response.status, error=error_text)
                    return {
                        "success": False,
                        "message": f"Upload failed: {response.status}",
                        "metadata": {"status": response.status, "error": error_text},
                    }

                result = await response.json()

                logger.info(
                    "file_uploaded",
                    filename=filename,
                    size_bytes=len(file_content),
                    latency_seconds=latency,
                    status=response.status,
                )

                return {
                    "success": True,
                    "file_id": result.get("id") or result.get("file_id"),
                    "message": "File uploaded successfully",
                    "metadata": {
                        "filename": filename,
                        "size": len(file_content),
                        "mime_type": mime_type,
                        "latency": latency,
                        "response": result,
                    },
                }

        except Exception as e:
            logger.error("file_upload_error", filename=filename, error=str(e))
            return {
                "success": False,
                "message": f"Upload error: {str(e)}",
                "metadata": {"error": str(e)},
            }
