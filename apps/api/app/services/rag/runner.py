from __future__ import annotations

from typing import Optional

from ..routers.runner import CodeRunRequest, CodeRunResponse, submit_code_execution


class LocalCodeRunner:
    """Bridge the RAG pipeline to the internal `/api/run` endpoint."""

    async def run(self, language: str, source: str) -> CodeRunResponse:
        request = CodeRunRequest(language=language, source=source)
        return await submit_code_execution(request)


RunnerLike = Optional[LocalCodeRunner]
