"""Database layer for EmDash.

Provides an abstraction over database backends with Supabase as the default implementation.
"""

import os
from typing import Optional

from .models import (
    Feature,
    FeatureAssignee,
    FeaturePR,
    FeatureStatus,
    PRStatus,
    Project,
    TeamMember,
)
from .provider import DatabaseProvider
from .providers.supabase import SupabaseProvider
from .auth import AuthProvider, User, get_auth

__all__ = [
    # Models
    "Feature",
    "FeatureAssignee",
    "FeaturePR",
    "FeatureStatus",
    "PRStatus",
    "Project",
    "TeamMember",
    "User",
    # Provider
    "DatabaseProvider",
    "SupabaseProvider",
    # Auth
    "AuthProvider",
    "get_auth",
    # Factory
    "get_provider",
]

_provider_instance: Optional[DatabaseProvider] = None


def get_provider() -> DatabaseProvider:
    """Get the configured database provider instance.

    Returns a singleton instance of the database provider.
    Currently only supports Supabase.

    Returns:
        DatabaseProvider instance

    Raises:
        ValueError: If required environment variables are not set
    """
    global _provider_instance

    if _provider_instance is None:
        provider_type = os.getenv("EMDASH_DB_PROVIDER", "supabase")

        if provider_type == "supabase":
            _provider_instance = SupabaseProvider()
        else:
            raise ValueError(f"Unknown database provider: {provider_type}")

    return _provider_instance
