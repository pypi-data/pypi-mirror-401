"""Supabase authentication with GitHub OAuth."""

import os
from dataclasses import dataclass
from typing import Optional

from supabase import create_client, Client


@dataclass
class User:
    """Authenticated user from Supabase Auth."""

    id: str
    email: Optional[str]
    github_handle: Optional[str]
    avatar_url: Optional[str]
    access_token: Optional[str] = None


class AuthProvider:
    """Handle Supabase authentication with GitHub OAuth."""

    def __init__(self, url: Optional[str] = None, key: Optional[str] = None):
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

        self.client: Client = create_client(self.url, self.key)

    def get_github_login_url(self, redirect_to: Optional[str] = None) -> str:
        """Get the GitHub OAuth login URL.

        Args:
            redirect_to: URL to redirect after login (for web apps)

        Returns:
            GitHub OAuth URL to redirect user to
        """
        options = {}
        if redirect_to:
            options["redirect_to"] = redirect_to

        response = self.client.auth.sign_in_with_oauth(
            {"provider": "github", "options": options}
        )
        return response.url

    def sign_in_with_github_token(self, access_token: str) -> Optional[User]:
        """Sign in with an existing GitHub access token.

        Args:
            access_token: GitHub OAuth access token

        Returns:
            User if successful, None otherwise
        """
        try:
            response = self.client.auth.sign_in_with_id_token(
                {"provider": "github", "token": access_token}
            )
            return self._session_to_user(response)
        except Exception:
            return None

    def get_session(self) -> Optional[User]:
        """Get the current authenticated user from session.

        Returns:
            User if authenticated, None otherwise
        """
        try:
            response = self.client.auth.get_session()
            if response and response.user:
                return self._response_to_user(response)
            return None
        except Exception:
            return None

    def sign_out(self) -> bool:
        """Sign out the current user.

        Returns:
            True if successful
        """
        try:
            self.client.auth.sign_out()
            return True
        except Exception:
            return False

    def _session_to_user(self, session) -> Optional[User]:
        """Convert Supabase session to User model."""
        if not session or not session.user:
            return None

        user_meta = session.user.user_metadata or {}

        return User(
            id=session.user.id,
            email=session.user.email,
            github_handle=user_meta.get("user_name") or user_meta.get("preferred_username"),
            avatar_url=user_meta.get("avatar_url"),
            access_token=session.access_token if hasattr(session, "access_token") else None,
        )

    def _response_to_user(self, response) -> Optional[User]:
        """Convert Supabase auth response to User model."""
        if not response or not response.user:
            return None

        user_meta = response.user.user_metadata or {}

        return User(
            id=response.user.id,
            email=response.user.email,
            github_handle=user_meta.get("user_name") or user_meta.get("preferred_username"),
            avatar_url=user_meta.get("avatar_url"),
            access_token=response.session.access_token if response.session else None,
        )


# Singleton instance
_auth_instance: Optional[AuthProvider] = None


def get_auth() -> AuthProvider:
    """Get the auth provider instance."""
    global _auth_instance
    if _auth_instance is None:
        _auth_instance = AuthProvider()
    return _auth_instance
