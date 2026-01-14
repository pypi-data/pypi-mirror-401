"""Agent runner for LLM-powered exploration."""

import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date
from typing import Any, Optional

from ..utils.logger import log
from ..core.config import get_config
from ..core.exceptions import ContextLengthError
from .toolkit import AgentToolkit
from .events import AgentEventEmitter, NullEmitter
from .providers import get_provider
from .providers.factory import DEFAULT_MODEL
from .context_manager import (
    truncate_tool_output,
    reduce_context_for_retry,
    is_context_overflow_error,
)
from .prompts import BASE_SYSTEM_PROMPT, build_system_prompt
from .tools.tasks import TaskState
from ..checkpoint import CheckpointManager


class SafeJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles Neo4j types and other non-serializable objects."""

    def default(self, obj: Any) -> Any:
        # Handle datetime objects
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()

        # Handle Neo4j DateTime
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()

        # Handle Neo4j Date, Time, etc.
        if hasattr(obj, 'to_native'):
            return str(obj.to_native())

        # Handle sets
        if isinstance(obj, set):
            return list(obj)

        # Handle bytes
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')

        # Fallback to string representation
        try:
            return str(obj)
        except Exception:
            return f"<non-serializable: {type(obj).__name__}>"


class AgentRunner:
    """Runs an LLM agent with tool access for code exploration.

    Example:
        runner = AgentRunner()
        response = runner.run("How does authentication work in this codebase?")
        print(response)
    """

    def __init__(
        self,
        toolkit: Optional[AgentToolkit] = None,
        model: str = DEFAULT_MODEL,
        system_prompt: Optional[str] = None,
        emitter: Optional[AgentEventEmitter] = None,
        max_iterations: int = int(os.getenv("EMDASH_MAX_ITERATIONS", "100")),
        verbose: bool = False,
        show_tool_results: bool = False,
        enable_thinking: Optional[bool] = None,
        checkpoint_manager: Optional[CheckpointManager] = None,
    ):
        """Initialize the agent runner.

        Args:
            toolkit: AgentToolkit instance. If None, creates default.
            model: LLM model to use.
            system_prompt: Custom system prompt. If None, uses default.
            emitter: Event emitter for streaming output.
            max_iterations: Maximum tool call iterations.
            verbose: Whether to print verbose output.
            show_tool_results: Whether to show detailed tool results.
            enable_thinking: Enable extended thinking. If None, auto-detect from model.
            checkpoint_manager: Optional checkpoint manager for git-based checkpoints.
        """
        self.toolkit = toolkit or AgentToolkit()
        self.provider = get_provider(model)
        self.model = model
        # Build system prompt, prepending plan mode prompt if in plan mode
        if system_prompt:
            self.system_prompt = system_prompt
        elif self.toolkit.plan_mode:
            from .prompts.plan_mode import PLAN_MODE_PROMPT
            self.system_prompt = PLAN_MODE_PROMPT + "\n\n" + build_system_prompt(self.toolkit)
        else:
            self.system_prompt = build_system_prompt(self.toolkit)
        self.emitter = emitter or NullEmitter()
        # Inject emitter into tools that need it (e.g., TaskTool for sub-agent streaming)
        self.toolkit.set_emitter(self.emitter)
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.show_tool_results = show_tool_results
        # Extended thinking support
        if enable_thinking is None:
            # Auto-detect from provider capabilities
            self.enable_thinking = (
                hasattr(self.provider, "supports_thinking")
                and self.provider.supports_thinking()
            )
        else:
            self.enable_thinking = enable_thinking
        # Conversation history for multi-turn support
        self._messages: list[dict] = []
        # Token usage tracking
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._total_thinking_tokens: int = 0
        # Store query for reranking
        self._current_query: str = ""
        # Todo state tracking for injection
        self._last_todo_snapshot: str = ""
        # Checkpoint manager for git-based checkpoints
        self._checkpoint_manager = checkpoint_manager
        # Track tools used during current run (for checkpoint metadata)
        self._tools_used_this_run: set[str] = set()
        # Plan approval state
        self._pending_plan: Optional[dict] = None  # Stores submitted plan awaiting approval

    def _get_todo_snapshot(self) -> str:
        """Get current todo state as string for comparison."""
        state = TaskState.get_instance()
        return json.dumps(state.get_all_tasks(), sort_keys=True)

    def _format_todo_reminder(self) -> str:
        """Format current todos as XML reminder for injection into context."""
        state = TaskState.get_instance()
        tasks = state.get_all_tasks()
        if not tasks:
            return ""

        counts = {"pending": 0, "in_progress": 0, "completed": 0}
        lines = []
        for t in tasks:
            status = t.get("status", "pending")
            counts[status] = counts.get(status, 0) + 1
            status_icon = {"pending": "⬚", "in_progress": "🔄", "completed": "✅"}.get(status, "?")
            lines.append(f'  {t["id"]}. {status_icon} {t["title"]}')

        header = f'Tasks: {counts["completed"]} completed, {counts["in_progress"]} in progress, {counts["pending"]} pending'
        task_list = "\n".join(lines)
        return f"<todo-state>\n{header}\n{task_list}\n</todo-state>"

    def _execute_tools_parallel(self, parsed_calls: list) -> list:
        """Execute multiple tool calls in parallel using a thread pool.

        Args:
            parsed_calls: List of (tool_call, args) tuples

        Returns:
            List of (tool_call, args, result) tuples in original order
        """
        # Emit tool start events for all calls
        for tool_call, args in parsed_calls:
            self.emitter.emit_tool_start(tool_call.name, args)

        def execute_one(item):
            tool_call, args = item
            try:
                result = self.toolkit.execute(tool_call.name, **args)
                return (tool_call, args, result)
            except Exception as e:
                log.exception(f"Tool {tool_call.name} failed")
                from .tools.base import ToolResult
                return (tool_call, args, ToolResult.error_result(str(e)))

        # Execute in parallel with up to 3 workers
        results: list = [None] * len(parsed_calls)
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {executor.submit(execute_one, item): i for i, item in enumerate(parsed_calls)}
            # Collect results maintaining order
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()

        # Emit tool result events for all calls
        for tool_call, args, result in results:
            self.emitter.emit_tool_result(
                tool_call.name,
                result.success,
                self._summarize_result(result),
            )

        return results

    def run(
        self,
        query: str,
        context: Optional[str] = None,
        images: Optional[list] = None,
    ) -> str:
        """Run the agent to answer a query.

        Args:
            query: User's question or request
            context: Optional additional context
            images: Optional list of images to include

        Returns:
            Agent's final response
        """
        # Store query for reranking context frame
        self._current_query = query

        # Build user message
        if context:
            user_message = {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {query}",
            }
        else:
            user_message = {
                "role": "user",
                "content": query,
            }

        # Save user message to history BEFORE running (so it's preserved even if interrupted)
        self._messages.append(user_message)
        messages = list(self._messages)  # Copy for the loop

        # TODO: Handle images if provided

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(messages, tools)
            # Update conversation history with full exchange
            self._messages = final_messages
            self.emitter.emit_end(success=True)
            # Create checkpoint if manager is configured
            self._create_checkpoint()
            return response

        except Exception as e:
            log.exception("Agent run failed")
            self.emitter.emit_error(str(e))
            # Keep user message in history even on error (already appended above)
            return f"Error: {str(e)}"

    def has_pending_plan(self) -> bool:
        """Check if there's a plan awaiting approval.

        Returns:
            True if a plan has been submitted and is awaiting approval.
        """
        return self._pending_plan is not None

    def get_pending_plan(self) -> Optional[dict]:
        """Get the pending plan if one exists.

        Returns:
            The pending plan dict, or None if no plan is pending.
        """
        return self._pending_plan

    def approve_plan(self) -> str:
        """Approve the pending plan and transition back to code mode.

        This method should be called after the user approves a submitted plan.
        It transitions the agent from plan mode back to code mode, allowing
        it to implement the approved plan.

        Returns:
            The agent's response after transitioning to code mode.
        """
        if not self._pending_plan:
            return "No pending plan to approve."

        plan = self._pending_plan
        self._pending_plan = None  # Clear pending plan

        # Reset ModeState singleton to code mode
        from .tools.modes import ModeState, AgentMode
        state = ModeState.get_instance()
        state.current_mode = AgentMode.CODE
        state.plan_content = plan.get("summary", "")

        # Rebuild toolkit with plan_mode=False (code mode)
        self.toolkit = AgentToolkit(
            connection=self.toolkit.connection,
            repo_root=self.toolkit._repo_root,
            plan_mode=False,
        )
        self.toolkit.set_emitter(self.emitter)

        # Update system prompt back to code mode
        self.system_prompt = build_system_prompt(self.toolkit)

        # Resume execution with approval message
        approval_message = f"""Your plan "{plan.get('title', 'Untitled')}" has been APPROVED.

