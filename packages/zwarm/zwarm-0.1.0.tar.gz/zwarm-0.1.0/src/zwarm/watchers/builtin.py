"""
Built-in watchers for common trajectory alignment needs.
"""

from __future__ import annotations

import re
from typing import Any

from zwarm.watchers.base import Watcher, WatcherContext, WatcherResult, WatcherAction
from zwarm.watchers.registry import register_watcher


@register_watcher("progress")
class ProgressWatcher(Watcher):
    """
    Watches for lack of progress.

    Detects when the agent appears stuck:
    - Repeating same tool calls
    - Not making session progress
    - Spinning without completing tasks
    """

    name = "progress"
    description = "Detects when agent is stuck or spinning"

    async def observe(self, ctx: WatcherContext) -> WatcherResult:
        config = self.config
        max_same_calls = config.get("max_same_calls", 3)
        min_progress_steps = config.get("min_progress_steps", 5)

        # Check for repeated tool calls
        if len(ctx.messages) >= max_same_calls * 2:
            recent_assistant = [
                m for m in ctx.messages[-max_same_calls * 2 :]
                if m.get("role") == "assistant"
            ]
            if len(recent_assistant) >= max_same_calls:
                # Check if tool calls are repeating
                tool_calls = []
                for msg in recent_assistant:
                    if "tool_calls" in msg:
                        for tc in msg["tool_calls"]:
                            tool_calls.append(
                                f"{tc.get('function', {}).get('name', '')}:{tc.get('function', {}).get('arguments', '')}"
                            )

                if len(tool_calls) >= max_same_calls:
                    # Check for repetition
                    if len(set(tool_calls[-max_same_calls:])) == 1:
                        return WatcherResult.nudge(
                            guidance=(
                                "You appear to be repeating the same action. "
                                "Consider a different approach or ask for clarification."
                            ),
                            reason=f"Repeated tool call: {tool_calls[-1][:100]}",
                        )

        # Check for no session completions in a while
        if ctx.step >= min_progress_steps:
            completed = [
                e for e in ctx.events
                if e.get("kind") == "session_completed"
            ]
            started = [
                e for e in ctx.events
                if e.get("kind") == "session_started"
            ]
            if len(started) > 0 and len(completed) == 0:
                return WatcherResult.nudge(
                    guidance=(
                        "Several sessions have been started but none completed. "
                        "Focus on completing current sessions before starting new ones."
                    ),
                    reason="No session completions",
                )

        return WatcherResult.ok()


@register_watcher("budget")
class BudgetWatcher(Watcher):
    """
    Watches resource budget (steps, sessions).

    Warns when approaching limits.
    """

    name = "budget"
    description = "Monitors resource usage against limits"

    async def observe(self, ctx: WatcherContext) -> WatcherResult:
        config = self.config
        warn_at_percent = config.get("warn_at_percent", 80)
        max_sessions = config.get("max_sessions", 10)

        # Check step budget
        if ctx.max_steps > 0:
            percent_used = (ctx.step / ctx.max_steps) * 100
            if percent_used >= warn_at_percent:
                remaining = ctx.max_steps - ctx.step
                return WatcherResult.nudge(
                    guidance=(
                        f"You have {remaining} steps remaining out of {ctx.max_steps}. "
                        "Prioritize completing the most important parts of the task."
                    ),
                    reason=f"Step budget {percent_used:.0f}% used",
                )

        # Check session count
        if len(ctx.sessions) >= max_sessions:
            return WatcherResult.nudge(
                guidance=(
                    f"You have {len(ctx.sessions)} active sessions. "
                    "Consider completing or closing existing sessions before starting new ones."
                ),
                reason=f"Session limit reached ({max_sessions})",
            )

        return WatcherResult.ok()


@register_watcher("scope")
class ScopeWatcher(Watcher):
    """
    Watches for scope creep.

    Ensures the agent stays focused on the original task.
    """

    name = "scope"
    description = "Detects scope creep and keeps agent on task"

    async def observe(self, ctx: WatcherContext) -> WatcherResult:
        config = self.config
        focus_keywords = config.get("focus_keywords", [])
        avoid_keywords = config.get("avoid_keywords", [])
        max_tangent_steps = config.get("max_tangent_steps", 3)

        # Check last few messages for avoid keywords
        if avoid_keywords:
            recent_content = " ".join(
                m.get("content", "") or ""
                for m in ctx.messages[-max_tangent_steps * 2:]
            ).lower()

            for keyword in avoid_keywords:
                if keyword.lower() in recent_content:
                    return WatcherResult.nudge(
                        guidance=(
                            f"The task involves '{keyword}' which may be out of scope. "
                            f"Remember the original task: {ctx.task[:200]}"
                        ),
                        reason=f"Detected avoid keyword: {keyword}",
                    )

        return WatcherResult.ok()


@register_watcher("pattern")
class PatternWatcher(Watcher):
    """
    Watches for specific patterns in output.

    Configurable regex patterns that trigger nudges/alerts.
    """

    name = "pattern"
    description = "Watches for configurable patterns in output"

    async def observe(self, ctx: WatcherContext) -> WatcherResult:
        config = self.config
        patterns = config.get("patterns", [])

        # Each pattern is: {"regex": "...", "action": "nudge|pause|abort", "message": "..."}
        for pattern_config in patterns:
            regex = pattern_config.get("regex")
            if not regex:
                continue

            try:
                compiled = re.compile(regex, re.IGNORECASE)
            except re.error:
                continue

            # Check recent messages
            for msg in ctx.messages[-10:]:
                content = msg.get("content", "") or ""
                if compiled.search(content):
                    action = pattern_config.get("action", "nudge")
                    message = pattern_config.get("message", f"Pattern matched: {regex}")

                    if action == "abort":
                        return WatcherResult.abort(message)
                    elif action == "pause":
                        return WatcherResult.pause(message)
                    else:
                        return WatcherResult.nudge(guidance=message, reason=f"Pattern: {regex}")

        return WatcherResult.ok()


@register_watcher("quality")
class QualityWatcher(Watcher):
    """
    Watches for quality issues.

    Detects:
    - Missing tests when code is written
    - Large file changes
    - Missing error handling
    """

    name = "quality"
    description = "Watches for quality issues in code changes"

    async def observe(self, ctx: WatcherContext) -> WatcherResult:
        config = self.config
        require_tests = config.get("require_tests", True)
        max_files_changed = config.get("max_files_changed", 10)

        # Check for large changes
        if len(ctx.files_changed) > max_files_changed:
            return WatcherResult.nudge(
                guidance=(
                    f"You've modified {len(ctx.files_changed)} files. "
                    "Consider breaking this into smaller, focused changes."
                ),
                reason=f"Large change: {len(ctx.files_changed)} files",
            )

        # Check for tests if code files are changed
        if require_tests and ctx.files_changed:
            code_files = [
                f for f in ctx.files_changed
                if f.endswith((".py", ".js", ".ts", ".go", ".rs"))
                and not f.startswith("test_")
                and not f.endswith("_test.py")
                and "/test" not in f
            ]
            test_files = [
                f for f in ctx.files_changed
                if "test" in f.lower()
            ]

            if code_files and not test_files:
                return WatcherResult.nudge(
                    guidance=(
                        "Code files were modified but no test files were added or updated. "
                        "Consider adding tests for the changes."
                    ),
                    reason="Code without tests",
                )

        return WatcherResult.ok()
