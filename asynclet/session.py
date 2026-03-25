"""Streamlit session helpers (no hard dependency on Streamlit — pass ``st.session_state``)."""

from __future__ import annotations

from typing import Any, Dict, MutableMapping


def session_tasks(
    session_state: MutableMapping[str, Any],
    key: str = "asynclet_tasks",
) -> Dict[str, Any]:
    """
    Return a task registry dict stored on ``session_state[key]``.

    Example::

        import streamlit as st
        import asynclet

        tasks = asynclet.session_tasks(st.session_state)
        tasks["fetch"] = asynclet.run(load_data)
    """
    if key not in session_state:
        session_state[key] = {}
    return session_state[key]
