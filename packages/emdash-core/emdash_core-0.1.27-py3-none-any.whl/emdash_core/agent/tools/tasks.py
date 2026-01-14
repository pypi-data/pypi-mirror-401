"""Task management tools for agent workflows."""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory


class TaskStatus(Enum):
    """Status of a task."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """A task in the todo list."""

    id: str
    title: str
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
        }


class TaskState:
    """Singleton state for task management."""

    _instance: Optional["TaskState"] = None

    def __init__(self):
        self.tasks: list[Task] = []
        self.completed: bool = False
        self.completion_summary: Optional[str] = None
        self.pending_question: Optional[str] = None
        self.user_response: Optional[str] = None
        self._next_id: int = 1

    @classmethod
    def get_instance(cls) -> "TaskState":
        """Get the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance."""
        cls._instance = None

    def add_task(
        self,
        title: str,
        description: str = "",
    ) -> Task:
        """Add a new task.

        Args:
            title: Task title
            description: Detailed description
        """
        task = Task(
            id=str(self._next_id),
            title=title,
            description=description,
        )
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_status(self, task_id: str, status: TaskStatus) -> bool:
        """Update task status."""
        task = self.get_task(task_id)
        if task:
            task.status = status
            return True
        return False

    def get_all_tasks(self) -> list[dict]:
        """Get all tasks as dicts."""
        return [t.to_dict() for t in self.tasks]

    def mark_completed(self, summary: str):
        """Mark the overall task as completed."""
        self.completed = True
        self.completion_summary = summary

    def ask_question(self, question: str):
        """Set a pending question for the user."""
        self.pending_question = question
        self.user_response = None


class TaskManagementTool(BaseTool):
    """Base class for task management tools."""

    category = ToolCategory.PLANNING

    def __init__(self, connection=None):
        """Initialize without requiring connection."""
        self.connection = connection

    @property
    def state(self) -> TaskState:
        """Get current TaskState instance (always fresh to handle resets)."""
        return TaskState.get_instance()


class WriteTodoTool(TaskManagementTool):
    """Create a new task for tracking work."""

    name = "write_todo"
    description = "Create a new task. Use reset=true to clear all existing tasks first."

    def execute(
        self,
        title: str,
        description: str = "",
        reset: bool = False,
        **kwargs,
    ) -> ToolResult:
        """Create a new task.

        Args:
            title: Short task title
            description: Detailed description (optional)
            reset: If true, clear all existing tasks before adding this one

        Returns:
            ToolResult with task info
        """
        if not title or not title.strip():
            return ToolResult.error_result("Task title is required")

        # Reset all tasks if requested
        if reset:
            TaskState.reset()

        task = self.state.add_task(
            title=title.strip(),
            description=description.strip() if description else "",
        )

        return ToolResult.success_result({
            "task": task.to_dict(),
            "total_tasks": len(self.state.tasks),
            "all_tasks": self.state.get_all_tasks(),
            "was_reset": reset,
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "title": {
                    "type": "string",
                    "description": "Short task title",
                },
                "description": {
                    "type": "string",
                    "description": "Detailed description of what needs to be done",
                },
                "reset": {
                    "type": "boolean",
                    "description": "Set to true to clear all existing tasks before adding this one",
                    "default": False,
                },
            },
            required=["title"],
        )


class UpdateTodoListTool(TaskManagementTool):
    """Update task status."""

    name = "update_todo_list"
    description = "Update task status. Auto-creates tasks if they don't exist."

    def execute(
        self,
        task_id: str,
        status: str = None,
        title: str = "",
        description: str = "",
        **kwargs,  # Ignore unexpected params from LLM
    ) -> ToolResult:
        """Update task status.

        Args:
            task_id: Task ID to update (e.g., "1", "2")
            status: New status (pending, in_progress, completed)
            title: Optional title for auto-created tasks
            description: Optional description for auto-created tasks

        Returns:
            ToolResult with updated task list
        """
        task = self.state.get_task(task_id)

        # Auto-create task if not found
        if not task:
            new_status = TaskStatus.PENDING
            if status:
                try:
                    new_status = TaskStatus(status.lower())
                except ValueError:
                    pass

            task = Task(
                id=str(task_id),
                title=title or f"Task {task_id}",
                status=new_status,
                description=description,
            )
            self.state.tasks.append(task)
            return ToolResult.success_result({
                "task_id": task_id,
                "auto_created": True,
                "task": task.to_dict(),
                "all_tasks": self.state.get_all_tasks(),
            })

        # Update status if provided
        if status:
            try:
                task.status = TaskStatus(status.lower())
            except ValueError:
                return ToolResult.error_result(
                    f"Invalid status: {status}. Use: pending, in_progress, completed"
                )

        return ToolResult.success_result({
            "task_id": task_id,
            "task": task.to_dict(),
            "all_tasks": self.state.get_all_tasks(),
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "task_id": {
                    "type": "string",
                    "description": "ID of the task to update (e.g., '1', '2')",
                },
                "status": {
                    "type": "string",
                    "enum": ["pending", "in_progress", "completed"],
                    "description": "New status for the task",
                },
                "title": {
                    "type": "string",
                    "description": "Task title (used if auto-creating)",
                },
                "description": {
                    "type": "string",
                    "description": "Task description (used if auto-creating)",
                },
            },
            required=["task_id"],
        )


class AskFollowupQuestionTool(TaskManagementTool):
    """Request clarification from the user."""

    name = "ask_followup_question"
    description = """Ask the user a clarifying question when you need more information to proceed.

