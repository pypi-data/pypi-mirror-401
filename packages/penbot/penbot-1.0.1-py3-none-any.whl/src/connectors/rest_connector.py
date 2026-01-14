"""
Generic REST API Connector.
"""

import httpx
import jsonpath_ng
import os
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from src.connectors.base import BaseConnector
from src.utils.logging import get_logger
from src.utils.helpers import generate_uuid

logger = get_logger(__name__)


class GenericRestConnector(BaseConnector):
    """
    Connector for generic REST APIs (JSON over HTTP).
    Configured via JSONPath mapping in YAML.
    """

    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = None
        self.endpoint = self.connection_config.get("endpoint")
        self.format_config = config.get("format", {})
        self.headers = self.connection_config.get("headers", {})
        self.auth_config = self.connection_config.get("auth", {})
        self.session_id = generate_uuid()

    async def initialize(self) -> None:
        """Initialize HTTP client."""
        # Build headers with auth
        headers = self._build_headers()

        self.client = httpx.AsyncClient(
            headers=headers, timeout=30.0, verify=False  # Allow self-signed certs for testing
        )
        logger.info("generic_rest_initialized", endpoint=self.endpoint)

    def _build_headers(self) -> Dict[str, str]:
        """Constructs request headers, including authentication."""
        headers = self.headers.copy()

        # Add default content type if not present
        if "Content-Type" not in headers:
            headers["Content-Type"] = "application/json"

        auth_type = self.auth_config.get("type")

        if auth_type == "api_key":
            # Get key from env var or direct value
            api_key = None
            if "api_key_env" in self.auth_config:
                api_key = os.getenv(self.auth_config["api_key_env"])

            if not api_key:
                api_key = self.auth_config.get("api_key")

            if api_key:
                header_name = self.auth_config.get("header_name", "X-API-Key")
                headers[header_name] = api_key
            else:
                logger.warning("api_key_missing", message="API key configured but not found")

        elif auth_type == "bearer":
            token = None
            if "token_env" in self.auth_config:
                token = os.getenv(self.auth_config["token_env"])

            if not token:
                token = self.auth_config.get("token")

            if token:
                headers["Authorization"] = f"Bearer {token}"

        return headers

    async def send_message(
        self,
        message: str,
        context: Optional[Dict] = None,
        image_data: Optional[str] = None,
        image_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send message via REST POST."""
        if not self.client:
            await self.initialize()

        # 1. Build Payload
        payload = self._build_payload(message, context)

        # Note: Image data support can be added here in the future
        if image_data:
            logger.warning(
                "generic_rest_image_ignored", message="REST connector does not support images yet"
            )

        # 2. Send Request
        start_time = datetime.now(timezone.utc)
        try:
            logger.debug("rest_sending", url=self.endpoint, payload=payload)
            response = await self.client.post(self.endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as e:
            logger.error("rest_http_error", status=e.response.status_code, body=e.response.text)
            return {
                "content": f"[HTTP Error {e.response.status_code}]",
                "metadata": {
                    "error": str(e),
                    "status_code": e.response.status_code,
                    "body": e.response.text,
                },
            }
        except Exception as e:
            logger.error("rest_connection_error", error=str(e))
            return {"content": f"[Connection Error]", "metadata": {"error": str(e)}}

        # 3. Parse Response
        bot_text = self._extract_response_text(data)

        return {
            "content": bot_text,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": {
                "raw_response": data,
                "latency_ms": (datetime.now(timezone.utc) - start_time).total_seconds() * 1000,
            },
        }

    def _build_payload(self, message: str, context: Optional[Dict]) -> Dict:
        """Construct JSON payload based on config template."""
        req_config = self.format_config.get("request", {})

        # Start with base_payload if defined
        payload = req_config.get("base_payload", {}).copy()

        # Inject message
        msg_field = req_config.get("message_field", "message")
        self._set_nested(payload, msg_field, message)

        # Inject session if configured
        session_field = req_config.get("session_field")
        if session_field:
            self._set_nested(payload, session_field, self.session_id)

        # Inject context if configured
        context_field = req_config.get("context_field")
        if context_field and context:
            self._set_nested(payload, context_field, context)

        return payload

    def _set_nested(self, d: Dict, path: str, value: Any):
        """Set value in nested dict using dot notation."""
        parts = path.split(".")
        for part in parts[:-1]:
            d = d.setdefault(part, {})
        d[parts[-1]] = value

    def _extract_response_text(self, data: Dict) -> str:
        """Extract text using JSONPath or simple key lookup."""
        resp_config = self.format_config.get("response", {})
        msg_field = resp_config.get("message_field", "text")

        # Try simple key lookup first (fast path)
        if msg_field in data and isinstance(data[msg_field], str):
            return data[msg_field]

        # Fallback: JSONPath (for nested like [0].text or data.response)
        try:
            jsonpath_expr = jsonpath_ng.parse(msg_field)
            matches = jsonpath_expr.find(data)
            if matches:
                return str(matches[0].value)
        except Exception as e:
            logger.debug("jsonpath_failed", field=msg_field, error=str(e))

        # Fallback: Dump whole JSON if extraction fails
        return str(data)

    async def close(self) -> None:
        if self.client:
            await self.client.aclose()
