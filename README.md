# asynclet

Small **async task layer** for [Streamlit](https://streamlit.io/) (and similar “sync main thread + rerun” UIs): run sync or async work on a **dedicated background event loop**, then **poll** status, results, **progress**, and **cancellation** without blocking the UI thread.

## Install

```bash
pip install asynclet
```

Optional extras:

- **Streamlit** (for a typical app environment): `pip install 'asynclet[streamlit]'`
- **APScheduler** (optional timers/jobs): `pip install 'asynclet[scheduler]'`

Requires **Python 3.9+**.

## Quick start

```python
import streamlit as st
import asynclet

task = asynclet.run(fetch_data)

if task.done:
    st.write(task.result)
else:
    st.write("Loading…")
```

On each rerun, check `task.done` and read `task.result` when finished.

## Public API

| Item | Role |
|------|------|
| `asynclet.run(func, /, *args, manager=None, **kwargs)` | Submit `func` on the worker; returns a `Task`. |
| `Task.done` | Whether the result (or error) is ready. |
| `Task.result` | Result value; raises if not complete. |
| `Task.status` | `TaskStatus`: `PENDING`, `RUNNING`, `DONE`, `ERROR`, `CANCELLED`. |
| `Task.error` | Exception object when `status` is `ERROR`, else `None`. |
| `Task.cancel()` | Request cancellation (running tasks use asyncio cancellation; pending tasks cancel the result future). |
| `Task.progress` | Non-blocking drain of progress values (see below). |
| `TaskManager` / `get_default_manager()` | Custom registry and `cleanup()` when you keep many completed tasks. |
| `session_tasks(session_state)` | Dict stored on `st.session_state` for named tasks. |

## Progress (Janus)

Progress is supported for **async** functions only.

Declare a parameter named **`queue`** or **`progress_queue`**:

- If it is the **first** parameter, asynclet injects the Janus queue **positionally** and the remaining positional arguments to `run()` map to the rest of the signature.
- Otherwise, asynclet injects the queue by **keyword** (`queue=` / `progress_queue=`).

```python
async def job(queue, steps: int):
    for i in range(steps):
        await queue.async_q.put(i)
    return steps

task = asynclet.run(job, 10)
# Each rerun:
for x in task.progress:
    st.write(x)
```

The UI thread reads via `task.progress`, which pulls from the sync side of a [janus](https://github.com/aio-libs/janus) queue.

## Streamlit session state

```python
import streamlit as st
import asynclet

tasks = asynclet.session_tasks(st.session_state)
if "load" not in tasks:
    tasks["load"] = asynclet.run(load_data)

task = tasks["load"]
```

## Patterns

### Named tasks (per session)

Use `session_tasks(st.session_state)` as a stable dict to store tasks across reruns:

```python
tasks = asynclet.session_tasks(st.session_state)

if "load" not in tasks:
    tasks["load"] = asynclet.run(load_data)

task = tasks["load"]
```

### Cleanup (when you create many tasks)

If you create many tasks over time, keep them in a `TaskManager` and periodically call `cleanup()` to trim completed entries:

```python
m = asynclet.TaskManager(max_completed=256)
task = asynclet.run(load_data, manager=m)

# ... later:
m.cleanup()
```

## Errors

If the callable raises, `task.status` becomes `ERROR`, `task.error` holds the exception, and reading `task.result` re-raises it.

```python
if task.status == asynclet.TaskStatus.ERROR:
    st.error(f"failed: {task.error!r}")
elif task.done:
    st.write(task.result)
else:
    st.write("Loading…")
```

## Cancellation

`task.cancel()` requests cancellation:

- If the task is **running**, it schedules `asyncio` cancellation on the worker loop.
- If the task is still **pending** (not yet bound on the worker loop), it cancels the result future.

Treat `CANCELLED` as a terminal state in UI code.

## Troubleshooting / FAQ

### Why does it keep showing `wait`?

In rerun-driven UIs, a single script run may finish before the background task completes. The usual pattern is: show `wait`, then on the next rerun read `task.done` / `task.result`.

In tests (or special cases), you may need to allow a small amount of wall time between reruns for the worker to finish.

## How it works (short)

- One **daemon thread** runs a single **asyncio** event loop.
- **Async** callables run on that loop; **sync** callables run via [asyncer](https://github.com/tiangolo/asyncer)’s `asyncify` (thread pool).
- Submissions use `asyncio.run_coroutine_threadsafe`; results are bridged with a `concurrent.futures.Future` for the polling API.

## Development

```bash
pip install -e '.[dev]'
pytest
```

### Development (uv)

If you use [uv](https://github.com/astral-sh/uv), you can run tests in a fresh env like:

```bash
uv venv
uv pip install -e '.[dev]'
uv run pytest
```

The **dev** extra includes Streamlit so CI can run headless **[AppTest](https://docs.streamlit.io/develop/api-reference/app-testing)** checks in `tests/test_streamlit_apptest.py` against the sample apps under `tests/streamlit_apps/`.

## License

MIT.
