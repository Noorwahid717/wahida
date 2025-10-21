#!/usr/bin/env python3
"""Standalone script to seed quiz data."""

import os
import sys
from pathlib import Path
import uuid

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "apps" / "api"))

# Set up minimal environment
os.environ.setdefault("POSTGRES_DSN", "sqlite:///wahida.db")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.core import Base, Exercise, ExerciseType

def seed_quiz_data():
    """Insert sample quiz questions into the database."""

    # Create engine and tables
    engine = create_engine("sqlite:///wahida.db", future=True, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    sample_exercises = [
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa output dari print(1 + 1)?",
                "choices": ["11", "2", "'1 + 1'"],
            },
            "answer_key": {
                "answer_index": 1
            }
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Fungsi apa yang digunakan untuk mencetak output di Python?",
                "choices": ["input()", "print()", "output()", "write()"],
            },
            "answer_key": {
                "answer_index": 1
            }
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440003"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa tipe data dari hasil 5 / 2 di Python 3?",
                "choices": ["int", "float", "str", "bool"],
            },
            "answer_key": {
                "answer_index": 1
            }
        }
    ]

    session = SessionLocal()
    try:
        for exercise_data in sample_exercises:
            # Check if exercise already exists
            existing = session.query(Exercise).filter(Exercise.id == exercise_data["id"]).first()
            if existing:
                print(f"Exercise {exercise_data['id']} already exists, skipping...")
                continue

            exercise = Exercise(
                id=exercise_data["id"],
                type=exercise_data["type"],
                payload=exercise_data["payload"],
                answer_key=exercise_data["answer_key"]
            )
            session.add(exercise)
            print(f"Added exercise: {exercise_data['payload']['prompt'][:50]}...")

        session.commit()
        print("Quiz seeding completed!")
    except Exception as e:
        session.rollback()
        print(f"Error seeding data: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_quiz_data()