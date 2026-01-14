"""Intelligent merge agent for combining parallel work."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TYPE_CHECKING

from git import Repo

from .task_definition import SwarmTask, TaskStatus
from .worktree_manager import WorktreeManager
from ..utils.logger import log

# Optional agent providers import (for LLM-assisted merging)
try:
    from ..agent.providers import get_provider
    from ..agent.providers.factory import DEFAULT_MODEL
    _HAS_AGENT_PROVIDERS = True
except ImportError:
    _HAS_AGENT_PROVIDERS = False
    DEFAULT_MODEL = "gpt-4o-mini"
    get_provider = None  # type: ignore


@dataclass
class MergeResult:
    """Result of merging a task branch."""
    task_id: str
    success: bool
    merge_type: str  # fast-forward, merge, rebase, manual, skipped
    conflicts: list[str]
    commit_sha: Optional[str]
    error_message: Optional[str]


MERGE_AGENT_PROMPT = """You are an expert software engineer merging multiple feature branches.

## Completed Tasks (Already Merged)
{task_summaries}

## Current Branch to Merge
Branch: {current_branch}
Task: {task_title}
Files modified: {files_modified}

## Merge Conflicts Detected
{conflict_files}

## Conflict Content
{conflict_content}

## Instructions
Analyze the conflicts and provide resolution guidance. For each conflict:
1. Understand what both sides are trying to do
2. Determine if changes are complementary (combine) or contradictory (choose one)
3. Provide the resolved content

