"""Task 3: Compliance Check."""
from typing import Any, Dict
from app.features.environment.models import Action, Reward
from app.features.tasks.base import BaseTask
from app.features.tasks.compliance_check.fixtures import FIXTURES
from app.features.tasks.compliance_check.grader import ComplianceCheckGrader


class ComplianceCheckTask(BaseTask):
    task_id = "compliance-check"

    def __init__(self) -> None:
        self._grader = ComplianceCheckGrader()

    def get_fixtures(self):
        return FIXTURES

    def grade(self, action: Action, ground_truth: Dict[str, Any], step: int, max_steps: int) -> Reward:
        return self._grader.grade(action, ground_truth, step, max_steps)
