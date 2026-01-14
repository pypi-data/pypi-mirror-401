"""Abstract database provider interface."""

from abc import ABC, abstractmethod
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


class DatabaseProvider(ABC):
    """Abstract base class for database providers.

    Implementations must provide all CRUD operations for the data models.
    """

    # -------------------------------------------------------------------------
    # Projects
    # -------------------------------------------------------------------------

    @abstractmethod
    async def create_project(
        self, name: str, repo_url: Optional[str] = None, owner_id: Optional[str] = None
    ) -> Project:
        """Create a new project.

        Args:
            name: Project name
            repo_url: GitHub repository URL
            owner_id: Auth user ID of the project owner
        """
        pass

    @abstractmethod
    async def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        pass

    @abstractmethod
    async def get_project_by_name(self, name: str) -> Optional[Project]:
        """Get a project by name."""
        pass

    @abstractmethod
    async def list_projects(self) -> list[Project]:
        """List all projects."""
        pass

    @abstractmethod
    async def update_project(
        self, project_id: str, name: Optional[str] = None, repo_url: Optional[str] = None
    ) -> Optional[Project]:
        """Update a project."""
        pass

    @abstractmethod
    async def delete_project(self, project_id: str) -> bool:
        """Delete a project and all related data."""
        pass

    # -------------------------------------------------------------------------
    # Team Members
    # -------------------------------------------------------------------------

    @abstractmethod
    async def create_team_member(
        self,
        project_id: str,
        name: str,
        email: Optional[str] = None,
        github_handle: Optional[str] = None,
        role: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> TeamMember:
        """Create a new team member.

        Args:
            project_id: Project this member belongs to
            name: Display name
            email: Email address
            github_handle: GitHub username
            role: Role in the project
            user_id: Auth user ID (links to Supabase auth.users)
        """
        pass

    @abstractmethod
    async def get_team_member(self, member_id: str) -> Optional[TeamMember]:
        """Get a team member by ID."""
        pass

    @abstractmethod
    async def list_team_members(self, project_id: str) -> list[TeamMember]:
        """List all team members for a project."""
        pass

    @abstractmethod
    async def update_team_member(
        self,
        member_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        github_handle: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Optional[TeamMember]:
        """Update a team member."""
        pass

    @abstractmethod
    async def delete_team_member(self, member_id: str) -> bool:
        """Delete a team member."""
        pass

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

    @abstractmethod
    async def create_feature(
        self,
        project_id: str,
        title: str,
        description: Optional[str] = None,
        status: FeatureStatus = FeatureStatus.TODO,
        spec: Optional[str] = None,
        plan: Optional[str] = None,
        tasks: Optional[str] = None,
    ) -> Feature:
        """Create a new feature."""
        pass

    @abstractmethod
    async def get_feature(self, feature_id: str, include_relations: bool = True) -> Optional[Feature]:
        """Get a feature by ID, optionally including assignees and PRs."""
        pass

    @abstractmethod
    async def list_features(
        self, project_id: str, status: Optional[FeatureStatus] = None, include_relations: bool = False
    ) -> list[Feature]:
        """List features for a project, optionally filtered by status."""
        pass

    @abstractmethod
    async def update_feature(
        self,
        feature_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[FeatureStatus] = None,
        spec: Optional[str] = None,
        plan: Optional[str] = None,
        tasks: Optional[str] = None,
    ) -> Optional[Feature]:
        """Update a feature."""
        pass

    @abstractmethod
    async def delete_feature(self, feature_id: str) -> bool:
        """Delete a feature and all related data."""
        pass

    # -------------------------------------------------------------------------
    # Feature Assignees
    # -------------------------------------------------------------------------

    @abstractmethod
    async def assign_feature(self, feature_id: str, team_member_id: str) -> FeatureAssignee:
        """Assign a team member to a feature."""
        pass

    @abstractmethod
    async def unassign_feature(self, feature_id: str, team_member_id: str) -> bool:
        """Remove a team member from a feature."""
        pass

    @abstractmethod
    async def get_feature_assignees(self, feature_id: str) -> list[TeamMember]:
        """Get all assignees for a feature."""
        pass

    # -------------------------------------------------------------------------
    # Feature PRs
    # -------------------------------------------------------------------------

    @abstractmethod
    async def add_feature_pr(
        self,
        feature_id: str,
        pr_url: str,
        pr_number: int,
        title: Optional[str] = None,
        status: PRStatus = PRStatus.OPEN,
    ) -> FeaturePR:
        """Add a PR to a feature."""
        pass

    @abstractmethod
    async def update_feature_pr(
        self,
        pr_id: str,
        title: Optional[str] = None,
        status: Optional[PRStatus] = None,
    ) -> Optional[FeaturePR]:
        """Update a feature PR."""
        pass

    @abstractmethod
    async def remove_feature_pr(self, pr_id: str) -> bool:
        """Remove a PR from a feature."""
        pass

    @abstractmethod
    async def get_feature_prs(self, feature_id: str) -> list[FeaturePR]:
        """Get all PRs for a feature."""
        pass
