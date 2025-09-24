from __future__ import annotations

from learning_app.curriculum import generate_curriculum
from learning_app.models import Lesson


def make_lessons() -> list[Lesson]:
    return [
        Lesson(
            id="math_easy",
            topic="Mathematics",
            title="Math Foundations",
            description="",
            difficulty=1,
            duration="15",
            activities=[],
        ),
        Lesson(
            id="math_medium",
            topic="Mathematics",
            title="Math Practice",
            description="",
            difficulty=2,
            duration="15",
            activities=[],
        ),
        Lesson(
            id="science_easy",
            topic="Science",
            title="Science Intro",
            description="",
            difficulty=1,
            duration="15",
            activities=[],
        ),
        Lesson(
            id="science_hard",
            topic="Science",
            title="Science Extension",
            description="",
            difficulty=3,
            duration="15",
            activities=[],
        ),
    ]


def test_generate_curriculum_prioritises_lower_scores():
    lessons = make_lessons()
    summary = {
        "Mathematics": {"correct": 1, "total": 5},
        "Science": {"correct": 4, "total": 4},
    }

    plan = generate_curriculum(summary, lessons, days_per_topic=1)

    assert len(plan) == 2
    assert plan[0]["lesson"]["id"] == "math_easy"
    assert plan[1]["lesson"]["id"] in {"science_easy", "science_hard"}
    assert plan[0]["summary"]["target_difficulty"] == 1
    assert plan[1]["summary"]["target_difficulty"] == 3


def test_generate_curriculum_empty_results():
    lessons = make_lessons()
    plan = generate_curriculum({}, lessons)
    assert plan == []
