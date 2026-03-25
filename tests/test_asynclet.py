from __future__ import annotations

import asyncio
import time

import pytest

import asynclet


def test_run_sync_function():
    def add(a: int, b: int) -> int:
        return a + b

    task = asynclet.run(add, 2, 3)
    deadline = time.monotonic() + 10.0
    while not task.done and time.monotonic() < deadline:
        time.sleep(0.01)
    assert task.done
    assert task.status == asynclet.TaskStatus.DONE
    assert task.result == 5


@pytest.mark.asyncio
async def test_run_async_coroutine():
    async def double(x: int) -> int:
        await asyncio.sleep(0.01)
        return x * 2

    task = asynclet.run(double, 21)
    for _ in range(500):
        if task.done:
            break
        await asyncio.sleep(0.01)
    assert task.done
    assert task.result == 42


@pytest.mark.asyncio
async def test_progress_queue_injected():
    async def emit(progress_queue, n: int) -> int:
        for i in range(n):
            await progress_queue.async_q.put(i)
        return n

    task = asynclet.run(emit, 4)
    seen: list[int] = []
    for _ in range(200):
        seen.extend(task.progress)
        if task.done:
            break
        await asyncio.sleep(0.01)
    seen.extend(task.progress)
    assert task.result == 4
    assert seen == [0, 1, 2, 3]


def test_cancel_before_run_finishes():
    async def slow() -> str:
        await asyncio.sleep(60)
        return "done"

    task = asynclet.run(slow)
    # Allow worker to start the coroutine
    time.sleep(0.05)
    assert task.cancel() is True
    deadline = time.monotonic() + 10.0
    while not task.done and time.monotonic() < deadline:
        time.sleep(0.01)
    assert task.status == asynclet.TaskStatus.CANCELLED


def test_error_surfaces_on_task():
    def boom() -> None:
        raise ValueError("nope")

    task = asynclet.run(boom)
    deadline = time.monotonic() + 10.0
    while not task.done and time.monotonic() < deadline:
        time.sleep(0.01)
    assert task.status == asynclet.TaskStatus.ERROR
    assert task.error is not None
    with pytest.raises(ValueError, match="nope"):
        _ = task.result
