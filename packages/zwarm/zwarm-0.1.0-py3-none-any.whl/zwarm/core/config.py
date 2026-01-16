"""
Configuration system for zwarm.

Supports:
- config.toml for user settings (weave project, defaults)
- .env for environment variables
- Composable YAML configs with inheritance (extends:)
- CLI overrides via --set key=value
"""

from __future__ import annotations

import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


@dataclass
class WeaveConfig:
    """Weave integration settings."""

    project: str | None = None
    enabled: bool = True


@dataclass
class ExecutorConfig:
    """Configuration for an executor (coding agent)."""

    adapter: str = "codex_mcp"  # codex_mcp | codex_exec | claude_code
    model: str | None = None
    sandbox: str = "workspace-write"  # read-only | workspace-write | danger-full-access
    timeout: int = 3600


@dataclass
class OrchestratorConfig:
    """Configuration for the orchestrator."""

    lm: str = "gpt-5-mini"
    prompt: str | None = None  # path to prompt yaml
    tools: list[str] = field(default_factory=lambda: ["delegate", "converse", "check_session", "end_session", "bash"])
    max_steps: int = 50
    parallel_delegations: int = 4
    sync_first: bool = True  # prefer sync mode by default


@dataclass
class WatcherConfigItem:
    """Configuration for a single watcher."""

    name: str
    enabled: bool = True
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class WatchersConfig:
    """Configuration for watchers."""

    enabled: bool = True
    watchers: list[WatcherConfigItem] = field(default_factory=lambda: [
        WatcherConfigItem(name="progress"),
        WatcherConfigItem(name="budget"),
    ])


@dataclass
class ZwarmConfig:
    """Root configuration for zwarm."""

    weave: WeaveConfig = field(default_factory=WeaveConfig)
    executor: ExecutorConfig = field(default_factory=ExecutorConfig)
    orchestrator: OrchestratorConfig = field(default_factory=OrchestratorConfig)
    watchers: WatchersConfig = field(default_factory=WatchersConfig)
    state_dir: str = ".zwarm"

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ZwarmConfig:
        """Create config from dictionary."""
        weave_data = data.get("weave", {})
        executor_data = data.get("executor", {})
        orchestrator_data = data.get("orchestrator", {})
        watchers_data = data.get("watchers", {})

        # Parse watchers config
        watchers_config = WatchersConfig(
            enabled=watchers_data.get("enabled", True),
            watchers=[
                WatcherConfigItem(**w) if isinstance(w, dict) else w
                for w in watchers_data.get("watchers", [])
            ] or WatchersConfig().watchers,
        )

        return cls(
            weave=WeaveConfig(**weave_data) if weave_data else WeaveConfig(),
            executor=ExecutorConfig(**executor_data) if executor_data else ExecutorConfig(),
            orchestrator=OrchestratorConfig(**orchestrator_data) if orchestrator_data else OrchestratorConfig(),
            watchers=watchers_config,
            state_dir=data.get("state_dir", ".zwarm"),
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "weave": {
                "project": self.weave.project,
                "enabled": self.weave.enabled,
            },
            "executor": {
                "adapter": self.executor.adapter,
                "model": self.executor.model,
                "sandbox": self.executor.sandbox,
                "timeout": self.executor.timeout,
            },
            "orchestrator": {
                "lm": self.orchestrator.lm,
                "prompt": self.orchestrator.prompt,
                "tools": self.orchestrator.tools,
                "max_steps": self.orchestrator.max_steps,
                "parallel_delegations": self.orchestrator.parallel_delegations,
                "sync_first": self.orchestrator.sync_first,
            },
            "watchers": {
                "enabled": self.watchers.enabled,
                "watchers": [
                    {"name": w.name, "enabled": w.enabled, "config": w.config}
                    for w in self.watchers.watchers
                ],
            },
            "state_dir": self.state_dir,
        }


def load_env(path: Path | None = None) -> None:
    """Load .env file if it exists."""
    if path is None:
        path = Path.cwd() / ".env"
    if path.exists():
        load_dotenv(path)


def load_toml_config(path: Path | None = None) -> dict[str, Any]:
    """Load config.toml file."""
    if path is None:
        path = Path.cwd() / "config.toml"
    if not path.exists():
        return {}
    with open(path, "rb") as f:
        return tomllib.load(f)


def load_yaml_config(path: Path) -> dict[str, Any]:
    """
    Load YAML config with inheritance support.

    Supports 'extends: path/to/base.yaml' for composition.
    """
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f) or {}

    # Handle inheritance
    extends = data.pop("extends", None)
    if extends:
        base_path = (path.parent / extends).resolve()
        base_data = load_yaml_config(base_path)
        # Deep merge: data overrides base
        data = deep_merge(base_data, data)

    return data


def deep_merge(base: dict, override: dict) -> dict:
    """Deep merge two dicts, with override taking precedence."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def apply_overrides(config: dict[str, Any], overrides: list[str]) -> dict[str, Any]:
    """
    Apply CLI overrides in format 'key.path=value'.

    Example: 'orchestrator.lm=claude-sonnet' sets config['orchestrator']['lm'] = 'claude-sonnet'
    """
    result = config.copy()
    for override in overrides:
        if "=" not in override:
            continue
        key_path, value = override.split("=", 1)
        keys = key_path.split(".")

        # Parse value (try int, float, bool, then string)
        parsed_value: Any = value
        if value.lower() == "true":
            parsed_value = True
        elif value.lower() == "false":
            parsed_value = False
        else:
            try:
                parsed_value = int(value)
            except ValueError:
                try:
                    parsed_value = float(value)
                except ValueError:
                    pass  # Keep as string

        # Navigate and set
        target = result
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        target[keys[-1]] = parsed_value

    return result


def load_config(
    config_path: Path | None = None,
    toml_path: Path | None = None,
    env_path: Path | None = None,
    overrides: list[str] | None = None,
) -> ZwarmConfig:
    """
    Load configuration with full precedence chain:
    1. Defaults (in dataclasses)
    2. config.toml (user settings)
    3. YAML config file (if provided)
    4. CLI overrides (--set key=value)
    5. Environment variables (for secrets)
    """
    # Load .env first (for secrets)
    load_env(env_path)

    # Start with defaults
    config_dict: dict[str, Any] = {}

    # Layer in config.toml
    toml_config = load_toml_config(toml_path)
    if toml_config:
        config_dict = deep_merge(config_dict, toml_config)

    # Layer in YAML config
    if config_path and config_path.exists():
        yaml_config = load_yaml_config(config_path)
        config_dict = deep_merge(config_dict, yaml_config)

    # Apply CLI overrides
    if overrides:
        config_dict = apply_overrides(config_dict, overrides)

    # Apply environment variables for weave
    if os.getenv("WEAVE_PROJECT"):
        if "weave" not in config_dict:
            config_dict["weave"] = {}
        config_dict["weave"]["project"] = os.getenv("WEAVE_PROJECT")

    return ZwarmConfig.from_dict(config_dict)
