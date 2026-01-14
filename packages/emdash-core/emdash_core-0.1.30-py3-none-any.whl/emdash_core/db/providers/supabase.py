"""Supabase database provider implementation."""

import os
from datetime import datetime
from typing import Optional

from supabase import create_client, Client

from ..models import (
    Feature,
    FeatureAssignee,
    FeaturePR,
    FeatureStatus,
    PRStatus,
    Project,
    TeamMember,
)
from ..provider import DatabaseProvider


class SupabaseProvider(DatabaseProvider):
    """Supabase implementation of the database provider."""

    def __init__(
        self,
        url: Optional[str] = None,
        key: Optional[str] = None,
        access_token: Optional[str] = None,
    ):
        """Initialize Supabase client.

        Args:
            url: Supabase project URL. Defaults to SUPABASE_URL env var.
            key: Supabase anon/service key. Defaults to SUPABASE_KEY env var.
            access_token: User's JWT access token for authenticated requests.
                         Required for RLS policies to work correctly.
        """
        self.url = url or os.getenv("SUPABASE_URL")
        self.key = key or os.getenv("SUPABASE_KEY")

        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")

        self.client: Client = create_client(self.url, self.key)

        # Set auth header for RLS if access token provided
        if access_token:
            self.client.postgrest.auth(access_token)

    def _parse_datetime(self, value: Optional[str]) -> Optional[datetime]:
        """Parse ISO datetime string from Supabase."""
        if not value:
            return None
        return datetime.fromisoformat(value.replace("Z", "+00:00"))

    def _row_to_project(self, row: dict) -> Project:
        """Convert a database row to a Project model."""
        return Project(
            id=row["id"],
            name=row["name"],
            repo_url=row.get("repo_url"),
            owner_id=row.get("owner_id"),
            created_at=self._parse_datetime(row.get("created_at")),
            updated_at=self._parse_datetime(row.get("updated_at")),
        )

    def _row_to_team_member(self, row: dict) -> TeamMember:
        """Convert a database row to a TeamMember model."""
        return TeamMember(
            id=row["id"],
            project_id=row["project_id"],
            name=row["name"],
            email=row.get("email"),
            github_handle=row.get("github_handle"),
            role=row.get("role"),
            user_id=row.get("user_id"),
            created_at=self._parse_datetime(row.get("created_at")),
        )

    def _row_to_feature(self, row: dict) -> Feature:
        """Convert a database row to a Feature model."""
        return Feature(
            id=row["id"],
            project_id=row["project_id"],
            title=row["title"],
            description=row.get("description"),
            status=FeatureStatus(row.get("status", "todo")),
            spec=row.get("spec"),
            plan=row.get("plan"),
            tasks=row.get("tasks"),
            created_at=self._parse_datetime(row.get("created_at")),
            updated_at=self._parse_datetime(row.get("updated_at")),
        )

    def _row_to_feature_pr(self, row: dict) -> FeaturePR:
        """Convert a database row to a FeaturePR model."""
        return FeaturePR(
            id=row["id"],
            feature_id=row["feature_id"],
            pr_url=row["pr_url"],
            pr_number=row["pr_number"],
            title=row.get("title"),
            status=PRStatus(row.get("status", "open")),
            created_at=self._parse_datetime(row.get("created_at")),
        )

    # -------------------------------------------------------------------------
    # Projects
    # -------------------------------------------------------------------------

    async def create_project(
        self, name: str, repo_url: Optional[str] = None, owner_id: Optional[str] = None
    ) -> Project:
        data = {"name": name, "repo_url": repo_url}
        if owner_id:
            data["owner_id"] = owner_id
        result = self.client.table("projects").insert(data).execute()
        return self._row_to_project(result.data[0])

    async def get_project(self, project_id: str) -> Optional[Project]:
        result = self.client.table("projects").select("*").eq("id", project_id).execute()
        if not result.data:
            return None
        return self._row_to_project(result.data[0])

    async def get_project_by_name(self, name: str) -> Optional[Project]:
        result = self.client.table("projects").select("*").eq("name", name).execute()
        if not result.data:
            return None
        return self._row_to_project(result.data[0])

    async def list_projects(self) -> list[Project]:
        result = self.client.table("projects").select("*").order("created_at", desc=True).execute()
        return [self._row_to_project(row) for row in result.data]

    async def get_project_by_repo_url(self, repo_url: str) -> Optional[Project]:
        """Find a project by matching repository URL.

        Normalizes URLs before comparison to handle different formats
        (git@, https://, with/without .git suffix).

        Args:
            repo_url: Repository URL to match (will be normalized)

        Returns:
            Project if found, None otherwise
        """
        from ...utils.git import normalize_repo_url

        normalized_search = normalize_repo_url(repo_url)

        # Get all projects and compare normalized URLs
        result = self.client.table("projects").select("*").execute()
        for row in result.data:
            if row.get("repo_url"):
                if normalize_repo_url(row["repo_url"]) == normalized_search:
                    return self._row_to_project(row)
        return None

    async def update_project(
        self, project_id: str, name: Optional[str] = None, repo_url: Optional[str] = None
    ) -> Optional[Project]:
        updates = {}
        if name is not None:
            updates["name"] = name
        if repo_url is not None:
            updates["repo_url"] = repo_url

        if not updates:
            return await self.get_project(project_id)

        result = self.client.table("projects").update(updates).eq("id", project_id).execute()
        if not result.data:
            return None
        return self._row_to_project(result.data[0])

    async def delete_project(self, project_id: str) -> bool:
        result = self.client.table("projects").delete().eq("id", project_id).execute()
        return len(result.data) > 0

    # -------------------------------------------------------------------------
    # Team Members
    # -------------------------------------------------------------------------

    async def create_team_member(
        self,
        project_id: str,
        name: str,
        email: Optional[str] = None,
        github_handle: Optional[str] = None,
        role: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> TeamMember:
        result = (
            self.client.table("team_members")
            .insert(
                {
                    "project_id": project_id,
                    "name": name,
                    "email": email,
                    "github_handle": github_handle,
                    "role": role,
                    "user_id": user_id,
                }
            )
            .execute()
        )
        return self._row_to_team_member(result.data[0])

    async def get_team_member(self, member_id: str) -> Optional[TeamMember]:
        result = self.client.table("team_members").select("*").eq("id", member_id).execute()
        if not result.data:
            return None
        return self._row_to_team_member(result.data[0])

    async def list_team_members(self, project_id: str) -> list[TeamMember]:
        result = (
            self.client.table("team_members")
            .select("*")
            .eq("project_id", project_id)
            .order("created_at")
            .execute()
        )
        return [self._row_to_team_member(row) for row in result.data]

    async def update_team_member(
        self,
        member_id: str,
        name: Optional[str] = None,
        email: Optional[str] = None,
        github_handle: Optional[str] = None,
        role: Optional[str] = None,
    ) -> Optional[TeamMember]:
        updates = {}
        if name is not None:
            updates["name"] = name
        if email is not None:
            updates["email"] = email
        if github_handle is not None:
            updates["github_handle"] = github_handle
        if role is not None:
            updates["role"] = role

        if not updates:
            return await self.get_team_member(member_id)

        result = self.client.table("team_members").update(updates).eq("id", member_id).execute()
        if not result.data:
            return None
        return self._row_to_team_member(result.data[0])

    async def delete_team_member(self, member_id: str) -> bool:
        result = self.client.table("team_members").delete().eq("id", member_id).execute()
        return len(result.data) > 0

    # -------------------------------------------------------------------------
    # Features
    # -------------------------------------------------------------------------

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
        result = (
            self.client.table("features")
            .insert(
                {
                    "project_id": project_id,
                    "title": title,
                    "description": description,
                    "status": status.value,
                    "spec": spec,
                    "plan": plan,
                    "tasks": tasks,
                }
            )
            .execute()
        )
        return self._row_to_feature(result.data[0])

    async def get_feature(self, feature_id: str, include_relations: bool = True) -> Optional[Feature]:
        result = self.client.table("features").select("*").eq("id", feature_id).execute()
        if not result.data:
            return None

        feature = self._row_to_feature(result.data[0])

        if include_relations:
            feature.assignees = await self.get_feature_assignees(feature_id)
            feature.prs = await self.get_feature_prs(feature_id)

        return feature

    async def list_features(
        self, project_id: str, status: Optional[FeatureStatus] = None, include_relations: bool = False
    ) -> list[Feature]:
        query = self.client.table("features").select("*").eq("project_id", project_id)

        if status:
            query = query.eq("status", status.value)

        result = query.order("created_at", desc=True).execute()
        features = [self._row_to_feature(row) for row in result.data]

        if include_relations:
            for feature in features:
                feature.assignees = await self.get_feature_assignees(feature.id)
                feature.prs = await self.get_feature_prs(feature.id)

        return features

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
        updates = {}
        if title is not None:
            updates["title"] = title
        if description is not None:
            updates["description"] = description
        if status is not None:
            updates["status"] = status.value
        if spec is not None:
            updates["spec"] = spec
        if plan is not None:
            updates["plan"] = plan
        if tasks is not None:
            updates["tasks"] = tasks

        if not updates:
            return await self.get_feature(feature_id)

        result = self.client.table("features").update(updates).eq("id", feature_id).execute()
        if not result.data:
            return None
        return self._row_to_feature(result.data[0])

    async def delete_feature(self, feature_id: str) -> bool:
        result = self.client.table("features").delete().eq("id", feature_id).execute()
        return len(result.data) > 0

    # -------------------------------------------------------------------------
    # Feature Assignees
    # -------------------------------------------------------------------------

    async def assign_feature(self, feature_id: str, team_member_id: str) -> FeatureAssignee:
        result = (
            self.client.table("feature_assignees")
            .insert({"feature_id": feature_id, "team_member_id": team_member_id})
            .execute()
        )
        row = result.data[0]
        return FeatureAssignee(
            feature_id=row["feature_id"],
            team_member_id=row["team_member_id"],
            assigned_at=self._parse_datetime(row.get("assigned_at")),
        )

    async def unassign_feature(self, feature_id: str, team_member_id: str) -> bool:
        result = (
            self.client.table("feature_assignees")
            .delete()
            .eq("feature_id", feature_id)
            .eq("team_member_id", team_member_id)
            .execute()
        )
        return len(result.data) > 0

    async def get_feature_assignees(self, feature_id: str) -> list[TeamMember]:
        result = (
            self.client.table("feature_assignees")
            .select("team_member_id, team_members(*)")
            .eq("feature_id", feature_id)
            .execute()
        )
        return [self._row_to_team_member(row["team_members"]) for row in result.data if row.get("team_members")]

    # -------------------------------------------------------------------------
    # Feature PRs
    # -------------------------------------------------------------------------

    async def add_feature_pr(
        self,
        feature_id: str,
        pr_url: str,
        pr_number: int,
        title: Optional[str] = None,
        status: PRStatus = PRStatus.OPEN,
    ) -> FeaturePR:
        result = (
            self.client.table("feature_prs")
            .insert(
                {
                    "feature_id": feature_id,
                    "pr_url": pr_url,
                    "pr_number": pr_number,
                    "title": title,
                    "status": status.value,
                }
            )
            .execute()
        )
        return self._row_to_feature_pr(result.data[0])

    async def update_feature_pr(
        self,
        pr_id: str,
        title: Optional[str] = None,
        status: Optional[PRStatus] = None,
    ) -> Optional[FeaturePR]:
        updates = {}
        if title is not None:
            updates["title"] = title
        if status is not None:
            updates["status"] = status.value

        if not updates:
            result = self.client.table("feature_prs").select("*").eq("id", pr_id).execute()
            if not result.data:
                return None
            return self._row_to_feature_pr(result.data[0])

        result = self.client.table("feature_prs").update(updates).eq("id", pr_id).execute()
        if not result.data:
            return None
        return self._row_to_feature_pr(result.data[0])

    async def remove_feature_pr(self, pr_id: str) -> bool:
        result = self.client.table("feature_prs").delete().eq("id", pr_id).execute()
        return len(result.data) > 0

    async def get_feature_prs(self, feature_id: str) -> list[FeaturePR]:
        result = (
            self.client.table("feature_prs")
            .select("*")
            .eq("feature_id", feature_id)
            .order("created_at")
            .execute()
        )
        return [self._row_to_feature_pr(row) for row in result.data]
