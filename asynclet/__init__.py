"""Async task layer for Streamlit: background execution, polling, progress, cancellation."""

from asynclet.manager import TaskManager, get_default_manager, run
from asynclet.session import session_tasks
from asynclet.task import Task, TaskStatus

__all__ = [
    "Task",
    "TaskStatus",
    "TaskManager",
    "get_default_manager",
    "run",
    "session_tasks",
]

__version__ = "0.1.0"
