"""Agent chat endpoint with SSE streaming."""

import asyncio
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..config import get_config
from ..models.agent import AgentChatRequest, AgentMode
from ..sse.stream import SSEHandler, EventType

router = APIRouter(prefix="/agent", tags=["agent"])

# Thread pool for running blocking agent code
_executor = ThreadPoolExecutor(max_workers=4)

# Active sessions (in-memory for now)
_sessions: dict[str, dict] = {}


def _ensure_emdash_importable():
    """Ensure the emdash_core package is importable.

    This is now a no-op since we use emdash_core directly.
    """
    pass  # emdash_core is already in the package


def _run_agent_sync(
    message: str,
    model: str,
    max_iterations: int,
    sse_handler: SSEHandler,
    session_id: str,
    images: list = None,
    plan_mode: bool = False,
):
    """Run the agent synchronously (in thread pool).

    This function runs in a background thread and emits events
    to the SSE handler for streaming to the client.
    """
    try:
        _ensure_emdash_importable()

        # Import agent components from emdash_core
        from ..agent.runner import AgentRunner
        from ..agent.toolkit import AgentToolkit
        from ..agent.events import AgentEventEmitter

        # Create an emitter that forwards to SSE handler
        class SSEBridgeHandler:
            """Bridges AgentEventEmitter to SSEHandler."""

            def __init__(self, sse_handler: SSEHandler):
                self._sse = sse_handler

            def handle(self, event):
                """Forward event to SSE handler."""
                self._sse.handle(event)

        # Create agent with event emitter
        emitter = AgentEventEmitter(agent_name="Emdash Code")
        emitter.add_handler(SSEBridgeHandler(sse_handler))

        # Create toolkit with plan_mode if requested
        toolkit = AgentToolkit(plan_mode=plan_mode)

        runner = AgentRunner(
            toolkit=toolkit,
            model=model,
            verbose=True,
            max_iterations=max_iterations,
            emitter=emitter,
        )

        # Store session state BEFORE running (so it exists even if interrupted)
        _sessions[session_id] = {
            "runner": runner,
            "message_count": 1,
            "model": model,
            "plan_mode": plan_mode,
        }

        # Convert image data if provided
        agent_images = None
        if images:
            from ..agent.providers.base import ImageContent
            agent_images = [
                ImageContent(data=img.data, format=img.format)
                for img in images
            ]

        # Run the agent
        response = runner.run(message, images=agent_images)

        return response

    except Exception as e:
        # Emit error event
        sse_handler.emit(EventType.ERROR, {
            "message": str(e),
            "details": None,
        })
        raise


async def _run_agent_async(
    request: AgentChatRequest,
    sse_handler: SSEHandler,
    session_id: str,
):
    """Run agent in thread pool and stream events."""
    config = get_config()

    # Get model from request or config
    model = request.model or config.default_model
    max_iterations = request.options.max_iterations
    plan_mode = request.options.mode == AgentMode.PLAN

    # Emit session start
    sse_handler.emit(EventType.SESSION_START, {
        "agent_name": "Emdash Code",
        "model": model,
        "session_id": session_id,
        "query": request.message,
        "mode": request.options.mode.value,
    })

    loop = asyncio.get_event_loop()

    try:
        # Run agent in thread pool
        await loop.run_in_executor(
            _executor,
            _run_agent_sync,
            request.message,
            model,
            max_iterations,
            sse_handler,
            session_id,
            request.images,
            plan_mode,
        )

        # Emit session end
        sse_handler.emit(EventType.SESSION_END, {
            "success": True,
            "session_id": session_id,
        })

    except Exception as e:
        sse_handler.emit(EventType.SESSION_END, {
            "success": False,
            "error": str(e),
            "session_id": session_id,
        })

    finally:
        sse_handler.close()


@router.post("/chat")
async def agent_chat(request: AgentChatRequest):
    """Start an agent chat session with SSE streaming.

    The response is a Server-Sent Events stream containing:
    - session_start: Initial session info
    - tool_start: When a tool begins execution
    - tool_result: When a tool completes
    - thinking: Agent reasoning messages
    - response/partial_response: Agent text output
    - clarification: When agent needs user input
    - error/warning: Error messages
    - session_end: Session completion

    Example:
        curl -N -X POST http://localhost:8765/api/agent/chat \\
            -H "Content-Type: application/json" \\
            -d '{"message": "Find authentication code"}'
    """
    # Generate or use provided session ID
    session_id = request.session_id or str(uuid.uuid4())

    # Create SSE handler
    sse_handler = SSEHandler(agent_name="Emdash Code")

    # Start agent in background
    asyncio.create_task(_run_agent_async(request, sse_handler, session_id))

    # Return SSE stream
    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.post("/chat/{session_id}/continue")
async def continue_chat(session_id: str, request: AgentChatRequest):
    """Continue an existing chat session.

    This allows multi-turn conversations by reusing the session state.
    """
    if session_id not in _sessions:
        raise HTTPException(
            status_code=404,
            detail=f"Session {session_id} not found"
        )

    session = _sessions[session_id]
    runner = session.get("runner")
    if not runner:
        raise HTTPException(
            status_code=400,
            detail="Session has no active runner"
        )

    # Create SSE handler
    sse_handler = SSEHandler(agent_name="Emdash Code")

    async def _continue_session():
        sse_handler.emit(EventType.SESSION_START, {
            "agent_name": "Emdash Code",
            "model": session["model"],
            "session_id": session_id,
            "query": request.message,
            "continued": True,
        })

        loop = asyncio.get_event_loop()

        try:
            # Wire up SSE handler to runner's emitter for this request
            from ..agent.events import AgentEventEmitter

            class SSEBridgeHandler:
                def __init__(self, sse_handler: SSEHandler):
                    self._sse = sse_handler

                def handle(self, event):
                    self._sse.handle(event)

            # Create fresh emitter with new SSE handler
            emitter = AgentEventEmitter(agent_name="Emdash Code")
            emitter.add_handler(SSEBridgeHandler(sse_handler))
            runner.emitter = emitter

            # Continue conversation in thread pool
            await loop.run_in_executor(
                _executor,
                lambda: runner.chat(request.message),
            )

            session["message_count"] += 1

            sse_handler.emit(EventType.SESSION_END, {
                "success": True,
                "session_id": session_id,
            })

        except Exception as e:
            sse_handler.emit(EventType.ERROR, {
                "message": str(e),
            })
            sse_handler.emit(EventType.SESSION_END, {
                "success": False,
                "error": str(e),
                "session_id": session_id,
            })

        finally:
            sse_handler.close()

    asyncio.create_task(_continue_session())

    return StreamingResponse(
        sse_handler,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Session-ID": session_id,
        },
    )


@router.get("/sessions")
async def list_sessions():
    """List active chat sessions."""
    return {
        "sessions": [
            {
                "session_id": sid,
                "model": data.get("model"),
                "message_count": data.get("message_count", 0),
            }
            for sid, data in _sessions.items()
        ]
    }


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a chat session."""
    if session_id in _sessions:
        del _sessions[session_id]
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Session not found")
