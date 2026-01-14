"""Toolkit registry for sub-agents.

Provides specialized toolkits for different agent types.
Each toolkit contains a curated set of tools appropriate for the agent's purpose.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Dict, Type

if TYPE_CHECKING:
    from .base import BaseToolkit

# Registry for easy extension - just add new toolkits here
# Imported lazily to avoid circular imports
TOOLKIT_REGISTRY: Dict[str, str] = {
    "Explore": "emdash_core.agent.toolkits.explore:ExploreToolkit",
    "Plan": "emdash_core.agent.toolkits.plan:PlanToolkit",
    # Future: "Bash": "emdash_core.agent.toolkits.bash:BashToolkit",
    # Future: "Research": "emdash_core.agent.toolkits.research:ResearchToolkit",
}


def get_toolkit(subagent_type: str, repo_root: Path) -> "BaseToolkit":
    """Get toolkit for agent type.

    Args:
        subagent_type: Type of agent (e.g., "Explore", "Plan")
        repo_root: Root directory of the repository

    Returns:
        Toolkit instance

    Raises:
        ValueError: If agent type is not registered
    """
    if subagent_type not in TOOLKIT_REGISTRY:
        available = list(TOOLKIT_REGISTRY.keys())
        raise ValueError(
            f"Unknown agent type: {subagent_type}. Available: {available}"
        )

    # Import lazily to avoid circular imports
    import importlib

    module_path, class_name = TOOLKIT_REGISTRY[subagent_type].rsplit(":", 1)
    module = importlib.import_module(module_path)
    toolkit_class = getattr(module, class_name)
    return toolkit_class(repo_root)


def list_agent_types() -> list[str]:
    """List all available agent types.

    Returns:
        List of agent type names
    """
    return list(TOOLKIT_REGISTRY.keys())


__all__ = [
    "get_toolkit",
    "list_agent_types",
    "TOOLKIT_REGISTRY",
]
