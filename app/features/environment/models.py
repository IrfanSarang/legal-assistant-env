"""
OpenEnv typed Pydantic models — Action, Observation, Reward.
These are the core contract of the Legal-Assistant environment.
"""
from __future__ import annotations

from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel, Field, field_validator


VALID_TASKS = Literal["format-check", "content-review", "compliance-check"]


class Action(BaseModel):
    """Agent's action — a structured legal analysis submission."""

    task: VALID_TASKS = Field(..., description="Which task the agent is performing")
    analysis: Dict[str, Any] = Field(
        ...,
        description=(
            "Structured analysis output. Schema varies by task:\n"
            "  format-check: {issues: [...], summary: str, format_score: float}\n"
            "  content-review: {errors: [...], pii: {names, emails, phones, addresses, companies}, summary: str}\n"
            "  compliance-check: {violations: [...], compliant_clauses: [...], summary: str}"
        ),
    )
    step_notes: str = Field("", description="Optional agent reasoning trace / chain-of-thought")


class Observation(BaseModel):
    """Environment observation returned to the agent after reset() or step()."""

    task: str = Field(..., description="Current task identifier")
    document_text: str = Field(..., description="The legal document to analyze")
    instructions: str = Field(..., description="Task-specific instructions for the agent")
    step: int = Field(..., description="Current step number (1-indexed)")
    max_steps: int = Field(..., description="Maximum steps allowed in this episode")
    previous_reward: float = Field(0.0, description="Reward from the previous step (0.0 on reset)")
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Document metadata: type, jurisdiction, difficulty, fixture_id",
    )


class Reward(BaseModel):
    """Reward signal returned after each step."""

    score: float = Field(..., description="Normalized reward in [0.0, 1.0]")
    breakdown: Dict[str, float] = Field(
        ..., description="Per-criterion partial scores contributing to total"
    )
    feedback: str = Field(..., description="Human-readable feedback explaining the score")
    done: bool = Field(..., description="Whether the episode is complete")

    @field_validator("score")
    @classmethod
    def clamp_score(cls, v: float) -> float:
        return max(0.0, min(1.0, v))


class StepResponse(BaseModel):
    """Full response from POST /env/step."""

    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class CurrentState(BaseModel):
    """Response from GET /env/state — current episode state snapshot."""

    active: bool = Field(..., description="Whether an episode is currently running")
    task: Optional[str] = None
    step: int = 0
    max_steps: int = 0
    cumulative_reward: float = 0.0
    fixture_id: Optional[str] = None
    rewards_history: list[float] = Field(default_factory=list)
