#!/usr/bin/env python3
"""Seed the database with sample quiz questions."""

import uuid
from app.core.db import session_scope
from app.models.core import Exercise, ExerciseType


def seed_quiz_data():
    """Insert sample quiz questions into the database."""
    
    sample_exercises = [
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
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
            "id": "550e8400-e29b-41d4-a716-446655440002", 
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
            "id": "550e8400-e29b-41d4-a716-446655440003",
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
    
    with session_scope() as session:
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
    
    print("Quiz seeding completed!")


if __name__ == "__main__":
    seed_quiz_data()