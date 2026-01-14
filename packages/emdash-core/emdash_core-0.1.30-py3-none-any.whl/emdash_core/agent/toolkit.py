"""Main AgentToolkit class for LLM agent graph exploration."""

from pathlib import Path
from typing import Optional

from ..graph.connection import KuzuConnection, get_connection
from .tools.base import BaseTool, ToolResult, ToolCategory
from .session import AgentSession
from ..utils.logger import log


class AgentToolkit:
    """Main entry point for LLM agent graph exploration.

    Provides a unified interface for executing graph exploration tools
    and managing exploration session state.

    Example:
        toolkit = AgentToolkit()

        # Search for relevant code
        result = toolkit.search("user authentication")

        # Expand the top result
        if result.success:
            top = result.data["results"][0]
            expanded = toolkit.expand(top["type"], top["qualified_name"])

        # Get OpenAI schemas for function calling
        schemas = toolkit.get_all_schemas()

        # With custom MCP servers
        toolkit = AgentToolkit(mcp_config_path=Path(".emdash/mcp.json"))
    """

    def __init__(
        self,
        connection: Optional[KuzuConnection] = None,
        enable_session: bool = True,
        mcp_config_path: Optional[Path] = None,
        repo_root: Optional[Path] = None,
        plan_mode: bool = False,
        save_spec_path: Optional[Path] = None,
    ):
        """Initialize the agent toolkit.

        Args:
            connection: Kuzu connection. If None, uses global connection.
            enable_session: Whether to track exploration state across calls.
            mcp_config_path: Path to MCP config file for dynamic tool registration.
                           If None, checks for .emdash/mcp.json in cwd.
            repo_root: Root directory of the repository for file operations.
                      If None, uses repo_root from config or current working directory.
            plan_mode: Whether to include spec planning tools and restrict to read-only.
            save_spec_path: If provided, specs will be saved to this path.
        """
        self.connection = connection or get_connection()
        self.session = AgentSession() if enable_session else None
        self._tools: dict[str, BaseTool] = {}
        self._mcp_manager = None
        self._mcp_config_path = mcp_config_path
        self.plan_mode = plan_mode
        self.save_spec_path = save_spec_path

        # Get repo_root from config if not explicitly provided
        if repo_root is None:
            from ..config import get_config
            config = get_config()
            if config.repo_root:
                repo_root = Path(config.repo_root)
        self._repo_root = repo_root or Path.cwd()

        # Configure mode state and spec state if plan mode
        if plan_mode:
            from .tools.modes import ModeState, AgentMode
            mode_state = ModeState.get_instance()
            mode_state.current_mode = AgentMode.PLAN

            from .tools.spec import SpecState
            spec_state = SpecState.get_instance()
            spec_state.configure(save_path=save_spec_path)

        self._register_default_tools()

        # Register dynamic MCP tools from config
        self._init_mcp_manager()

    def _register_default_tools(self) -> None:
        """Register all built-in tools."""
        # Import tools here to avoid circular imports
        from .tools.search import (
            SemanticSearchTool,
            # TextSearchTool,  # Disabled due to DB locking issues
            GrepTool,
            GlobTool,
        )
        from .tools.web import WebTool
        from .tools.coding import (
            ReadFileTool,
            ListFilesTool,
        )

        # Register search tools
        self.register_tool(SemanticSearchTool(self.connection))
        # self.register_tool(TextSearchTool(self.connection))  # Disabled due to DB locking issues
        self.register_tool(GrepTool(self.connection))
        self.register_tool(GlobTool(self.connection))
        self.register_tool(WebTool(self.connection))

        # Register skill tools and load skills
        self._register_skill_tools()

        # Register read-only file tools (always available)
        self.register_tool(ReadFileTool(self._repo_root, self.connection))
        self.register_tool(ListFilesTool(self._repo_root, self.connection))

        # Register write tools (only in non-plan mode)
        if not self.plan_mode:
            from .tools.coding import (
                WriteToFileTool,
                ApplyDiffTool,
                DeleteFileTool,
                ExecuteCommandTool,
            )
            self.register_tool(WriteToFileTool(self._repo_root, self.connection))
            self.register_tool(ApplyDiffTool(self._repo_root, self.connection))
            self.register_tool(DeleteFileTool(self._repo_root, self.connection))
            self.register_tool(ExecuteCommandTool(self._repo_root, self.connection))

        # Register sub-agent tools for spawning lightweight agents
        self._register_subagent_tools()

        # Register mode tools
        self._register_mode_tools()

        # Register task management tools
        # In plan mode: only register ask_followup_question for clarifications
        # In code mode: register all task tools
        if self.plan_mode:
            self._register_plan_mode_task_tools()
        else:
            self._register_task_tools()

        # Register spec planning tools (only in plan mode)
        if self.plan_mode:
            self._register_spec_tools()

        # Traversal tools (expand_node, get_callers, etc.) and analytics tools
        # (get_area_importance, get_top_pagerank, etc.) are now provided
        # by the emdash-graph MCP server - registered via _init_mcp_manager()

        # NOTE: GitHub MCP tools are registered via _init_mcp_manager()
        # from the MCP config file (e.g., .emdash/mcp.json)
        # This allows using the official github-mcp-server directly

        log.debug(f"Registered {len(self._tools)} agent tools")

    def _register_subagent_tools(self) -> None:
        """Register sub-agent tools for spawning lightweight agents.

        These tools allow spawning specialized sub-agents as subprocesses
        for focused tasks like exploration and planning.
        """
        from .tools.task import TaskTool
        from .tools.task_output import TaskOutputTool

        self.register_tool(TaskTool(repo_root=self._repo_root, connection=self.connection))
        self.register_tool(TaskOutputTool(repo_root=self._repo_root, connection=self.connection))

    def _register_mode_tools(self) -> None:
        """Register mode switching tools.

        - enter_mode: Available in code mode to enter other modes (e.g., plan)
        - exit_plan: Available in plan mode to submit plan and request approval
        - get_mode: Always available to check current mode
        """
        from .tools.modes import EnterModeTool, ExitPlanModeTool, GetModeTool

        # get_mode is always available
        self.register_tool(GetModeTool())

        if self.plan_mode:
            # In plan mode: can exit with plan submission
            self.register_tool(ExitPlanModeTool())
        else:
            # In code mode: can enter other modes
            self.register_tool(EnterModeTool())

    def _register_plan_mode_task_tools(self) -> None:
        """Register subset of task tools for plan mode.

        In plan mode, the agent can ask clarifying questions but
        doesn't need completion/todo tools since exit_plan handles that.
        """
        from .tools.tasks import AskFollowupQuestionTool
        self.register_tool(AskFollowupQuestionTool())

    def _register_task_tools(self) -> None:
        """Register task management tools.

        These tools enable structured task tracking with todos,
        user interaction via follow-up questions, and completion signaling.
        """
        from .tools.tasks import (
            WriteTodoTool,
            UpdateTodoListTool,
            AskFollowupQuestionTool,
            AttemptCompletionTool,
        )

        self.register_tool(WriteTodoTool())
        self.register_tool(UpdateTodoListTool())
        self.register_tool(AskFollowupQuestionTool())
        self.register_tool(AttemptCompletionTool())

    def _register_spec_tools(self) -> None:
        """Register spec planning tools.

        These tools are only available in plan_mode and enable
        structured specification output.
        """
        from .tools.spec import (
            SubmitSpecTool,
            GetSpecTool,
            UpdateSpecTool,
        )

        self.register_tool(SubmitSpecTool())
        self.register_tool(GetSpecTool())
        self.register_tool(UpdateSpecTool())

    def _register_skill_tools(self) -> None:
        """Register skill tools and load skills from .emdash/skills/.

        Skills are markdown-based instruction files that teach the agent
        how to perform specific, repeatable tasks. Similar to Claude Code's
        skills system.
        """
        from .tools.skill import SkillTool, ListSkillsTool
        from .skills import SkillRegistry

        # Load skills from .emdash/skills/
        skills_dir = self._repo_root / ".emdash" / "skills"
        registry = SkillRegistry.get_instance()
        registry.load_skills(skills_dir)

        # Register skill tools
        self.register_tool(SkillTool(self.connection))
        self.register_tool(ListSkillsTool(self.connection))

        skills_count = len(registry.list_skills())
        if skills_count > 0:
            log.info(f"Registered skill tools with {skills_count} skills available")

    def _register_mcp_tools(self) -> None:
        """Register GitHub MCP tools if available.

        MCP tools provide enhanced GitHub research capabilities including
        code search, file content retrieval, and rich PR analysis.
        These tools require:
        - GITHUB_TOKEN or GITHUB_PERSONAL_ACCESS_TOKEN environment variable
        - github-mcp-server binary installed
        """
        from .tools.github_mcp import (
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
        from ..core.config import get_config

        config = get_config()

        # Only register MCP tools if token is available
        if not config.mcp.is_available:
            log.debug("GitHub MCP tools not registered (no token configured)")
            return

        # Register GitHub MCP tools
        self.register_tool(GitHubSearchCodeTool(self.connection))
        self.register_tool(GitHubGetFileContentTool(self.connection))
        self.register_tool(GitHubPRDetailsTool(self.connection))
        self.register_tool(GitHubListPRsTool(self.connection))
        self.register_tool(GitHubSearchReposTool(self.connection))
        self.register_tool(GitHubSearchPRsTool(self.connection))
        self.register_tool(GitHubGetIssueTool(self.connection))
        self.register_tool(GitHubViewRepoStructureTool(self.connection))
        self.register_tool(GitHubCreateReviewTool(self.connection))

        log.debug("Registered 8 GitHub MCP tools")

    def _init_mcp_manager(self) -> None:
        """Initialize MCP manager and register dynamic tools from config.

        This method loads the MCP configuration file and registers all tools
        from enabled MCP servers. It's called after default tool registration.
        Creates default MCP config if it doesn't exist.
        """
        from .mcp import (
            MCPServerManager,
            get_default_mcp_config_path,
            create_tools_from_mcp,
        )
        from .mcp.config import ensure_mcp_config

        # Determine config path
        config_path = self._mcp_config_path
        if config_path is None:
            config_path = get_default_mcp_config_path()

        # Ensure MCP config exists (creates default with github + emdash-graph)
        ensure_mcp_config(config_path)

        try:
            # Create manager
            self._mcp_manager = MCPServerManager(config_path=config_path)

            # Create and register dynamic tools
            tools = create_tools_from_mcp(self._mcp_manager, self.connection)
            for tool in tools:
                # Skip if tool name conflicts with existing tool
                if tool.name in self._tools:
                    log.warning(f"Skipping MCP tool '{tool.name}': conflicts with existing tool")
                    continue
                self.register_tool(tool)

            if tools:
                log.info(f"Registered {len(tools)} dynamic MCP tools from config")

        except Exception as e:
            log.warning(f"Failed to initialize MCP manager: {e}")
            self._mcp_manager = None

    def get_mcp_manager(self):
        """Get the MCP manager instance.

        Returns:
            MCPServerManager or None if not initialized
        """
        return self._mcp_manager

    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool.

        Args:
            tool: Tool instance to register
        """
        self._tools[tool.name] = tool

    def set_emitter(self, emitter) -> None:
        """Inject emitter into tools that need it.

        This should be called by the runner after toolkit creation
        to enable event streaming from tools like TaskTool.

        Args:
            emitter: AgentEventEmitter for streaming events
        """
        # Inject emitter into TaskTool for sub-agent event streaming
        task_tool = self.get_tool("task")
        if task_tool and hasattr(task_tool, "emitter"):
            task_tool.emitter = emitter
            log.debug("Injected emitter into TaskTool")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name.

        Args:
            name: Tool name

        Returns:
            Tool instance or None if not found
        """
        return self._tools.get(name)

    def list_tools(self) -> list[dict]:
        """List all available tools.

        Returns:
            List of tool info dicts with name, description, category
        """
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "category": tool.category.value,
            }
            for tool in self._tools.values()
        ]

    def execute(self, tool_name: str, **params) -> ToolResult:
        """Execute a tool by name with parameters.

        Args:
            tool_name: Name of the tool to execute
            **params: Tool-specific parameters

        Returns:
            ToolResult with success/data or error
        """
        tool = self.get_tool(tool_name)

        if not tool:
            return ToolResult.error_result(
                f"Unknown tool: {tool_name}",
                suggestions=[f"Available tools: {list(self._tools.keys())}"],
            )

        try:
            result = tool.execute(**params)

            # Track in session if enabled
            if self.session:
                self.session.record_action(tool_name, params, result)

            return result

        except Exception as e:
            log.exception(f"Tool execution error: {tool_name}")
            return ToolResult.error_result(
                f"Tool execution failed: {str(e)}",
                suggestions=["Check the parameters and try again"],
            )

    def get_all_schemas(self) -> list[dict]:
        """Get OpenAI function calling schemas for all tools.

        Returns:
            List of OpenAI function schemas
        """
        return [tool.get_schema() for tool in self._tools.values()]

    def get_schemas_by_category(self, category: str) -> list[dict]:
        """Get schemas for tools in a specific category.

        Args:
            category: Category name (search, traversal, analytics, history, planning)

        Returns:
            List of OpenAI function schemas for that category
        """
        return [
            tool.get_schema()
            for tool in self._tools.values()
            if tool.category.value == category
        ]

    def get_tools_by_category(self, category: str) -> list[BaseTool]:
        """Get all tools in a category.

        Args:
            category: Category name

        Returns:
            List of tool instances
        """
        return [
            tool
            for tool in self._tools.values()
            if tool.category.value == category
        ]

    def get_session_context(self) -> Optional[dict]:
        """Get current session context summary.

        Returns:
            Session context dict or None if session disabled
        """
        if self.session:
            return self.session.get_context_summary()
        return None

    def get_exploration_steps(self) -> list:
        """Get exploration steps from the current session.

        Returns:
            List of ExplorationStep objects or empty list if session disabled
        """
        if self.session:
            return self.session.steps
        return []

    def reset_session(self) -> None:
        """Reset the exploration session state."""
        if self.session:
            self.session.reset()
        # Also reset task state
        from .tools.tasks import TaskState
        TaskState.reset()
        # Also reset spec state if in plan mode
        if self.plan_mode:
            from .tools.spec import SpecState
            SpecState.reset()

    # Convenience methods for common operations

    def search(self, query: str, **kwargs) -> ToolResult:
        """Convenience method for semantic search.

        Args:
            query: Natural language search query
            **kwargs: Additional parameters (entity_types, limit, min_score)

        Returns:
            ToolResult with matching entities
        """
        return self.execute("semantic_search", query=query, **kwargs)

    def expand(
        self,
        node_type: str,
        identifier: str,
        **kwargs,
    ) -> ToolResult:
        """Convenience method for node expansion.

        Args:
            node_type: Type of node (Function, Class, File)
            identifier: Qualified name or file path
            **kwargs: Additional parameters (max_hops)

        Returns:
            ToolResult with expanded graph context
        """
        return self.execute(
            "expand_node",
            node_type=node_type,
            identifier=identifier,
            **kwargs,
        )

    # def plan(self, goal: str, **kwargs) -> ToolResult:
    #     """Convenience method for exploration planning.
    #
    #     Args:
    #         goal: What you're trying to understand or accomplish
    #         **kwargs: Additional parameters (context, constraints, exploration_depth)
    #
    #     Returns:
    #         ToolResult with exploration plan
    #     """
    #     return self.execute("plan_exploration", goal=goal, **kwargs)  # Disabled
