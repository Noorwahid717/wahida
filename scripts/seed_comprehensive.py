#!/usr/bin/env python3
"""Comprehensive seed script for Wahida educational content."""

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

def seed_comprehensive_data():
    """Insert comprehensive educational content into the database."""

    # Create engine and tables
    engine = create_engine("sqlite:///wahida.db", future=True, pool_pre_ping=True)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    # 10 Exercises covering different topics
    exercises_data = [
        # Loops
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440001"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa output dari kode berikut?\nfor i in range(3):\n    print(i)",
                "choices": ["0 1 2", "1 2 3", "0 1 2 3", "Error"],
            },
            "answer_key": {"answer_index": 0}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440002"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Loop mana yang benar untuk mengulang list ['a', 'b', 'c']?",
                "choices": [
                    "for item in my_list:",
                    "for i in len(my_list):",
                    "while my_list:",
                    "foreach item in my_list:"
                ],
            },
            "answer_key": {"answer_index": 0}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440003"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa fungsi range(5) di Python?",
                "choices": [
                    "Membuat list [5]",
                    "Membuat sequence 0,1,2,3,4",
                    "Mengulang 5 kali",
                    "Error"
                ],
            },
            "answer_key": {"answer_index": 1}
        },

        # Lists and Dictionaries
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440004"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Bagaimana mengakses elemen pertama list my_list?",
                "choices": ["my_list[1]", "my_list[0]", "my_list.first()", "my_list.get(0)"],
            },
            "answer_key": {"answer_index": 1}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440005"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa output dari len([1,2,3,4])?",
                "choices": ["3", "4", "5", "[1,2,3,4]"],
            },
            "answer_key": {"answer_index": 1}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440006"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Bagaimana membuat dictionary di Python?",
                "choices": [
                    "dict = {key: value}",
                    "dict = [key, value]",
                    "dict = (key, value)",
                    "dict = key: value"
                ],
            },
            "answer_key": {"answer_index": 0}
        },

        # CSV Processing
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440007"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Library apa yang digunakan untuk membaca CSV di Python?",
                "choices": ["csv", "pandas", "json", "xml"],
            },
            "answer_key": {"answer_index": 0}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440008"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Fungsi apa yang digunakan untuk membaca CSV?",
                "choices": ["csv.read()", "csv.reader()", "csv.open()", "csv.load()"],
            },
            "answer_key": {"answer_index": 1}
        },

        # AI Literacy
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440009"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Apa yang dimaksud dengan Machine Learning?",
                "choices": [
                    "Komputer yang bisa berbicara",
                    "Algoritma yang belajar dari data",
                    "Robot yang bisa berjalan",
                    "Program yang menerjemahkan bahasa"
                ],
            },
            "answer_key": {"answer_index": 1}
        },
        {
            "id": uuid.UUID("550e8400-e29b-41d4-a716-446655440010"),
            "type": ExerciseType.MCQ,
            "payload": {
                "prompt": "Contoh aplikasi AI di kehidupan sehari-hari?",
                "choices": [
                    "Kalkulator sederhana",
                    "Rekomendasi video di YouTube",
                    "Kamus bahasa",
                    "Kalender"
                ],
            },
            "answer_key": {"answer_index": 1}
        },
    ]

    session = SessionLocal()
    try:
        print("🌱 Seeding exercises...")

        for exercise_data in exercises_data:
            # Check if exercise already exists
            existing = session.query(Exercise).filter(Exercise.id == exercise_data["id"]).first()
            if existing:
                print(f"⏭️  Exercise {exercise_data['id']} already exists, skipping...")
                continue

            exercise = Exercise(
                id=exercise_data["id"],
                type=exercise_data["type"],
                payload=exercise_data["payload"],
                answer_key=exercise_data["answer_key"]
            )
            session.add(exercise)
            print(f"✅ Added exercise: {exercise_data['payload']['prompt'][:50]}...")

        session.commit()
        print("🎉 Exercise seeding completed!")

        # Summary
        total_exercises = len(exercises_data)
        print(f"\n📊 Seeding Summary:")
        print(f"   • Total exercises: {total_exercises}")
        print(f"   • Loops: 3 exercises")
        print(f"   • Lists/Dicts: 3 exercises")
        print(f"   • CSV: 2 exercises")
        print(f"   • AI Literacy: 2 exercises")

    except Exception as e:
        session.rollback()
        print(f"❌ Error seeding data: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_comprehensive_data()