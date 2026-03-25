"""
Optional APScheduler integration — install with ``pip install 'asynclet[scheduler]'``.

To drive timers on the same loop as asynclet tasks, obtain the loop with
``asynclet.worker.get_worker_loop()`` and configure ``AsyncIOScheduler`` with that loop
(see APScheduler docs for ``AsyncIOScheduler(event_loop=...)``).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Type

__all__: list[str] = []

if TYPE_CHECKING:  # pragma: no cover
    from apscheduler.schedulers.asyncio import AsyncIOScheduler as _AsyncIOScheduler

AsyncIOScheduler: Optional[Type["_AsyncIOScheduler"]]

try:  # pragma: no branch - optional dependency
    from apscheduler.schedulers.asyncio import AsyncIOScheduler as _RuntimeAsyncIOScheduler

    AsyncIOScheduler = _RuntimeAsyncIOScheduler
    __all__.append("AsyncIOScheduler")
except ImportError:
    AsyncIOScheduler = None
