"""Pydantic models for agent API."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class AgentMode(str, Enum):
    """Agent operation modes."""

    CODE = "code"
    RESEARCH = "research"
    REVIEW = "review"
    SPEC = "spec"
    PLAN = "plan"


class ImageData(BaseModel):
    """Image data for vision-capable models."""

    data: str = Field(..., description="Base64 encoded image data")
    format: str = Field(default="png", description="Image format (png, jpg, etc.)")


class AgentChatOptions(BaseModel):
    """Options for agent chat."""

    max_iterations: int = Field(default=100, description="Maximum agent iterations")
    verbose: bool = Field(default=True, description="Enable verbose output")
    mode: AgentMode = Field(default=AgentMode.CODE, description="Agent mode")
    context_threshold: float = Field(
        default=0.6,
        description="Context window threshold for summarization (0-1)"
    )


class AgentChatRequest(BaseModel):
    """Request for agent chat endpoint."""

    message: str = Field(..., description="User message/task")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID for conversation continuity"
    )
    model: Optional[str] = Field(
        default=None,
        description="Model to use (defaults to server config)"
    )
    images: list[ImageData] = Field(
        default_factory=list,
        description="Images for vision-capable models"
    )
    options: AgentChatOptions = Field(
        default_factory=AgentChatOptions,
        description="Agent options"
    )


class SessionInfo(BaseModel):
    """Information about an agent session."""

    session_id: str
    agent_name: str
    model: str
    created_at: str
    message_count: int
    is_active: bool