CRITICAL CONSTRAINTS:
- Only ask ONE question at a time - never call this tool multiple times in parallel
- Only ask AFTER doing research first (read files, search code, explore the codebase)
- Questions should be informed by what you've learned, not generic upfront questionnaires
- If you need multiple pieces of information, ask the most important one first"""

    def execute(
        self,
        question: str,
        options: Optional[list[str]] = None,
    ) -> ToolResult:
        """Ask a followup question.

        Args:
            question: Question to ask the user
            options: Optional list of suggested answers

        Returns:
            ToolResult indicating question was set
        """
        if not question or not question.strip():
            return ToolResult.error_result("Question is required")

        self.state.ask_question(question.strip())

        return ToolResult.success_result({
            "question": question,
            "options": options,
            "status": "awaiting_response",
            "message": "Question will be shown to user. Agent loop will pause.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "question": {
                    "type": "string",
                    "description": "The question to ask the user",
                },
                "options": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Suggested answer options",
                },
            },
            required=["question"],
        )


class AttemptCompletionTool(TaskManagementTool):
    """Signal task completion with summary."""

    name = "attempt_completion"
    description = "Signal that the task is complete. Provide a summary of what was accomplished and list files that were modified."

    def execute(
        self,
        summary: str,
        files_modified: list[str] = None,
    ) -> ToolResult:
        """Signal task completion.

        Args:
            summary: Summary of what was accomplished
            files_modified: List of files that were modified

        Returns:
            ToolResult with completion info
        """
        if not summary or not summary.strip():
            return ToolResult.error_result("Summary is required")

        self.state.mark_completed(summary.strip())

        # Count completed vs total tasks
        completed = sum(1 for t in self.state.tasks if t.status == TaskStatus.COMPLETED)
        total = len(self.state.tasks)

        return ToolResult.success_result({
            "status": "completed",
            "summary": summary,
            "files_modified": files_modified or [],
            "tasks_completed": f"{completed}/{total}" if total > 0 else "No subtasks",
            "message": "Task marked as complete. Agent loop will terminate.",
        })

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "summary": {
                    "type": "string",
                    "description": "Summary of what was accomplished",
                },
                "files_modified": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of file paths that were modified",
                },
            },
            required=["summary"],
        )


