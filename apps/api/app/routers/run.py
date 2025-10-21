from __future__ import annotations

import asyncio
import http.client
import json
from collections.abc import Awaitable, Callable

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field

from app.core import RateLimitExceeded
from app.core.config import settings
from app.core.auth import get_current_user


class CodeRunRequest(BaseModel):
    language: str = Field(pattern=r"^[a-zA-Z0-9+#]+$")
    source: str = Field(min_length=1, max_length=5000)


class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str | None = None
    status: str = "queued"
    execution_time_ms: int | None = None


router = APIRouter(prefix="/run", tags=["run"])


def enforce_run_rate_limit(request: Request) -> None:
    limiter = request.app.state.rate_limiters["run"]
    client_host = request.client.host if request.client else "anonymous"
    try:
        limiter.hit(client_host)
    except RateLimitExceeded as exc:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc)) from exc


async def _simulate_execution(payload: CodeRunRequest) -> CodeRunResponse:
    if "import socket" in payload.source or "http" in payload.source:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Network access is not permitted in the sandbox.")
    await asyncio.sleep(0.05)
    truncated_output = payload.source[:80].replace("\n", " ")
    return CodeRunResponse(
        stdout=f"Executed {payload.language} safely: {truncated_output}…",
        status="completed",
        execution_time_ms=120,
    )


@router.post("/", response_model=CodeRunResponse, dependencies=[Depends(get_current_user)])
async def submit_code_execution(
    payload: CodeRunRequest,
    _: None = Depends(enforce_run_rate_limit),
    executor: Callable[[CodeRunRequest], Awaitable[CodeRunResponse]] | None = None,
) -> CodeRunResponse:
    """Submit code execution to Judge0 or the built-in simulator."""

    # Use Judge0 if configured, otherwise simulate
    if settings.judge0_url and settings.judge0_url.startswith("https://judge0-ce.p.rapidapi.com"):
        run_callable = executor or _execute_with_judge0
    else:
        run_callable = executor or _simulate_execution

    result = await run_callable(payload)
    if result.execution_time_ms and result.execution_time_ms > 3000:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Execution exceeded time limit.")
    return result


async def _execute_with_judge0(payload: CodeRunRequest) -> CodeRunResponse:
    """Execute code using Judge0 API."""
    url = settings.judge0_url
    async with http.client.AsyncHTTPConnection(url) as conn:
        payload_json = json.dumps({
            "source": payload.source,
            "language": payload.language,
        })
        headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
            "x-rapidapi-key": settings.judge0_api_key,
        }
        response = await conn.request("POST", "/submissions", body=payload_json, headers=headers)
        if response.status != 201:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Failed to submit code to Judge0.")

        result = json.loads(response.read())
        if result["status"]["id"] == 3:  # Compilation error
            return CodeRunResponse(
                stdout="",
                stderr=result["compile_output"],
                status="error",
                execution_time_ms=0,
            )
        elif result["status"]["id"] == 2:  # Runtime error
            return CodeRunResponse(
                stdout="",
                stderr=result["stderr"],
                status="error",
                execution_time_ms=result["time"],
            )
        elif result["status"]["id"] == 1:  # Success
            return CodeRunResponse(
                stdout=result["stdout"],
                stderr="",
                status="completed",
                execution_time_ms=result["time"],
            )
        else:
            raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown error from Judge0.")
