"""Task 2: Content Review."""
from typing import Any, Dict
from app.features.environment.models import Action, Reward
from app.features.tasks.base import BaseTask
from app.features.tasks.content_review.fixtures import FIXTURES
from app.features.tasks.content_review.grader import ContentReviewGrader


class ContentReviewTask(BaseTask):
    task_id = "content-review"

    def __init__(self) -> None:
        self._grader = ContentReviewGrader()

    def get_fixtures(self):
        return FIXTURES

    def grade(self, action: Action, ground_truth: Dict[str, Any], step: int, max_steps: int) -> Reward:
        return self._grader.grade(action, ground_truth, step, max_steps)
