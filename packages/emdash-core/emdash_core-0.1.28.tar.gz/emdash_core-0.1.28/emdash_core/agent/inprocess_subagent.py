"""In-process sub-agent runner.

Runs sub-agents in the same process for better UX (real-time events)
while keeping isolated message histories.
"""

import json
import time
import uuid
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, Future

from .toolkits import get_toolkit
from .subagent_prompts import get_subagent_prompt
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from ..utils.logger import log


@dataclass
class SubAgentResult:
    """Result from a sub-agent execution."""

    success: bool
    agent_type: str
    agent_id: str
    task: str
    summary: str
    files_explored: list[str]
    findings: list[dict]
    iterations: int
    tools_used: list[str]
    execution_time: float
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


class InProcessSubAgent:
    """Sub-agent that runs in the same process.

    Benefits over subprocess:
    - Real-time event streaming to parent emitter
    - No stdout/stderr parsing
    - Simpler debugging
    - Natural UI integration

    Each sub-agent has its own:
    - Message history (isolated)
    - Agent ID (for event tagging)
    - Toolkit instance
    """

    def __init__(
        self,
        subagent_type: str,
        repo_root: Path,
        emitter=None,
        model: Optional[str] = None,
        max_turns: int = 10,
        agent_id: Optional[str] = None,
    ):
        """Initialize in-process sub-agent.

        Args:
            subagent_type: Type of agent (Explore, Plan, etc.)
            repo_root: Repository root directory
            emitter: Parent emitter for events (optional)
            model: Model to use (defaults to fast model)
            max_turns: Maximum iterations
            agent_id: Optional agent ID (generated if not provided)
        """
        self.subagent_type = subagent_type
        self.repo_root = repo_root.resolve()
        self.emitter = emitter
        self.max_turns = max_turns
        self.agent_id = agent_id or str(uuid.uuid4())[:8]

        # Get toolkit for this agent type
        self.toolkit = get_toolkit(subagent_type, repo_root)

        # Get model and create provider
        model_name = model or DEFAULT_MODEL
        self.provider = get_provider(model_name)

        # Get system prompt
        self.system_prompt = get_subagent_prompt(subagent_type)

        # Tracking
        self.files_explored: set[str] = set()
        self.tools_used: list[str] = []

    def _emit(self, event_type: str, **data) -> None:
        """Emit event with agent tagging.

        Uses the generic emit() method to preserve subagent_id and subagent_type
        in the event data, allowing the UI to display sub-agent events differently.
        """
        if self.emitter and hasattr(self.emitter, "emit"):
            from .events import EventType

            # Tag event with agent info
            data["subagent_id"] = self.agent_id
            data["subagent_type"] = self.subagent_type

            # Map event types
            event_map = {
                "tool_start": EventType.TOOL_START,
                "tool_result": EventType.TOOL_RESULT,
            }

            if event_type in event_map:
                self.emitter.emit(event_map[event_type], data)

    def run(self, prompt: str) -> SubAgentResult:
        """Execute the task and return results.

        Args:
            prompt: The task to perform

        Returns:
            SubAgentResult with findings
        """
        start_time = time.time()
        messages = []
        iterations = 0
        last_content = ""
        error = None

        # Add user message
        messages.append({"role": "user", "content": prompt})

        log.info(
            "SubAgent {} starting: type={} prompt={}",
            self.agent_id,
            self.subagent_type,
            prompt[:50] + "..." if len(prompt) > 50 else prompt,
        )

        try:
            # Agent loop
            while iterations < self.max_turns:
                iterations += 1

                log.debug(f"SubAgent {self.agent_id} turn {iterations}/{self.max_turns}")

                # Call LLM
                response = self.provider.chat(
                    messages=messages,
                    tools=self.toolkit.get_all_schemas(),
                    system=self.system_prompt,
                )

                # Add assistant response
                assistant_msg = self.provider.format_assistant_message(response)
                if assistant_msg:
                    messages.append(assistant_msg)

                # Save content
                if response.content:
                    last_content = response.content

                # Check if done
                if not response.tool_calls:
                    break

                # Execute tool calls
                for tool_call in response.tool_calls:
                    self.tools_used.append(tool_call.name)

                    # Parse arguments
                    try:
                        args = json.loads(tool_call.arguments) if tool_call.arguments else {}
                    except (json.JSONDecodeError, TypeError):
                        args = {}

                    # Emit tool start
                    self._emit("tool_start", name=tool_call.name, args=args)

                    # Track files
                    if "path" in args:
                        self.files_explored.add(args["path"])

                    # Execute tool
                    result = self.toolkit.execute(tool_call.name, **args)

                    # Emit tool result
                    summary = str(result.data)[:100] if result.data else ""
                    self._emit(
                        "tool_result",
                        name=tool_call.name,
                        success=result.success,
                        summary=summary,
                    )

                    # Add tool result to messages
                    tool_result_msg = self.provider.format_tool_result(
                        tool_call.id,
                        json.dumps(result.to_dict(), indent=2),
                    )
                    if tool_result_msg:
                        messages.append(tool_result_msg)

        except Exception as e:
            log.exception(f"SubAgent {self.agent_id} failed")
            error = str(e)

        execution_time = time.time() - start_time

        log.info(
            "SubAgent {} completed: {} turns, {} files, {:.1f}s",
            self.agent_id,
            iterations,
            len(self.files_explored),
            execution_time,
        )

        return SubAgentResult(
            success=error is None,
            agent_type=self.subagent_type,
            agent_id=self.agent_id,
            task=prompt,
            summary=last_content or "No response generated",
            files_explored=list(self.files_explored),
            findings=self._extract_findings(messages),
            iterations=iterations,
            tools_used=list(set(self.tools_used)),
            execution_time=execution_time,
            error=error,
        )

    def _extract_findings(self, messages: list[dict]) -> list[dict]:
        """Extract key findings from tool results."""
        findings = []
        for msg in messages:
            if msg and msg.get("role") == "tool":
                try:
                    content = json.loads(msg.get("content", "{}"))
                    if content and content.get("success") and content.get("data"):
                        findings.append(content["data"])
                except (json.JSONDecodeError, TypeError):
                    pass
        return findings[-10:]


