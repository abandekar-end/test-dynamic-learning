"""Utility helpers for loading static learning content."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .models import Lesson

DATA_DIR = Path(__file__).resolve().parent / "data"
LESSON_FILE = DATA_DIR / "lessons.json"


def load_lessons(source: Path | None = None) -> List[Lesson]:
    """Load curated lessons from disk.

    Parameters
    ----------
    source:
        Optional path override for the lesson definition file.

    Returns
    -------
    list[Lesson]
        A list of available lessons across all topics and difficulty levels.
    """

    path = source or LESSON_FILE
    with path.open("r", encoding="utf-8") as handle:
        raw_items: Iterable[dict] = json.load(handle)
    return [Lesson(**item) for item in raw_items]


__all__ = ["load_lessons", "DATA_DIR", "LESSON_FILE"]
