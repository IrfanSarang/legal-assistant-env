"""Task 1: Format Check — wires fixtures and grader together."""
from typing import Any, Dict

from app.features.environment.models import Action, Reward
from app.features.tasks.base import BaseTask
from app.features.tasks.format_check.fixtures import FIXTURES
from app.features.tasks.format_check.grader import FormatCheckGrader


class FormatCheckTask(BaseTask):
    task_id = "format-check"

    def __init__(self) -> None:
        self._grader = FormatCheckGrader()

    def get_fixtures(self):
        return FIXTURES

    def grade(self, action: Action, ground_truth: Dict[str, Any], step: int, max_steps: int) -> Reward:
        return self._grader.grade(action, ground_truth, step, max_steps)
