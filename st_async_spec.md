# Streamlit Async Task Layer -- Package Specification

## Package Name (working)

st_async

------------------------------------------------------------------------

## 1. Overview

st_async provides an async task layer for Streamlit, enabling: -
Background execution of sync and async functions - Non-blocking UI
updates via polling - Progress streaming - Task lifecycle management
(status, result, cancel)

------------------------------------------------------------------------

## 2. Goals

-   Preserve Streamlit's rerun model
-   Provide simple API for async execution
-   Support both sync and async functions transparently
-   Avoid requiring users to understand asyncio

------------------------------------------------------------------------

## 3. Core Architecture

### Components

1.  Async Worker

-   Dedicated background thread
-   Runs asyncio event loop

2.  Task Manager

-   Submits tasks
-   Tracks task lifecycle
-   Stores results

3.  Janus Queue

-   Sync/async bridge
-   Enables progress streaming

4.  Scheduler (optional)

-   APScheduler for retries and periodic tasks

------------------------------------------------------------------------

## 4. Dependencies

-   asyncer
-   janus
-   APScheduler (optional)
-   asyncio (stdlib)
-   concurrent.futures (stdlib)

------------------------------------------------------------------------

## 5. Public API

### Run Task

``` python
task = st_async.run(func, *args, **kwargs)
```

### Task Properties

``` python
task.done
task.result
task.status
task.cancel()
task.progress
```

------------------------------------------------------------------------

## 6. Task Lifecycle

States: - PENDING - RUNNING - DONE - ERROR - CANCELLED

------------------------------------------------------------------------

## 7. Internal Design

### Task Object

-   id: str
-   future: Future
-   progress_queue: Janus Queue
-   status: Enum

### Task Manager

-   submit()
-   get()
-   cleanup()

------------------------------------------------------------------------

## 8. Progress Streaming

Async functions can emit progress:

``` python
async def job(queue):
    for i in range(10):
        await queue.async_q.put(i)
```

Streamlit side reads from queue.

------------------------------------------------------------------------

## 9. Session Handling

-   Tasks stored in st.session_state
-   Optional global registry for shared tasks

------------------------------------------------------------------------

## 10. Error Handling

-   Exceptions captured in Future
-   Exposed via task.error

------------------------------------------------------------------------

## 11. Cancellation

-   Uses future.cancel()
-   Graceful cancellation via anyio

------------------------------------------------------------------------

## 12. Performance Considerations

-   Single global event loop
-   Thread-safe structures
-   Cleanup completed tasks

------------------------------------------------------------------------

## 13. Roadmap

### v0.1

-   Basic task execution
-   Sync + async support
-   Polling API

### v0.2

-   Progress streaming
-   Cancellation

### v0.3

-   APScheduler integration
-   Retry support

### v1.0

-   Distributed backend support
-   Plugin system

------------------------------------------------------------------------

## 14. Example Usage

``` python
import st_async

task = st_async.run(fetch_data)

if task.done:
    st.write(task.result)
else:
    st.write("Loading...")
```

------------------------------------------------------------------------

## 15. Future Extensions

-   Celery / Ray backend
-   WebSocket updates
-   Reactive UI bindings

------------------------------------------------------------------------

## 16. Conclusion

st_async enhances Streamlit with modern async capabilities while
preserving its simplicity.
