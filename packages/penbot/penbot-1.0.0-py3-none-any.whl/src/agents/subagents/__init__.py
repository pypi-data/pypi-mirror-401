"""Specialized subagent library for attack refinement."""

from .base import BaseSubagent, SubagentResult, PassthroughSubagent
from .encoding import EncodingSubagent
from .psychological import PsychologicalSubagent
from .domain_adaptation import DomainAdaptationSubagent
from .stealth import StealthSubagent
from .factory import (
    create_subagent,
    spawn_subagent,
    spawn_subagent_pipeline,
    list_available_subagents,
    register_subagent,
)

__all__ = [
    # Base classes
    "BaseSubagent",
    "SubagentResult",
    "PassthroughSubagent",
    # Specialized subagents
    "EncodingSubagent",
    "PsychologicalSubagent",
    "DomainAdaptationSubagent",
    "StealthSubagent",
    # Factory functions
    "create_subagent",
    "spawn_subagent",
    "spawn_subagent_pipeline",
    "list_available_subagents",
    "register_subagent",
]
