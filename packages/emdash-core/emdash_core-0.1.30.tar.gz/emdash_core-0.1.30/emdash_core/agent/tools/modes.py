"""Agent mode management tools.

Provides tools for entering and exiting modes, following
Claude Code's approach of explicit mode transitions.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory


class AgentMode(Enum):
    """Available agent modes."""
    PLAN = "plan"
    CODE = "code"


# Modes that can be entered via enter_mode tool
SUPPORTED_MODES = ["plan"]  # Extensible list


@dataclass
class ModeState:
    """Singleton state for agent mode."""

    current_mode: AgentMode = AgentMode.CODE
    plan_content: Optional[str] = None  # Stores the current plan

    _instance: Optional["ModeState"] = None

    @classmethod
    def get_instance(cls) -> "ModeState":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance."""
        cls._instance = None


class EnterModeTool(BaseTool):
    """Tool for entering a different mode from code mode."""

    name = "enter_mode"
    description = """Enter a different operating mode.

Currently supported modes:
- plan: Enter plan mode to explore the codebase and design an implementation plan.
        In plan mode you can ONLY use read-only tools (no file modifications).
        Use exit_plan when your plan is ready for user approval."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        mode: str,
        reason: str = "",
        **kwargs,
    ) -> ToolResult:
        """Enter a new mode.

        Args:
            mode: Mode to enter (currently only "plan" supported)
            reason: Why you're entering this mode (helps context)

        Returns:
            ToolResult indicating mode switch
        """
        mode_lower = mode.lower()

        if mode_lower not in SUPPORTED_MODES:
            return ToolResult.error_result(
                f"Unsupported mode: {mode}",
                suggestions=[f"Supported modes: {', '.join(SUPPORTED_MODES)}"],
            )

        state = ModeState.get_instance()

        if mode_lower == "plan":
            if state.current_mode == AgentMode.PLAN:
                return ToolResult.error_result(
                    "Already in plan mode",
                    suggestions=["Use exit_plan to submit your plan for approval"],
                )

            state.current_mode = AgentMode.PLAN
            state.plan_content = None  # Reset plan content

            return ToolResult.success_result(
                data={
                    "status": "entered_plan_mode",
                    "mode": "plan",
                    "reason": reason,
                    "message": "You are now in plan mode. Explore the codebase and design your plan. Use exit_plan when ready.",
                },
            )

        # Placeholder for future modes
        return ToolResult.error_result(f"Mode '{mode}' not yet implemented")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "mode": {
                    "type": "string",
                    "enum": SUPPORTED_MODES,
                    "description": "Mode to enter",
                },
                "reason": {
                    "type": "string",
                    "description": "Brief reason for entering this mode",
                },
            },
            required=["mode"],
        )


class ExitPlanModeTool(BaseTool):
    """Tool for exiting plan mode and submitting plan for approval."""

    name = "exit_plan"
    description = """Exit plan mode and submit your plan for user approval.

Scale detail based on task complexity:
- Simple task: title, summary, files_to_modify (steps optional)
- Complex task: all fields including phases, risks, open questions

Required fields:
- title: Clear, concise plan title
- summary: What will be implemented and why
- files_to_modify: List of file changes with paths, line numbers, and descriptions

Optional fields (include only if needed - each must "earn its place"):
- implementation_steps: For complex tasks needing ordered steps
- risks: Non-trivial risks only
- testing_strategy: Beyond obvious test cases

The user will either:
- Approve: You'll return to code mode to implement the plan
- Reject: You'll receive feedback and can revise in plan mode"""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def _parse_list(self, value, default=None):
        """Parse a value that might be a JSON string into a list."""
        import json
        if value is None:
            return default or []
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
                if isinstance(parsed, list):
                    return parsed
            except (json.JSONDecodeError, ValueError):
                pass
            return default or []
        if isinstance(value, list):
            return value
        return default or []

    def execute(
        self,
        title: str,
        summary: str,
        files_to_modify: list[dict] = None,
        implementation_steps: list[str] = None,
        risks: list[str] = None,
        testing_strategy: str = None,
        **kwargs,
    ) -> ToolResult:
        """Exit plan mode and submit plan for approval.

        Args:
            title: Title of the plan
            summary: Summary of what will be implemented and why
            files_to_modify: List of file changes, each with:
                - path: File path (e.g., "src/auth.py")
                - lines: Line range (e.g., "45-60" or "new file")
                - changes: Description of what changes
            implementation_steps: Ordered list of detailed implementation steps
            risks: List of potential risks or considerations
            testing_strategy: Description of how changes will be tested

        Returns:
            ToolResult triggering user approval flow
        """
        state = ModeState.get_instance()

        if state.current_mode != AgentMode.PLAN:
            return ToolResult.error_result(
                "Not in plan mode",
                suggestions=["Use enter_mode with mode='plan' to enter plan mode first"],
            )

        if not title or not title.strip():
            return ToolResult.error_result("Title is required")
        if not summary or not summary.strip():
            return ToolResult.error_result("Summary is required")

        # Parse lists that might come as JSON strings from LLM
        files_list = self._parse_list(files_to_modify)
        steps_list = self._parse_list(implementation_steps)
        risks_list = self._parse_list(risks)

        if not files_list:
            return ToolResult.error_result(
                "files_to_modify is required",
                suggestions=["Include at least one file with path, lines, and changes"],
            )
        # implementation_steps optional for simple tasks where files_to_modify is self-explanatory

        # Store plan content for reference
        state.plan_content = summary

        return ToolResult.success_result({
            "status": "plan_submitted",
            "title": title.strip(),
            "summary": summary.strip(),
            "files_to_modify": files_list,
            "implementation_steps": steps_list,
            "risks": risks_list,
            "testing_strategy": testing_strategy or "",
            "message": "Plan submitted for user approval. Waiting for user response.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Clear, concise title of the plan",
                },
                "summary": {
                    "type": "string",
                    "description": "Detailed summary of what will be implemented and why",
                },
                "files_to_modify": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "File path (e.g., 'src/auth.py')",
                            },
                            "lines": {
                                "type": "string",
                                "description": "Line range (e.g., '45-60') or 'new file'",
                            },
                            "changes": {
                                "type": "string",
                                "description": "Description of what changes in this file",
                            },
                        },
                        "required": ["path", "changes"],
                    },
                    "description": "List of files to modify with line numbers and change descriptions",
                },
                "implementation_steps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Detailed ordered list of implementation steps with sub-tasks",
                },
                "risks": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Potential risks, breaking changes, or considerations",
                },
                "testing_strategy": {
                    "type": "string",
                    "description": "How the changes will be tested (unit tests, integration tests, etc.)",
                },
            },
            required=["title", "summary", "files_to_modify"],
        )


class GetModeTool(BaseTool):
    """Tool for getting current agent mode."""

    name = "get_mode"
    description = "Get the current agent operating mode (plan or code)."
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(self, **kwargs) -> ToolResult:
        """Get current mode.

        Returns:
            ToolResult with current mode info
        """
        state = ModeState.get_instance()

        return ToolResult.success_result(
            data={
                "current_mode": state.current_mode.value,
                "has_plan": state.plan_content is not None,
                "available_modes": SUPPORTED_MODES,
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(properties={}, required=[])
