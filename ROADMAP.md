# asynclet roadmap

This document tracks intended direction for **asynclet**. It is aspirational: priorities and versions can change. For behavior and API details, see [`docs/asynclet-spec.md`](docs/asynclet-spec.md).

---

## Current release line (0.1.x)

**Theme:** solid baseline for Streamlit-style polling UIs.

Already in scope for this line:

- Dedicated **worker thread** with a single **asyncio** loop  
- **`asynclet.run`** for **sync** (via asyncer `asyncify`) and **async** callables  
- **`Task`**: `done`, `result`, `status`, `error`, `cancel`, `progress`  
- **Janus**-based **progress** for async jobs (`queue` / `progress_queue`)  
- **`TaskManager`**, default manager, **`cleanup`**, optional **`register_global`**  
- **`session_tasks`** helper for `st.session_state` (or any mapping)  
- Optional **`[scheduler]`** extra; loop access for advanced integration  

Possible **patch** work (still 0.1.x):

- Docs and examples (Streamlit snippets, edge cases)  
-   - Add a short “patterns” section: session-scoped tasks, named tasks, and cleanup guidance
-   - Document progress queue injection rules (`queue`/`progress_queue`, positional vs keyword)
-   - Document cancellation semantics (pending vs running) and what callers should expect
-   - Add a small troubleshooting/FAQ (common “why does it stay `wait`?” rerun timing gotchas)
-   - Expand examples to show error handling (`task.status`, `task.error`) and retries as user-land patterns
- Typing and API polish without breaking changes  
-   - Tighten generics on `Task[T]` and `TaskManager.submit/run` return types
-   - Clarify and standardize public annotations (`Task.progress`, `Task.error`, `session_tasks` mapping types)
-   - Ensure `asynclet/scheduler.py` optional export is typed cleanly when APScheduler is missing
- Test coverage for races and cancellation edge cases  
-   - Stress-test rapid submit/cancel before bind (“pending cancellation”) and ensure status settles correctly
-   - Add concurrency tests for many tasks completing out of order (result correctness + registry consistency)
-   - Add cancellation tests for: already-done, already-cancelled, and cancel-after-error idempotency
-   - Add progress tests for mid-run polling (drain behavior) vs tail buffering after completion

---

## Next (0.2)

**Theme:** scheduling and resilience.

- **APScheduler**: documented helpers or small wrapper types for periodic work and retries on the worker loop  
- **Retries**: configurable retry/backoff for failed tasks (opt-in per `run` or manager)  
- **Cancellation**: optional **anyio**-style or clearer cooperative-cancel patterns where it helps  

---

## Later (0.3+)

**Theme:** scale-out and richer integrations.

- **Distributed backends** (optional): e.g. **Celery** or **Ray** as pluggable executors, keeping the same `Task` polling model where feasible  
- **WebSocket** or other **push** channels alongside polling  
- **Plugins** for custom transports or observability (metrics, tracing)  

---

## 1.0 and beyond

**Theme:** stability and ecosystem.

- **Stable API** commitment and deprecation policy  
- **Reactive** patterns: tighter optional integration with Streamlit state/widgets where it does not fight the rerun model  
- Broader **examples** and **cookbook** patterns (long-running jobs, fan-out, progress UX)  

---

## How to contribute

Open issues or PRs on the project repository with concrete use cases. Roadmap items move faster when tied to real apps and clear API sketches.
