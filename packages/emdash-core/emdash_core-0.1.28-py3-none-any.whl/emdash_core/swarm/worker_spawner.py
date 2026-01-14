"""Subprocess spawning and management for parallel agent workers."""

import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

from .task_definition import SwarmTask, TaskStatus
from .worktree_manager import WorktreeManager, WorktreeInfo
from ..utils.logger import log


@dataclass
class WorkerResult:
    """Result from a worker subprocess."""
    task_id: str
    success: bool
    files_modified: list[str]
    completion_summary: Optional[str]
    error_message: Optional[str]
    stdout: str
    stderr: str
    return_code: int


def run_agent_in_worktree(
    worktree_path: str,
    task_description: str,
    model: str = "gpt-4o-mini",
    include_graph_tools: bool = False,
    timeout: int = 600,
) -> WorkerResult:
    """Run a coding agent in a worktree subprocess.

    This function is designed to be called in a separate process.
    It invokes `emdash agent code` within the worktree directory.

    Args:
        worktree_path: Path to the worktree
        task_description: Task for the agent to complete
        model: LLM model to use
        include_graph_tools: Whether to include graph tools
        timeout: Maximum seconds to run

    Returns:
        WorkerResult with execution details
    """
    worktree = Path(worktree_path)
    task_file = worktree / ".emdash-task" / "task.json"

    # Load task for ID
    task_id = "unknown"
    if task_file.exists():
        with open(task_file) as f:
            task_data = json.load(f)
            task_id = task_data.get("id", "unknown")

    # Build command - run emdash agent code in non-interactive mode
    cmd = [
        sys.executable, "-m", "emdash",
        "agent", "code",
        task_description,
        "--model", model,
        "--mode", "code",
        "-q",  # Quiet mode
    ]

    if not include_graph_tools:
        cmd.append("--no-graph-tools")

    # Set environment for isolated execution
    env = os.environ.copy()
    # Each worktree gets its own Kuzu DB to avoid lock contention
    env["KUZU_DATABASE_PATH"] = str(worktree / ".emdash-task" / "kuzu_db")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(worktree),
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )

        # Parse output to extract modified files
        files_modified = _extract_modified_files(result.stdout)
        completion_summary = _extract_summary(result.stdout)

        return WorkerResult(
            task_id=task_id,
            success=result.returncode == 0,
            files_modified=files_modified,
            completion_summary=completion_summary,
            error_message=result.stderr if result.returncode != 0 else None,
            stdout=result.stdout,
            stderr=result.stderr,
            return_code=result.returncode,
        )

    except subprocess.TimeoutExpired:
        return WorkerResult(
            task_id=task_id,
            success=False,
            files_modified=[],
            completion_summary=None,
            error_message=f"Task timed out after {timeout} seconds",
            stdout="",
            stderr="",
            return_code=-1,
        )
    except Exception as e:
        return WorkerResult(
            task_id=task_id,
            success=False,
            files_modified=[],
            completion_summary=None,
            error_message=str(e),
            stdout="",
            stderr="",
            return_code=-1,
        )


def _extract_modified_files(output: str) -> list[str]:
    """Extract list of modified files from agent output."""
    files = []
    for line in output.split("\n"):
        # Look for common patterns indicating file modifications
        lower = line.lower()
        if any(x in lower for x in ["modified:", "created:", "applied diff to", "wrote to"]):
            # Try to extract file path
            parts = line.split()
            for part in parts:
                if "/" in part or part.endswith(".py") or part.endswith(".ts"):
                    # Clean up the path
                    path = part.strip(",:\"'`")
                    if path and not path.startswith("-"):
                        files.append(path)
    return list(set(files))  # Dedupe


def _extract_summary(output: str) -> Optional[str]:
    """Extract completion summary from agent output."""
    # Look for completion markers
    lines = output.split("\n")
    for i, line in enumerate(lines):
        if "completed" in line.lower() or "summary" in line.lower():
            # Return this line and a few following
            summary_lines = lines[i:i+5]
            return "\n".join(summary_lines).strip()

    # Fall back to last non-empty lines
    non_empty = [l.strip() for l in lines if l.strip()]
    if non_empty:
        return "\n".join(non_empty[-3:])
    return None


