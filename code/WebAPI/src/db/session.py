from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config import DATABASE_URL
from .base import Base

# SQLAlchemy engine initialization
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db() -> None:
    """Create database tables if they do not exist."""
    Base.metadata.create_all(engine)

# === GET DB===
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()