Output your analysis as JSON:
```json
{{
  "analysis": "Brief analysis of the conflicts",
  "resolutions": [
    {{
      "file": "path/to/file",
      "strategy": "combine|keep_ours|keep_theirs",
      "explanation": "Why this resolution",
      "resolved_content": "The merged content (if strategy is combine)"
    }}
  ],
  "commit_message": "Suggested merge commit message"
}}
```
"""


class MergeAgent:
    """Intelligently merges completed task branches.

    Uses LLM to analyze changes and resolve conflicts when needed.
    Falls back to manual intervention for complex conflicts.

    Example:
        agent = MergeAgent(repo_root=Path("."))

        # Merge all completed tasks
        results = agent.merge_all_completed(tasks, target_branch="main")

        # Or merge with AI assistance
        results = agent.merge_with_assistance(tasks, model="gpt-4o")
    """

    def __init__(self, repo_root: Path, model: str = DEFAULT_MODEL):
        self.repo_root = repo_root.resolve()
        self.repo = Repo(repo_root)
        self.model = model
        self.worktree_manager = WorktreeManager(repo_root)

    def get_branch_diff_summary(self, branch: str, base: str = "main") -> dict:
        """Get summary of changes on a branch."""
        try:
            # Get list of changed files
            diff = self.repo.git.diff(f"{base}...{branch}", name_only=True)
            files = diff.strip().split("\n") if diff.strip() else []

            # Get commit count
            commits = self.repo.git.rev_list(f"{base}..{branch}", count=True)

            # Get diff stats
            stat = self.repo.git.diff(f"{base}...{branch}", stat=True)

            return {
                "branch": branch,
                "files_changed": files,
                "commit_count": int(commits) if commits else 0,
                "stat_summary": stat[-500:] if stat else "",
            }
        except Exception as e:
            log.warning(f"Failed to get diff summary for {branch}: {e}")
            return {
                "branch": branch,
                "files_changed": [],
                "commit_count": 0,
                "stat_summary": "",
            }

    def attempt_fast_forward(self, branch: str, target: str = "main") -> MergeResult:
        """Try fast-forward merge (cleanest option)."""
        try:
            # Check if FF is possible
            merge_base = self.repo.git.merge_base(target, branch)
            target_sha = self.repo.refs[target].commit.hexsha

            if merge_base == target_sha:
                # Fast-forward possible
                self.repo.git.checkout(target)
                self.repo.git.merge(branch, ff_only=True)

                return MergeResult(
                    task_id="",
                    success=True,
                    merge_type="fast-forward",
                    conflicts=[],
                    commit_sha=self.repo.head.commit.hexsha,
                    error_message=None,
                )
        except Exception:
            pass

        return MergeResult(
            task_id="",
            success=False,
            merge_type="none",
            conflicts=[],
            commit_sha=None,
            error_message="Fast-forward not possible",
        )

    def attempt_merge(self, branch: str, target: str = "main") -> MergeResult:
        """Try standard merge."""
        try:
            self.repo.git.checkout(target)

            try:
                self.repo.git.merge(branch, no_ff=True, m=f"Merge {branch}")

                return MergeResult(
                    task_id="",
                    success=True,
                    merge_type="merge",
                    conflicts=[],
                    commit_sha=self.repo.head.commit.hexsha,
                    error_message=None,
                )
            except Exception as e:
                # Check for conflicts
                status = self.repo.git.status(porcelain=True)
                conflicts = []
                for line in status.split("\n"):
                    if line.startswith("UU ") or line.startswith("AA "):
                        conflicts.append(line[3:])

                # Abort the merge
                try:
                    self.repo.git.merge(abort=True)
                except Exception:
                    pass

                return MergeResult(
                    task_id="",
                    success=False,
                    merge_type="conflicts",
                    conflicts=conflicts,
                    commit_sha=None,
                    error_message=str(e),
                )

        except Exception as e:
            return MergeResult(
                task_id="",
                success=False,
                merge_type="error",
                conflicts=[],
                commit_sha=None,
                error_message=str(e),
            )

    def get_conflict_content(self, files: list[str]) -> str:
        """Get the content of conflicted files."""
        content_parts = []
        for file_path in files[:5]:  # Limit to 5 files
            try:
                full_path = self.repo_root / file_path
                if full_path.exists():
                    content = full_path.read_text()
                    # Only include conflict markers section
                    if "<<<<<<<" in content:
                        content_parts.append(f"### {file_path}\n```\n{content[:3000]}\n```")
            except Exception:
                pass
        return "\n\n".join(content_parts) if content_parts else "No conflict content available"

    def merge_with_llm_assistance(
        self,
        task: SwarmTask,
        target: str = "main",
        other_tasks: Optional[list[SwarmTask]] = None,
    ) -> MergeResult:
        """Use LLM to help with merge strategy and conflict resolution."""
        if not _HAS_AGENT_PROVIDERS or get_provider is None:
            log.warning("Agent providers not available, falling back to standard merge")
            return self.attempt_merge(task.branch, target)

        provider = get_provider(self.model)

        # First, try a normal merge to see if there are conflicts
        self.repo.git.checkout(target)
        try:
            self.repo.git.merge(task.branch, no_commit=True, no_ff=True)
            # No conflicts - commit the merge
            self.repo.git.commit(m=f"Merge {task.branch}: {task.title}")
            return MergeResult(
                task_id=task.id,
                success=True,
                merge_type="merge",
                conflicts=[],
                commit_sha=self.repo.head.commit.hexsha,
                error_message=None,
            )
        except Exception:
            pass

        # There are conflicts - get their details
        status = self.repo.git.status(porcelain=True)
        conflicts = []
        for line in status.split("\n"):
            if line.startswith("UU ") or line.startswith("AA "):
                conflicts.append(line[3:])

        if not conflicts:
            # No conflicts detected, abort and return
            try:
                self.repo.git.merge(abort=True)
            except Exception:
                pass
            return MergeResult(
                task_id=task.id,
                success=False,
                merge_type="error",
                conflicts=[],
                commit_sha=None,
                error_message="Merge failed without detectable conflicts",
            )

        # Get conflict content for LLM
        conflict_content = self.get_conflict_content(conflicts)

        # Build context for LLM
        task_summaries = []
        for t in (other_tasks or []):
            if t.status == TaskStatus.MERGED:
                task_summaries.append(f"- {t.title}: {t.completion_summary or 'No summary'}")

        diff_info = self.get_branch_diff_summary(task.branch, target)

        prompt = MERGE_AGENT_PROMPT.format(
            task_summaries="\n".join(task_summaries) or "None yet",
            current_branch=task.branch,
            task_title=task.title,
            files_modified=", ".join(diff_info["files_changed"][:20]),
            conflict_files=", ".join(conflicts),
            conflict_content=conflict_content,
        )

        # Get LLM recommendation
        messages = [{"role": "user", "content": prompt}]
        response = provider.chat(messages)

        # Log the LLM's analysis
        log.info(f"LLM merge analysis for {task.slug}: {response.content[:500] if response.content else 'No response'}")

        # For now, abort and mark as needing manual intervention
        # A more sophisticated version would parse the JSON and apply resolutions
        try:
            self.repo.git.merge(abort=True)
        except Exception:
            pass

        return MergeResult(
            task_id=task.id,
            success=False,
            merge_type="manual",
            conflicts=conflicts,
            commit_sha=None,
            error_message=f"LLM analysis complete. Manual resolution needed. See logs for guidance.",
        )

    def merge_all_completed(
        self,
        tasks: list[SwarmTask],
        target: str = "main",
        use_llm: bool = False,
        cleanup_worktrees: bool = True,
    ) -> list[MergeResult]:
        """Merge all completed tasks in order.

        Args:
            tasks: All tasks (will filter to completed ones)
            target: Target branch to merge into
            use_llm: Whether to use LLM for merge assistance
            cleanup_worktrees: Whether to delete worktrees after successful merge

        Returns:
            List of merge results
        """
        results = []
        completed_tasks = [t for t in tasks if t.status == TaskStatus.COMPLETED]

        if not completed_tasks:
            log.info("No completed tasks to merge")
            return results

        # Sort by completion time (merge earlier completions first)
        completed_tasks.sort(key=lambda t: t.completed_at or "")

        merged_tasks: list[SwarmTask] = []

        for task in completed_tasks:
            log.info(f"Merging task: {task.title} ({task.branch})")

            # Try fast-forward first
            result = self.attempt_fast_forward(task.branch, target)

            if not result.success:
                if use_llm:
                    result = self.merge_with_llm_assistance(task, target, merged_tasks)
                else:
                    result = self.attempt_merge(task.branch, target)

            result.task_id = task.id
            results.append(result)

            # Update task status
            if result.success:
                task.status = TaskStatus.MERGED
                task.merge_status = "success"
                merged_tasks.append(task)

                # Clean up worktree after successful merge
                if cleanup_worktrees and task.slug:
                    try:
                        self.worktree_manager.remove_worktree(task.slug)
                        log.info(f"Cleaned up worktree for merged task: {task.slug}")
                    except Exception as e:
                        log.warning(f"Failed to clean up worktree {task.slug}: {e}")
            else:
                task.merge_status = "conflicts"
                task.merge_conflicts = result.conflicts

                # Save updated task state (only if not cleaned up)
                if task.worktree_path:
                    task.save(Path(task.worktree_path))

        return results
