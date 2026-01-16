"""
Delegation tools for the orchestrator.

These are the core tools that orchestrators use to delegate work to executors:
- delegate: Start a new session with an executor
- converse: Continue a sync conversation
- check_session: Check status of an async session
- end_session: End a session
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any, Literal

from wbal.helper import weaveTool

if TYPE_CHECKING:
    from zwarm.orchestrator import Orchestrator


def _truncate(text: str, max_len: int = 200) -> str:
    """Truncate text with ellipsis."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def _format_session_header(session_id: str, adapter: str, mode: str) -> str:
    """Format a nice session header."""
    return f"[{session_id[:8]}] {adapter} ({mode})"


@weaveTool
def delegate(
    self: "Orchestrator",
    task: str,
    mode: Literal["sync", "async"] = "sync",
    adapter: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    """
    Delegate work to an executor agent.

    Use this to assign coding tasks to an executor. Two modes available:

    **sync** (default): Start a conversation with the executor.
    You can iteratively refine requirements using converse().
    Best for: ambiguous tasks, complex requirements, tasks needing guidance.

    **async**: Fire-and-forget execution.
    Check progress later with check_session().
    Best for: clear self-contained tasks, parallel work.

    Args:
        task: Clear description of what to do. Be specific about requirements.
        mode: "sync" for conversational, "async" for fire-and-forget.
        adapter: Which executor adapter to use (default: config setting).
        model: Model override for the executor.

    Returns:
        {session_id, status, response (if sync)}

    Example:
        delegate(task="Add a logout button to the navbar", mode="sync")
        # Then use converse() to refine: "Also add a confirmation dialog"
    """
    # Get adapter (use default from config if not specified)
    adapter_name = adapter or self.config.executor.adapter
    executor = self._get_adapter(adapter_name)

    # Run async start_session
    session = asyncio.get_event_loop().run_until_complete(
        executor.start_session(
            task=task,
            working_dir=self.working_dir,
            mode=mode,
            model=model or self.config.executor.model,
            sandbox=self.config.executor.sandbox,
        )
    )

    # Track session
    self._sessions[session.id] = session
    self.state.add_session(session)

    # Log events
    from zwarm.core.models import event_session_started, event_message_sent, Message
    self.state.log_event(event_session_started(session))
    self.state.log_event(event_message_sent(session, Message(role="user", content=task)))

    # Get response for sync mode
    response_text = ""
    if mode == "sync" and session.messages:
        response_text = session.messages[-1].content
        # Log the assistant response too
        self.state.log_event(event_message_sent(
            session,
            Message(role="assistant", content=response_text)
        ))

    # Build nice result
    header = _format_session_header(session.id, adapter_name, mode)

    if mode == "sync":
        return {
            "success": True,
            "session": header,
            "session_id": session.id,
            "status": "active",
            "task": _truncate(task, 100),
            "response": response_text,
            "hint": "Use converse(session_id, message) to continue this conversation",
        }
    else:
        return {
            "success": True,
            "session": header,
            "session_id": session.id,
            "status": "running",
            "task": _truncate(task, 100),
            "hint": "Use check_session(session_id) to monitor progress",
        }


@weaveTool
def converse(
    self: "Orchestrator",
    session_id: str,
    message: str,
) -> dict[str, Any]:
    """
    Continue a sync conversation with an executor.

    Use this to iteratively refine requirements, ask for changes,
    or guide the executor step-by-step. Like chatting with a developer.

    Args:
        session_id: The session to continue (from delegate() result).
        message: Your next message to the executor.

    Returns:
        {session_id, response, turn}

    Example:
        result = delegate(task="Add user authentication")
        # Executor responds with initial plan
        converse(session_id=result["session_id"], message="Use JWT, not sessions")
        # Executor adjusts approach
        converse(session_id=result["session_id"], message="Now add tests")
    """
    session = self._sessions.get(session_id)
    if not session:
        return {
            "success": False,
            "error": f"Unknown session: {session_id}",
            "hint": "Use list_sessions() to see available sessions",
        }

    if session.mode.value != "sync":
        return {
            "success": False,
            "error": "Cannot converse with async session",
            "hint": "Use check_session() for async sessions instead",
        }

    if session.status.value != "active":
        return {
            "success": False,
            "error": f"Session is {session.status.value}, not active",
            "hint": "Start a new session with delegate()",
        }

    # Get adapter and send message
    executor = self._get_adapter(session.adapter)
    try:
        response = asyncio.get_event_loop().run_until_complete(
            executor.send_message(session, message)
        )
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "session_id": session_id,
        }

    # Update state
    self.state.update_session(session)

    # Log both messages
    from zwarm.core.models import event_message_sent, Message
    self.state.log_event(event_message_sent(session, Message(role="user", content=message)))
    self.state.log_event(event_message_sent(session, Message(role="assistant", content=response)))

    # Calculate turn number
    turn = len([m for m in session.messages if m.role == "user"])
    header = _format_session_header(session.id, session.adapter, session.mode.value)

    return {
        "success": True,
        "session": header,
        "session_id": session_id,
        "turn": turn,
        "you_said": _truncate(message, 100),
        "response": response,
    }


