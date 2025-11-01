"""
FastAPI router exposing the consensus analysis endpoints.

Includes:
- POST /analyze/ → runs an AI consensus analysis and stores results.
- GET /analyze/report/{question_id} → retrieves the report for a question if available.

This module connects the analyzer dispatcher with FastAPI,
handles validation, persistence, and structured responses.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict

from analyzer import analyze_topic
from db.session import SessionLocal, init_db
from db.models.question import Question
from db.models.ai_analysis import (
    StanceAnalysis,
    OptionComparison,
    IdeaGeneration,
    PriorityRanking,
    FeedbackAnalysis,
)

router = APIRouter(prefix="/analyze", tags=["analysis"])


# ---------------------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------------------
def get_db():
    """Dependency that provides a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------
class AnalyzeRequest(BaseModel):
    """Schema for incoming analysis requests."""
    question_id: int = Field(..., description="ID of the existing question to analyze.")
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
# POST /analyze/ — Run analysis (requires existing question)
# ---------------------------------------------------------------------
@router.post("/", response_model=AnalyzeResponse, status_code=status.HTTP_201_CREATED)
def run_analysis(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Run an AI consensus analysis for an existing question.

    The question must already exist in the database.
    The analysis type is determined from the question's type.
    Once complete, the question's `report_id` is updated with the new analysis record.
    """
    init_db()

    # -----------------------------------------------------------------
    # 1. Check that the question exists
    # -----------------------------------------------------------------
    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Question with ID {payload.question_id} not found."
        )

    # -----------------------------------------------------------------
    # 2. Retrieve the question type from related QuestionType
    # -----------------------------------------------------------------
    if not question.question_type or not question.question_type.type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question type is missing or invalid."
        )

    question_type = question.question_type.type

    # Prevent re-analysis if already processed
    if question.report_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Report already exists for question {payload.question_id}."
        )

    # -----------------------------------------------------------------
    # 3. Run the analysis
    # -----------------------------------------------------------------
    try:
        result = analyze_topic(
            question_type=question_type,
            topic=payload.topic,
            opinions=payload.opinions,
            session=db,
            question_id=question.id,
        )

        # Link the analysis record back to the question
        question.report_id = result["id"]
        db.commit()

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid analysis parameters: {exc}"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {exc}"
        )

    # -----------------------------------------------------------------
    # 4. Structure the response
    # -----------------------------------------------------------------
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


# ---------------------------------------------------------------------
# GET /analyze/report/{question_id} — Retrieve report
# ---------------------------------------------------------------------
MODEL_MAP = {
    "stance_analysis": StanceAnalysis,
    "option_comparison": OptionComparison,
    "idea_generation": IdeaGeneration,
    "priority_ranking": PriorityRanking,
    "feedback_analysis": FeedbackAnalysis,
}


@router.get("/report/{question_id}")
def get_report(question_id: int, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Retrieve the AI analysis report associated with a specific question.

    If the report has not yet been generated, a clear message is returned
    indicating the current state (pending or missing).
    """
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if not question.question_type or not question.question_type.type:
        raise HTTPException(status_code=400, detail="Question type not defined.")

    model_class = MODEL_MAP.get(question.question_type.type)
    if not model_class:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported analysis type '{question.question_type.type}' for this question."
        )

    # If report not yet generated
    if not question.report_id:
        return {
            "question_id": question.id,
            "type": question.question_type.type,
            "status": "pending",
            "message": "Analysis report not yet generated for this question."
        }

    # Retrieve report
    report = db.query(model_class).filter(model_class.id == question.report_id).first()
    if not report:
        return {
            "question_id": question.id,
            "type": question.question_type.type,
            "status": "missing",
            "message": f"Report ID {question.report_id} not found. It may not have been generated yet."
        }

    # Convert model instance to dict
    data = report.__dict__.copy()
    data.pop("_sa_instance_state", None)
    data["question_id"] = question.id
    data["type"] = question.question_type.type
    data["status"] = "ready"

    return data
