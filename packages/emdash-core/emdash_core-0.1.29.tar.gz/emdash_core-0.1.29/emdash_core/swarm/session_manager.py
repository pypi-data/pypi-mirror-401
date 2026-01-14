"""Session management for automatic worktree isolation."""

import atexit
import fcntl
import json
import os
import signal
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional
from uuid import uuid4

from .worktree_manager import WorktreeManager
from ..utils.logger import log


@dataclass
class Session:
    """An active emdash agent session."""
    id: str
    pid: int
    worktree_path: Optional[str]  # None if using main repo
    branch: Optional[str]
    started_at: str
    task_hint: str  # First task or description

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Session":
        return cls(**data)


class SessionManager:
    """Manages multiple concurrent emdash agent sessions.

    When multiple `emdash agent code` instances run:
    1. First instance uses main repo
    2. Subsequent instances get auto-created worktrees
    3. Sessions are tracked in .emdash-worktrees/.sessions.json
    4. Cleanup happens on exit

    Example:
        # Terminal 1
        $ emdash agent code "Add auth"
        # Uses main repo

        # Terminal 2 (while terminal 1 is running)
        $ emdash agent code "Fix bug"
        # Auto-creates worktree, prints message about isolation

        # Both can work in parallel without conflicts
    """

    SESSIONS_DIR = ".emdash-worktrees"
    SESSIONS_FILE = ".sessions.json"
    LOCK_FILE = ".sessions.lock"

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()
        self.sessions_dir = self.repo_root / self.SESSIONS_DIR
        self.sessions_file = self.sessions_dir / self.SESSIONS_FILE
        self.lock_file = self.sessions_dir / self.LOCK_FILE
        self.worktree_manager = WorktreeManager(repo_root)

        self.current_session: Optional[Session] = None
        self._lock_fd: Optional[int] = None

    def _ensure_dir(self):
        """Ensure sessions directory exists."""
        self.sessions_dir.mkdir(parents=True, exist_ok=True)

    def _acquire_lock(self) -> bool:
        """Acquire exclusive lock for session file operations."""
        self._ensure_dir()
        try:
            self._lock_fd = os.open(str(self.lock_file), os.O_CREAT | os.O_RDWR)
            fcntl.flock(self._lock_fd, fcntl.LOCK_EX)
            return True
        except Exception as e:
            log.warning(f"Failed to acquire session lock: {e}")
            return False

    def _release_lock(self):
        """Release the session lock."""
        if self._lock_fd is not None:
            try:
                fcntl.flock(self._lock_fd, fcntl.LOCK_UN)
                os.close(self._lock_fd)
            except Exception:
                pass
            self._lock_fd = None

    def _load_sessions(self) -> list[Session]:
        """Load current sessions from file."""
        if not self.sessions_file.exists():
            return []

        try:
            with open(self.sessions_file) as f:
                data = json.load(f)
                return [Session.from_dict(s) for s in data.get("sessions", [])]
        except Exception:
            return []

    def _save_sessions(self, sessions: list[Session]):
        """Save sessions to file."""
        self._ensure_dir()
        with open(self.sessions_file, "w") as f:
            json.dump({
                "sessions": [s.to_dict() for s in sessions],
                "updated_at": datetime.now().isoformat(),
            }, f, indent=2)

    def _is_process_alive(self, pid: int) -> bool:
        """Check if a process is still running."""
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False

    def _cleanup_dead_sessions(self, sessions: list[Session]) -> list[Session]:
        """Remove sessions from dead processes."""
        alive = []
        for session in sessions:
            if self._is_process_alive(session.pid):
                alive.append(session)
            else:
                log.debug(f"Cleaning up dead session {session.id} (pid {session.pid})")
        return alive

    def _is_main_repo_occupied(self, sessions: list[Session]) -> bool:
        """Check if any session is using the main repo."""
        for session in sessions:
            if session.worktree_path is None:
                return True
        return False

    def start_session(self, task_hint: str = "", base_branch: str | None = None) -> tuple[Path, Optional[str]]:
        """Start a new session, creating worktree if needed.

        Args:
            task_hint: Description of the task (used for worktree naming)
            base_branch: Branch to base worktree on

        Returns:
            (working_directory, branch_name or None if main repo)
        """
        self._acquire_lock()
        try:
            sessions = self._load_sessions()
            sessions = self._cleanup_dead_sessions(sessions)

            session_id = str(uuid4())[:8]
            pid = os.getpid()

            if self._is_main_repo_occupied(sessions):
                # Create worktree for this session
                slug = self._make_slug(task_hint, session_id)
                info = self.worktree_manager.create_worktree(
                    task_name=slug,
                    base_branch=base_branch,
                    force=True,
                )

                self.current_session = Session(
                    id=session_id,
                    pid=pid,
                    worktree_path=str(info.path),
                    branch=info.branch,
                    started_at=datetime.now().isoformat(),
                    task_hint=task_hint[:100] if task_hint else "",
                )

                sessions.append(self.current_session)
                self._save_sessions(sessions)

                # Register cleanup handlers
                self._register_cleanup()

                return info.path, info.branch
            else:
                # Use main repo
                self.current_session = Session(
                    id=session_id,
                    pid=pid,
                    worktree_path=None,
                    branch=None,
                    started_at=datetime.now().isoformat(),
                    task_hint=task_hint[:100] if task_hint else "",
                )

                sessions.append(self.current_session)
                self._save_sessions(sessions)

                # Register cleanup handlers
                self._register_cleanup()

                return self.repo_root, None

        finally:
            self._release_lock()

    def _make_slug(self, task_hint: str, session_id: str) -> str:
        """Create a slug for the worktree."""
        import re
        if task_hint:
            slug = task_hint.lower().strip()
            slug = re.sub(r"[^\w\s-]", "", slug)
            slug = re.sub(r"[-\s]+", "-", slug)
            slug = slug[:30]
        else:
            slug = f"session-{session_id}"
        return slug

    def end_session(self):
        """End the current session."""
        if not self.current_session:
            return

        self._acquire_lock()
        try:
            sessions = self._load_sessions()
            sessions = [s for s in sessions if s.id != self.current_session.id]
            self._save_sessions(sessions)

            # Note: We don't auto-delete the worktree - user may want to merge
            log.info(f"Session {self.current_session.id} ended")

            if self.current_session.worktree_path:
                log.info(f"Worktree preserved at: {self.current_session.worktree_path}")
                log.info(f"Branch: {self.current_session.branch}")

        finally:
            self._release_lock()
            self.current_session = None

    def _register_cleanup(self):
        """Register cleanup handlers for process exit."""
        atexit.register(self.end_session)

        # Handle signals
        def signal_handler(signum, frame):
            self.end_session()
            sys.exit(0)

        try:
            signal.signal(signal.SIGTERM, signal_handler)
            signal.signal(signal.SIGINT, signal_handler)
        except Exception:
            pass  # May fail in non-main thread

    def get_active_sessions(self) -> list[Session]:
        """Get list of currently active sessions."""
        self._acquire_lock()
        try:
            sessions = self._load_sessions()
            return self._cleanup_dead_sessions(sessions)
        finally:
            self._release_lock()

    def is_using_worktree(self) -> bool:
        """Check if current session is using a worktree."""
        return self.current_session is not None and self.current_session.worktree_path is not None

    def get_current_branch(self) -> Optional[str]:
        """Get branch name if using worktree."""
        if self.current_session:
            return self.current_session.branch
        return None
