"""Coding tools for file operations."""

import os
import subprocess
from pathlib import Path
from typing import Optional

from .base import BaseTool, ToolResult, ToolCategory
from ...utils.logger import log


class CodingTool(BaseTool):
    """Base class for coding tools that operate on files."""

    category = ToolCategory.PLANNING  # File ops are part of planning/coding workflow

    def __init__(self, repo_root: Path, connection=None):
        """Initialize with repo root for path validation.

        Args:
            repo_root: Root directory of the repository
            connection: Optional connection (not used for file ops)
        """
        self.repo_root = repo_root.resolve()
        self.connection = connection

    def _validate_path(self, path: str) -> tuple[bool, str, Optional[Path]]:
        """Validate that a path is within the repo root.

        Args:
            path: Path to validate

        Returns:
            Tuple of (is_valid, error_message, resolved_path)
        """
        try:
            # Handle relative and absolute paths
            if os.path.isabs(path):
                full_path = Path(path).resolve()
            else:
                full_path = (self.repo_root / path).resolve()

            # Check if within repo
            try:
                full_path.relative_to(self.repo_root)
            except ValueError:
                return False, f"Path {path} is outside repository", None

            return True, "", full_path

        except Exception as e:
            return False, f"Invalid path: {e}", None


class ReadFileTool(CodingTool):
    """Read the contents of a file."""

    name = "read_file"
    description = """Read the contents of a file.
Returns the file content as text."""

    def execute(
        self,
        path: str,
        start_line: Optional[int] = None,
        end_line: Optional[int] = None,
    ) -> ToolResult:
        """Read a file.

        Args:
            path: Path to the file
            start_line: Optional starting line (1-indexed)
            end_line: Optional ending line (1-indexed)

        Returns:
            ToolResult with file content
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {path}")

        if not full_path.is_file():
            return ToolResult.error_result(f"Not a file: {path}")

        try:
            content = full_path.read_text()
            lines = content.split("\n")

            # Handle line ranges
            if start_line or end_line:
                start_idx = (start_line - 1) if start_line else 0
                end_idx = end_line if end_line else len(lines)
                lines = lines[start_idx:end_idx]
                content = "\n".join(lines)

            return ToolResult.success_result(
                data={
                    "path": path,
                    "content": content,
                    "line_count": len(lines),
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to read file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to read",
                },
                "start_line": {
                    "type": "integer",
                    "description": "Starting line number (1-indexed)",
                },
                "end_line": {
                    "type": "integer",
                    "description": "Ending line number (1-indexed)",
                },
            },
            required=["path"],
        )


class WriteToFileTool(CodingTool):
    """Write content to a file."""

    name = "write_to_file"
    description = """Write content to a file.
Creates the file if it doesn't exist, or overwrites if it does."""

    def execute(
        self,
        path: str,
        content: str,
    ) -> ToolResult:
        """Write to a file.

        Args:
            path: Path to the file
            content: Content to write

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        try:
            # Create parent directories
            full_path.parent.mkdir(parents=True, exist_ok=True)

            # Write content
            full_path.write_text(content)

            return ToolResult.success_result(
                data={
                    "path": path,
                    "bytes_written": len(content),
                    "lines_written": content.count("\n") + 1,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to write file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to write",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
            required=["path", "content"],
        )


class ApplyDiffTool(CodingTool):
    """Apply a diff/patch to a file."""

    name = "apply_diff"
    description = """Apply a unified diff to a file.
The diff should be in standard unified diff format."""

    def execute(
        self,
        path: str,
        diff: str,
    ) -> ToolResult:
        """Apply a diff to a file.

        Args:
            path: Path to the file
            diff: Unified diff content

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {path}")

        try:
            # Try to apply with patch command
            result = subprocess.run(
                ["patch", "-p0", "--forward"],
                input=diff,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=30,
            )

            if result.returncode != 0:
                # Try with -p1
                result = subprocess.run(
                    ["patch", "-p1", "--forward"],
                    input=diff,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_root,
                    timeout=30,
                )

            if result.returncode != 0:
                return ToolResult.error_result(
                    f"Patch failed: {result.stderr}",
                    suggestions=["Check the diff format", "Ensure the file matches the diff context"],
                )

            return ToolResult.success_result(
                data={
                    "path": path,
                    "output": result.stdout,
                },
            )

        except FileNotFoundError:
            return ToolResult.error_result(
                "patch command not found",
                suggestions=["Install patch: brew install gpatch"],
            )
        except subprocess.TimeoutExpired:
            return ToolResult.error_result("Patch timed out")
        except Exception as e:
            return ToolResult.error_result(f"Failed to apply diff: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to patch",
                },
                "diff": {
                    "type": "string",
                    "description": "Unified diff content to apply",
                },
            },
            required=["path", "diff"],
        )


