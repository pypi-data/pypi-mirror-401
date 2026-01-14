"""Data models for the database layer."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class FeatureStatus(str, Enum):
    """Status of a feature in the workflow."""

    TODO = "todo"
    IN_DESIGN_REVIEW = "in_design_review"
    IN_PROGRESS = "in_progress"
    IN_PR = "in_pr"
    DONE = "done"


class PRStatus(str, Enum):
    """Status of a pull request."""

    OPEN = "open"
    MERGED = "merged"
    CLOSED = "closed"


@dataclass
class Project:
    """A project in the system."""

    id: str
    name: str
    repo_url: Optional[str] = None
    owner_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TeamMember:
    """A team member belonging to a project."""

    id: str
    project_id: str
    name: str
    email: Optional[str] = None
    github_handle: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[str] = None  # Links to auth.users
    created_at: Optional[datetime] = None


@dataclass
class Feature:
    """A feature belonging to a project."""

    id: str
    project_id: str
    title: str
    description: Optional[str] = None
    status: FeatureStatus = FeatureStatus.TODO
    spec: Optional[str] = None
    plan: Optional[str] = None
    tasks: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    # Populated by joins
    assignees: list["TeamMember"] = field(default_factory=list)
    prs: list["FeaturePR"] = field(default_factory=list)


@dataclass
class FeatureAssignee:
    """Junction table for feature-assignee many-to-many relationship."""

    feature_id: str
    team_member_id: str
    assigned_at: Optional[datetime] = None


@dataclass
class FeaturePR:
    """A pull request linked to a feature."""

    id: str
    feature_id: str
    pr_url: str
    pr_number: int
    title: Optional[str] = None
    status: PRStatus = PRStatus.OPEN
    created_at: Optional[datetime] = None
