"""
Legal-Assistant OpenEnv — FastAPI application factory.
Feature-based architecture: each feature owns its router.
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.exceptions import (
    EpisodeNotStartedError,
    InvalidActionError,
    TaskNotFoundError,
    episode_not_started_handler,
    invalid_action_handler,
    task_not_found_handler,
)
from app.core.logging import get_logger, setup_logging
from app.features.environment.router import router as env_router
from app.features.health.router import router as health_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    s = get_settings()
    setup_logging(s.log_level)
    logger.info(f"Starting {s.environment_name} v{s.environment_version}")
    yield
    logger.info("Shutting down")


def create_app() -> FastAPI:
    s = get_settings()

    app = FastAPI(
        title="Legal-Assistant OpenEnv",
        description=(
            "An OpenEnv environment for AI-powered legal document analysis. "
            "Includes 3 tasks: format-check (easy), content-review (medium), "
            "compliance-check (hard — Indian contract law)."
        ),
        version=s.environment_version,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS (open for HF Space access) ─────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ───────────────────────────────────────────────────
    app.add_exception_handler(TaskNotFoundError, task_not_found_handler)
    app.add_exception_handler(EpisodeNotStartedError, episode_not_started_handler)
    app.add_exception_handler(InvalidActionError, invalid_action_handler)

    # ── Routers ──────────────────────────────────────────────────────────────
    app.include_router(health_router)
    app.include_router(env_router)

    return app


app = create_app()
