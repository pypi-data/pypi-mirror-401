"""Spec planning tools for feature specifications."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ..spec_schema import Spec
from ...utils.logger import log


@dataclass
class SpecState:
    """Singleton state for spec management."""

    current_spec: Optional[Spec] = None
    save_path: Optional[Path] = None
    history: list[Spec] = field(default_factory=list)

    _instance: Optional["SpecState"] = None

    @classmethod
    def get_instance(cls) -> "SpecState":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance."""
        cls._instance = None

    def configure(self, save_path: Optional[Path] = None) -> None:
        """Configure the spec state.

        Args:
            save_path: Path to save specs to
        """
        self.save_path = save_path


class SubmitSpecTool(BaseTool):
    """Tool for submitting a new specification."""

    name = "submit_spec"
    description = """Submit a feature specification for review.
Creates a structured spec document with requirements and acceptance criteria."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        title: str,
        summary: str,
        requirements: list[str],
        acceptance_criteria: list[str],
        technical_notes: Optional[list[str]] = None,
        dependencies: Optional[list[str]] = None,
        open_questions: Optional[list[str]] = None,
    ) -> ToolResult:
        """Submit a specification.

        Args:
            title: Spec title
            summary: Brief summary
            requirements: List of requirements
            acceptance_criteria: Acceptance criteria
            technical_notes: Optional technical notes
            dependencies: Optional dependencies
            open_questions: Optional open questions

        Returns:
            ToolResult with spec info
        """
        try:
            # Build markdown content from structured fields
            content_parts = []

            if summary:
                content_parts.append(f"> {summary}\n")

            if requirements:
                content_parts.append("## Requirements")
                content_parts.extend(f"- {req}" for req in requirements)
                content_parts.append("")

            if acceptance_criteria:
                content_parts.append("## Acceptance Criteria")
                content_parts.extend(f"- {crit}" for crit in acceptance_criteria)
                content_parts.append("")

            if technical_notes:
                content_parts.append("## Technical Notes")
                content_parts.extend(f"- {note}" for note in technical_notes)
                content_parts.append("")

            if dependencies:
                content_parts.append("## Dependencies")
                content_parts.extend(f"- {dep}" for dep in dependencies)
                content_parts.append("")

            if open_questions:
                content_parts.append("## Open Questions")
                content_parts.extend(f"- {q}" for q in open_questions)
                content_parts.append("")

            content = "\n".join(content_parts)

            # Create spec with title and content only (matches Spec schema)
            spec = Spec(title=title, content=content)

            # Store in state
            state = SpecState.get_instance()
            if state.current_spec:
                state.history.append(state.current_spec)
            state.current_spec = spec

            # Save to file if configured
            if state.save_path:
                try:
                    state.save_path.write_text(spec.to_markdown())
                    log.info(f"Saved spec to {state.save_path}")
                except Exception as e:
                    log.warning(f"Failed to save spec: {e}")

            return ToolResult.success_result(
                data={
                    "title": title,
                    "requirements_count": len(requirements),
                    "acceptance_criteria_count": len(acceptance_criteria),
                    "markdown": spec.to_markdown(),
                },
            )

        except Exception as e:
            log.exception("Submit spec failed")
            return ToolResult.error_result(f"Failed to submit spec: {str(e)}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Spec title",
                },
                "summary": {
                    "type": "string",
                    "description": "Brief summary of the feature",
                },
                "requirements": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of requirements",
                },
                "acceptance_criteria": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Acceptance criteria for completion",
                },
                "technical_notes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Technical implementation notes",
                },
                "dependencies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Dependencies on other features/specs",
                },
                "open_questions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Open questions to resolve",
                },
            },
            required=["title", "summary", "requirements", "acceptance_criteria"],
        )


class GetSpecTool(BaseTool):
    """Tool for getting the current specification."""

    name = "get_spec"
    description = """Get the current feature specification.
Returns the spec in markdown format."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(self) -> ToolResult:
        """Get the current spec.

        Returns:
            ToolResult with spec content
        """
        state = SpecState.get_instance()

        if not state.current_spec:
            return ToolResult.error_result(
                "No spec has been submitted yet",
                suggestions=["Use submit_spec to create a specification"],
            )

        spec = state.current_spec

        return ToolResult.success_result(
            data={
                "title": spec.title,
                "content": spec.content,
                "markdown": spec.to_markdown(),
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(properties={}, required=[])


class UpdateSpecTool(BaseTool):
    """Tool for updating the current specification."""

    name = "update_spec"
    description = """Update the current feature specification.
Append content or replace the entire spec content."""
    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    def execute(
        self,
        append_content: Optional[str] = None,
        replace_content: Optional[str] = None,
        update_title: Optional[str] = None,
        **kwargs,
    ) -> ToolResult:
        """Update the current spec.

        Args:
            append_content: Content to append to existing spec
            replace_content: Content to replace entire spec content
            update_title: New title for the spec

        Returns:
            ToolResult with updated spec
        """
        state = SpecState.get_instance()

        if not state.current_spec:
            return ToolResult.error_result(
                "No spec to update",
                suggestions=["Use submit_spec first"],
            )

        spec = state.current_spec

        # Update title if provided
        if update_title:
            spec.title = update_title

        # Replace or append content
        if replace_content is not None:
            spec.content = replace_content
        elif append_content:
            spec.content = spec.content + "\n\n" + append_content

        # Save if configured
        if state.save_path:
            try:
                state.save_path.write_text(spec.to_markdown())
            except Exception as e:
                log.warning(f"Failed to save spec: {e}")

        return ToolResult.success_result(
            data={
                "title": spec.title,
                "content": spec.content,
                "markdown": spec.to_markdown(),
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "append_content": {
                    "type": "string",
                    "description": "Markdown content to append to existing spec",
                },
                "replace_content": {
                    "type": "string",
                    "description": "Markdown content to replace entire spec content",
                },
                "update_title": {
                    "type": "string",
                    "description": "New title for the spec",
                },
            },
            required=[],
        )
