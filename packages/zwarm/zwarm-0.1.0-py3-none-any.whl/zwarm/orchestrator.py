"""
Orchestrator: The agent that coordinates multiple executor agents.

The orchestrator:
- Plans and breaks down complex tasks
- Delegates work to executor agents (codex, claude-code, etc.)
- Supervises progress and provides clarification
- Verifies work before marking complete

It does NOT write code directly - that's the executor's job.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

import weave
from pydantic import Field, PrivateAttr
from wbal.agents.yaml_agent import YamlAgent
from wbal.helper import TOOL_CALL_TYPE, format_openai_tool_response

from zwarm.adapters.base import ExecutorAdapter
from zwarm.adapters.claude_code import ClaudeCodeAdapter
from zwarm.adapters.codex_mcp import CodexMCPAdapter
from zwarm.core.config import ZwarmConfig, load_config
from zwarm.core.environment import OrchestratorEnv
from zwarm.core.models import ConversationSession
from zwarm.core.state import StateManager
from zwarm.prompts import get_orchestrator_prompt
from zwarm.watchers import WatcherManager, WatcherContext, WatcherAction, build_watcher_manager


class Orchestrator(YamlAgent):
    """
    Multi-agent orchestrator built on WBAL's YamlAgent.

    Extends YamlAgent with:
    - Delegation tools (delegate, converse, check_session, end_session)
    - Session tracking
    - State persistence
    - Watcher integration
    - Weave integration
    """

    # Configuration
    config: ZwarmConfig = Field(default_factory=ZwarmConfig)
    working_dir: Path = Field(default_factory=Path.cwd)

    # Load tools from modules (delegation + bash for verification)
    agent_tool_modules: list[str] = Field(default=[
        "zwarm.tools.delegation",
        "wbal.tools.bash",
    ])

    # State management
    _state: StateManager = PrivateAttr()
    _sessions: dict[str, ConversationSession] = PrivateAttr(default_factory=dict)
    _adapters: dict[str, ExecutorAdapter] = PrivateAttr(default_factory=dict)
    _watcher_manager: WatcherManager | None = PrivateAttr(default=None)
    _resumed: bool = PrivateAttr(default=False)

    def model_post_init(self, __context: Any) -> None:
        """Initialize state and adapters after model creation."""
        super().model_post_init(__context)

        # Initialize state manager
        self._state = StateManager(self.working_dir / self.config.state_dir)
        self._state.init()
        self._state.load()

        # Load existing sessions
        for session in self._state.list_sessions():
            self._sessions[session.id] = session

        # Initialize Weave if configured
        if self.config.weave.enabled and self.config.weave.project:
            weave.init(self.config.weave.project)

        # Initialize watchers if configured
        if self.config.watchers.enabled:
            self._watcher_manager = build_watcher_manager({
                "watchers": [
                    {"name": w.name, "enabled": w.enabled, "config": w.config}
                    for w in self.config.watchers.watchers
                ]
            })

        # Link sessions to environment for observe()
        if hasattr(self.env, 'set_sessions'):
            self.env.set_sessions(self._sessions)

    @property
    def state(self) -> StateManager:
        """Access state manager."""
        return self._state

    def _get_adapter(self, name: str) -> ExecutorAdapter:
        """Get or create an adapter by name."""
        if name not in self._adapters:
            if name == "codex_mcp":
                self._adapters[name] = CodexMCPAdapter()
            elif name == "claude_code":
                self._adapters[name] = ClaudeCodeAdapter()
            else:
                raise ValueError(f"Unknown adapter: {name}")
        return self._adapters[name]

    def save_state(self) -> None:
        """Save orchestrator state for resume."""
        self._state.save_orchestrator_messages(self.messages)

    def load_state(self) -> None:
        """Load orchestrator state for resume."""
        self.messages = self._state.load_orchestrator_messages()
        self._resumed = True

    def _inject_resume_message(self) -> None:
        """Inject a system message about resumed state."""
        if not self._resumed:
            return

        # Build list of old sessions
        old_sessions = []
        for sid, session in self._sessions.items():
            old_sessions.append(f"  - {sid[:8]}... ({session.adapter}, {session.status.value})")

        session_info = "\n".join(old_sessions) if old_sessions else "  (none)"

        resume_msg = {
            "role": "user",
            "content": f"""[SYSTEM NOTICE] You have been resumed from a previous session.

IMPORTANT: Your previous executor sessions are NO LONGER ACTIVE. The MCP connections and subprocess handles were lost when the previous session ended.

Previous sessions (now stale):
{session_info}

You must start NEW sessions with delegate() if you need to continue work. Do NOT try to use converse() or check_session() with the old session IDs - they will fail.

