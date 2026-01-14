"""Main swarm orchestrator combining all components."""

import re
from pathlib import Path
from typing import Callable, Optional
from uuid import uuid4

from .task_definition import SwarmTask, SwarmState, TaskStatus
from .worktree_manager import WorktreeManager
from .worker_spawner import WorkerSpawner, WorkerResult
from .merge_agent import MergeAgent, MergeResult
from ..utils.logger import log


class SwarmRunner:
    """Orchestrates the full swarm lifecycle.

    1. Creates worktrees for each task
    2. Spawns parallel agent workers
    3. Collects results
    4. Merges completed work

    Example:
        runner = SwarmRunner(repo_root=Path("."))

        tasks = [
            "Add user authentication",
            "Fix the login page CSS",
            "Add unit tests for auth module",
        ]

        state = runner.run(tasks)
        runner.merge_completed()
    """

    def __init__(
        self,
        repo_root: Path,
        model: str = "gpt-4o-mini",
        max_workers: int = 3,
        timeout_per_task: int = 600,
        base_branch: str = "main",
        include_graph_tools: bool = False,
    ):
        self.repo_root = repo_root.resolve()
        self.model = model
        self.max_workers = max_workers
        self.timeout = timeout_per_task
        self.base_branch = base_branch
        self.include_graph_tools = include_graph_tools

        self.worktree_manager = WorktreeManager(repo_root)
        self.spawner = WorkerSpawner(
            repo_root=repo_root,
            model=model,
            include_graph_tools=include_graph_tools,
            timeout_per_task=timeout_per_task,
        )
        self.merge_agent = MergeAgent(repo_root, model)

        self.state: Optional[SwarmState] = None

    def slugify(self, text: str) -> str:
        """Create URL-safe slug from text."""
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text[:50]

    def run(
        self,
        task_descriptions: list[str],
        progress_callback: Optional[Callable[[SwarmTask, WorkerResult], None]] = None,
    ) -> SwarmState:
        """Execute the full swarm workflow.

        Args:
            task_descriptions: List of task descriptions
            progress_callback: Called when each task completes

        Returns:
            SwarmState with all task results
        """
        # Create swarm state
        swarm_id = str(uuid4())[:8]
        tasks = []

        for i, desc in enumerate(task_descriptions):
            slug = self.slugify(desc)
            # Add index suffix if slug is duplicate
            existing_slugs = [t.slug for t in tasks]
            if slug in existing_slugs:
                slug = f"{slug}-{i+1}"

            task = SwarmTask(
                id=str(uuid4()),
                slug=slug,
                title=desc[:100],
                description=desc,
                base_branch=self.base_branch,
            )
            tasks.append(task)

        self.state = SwarmState(
            id=swarm_id,
            tasks=tasks,
            base_branch=self.base_branch,
        )

        # Save initial state
        self.state.save(self.repo_root)

        log.info(f"Starting swarm {swarm_id} with {len(tasks)} tasks")

        # Run parallel workers
        self.spawner.run_parallel(
            tasks=tasks,
            max_workers=self.max_workers,
            progress_callback=progress_callback,
        )

        # Update and save final state
        self.state.save(self.repo_root)

        return self.state

    def merge_completed(
        self,
        use_llm: bool = False,
        target_branch: Optional[str] = None,
        cleanup_worktrees: bool = True,
    ) -> list[MergeResult]:
        """Merge all completed task branches.

        Args:
            use_llm: Whether to use LLM assistance for merges
            target_branch: Target branch (defaults to base_branch)
            cleanup_worktrees: Whether to delete worktrees after successful merge

        Returns:
            List of merge results
        """
        if not self.state:
            self.state = SwarmState.load(self.repo_root)

        if not self.state:
            raise ValueError("No swarm state found")

        target = target_branch or self.state.base_branch

        results = self.merge_agent.merge_all_completed(
            self.state.tasks,
            target=target,
            use_llm=use_llm,
            cleanup_worktrees=cleanup_worktrees,
        )

        # Update state
        self.state.save(self.repo_root)

        return results

    def cleanup(self) -> int:
        """Clean up all worktrees from this swarm.

        Returns:
            Number of worktrees removed
        """
        return self.worktree_manager.cleanup_all()

    def get_status(self) -> dict:
        """Get current swarm status.

        Returns:
            Dict with status summary
        """
        if not self.state:
            self.state = SwarmState.load(self.repo_root)

        if not self.state:
            return {"active": False, "message": "No active swarm"}

        summary = {
            "active": True,
            "swarm_id": self.state.id,
            "base_branch": self.state.base_branch,
            "created_at": self.state.created_at,
            "total_tasks": len(self.state.tasks),
            "pending": sum(1 for t in self.state.tasks if t.status == TaskStatus.PENDING),
            "running": sum(1 for t in self.state.tasks if t.status == TaskStatus.RUNNING),
            "completed": sum(1 for t in self.state.tasks if t.status == TaskStatus.COMPLETED),
            "failed": sum(1 for t in self.state.tasks if t.status == TaskStatus.FAILED),
            "merged": sum(1 for t in self.state.tasks if t.status == TaskStatus.MERGED),
            "tasks": [
                {
                    "slug": t.slug,
                    "title": t.title,
                    "status": t.status.value,
                    "branch": t.branch,
                    "files_modified": len(t.files_modified),
                }
                for t in self.state.tasks
            ],
        }
        return summary

    @classmethod
    def load(cls, repo_root: Path) -> Optional["SwarmRunner"]:
        """Load an existing swarm runner from state.

        Args:
            repo_root: Repository root path

        Returns:
            SwarmRunner if state exists, None otherwise
        """
        state = SwarmState.load(repo_root)
        if not state:
            return None

        runner = cls(
            repo_root=repo_root,
            base_branch=state.base_branch,
        )
        runner.state = state
        return runner
