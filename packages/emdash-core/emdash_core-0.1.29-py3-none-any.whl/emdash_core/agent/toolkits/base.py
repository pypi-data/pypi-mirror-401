"""Base class for sub-agent toolkits."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..tools.base import BaseTool, ToolResult


class BaseToolkit(ABC):
    """Abstract base class for sub-agent toolkits.

    Each toolkit provides a curated set of tools appropriate for a specific
    agent type. Toolkits are responsible for:
    - Registering appropriate tools
    - Providing OpenAI function schemas
    - Executing tools by name
    """

    # List of tool names this toolkit provides (for documentation)
    TOOLS: list[str] = []

    def __init__(self, repo_root: Path):
        """Initialize the toolkit.

        Args:
            repo_root: Root directory of the repository
        """
        self.repo_root = repo_root.resolve()
        self._tools: dict[str, BaseTool] = {}
        self._register_tools()

    @abstractmethod
    def _register_tools(self) -> None:
        """Register tools for this toolkit.

        Subclasses must implement this to register their specific tools.
        """
        pass

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self) -> list[str]:
        """List all tool names in this toolkit.

        Returns:
            List of tool names
        """
        return list(self._tools.keys())

    def execute(self, tool_name: str, **params) -> ToolResult:
        """Execute a tool by name.

        Args:
            tool_name: Name of the tool
            **params: Tool parameters

        Returns:
            ToolResult
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return ToolResult.error_result(
                f"Unknown tool: {tool_name}",
                suggestions=[f"Available tools: {self.list_tools()}"],
            )

        try:
            return tool.execute(**params)
        except Exception as e:
            return ToolResult.error_result(f"Tool execution failed: {str(e)}")

    def get_all_schemas(self) -> list[dict]:
        """Get OpenAI function calling schemas for all tools.

        Returns:
            List of function schemas
        """
        return [tool.get_schema() for tool in self._tools.values()]
