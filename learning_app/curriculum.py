"""Curriculum generation logic for the continuous learning experience."""
from __future__ import annotations

from typing import Dict, Iterable, List

from .models import Lesson

QuizSummary = Dict[str, Dict[str, int]]
CurriculumEntry = Dict[str, object]


def _score_ratio(summary: Dict[str, int]) -> float:
    total = summary.get("total", 0)
    if total <= 0:
        return 0.0
    return summary.get("correct", 0) / total


def _difficulty_from_ratio(ratio: float) -> int:
    if ratio < 0.4:
        return 1
    if ratio < 0.75:
        return 2
    return 3


def _rationale_for_ratio(topic: str, ratio: float) -> str:
    if ratio < 0.4:
        return f"Focus on {topic.lower()} foundations and confidence-building reps."
    if ratio < 0.75:
        return f"Strengthen {topic.lower()} strategies with supported practice."
    return f"Stretch your {topic.lower()} mastery with advanced extensions."


def generate_curriculum(
    quiz_summary: QuizSummary,
    lessons: Iterable[Lesson],
    *,
    days_per_topic: int = 2,
) -> List[CurriculumEntry]:
    """Build a personalised curriculum plan from quiz performance."""

    if not quiz_summary:
        return []

    lessons_by_topic: Dict[str, List[Lesson]] = {}
    for lesson in lessons:
        lessons_by_topic.setdefault(lesson.topic, []).append(lesson)

    for topic_lessons in lessons_by_topic.values():
        topic_lessons.sort(key=lambda item: (item.difficulty, item.title))

    ordered_topics = sorted(
        quiz_summary.items(), key=lambda item: _score_ratio(item[1])
    )

    plan: List[CurriculumEntry] = []
    day_counter = 1

    for topic, summary in ordered_topics:
        ratio = _score_ratio(summary)
        target_difficulty = _difficulty_from_ratio(ratio)
        rationale = _rationale_for_ratio(topic, ratio)
        available = lessons_by_topic.get(topic, [])
        if not available:
            continue

        ranked_lessons = sorted(
            available,
            key=lambda lesson: (
                abs(lesson.difficulty - target_difficulty),
                lesson.difficulty,
                lesson.title,
            ),
        )

        selected = ranked_lessons[:days_per_topic]
        for lesson in selected:
            entry: CurriculumEntry = {
                "entry_id": f"{lesson.id}-d{day_counter}",
                "day": day_counter,
                "lesson": lesson.to_dict(),
                "status": "pending",
                "topic": topic,
                "score_ratio": ratio,
                "summary": {
                    "correct": summary.get("correct", 0),
                    "total": summary.get("total", 0),
                    "target_difficulty": target_difficulty,
                },
                "rationale": rationale,
            }
            plan.append(entry)
            day_counter += 1

    return plan


__all__ = ["generate_curriculum"]
