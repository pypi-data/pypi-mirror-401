"""ExploredAreasProvider - Context from agent exploration with tool-based relevance."""

from dataclasses import asdict
from typing import Optional, Union

from ..models import ContextItem, ContextProviderSpec
from .base import ContextProvider
from ..registry import ContextProviderRegistry
from ...graph.connection import KuzuConnection
from ...utils.logger import log


class ExploredAreasProvider(ContextProvider):
    """Context provider that extracts entities from agent exploration.

    Analyzes the steps recorded during an agent session and assigns
    relevance scores based on the tool type used to discover each entity.

    High relevance: deliberate investigation (expand_node, get_callers, etc.)
    Medium relevance: targeted search (semantic_search, text_search)
    Low relevance: broad search (grep, get_top_pagerank)
    """

    # Tool-based relevance scores
    TOOL_RELEVANCE = {
        # High relevance - deliberate investigation
        "expand_node": 1.0,
        "get_callers": 0.9,
        "get_callees": 0.9,
        "get_class_hierarchy": 0.9,
        "get_neighbors": 0.85,
        "get_impact_analysis": 0.85,
        "read_file": 0.8,  # Reading a file is deliberate investigation
        # Medium relevance - targeted search
        "semantic_search": 0.7,
        "text_search": 0.6,
        "get_file_dependencies": 0.6,
        "find_entity": 0.6,
        # Lower relevance - broad search/modification
        "grep": 0.4,
        "write_to_file": 0.4,
        "apply_diff": 0.4,
        "get_top_pagerank": 0.3,
        "get_communities": 0.3,
        "list_files": 0.2,
        "execute_command": 0.1,
    }

    # Only top N results from search tools are considered highly relevant
    TOP_RESULTS_LIMIT = 3

    # Tools where we limit to top results
    SEARCH_TOOLS = {"semantic_search", "text_search", "grep", "find_entity"}

    def __init__(self, connection: KuzuConnection, config: Optional[dict] = None):
        super().__init__(connection, config)

    @property
    def spec(self) -> ContextProviderSpec:
        return ContextProviderSpec(
            name="explored_areas",
            description="Context from agent exploration with tool-based relevance",
            requires_graph=False,  # Uses session data, not graph queries
        )

    def extract_context(self, exploration_steps: list) -> list[ContextItem]:
        """Extract context items from exploration steps.

        Args:
            exploration_steps: List of ExplorationStep objects or dicts from AgentSession

        Returns:
            Context items with relevance-based scores
        """
        if not exploration_steps:
            return []

        # Track best score for each entity
        entity_scores: dict[str, tuple[float, Optional[str], Optional[str]]] = {}

        for step in exploration_steps:
            # Handle both ExplorationStep objects and dicts
            if hasattr(step, "tool_name"):
                tool_name = step.tool_name
                entities = step.entities_discovered
            else:
                tool_name = step.get("tool_name", "")
                entities = step.get("entities_discovered", [])

            # Get base relevance score for this tool
            base_score = self.TOOL_RELEVANCE.get(tool_name, 0.2)

            # For search tools, only top results are highly relevant
            if tool_name in self.SEARCH_TOOLS:
                # Process top results with full score, others with reduced score
                for i, entity in enumerate(entities):
                    qname = self._extract_qualified_name(entity)
                    if not qname:
                        continue

                    # Top results get full score, others get reduced
                    if i < self.TOP_RESULTS_LIMIT:
                        score = base_score
                    else:
                        score = base_score * 0.5  # Reduced score for non-top results

                    self._update_entity_score(entity_scores, qname, score, entity)
            else:
                # Non-search tools: all entities get the same score
                for entity in entities:
                    qname = self._extract_qualified_name(entity)
                    if not qname:
                        continue
                    self._update_entity_score(entity_scores, qname, base_score, entity)

        # Convert to ContextItems
        items = []
        for qname, (score, entity_type, file_path) in entity_scores.items():
            # Skip file: prefix for display if it's a File type
            display_name = qname
            if qname.startswith("file:"):
                display_name = qname[5:]  # Remove "file:" prefix
            items.append(
                ContextItem(
                    qualified_name=display_name,
                    entity_type=entity_type or "Unknown",
                    file_path=file_path,
                    score=score,
                    neighbors=[],  # Could fetch from graph if needed
                )
            )

        log.info(
            f"ExploredAreasProvider: extracted {len(items)} context items "
            f"from {len(exploration_steps)} exploration steps"
        )
        return items

    def _extract_qualified_name(self, entity: Union[str, dict]) -> Optional[str]:
        """Extract qualified name from entity (string or dict)."""
        if isinstance(entity, str):
            return entity
        if isinstance(entity, dict):
            return entity.get("qualified_name")
        return None

    def _update_entity_score(
        self,
        entity_scores: dict,
        qname: str,
        score: float,
        entity: Union[str, dict],
    ) -> None:
        """Update entity score, keeping the highest score."""
        current = entity_scores.get(qname)
        if current is None or score > current[0]:
            entity_type = self._infer_type(entity)
            file_path = self._infer_file(entity)
            entity_scores[qname] = (score, entity_type, file_path)

    def _infer_type(self, entity: Union[str, dict]) -> Optional[str]:
        """Infer entity type from entity data."""
        if isinstance(entity, dict):
            return entity.get("type") or entity.get("entity_type")
        # Try to infer from qualified name pattern
        if isinstance(entity, str):
            if "." in entity:
                parts = entity.split(".")
                # If last part starts with uppercase, likely a class
                if parts[-1] and parts[-1][0].isupper():
                    return "Class"
            return "Function"  # Default assumption
        return None

    def _infer_file(self, entity: Union[str, dict]) -> Optional[str]:
        """Infer file path from entity data."""
        if isinstance(entity, dict):
            return entity.get("file_path") or entity.get("path")
        return None


# Auto-register provider
ContextProviderRegistry.register("explored_areas", ExploredAreasProvider)
