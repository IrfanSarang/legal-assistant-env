"""Abstract base classes for tasks and graders."""
from __future__ import annotations

import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from app.features.environment.models import Action, Reward


class BaseTask(ABC):
    """Abstract base for all legal-assistant tasks."""

    task_id: str = ""

    @abstractmethod
    def get_fixtures(self) -> List[Dict[str, Any]]:
        """Return list of all available fixtures for this task."""
        ...

    def sample_fixture(self, fixture_id: Optional[str] = None) -> Dict[str, Any]:
        """Return a fixture by ID or a random one."""
        fixtures = self.get_fixtures()
        if fixture_id is not None:
            matches = [f for f in fixtures if f["id"] == fixture_id]
            if matches:
                return matches[0]
        return random.choice(fixtures)

    @abstractmethod
    def grade(
        self,
        action: Action,
        ground_truth: Dict[str, Any],
        step: int,
        max_steps: int,
    ) -> Reward:
        """Grade the agent's action and return a Reward."""
        ...


def f1_score(predicted: List[str], expected: List[str]) -> float:
    """Compute F1 score between two lists of strings (case-insensitive)."""
    if not expected and not predicted:
        return 1.0
    if not expected or not predicted:
        return 0.0

    pred_set = {s.lower().strip() for s in predicted}
    exp_set = {s.lower().strip() for s in expected}

    tp = len(pred_set & exp_set)
    precision = tp / len(pred_set) if pred_set else 0.0
    recall = tp / len(exp_set) if exp_set else 0.0

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def partial_match_score(predicted: List[str], expected: List[str], threshold: float = 0.6) -> float:
    """
    Compute a score using partial string matching (substring containment).
    Useful for addresses and names where exact match is too strict.
    """
    if not expected:
        return 1.0 if not predicted else 0.8  # no false positives bonus
    if not predicted:
        return 0.0

    matched = 0
    for exp in expected:
        exp_lower = exp.lower().strip()
        for pred in predicted:
            pred_lower = pred.lower().strip()
            if exp_lower in pred_lower or pred_lower in exp_lower:
                matched += 1
                break

    recall = matched / len(expected)

    # Penalize false positives mildly
    false_pos = max(0, len(predicted) - matched)
    fp_penalty = min(0.2, false_pos * 0.05)

    return max(0.0, recall - fp_penalty)
