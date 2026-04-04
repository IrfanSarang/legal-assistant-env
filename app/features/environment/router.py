"""
OpenEnv environment API routes.
  POST /env/reset  → Observation
  POST /env/step   → StepResponse
  GET  /env/state  → CurrentState
"""
from fastapi import APIRouter, Query

from app.features.environment.env import LegalAssistantEnv
from app.features.environment.models import (
    Action,
    CurrentState,
    Observation,
    StepResponse,
)

router = APIRouter(prefix="/env", tags=["environment"])

# Singleton env instance (stateful per process — fine for single-user HF Space)
_env = LegalAssistantEnv()


@router.post(
    "/reset",
    response_model=Observation,
    summary="Reset environment",
    description="Start a new episode. Returns the initial observation with the document and instructions.",
)
async def reset(
    task: str = Query(
        default="format-check",
        description="Task to run: format-check | content-review | compliance-check",
    ),
    fixture_id: str | None = Query(
        default=None,
        description="Optional specific fixture ID. If None, a random fixture is selected.",
    ),
) -> Observation:
    return _env.reset(task=task, fixture_id=fixture_id)


@router.post(
    "/step",
    response_model=StepResponse,
    summary="Submit agent action",
    description="Submit the agent's analysis. Returns reward, next observation, and done flag.",
)
async def step(action: Action) -> StepResponse:
    obs, reward, done, info = _env.step(action)
    return StepResponse(observation=obs, reward=reward, done=done, info=info)


@router.get(
    "/state",
    response_model=CurrentState,
    summary="Get current state",
    description="Returns a snapshot of the current episode state without advancing it.",
)
async def state() -> CurrentState:
    return _env.state()
