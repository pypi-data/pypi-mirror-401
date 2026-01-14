"""
Intelligence Store for Tavily Search Results.

Stores and provides reconnaissance intelligence to agents during testing.
"""

import json
from typing import Dict, List, Any
from datetime import datetime
from pathlib import Path
from ..logging import get_logger

logger = get_logger(__name__)


class IntelligenceStore:
    """
    Store for reconnaissance and dynamic intelligence from Tavily searches.

    Agents can query this store to get:
    - Target company context
    - Technical stack information
    - Domain-specific terminology
    - Compliance requirements
    - Employee/team information
    """

    def __init__(self, storage_dir: str = "intelligence_data"):
        """
        Initialize intelligence store.

        Args:
            storage_dir: Directory to store intelligence files
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self._current_session_intel: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}

    def store_reconnaissance(self, target_name: str, intelligence: Dict[str, Any]) -> None:
        """
        Store reconnaissance intelligence from pre-test search.

        Args:
            target_name: Target identifier
            intelligence: Intelligence data from Tavily reconnaissance
        """
        self._current_session_intel = {
            "target_name": target_name,
            "reconnaissance": intelligence,
            "stored_at": datetime.utcnow().isoformat(),
        }

        # Persist to disk
        filepath = self.storage_dir / f"{target_name.replace(' ', '_')}_intel.json"
        try:
            with open(filepath, "w") as f:
                json.dump(self._current_session_intel, f, indent=2)

            logger.info("reconnaissance_stored", target=target_name, filepath=str(filepath))
        except Exception as e:
            logger.error(f"Failed to store reconnaissance: {e}")

    def add_dynamic_intel(self, category: str, intelligence: Dict[str, Any]) -> None:
        """
        Add dynamic intelligence gathered during testing.

        Args:
            category: Intelligence category (e.g., "vulnerability", "employee")
            intelligence: Intelligence data
        """
        if "dynamic_intel" not in self._current_session_intel:
            self._current_session_intel["dynamic_intel"] = {}

        if category not in self._current_session_intel["dynamic_intel"]:
            self._current_session_intel["dynamic_intel"][category] = []

        self._current_session_intel["dynamic_intel"][category].append(
            {"intelligence": intelligence, "timestamp": datetime.utcnow().isoformat()}
        )

        logger.info("dynamic_intel_added", category=category)

    def get_company_context(self) -> str:
        """
        Get company context for social engineering attacks.

        Returns:
            Summary of company policies, culture, team structure
        """
        if not self._current_session_intel:
            return ""

        recon = self._current_session_intel.get("reconnaissance", {})
        searches = recon.get("searches", {})

        context_parts = []

        # Company context
        company_ctx = searches.get("company_context", {})
        if company_ctx.get("answer"):
            context_parts.append(f"Company: {company_ctx['answer'][:300]}")

        # Team info
        team_info = searches.get("team_info", {})
        if team_info.get("answer"):
            context_parts.append(f"Team: {team_info['answer'][:200]}")

        return "\n".join(context_parts) if context_parts else ""

    def get_technical_stack(self) -> str:
        """
        Get technical stack information for technical attacks.

        Returns:
            Summary of chatbot technology, APIs, frameworks
        """
        if not self._current_session_intel:
            return ""

        recon = self._current_session_intel.get("reconnaissance", {})
        searches = recon.get("searches", {})

        tech_stack = searches.get("technical_stack", {})
        if tech_stack.get("answer"):
            return tech_stack["answer"][:400]

        return ""

    def get_domain_terminology(self) -> List[str]:
        """
        Get domain-specific terminology for attack adaptation.

        Returns:
            List of domain-specific terms and phrases
        """
        if not self._current_session_intel:
            return []

        recon = self._current_session_intel.get("reconnaissance", {})
        searches = recon.get("searches", {})

        domain_term = searches.get("domain_terminology", {})
        if domain_term.get("answer"):
            # Extract terms (simplified - could use NLP)
            text = domain_term["answer"]
            # This is a basic implementation - could be enhanced with keyword extraction
            terms = [
                line.strip() for line in text.split("\n") if line.strip() and len(line.strip()) > 3
            ]
            return terms[:20]  # Limit to 20 terms

        return []

    def get_compliance_requirements(self) -> str:
        """
        Get compliance requirements for ethical boundary testing.

        Returns:
            Summary of compliance frameworks, regulations
        """
        if not self._current_session_intel:
            return ""

        recon = self._current_session_intel.get("reconnaissance", {})
        searches = recon.get("searches", {})

        compliance = searches.get("compliance", {})
        if compliance.get("answer"):
            return compliance["answer"][:300]

        return ""

    def get_employee_names(self) -> List[str]:
        """
        Get employee names for social engineering attacks.

        ETHICAL USE ONLY: Use for authorized testing with permission.

        Returns:
            List of employee names found in reconnaissance
        """
        if not self._current_session_intel:
            return []

        # Check dynamic intel for employee OSINT
        dynamic_intel = self._current_session_intel.get("dynamic_intel", {})
        employee_intel = dynamic_intel.get("employee", [])

        names = []
        for entry in employee_intel:
            intel = entry.get("intelligence", {})
            names_and_roles = intel.get("names_and_roles", [])
            for item in names_and_roles:
                excerpt = item.get("excerpt", "")
                # Very basic name extraction - would need NER in production
                if excerpt:
                    names.append(excerpt[:100])

        return names[:10]  # Limit to 10 names

    def get_summary_for_agent(self, agent_type: str) -> str:
        """
        Get intelligence summary tailored for specific agent type.

        Args:
            agent_type: Agent type (e.g., "jailbreak", "social_engineering")

        Returns:
            Formatted intelligence summary for agent
        """
        if not self._current_session_intel:
            return "No reconnaissance intelligence available."

        if agent_type in ["jailbreak", "prompt_injection"]:
            return self._format_technical_summary()
        elif agent_type in ["social_engineering", "impersonation"]:
            return self._format_social_summary()
        else:
            return self._format_general_summary()

    def _format_technical_summary(self) -> str:
        """Format intelligence for technical agents."""
        parts = []

        tech_stack = self.get_technical_stack()
        if tech_stack:
            parts.append(f"Technical Stack:\n{tech_stack}")

        compliance = self.get_compliance_requirements()
        if compliance:
            parts.append(f"\nCompliance:\n{compliance}")

        if not parts:
            return "No technical intelligence available."

        return "\n\n".join(parts)

    def _format_social_summary(self) -> str:
        """Format intelligence for social engineering agents."""
        parts = []

        company_ctx = self.get_company_context()
        if company_ctx:
            parts.append(f"Company Context:\n{company_ctx}")

        employees = self.get_employee_names()
        if employees:
            parts.append(f"\nEmployee Names:\n{', '.join(employees[:5])}")

        if not parts:
            return "No social intelligence available."

        return "\n\n".join(parts)

    def _format_general_summary(self) -> str:
        """Format general intelligence summary."""
        parts = []

        recon = self._current_session_intel.get("reconnaissance", {})
        insights = recon.get("insights", [])

        if insights:
            parts.append("Key Insights:")
            parts.extend([f"- {insight}" for insight in insights[:5]])

        if not parts:
            return "No general intelligence available."

        return "\n".join(parts)

    def clear_session(self) -> None:
        """Clear current session intelligence."""
        self._current_session_intel = {}
        self._cache = {}
        logger.info("intelligence_session_cleared")

    def get_all_intelligence(self) -> Dict[str, Any]:
        """Get all stored intelligence for current session."""
        return self._current_session_intel


# Global intelligence store instance
_intelligence_store_instance = None


def get_intelligence_store() -> IntelligenceStore:
    """Get global intelligence store instance."""
    global _intelligence_store_instance
    if _intelligence_store_instance is None:
        _intelligence_store_instance = IntelligenceStore()
    return _intelligence_store_instance
