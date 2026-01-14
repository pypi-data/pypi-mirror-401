"""Swarm (multi-agent) endpoints with SSE streaming."""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/swarm", tags=["swarm"])

_executor = ThreadPoolExecutor(max_workers=1)


class SwarmRequest(BaseModel):
    """Request to run swarm."""
    tasks: list[str] = Field(..., description="List of tasks to run in parallel")
    model: Optional[str] = Field(default=None, description="LLM model")
    workers: int = Field(default=3, description="Number of parallel workers")
    timeout: int = Field(default=300, description="Timeout per task in seconds")
    base_branch: Optional[str] = Field(default=None, description="Base branch")
    auto_merge: bool = Field(default=True, description="Auto-merge completed branches")
    llm_merge: bool = Field(default=False, description="Use LLM for merge conflicts")


class SwarmStatus(BaseModel):
    """Status of swarm execution."""
    is_running: bool
    tasks_total: int
    tasks_completed: int
    tasks_failed: int
    current_tasks: list[str]


class SwarmSession(BaseModel):
    """An active swarm session."""
    id: str
    task: str
    status: str  # running, completed, failed
    branch: Optional[str] = None


def _run_swarm_sync(
    tasks: list[str],
    model: Optional[str],
    workers: int,
    sse_handler: SSEHandler,
):
    """Run swarm synchronously."""
    import sys
    from pathlib import Path

    repo_root = Path(__file__).parent.parent.parent.parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    try:
        from ..swarm.swarm_runner import SwarmRunner
        from ..agent.events import AgentEventEmitter

        class SSEBridge:
            def __init__(self, handler):
                self._handler = handler

            def handle(self, event):
                self._handler.handle(event)

        emitter = AgentEventEmitter(agent_name="Swarm")
        emitter.add_handler(SSEBridge(sse_handler))

        runner = SwarmRunner(
            repo_root=repo_root,
            model=model or "gpt-4o-mini",
            max_workers=workers,
        )

        sse_handler.emit(EventType.PROGRESS, {
            "step": f"Starting {len(tasks)} tasks with {workers} workers",
            "percent": 0,
        })

        state = runner.run(tasks)

        # Count results from swarm state
        from ..swarm.task_definition import TaskStatus
        completed = sum(1 for t in state.tasks if t.status == TaskStatus.COMPLETED)
        failed = sum(1 for t in state.tasks if t.status == TaskStatus.FAILED)

        sse_handler.emit(EventType.RESPONSE, {
            "completed": completed,
            "failed": failed,
            "results": [{"slug": t.slug, "status": t.status.value} for t in state.tasks],
        })

    except Exception as e:
        sse_handler.emit(EventType.ERROR, {"message": str(e)})
    finally:
        sse_handler.close()


@router.post("/run")
async def run_swarm(request: SwarmRequest):
    """Run multiple agents in parallel on separate tasks.

    Each task runs in its own git worktree branch.
    """
    if not request.tasks:
        raise HTTPException(status_code=400, detail="No tasks provided")

    sse_handler = SSEHandler(agent_name="Swarm")

    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Swarm",
        "task_count": len(request.tasks),
        "workers": request.workers,
    })

    async def run():
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            _executor,
            _run_swarm_sync,
            request.tasks,
            request.model,
            request.workers,
            sse_handler,
        )

    asyncio.create_task(run())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@router.get("/status", response_model=SwarmStatus)
async def get_swarm_status():
    """Get status of current swarm execution."""
    # TODO: Implement actual status tracking
    return SwarmStatus(
        is_running=False,
        tasks_total=0,
        tasks_completed=0,
        tasks_failed=0,
        current_tasks=[],
    )


@router.get("/sessions")
async def get_swarm_sessions():
    """List active swarm sessions."""
    # TODO: Implement session tracking
    return {"sessions": []}


@router.post("/cleanup")
async def cleanup_swarm(force: bool = False):
    """Clean up all swarm worktrees and branches."""
    try:
        from pathlib import Path
        from ..swarm.swarm_runner import SwarmRunner

        repo_root = Path(__file__).parent.parent.parent.parent.parent
        runner = SwarmRunner.load(repo_root)

        if runner:
            cleaned = runner.cleanup()
        else:
            # No active swarm, just cleanup orphaned worktrees
            from ..swarm.worktree_manager import WorktreeManager
            manager = WorktreeManager(repo_root)
            cleaned = manager.cleanup_all()

        return {
            "success": True,
            "cleaned_worktrees": cleaned,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/merge")
async def merge_swarm_branches(
    llm_merge: bool = False,
    target: Optional[str] = None,
):
    """Merge all completed task branches."""
    try:
        from pathlib import Path
        from ..swarm.swarm_runner import SwarmRunner

        repo_root = Path(__file__).parent.parent.parent.parent.parent
        runner = SwarmRunner.load(repo_root)

        if not runner:
            return {
                "success": False,
                "error": "No active swarm found",
                "merged_branches": [],
                "conflicts": [],
            }

        results = runner.merge_completed(
            use_llm=llm_merge,
            target_branch=target,
        )

        merged = [r.task_id for r in results if r.success]
        failed = [{"task_id": r.task_id, "conflicts": r.conflicts, "error": r.error_message}
                  for r in results if not r.success]

        return {
            "success": len(failed) == 0,
            "merged_tasks": merged,
            "failed": failed,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
