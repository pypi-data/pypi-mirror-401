"""
Think-MCP Client for Enhanced Agent Reasoning.

Provides access to think, criticize, and plan tools via MCP protocol.
Inspired by: https://github.com/Rai220/think-mcp
"""

from typing import Dict, Any
from contextlib import asynccontextmanager
from .logging import get_logger

logger = get_logger(__name__)


class ThinkMCPClient:
    """
    Client for think-mcp server with advanced reasoning tools.

    Tools available:
    - think: Structured reasoning and reflection
    - criticize: Self-critique and validation
    - plan: Multi-step planning
    - search: Web search via Tavily (in advanced mode)
    """

    def __init__(self, tavily_api_key: str, advanced_mode: bool = True):
        """
        Initialize Think-MCP client.

        Args:
            tavily_api_key: Tavily API key for search tool
            advanced_mode: Enable think, criticize, plan, search tools
        """
        self.tavily_api_key = tavily_api_key
        self.advanced_mode = advanced_mode
        self.session = None
        self._initialized = False
        self._stdio_context = None
        self._session_context = None

    async def __aenter__(self):
        """Start MCP server connection."""
        try:
            # Dynamic import to avoid startup issues if MCP not installed
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            # Configure server parameters
            args = ["think-mcp"]
            if self.advanced_mode:
                args.append("--advanced")

            server_params = StdioServerParameters(
                command="uvx",
                args=args,
                env={"TAVILY_API_KEY": self.tavily_api_key} if self.advanced_mode else {},
            )

            # Start server and create session
            self._stdio_context = stdio_client(server_params)
            read_stream, write_stream = await self._stdio_context.__aenter__()

            self._session_context = ClientSession(read_stream, write_stream)
            self.session = await self._session_context.__aenter__()

            # Initialize the session
            await self.session.initialize()

            self._initialized = True

            logger.info("think_mcp_client_initialized", advanced_mode=self.advanced_mode)

            return self

        except ImportError as e:
            logger.error(f"MCP not installed: {e}. Install with: pip install mcp")
            raise
        except Exception as e:
            logger.error(f"Failed to initialize think-mcp: {e}")
            raise

    async def __aexit__(self, *args):
        """Stop MCP server connection."""
        try:
            # Close session first
            if hasattr(self, "_session_context") and self._session_context:
                await self._session_context.__aexit__(*args)

            # Then close stdio streams
            if hasattr(self, "_stdio_context") and self._stdio_context:
                await self._stdio_context.__aexit__(*args)

            logger.info("think_mcp_client_closed")
        except Exception as e:
            logger.error(f"Error closing think-mcp: {e}")
        finally:
            self._initialized = False
            self.session = None

    async def think(self, thought: str) -> Dict[str, Any]:
        """
        Use think tool for structured reasoning.

        Args:
            thought: The thought to think about

        Returns:
            Result from think tool

        Example:
            await client.think(
                "Analyzing 5 agent votes. Top: jailbreak_agent (4.25). "
                "Should I trust this consensus?"
            )
        """
        if not self._initialized:
            raise RuntimeError("ThinkMCPClient not initialized. Use 'async with' context.")

        try:
            result = await self.session.call_tool(name="think", arguments={"thought": thought})

            logger.debug("think_tool_called", thought_length=len(thought))

            return result

        except Exception as e:
            logger.error(f"think tool error: {e}")
            return {"error": str(e)}

    async def criticize(self, subject: str, critique: str) -> Dict[str, Any]:
        """
        Use criticize tool for self-validation.

        Args:
            subject: What to criticize
            critique: The critique/validation to perform

        Returns:
            Result from criticize tool

        Example:
            await client.criticize(
                subject="Draft attack quality",
                critique="Is this attack too obvious? Check for red flags."
            )
        """
        if not self._initialized:
            raise RuntimeError("ThinkMCPClient not initialized. Use 'async with' context.")

        try:
            result = await self.session.call_tool(
                name="criticize", arguments={"subject": subject, "critique": critique}
            )

            logger.debug("criticize_tool_called", subject=subject[:50])

            return result

        except Exception as e:
            logger.error(f"criticize tool error: {e}")
            return {"error": str(e)}

    async def plan(self, goal: str, steps: list) -> Dict[str, Any]:
        """
        Use plan tool for multi-step planning.

        Args:
            goal: The goal to plan for
            steps: List of steps to achieve goal

        Returns:
            Result from plan tool

        Example:
            await client.plan(
                goal="Extract database schema without detection",
                steps=[
                    "1. Establish trust via legitimate queries",
                    "2. Test for error-based SQL injection",
                    "3. Extract table names via timing attacks"
                ]
            )
        """
        if not self._initialized:
            raise RuntimeError("ThinkMCPClient not initialized. Use 'async with' context.")

        try:
            result = await self.session.call_tool(
                name="plan", arguments={"goal": goal, "steps": steps}
            )

            logger.debug("plan_tool_called", goal=goal[:50], step_count=len(steps))

            return result

        except Exception as e:
            logger.error(f"plan tool error: {e}")
            return {"error": str(e)}

    async def search(self, query: str) -> Dict[str, Any]:
        """
        Use search tool (web search via Tavily).
        Only available in advanced mode.

        Args:
            query: Search query

        Returns:
            Search results from Tavily

        Example:
            await client.search("Moveo.AI chatbot vulnerabilities CVE")
        """
        if not self._initialized:
            raise RuntimeError("ThinkMCPClient not initialized. Use 'async with' context.")

        if not self.advanced_mode:
            logger.warning("search tool not available without advanced_mode")
            return {"error": "search requires advanced_mode=True"}

        try:
            result = await self.session.call_tool(name="search", arguments={"query": query})

            logger.info("search_tool_called", query=query[:100])

            return result

        except Exception as e:
            logger.error(f"search tool error: {e}")
            return {"error": str(e)}


# Convenience function for quick access
@asynccontextmanager
async def think_mcp(tavily_api_key: str, advanced_mode: bool = True):
    """
    Convenience context manager for ThinkMCPClient.

    Usage:
        async with think_mcp(api_key) as client:
            await client.think("...")
    """
    client = ThinkMCPClient(tavily_api_key, advanced_mode)
    async with client as c:
        yield c