class DeleteFileTool(CodingTool):
    """Delete a file."""

    name = "delete_file"
    description = """Delete a file from the repository.
Use with caution - this cannot be undone."""

    def execute(self, path: str) -> ToolResult:
        """Delete a file.

        Args:
            path: Path to the file

        Returns:
            ToolResult indicating success
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"File not found: {path}")

        if not full_path.is_file():
            return ToolResult.error_result(f"Not a file: {path}")

        try:
            full_path.unlink()

            return ToolResult.success_result(
                data={
                    "path": path,
                    "deleted": True,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to delete file: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Path to the file to delete",
                },
            },
            required=["path"],
        )


class ListFilesTool(CodingTool):
    """List files in a directory."""

    name = "list_files"
    description = """List files in a directory.
Can filter by pattern and recurse into subdirectories."""

    def execute(
        self,
        path: str = ".",
        pattern: Optional[str] = None,
        recursive: bool = False,
    ) -> ToolResult:
        """List files in a directory.

        Args:
            path: Directory path
            pattern: Optional glob pattern
            recursive: Whether to recurse

        Returns:
            ToolResult with file list
        """
        valid, error, full_path = self._validate_path(path)
        if not valid:
            return ToolResult.error_result(error)

        if not full_path.exists():
            return ToolResult.error_result(f"Directory not found: {path}")

        if not full_path.is_dir():
            return ToolResult.error_result(f"Not a directory: {path}")

        try:
            files = []
            glob_pattern = pattern or "*"

            if recursive:
                matches = full_path.rglob(glob_pattern)
            else:
                matches = full_path.glob(glob_pattern)

            for match in matches:
                if match.is_file():
                    # Get relative path from repo root
                    rel_path = match.relative_to(self.repo_root)
                    files.append({
                        "path": str(rel_path),
                        "size": match.stat().st_size,
                    })

            # Sort by path
            files.sort(key=lambda x: x["path"])

            return ToolResult.success_result(
                data={
                    "directory": path,
                    "files": files[:1000],  # Limit results
                    "count": len(files),
                    "truncated": len(files) > 1000,
                },
            )

        except Exception as e:
            return ToolResult.error_result(f"Failed to list files: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "path": {
                    "type": "string",
                    "description": "Directory path (default: current directory)",
                    "default": ".",
                },
                "pattern": {
                    "type": "string",
                    "description": "Glob pattern to filter files",
                },
                "recursive": {
                    "type": "boolean",
                    "description": "Recurse into subdirectories",
                    "default": False,
                },
            },
            required=[],
        )


class ExecuteCommandTool(CodingTool):
    """Execute a shell command."""

    name = "execute_command"
    description = """Execute a shell command in the repository.
Commands are run from the repository root."""

    def execute(
        self,
        command: str,
        timeout: int = 60,
    ) -> ToolResult:
        """Execute a command.

        Args:
            command: Command to execute
            timeout: Timeout in seconds

        Returns:
            ToolResult with command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_root,
                timeout=timeout,
            )

            return ToolResult.success_result(
                data={
                    "command": command,
                    "exit_code": result.returncode,
                    "stdout": result.stdout[-10000:] if result.stdout else "",
                    "stderr": result.stderr[-5000:] if result.stderr else "",
                },
            )

        except subprocess.TimeoutExpired:
            return ToolResult.error_result(
                f"Command timed out after {timeout}s",
            )
        except Exception as e:
            return ToolResult.error_result(f"Command failed: {e}")

    def get_schema(self) -> dict:
        """Get OpenAI function schema."""
        return self._make_schema(
            properties={
                "command": {
                    "type": "string",
                    "description": "Shell command to execute",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds",
                    "default": 60,
                },
            },
            required=["command"],
        )