You are now in code mode. Please implement the plan:

## Summary
{plan.get('summary', '')}

## Files to Modify
{self._format_files_to_modify(plan.get('files_to_modify', []))}

Proceed with implementation using the available tools (write_to_file, apply_diff, execute_command, etc.)."""

        return self.run(approval_message)

    def reject_plan(self, feedback: str = "") -> str:
        """Reject the pending plan and provide feedback.

        The agent remains in plan mode to revise the plan based on feedback.

        Args:
            feedback: Optional feedback explaining why the plan was rejected.

        Returns:
            The agent's response after receiving the rejection.
        """
        if not self._pending_plan:
            return "No pending plan to reject."

        plan_title = self._pending_plan.get("title", "Untitled")
        self._pending_plan = None  # Clear pending plan (but stay in plan mode)

        rejection_message = f"""Your plan "{plan_title}" was REJECTED.

{f"Feedback: {feedback}" if feedback else "Please revise the plan."}

You are still in plan mode. Please address the feedback and submit a revised plan using exit_plan."""

        return self.run(rejection_message)

    def _format_files_to_modify(self, files: list[dict]) -> str:
        """Format files_to_modify list for display."""
        if not files:
            return "No files specified"
        lines = []
        for f in files:
            path = f.get("path", "unknown")
            lines_info = f.get("lines", "")
            changes = f.get("changes", "")
            lines.append(f"- {path} ({lines_info}): {changes}")
        return "\n".join(lines)

    def _run_loop(
        self,
        messages: list[dict],
        tools: list[dict],
    ) -> tuple[str, list[dict]]:
        """Run the agent loop until completion.

        Args:
            messages: Initial messages
            tools: Tool schemas

        Returns:
            Tuple of (final response text, conversation messages)
        """
        max_retries = 3

        for iteration in range(self.max_iterations):
            # When approaching max iterations, ask agent to wrap up
            if iteration == self.max_iterations - 2:
                messages.append({
                    "role": "user",
                    "content": "[SYSTEM: You are approaching your iteration limit. Please provide your findings and conclusions now, even if incomplete. Summarize what you've learned and any recommendations.]",
                })

            # Try API call with retry on context overflow
            retry_count = 0
            response = None

            while retry_count < max_retries:
                try:
                    # Proactively compact context if approaching limit
                    messages = self._maybe_compact_context(messages)

                    response = self.provider.chat(
                        messages=messages,
                        system=self.system_prompt,
                        tools=tools,
                        thinking=self.enable_thinking,
                    )
                    break  # Success

                except Exception as exc:
                    if is_context_overflow_error(exc):
                        retry_count += 1
                        log.warning(
                            "Context overflow on attempt {}/{}, reducing context...",
                            retry_count,
                            max_retries,
                        )

                        if retry_count >= max_retries:
                            raise ContextLengthError(
                                f"Failed to reduce context after {max_retries} attempts: {exc}",
                            )

                        # Reduce context by removing old messages
                        messages = reduce_context_for_retry(
                            messages,
                            keep_recent=max(2, 6 - retry_count * 2),  # Fewer messages each retry
                        )
                    else:
                        raise  # Re-raise non-context errors

            if response is None:
                raise RuntimeError("Failed to get response from provider")

            # Accumulate token usage
            self._total_input_tokens += response.input_tokens
            self._total_output_tokens += response.output_tokens
            self._total_thinking_tokens += getattr(response, "thinking_tokens", 0)

            # Emit thinking if present
            if response.thinking:
                self.emitter.emit_thinking(response.thinking)

            # Check for tool calls
            if response.tool_calls:
                # Don't emit thinking text when there are tool calls - it clutters the output
                # The thinking is still in the conversation history for context

                # Track if we need to pause for user input
                needs_user_input = False

                # Parse all tool call arguments first
                parsed_calls = []
                for tool_call in response.tool_calls:
                    args = tool_call.arguments
                    if isinstance(args, str):
                        args = json.loads(args)
                    parsed_calls.append((tool_call, args))

                # Execute tools in parallel if multiple calls
                if len(parsed_calls) > 1:
                    results = self._execute_tools_parallel(parsed_calls)
                else:
                    # Single tool - execute directly
                    tool_call, args = parsed_calls[0]
                    self.emitter.emit_tool_start(tool_call.name, args)
                    result = self.toolkit.execute(tool_call.name, **args)
                    self.emitter.emit_tool_result(
                        tool_call.name,
                        result.success,
                        self._summarize_result(result),
                    )
                    results = [(tool_call, args, result)]

                # Track if we need to rebuild toolkit for mode change
                mode_changed = False

                # Process results and build messages
                for tool_call, args, result in results:
                    # Track tool for checkpoint metadata
                    self._tools_used_this_run.add(tool_call.name)
                    # Check if tool is asking a clarification question
                    if (result.success and
                        result.data and
                        result.data.get("status") == "awaiting_response" and
                        "question" in result.data):
                        self.emitter.emit_clarification(
                            question=result.data["question"],
                            context="",
                            options=result.data.get("options", []),
                        )
                        needs_user_input = True

                    # Check if agent entered plan mode
                    if (result.success and
                        result.data and
                        result.data.get("status") == "entered_plan_mode"):
                        mode_changed = True
                        # Rebuild toolkit with plan_mode=True
                        self.toolkit = AgentToolkit(
                            connection=self.toolkit.connection,
                            repo_root=self.toolkit._repo_root,
                            plan_mode=True,
                        )
                        self.toolkit.set_emitter(self.emitter)
                        # Update system prompt with plan mode instructions
                        from .prompts.plan_mode import PLAN_MODE_PROMPT
                        self.system_prompt = PLAN_MODE_PROMPT + "\n\n" + build_system_prompt(self.toolkit)
                        # Update tools for LLM
                        tools = self.toolkit.get_all_schemas()

                    # Check if tool is submitting a plan for approval (exit_plan)
                    if (result.success and
                        result.data and
                        result.data.get("status") == "plan_submitted"):
                        # Store the pending plan
                        self._pending_plan = {
                            "title": result.data.get("title", ""),
                            "summary": result.data.get("summary", ""),
                            "files_to_modify": result.data.get("files_to_modify", []),
                            "implementation_steps": result.data.get("implementation_steps", []),
                            "risks": result.data.get("risks", []),
                            "testing_strategy": result.data.get("testing_strategy", ""),
                        }
                        self.emitter.emit_plan_submitted(
                            title=self._pending_plan["title"],
                            summary=self._pending_plan["summary"],
                            files_to_modify=self._pending_plan["files_to_modify"],
                            implementation_steps=self._pending_plan["implementation_steps"],
                            risks=self._pending_plan["risks"],
                            testing_strategy=self._pending_plan["testing_strategy"],
                        )
                        # Pause and wait for approval (similar to clarification flow)
                        needs_user_input = True

                    # Add assistant message with tool call
                    messages.append({
                        "role": "assistant",
                        "content": response.content or "",
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_call.name,
                                "arguments": json.dumps(args),
                            },
                        }],
                    })

                    # Serialize and truncate tool result to prevent context overflow
                    result_json = json.dumps(result.to_dict(), cls=SafeJSONEncoder)
                    result_json = truncate_tool_output(result_json)

                    # Check if todos changed and inject reminder
                    if tool_call.name in ("write_todo", "update_todo_list"):
                        new_snapshot = self._get_todo_snapshot()
                        if new_snapshot != self._last_todo_snapshot:
                            self._last_todo_snapshot = new_snapshot
                            reminder = self._format_todo_reminder()
                            if reminder:
                                result_json += f"\n\n{reminder}"

                    # Add tool result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result_json,
                    })

                # If a clarification question was asked, pause and wait for user input
                if needs_user_input:
                    log.debug("Pausing agent loop - waiting for user input")
                    return "", messages

            else:
                # No tool calls - check if response was truncated
                if response.stop_reason in ("max_tokens", "length"):
                    # Response was truncated, request continuation
                    log.debug("Response truncated ({}), requesting continuation", response.stop_reason)
                    if response.content:
                        messages.append({
                            "role": "assistant",
                            "content": response.content,
                        })
                    messages.append({
                        "role": "user",
                        "content": "Your response was cut off. Please continue.",
                    })
                    continue

                # Agent is done - emit final response
                if response.content:
                    self.emitter.emit_message_start()
                    self.emitter.emit_message_delta(response.content)
                    self.emitter.emit_message_end()
                    # Add final assistant message to history
                    messages.append({
                        "role": "assistant",
                        "content": response.content,
                    })

                # Emit final context frame summary
                self._emit_context_frame(messages)

                return response.content or "", messages

        # Hit max iterations - try one final request without tools to force a response
        try:
            final_response = self.provider.chat(
                messages=messages + [{
                    "role": "user",
                    "content": "[SYSTEM: Maximum iterations reached. Provide your final response now with whatever information you have gathered. Do not use any tools.]",
                }],
                system=self.system_prompt,
                tools=None,  # No tools - force text response
                thinking=self.enable_thinking,
            )
            # Emit thinking if present
            if final_response.thinking:
                self.emitter.emit_thinking(final_response.thinking)
            if final_response.content:
                self.emitter.emit_message_start()
                self.emitter.emit_message_delta(final_response.content)
                self.emitter.emit_message_end()
                self._emit_context_frame(messages)
                return final_response.content, messages
        except Exception as e:
            log.warning(f"Failed to get final response: {e}")

        # Fallback message if final response fails
        final_message = "Reached maximum iterations. The agent was unable to complete the task within the allowed iterations."
        self.emitter.emit_message_start()
        self.emitter.emit_message_delta(final_message)
        self.emitter.emit_message_end()
        self._emit_context_frame(messages)
        return final_message, messages

    def _summarize_result(self, result: Any) -> str:
        """Create a brief summary of a tool result."""
        if not result.success:
            return f"Error: {result.error}"

        if not result.data:
            return "Empty result"

        data = result.data

        if "results" in data:
            return f"{len(data['results'])} results"
        elif "root_node" in data:
            node = data["root_node"]
            name = node.get("qualified_name") or node.get("file_path", "unknown")
            return f"Expanded: {name}"
        elif "callers" in data:
            return f"{len(data['callers'])} callers"
        elif "callees" in data:
            return f"{len(data['callees'])} callees"

        return "Completed"

    def _emit_context_frame(self, messages: list[dict] | None = None) -> None:
        """Emit a context frame event with current exploration state.

        Args:
            messages: Current conversation messages to estimate context size
        """
        # Get exploration steps from toolkit session
        steps = self.toolkit.get_exploration_steps()

        # Estimate current context window tokens and get breakdown
        context_tokens = 0
        context_breakdown = {}
        largest_messages = []
        if messages:
            context_tokens = self._estimate_context_tokens(messages)
            context_breakdown, largest_messages = self._get_context_breakdown(messages)

        # Summarize exploration by tool
        tool_counts: dict[str, int] = {}
        entities_found = 0
        step_details: list[dict] = []

        for step in steps:
            tool_name = getattr(step, 'tool', 'unknown')
            tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1

            # Count entities from the step
            step_entities = getattr(step, 'entities_found', [])
            entities_found += len(step_entities)

            # Collect step details
            params = getattr(step, 'params', {})
            summary = getattr(step, 'result_summary', '')

            # Extract meaningful info based on tool type
            detail = {
                "tool": tool_name,
                "summary": summary,
            }

            # Add relevant params based on tool
            if tool_name == 'read_file' and 'file_path' in params:
                detail["file"] = params['file_path']
            elif tool_name == 'read_file' and 'path' in params:
                detail["file"] = params['path']
            elif tool_name in ('grep', 'semantic_search') and 'query' in params:
                detail["query"] = params['query']
            elif tool_name == 'glob' and 'pattern' in params:
                detail["pattern"] = params['pattern']
            elif tool_name == 'list_files' and 'path' in params:
                detail["path"] = params['path']

            # Add content preview if available
            content_preview = getattr(step, 'content_preview', None)
            if content_preview:
                detail["content_preview"] = content_preview

            # Add token count if available
            token_count = getattr(step, 'token_count', 0)
            if token_count > 0:
                detail["tokens"] = token_count

            # Add entities if any
            if step_entities:
                detail["entities"] = step_entities[:5]  # Limit to 5

            step_details.append(detail)

        exploration_steps = [
            {"tool": tool, "count": count}
            for tool, count in tool_counts.items()
        ]

        # Build context frame data
        adding = {
            "exploration_steps": exploration_steps,
            "entities_found": entities_found,
            "step_count": len(steps),
            "details": step_details[-20:],  # Last 20 steps
            "input_tokens": self._total_input_tokens,
            "output_tokens": self._total_output_tokens,
            "context_tokens": context_tokens,  # Current context window size
            "context_breakdown": context_breakdown,  # Tokens by message type
            "largest_messages": largest_messages,  # Top 5 biggest messages
        }

        # Get reranked context items
        reading = self._get_reranked_context()

        # Emit the context frame
        self.emitter.emit_context_frame(adding=adding, reading=reading)

    def _estimate_context_tokens(self, messages: list[dict]) -> int:
        """Estimate the current context window size in tokens.

        Args:
            messages: Conversation messages

        Returns:
            Estimated token count for the context
        """
        total_chars = 0

        # Count characters in all messages
        for msg in messages:
            content = msg.get("content", "")
            if isinstance(content, str):
                total_chars += len(content)
            elif isinstance(content, list):
                # Handle multi-part messages (e.g., with images)
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        total_chars += len(part["text"])

            # Add role overhead (~4 tokens per message for role/structure)
            total_chars += 16

        # Also count system prompt
        if self.system_prompt:
            total_chars += len(self.system_prompt)

        # Estimate: ~4 characters per token
        return total_chars // 4

    def _get_context_breakdown(self, messages: list[dict]) -> tuple[dict, list[dict]]:
        """Get breakdown of context usage by message type.

        Args:
            messages: Conversation messages

        Returns:
            Tuple of (breakdown dict, list of largest messages)
        """
        breakdown = {
            "system_prompt": len(self.system_prompt) // 4 if self.system_prompt else 0,
            "user": 0,
            "assistant": 0,
            "tool_results": 0,
        }

        # Track individual message sizes for finding largest
        message_sizes = []

        for i, msg in enumerate(messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Calculate content size
            if isinstance(content, str):
                size = len(content)
            elif isinstance(content, list):
                size = sum(len(p.get("text", "")) for p in content if isinstance(p, dict))
            else:
                size = 0

            tokens = size // 4

            # Categorize
            if role == "user":
                breakdown["user"] += tokens
            elif role == "assistant":
                breakdown["assistant"] += tokens
            elif role == "tool":
                breakdown["tool_results"] += tokens

            # Track for largest messages
            if tokens > 100:  # Only track substantial messages
                # Try to get a label for this message
                label = f"{role}[{i}]"
                if role == "tool":
                    tool_call_id = msg.get("tool_call_id", "")
                    # Try to find the tool name from previous assistant message
                    for prev_msg in reversed(messages[:i]):
                        if prev_msg.get("role") == "assistant" and "tool_calls" in prev_msg:
                            for tc in prev_msg.get("tool_calls", []):
                                if tc.get("id") == tool_call_id:
                                    label = tc.get("function", {}).get("name", "tool")
                                    break
                            break

                message_sizes.append({
                    "index": i,
                    "role": role,
                    "label": label,
                    "tokens": tokens,
                    "preview": content[:100] if isinstance(content, str) else str(content)[:100],
                })

        # Sort by size and get top 5
        message_sizes.sort(key=lambda x: x["tokens"], reverse=True)
        largest = message_sizes[:5]

        return breakdown, largest

    def _maybe_compact_context(
        self,
        messages: list[dict],
        threshold: float = 0.8,
    ) -> list[dict]:
        """Proactively compact context if approaching limit.

        Args:
            messages: Current conversation messages
            threshold: Trigger compaction at this % of context limit (default 80%)

        Returns:
            Original or compacted messages
        """
        context_tokens = self._estimate_context_tokens(messages)
        context_limit = self.provider.get_context_limit()

        # Check if we need to compact
        if context_tokens < context_limit * threshold:
            return messages  # No compaction needed

        log.info(
            f"Context at {context_tokens:,}/{context_limit:,} tokens "
            f"({context_tokens/context_limit:.0%}), compacting..."
        )

        return self._compact_messages_with_llm(
            messages, target_tokens=int(context_limit * 0.5)
        )

    def _compact_messages_with_llm(
        self,
        messages: list[dict],
        target_tokens: int,
    ) -> list[dict]:
        """Use fast LLM to summarize middle messages.

        Preserves:
        - First message (original user request)
        - Last 4 messages (recent context)
        - Summarizes everything in between

        Args:
            messages: Current conversation messages
            target_tokens: Target token count after compaction

        Returns:
            Compacted messages list
        """
        from .subagent import get_model_for_tier
        from .providers import get_provider

        if len(messages) <= 5:
            return messages  # Too few to compact

        # Split messages
        first_msg = messages[0]
        recent_msgs = messages[-4:]
        middle_msgs = messages[1:-4]

        if not middle_msgs:
            return messages

        # Build summary prompt
        middle_content = self._format_messages_for_summary(middle_msgs)

        prompt = f"""Summarize this conversation history concisely.

