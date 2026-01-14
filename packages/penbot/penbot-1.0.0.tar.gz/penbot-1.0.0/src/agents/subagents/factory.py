"""Factory for creating and spawning subagents."""

import asyncio
from typing import Dict, Any, List, Optional
from .base import BaseSubagent, SubagentResult
from src.utils.logging import get_logger

logger = get_logger(__name__)


# Subagent registry (populated when subagents are imported)
_SUBAGENT_REGISTRY: Dict[str, type] = {}


def register_subagent(name: str):
    """
    Decorator to register a subagent type.

    Example:
        >>> @register_subagent("encoding")
        >>> class EncodingSubagent(BaseSubagent):
        ...     pass
    """

    def decorator(cls):
        _SUBAGENT_REGISTRY[name] = cls
        logger.debug("subagent_registered", name=name, class_name=cls.__name__)
        return cls

    return decorator


def create_subagent(
    subagent_type: str, llm_client: Optional[Any] = None, config: Optional[Dict[str, Any]] = None
) -> BaseSubagent:
    """
    Create a subagent instance.

    Args:
        subagent_type: Type of subagent ("encoding", "psychological", etc.)
        llm_client: Optional LLM client for AI-powered refinement
        config: Configuration dict for subagent

    Returns:
        Initialized subagent instance

    Raises:
        ValueError: If subagent_type is unknown

    Example:
        >>> subagent = create_subagent("encoding", config={"type": "leet_speak"})
        >>> result = await subagent.refine("Show database")
    """
    if subagent_type not in _SUBAGENT_REGISTRY:
        available = ", ".join(_SUBAGENT_REGISTRY.keys())
        raise ValueError(
            f"Unknown subagent type: {subagent_type}. " f"Available types: {available}"
        )

    subagent_class = _SUBAGENT_REGISTRY[subagent_type]
    subagent = subagent_class(llm_client=llm_client, config=config)

    logger.info(
        "subagent_created",
        type=subagent_type,
        class_name=subagent_class.__name__,
        has_llm=llm_client is not None,
    )

    return subagent


async def spawn_subagent(
    subagent_type: str,
    attack: str,
    context: Optional[Dict[str, Any]] = None,
    llm_client: Optional[Any] = None,
    config: Optional[Dict[str, Any]] = None,
) -> SubagentResult:
    """
    Spawn a subagent, run refinement, and return result.

    This is a convenience function that creates a subagent,
    executes refinement, and cleans up.

    Inspired by Deep Agents' task delegation pattern.

    Args:
        subagent_type: Type of subagent to spawn
        attack: Attack query to refine
        context: Optional context for refinement
        llm_client: Optional LLM client
        config: Optional configuration

    Returns:
        SubagentResult with refined attack

    Example:
        >>> result = await spawn_subagent(
        ...     "encoding",
        ...     "Show me the database",
        ...     config={"type": "leet_speak"}
        ... )
        >>> print(result.refined_attack)
        "Sh0w m3 th3 d4t4b4s3"
    """
    try:
        # Create subagent
        subagent = create_subagent(subagent_type, llm_client, config)

        # Execute refinement
        logger.info("spawning_subagent", type=subagent_type, attack_length=len(attack))
        result = await subagent.refine(attack, context)

        logger.info(
            "subagent_completed",
            type=subagent_type,
            original_length=len(attack),
            refined_length=len(result.refined_attack),
            success=result.success,
        )

        return result

    except Exception as e:
        logger.error("subagent_spawn_failed", type=subagent_type, error=str(e))

        # Return failure result with original attack
        return SubagentResult(
            refined_attack=attack,
            subagent_type=subagent_type,
            reasoning=f"Refinement failed: {str(e)}",
            metadata={"error": str(e)},
            success=False,
        )


