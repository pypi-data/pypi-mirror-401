"""TaskOutput tool for retrieving sub-agent results.

Retrieves output from background sub-agents started with run_in_background=True.
"""

import json
import time
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class TaskOutputTool(BaseTool):
    """Get output from a running or completed background sub-agent.

    Use this to check on sub-agents that were started with run_in_background=True.
    """

    name = "task_output"
    description = """Get output from a background sub-agent.

Use this to check the status and results of sub-agents started with
run_in_background=True. Can wait for completion or check immediately."""
    category = ToolCategory.PLANNING

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used)
        """
        self.repo_root = repo_root.resolve()
        self.agents_dir = repo_root / ".emdash" / "agents"
        self.connection = connection

    def execute(
        self,
        agent_id: str = "",
        block: bool = True,
        timeout: int = 60,
        **kwargs,
    ) -> ToolResult:
        """Get output from a background agent.

        Args:
            agent_id: Agent ID to get output from
            block: Whether to wait for completion
            timeout: Max wait time in seconds (if blocking)

        Returns:
            ToolResult with agent output or status
        """
        if not agent_id:
            return ToolResult.error_result(
                "agent_id is required",
                suggestions=["Provide the agent_id from the task() call"],
            )

        output_file = self.agents_dir / f"{agent_id}.output"
        transcript_file = self.agents_dir / f"{agent_id}.jsonl"

        if block:
            return self._wait_for_completion(
                agent_id, output_file, transcript_file, timeout
            )
        else:
            return self._check_status(agent_id, output_file, transcript_file)

    def _wait_for_completion(
        self,
        agent_id: str,
        output_file: Path,
        transcript_file: Path,
        timeout: int,
    ) -> ToolResult:
        """Wait for agent to complete.

        Args:
            agent_id: Agent ID
            output_file: Path to output file
            transcript_file: Path to transcript file
            timeout: Max wait time in seconds

        Returns:
            ToolResult with results
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            if output_file.exists():
                content = output_file.read_text().strip()

                # Check if output is complete JSON
                try:
                    data = json.loads(content)
                    if isinstance(data, dict) and "success" in data:
                        return ToolResult.success_result(
                            data=data,
                            metadata={"agent_id": agent_id, "status": "completed"},
                        )
                except json.JSONDecodeError:
                    pass

                # Still running if output exists but isn't complete JSON
                if content:
                    return ToolResult.success_result(
                        data={
                            "status": "running",
                            "agent_id": agent_id,
                            "partial_output": content[-2000:],  # Last 2KB
                        },
                    )

            time.sleep(1)

        # Timeout
        return ToolResult.success_result(
            data={
                "status": "timeout",
                "agent_id": agent_id,
                "message": f"Agent did not complete within {timeout}s",
            },
            suggestions=["Use block=false to check status without waiting"],
        )

    def _check_status(
        self,
        agent_id: str,
        output_file: Path,
        transcript_file: Path,
    ) -> ToolResult:
        """Check agent status without waiting.

        Args:
            agent_id: Agent ID
            output_file: Path to output file
            transcript_file: Path to transcript file

        Returns:
            ToolResult with status
        """
        # Check if output file exists
        if not output_file.exists():
            # Check if transcript exists (agent was started)
            if transcript_file.exists():
                return ToolResult.success_result(
                    data={
                        "status": "running",
                        "agent_id": agent_id,
                    },
                )
            else:
                return ToolResult.error_result(
                    f"Agent {agent_id} not found",
                    suggestions=["Check the agent_id is correct"],
                )

        # Output exists, check if complete
        try:
            content = output_file.read_text().strip()
            data = json.loads(content)

            if isinstance(data, dict) and "success" in data:
                return ToolResult.success_result(
                    data=data,
                    metadata={"agent_id": agent_id, "status": "completed"},
                )

        except json.JSONDecodeError:
            pass

        # Partial output
        return ToolResult.success_result(
            data={
                "status": "running",
                "agent_id": agent_id,
                "has_output": True,
            },
        )

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "agent_id": {
                    "type": "string",
                    "description": "Agent ID to get output from",
                },
                "block": {
                    "type": "boolean",
                    "description": "Wait for completion (default: true)",
                    "default": True,
                },
                "timeout": {
                    "type": "integer",
                    "description": "Max wait time in seconds if blocking",
                    "default": 60,
                },
            },
            required=["agent_id"],
        )
