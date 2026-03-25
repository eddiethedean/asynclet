"""
Optional APScheduler integration — install with ``pip install 'asynclet[scheduler]'``.

To drive timers on the same loop as asynclet tasks, obtain the loop with
``asynclet.worker.get_worker_loop()`` and configure ``AsyncIOScheduler`` with that loop
(see APScheduler docs for ``AsyncIOScheduler(event_loop=...)``).
"""

from __future__ import annotations

__all__: list[str] = []

try:  # pragma: no branch - optional dependency
    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    __all__.append("AsyncIOScheduler")
except ImportError:
    AsyncIOScheduler = None  # type: ignore[misc,assignment]
