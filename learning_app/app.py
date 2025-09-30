"""Tkinter desktop application for continuous learning."""
from __future__ import annotations

import datetime as _dt
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict

from .curriculum import generate_curriculum
from .data import load_lessons
from .quiz import QUIZ_QUESTIONS, evaluate_responses
from .storage import default_state, load_state, save_state

REMINDER_INTERVAL_SECONDS = 60


class QuizDialog(tk.Toplevel):
    """Simple multi-step quiz dialog."""

    def __init__(self, parent: tk.Tk):
        super().__init__(parent)
        self.title("Diagnostic Quiz")
        self.geometry("520x400")
        self.resizable(False, False)
        self.questions = QUIZ_QUESTIONS
        self.responses: Dict[str, str] = {}
        self._index = 0
        self.result: Dict[str, Dict[str, int]] | None = None

        self.option_var = tk.StringVar(value="")
        self.progress_var = tk.StringVar()

        self._build_widgets()
        self._show_question()

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self._cancel)

    def _build_widgets(self) -> None:
        padding = {"padx": 16, "pady": 8}
        ttk.Label(self, text="Tell us where to focus today", font=("Segoe UI", 14, "bold")).pack(
            **padding
        )
        self.progress_label = ttk.Label(self, textvariable=self.progress_var)
        self.progress_label.pack(**padding)

        self.prompt_label = ttk.Label(
            self,
            wraplength=460,
            font=("Segoe UI", 11),
            anchor="center",
            justify="center",
        )
        self.prompt_label.pack(fill="x", padx=20, pady=(10, 4))

        self.options_frame = ttk.Frame(self)
        self.options_frame.pack(fill="x", padx=40, pady=12)

        self.skill_focus_label = ttk.Label(
            self,
            wraplength=460,
            font=("Segoe UI", 9, "italic"),
            foreground="#555555",
        )
        self.skill_focus_label.pack(fill="x", padx=20, pady=(0, 10))

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        self.back_button = ttk.Button(button_frame, text="Back", command=self._go_back)
        self.back_button.grid(row=0, column=0, padx=6)
        self.next_button = ttk.Button(button_frame, text="Next", command=self._go_next)
        self.next_button.grid(row=0, column=1, padx=6)

    def _show_question(self) -> None:
        question = self.questions[self._index]
        total_questions = len(self.questions)
        self.progress_var.set(f"Question {self._index + 1} of {total_questions}")
        self.prompt_label.config(text=question["prompt"])
        self.skill_focus_label.config(text=question["skill_focus"])

        for child in self.options_frame.winfo_children():
            child.destroy()

        self.option_var.set(self.responses.get(question["id"], ""))

        for option in question["options"]:
            ttk.Radiobutton(
                self.options_frame,
                text=option,
                value=option,
                variable=self.option_var,
            ).pack(anchor="w", pady=4)

        self.back_button.state(["!disabled"] if self._index > 0 else ["disabled"])
        is_last = self._index == total_questions - 1
        self.next_button.config(text="Finish" if is_last else "Next")

    def _go_next(self) -> None:
        selected = self.option_var.get()
        question = self.questions[self._index]
        if not selected:
            messagebox.showinfo("Select an option", "Please choose an answer to continue.")
            return
        self.responses[question["id"]] = selected

        if self._index == len(self.questions) - 1:
            self._finish()
            return
        self._index += 1
        self._show_question()

    def _go_back(self) -> None:
        if self._index == 0:
            return
        self._index -= 1
        self._show_question()

    def _finish(self) -> None:
        if len(self.responses) != len(self.questions):
            messagebox.showinfo("Incomplete", "Please answer all questions.")
            return
        self.result = evaluate_responses(self.responses)
        self.destroy()

    def _cancel(self) -> None:
        self.result = None
        self.destroy()


