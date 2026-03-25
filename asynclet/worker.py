from __future__ import annotations

import asyncio
import atexit
import concurrent.futures
import threading
from typing import Any, Coroutine, Optional, TypeVar

T = TypeVar("T")

_loop: Optional[asyncio.AbstractEventLoop] = None
_thread: Optional[threading.Thread] = None
_lock = threading.Lock()


def _run_loop(loop: asyncio.AbstractEventLoop, ready: threading.Event) -> None:
    asyncio.set_event_loop(loop)
    ready.set()
    loop.run_forever()


def get_worker_loop() -> asyncio.AbstractEventLoop:
    """Return the dedicated asyncio loop (starts the worker thread on first use)."""
    global _loop, _thread
    with _lock:
        if _thread is not None and _thread.is_alive() and _loop is not None:
            return _loop
        ready = threading.Event()
        loop = asyncio.new_event_loop()
        thread = threading.Thread(
            target=_run_loop,
            args=(loop, ready),
            name="asynclet-worker",
            daemon=True,
        )
        thread.start()
        if not ready.wait(timeout=30.0):
            raise RuntimeError("asynclet worker failed to start")
        _loop = loop
        _thread = thread
        return loop


def submit_coro(coro: Coroutine[Any, Any, T]) -> concurrent.futures.Future[T]:
    loop = get_worker_loop()
    return asyncio.run_coroutine_threadsafe(coro, loop)


def shutdown_worker() -> None:
    global _loop, _thread
    with _lock:
        loop, _loop = _loop, None
        th, _thread = _thread, None
    if loop is not None and loop.is_running():
        loop.call_soon_threadsafe(loop.stop)
    if th is not None:
        th.join(timeout=5.0)


atexit.register(shutdown_worker)
