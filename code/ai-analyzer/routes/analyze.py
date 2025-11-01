"""
FastAPI router exposing the consensus analysis endpoint.

This module integrates the analyzer dispatcher with FastAPI.
It handles request validation, runs the correct AI pipeline,
stores the result in the database, and returns a structured JSON response.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional

from analyzer import analyze_topic
from db.session import SessionLocal, init_db

router = APIRouter(prefix="/analyze", tags=["analysis"])


# ---------------------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------------------
def get_db():
    """Dependency for injecting a SQLAlchemy session into routes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------
# Request and response schemas
# ---------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    """Schema for incoming analysis requests."""
    question_id: Optional[int] = Field(
        default=None,
        description="Optional ID of the question being analyzed. If omitted, a temporary question will be created."
    )
    question_type: str = Field(
        description=(
            "Type of analysis: 'stance_analysis', 'option_comparison', "
            "'idea_generation', 'priority_ranking', or 'feedback_analysis'."
        )
    )
    topic: str = Field(..., description="The topic or question being analyzed.")
    opinions: List[str] = Field(..., description="List of opinions, ideas, or feedback texts.")


class AnalyzeResponse(BaseModel):
    """Schema for returning analysis results."""
    id: str
    question_type: str
    topic: str
    summary: Optional[str] = None
    recommendation: Optional[str] = None
    ai_thought: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    extra: Optional[dict] = None


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@router.post("/", response_model=AnalyzeResponse, status_code=status.HTTP_201_CREATED)
def run_analysis(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Run an AI consensus analysis on the given topic.

    This endpoint triggers the appropriate analysis pipeline based on `question_type`,
    stores the result in the database, and returns a structured summary.
    """
    init_db()
    try:
        result = analyze_topic(
            question_type=payload.question_type,
            topic=payload.topic,
            opinions=payload.opinions,
            session=db,
            question_id=payload.question_id,  # ✅ new field passed through
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))

    # Separate generic fields from any additional data
    generic_keys = {
        "id", "question_type", "topic", "summary", "recommendation",
        "ai_thought", "created_at", "updated_at"
    }
    extra = {k: v for k, v in result.items() if k not in generic_keys}

    return AnalyzeResponse(
        id=result["id"],
        question_type=result["question_type"],
        topic=result["topic"],
        summary=result.get("summary"),
        recommendation=result.get("recommendation"),
        ai_thought=result.get("ai_thought"),
        created_at=result.get("created_at"),
        updated_at=result.get("updated_at"),
        extra=extra or None,
    )
