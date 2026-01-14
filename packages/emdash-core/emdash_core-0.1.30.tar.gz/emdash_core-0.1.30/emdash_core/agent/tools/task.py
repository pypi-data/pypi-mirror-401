"""Task tool for spawning sub-agents.

Follows Claude Code's Task tool pattern - spawns specialized sub-agents
for focused tasks like exploration and planning.

Uses in-process execution for better UX (real-time events) while
maintaining isolated message histories per sub-agent.
"""

import uuid
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ..toolkits import list_agent_types
from ..inprocess_subagent import run_subagent, run_subagent_async
from ...utils.logger import log


class TaskTool(BaseTool):
    """Spawn a sub-agent to handle complex, multi-step tasks autonomously.

    The Task tool launches specialized agents in-process with isolated
    message histories. Each agent type has specific capabilities:

    - **Explore**: Fast codebase exploration using read_file, glob, grep, semantic_search
    - **Plan**: Design implementation plans, can write to .emdash/plans/*.md

    Sub-agents run with their own context and tools, returning a summary when done.
    Events are tagged with agent_id to prevent mixing in the UI.
    """

    name = "task"
    description = """Launch a specialized sub-agent for focused tasks.

Use this to spawn lightweight agents for:
- Fast codebase exploration (Explore agent)
- Implementation planning (Plan agent)

Sub-agents run autonomously and return structured results.
Multiple sub-agents can be launched in parallel."""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None, emitter=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
            emitter: Optional event emitter for progress events
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection
        self.emitter = emitter

    def execute(
        self,
        description: str = "",
        prompt: str = "",
        subagent_type: str = "Explore",
        model_tier: str = "fast",
        max_turns: int = 10,
        run_in_background: bool = False,
        resume: Optional[str] = None,
        **kwargs,
    ) -> ToolResult:
        """Spawn a sub-agent to perform a task.

        Args:
            description: Short (3-5 word) description of the task
            prompt: The task for the agent to perform
            subagent_type: Type of agent (Explore, Plan)
            model_tier: Model tier (fast, standard, powerful)
            max_turns: Maximum API round-trips
            run_in_background: Run asynchronously
            resume: Agent ID to resume from

        Returns:
            ToolResult with agent results or background task info
        """
        # Validate inputs
        if not prompt:
            return ToolResult.error_result(
                "Prompt is required",
                suggestions=["Provide a clear task description in 'prompt'"],
            )

        available_types = list_agent_types()
        if subagent_type not in available_types:
            return ToolResult.error_result(
                f"Unknown agent type: {subagent_type}",
                suggestions=[f"Available types: {available_types}"],
            )

        log.info(
            "Spawning sub-agent type={} model={} prompt={}",
            subagent_type,
            model_tier,
            prompt[:50] + "..." if len(prompt) > 50 else prompt,
        )

        if run_in_background:
            return self._run_background(subagent_type, prompt, max_turns)
        else:
            return self._run_sync(subagent_type, prompt, max_turns)

    def _run_sync(
        self,
        subagent_type: str,
        prompt: str,
        max_turns: int,
    ) -> ToolResult:
        """Run sub-agent synchronously in the same process.

        Args:
            subagent_type: Agent type
            prompt: Task prompt
            max_turns: Maximum API round-trips

        Returns:
            ToolResult with agent results
        """
        try:
            result = run_subagent(
                subagent_type=subagent_type,
                prompt=prompt,
                repo_root=self.repo_root,
                emitter=self.emitter,
                max_turns=max_turns,
            )

            if result.success:
                return ToolResult.success_result(
                    data=result.to_dict(),
                    suggestions=self._generate_suggestions(result.to_dict()),
                )
            else:
                return ToolResult.error_result(
                    f"Sub-agent failed: {result.error}",
                    suggestions=["Check the prompt and try again"],
                )

        except Exception as e:
            log.exception("Failed to run sub-agent")
            return ToolResult.error_result(f"Failed to run sub-agent: {e}")

    def _run_background(
        self,
        subagent_type: str,
        prompt: str,
        max_turns: int,
    ) -> ToolResult:
        """Run sub-agent in background using a thread.

        Args:
            subagent_type: Agent type
            prompt: Task prompt
            max_turns: Maximum API round-trips

        Returns:
            ToolResult with task info
        """
        agent_id = str(uuid.uuid4())[:8]

        # Output file for results
        output_dir = self.repo_root / ".emdash" / "agents"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{agent_id}.output"

        try:
            # Start async execution
            future = run_subagent_async(
                subagent_type=subagent_type,
                prompt=prompt,
                repo_root=self.repo_root,
                emitter=self.emitter,
                max_turns=max_turns,
            )

            # Store future for later retrieval (attach to class for now)
            if not hasattr(self, "_background_tasks"):
                self._background_tasks = {}
            self._background_tasks[agent_id] = {
                "future": future,
                "output_file": output_file,
            }

            log.info(f"Started background agent {agent_id}")

            return ToolResult.success_result(
                data={
                    "agent_id": agent_id,
                    "status": "running",
                    "agent_type": subagent_type,
                    "output_file": str(output_file),
                },
                suggestions=[
                    f"Use task_output(agent_id='{agent_id}') to check results",
                ],
            )

        except Exception as e:
            log.exception("Failed to start background agent")
            return ToolResult.error_result(f"Failed to start background agent: {e}")

    def _generate_suggestions(self, data: dict) -> list[str]:
        """Generate follow-up suggestions based on results."""
        suggestions = []

        files = data.get("files_explored", [])
        if files:
            suggestions.append(f"Found {len(files)} relevant files")

        if data.get("agent_type") == "Plan":
            suggestions.append("Review the plan in .emdash/plans/")

        if data.get("agent_id"):
            suggestions.append(f"Agent ID: {data['agent_id']} (can resume later)")

        return suggestions

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "description": {
                    "type": "string",
                    "description": "Short (3-5 word) description of the task",
                },
                "prompt": {
                    "type": "string",
                    "description": "The task for the agent to perform",
                },
                "subagent_type": {
                    "type": "string",
                    "enum": ["Explore", "Plan"],
                    "description": "Type of specialized agent",
                    "default": "Explore",
                },
                "model_tier": {
                    "type": "string",
                    "enum": ["fast", "model"],
                    "description": "Model tier (fast=cheap/quick, model=standard)",
                    "default": "fast",
                },
                "max_turns": {
                    "type": "integer",
                    "description": "Maximum API round-trips",
                    "default": 10,
                },
                "run_in_background": {
                    "type": "boolean",
                    "description": "Run agent asynchronously",
                    "default": False,
                },
                "resume": {
                    "type": "string",
                    "description": "Agent ID to resume from previous execution",
                },
            },
            required=["prompt"],
        )
