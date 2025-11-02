import json
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL
from .base import Base
from .models import QuestionType

# ---------------------------------------------------------------------
# SQLAlchemy setup
# ---------------------------------------------------------------------
engine = create_engine(DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# ---------------------------------------------------------------------
# Database initialization
# ---------------------------------------------------------------------
def init_db() -> None:
    """Create database tables if they do not exist and seed initial data."""
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        # Locate the JSON seed file
        json_path = Path(__file__).parent / "question_type.json"

        if not json_path.exists():
            print("⚠️  question_type.json not found — skipping default seeding.")
            return

        with open(json_path, "r", encoding="utf-8") as f:
            question_types = json.load(f)

        inserted = 0
        for q in question_types:
            # Check if the type already exists
            existing = session.query(QuestionType).filter_by(type=q["type"]).first()
            if not existing:
                new_q = QuestionType(id=q["id"], type=q["type"])
                session.add(new_q)
                inserted += 1

        if inserted:
            session.commit()
            print(f"✅ Added {inserted} new question types.")
        else:
            print("ℹ️  All default question types already exist. No changes made.")

    except Exception as e:
        session.rollback()
        print(f"❌ Error during database initialization: {e}")
    finally:
        session.close()


# ---------------------------------------------------------------------
# Dependency for getting a DB session
# ---------------------------------------------------------------------
def get_db():
    """Provide a SQLAlchemy session for dependency injection (e.g., FastAPI)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
