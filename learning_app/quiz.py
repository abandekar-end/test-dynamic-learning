"""Diagnostic quiz configuration and utilities."""
from __future__ import annotations

from typing import Dict, List

Question = Dict[str, object]
QUIZ_QUESTIONS: List[Question] = [
    {
        "id": "math_growth_patterns",
        "topic": "Mathematics",
        "prompt": "A sequence grows by adding 4 each time (3, 7, 11, ...). What is the 6th term?",
        "options": ["19", "23", "24", "27"],
        "answer": "23",
        "skill_focus": "Recognising arithmetic patterns and extrapolating.",
    },
    {
        "id": "math_fraction_reasoning",
        "topic": "Mathematics",
        "prompt": "Which fraction is equivalent to 3/4?",
        "options": ["6/8", "8/6", "12/16", "16/12"],
        "answer": "6/8",
        "skill_focus": "Comparing and scaling rational numbers.",
    },
    {
        "id": "science_inquiry_cycle",
        "topic": "Science",
        "prompt": "Which step usually comes first in a scientific investigation?",
        "options": [
            "Collecting data",
            "Forming a hypothesis",
            "Communicating results",
            "Drawing conclusions",
        ],
        "answer": "Forming a hypothesis",
        "skill_focus": "Understanding the scientific method.",
    },
    {
        "id": "science_energy_flow",
        "topic": "Science",
        "prompt": "In a food chain, energy primarily flows from the sun to plants and then to animals. What are plants called in this system?",
        "options": ["Consumers", "Producers", "Decomposers", "Recyclers"],
        "answer": "Producers",
        "skill_focus": "Interpreting systems and energy transfer.",
    },
    {
        "id": "history_source_eval",
        "topic": "History",
        "prompt": "A diary entry from 1914 describing the start of World War I is an example of what type of source?",
        "options": [
            "Secondary source",
            "Primary source",
            "Tertiary source",
            "Reference work",
        ],
        "answer": "Primary source",
        "skill_focus": "Evaluating historical evidence.",
    },
    {
        "id": "history_causation",
        "topic": "History",
        "prompt": "Which of the following best describes a cause of the American Revolution?",
        "options": [
            "The invention of the telegraph",
            "High taxation without representation",
            "Discovery of gold in California",
            "Building of the transcontinental railroad",
        ],
        "answer": "High taxation without representation",
        "skill_focus": "Connecting political and economic change.",
    },
]


def evaluate_responses(responses: Dict[str, str]) -> Dict[str, Dict[str, int]]:
    """Summarise quiz accuracy per topic from raw responses."""

    summary: Dict[str, Dict[str, int]] = {}
    for question in QUIZ_QUESTIONS:
        topic = question["topic"]
        summary.setdefault(topic, {"correct": 0, "total": 0})
        summary[topic]["total"] += 1
        if responses.get(question["id"]) == question["answer"]:
            summary[topic]["correct"] += 1
    return summary


__all__ = ["QUIZ_QUESTIONS", "evaluate_responses"]
