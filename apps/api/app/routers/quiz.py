from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field


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


FAKE_QUESTIONS = {
    "intro-python": QuizQuestion(
        id="intro-python",
        prompt="Apa output dari print(1 + 1)?",
        choices=["11", "2", "'1 + 1'"],
        answer_index=1,
    )
}


@router.get("/{question_id}", response_model=QuizQuestion)
async def get_quiz(question_id: str) -> QuizQuestion:
    try:
        return FAKE_QUESTIONS[question_id]
    except KeyError as exc:  # pragma: no cover - simple placeholder
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found") from exc


@router.post("/{question_id}", response_model=QuizResult)
async def submit_quiz(question_id: str, attempt: QuizAttempt) -> QuizResult:
    question = FAKE_QUESTIONS.get(question_id)
    if not question:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Quiz not found")
    is_correct = attempt.selected_index == question.answer_index
    return QuizResult(correct=is_correct, submitted_at=datetime.utcnow())
