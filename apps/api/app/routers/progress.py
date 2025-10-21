from datetime import date
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.core import User, Streak, UserBadge, Badge


class ProgressSummary(BaseModel):
    user_id: str
    streak_days: int
    badges: List[str]
    last_active: date


router = APIRouter(prefix="/progress", tags=["progress"])


@router.get(
    "/{user_id}",
    response_model=ProgressSummary,
    dependencies=[Depends(get_current_user)],
)
async def get_progress(user_id: str, db: Session = Depends(get_db)) -> ProgressSummary:
    """Get user progress from database."""
    try:
        # Get user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get streak data
        streak = db.query(Streak).filter(Streak.user_id == user_id).first()
        streak_days = streak.current if streak else 0
        
        # Get badges
        user_badges = (
            db.query(Badge.name)
            .join(UserBadge)
            .filter(UserBadge.user_id == user_id)
            .all()
        )
        badges = [badge.name for badge, in user_badges]
        
        # Calculate last active (simplified - could be based on last attempt)
        last_active = date.today()  # Placeholder
        
        return ProgressSummary(
            user_id=user_id,
            streak_days=streak_days,
            badges=badges,
            last_active=last_active,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
