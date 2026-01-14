"""Task definitions and state for swarm execution."""

from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Optional, Any
from datetime import datetime
import json


class TaskStatus(Enum):
    """Status of a swarm task."""
    PENDING = "pending"
    WORKTREE_CREATED = "worktree_created"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    MERGED = "merged"


@dataclass
class SwarmTask:
    """A task to be executed by a swarm worker.

    Each task gets its own worktree and subprocess.
    State is persisted to {worktree}/.emdash-task/task.json
    """
    # Core identity
    id: str
    slug: str
    title: str
    description: str

    # Git context
    base_branch: str = "main"
    branch: str = ""
    worktree_path: Optional[str] = None

    # Status tracking
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    started_at: Optional[str] = None
    completed_at: Optional[str] = None

    # Results
    files_modified: list[str] = field(default_factory=list)
    completion_summary: Optional[str] = None
    error_message: Optional[str] = None
    agent_output: Optional[str] = None

    # Merge status
    merge_status: Optional[str] = None
    merge_conflicts: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d["status"] = self.status.value
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SwarmTask":
        """Create from dictionary."""
        data = data.copy()
        data["status"] = TaskStatus(data["status"])
        return cls(**data)

    def save(self, worktree_path: Path) -> None:
        """Save task state to worktree."""
        task_dir = worktree_path / ".emdash-task"
        task_dir.mkdir(parents=True, exist_ok=True)

        task_file = task_dir / "task.json"
        with open(task_file, "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, worktree_path: Path) -> Optional["SwarmTask"]:
        """Load task state from worktree."""
        task_file = worktree_path / ".emdash-task" / "task.json"
        if not task_file.exists():
            return None

        with open(task_file) as f:
            return cls.from_dict(json.load(f))


@dataclass
class SwarmState:
    """Overall state of a swarm execution.

    Persisted to {repo}/.emdash-worktrees/.swarm-state.json
    """
    id: str
    tasks: list[SwarmTask]
    base_branch: str = "main"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None

    def save(self, repo_root: Path) -> None:
        """Save swarm state to repo root."""
        state_file = repo_root / ".emdash-worktrees" / ".swarm-state.json"
        state_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "id": self.id,
            "tasks": [t.to_dict() for t in self.tasks],
            "base_branch": self.base_branch,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
            "summary": {
                "total": len(self.tasks),
                "completed": sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED),
                "failed": sum(1 for t in self.tasks if t.status == TaskStatus.FAILED),
                "merged": sum(1 for t in self.tasks if t.status == TaskStatus.MERGED),
            },
        }
        with open(state_file, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, repo_root: Path) -> Optional["SwarmState"]:
        """Load swarm state from repo root."""
        state_file = repo_root / ".emdash-worktrees" / ".swarm-state.json"
        if not state_file.exists():
            return None

        with open(state_file) as f:
            data = json.load(f)
            tasks = [SwarmTask.from_dict(t) for t in data.get("tasks", [])]
            return cls(
                id=data["id"],
                tasks=tasks,
                base_branch=data.get("base_branch", "main"),
                created_at=data.get("created_at", ""),
                completed_at=data.get("completed_at"),
            )
