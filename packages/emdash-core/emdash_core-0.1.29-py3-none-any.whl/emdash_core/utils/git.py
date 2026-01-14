"""Git utilities for repository detection and URL handling."""

import subprocess
from pathlib import Path
from typing import Optional


def get_git_remote_url(repo_root: Path) -> Optional[str]:
    """Get the origin remote URL from git.

    Args:
        repo_root: Path to the git repository root

    Returns:
        The remote URL or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def normalize_repo_url(url: str) -> str:
    """Normalize git URL to https format for matching.

    Handles various git URL formats:
    - git@github.com:user/repo.git -> https://github.com/user/repo
    - https://github.com/user/repo.git -> https://github.com/user/repo
    - ssh://git@github.com/user/repo.git -> https://github.com/user/repo

    Args:
        url: Git remote URL in any format

    Returns:
        Normalized https URL without .git suffix
    """
    url = url.strip()

    # Remove .git suffix
    if url.endswith(".git"):
        url = url[:-4]

    # Handle SSH format: git@github.com:user/repo
    if url.startswith("git@"):
        # git@github.com:user/repo -> https://github.com/user/repo
        url = url.replace("git@", "https://", 1)
        url = url.replace(":", "/", 1)

    # Handle ssh:// format: ssh://git@github.com/user/repo
    elif url.startswith("ssh://"):
        url = url.replace("ssh://git@", "https://", 1)
        url = url.replace("ssh://", "https://", 1)

    # Ensure https prefix
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    return url


def get_normalized_remote_url(repo_root: Path) -> Optional[str]:
    """Get the normalized origin remote URL.

    Combines get_git_remote_url and normalize_repo_url.

    Args:
        repo_root: Path to the git repository root

    Returns:
        Normalized https URL or None if not found
    """
    remote_url = get_git_remote_url(repo_root)
    if remote_url:
        return normalize_repo_url(remote_url)
    return None