PRESERVE (include verbatim if present):
- Code snippets and file paths
- Error messages
- Key decisions made
- Important tool results (file contents, search results)

CONDENSE:
- Repetitive searches
- Verbose tool outputs
- Intermediate reasoning

CONVERSATION HISTORY:
{middle_content}

OUTPUT FORMAT:
Provide a concise summary (max 2000 tokens) that captures the essential context needed to continue this task."""

        # Use fast model for summarization
        fast_model = get_model_for_tier("fast")
        fast_provider = get_provider(fast_model)

        try:
            self.emitter.emit_thinking("Compacting context with fast model...")

            response = fast_provider.chat(
                messages=[{"role": "user", "content": prompt}],
                system="You are a context summarizer. Be concise but preserve code and technical details.",
            )

            summary = response.content or ""

            log.info(
                f"Compacted {len(middle_msgs)} messages into summary "
                f"({len(summary)} chars)"
            )

            # Build compacted messages
            return [
                first_msg,
                {
                    "role": "assistant",
                    "content": f"[Context Summary]\n{summary}\n[End Summary]",
                },
                *recent_msgs,
            ]
        except Exception as e:
            log.warning(f"LLM compaction failed: {e}, falling back to truncation")
            return [first_msg] + recent_msgs

    def _format_messages_for_summary(self, messages: list[dict]) -> str:
        """Format messages for summarization prompt.

        Args:
            messages: Messages to format

        Returns:
            Formatted string for summarization
        """
        parts = []
        for msg in messages:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            # Handle tool calls in assistant messages
            if role == "assistant" and "tool_calls" in msg:
                tool_calls = msg.get("tool_calls", [])
                tool_info = [
                    f"Called: {tc.get('function', {}).get('name', 'unknown')}"
                    for tc in tool_calls
                ]
                content = f"{content}\n[Tools: {', '.join(tool_info)}]" if content else f"[Tools: {', '.join(tool_info)}]"

            # Truncate very long content
            if len(content) > 4000:
                content = content[:4000] + "\n[...truncated...]"

            parts.append(f"[{role.upper()}]\n{content}")

        return "\n\n---\n\n".join(parts)

    def _get_reranked_context(self) -> dict:
        """Get reranked context items based on the current query.

        Returns:
            Dict with item_count and items list
        """
        try:
            from ..context.service import ContextService
            from ..context.reranker import rerank_context_items

            # Get exploration steps for context extraction
            steps = self.toolkit.get_exploration_steps()
            if not steps:
                return {"item_count": 0, "items": []}

            # Use context service to extract context items from exploration
            service = ContextService(connection=self.toolkit.connection)
            terminal_id = service.get_terminal_id()

            # Update context with exploration steps
            service.update_context(
                terminal_id=terminal_id,
                exploration_steps=steps,
            )

            # Get context items
            items = service.get_context_items(terminal_id)
            if not items:
                return {"item_count": 0, "items": []}

            # Rerank by query relevance
            if self._current_query:
                items = rerank_context_items(
                    items,
                    self._current_query,
                    top_k=20,
                )

            # Convert to serializable format
            result_items = []
            for item in items[:20]:  # Limit to 20 items
                result_items.append({
                    "name": item.qualified_name,
                    "type": item.entity_type,
                    "file": item.file_path,
                    "score": round(item.score, 3) if hasattr(item, 'score') else None,
                })

            return {
                "item_count": len(result_items),
                "items": result_items,
            }

        except Exception as e:
            log.debug(f"Failed to get reranked context: {e}")
            return {"item_count": 0, "items": []}

    def chat(self, message: str, images: Optional[list] = None) -> str:
        """Continue a conversation with a new message.

        This method maintains conversation history for multi-turn interactions.
        Call run() first to start a conversation, then chat() for follow-ups.

        Args:
            message: User's follow-up message
            images: Optional list of images to include

        Returns:
            Agent's response
        """
        if not self._messages:
            # No history, just run fresh
            return self.run(message, images=images)

        # Store query for reranking context frame
        self._current_query = message

        # Add new user message to history
        self._messages.append({
            "role": "user",
            "content": message,
        })

        # Get tool schemas
        tools = self.toolkit.get_all_schemas()

        try:
            response, final_messages = self._run_loop(self._messages, tools)
            # Update conversation history
            self._messages = final_messages
            self.emitter.emit_end(success=True)
            # Create checkpoint if manager is configured
            self._create_checkpoint()
            return response

        except Exception as e:
            log.exception("Agent chat failed")
            self.emitter.emit_error(str(e))
            return f"Error: {str(e)}"

    def _create_checkpoint(self) -> None:
        """Create a git checkpoint after successful run.

        Only creates a checkpoint if:
        - A checkpoint manager is configured
        - There are file changes to commit
        """
        if not self._checkpoint_manager:
            return

        try:
            self._checkpoint_manager.create_checkpoint(
                messages=self._messages,
                model=self.model,
                system_prompt=self.system_prompt,
                tools_used=list(self._tools_used_this_run),
                token_usage={
                    "input": self._total_input_tokens,
                    "output": self._total_output_tokens,
                    "thinking": self._total_thinking_tokens,
                },
            )
        except Exception as e:
            log.warning(f"Failed to create checkpoint: {e}")
        finally:
            # Clear tools for next run
            self._tools_used_this_run.clear()

    def reset(self) -> None:
        """Reset the agent state."""
        self.toolkit.reset_session()
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._current_query = ""
