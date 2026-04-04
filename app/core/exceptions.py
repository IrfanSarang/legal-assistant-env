"""Custom exception classes and FastAPI exception handlers."""
from fastapi import Request
from fastapi.responses import JSONResponse


class TaskNotFoundError(Exception):
    def __init__(self, task: str):
        self.task = task
        super().__init__(f"Task '{task}' not found. Valid tasks: format-check, content-review, compliance-check")


class EpisodeNotStartedError(Exception):
    def __init__(self):
        super().__init__("No active episode. Call POST /env/reset first.")


class InvalidActionError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(f"Invalid action: {detail}")


async def task_not_found_handler(request: Request, exc: TaskNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"error": str(exc), "task": exc.task})


async def episode_not_started_handler(request: Request, exc: EpisodeNotStartedError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"error": str(exc)})


async def invalid_action_handler(request: Request, exc: InvalidActionError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"error": str(exc)})