# Thread pool for parallel execution
_executor: Optional[ThreadPoolExecutor] = None


def _get_executor() -> ThreadPoolExecutor:
    """Get or create thread pool executor."""
    global _executor
    if _executor is None:
        _executor = ThreadPoolExecutor(max_workers=4, thread_name_prefix="subagent")
    return _executor


def run_subagent(
    subagent_type: str,
    prompt: str,
    repo_root: Path,
    emitter=None,
    model: Optional[str] = None,
    max_turns: int = 10,
) -> SubAgentResult:
    """Run a sub-agent synchronously.

    Args:
        subagent_type: Type of agent (Explore, Plan)
        prompt: Task to perform
        repo_root: Repository root
        emitter: Event emitter
        model: Model to use
        max_turns: Max iterations

    Returns:
        SubAgentResult
    """
    agent = InProcessSubAgent(
        subagent_type=subagent_type,
        repo_root=repo_root,
        emitter=emitter,
        model=model,
        max_turns=max_turns,
    )
    return agent.run(prompt)


def run_subagent_async(
    subagent_type: str,
    prompt: str,
    repo_root: Path,
    emitter=None,
    model: Optional[str] = None,
    max_turns: int = 10,
) -> Future[SubAgentResult]:
    """Run a sub-agent asynchronously (returns Future).

    Args:
        subagent_type: Type of agent (Explore, Plan)
        prompt: Task to perform
        repo_root: Repository root
        emitter: Event emitter
        model: Model to use
        max_turns: Max iterations

    Returns:
        Future[SubAgentResult] - call .result() to get result
    """
    executor = _get_executor()
    return executor.submit(
        run_subagent,
        subagent_type=subagent_type,
        prompt=prompt,
        repo_root=repo_root,
        emitter=emitter,
        model=model,
        max_turns=max_turns,
    )


def run_subagents_parallel(
    tasks: list[dict],
    repo_root: Path,
    emitter=None,
) -> list[SubAgentResult]:
    """Run multiple sub-agents in parallel.

    Args:
        tasks: List of task dicts with keys:
            - subagent_type: str
            - prompt: str
            - model: str (optional)
            - max_turns: int (optional)
        repo_root: Repository root
        emitter: Shared event emitter

    Returns:
        List of SubAgentResults in same order as tasks
    """
    futures = []
    for task in tasks:
        future = run_subagent_async(
            subagent_type=task.get("subagent_type", "Explore"),
            prompt=task["prompt"],
            repo_root=repo_root,
            emitter=emitter,
            model=task.get("model"),
            max_turns=task.get("max_turns", 10),
        )
        futures.append(future)

    # Wait for all to complete and gather results
    results = []
    for future in futures:
        try:
            results.append(future.result())
        except Exception as e:
            log.exception("Sub-agent failed")
            results.append(SubAgentResult(
                success=False,
                agent_type="unknown",
                agent_id="error",
                task="",
                summary="",
                files_explored=[],
                findings=[],
                iterations=0,
                tools_used=[],
                execution_time=0,
                error=str(e),
            ))

    return results
