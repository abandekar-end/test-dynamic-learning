"""Core data models for the continuous learning application."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass
class Lesson:
    """Represents a single learning activity suggestion."""

    id: str
    topic: str
    title: str
    description: str
    difficulty: int
    duration: str
    activities: List[str]

    def to_dict(self) -> Dict[str, object]:
        """Return a JSON-serialisable representation of the lesson."""

        return asdict(self)


__all__ = ["Lesson"]