class WorkerSpawner:
    """Orchestrates parallel worker subprocesses.

    Creates worktrees for each task and runs agents in parallel,
    collecting results as they complete.

    Example:
        spawner = WorkerSpawner(repo_root=Path("."))

        tasks = [
            SwarmTask(id="1", slug="add-auth", ...),
            SwarmTask(id="2", slug="fix-bug", ...),
        ]

        results = spawner.run_parallel(tasks, max_workers=3)
    """

    def __init__(
        self,
        repo_root: Path,
        model: str = "gpt-4o-mini",
        include_graph_tools: bool = False,
        timeout_per_task: int = 600,
    ):
        self.repo_root = repo_root.resolve()
        self.worktree_manager = WorktreeManager(repo_root)
        self.model = model
        self.include_graph_tools = include_graph_tools
        self.timeout = timeout_per_task

    def prepare_worktree(self, task: SwarmTask) -> WorktreeInfo:
        """Create worktree and initialize task state."""
        info = self.worktree_manager.create_worktree(
            task_name=task.slug,
            base_branch=task.base_branch,
            force=True,
        )

        # Update task with worktree info
        task.worktree_path = str(info.path)
        task.branch = info.branch
        task.status = TaskStatus.WORKTREE_CREATED

        # Save task state to worktree
        task.save(info.path)

        return info

    def run_parallel(
        self,
        tasks: list[SwarmTask],
        max_workers: int = 3,
        progress_callback: Optional[Callable[[SwarmTask, WorkerResult], None]] = None,
    ) -> dict[str, WorkerResult]:
        """Run all tasks in parallel.

        Args:
            tasks: List of tasks to execute
            max_workers: Maximum concurrent workers
            progress_callback: Called when each task completes

        Returns:
            Dict mapping task_id to WorkerResult
        """
        results: dict[str, WorkerResult] = {}

        # Create all worktrees first
        log.info(f"Creating {len(tasks)} worktrees...")
        for task in tasks:
            self.prepare_worktree(task)
            task.status = TaskStatus.RUNNING
            task.started_at = datetime.now().isoformat()
            if task.worktree_path:
                task.save(Path(task.worktree_path))

        # Run agents in parallel using ProcessPoolExecutor
        log.info(f"Starting {len(tasks)} agents with max {max_workers} workers...")

        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(
                    run_agent_in_worktree,
                    task.worktree_path,
                    task.description,
                    self.model,
                    self.include_graph_tools,
                    self.timeout,
                ): task
                for task in tasks
            }

            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]

                try:
                    result = future.result()
                    results[task.id] = result

                    # Update task status
                    task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
                    task.files_modified = result.files_modified
                    task.completion_summary = result.completion_summary
                    task.error_message = result.error_message
                    task.agent_output = result.stdout[:5000] if result.stdout else None
                    task.completed_at = datetime.now().isoformat()

                    # Save updated state
                    if task.worktree_path:
                        task.save(Path(task.worktree_path))

                    if progress_callback:
                        progress_callback(task, result)

                    status = "SUCCESS" if result.success else "FAILED"
                    log.info(f"Task {task.slug} completed: {status}")

                except Exception as e:
                    log.exception(f"Task {task.slug} raised exception")
                    task.status = TaskStatus.FAILED
                    task.error_message = str(e)
                    task.completed_at = datetime.now().isoformat()

                    if task.worktree_path:
                        task.save(Path(task.worktree_path))

                    results[task.id] = WorkerResult(
                        task_id=task.id,
                        success=False,
                        files_modified=[],
                        completion_summary=None,
                        error_message=str(e),
                        stdout="",
                        stderr="",
                        return_code=-1,
                    )

        return results

    def run_sequential(
        self,
        tasks: list[SwarmTask],
        progress_callback: Optional[Callable[[SwarmTask, WorkerResult], None]] = None,
    ) -> dict[str, WorkerResult]:
        """Run tasks sequentially (for debugging or dependent tasks).

        Args:
            tasks: List of tasks to execute
            progress_callback: Called when each task completes

        Returns:
            Dict mapping task_id to WorkerResult
        """
        return self.run_parallel(tasks, max_workers=1, progress_callback=progress_callback)