Continue with your task from where you left off."""
        }

        self.messages.append(resume_msg)
        self._resumed = False  # Only inject once

    def _run_watchers(self) -> WatcherAction:
        """Run watchers and return the action to take."""
        if not self._watcher_manager:
            return WatcherAction.CONTINUE

        # Build watcher context
        ctx = WatcherContext(
            step=self._step_count,
            messages=self.messages,
            sessions={sid: s.to_dict() for sid, s in self._sessions.items()},
            task=self.env.task if hasattr(self.env, 'task') else "",
            metadata={
                "max_steps": self.maxSteps,
                "config": self.config.to_dict() if hasattr(self.config, 'to_dict') else {},
            },
        )

        # Run watchers synchronously (they're async internally)
        import asyncio
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # We're in an async context, create a task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                result = pool.submit(asyncio.run, self._watcher_manager.observe(ctx)).result()
        else:
            result = asyncio.run(self._watcher_manager.observe(ctx))

        # Handle watcher result
        if result.action == WatcherAction.NUDGE and result.guidance:
            # Inject guidance as a system message
            self.messages.append({
                "role": "user",
                "content": f"[WATCHER: {result.metadata.get('triggered_by', 'unknown')}] {result.guidance}"
            })

        return result.action

    def do(self) -> list[tuple[dict[str, Any], Any]]:
        """
        Execute tool calls from the LLM response.

        Overrides base do() to capture and return tool calls with results
        for Weave tracing visibility.

        Returns:
            List of (tool_call_info, result) tuples
        """
        if self._last_response is None:
            return []

        output = getattr(self._last_response, 'output', None)
        if output is None:
            return []

        # Extract tool calls
        tool_calls = [
            item for item in output
            if getattr(item, 'type', None) == TOOL_CALL_TYPE
        ]

        # If no tool calls, handle text output
        if not tool_calls:
            output_text = getattr(self._last_response, 'output_text', '')
            if output_text and hasattr(self.env, 'output_handler'):
                self.env.output_handler(output_text)
            return []

        # Execute each tool call and collect results
        tool_results: list[tuple[dict[str, Any], Any]] = []

        for tc in tool_calls:
            tc_name = getattr(tc, 'name', '')
            tc_args_raw = getattr(tc, 'arguments', '{}')
            tc_id = getattr(tc, 'call_id', '')

            # Parse arguments
            if isinstance(tc_args_raw, str):
                try:
                    tc_args = json.loads(tc_args_raw)
                except json.JSONDecodeError:
                    tc_args = {}
            else:
                tc_args = tc_args_raw or {}

            # Execute tool
            if tc_name in self._tool_callables:
                try:
                    tc_output = self._tool_callables[tc_name](**tc_args)
                except Exception as e:
                    tc_output = f"Error executing {tc_name}: {e}"
            else:
                tc_output = f"Unknown tool: {tc_name}"

            # Collect tool call info and result
            tool_call_info = {
                "name": tc_name,
                "args": tc_args,
                "call_id": tc_id,
            }
            tool_results.append((tool_call_info, tc_output))

            # Format and append result to messages
            result = format_openai_tool_response(tc_output, tc_id)
            self.messages.append(result)

        return tool_results

    @weave.op()
    def step(self) -> list[tuple[dict[str, Any], Any]]:
        """
        Execute one perceive-invoke-do cycle.

        Overrides base step() to return tool calls with results
        for Weave tracing visibility.

        Returns:
            List of (tool_call_info, result) tuples from this step.
            Each tuple contains:
            - tool_call_info: {"name": str, "args": dict, "call_id": str}
            - result: The tool output (any type)
        """
        self.perceive()
        self.invoke()
        tool_results = self.do()
        self._step_count += 1
        return tool_results

    @weave.op()
    def run(self, task: str | None = None, max_steps: int | None = None) -> dict[str, Any]:
        """
        Run the orchestrator until stop condition is met.

        Overrides base run() to integrate watchers.

        Args:
            task: The task string. If not provided, uses env.task
            max_steps: Override maxSteps for this run.

        Returns:
            Dict with run results
        """
        # Set task from argument or environment
        if task is not None:
            self.env.task = task

        # Override max_steps if provided
        if max_steps is not None:
            self.maxSteps = max_steps

        # Reset step counter
        self._step_count = 0

        # Inject resume message if we were resumed
        self._inject_resume_message()

        for _ in range(self.maxSteps):
            # Run watchers before each step
            watcher_action = self._run_watchers()

            if watcher_action == WatcherAction.ABORT:
                return {
                    "steps": self._step_count,
                    "task": self.env.task,
                    "stopped_by": "watcher_abort",
                }
            elif watcher_action == WatcherAction.PAUSE:
                # For now, treat pause as stop (could add human-in-loop later)
                return {
                    "steps": self._step_count,
                    "task": self.env.task,
                    "stopped_by": "watcher_pause",
                }
            # NUDGE and CONTINUE just continue

            self.step()

            if self.stopCondition:
                break

        return {
            "steps": self._step_count,
            "task": self.env.task,
        }

    async def cleanup(self) -> None:
        """Clean up resources."""
        for adapter in self._adapters.values():
            await adapter.cleanup()


def build_orchestrator(
    config_path: Path | None = None,
    task: str | None = None,
    working_dir: Path | None = None,
    overrides: list[str] | None = None,
    resume: bool = False,
    output_handler: Callable[[str], None] | None = None,
) -> Orchestrator:
    """
    Build an orchestrator from configuration.

    Args:
        config_path: Path to YAML config file
        task: The task to accomplish
        working_dir: Working directory (default: cwd)
        overrides: CLI overrides (--set key=value)
        resume: Whether to resume from previous state
        output_handler: Function to handle orchestrator output

    Returns:
        Configured Orchestrator instance
    """
    # Load configuration
    config = load_config(
        config_path=config_path,
        overrides=overrides,
    )

    # Resolve working directory
    working_dir = working_dir or Path.cwd()

    # Build system prompt
    system_prompt = _build_system_prompt(config, working_dir)

    # Create lean orchestrator environment
    env = OrchestratorEnv(
        task=task or "",
        working_dir=working_dir,
    )

    # Set up output handler
    if output_handler:
        env.output_handler = output_handler

    # Create orchestrator
    orchestrator = Orchestrator(
        config=config,
        working_dir=working_dir,
        system_prompt=system_prompt,
        maxSteps=config.orchestrator.max_steps,
        env=env,
    )

    # Resume if requested
    if resume:
        orchestrator.load_state()

    return orchestrator


def _build_system_prompt(config: ZwarmConfig, working_dir: Path | None = None) -> str:
    """Build the orchestrator system prompt."""
    return get_orchestrator_prompt(working_dir=str(working_dir) if working_dir else None)
