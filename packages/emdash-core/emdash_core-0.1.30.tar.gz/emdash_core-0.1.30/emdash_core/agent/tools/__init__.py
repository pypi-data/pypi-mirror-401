"""Agent tools for graph exploration and code analysis.

This module provides tools that LLM agents can use to explore
code graphs, search for code, and analyze dependencies.
"""

from .base import BaseTool, ToolResult, ToolCategory

# Search tools
from .search import SemanticSearchTool, TextSearchTool, GrepTool

# Traversal tools
from .traversal import (
    ExpandNodeTool,
    GetCallersTool,
    GetCalleesTool,
    GetClassHierarchyTool,
    GetFileDependenciesTool,
    GetImpactAnalysisTool,
    GetNeighborsTool,
)

# Analytics tools
from .analytics import (
    GetAreaImportanceTool,
    GetTopPageRankTool,
    GetCommunitiesTool,
    GetCommunityMembersTool,
)

# Task tools
from .tasks import (
    TaskState,
    TaskStatus,
    Task,
    WriteTodoTool,
    UpdateTodoListTool,
    AskFollowupQuestionTool,
    AttemptCompletionTool,
)

# Plan tools
from .plan import PlanExplorationTool

# Mode tools
from .modes import AgentMode, ModeState, EnterModeTool, ExitPlanModeTool, GetModeTool

# Spec tools
from .spec import SubmitSpecTool, GetSpecTool, UpdateSpecTool

# Web tools
from .web import WebTool

# Coding tools
from .coding import (
    CodingTool,
    ReadFileTool,
    WriteToFileTool,
    ApplyDiffTool,
    DeleteFileTool,
    ListFilesTool,
    ExecuteCommandTool,
)

# GitHub MCP tools
from .github_mcp import (
    MCPBaseTool,
    GitHubSearchCodeTool,
    GitHubGetFileContentTool,
    GitHubPRDetailsTool,
    GitHubListPRsTool,
    GitHubSearchReposTool,
    GitHubSearchPRsTool,
    GitHubGetIssueTool,
    GitHubViewRepoStructureTool,
    GitHubCreateReviewTool,
)

__all__ = [
    # Base
    "BaseTool",
    "ToolResult",
    "ToolCategory",
    # Search
    "SemanticSearchTool",
    "TextSearchTool",
    "GrepTool",
    # Traversal
    "ExpandNodeTool",
    "GetCallersTool",
    "GetCalleesTool",
    "GetClassHierarchyTool",
    "GetFileDependenciesTool",
    "GetImpactAnalysisTool",
    "GetNeighborsTool",
    # Analytics
    "GetAreaImportanceTool",
    "GetTopPageRankTool",
    "GetCommunitiesTool",
    "GetCommunityMembersTool",
    # Tasks
    "TaskState",
    "TaskStatus",
    "Task",
    "WriteTodoTool",
    "UpdateTodoListTool",
    "AskFollowupQuestionTool",
    "AttemptCompletionTool",
    # Plan
    "PlanExplorationTool",
    # Mode
    "AgentMode",
    "ModeState",
    "EnterModeTool",
    "ExitPlanModeTool",
    "GetModeTool",
    # Spec
    "SubmitSpecTool",
    "GetSpecTool",
    "UpdateSpecTool",
    # Web
    "WebTool",
    # Coding
    "CodingTool",
    "ReadFileTool",
    "WriteToFileTool",
    "ApplyDiffTool",
    "DeleteFileTool",
    "ListFilesTool",
    "ExecuteCommandTool",
    # GitHub MCP tools
    "MCPBaseTool",
    "GitHubSearchCodeTool",
    "GitHubGetFileContentTool",
    "GitHubPRDetailsTool",
    "GitHubListPRsTool",
    "GitHubSearchReposTool",
    "GitHubSearchPRsTool",
    "GitHubGetIssueTool",
    "GitHubViewRepoStructureTool",
    "GitHubCreateReviewTool",
]
