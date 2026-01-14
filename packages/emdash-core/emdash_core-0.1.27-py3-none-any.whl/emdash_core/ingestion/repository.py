"""Repository management - clone, fetch, and track Git repositories."""

import hashlib
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import git
from git import Repo, GitCommandError

from ..core.exceptions import RepositoryError
from ..core.models import RepositoryEntity
from ..utils.logger import log


class RepositoryManager:
    """Manages Git repository operations (clone, fetch, status)."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize repository manager.

        Args:
            cache_dir: Directory to cache cloned repositories.
                      Defaults to ~/.emdash/repos
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".emdash" / "repos"

        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get_or_clone(
        self,
        repo_path: str,
        skip_commit_count: bool = False
    ) -> tuple[Repo, RepositoryEntity]:
        """Get a repository from cache or clone it.

        Args:
            repo_path: URL or local path to repository
            skip_commit_count: Whether to skip counting commits

        Returns:
            Tuple of (git.Repo, RepositoryEntity)

        Raises:
            RepositoryError: If repository cannot be accessed
        """
        # Check if it's a local path
        if Path(repo_path).exists():
            return self._open_local_repo(repo_path)

        # It's a URL - clone or fetch
        return self._clone_or_fetch(repo_path, skip_commit_count)

    def _open_local_repo(self, path: str) -> tuple[Repo, RepositoryEntity]:
        """Open a local repository.

        Args:
            path: Local path to repository

        Returns:
            Tuple of (git.Repo, RepositoryEntity)
        """
        log.info(f"Opening local repository: {path}")

        try:
            repo = Repo(path)

            # Get repository info
            origin_url = self._get_origin_url(repo)
            repo_name = Path(path).name

            entity = RepositoryEntity(
                url=origin_url or f"file://{path}",
                name=repo_name,
                owner=None,
                default_branch=repo.active_branch.name,
                last_ingested=None,
                ingestion_status="pending",
            )

            return repo, entity

        except Exception as e:
            raise RepositoryError(f"Failed to open local repository {path}: {e}")

    def _clone_or_fetch(
        self,
        url: str,
        skip_commit_count: bool
    ) -> tuple[Repo, RepositoryEntity]:
        """Clone a repository or fetch updates if already cloned.

        Args:
            url: Repository URL
            skip_commit_count: Whether to skip counting commits

        Returns:
            Tuple of (git.Repo, RepositoryEntity)
        """
        # Generate cache path from URL
        cache_path = self._get_cache_path(url)

        if cache_path.exists():
            log.info(f"Repository already cached at {cache_path}")
            return self._fetch_updates(cache_path, url, skip_commit_count)
        else:
            log.info(f"Cloning repository: {url}")
            return self._clone_repo(url, cache_path, skip_commit_count)

    def _clone_repo(
        self,
        url: str,
        cache_path: Path,
        skip_commit_count: bool
    ) -> tuple[Repo, RepositoryEntity]:
        """Clone a repository.

        Args:
            url: Repository URL
            cache_path: Path to clone into
            skip_commit_count: Whether to skip counting commits

        Returns:
            Tuple of (git.Repo, RepositoryEntity)
        """
        try:
            repo = Repo.clone_from(url, cache_path, depth=None)
            log.info(f"Successfully cloned {url}")

            entity = self._create_repository_entity(
                repo,
                url,
                skip_commit_count=skip_commit_count
            )
            return repo, entity

        except GitCommandError as e:
            raise RepositoryError(f"Failed to clone repository {url}: {e}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error cloning {url}: {e}")

    def _fetch_updates(
        self,
        cache_path: Path,
        url: str,
        skip_commit_count: bool
    ) -> tuple[Repo, RepositoryEntity]:
        """Fetch updates for an existing repository.

        Args:
            cache_path: Path to cached repository
            url: Repository URL
            skip_commit_count: Whether to skip counting commits

        Returns:
            Tuple of (git.Repo, RepositoryEntity)
        """
        try:
            repo = Repo(cache_path)

            log.info("Fetching updates from remote...")
            repo.remotes.origin.fetch()

            # Pull latest changes
            repo.remotes.origin.pull()

            log.info("Repository updated successfully")

            entity = self._create_repository_entity(
                repo,
                url,
                skip_commit_count=skip_commit_count
            )
            return repo, entity

        except GitCommandError as e:
            raise RepositoryError(f"Failed to fetch updates for {url}: {e}")
        except Exception as e:
            raise RepositoryError(f"Unexpected error fetching updates: {e}")

    def _create_repository_entity(
        self,
        repo: Repo,
        url: str,
        skip_commit_count: bool = False
    ) -> RepositoryEntity:
        """Create a RepositoryEntity from a git.Repo.

        Args:
            repo: Git repository
            url: Repository URL
            skip_commit_count: Whether to skip counting commits

        Returns:
            RepositoryEntity
        """
        # Parse URL to extract owner and name
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")

        if len(path_parts) >= 2:
            owner = path_parts[-2]
            repo_name = path_parts[-1].replace(".git", "")
        else:
            owner = None
            repo_name = path_parts[-1].replace(".git", "") if path_parts else "unknown"

        commit_count = 0
        if not skip_commit_count:
            try:
                commit_count = sum(1 for _ in repo.iter_commits())
            except Exception:
                commit_count = 0

        return RepositoryEntity(
            url=url,
            name=repo_name,
            owner=owner,
            default_branch=repo.active_branch.name if repo.active_branch else "main",
            last_ingested=None,
            ingestion_status="pending",
            commit_count=commit_count,
        )

    def _get_cache_path(self, url: str) -> Path:
        """Get the cache path for a repository URL.

        Args:
            url: Repository URL

        Returns:
            Path to cache directory
        """
        # Create a unique directory name from URL
        url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

        # Extract repo name from URL
        parsed = urlparse(url)
        path_parts = parsed.path.strip("/").split("/")
        repo_name = path_parts[-1].replace(".git", "")

        return self.cache_dir / f"{repo_name}_{url_hash}"

    def _get_origin_url(self, repo: Repo) -> Optional[str]:
        """Get the origin URL of a repository.

        Args:
            repo: Git repository

        Returns:
            Origin URL or None
        """
        try:
            if hasattr(repo.remotes, "origin"):
                return repo.remotes.origin.url
        except Exception:
            pass
        return None

    def get_source_files(
        self,
        repo: Repo,
        extensions: list[str],
        ignore_patterns: list[str] = None
    ) -> list[Path]:
        """Get all source files matching given extensions.

        Args:
            repo: Git repository
            extensions: List of file extensions (e.g., ['.py', '.ts', '.js'])
            ignore_patterns: Patterns to ignore (e.g., "__pycache__", "venv")

        Returns:
            List of source file paths
        """
        if ignore_patterns is None:
            ignore_patterns = [
                "__pycache__",
                "*.pyc",
                "*.pyo",
                ".git",
                ".venv",
                "venv",
                "env",
                "node_modules",
                ".tox",
                ".pytest_cache",
                "*.egg-info",
                "dist",
                "build",
            ]

        repo_path = Path(repo.working_dir)
        source_files = []

        # Normalize extensions to lowercase
        extensions = [ext.lower() for ext in extensions]

        for source_file in repo_path.rglob("*"):
            # Check if file (not directory)
            if not source_file.is_file():
                continue

            # Check extension
            if source_file.suffix.lower() not in extensions:
                continue

            # Check ignore patterns
            relative_path = source_file.relative_to(repo_path)
            if any(pattern in str(relative_path) for pattern in ignore_patterns):
                continue

            source_files.append(source_file)

        log.info(f"Found {len(source_files)} source files with extensions {extensions}")
        return source_files

    def get_python_files(self, repo: Repo, ignore_patterns: list[str] = None) -> list[Path]:
        """Get all Python files in a repository.

        Args:
            repo: Git repository
            ignore_patterns: Patterns to ignore (e.g., "__pycache__", "venv")

        Returns:
            List of Python file paths

        Note:
            This is a convenience wrapper around get_source_files() for backward compatibility.
        """
        return self.get_source_files(repo, ['.py'], ignore_patterns)

    def clear_cache(self):
        """Clear all cached repositories."""
        log.warning("Clearing repository cache...")

        if self.cache_dir.exists():
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)

        log.info("Cache cleared successfully")
