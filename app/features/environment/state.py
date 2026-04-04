"""Episode state — tracks the current session for the environment."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class EpisodeState:
    """Mutable episode state. One instance per running session."""

    active: bool = False
    task: Optional[str] = None
    fixture_id: Optional[str] = None
    document_text: str = ""
    ground_truth: Dict[str, Any] = field(default_factory=dict)
    step: int = 0
    max_steps: int = 0
    cumulative_reward: float = 0.0
    rewards_history: List[float] = field(default_factory=list)
    done: bool = False

    def reset(
        self,
        task: str,
        fixture_id: str,
        document_text: str,
        ground_truth: Dict[str, Any],
        max_steps: int,
    ) -> None:
        self.active = True
        self.task = task
        self.fixture_id = fixture_id
        self.document_text = document_text
        self.ground_truth = ground_truth
        self.step = 0
        self.max_steps = max_steps
        self.cumulative_reward = 0.0
        self.rewards_history = []
        self.done = False

    def record_step(self, reward: float) -> None:
        self.step += 1
        self.cumulative_reward += reward
        self.rewards_history.append(reward)
        if self.step >= self.max_steps:
            self.done = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active": self.active,
            "task": self.task,
            "step": self.step,
            "max_steps": self.max_steps,
            "cumulative_reward": round(self.cumulative_reward, 4),
            "fixture_id": self.fixture_id,
            "rewards_history": [round(r, 4) for r in self.rewards_history],
        }
