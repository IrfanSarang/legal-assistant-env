"""Health check endpoints — required for HF Space automated ping."""
from fastapi import APIRouter
from app.core.config import get_settings

router = APIRouter(tags=["health"])


@router.get("/", summary="Root health check")
async def root():
    s = get_settings()
    return {
        "status": "ok",
        "environment": s.environment_name,
        "version": s.environment_version,
        "tasks": ["format-check", "content-review", "compliance-check"],
    }


@router.get("/health", summary="Health check")
async def health():
    return {"status": "healthy"}
