"""
Codex MCP adapter for sync conversations.

Uses codex mcp-server for true iterative conversations:
- codex() to start a session with conversationId
- codex-reply() to continue the conversation
"""

from __future__ import annotations

import asyncio
import json
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


class MCPClient:
    """Minimal MCP client for communicating with codex mcp-server."""

    def __init__(self, proc: subprocess.Popen):
        self.proc = proc
        self._request_id = 0
        self._initialized = False

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    async def _read_line(self) -> str:
        """Read a line from stdout asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.proc.stdout.readline)

    async def send_request(self, method: str, params: dict | None = None) -> dict:
        """Send JSON-RPC request and wait for response."""
        request: dict[str, Any] = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": method,
        }
        if params:
            request["params"] = params

        request_line = json.dumps(request) + "\n"

        # Write request
        self.proc.stdin.write(request_line)
        self.proc.stdin.flush()

        # Read response
        response_line = await self._read_line()

        if not response_line:
            raise RuntimeError("No response from MCP server")

        response = json.loads(response_line)

        # Check for error
        if "error" in response:
            error = response["error"]
            raise RuntimeError(f"MCP error: {error.get('message', error)}")

        return response

    async def initialize(self) -> dict:
        """Initialize MCP connection."""
        result = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "zwarm", "version": "0.1.0"},
        })

        # Send initialized notification
        notif = json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
        }) + "\n"
        self.proc.stdin.write(notif)
        self.proc.stdin.flush()

        self._initialized = True
        return result

    async def call_tool(self, name: str, arguments: dict) -> dict:
        """
        Call an MCP tool and collect streaming events.

        Codex MCP uses streaming events, so we read multiple responses
        until we get the final result.
        """
        if not self._initialized:
            await self.initialize()

        request_id = self._next_id()
        request = {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {
                "name": name,
                "arguments": arguments,
            },
        }
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()

        # Collect streaming events until final result
        session_id = None
        agent_messages: list[str] = []
        final_result = None

        for _ in range(500):  # Safety limit on events
            line = await self._read_line()
            if not line:
                break

            event = json.loads(line)

            # Check for final result (has matching id)
            if event.get("id") == request_id and "result" in event:
                final_result = event.get("result", {})
                break

            # Process streaming events
            if event.get("method") == "codex/event":
                params = event.get("params", {})
                msg = params.get("msg", {})
                msg_type = msg.get("type")

                if msg_type == "session_configured":
                    session_id = msg.get("session_id")
                elif msg_type == "agent_message":
                    agent_messages.append(msg.get("message", ""))
                elif msg_type == "task_completed":
                    # Task is done, break
                    break
                elif msg_type == "error":
                    raise RuntimeError(f"Codex error: {msg.get('error', msg)}")

        # Build result from collected events
        result = {
            "conversationId": session_id,
            "messages": agent_messages,
            "output": "\n".join(agent_messages) if agent_messages else "",
        }
        if final_result:
            result.update(final_result)

        return result

    def close(self) -> None:
        """Close the MCP connection."""
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class CodexMCPAdapter(ExecutorAdapter):
    """
    Codex adapter using MCP server for sync conversations.

    This is the recommended way to have iterative conversations with Codex.
    """

    name = "codex_mcp"

    def __init__(self):
        self._mcp_client: MCPClient | None = None
        self._mcp_proc: subprocess.Popen | None = None
        self._sessions: dict[str, str] = {}  # session_id -> conversationId

    async def _ensure_server(self) -> MCPClient:
        """Ensure MCP server is running and return client."""
        if self._mcp_client is not None:
            # Check if process is still alive
            if self._mcp_proc and self._mcp_proc.poll() is None:
                return self._mcp_client
            # Process died, restart
            self._mcp_client = None
            self._mcp_proc = None

        # Start codex mcp-server
        self._mcp_proc = subprocess.Popen(
            ["codex", "mcp-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._mcp_client = MCPClient(self._mcp_proc)
        await self._mcp_client.initialize()
        return self._mcp_client

    @weave.op()
    async def _call_codex(
        self,
        task: str,
        cwd: str,
        sandbox: str,
        model: str | None = None,
    ) -> dict[str, Any]:
        """
        Call codex MCP tool - traced by Weave.

        This wraps the actual codex call so it appears in Weave traces
        with full input/output visibility.
        """
        client = await self._ensure_server()

        args: dict[str, Any] = {
            "prompt": task,
            "cwd": cwd,
            "sandbox": sandbox,
        }
        if model:
            args["model"] = model

        result = await client.call_tool("codex", args)

        # Return structured result for Weave
        return {
            "conversation_id": result.get("conversationId"),
            "response": self._extract_response(result),
            "raw_messages": result.get("messages", []),
        }

    @weave.op()
    async def _call_codex_reply(
        self,
        conversation_id: str,
        message: str,
    ) -> dict[str, Any]:
        """
        Call codex-reply MCP tool - traced by Weave.

        This wraps the reply call so it appears in Weave traces
        with full input/output visibility.
        """
        client = await self._ensure_server()

        result = await client.call_tool("codex-reply", {
            "conversationId": conversation_id,
            "prompt": message,
        })

        return {
            "response": self._extract_response(result),
            "raw_messages": result.get("messages", []),
        }

    async def start_session(
        self,
        task: str,
        working_dir: Path,
        mode: Literal["sync", "async"] = "sync",
        model: str | None = None,
        sandbox: str = "workspace-write",
        **kwargs,
    ) -> ConversationSession:
        """Start a Codex session."""
        session = ConversationSession(
            adapter=self.name,
            mode=SessionMode(mode),
            working_dir=working_dir,
            task_description=task,
            model=model,
        )

        if mode == "sync":
            # Use traced codex call
            result = await self._call_codex(
                task=task,
                cwd=str(working_dir.absolute()),
                sandbox=sandbox,
                model=model,
            )

            # Extract conversation ID and response
            session.conversation_id = result["conversation_id"]
            self._sessions[session.id] = session.conversation_id

            session.add_message("user", task)
            session.add_message("assistant", result["response"])

        else:
            # Async mode: use codex exec (fire-and-forget)
            # This runs in a subprocess without MCP
            cmd = [
                "codex", "exec",
                "--dangerously-bypass-approvals-and-sandbox",
                "--skip-git-repo-check",
                "--json",
            ]
            if model:
                cmd.extend(["--model", model])
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
        if not session.conversation_id:
            raise ValueError("Session has no conversation ID")

        # Use traced codex-reply call
        result = await self._call_codex_reply(
            conversation_id=session.conversation_id,
            message=message,
        )

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
            session.complete(stdout[:1000] if stdout else "Completed")
            return {"status": "completed", "output": stdout}
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

    async def cleanup(self) -> None:
        """Clean up MCP server."""
        if self._mcp_client:
            self._mcp_client.close()
            self._mcp_client = None
            self._mcp_proc = None

    def _extract_response(self, result: dict) -> str:
        """Extract response text from MCP result."""
        # First check for our collected output
        if "output" in result and result["output"]:
            return result["output"]

        # Check for messages list
        if "messages" in result and result["messages"]:
            return "\n".join(result["messages"])

        # Result may have different structures depending on codex version
        if "content" in result:
            content = result["content"]
            if isinstance(content, list):
                # Extract text from content blocks
                texts = []
                for block in content:
                    if isinstance(block, dict) and "text" in block:
                        texts.append(block["text"])
                    elif isinstance(block, str):
                        texts.append(block)
                return "\n".join(texts)
            elif isinstance(content, str):
                return content

        if "text" in result:
            return result["text"]

        # Fallback: stringify the result
        return json.dumps(result, indent=2)
