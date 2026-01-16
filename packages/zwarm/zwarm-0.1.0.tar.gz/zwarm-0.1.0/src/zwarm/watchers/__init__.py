"""
Watchers: Trajectory aligners for agent behavior.

Watchers observe agent activity and can intervene to correct course.
They are composable and can be layered.
"""

from zwarm.watchers.base import Watcher, WatcherContext, WatcherResult, WatcherAction
from zwarm.watchers.registry import register_watcher, get_watcher, list_watchers
from zwarm.watchers.manager import WatcherManager, WatcherConfig, build_watcher_manager

# Import built-in watchers to register them
from zwarm.watchers import builtin as _builtin  # noqa: F401

__all__ = [
    "Watcher",
    "WatcherContext",
    "WatcherResult",
    "WatcherAction",
    "WatcherConfig",
    "WatcherManager",
    "register_watcher",
    "get_watcher",
    "list_watchers",
    "build_watcher_manager",
]