class LearningApp(tk.Tk):
    """Main desktop application shell."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Continuum Learning Companion")
        self.geometry("980x640")
        self.minsize(820, 560)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.state_data = load_state()
        self.lessons = load_lessons()

        self.progress_var = tk.StringVar()
        self.reminder_var = tk.StringVar()
        self.status_var = tk.StringVar()

        self._build_layout()
        self._refresh_curriculum_view()
        self._schedule_reminder()

    def _build_layout(self) -> None:
        header = ttk.Frame(self, padding=(24, 16))
        header.grid(row=0, column=0, sticky="nsew")
        header.columnconfigure(0, weight=1)

        title = ttk.Label(
            header,
            text="Continuum Learning Companion",
            font=("Segoe UI", 18, "bold"),
        )
        title.grid(row=0, column=0, sticky="w")

        ttk.Label(header, textvariable=self.progress_var, font=("Segoe UI", 11)).grid(
            row=1, column=0, sticky="w", pady=(6, 0)
        )
        ttk.Label(header, textvariable=self.reminder_var, font=("Segoe UI", 10), foreground="#3b5b92").grid(
            row=2, column=0, sticky="w", pady=(4, 0)
        )

        content = ttk.Frame(self, padding=(24, 12))
        content.grid(row=1, column=0, sticky="nsew")
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        columns = ("day", "topic", "title", "duration", "status")
        self.tree = ttk.Treeview(
            content,
            columns=columns,
            show="headings",
            height=12,
        )
        for column in columns:
            self.tree.heading(column, text=column.title())
        self.tree.column("day", width=70, anchor="center")
        self.tree.column("topic", width=140, anchor="w")
        self.tree.column("title", width=320, anchor="w")
        self.tree.column("duration", width=120, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(content, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        sidebar = ttk.Frame(content, padding=(16, 0))
        sidebar.grid(row=0, column=2, sticky="ns")

        ttk.Button(sidebar, text="Take diagnostic quiz", command=self._launch_quiz).pack(
            fill="x", pady=(0, 12)
        )
        ttk.Button(sidebar, text="Mark as completed", command=self._mark_completed).pack(
            fill="x", pady=6
        )
        ttk.Button(sidebar, text="Reset curriculum", command=self._reset_curriculum).pack(
            fill="x", pady=6
        )

        ttk.Label(sidebar, text="Status", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(16, 4))
        ttk.Label(sidebar, textvariable=self.status_var, wraplength=220, justify="left").pack(
            fill="x"
        )

        footer = ttk.Frame(self, padding=(24, 12))
        footer.grid(row=2, column=0, sticky="ew")
        ttk.Label(footer, text="Continuous learning thrives on tiny, consistent actions.").pack(
            anchor="w"
        )

    def _refresh_curriculum_view(self) -> None:
        for child in self.tree.get_children():
            self.tree.delete(child)

        curriculum = self.state_data.get("curriculum", [])
        completed = sum(1 for item in curriculum if item.get("status") == "completed")
        pending = sum(1 for item in curriculum if item.get("status") != "completed")
        total = len(curriculum)

        for entry in curriculum:
            lesson = entry.get("lesson", {})
            iid = entry.get("entry_id", lesson.get("id", ""))
            self.tree.insert(
                "",
                "end",
                iid=iid,
                values=(
                    entry.get("day"),
                    lesson.get("topic"),
                    lesson.get("title"),
                    lesson.get("duration"),
                    entry.get("status", "pending"),
                ),
            )

        if total:
            self.progress_var.set(f"{completed} of {total} sessions completed · {pending} in queue")
        else:
            self.progress_var.set("No curriculum yet. Take the quiz to get started.")

        self.status_var.set(self._status_message())
        self._update_reminder_text()

    def _status_message(self) -> str:
        curriculum = self.state_data.get("curriculum", [])
        if not curriculum:
            return "Ready when you are. A 2-minute quiz unlocks a personalised path."
        pending = [item for item in curriculum if item.get("status") != "completed"]
        if not pending:
            return "Amazing! Everything in your current plan is complete. Consider retaking the quiz to unlock new focus areas."
        next_entry = min(pending, key=lambda item: item.get("day", 0))
        lesson = next_entry.get("lesson", {})
        return (
            f"Next up: {lesson.get('title')} ({lesson.get('duration')}). "
            f"{next_entry.get('rationale', '').capitalize()}"
        )

    def _launch_quiz(self) -> None:
        dialog = QuizDialog(self)
        self.wait_window(dialog)
        if not dialog.result:
            return

        summary = dialog.result
        curriculum = generate_curriculum(summary, self.lessons, days_per_topic=3)
        self.state_data["curriculum"] = curriculum
        self.state_data["last_quiz_results"] = summary
        save_state(self.state_data)
        self._refresh_curriculum_view()
        messagebox.showinfo(
            "Curriculum ready",
            "Your refreshed learning path is ready. Let's dive in!",
        )

    def _mark_completed(self) -> None:
        selection = self.tree.selection()
        if not selection:
            messagebox.showinfo("Select a session", "Choose a session to mark as completed.")
            return

        curriculum = self.state_data.get("curriculum", [])
        updated = 0
        for item_id in selection:
            for entry in curriculum:
                if entry.get("entry_id") == item_id:
                    if entry.get("status") != "completed":
                        entry["status"] = "completed"
                        entry["completed_at"] = _dt.datetime.utcnow().isoformat()
                        updated += 1
        if updated:
            save_state(self.state_data)
            self._refresh_curriculum_view()

    def _reset_curriculum(self) -> None:
        if not messagebox.askyesno(
            "Reset plan", "Clear the current curriculum and start from scratch?"
        ):
            return
        self.state_data.clear()
        self.state_data.update(default_state())
        save_state(self.state_data)
        self._refresh_curriculum_view()

    def _update_reminder_text(self) -> None:
        pending = [item for item in self.state_data.get("curriculum", []) if item.get("status") != "completed"]
        if not pending:
            self.reminder_var.set("No reminders scheduled. You're all caught up!")
            return
        next_entry = min(pending, key=lambda item: item.get("day", 0))
        lesson = next_entry.get("lesson", {})
        self.reminder_var.set(
            f"Next reminder: focus on {lesson.get('title')} — {lesson.get('duration')} ({lesson.get('topic')})."
        )

    def _schedule_reminder(self) -> None:
        self._update_reminder_text()
        self.after(REMINDER_INTERVAL_SECONDS * 1000, self._schedule_reminder)


def main() -> None:
    try:
        app = LearningApp()
    except tk.TclError as exc:
        print(
            "Unable to start the Continuum Learning Companion because no graphical "
            "display is available."
        )
        print("Ensure you are running in an environment with an X server/GUI.")
        print(f"Tkinter error: {exc}")
        return
    app.mainloop()


if __name__ == "__main__":
    main()
