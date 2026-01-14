"""Agent prompts module.

Centralized location for all agent system prompts and workflow patterns.
"""

from .workflow import (
    WORKFLOW_PATTERNS,
    EXPLORATION_STRATEGY,
    OUTPUT_GUIDELINES,
    EFFICIENCY_RULES,
    EXPLORATION_OUTPUT_FORMAT,
    PLAN_TEMPLATE,
    SIZING_GUIDELINES,
    PARALLEL_EXECUTION,
)
from .main_agent import (
    BASE_SYSTEM_PROMPT,
    build_system_prompt,
    build_tools_section,
)
from .subagents import SUBAGENT_PROMPTS, get_subagent_prompt
from .plan_mode import PLAN_MODE_PROMPT

__all__ = [
    # Workflow patterns
    "WORKFLOW_PATTERNS",
    "EXPLORATION_STRATEGY",
    "OUTPUT_GUIDELINES",
    "EFFICIENCY_RULES",
    "EXPLORATION_OUTPUT_FORMAT",
    "PLAN_TEMPLATE",
    "SIZING_GUIDELINES",
    "PARALLEL_EXECUTION",
    # Main agent
    "BASE_SYSTEM_PROMPT",
    "build_system_prompt",
    "build_tools_section",
    # Sub-agents
    "SUBAGENT_PROMPTS",
    "get_subagent_prompt",
    # Plan mode
    "PLAN_MODE_PROMPT",
]
