"""
OrchestratorEnv: A lean environment for the zwarm orchestrator.

Unlike ChatEnv, this environment:
- Has no notes/observations (we use StateManager instead)
- Has no chat() tool (orchestrator communicates via output_handler)
- Shows active sessions in observe() for context
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, TYPE_CHECKING

from wbal.environment import Environment

if TYPE_CHECKING:
    from zwarm.core.models import ConversationSession


class OrchestratorEnv(Environment):
    """
    Lean environment for the orchestrator agent.

    Provides:
    - Task context
    - Working directory info
    - Active session visibility
    - Output handler for messages
    """

    task: str = ""
    working_dir: Path = Path(".")
    output_handler: Callable[[str], None] = lambda x: print(x)

    # Session tracking (set by orchestrator)
    _sessions: dict[str, "ConversationSession"] | None = None

    def set_sessions(self, sessions: dict[str, "ConversationSession"]) -> None:
        """Set the sessions dict for observe() visibility."""
        self._sessions = sessions

    def observe(self) -> str:
        """
        Return observable state for the orchestrator.

        Shows:
        - Current task
        - Working directory
        - Active sessions with their status
        """
        parts = []

        # Task
        if self.task:
            parts.append(f"## Current Task\n{self.task}")

        # Working directory
        parts.append(f"## Working Directory\n{self.working_dir.absolute()}")

        # Active sessions
        if self._sessions:
            session_lines = []
            for sid, session in self._sessions.items():
                status_icon = {
                    "active": "[ACTIVE]",
                    "completed": "[DONE]",
                    "failed": "[FAILED]",
                }.get(session.status.value, "[?]")

                mode_icon = "sync" if session.mode.value == "sync" else "async"
                task_preview = session.task_description[:60] + "..." if len(session.task_description) > 60 else session.task_description

                session_lines.append(
                    f"  - {sid[:8]}... {status_icon} ({mode_icon}, {session.adapter}) {task_preview}"
                )

            if session_lines:
                parts.append("## Sessions\n" + "\n".join(session_lines))
            else:
                parts.append("## Sessions\n  (none)")

        return "\n\n".join(parts)
