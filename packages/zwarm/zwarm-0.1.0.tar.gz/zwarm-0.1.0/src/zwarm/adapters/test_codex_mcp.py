"""Tests for Codex MCP adapter."""

import asyncio
import subprocess
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from zwarm.adapters.codex_mcp import CodexMCPAdapter, MCPClient
from zwarm.core.models import SessionMode, SessionStatus


class TestMCPClient:
    """Tests for the MCP client."""

    def test_next_id_increments(self):
        proc = MagicMock()
        client = MCPClient(proc)
        assert client._next_id() == 1
        assert client._next_id() == 2
        assert client._next_id() == 3


class TestCodexMCPAdapter:
    """Tests for the Codex MCP adapter."""

    @pytest.fixture
    def adapter(self):
        return CodexMCPAdapter()

    @pytest.mark.asyncio
    async def test_start_session_creates_session(self, adapter):
        """Test that start_session creates a proper session object."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock the MCP client
            mock_client = AsyncMock()
            mock_client.call_tool = AsyncMock(return_value={
                "conversationId": "conv-123",
                "content": [{"text": "Hello! I'll help you with that."}],
            })

            with patch.object(adapter, "_ensure_server", return_value=mock_client):
                session = await adapter.start_session(
                    task="Say hello",
                    working_dir=Path(tmpdir),
                    mode="sync",
                )

                assert session.adapter == "codex_mcp"
                assert session.mode == SessionMode.SYNC
                assert session.status == SessionStatus.ACTIVE
                assert session.conversation_id == "conv-123"
                assert len(session.messages) == 2
                assert session.messages[0].role == "user"
                assert session.messages[1].role == "assistant"

    @pytest.mark.asyncio
    async def test_send_message_continues_conversation(self, adapter):
        """Test that send_message continues an existing conversation."""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_client = AsyncMock()
            mock_client.call_tool = AsyncMock(side_effect=[
                # First call: start session
                {
                    "conversationId": "conv-123",
                    "content": [{"text": "Initial response"}],
                },
                # Second call: reply
                {
                    "content": [{"text": "Follow-up response"}],
                },
            ])

            with patch.object(adapter, "_ensure_server", return_value=mock_client):
                session = await adapter.start_session(
                    task="Start task",
                    working_dir=Path(tmpdir),
                    mode="sync",
                )

                response = await adapter.send_message(session, "Continue please")

                assert response == "Follow-up response"
                assert len(session.messages) == 4  # 2 from start + 2 from reply

    @pytest.mark.asyncio
    async def test_send_message_fails_on_async_session(self, adapter):
        """Test that send_message raises error for async sessions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create async session (mocked to avoid actually starting codex)
            with patch("subprocess.Popen") as mock_popen:
                mock_popen.return_value = MagicMock()
                session = await adapter.start_session(
                    task="Async task",
                    working_dir=Path(tmpdir),
                    mode="async",
                )

            with pytest.raises(ValueError, match="Cannot send message to async session"):
                await adapter.send_message(session, "Should fail")

    @pytest.mark.asyncio
    async def test_check_status_async_running(self, adapter):
        """Test checking status of a running async session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("subprocess.Popen") as mock_popen:
                mock_proc = MagicMock()
                mock_proc.poll.return_value = None  # Still running
                mock_popen.return_value = mock_proc

                session = await adapter.start_session(
                    task="Async task",
                    working_dir=Path(tmpdir),
                    mode="async",
                )

                status = await adapter.check_status(session)
                assert status["status"] == "running"

    @pytest.mark.asyncio
    async def test_check_status_async_completed(self, adapter):
        """Test checking status of a completed async session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("subprocess.Popen") as mock_popen:
                mock_proc = MagicMock()
                mock_proc.poll.return_value = 0  # Completed
                mock_proc.communicate.return_value = ("Output text", "")
                mock_popen.return_value = mock_proc

                session = await adapter.start_session(
                    task="Async task",
                    working_dir=Path(tmpdir),
                    mode="async",
                )

                status = await adapter.check_status(session)
                assert status["status"] == "completed"
                assert session.status == SessionStatus.COMPLETED

    @pytest.mark.asyncio
    async def test_stop_session(self, adapter):
        """Test stopping a session."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with patch("subprocess.Popen") as mock_popen:
                mock_proc = MagicMock()
                mock_proc.poll.return_value = None  # Running
                mock_popen.return_value = mock_proc

                session = await adapter.start_session(
                    task="Async task",
                    working_dir=Path(tmpdir),
                    mode="async",
                )

                await adapter.stop(session)

                mock_proc.terminate.assert_called_once()
                assert session.status == SessionStatus.FAILED

    def test_extract_response_content_list(self, adapter):
        """Test response extraction from content list."""
        result = {"content": [{"text": "Line 1"}, {"text": "Line 2"}]}
        response = adapter._extract_response(result)
        assert response == "Line 1\nLine 2"

    def test_extract_response_output(self, adapter):
        """Test response extraction from output field."""
        result = {"output": "Direct output"}
        response = adapter._extract_response(result)
        assert response == "Direct output"

    def test_extract_response_fallback(self, adapter):
        """Test response extraction fallback to JSON."""
        result = {"unknown": "field"}
        response = adapter._extract_response(result)
        assert "unknown" in response


@pytest.mark.integration
class TestCodexMCPIntegration:
    """
    Integration tests that run against real codex mcp-server.

    These tests are skipped by default. Run with:
    pytest -m integration
    """

    @pytest.fixture
    def adapter(self):
        return CodexMCPAdapter()

    @pytest.mark.asyncio
    async def test_real_sync_conversation(self, adapter):
        """Test a real sync conversation with codex."""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Start a simple session
                session = await adapter.start_session(
                    task="What is 2 + 2? Reply with just the number.",
                    working_dir=Path(tmpdir),
                    mode="sync",
                    sandbox="read-only",
                )

                assert session.conversation_id is not None
                assert len(session.messages) >= 2

                # Continue conversation
                response = await adapter.send_message(
                    session,
                    "And what is that number times 3?"
                )

                assert response is not None
                assert len(session.messages) >= 4

            finally:
                await adapter.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "not integration"])
