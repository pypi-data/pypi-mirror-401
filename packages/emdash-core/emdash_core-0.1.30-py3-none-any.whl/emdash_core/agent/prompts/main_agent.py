"""Main agent system prompt.

The primary prompt for the orchestrating agent that manages sub-agents
and handles complex multi-step tasks.
"""

from .workflow import (
    WORKFLOW_PATTERNS,
    EXPLORATION_STRATEGY,
    OUTPUT_GUIDELINES,
    PARALLEL_EXECUTION,
)

# Base system prompt template with placeholder for tools
BASE_SYSTEM_PROMPT = """You are a code exploration and implementation assistant. You orchestrate focused sub-agents for exploration while maintaining the high-level view.

{tools_section}
""" + WORKFLOW_PATTERNS + PARALLEL_EXECUTION + EXPLORATION_STRATEGY + OUTPUT_GUIDELINES


def build_system_prompt(toolkit) -> str:
    """Build the complete system prompt with dynamic tool descriptions.

    Args:
        toolkit: The agent toolkit with registered tools

    Returns:
        Complete system prompt string
    """
    tools_section = build_tools_section(toolkit)
    skills_section = build_skills_section()
    prompt = BASE_SYSTEM_PROMPT.format(tools_section=tools_section)

    # Add skills section if there are skills available
    if skills_section:
        prompt += "\n" + skills_section

    return prompt


def build_skills_section() -> str:
    """Build the skills section of the system prompt.

    Returns:
        Formatted string with available skills, or empty string if none
    """
    from ..skills import SkillRegistry

    registry = SkillRegistry.get_instance()
    return registry.get_skills_for_prompt()


def build_tools_section(toolkit) -> str:
    """Build the tools section of the system prompt from registered tools.

    Args:
        toolkit: The agent toolkit with registered tools

    Returns:
        Formatted string with tool descriptions grouped by category
    """
    from ..tools.base import ToolCategory

    # Group tools by category
    tools_by_category: dict[str, list[tuple[str, str]]] = {}

    for tool in toolkit._tools.values():
        # Get category name
        if hasattr(tool, 'category'):
            category = tool.category.value if isinstance(tool.category, ToolCategory) else str(tool.category)
        else:
            category = "other"

        # Get tool name and description
        name = tool.name
        description = tool.description

        # Clean up description - take first sentence or first 150 chars
        if description:
            # Remove [server_name] prefix if present (from MCP tools)
            if description.startswith("["):
                description = description.split("]", 1)[-1].strip()
            # Take first sentence
            first_sentence = description.split(".")[0] + "."
            if len(first_sentence) > 150:
                first_sentence = description[:147] + "..."
            description = first_sentence
        else:
            description = "No description available."

        if category not in tools_by_category:
            tools_by_category[category] = []
        tools_by_category[category].append((name, description))

    # Build formatted section
    lines = ["## Available Tools\n"]

    # Define category display order and titles
    category_titles = {
        "search": "Search & Discovery",
        "traversal": "Graph Traversal",
        "analytics": "Analytics",
        "planning": "Planning",
        "history": "History",
        "other": "Other Tools",
    }

    # Sort categories by predefined order
    category_order = ["search", "traversal", "analytics", "planning", "history", "other"]
    sorted_categories = sorted(
        tools_by_category.keys(),
        key=lambda c: category_order.index(c) if c in category_order else 999
    )

    for category in sorted_categories:
        tools = tools_by_category[category]
        title = category_titles.get(category, category.title())

        lines.append(f"### {title}")
        for name, desc in sorted(tools):
            lines.append(f"- **{name}**: {desc}")
        lines.append("")

    return "\n".join(lines)
