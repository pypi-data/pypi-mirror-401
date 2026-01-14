"""Unified event stream for agent operations.

This module provides a centralized event system that both CLI and UI can consume,
ensuring consistent message handling across interfaces.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Protocol


class EventType(Enum):
    """Types of events emitted by agents."""

    # Tool lifecycle
    TOOL_START = "tool_start"
    TOOL_RESULT = "tool_result"

    # Agent thinking/progress
    THINKING = "thinking"
    PROGRESS = "progress"

    # Output
    RESPONSE = "response"
    PARTIAL_RESPONSE = "partial_response"

    # Interaction
    CLARIFICATION = "clarification"
    CLARIFICATION_RESPONSE = "clarification_response"
    PLAN_SUBMITTED = "plan_submitted"

    # Errors
    ERROR = "error"
    WARNING = "warning"

    # Session
    SESSION_START = "session_start"
    SESSION_END = "session_end"

    # Context
    CONTEXT_FRAME = "context_frame"


@dataclass
class AgentEvent:
    """A single event emitted by an agent.

    Attributes:
        type: The type of event
        data: Event-specific data payload
        timestamp: When the event occurred
        agent_name: Optional name of the agent that emitted this event
    """
    type: EventType
    data: dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    agent_name: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "agent_name": self.agent_name,
        }


class EventHandler(Protocol):
    """Protocol for event handlers."""

    def handle(self, event: AgentEvent) -> None:
        """Handle an emitted event."""
        ...


class AgentEventEmitter:
    """Emits and stores agent events for consumption by handlers.

    This is the central hub for the event stream. Agents emit events here,
    and handlers (CLI Rich renderer, JSON streamer, etc.) subscribe to receive them.

    Example:
        emitter = AgentEventEmitter()
        emitter.add_handler(RichConsoleHandler())

        # In agent code:
        emitter.emit(EventType.TOOL_START, {"name": "semantic_search", "args": {...}})
        result = execute_tool(...)
        emitter.emit(EventType.TOOL_RESULT, {"name": "semantic_search", "success": True})
    """

    def __init__(self, agent_name: str | None = None):
        """Initialize the emitter.

        Args:
            agent_name: Optional name to tag all events from this emitter
        """
        self._handlers: list[EventHandler] = []
        self._events: list[AgentEvent] = []
        self._agent_name = agent_name

    def add_handler(self, handler: EventHandler) -> None:
        """Add a handler to receive events.

        Args:
            handler: Handler that implements the EventHandler protocol
        """
        self._handlers.append(handler)

    def remove_handler(self, handler: EventHandler) -> None:
        """Remove a handler.

        Args:
            handler: Handler to remove
        """
        if handler in self._handlers:
            self._handlers.remove(handler)

    def emit(self, event_type: EventType, data: dict[str, Any] | None = None) -> AgentEvent:
        """Emit an event to all handlers.

        Args:
            event_type: Type of event to emit
            data: Event-specific data payload

        Returns:
            The created AgentEvent
        """
        event = AgentEvent(
            type=event_type,
            data=data or {},
            agent_name=self._agent_name,
        )
        self._events.append(event)

        for handler in self._handlers:
            try:
                handler.handle(event)
            except Exception:
                # Don't let handler errors break the agent
                pass

        return event

    def emit_tool_start(self, name: str, args: dict[str, Any] | None = None) -> AgentEvent:
        """Convenience method to emit a tool start event.

        Args:
            name: Tool name
            args: Tool arguments
        """
        return self.emit(EventType.TOOL_START, {
            "name": name,
            "args": args or {},
        })

    def emit_tool_result(
        self,
        name: str,
        success: bool,
        summary: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> AgentEvent:
        """Convenience method to emit a tool result event.

        Args:
            name: Tool name
            success: Whether the tool succeeded
            summary: Brief summary of the result
            data: Full result data (may be truncated by handlers)
        """
        return self.emit(EventType.TOOL_RESULT, {
            "name": name,
            "success": success,
            "summary": summary,
            "data": data,
        })

    def emit_thinking(self, message: str) -> AgentEvent:
        """Convenience method to emit a thinking/progress message.

        Args:
            message: What the agent is thinking/doing
        """
        return self.emit(EventType.THINKING, {"message": message})

    def emit_progress(self, message: str, percent: float | None = None) -> AgentEvent:
        """Convenience method to emit a progress update.

        Args:
            message: Progress message
            percent: Optional completion percentage (0-100)
        """
        return self.emit(EventType.PROGRESS, {
            "message": message,
            "percent": percent,
        })

    def emit_response(self, content: str, is_final: bool = True) -> AgentEvent:
        """Convenience method to emit a response.

        Args:
            content: Response content (usually markdown)
            is_final: Whether this is the final response
        """
        event_type = EventType.RESPONSE if is_final else EventType.PARTIAL_RESPONSE
        return self.emit(event_type, {"content": content})

    def emit_clarification(
        self,
        question: str,
        context: str | None = None,
        options: list[str] | None = None,
    ) -> AgentEvent:
        """Convenience method to emit a clarification request.

        Args:
            question: The question to ask
            context: Why we're asking
            options: Suggested answers
        """
        return self.emit(EventType.CLARIFICATION, {
            "question": question,
            "context": context,
            "options": options,
        })

    def emit_plan_submitted(
        self,
        title: str,
        summary: str,
        files_to_modify: list[dict] | None = None,
        implementation_steps: list[str] | None = None,
        risks: list[str] | None = None,
        testing_strategy: str | None = None,
    ) -> AgentEvent:
        """Convenience method to emit a plan submission event.

        Args:
            title: Plan title
            summary: Plan summary
            files_to_modify: List of files with path, lines, changes
            implementation_steps: Ordered implementation steps
            risks: Potential risks or considerations
            testing_strategy: How changes will be tested
        """
        return self.emit(EventType.PLAN_SUBMITTED, {
            "title": title,
            "summary": summary,
            "files_to_modify": files_to_modify or [],
            "implementation_steps": implementation_steps or [],
            "risks": risks or [],
            "testing_strategy": testing_strategy or "",
        })

    def emit_error(self, message: str, details: str | None = None) -> AgentEvent:
        """Convenience method to emit an error.

        Args:
            message: Error message
            details: Additional details (stack trace, etc.)
        """
        return self.emit(EventType.ERROR, {
            "message": message,
            "details": details,
        })

    def emit_start(self, goal: str, **kwargs) -> AgentEvent:
        """Convenience method to emit a session start event.

        Args:
            goal: The goal/query for this session
            **kwargs: Additional data to include
        """
        return self.emit(EventType.SESSION_START, {
            "goal": goal,
            **kwargs,
        })

    def emit_end(self, success: bool = True, **kwargs) -> AgentEvent:
        """Convenience method to emit a session end event.

        Args:
            success: Whether the session completed successfully
            **kwargs: Additional data to include
        """
        return self.emit(EventType.SESSION_END, {
            "success": success,
            **kwargs,
        })

    def emit_context_frame(
        self,
        adding: dict[str, Any] | None = None,
        reading: dict[str, Any] | None = None,
    ) -> AgentEvent:
        """Convenience method to emit a context frame update.

        Args:
            adding: What's being added to context (modified_files, exploration_steps, tokens)
            reading: What's being read from context (items with scores, tokens)
        """
        return self.emit(EventType.CONTEXT_FRAME, {
            "adding": adding or {},
            "reading": reading or {},
        })

    def emit_message_start(self) -> AgentEvent:
        """Convenience method to emit message start event."""
        self._accumulated_content = ""
        return self.emit(EventType.PARTIAL_RESPONSE, {"status": "start"})

    def emit_message_delta(self, content: str) -> AgentEvent:
        """Convenience method to emit message delta (streaming content).

        Args:
            content: The content chunk to stream
        """
        if hasattr(self, '_accumulated_content'):
            self._accumulated_content += content
        return self.emit(EventType.PARTIAL_RESPONSE, {"content": content})

    def emit_message_end(self) -> AgentEvent:
        """Convenience method to emit message end event with accumulated content."""
        content = getattr(self, '_accumulated_content', "")
        return self.emit(EventType.RESPONSE, {"content": content})

    def get_events(self) -> list[AgentEvent]:
        """Get all events emitted so far.

        Returns:
            Copy of the events list
        """
        return self._events.copy()

    def clear_events(self) -> None:
        """Clear the events history."""
        self._events.clear()


# Default no-op emitter for backwards compatibility
class NullEmitter(AgentEventEmitter):
    """An emitter that does nothing - for backwards compatibility."""

    def emit(self, event_type: EventType, data: dict[str, Any] | None = None) -> AgentEvent:
        """Create event but don't store or dispatch it."""
        return AgentEvent(type=event_type, data=data or {}, agent_name=self._agent_name)


# Global default emitter (can be replaced)
_default_emitter: AgentEventEmitter | None = None


def get_default_emitter() -> AgentEventEmitter:
    """Get the default global emitter."""
    global _default_emitter
    if _default_emitter is None:
        _default_emitter = NullEmitter()
    return _default_emitter


def set_default_emitter(emitter: AgentEventEmitter) -> None:
    """Set the default global emitter."""
    global _default_emitter
    _default_emitter = emitter
