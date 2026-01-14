"""GitHub OAuth authentication for EmDash."""

from .github import (
    GitHubAuth,
    AuthConfig,
    get_github_token,
    is_authenticated,
    get_auth_status,
)

__all__ = [
    "GitHubAuth",
    "AuthConfig",
    "get_github_token",
    "is_authenticated",
    "get_auth_status",
]
