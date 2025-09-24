"""Simple JSON persistence for user progress."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

DEFAULT_STATE: Dict[str, Any] = {
    "curriculum": [],
    "last_quiz_results": {},
    "reminder_minutes": 45,
}

STATE_FILE = Path(__file__).resolve().parent / "user_state.json"


def default_state() -> Dict[str, Any]:
    """Return a new copy of the default state structure."""

    return json.loads(json.dumps(DEFAULT_STATE))


def load_state(path: Path | None = None) -> Dict[str, Any]:
    """Load previously saved state or return the defaults."""

    target = path or STATE_FILE
    if not target.exists():
        return default_state()
    with target.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(state: Dict[str, Any], path: Path | None = None) -> None:
    """Persist application state to disk."""

    target = path or STATE_FILE
    with target.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)


__all__ = ["load_state", "save_state", "STATE_FILE", "DEFAULT_STATE", "default_state"]
