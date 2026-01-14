"""Plan toolkit - exploration tools plus plan writing capability."""

from pathlib import Path

from .base import BaseToolkit
from ..tools.coding import ReadFileTool, ListFilesTool
from ..tools.search import SemanticSearchTool, GrepTool, GlobTool
from ..tools.plan_write import WritePlanTool
from ...utils.logger import log


class PlanToolkit(BaseToolkit):
    """Toolkit for planning with limited write access (plan files only).

    Provides all read-only exploration tools plus the ability to write
    implementation plans to .emdash/plans/*.md.

    Tools available:
    - read_file: Read file contents
    - list_files: List directory contents
    - glob: Find files by pattern
    - grep: Search file contents
    - semantic_search: AI-powered code search
    - write_plan: Write implementation plans (restricted to .emdash/plans/)
    """

    TOOLS = [
        "read_file",
        "list_files",
        "glob",
        "grep",
        "semantic_search",
        "write_plan",
    ]

    def _register_tools(self) -> None:
        """Register exploration and plan writing tools."""
        # All read-only exploration tools
        self.register_tool(ReadFileTool(repo_root=self.repo_root))
        self.register_tool(ListFilesTool(repo_root=self.repo_root))

        # Pattern-based search
        self.register_tool(GlobTool(connection=None))
        self.register_tool(GrepTool(connection=None))

        # Semantic search (if available)
        try:
            self.register_tool(SemanticSearchTool(connection=None))
        except Exception as e:
            log.debug(f"Semantic search not available: {e}")

        # Special: can only write to .emdash/plans/*.md
        self.register_tool(WritePlanTool(repo_root=self.repo_root))

        log.debug(f"PlanToolkit registered {len(self._tools)} tools")
