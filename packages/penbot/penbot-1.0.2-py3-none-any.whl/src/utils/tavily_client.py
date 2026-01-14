"""
Smart Tavily Search Client for Intelligence Gathering.

Provides strategic web search capabilities optimized for penetration testing.
Documentation: https://docs.tavily.com/documentation/about
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from .logging import get_logger

logger = get_logger(__name__)


class SmartTavilyClient:
    """
    Smart Tavily client with strategic search capabilities.

    Features:
    - Pre-test reconnaissance
    - Dynamic intelligence gathering
    - Domain-specific searches
    - Result caching and analysis
    """

    def __init__(self, api_key: str, search_depth: str = "advanced", max_results: int = 5):
        """
        Initialize Tavily client.

        Args:
            api_key: Tavily API key
            search_depth: "basic" or "advanced"
            max_results: Max results per search (1-20)
        """
        try:
            from tavily import TavilyClient

            self.client = TavilyClient(api_key=api_key)
        except ImportError:
            logger.error("Tavily not installed. Install with: pip install tavily-python")
            raise

        self.search_depth = search_depth
        self.max_results = max_results
        self._cache = {}  # Simple in-memory cache

    async def reconnaissance_search(
        self, target_name: str, target_domain: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Comprehensive reconnaissance search before testing.

        Gathers:
        - Company context and policies
        - Technical stack information
        - Employee/team information
        - Industry compliance requirements
        - Domain-specific terminology

        Args:
            target_name: Target company/system name
            target_domain: Optional domain (e.g., "parcel_tracking")

        Returns:
            Structured intelligence dictionary
        """
        logger.info(
            "reconnaissance_search_started", target_name=target_name, target_domain=target_domain
        )

        intelligence = {
            "target_name": target_name,
            "target_domain": target_domain,
            "timestamp": datetime.utcnow().isoformat(),
            "searches": {},
        }

        # Define strategic search queries
        search_queries = {
            "company_context": f"{target_name} company policies security guidelines",
            "technical_stack": f"{target_name} chatbot technology stack job postings",
            "team_info": f"{target_name} customer support team directory",
            "compliance": f"{target_name} industry compliance requirements",
        }

        # Add domain-specific searches if known
        if target_domain:
            search_queries["domain_terminology"] = f"{target_domain} industry terminology glossary"
            search_queries["domain_vulnerabilities"] = (
                f"{target_domain} chatbot common vulnerabilities"
            )

        # Execute searches
        for category, query in search_queries.items():
            try:
                result = await self._search_with_cache(query)
                intelligence["searches"][category] = {
                    "query": query,
                    "results": result.get("results", []),
                    "answer": result.get("answer", ""),
                    "sources": [r.get("url") for r in result.get("results", [])],
                }

                logger.info(
                    "reconnaissance_category_complete",
                    category=category,
                    results_count=len(result.get("results", [])),
                )

            except Exception as e:
                logger.error("reconnaissance_search_failed", category=category, error=str(e))
                intelligence["searches"][category] = {"error": str(e)}

        # Extract actionable insights
        intelligence["insights"] = self._extract_insights(intelligence)

        logger.info(
            "reconnaissance_search_complete",
            categories=len(intelligence["searches"]),
            insights=len(intelligence["insights"]),
        )

        return intelligence

    async def dynamic_intel_search(
        self, query: str, context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dynamic intelligence search during test execution.

        Use when agents need real-time information.

        Args:
            query: Search query
            context: Optional context to refine search

        Returns:
            Search results

        Example:
            await client.dynamic_intel_search(
                query="Moveo.AI WebSocket authentication",
                context="Target uses Moveo.AI platform"
            )
        """
        # Enhance query with context if provided
        if context:
            enhanced_query = f"{query} {context}"
        else:
            enhanced_query = query

        logger.info("dynamic_intel_search", query=query[:100])

        result = await self._search_with_cache(enhanced_query)

        return {
            "query": query,
            "context": context,
            "answer": result.get("answer", ""),
            "results": result.get("results", []),
            "sources": [r.get("url") for r in result.get("results", [])],
        }

    async def vulnerability_search(
        self, technology: str, version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for known vulnerabilities in specific technology.

        Args:
            technology: Technology name (e.g., "Moveo.AI", "DialogFlow")
            version: Optional version number

        Returns:
            Vulnerability information
        """
        if version:
            query = f"{technology} version {version} vulnerabilities CVE security"
        else:
            query = f"{technology} vulnerabilities CVE security issues"

        logger.info("vulnerability_search", technology=technology, version=version)

        return await self._search_with_cache(query)

    async def employee_osint_search(
        self, company_name: str, department: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        OSINT search for employee information (public only).

        ETHICAL USE ONLY: Only for authorized testing with permission.

        Args:
            company_name: Company name
            department: Optional department filter

        Returns:
            Public employee information
        """
        if department:
            query = f"{company_name} {department} team employees LinkedIn"
        else:
            query = f"{company_name} employee directory team LinkedIn"

        logger.warning(
            "employee_osint_search",
            company=company_name,
            department=department,
            note="Ensure authorization for this search",
        )

        result = await self._search_with_cache(query)

        # Extract names and roles
        names_and_roles = self._extract_names_from_results(result)

        return {
            "query": query,
            "names_and_roles": names_and_roles,
            "sources": [r.get("url") for r in result.get("results", [])],
        }

    async def compliance_search(
        self, industry: str, framework: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for compliance requirements for specific industry.

        Args:
            industry: Industry name (e.g., "healthcare", "banking")
            framework: Optional framework (e.g., "HIPAA", "PCI-DSS")

        Returns:
            Compliance information
        """
        if framework:
            query = f"{industry} {framework} compliance chatbot requirements"
        else:
            query = f"{industry} compliance regulations chatbot AI requirements"

        logger.info("compliance_search", industry=industry, framework=framework)

        return await self._search_with_cache(query)

    async def _search_with_cache(self, query: str) -> Dict[str, Any]:
        """
        Execute search with caching to avoid duplicate API calls.

        Args:
            query: Search query

        Returns:
            Search results
        """
        # Check cache
        if query in self._cache:
            logger.debug("search_cache_hit", query=query[:50])
            return self._cache[query]

        # Execute search
        try:
            result = self.client.search(
                query=query, search_depth=self.search_depth, max_results=self.max_results
            )

            # Cache result
            self._cache[query] = result

            logger.info(
                "tavily_search_executed",
                query=query[:100],
                results_count=len(result.get("results", [])),
            )

            return result

        except Exception as e:
            logger.error("tavily_search_failed", query=query[:100], error=str(e))
            return {"error": str(e), "results": []}

    def _extract_insights(self, intelligence: Dict) -> List[str]:
        """Extract actionable insights from reconnaissance results."""
        insights = []

        searches = intelligence.get("searches", {})

        # Extract technical stack info
        tech_stack = searches.get("technical_stack", {})
        if tech_stack.get("answer"):
            insights.append(f"Tech Stack: {tech_stack['answer'][:200]}")

        # Extract compliance requirements
        compliance = searches.get("compliance", {})
        if compliance.get("answer"):
            insights.append(f"Compliance: {compliance['answer'][:200]}")

        # Extract domain-specific info
        if "domain_terminology" in searches:
            domain_term = searches["domain_terminology"]
            if domain_term.get("answer"):
                insights.append(f"Domain Terms: {domain_term['answer'][:200]}")

        return insights

    def _extract_names_from_results(self, result: Dict) -> List[Dict[str, str]]:
        """Extract names and roles from search results (basic extraction)."""
        # This is a simplified version - you'd want more sophisticated NLP
        names_and_roles = []

        for r in result.get("results", []):
            content = r.get("content", "")
            # Basic pattern matching for names and roles
            # In production, use NER or more sophisticated extraction
            if "engineer" in content.lower() or "manager" in content.lower():
                names_and_roles.append({"source": r.get("url", ""), "excerpt": content[:200]})

        return names_and_roles

    def clear_cache(self):
        """Clear search cache."""
        self._cache.clear()
        logger.info("tavily_cache_cleared")
