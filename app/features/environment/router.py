"""
OpenEnv environment API routes.
  POST /reset  → Observation
  POST /step   → StepResponse
  GET  /state  → CurrentState
"""
from fastapi import APIRouter, Query

from app.features.environment.env import LegalAssistantEnv
from app.features.environment.models import (
    Action,
    CurrentState,
    Observation,
    StepResponse,
)

router = APIRouter(tags=["environment"])

# Singleton env instance (stateful per process — fine for single-user HF Space)
_env = LegalAssistantEnv()


@router.post("/reset", response_model=Observation, summary="Reset environment")
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


@router.post("/step", response_model=StepResponse, summary="Submit agent action")
async def step(action: Action) -> StepResponse:
    obs, reward, done, info = _env.step(action)
    return StepResponse(observation=obs, reward=reward, done=done, info=info)


@router.get("/state", response_model=CurrentState, summary="Get current state")
async def state() -> CurrentState:
    return _env.state()