# Continuous Learning Desktop Companion

This repository contains a lightweight, always-on learning companion. The app guides you through a dynamic curriculum that adapts after a short diagnostic quiz. It is designed to sit on your desktop so you can return for micro-learning sessions throughout the day.

## Features

- **Adaptive diagnostic quiz**: A quick six-question check-in gauges strengths across mathematics, science, and history.
- **Dynamic curriculum**: Quiz results feed a personalised series of bite-sized learning sessions with rationale and target difficulty.
- **Progress tracking**: Mark sessions complete, revisit pending activities, and refresh your plan whenever you like.
- **Gentle reminders**: Built-in prompts keep the experience “always on” by highlighting the next recommended session.

## Getting started

1. Ensure you have Python 3.10+ installed.
2. Install dependencies (only the standard library is required).
3. Launch the desktop experience:

   ```bash
   python -m learning_app.app
   ```

4. Take the diagnostic quiz when prompted to generate your personalised curriculum.
5. Return to the app throughout the day to complete sessions and keep learning momentum.

## Running tests

Unit tests validate the curriculum engine logic. Run them with:

```bash
pytest
```

## Project structure

- `learning_app/app.py` – Tkinter user interface for the learning companion.
- `learning_app/quiz.py` – Quiz configuration and scoring helper.
- `learning_app/curriculum.py` – Dynamic curriculum generator.
- `learning_app/data/lessons.json` – Curated learning activities across topics and difficulty levels.
- `learning_app/storage.py` – Local JSON persistence for curriculum progress.
- `tests/` – Unit tests for the curriculum logic.

Enjoy your continuous learning journey!
