from datetime import date

from fastapi import APIRouter
from pydantic import BaseModel


class ProgressSummary(BaseModel):
    user_id: str
    streak_days: int
    badges: list[str]
    last_active: date


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/{user_id}", response_model=ProgressSummary)
async def get_progress(user_id: str) -> ProgressSummary:
    """Return a sample progress payload that mirrors the production contract."""
    return ProgressSummary(
        user_id=user_id,
        streak_days=3,
        badges=["starter", "consistent-learner"],
        last_active=date.today(),
    )
