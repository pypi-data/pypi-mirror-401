"""
Claude Code adapter for sync/async execution.

Uses the claude CLI for conversations:
- claude -p --output-format json for non-interactive mode
- claude -r <session_id> to continue conversations
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
from pathlib import Path
from typing import Any, Literal

import weave

from zwarm.adapters.base import ExecutorAdapter
from zwarm.core.models import (
    ConversationSession,
    SessionMode,
    SessionStatus,
)


class ClaudeCodeAdapter(ExecutorAdapter):
    """
    Claude Code adapter using the claude CLI.

    Supports both sync (conversational) and async (fire-and-forget) modes.
    """

    name = "claude_code"

    def __init__(self, model: str | None = None):
        self._model = model
        self._sessions: dict[str, str] = {}  # session_id -> claude session_id

    @weave.op()
    async def _call_claude(
        self,
        task: str,
        cwd: str,
        model: str | None = None,
        permission_mode: str = "bypassPermissions",
    ) -> dict[str, Any]:
        """
        Call claude CLI - traced by Weave.

        This wraps the actual claude call so it appears in Weave traces
        with full input/output visibility.
        """
        cmd = ["claude", "-p", "--output-format", "json"]

        if permission_mode:
            cmd.extend(["--permission-mode", permission_mode])
        if model:
            cmd.extend(["--model", model])

        cmd.extend(["--", task])

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300,
            )
        )

        response_text = self._extract_response(result.stdout, result.stderr)

        # Try to get session ID from JSON output
        session_id = None
        try:
            output = json.loads(result.stdout)
            session_id = output.get("session_id")
        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "response": response_text,
            "session_id": session_id,
            "exit_code": result.returncode,
        }

    @weave.op()
    async def _call_claude_continue(
        self,
        message: str,
        cwd: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Continue a claude conversation - traced by Weave.

        This wraps the continuation call so it appears in Weave traces
        with full input/output visibility.
        """
        cmd = ["claude", "-p", "--output-format", "json"]

        if session_id:
            cmd.extend(["--resume", session_id])
        else:
            cmd.extend(["--continue"])

        cmd.extend(["--permission-mode", "bypassPermissions"])
        cmd.extend(["--", message])

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=300,
            )
        )

        response_text = self._extract_response(result.stdout, result.stderr)

        # Try to get session ID from JSON output
        new_session_id = None
        try:
            output = json.loads(result.stdout)
            new_session_id = output.get("session_id")
        except (json.JSONDecodeError, TypeError):
            pass

        return {
            "response": response_text,
            "session_id": new_session_id or session_id,
            "exit_code": result.returncode,
        }

    async def start_session(
        self,
        task: str,
        working_dir: Path,
        mode: Literal["sync", "async"] = "sync",
        model: str | None = None,
        permission_mode: str = "bypassPermissions",
        **kwargs,
    ) -> ConversationSession:
        """Start a Claude Code session."""
        session = ConversationSession(
            adapter=self.name,
            mode=SessionMode(mode),
            working_dir=working_dir,
            task_description=task,
            model=model or self._model,
        )

        if mode == "sync":
            # Use traced claude call
            result = await self._call_claude(
                task=task,
                cwd=str(working_dir),
                model=model or self._model,
                permission_mode=permission_mode,
            )

            # Extract session ID and response
            if result["session_id"]:
                session.conversation_id = result["session_id"]
                self._sessions[session.id] = session.conversation_id

            session.add_message("user", task)
            session.add_message("assistant", result["response"])

        else:
            # Async mode: run in background
            cmd = ["claude", "-p", "--output-format", "json"]
            if permission_mode:
                cmd.extend(["--permission-mode", permission_mode])
            if model or self._model:
                cmd.extend(["--model", model or self._model])
            cmd.extend(["--", task])

            proc = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            session.process = proc
            session.add_message("user", task)

        return session

    async def send_message(
        self,
        session: ConversationSession,
        message: str,
    ) -> str:
        """Send a message to continue a sync conversation."""
        if session.mode != SessionMode.SYNC:
            raise ValueError("Cannot send message to async session")
        if session.status != SessionStatus.ACTIVE:
            raise ValueError(f"Session is not active: {session.status}")

        # Use traced continuation call
        result = await self._call_claude_continue(
            message=message,
            cwd=str(session.working_dir),
            session_id=session.conversation_id,
        )

        # Update session ID if we didn't have one
        if not session.conversation_id and result["session_id"]:
            session.conversation_id = result["session_id"]
            self._sessions[session.id] = session.conversation_id

        response_text = result["response"]
        session.add_message("user", message)
        session.add_message("assistant", response_text)

        return response_text

    async def check_status(
        self,
        session: ConversationSession,
    ) -> dict:
        """Check status of an async session."""
        if session.mode != SessionMode.ASYNC:
            return {"status": session.status.value}

        if session.process is None:
            return {"status": "unknown", "error": "No process handle"}

        # Check if process is still running
        poll = session.process.poll()
        if poll is None:
            return {"status": "running"}

        # Process finished
        stdout, stderr = session.process.communicate()
        if poll == 0:
            response = self._extract_response(stdout, stderr)
            session.complete(response[:1000] if response else "Completed")
            return {"status": "completed", "output": response}
        else:
            session.fail(stderr[:1000] if stderr else f"Exit code: {poll}")
            return {"status": "failed", "error": stderr, "exit_code": poll}

    async def stop(
        self,
        session: ConversationSession,
    ) -> None:
        """Stop a session."""
        if session.process and session.process.poll() is None:
            session.process.terminate()
            try:
                session.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                session.process.kill()

        session.fail("Stopped by user")

        # Remove from tracking
        if session.id in self._sessions:
            del self._sessions[session.id]

    def _extract_response(self, stdout: str, stderr: str) -> str:
        """Extract response text from CLI output."""
        # Try to parse as JSON
        try:
            output = json.loads(stdout)

            # Check for result/response fields
            if "result" in output:
                return output["result"]
            if "response" in output:
                return output["response"]
            if "content" in output:
                return output["content"]
            if "text" in output:
                return output["text"]

            # Handle messages array
            if "messages" in output and isinstance(output["messages"], list):
                for msg in reversed(output["messages"]):
                    if isinstance(msg, dict) and msg.get("role") == "assistant":
                        return msg.get("content", "")

            # Fallback: stringify the output
            return json.dumps(output, indent=2)

        except json.JSONDecodeError:
            # Not JSON, return raw output
            if stdout.strip():
                return stdout.strip()
            if stderr.strip():
                return f"Error: {stderr.strip()}"
            return "(no output)"