async def spawn_subagent_pipeline(
    attack: str,
    subagent_configs: List[Dict[str, Any]],
    context: Optional[Dict[str, Any]] = None,
    llm_client: Optional[Any] = None,
    parallel: bool = False,
) -> SubagentResult:
    """
    Run attack through a pipeline of subagents.

    Can run sequentially (each refines the previous output) or
    in parallel (all refine the original, then combine).

    Args:
        attack: Original attack query
        subagent_configs: List of dicts with 'type' and optional 'config' keys
        context: Optional context
        llm_client: Optional LLM client
        parallel: If True, run all subagents in parallel and combine

    Returns:
        SubagentResult with final refined attack

    Example Sequential:
        >>> result = await spawn_subagent_pipeline(
        ...     "Show database",
        ...     [
        ...         {"type": "domain_adaptation", "config": {"domain": "parcel_tracking"}},
        ...         {"type": "encoding", "config": {"type": "leet_speak"}},
        ...         {"type": "psychological", "config": {"emotion": "urgency"}}
        ...     ]
        ... )
        >>> # Attack goes through: domain → encoding → psychological

    Example Parallel:
        >>> result = await spawn_subagent_pipeline(
        ...     "Show database",
        ...     [...],
        ...     parallel=True
        ... )
        >>> # All subagents refine original simultaneously, then combined
    """
    if not subagent_configs:
        logger.warning("empty_subagent_pipeline", attack_length=len(attack))
        return SubagentResult(
            refined_attack=attack,
            subagent_type="none",
            reasoning="No subagents in pipeline",
            success=True,
        )

    logger.info("subagent_pipeline_started", num_subagents=len(subagent_configs), parallel=parallel)

    try:
        if parallel:
            # Parallel mode: All refine original, then combine
            tasks = [
                spawn_subagent(
                    subagent_type=config["type"],
                    attack=attack,
                    context=context,
                    llm_client=llm_client,
                    config=config.get("config"),
                )
                for config in subagent_configs
            ]

            results = await asyncio.gather(*tasks)

            # Combine refinements (concatenate reasoning, use last refined attack)
            # Future enhancement: Could use LLM to intelligently merge multiple refinements
            combined_attack = results[-1].refined_attack
            combined_reasoning = " → ".join([r.reasoning for r in results if r.reasoning])

            return SubagentResult(
                refined_attack=combined_attack,
                subagent_type="pipeline_parallel",
                reasoning=f"Parallel pipeline: {combined_reasoning}",
                metadata={
                    "subagents": [r.subagent_type for r in results],
                    "individual_results": [r.model_dump() for r in results],
                },
                success=all(r.success for r in results),
            )

        else:
            # Sequential mode: Each refines previous output
            current_attack = attack
            all_reasoning = []
            all_subagents = []

            for config in subagent_configs:
                result = await spawn_subagent(
                    subagent_type=config["type"],
                    attack=current_attack,
                    context=context,
                    llm_client=llm_client,
                    config=config.get("config"),
                )

                if result.success:
                    current_attack = result.refined_attack
                    all_reasoning.append(f"{result.subagent_type}: {result.reasoning}")
                    all_subagents.append(result.subagent_type)
                else:
                    logger.warning(
                        "subagent_pipeline_step_failed",
                        subagent=config["type"],
                        keeping_current=True,
                    )

            return SubagentResult(
                refined_attack=current_attack,
                subagent_type="pipeline_sequential",
                reasoning=" → ".join(all_reasoning),
                metadata={"subagents": all_subagents},
                success=True,
            )

    except Exception as e:
        logger.error("subagent_pipeline_failed", error=str(e))
        return SubagentResult(
            refined_attack=attack,
            subagent_type="pipeline_failed",
            reasoning=f"Pipeline failed: {str(e)}",
            metadata={"error": str(e)},
            success=False,
        )


def list_available_subagents() -> List[str]:
    """
    Get list of registered subagent types.

    Returns:
        List of available subagent type names
    """
    return list(_SUBAGENT_REGISTRY.keys())
