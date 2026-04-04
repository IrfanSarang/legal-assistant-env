"""
LegalAssistantEnv — the core OpenEnv environment class.
Implements reset() / step() / state() as required by the OpenEnv spec.
"""
from __future__ import annotations

import random
from typing import Any, Dict, Tuple

from app.core.config import get_settings
from app.core.exceptions import EpisodeNotStartedError, TaskNotFoundError
from app.features.environment.models import (
    Action,
    CurrentState,
    Observation,
    Reward,
    StepResponse,
)
from app.features.environment.state import EpisodeState
from app.features.tasks.format_check.task import FormatCheckTask
from app.features.tasks.content_review.task import ContentReviewTask
from app.features.tasks.compliance_check.task import ComplianceCheckTask

TASK_REGISTRY = {
    "format-check": FormatCheckTask,
    "content-review": ContentReviewTask,
    "compliance-check": ComplianceCheckTask,
}

TASK_INSTRUCTIONS = {
    "format-check": (
        "You are a legal document formatter. Analyze the document and identify ALL formatting issues. "
        "Return your analysis as a JSON object with keys:\n"
        "  - 'issues': list of dicts with {type, description, location, severity}\n"
        "  - 'summary': string summarizing the overall format compliance\n"
        "  - 'format_score': float 0-1 your self-assessed score\n"
        "Types: page_numbers, text_alignment, font, margins, headings, line_spacing"
    ),
    "content-review": (
        "You are a legal content reviewer. Analyze the document for errors and extract all PII. "
        "Return your analysis as a JSON object with keys:\n"
        "  - 'errors': list of dicts with {type, text, correction, location}\n"
        "    Error types: grammar, spelling, logical_inconsistency\n"
        "  - 'pii': dict with keys: names, emails, phones, addresses, companies, shops\n"
        "    Each is a list of strings found in the document\n"
        "  - 'summary': string summarizing findings"
    ),
    "compliance-check": (
        "You are an expert in Indian contract law. Analyze the document for legal compliance. "
        "Check against: Indian Contract Act 1872, IT Act 2000, Consumer Protection Act 2019, "
        "DPDP Act 2023, Arbitration and Conciliation Act 1996. "
        "Return your analysis as a JSON object with keys:\n"
        "  - 'violations': list of dicts with {clause, law, section, issue, suggestion}\n"
        "  - 'compliant_clauses': list of strings describing compliant clauses found\n"
        "  - 'summary': string summarizing compliance status"
    ),
}


class LegalAssistantEnv:
    """
    OpenEnv-compliant environment for legal document analysis.

    Episode lifecycle:
        reset(task) → Observation
        step(action) → StepResponse
        state() → CurrentState
    """

    def __init__(self) -> None:
        self._state = EpisodeState()
        self._settings = get_settings()
        self._task_handlers = {k: v() for k, v in TASK_REGISTRY.items()}

    # ── OpenEnv Interface ────────────────────────────────────────────────────

    def reset(self, task: str = "format-check", fixture_id: str | None = None) -> Observation:
        """Start a new episode. Returns the initial observation."""
        if task not in TASK_REGISTRY:
            raise TaskNotFoundError(task)

        handler = self._task_handlers[task]
        fixture = handler.sample_fixture(fixture_id)
        max_steps = self._settings.max_steps_for_task(task)

        self._state.reset(
            task=task,
            fixture_id=fixture["id"],
            document_text=fixture["document_text"],
            ground_truth=fixture["ground_truth"],
            max_steps=max_steps,
        )

        return Observation(
            task=task,
            document_text=fixture["document_text"],
            instructions=TASK_INSTRUCTIONS[task],
            step=0,
            max_steps=max_steps,
            previous_reward=0.0,
            metadata={
                "fixture_id": fixture["id"],
                "difficulty": fixture.get("difficulty", "unknown"),
                "document_type": fixture.get("document_type", "contract"),
                "jurisdiction": fixture.get("jurisdiction", "India"),
            },
        )

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """Process an agent action. Returns (observation, reward, done, info)."""
        if not self._state.active:
            raise EpisodeNotStartedError()

        handler = self._task_handlers[self._state.task]

        # Grade the action against ground truth
        reward = handler.grade(
            action=action,
            ground_truth=self._state.ground_truth,
            step=self._state.step,
            max_steps=self._state.max_steps,
        )

        # Record step — advances counter, checks done
        self._state.record_step(reward.score)
        done = self._state.done or reward.done

        if done:
            self._state.done = True
            self._state.active = False

        next_obs = Observation(
            task=self._state.task,
            document_text=self._state.document_text,
            instructions=TASK_INSTRUCTIONS[self._state.task],
            step=self._state.step,
            max_steps=self._state.max_steps,
            previous_reward=reward.score,
            metadata={
                "fixture_id": self._state.fixture_id,
                "cumulative_reward": round(self._state.cumulative_reward, 4),
            },
        )

        info = {
            "step": self._state.step,
            "cumulative_reward": round(self._state.cumulative_reward, 4),
            "fixture_id": self._state.fixture_id,
        }

        return next_obs, reward, done, info

    def state(self) -> CurrentState:
        """Return current episode state snapshot."""
        return CurrentState(**self._state.to_dict())
