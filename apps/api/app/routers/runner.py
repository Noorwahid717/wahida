from fastapi import APIRouter
from pydantic import BaseModel


class CodeRunRequest(BaseModel):
    language: str
    source: str


class CodeRunResponse(BaseModel):
    stdout: str
    stderr: str = ""
    status: str = "queued"


router = APIRouter(prefix="/run", tags=["runner"])


@router.post("/", response_model=CodeRunResponse)
async def submit_code_execution(payload: CodeRunRequest) -> CodeRunResponse:
    """Placeholder runner endpoint; integration with Judge0 will be added later."""
    return CodeRunResponse(stdout=f"Received {payload.language} code with {len(payload.source)} chars.", status="pending")
