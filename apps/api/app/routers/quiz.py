from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.core.db import get_db
from app.models.core import Exercise, Attempt, User


class QuizQuestion(BaseModel):
    id: str
    prompt: str
    choices: list[str]
    answer_index: int


class QuizAttempt(BaseModel):
    question_id: str
    selected_index: Annotated[int, Field(ge=0)]


class QuizResult(BaseModel):
    correct: bool
    submitted_at: datetime


router = APIRouter(prefix="/quiz", tags=["quiz"])


@router.get("/{question_id}", response_model=QuizQuestion, dependencies=[Depends(get_current_user)])
async def get_quiz(question_id: str, db: Session = Depends(get_db)) -> QuizQuestion:
    """Get a quiz question by ID."""
    try:
        exercise = db.query(Exercise).filter(Exercise.id == question_id).first()
        if not exercise:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")
        
        # Parse the exercise payload
        payload = exercise.payload
        return QuizQuestion(
            id=str(exercise.id),
            prompt=payload.get("prompt", ""),
            choices=payload.get("choices", []),
            answer_index=payload.get("answer_index", 0)
        )
    except Exception as e:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Database error: {str(e)}")


@router.post("/{question_id}", response_model=QuizResult, dependencies=[Depends(get_current_user)])
async def submit_quiz(
    question_id: str, 
    attempt: QuizAttempt, 
    request: Request,
    db: Session = Depends(get_db)
) -> QuizResult:
    """Submit a quiz attempt and save to database."""
    # Get current user from auth
    current_user = get_current_user(request)
    user_id = current_user.get("id") if isinstance(current_user, dict) else current_user.id
    
    # Get the exercise
    exercise = db.query(Exercise).filter(Exercise.id == question_id).first()
    if not exercise:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")
    
    # Check if answer is correct
    answer_key = exercise.answer_key
    is_correct = attempt.selected_index == answer_key.get("answer_index", -1)
    score = 100 if is_correct else 0
    
    # Create attempt record
    db_attempt = Attempt(
        user_id=user_id,
        exercise_id=question_id,
        score=score,
        feedback="Correct!" if is_correct else "Incorrect. Try again!",
        started_at=datetime.utcnow(),
        finished_at=datetime.utcnow()
    )
    
    try:
        db.add(db_attempt)
        db.commit()
        db.refresh(db_attempt)
    except Exception as e:
        db.rollback()
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, f"Failed to save attempt: {str(e)}")
    
    return QuizResult(correct=is_correct, submitted_at=datetime.utcnow())
