"""
Base adapter protocol for executor agents.

All CLI coding agent adapters (codex, claude-code, gemini) implement this protocol.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Literal

from zwarm.core.models import ConversationSession, SessionMode


class ExecutorAdapter(ABC):
    """
    Abstract base class for CLI coding agent adapters.

    Adapters handle the mechanics of:
    - Starting sessions (sync or async)
    - Sending messages in sync mode
    - Checking status in async mode
    - Stopping sessions
    """

    name: str = "base"

    @abstractmethod
    async def start_session(
        self,
        task: str,
        working_dir: Path,
        mode: Literal["sync", "async"] = "sync",
        model: str | None = None,
        **kwargs,
    ) -> ConversationSession:
        """
        Start a new session with the executor.

        Args:
            task: The task description/prompt
            working_dir: Directory to work in
            mode: "sync" for conversational, "async" for fire-and-forget
            model: Optional model override
            **kwargs: Adapter-specific options

        Returns:
            A ConversationSession with initial response (if sync)
        """
        ...

    @abstractmethod
    async def send_message(
        self,
        session: ConversationSession,
        message: str,
    ) -> str:
        """
        Send a message to a sync session and get response.

        Args:
            session: The active session
            message: Message to send

        Returns:
            The agent's response

        Raises:
            ValueError: If session is not in sync mode or not active
        """
        ...

    @abstractmethod
    async def check_status(
        self,
        session: ConversationSession,
    ) -> dict:
        """
        Check the status of an async session.

        Args:
            session: The session to check

        Returns:
            Status dict with at least {"status": "running"|"completed"|"failed"}
        """
        ...

    @abstractmethod
    async def stop(
        self,
        session: ConversationSession,
    ) -> None:
        """
        Stop/kill a session.

        Args:
            session: The session to stop
        """
        ...

    async def cleanup(self) -> None:
        """
        Clean up adapter resources (e.g., MCP server).

        Called when the orchestrator shuts down.
        """
        pass