@weaveTool
def check_session(
    self: "Orchestrator",
    session_id: str,
) -> dict[str, Any]:
    """
    Check the status of a session.

    For async sessions: Check if the executor has finished.
    For sync sessions: Get current status and message count.

    Args:
        session_id: The session to check.

    Returns:
        {session_id, status, ...}
    """
    session = self._sessions.get(session_id)
    if not session:
        return {
            "success": False,
            "error": f"Unknown session: {session_id}",
            "hint": "Use list_sessions() to see available sessions",
        }

    executor = self._get_adapter(session.adapter)
    status = asyncio.get_event_loop().run_until_complete(
        executor.check_status(session)
    )

    # Update state if status changed
    self.state.update_session(session)

    header = _format_session_header(session.id, session.adapter, session.mode.value)

    return {
        "success": True,
        "session": header,
        "session_id": session_id,
        "mode": session.mode.value,
        "status": session.status.value,
        "messages": len(session.messages),
        "task": _truncate(session.task_description, 80),
        **status,
    }


@weaveTool
def end_session(
    self: "Orchestrator",
    session_id: str,
    verdict: Literal["completed", "failed", "cancelled"] = "completed",
    summary: str | None = None,
) -> dict[str, Any]:
    """
    End a session with a verdict.

    Call this when:
    - Task is done (verdict="completed")
    - Task failed and you're giving up (verdict="failed")
    - You want to stop early (verdict="cancelled")

    Args:
        session_id: The session to end.
        verdict: How the session ended.
        summary: Optional summary of what was accomplished.

    Returns:
        {session_id, status, summary}
    """
    session = self._sessions.get(session_id)
    if not session:
        return {
            "success": False,
            "error": f"Unknown session: {session_id}",
        }

    # Stop the session if still running
    if session.status.value == "active":
        executor = self._get_adapter(session.adapter)
        if verdict == "completed":
            session.complete(summary)
        else:
            asyncio.get_event_loop().run_until_complete(executor.stop(session))
            if verdict == "failed":
                session.fail(summary)
            else:
                session.fail(f"Cancelled: {summary}" if summary else "Cancelled")

    # Update state
    self.state.update_session(session)

    # Log event
    from zwarm.core.models import event_session_completed
    self.state.log_event(event_session_completed(session))

    header = _format_session_header(session.id, session.adapter, session.mode.value)
    verdict_icon = {"completed": "✓", "failed": "✗", "cancelled": "○"}.get(verdict, "?")

    return {
        "success": True,
        "session": header,
        "session_id": session_id,
        "verdict": f"{verdict_icon} {verdict}",
        "summary": session.exit_message or "(no summary)",
        "total_turns": len([m for m in session.messages if m.role == "user"]),
    }


@weaveTool
def list_sessions(
    self: "Orchestrator",
    status: str | None = None,
) -> dict[str, Any]:
    """
    List all sessions, optionally filtered by status.

    Args:
        status: Filter by status ("active", "completed", "failed").

    Returns:
        {sessions: [...], count}
    """
    sessions = self.state.list_sessions(status=status)

    session_list = []
    for s in sessions:
        status_icon = {
            "active": "●",
            "completed": "✓",
            "failed": "✗",
        }.get(s.status.value, "?")

        session_list.append({
            "id": s.id[:8] + "...",
            "full_id": s.id,
            "status": f"{status_icon} {s.status.value}",
            "adapter": s.adapter,
            "mode": s.mode.value,
            "task": _truncate(s.task_description, 60),
            "turns": len([m for m in s.messages if m.role == "user"]),
        })

    return {
        "success": True,
        "sessions": session_list,
        "count": len(sessions),
        "filter": status or "all",
    }
