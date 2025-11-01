"""
FastAPI router exposing the consensus analysis endpoints.

Endpoints:
- POST /analyze/{question_id} → runs an AI analysis if not yet generated.
- PUT /analyze/{question_id} → re-runs AI analysis and overwrites existing report.
- GET /analyze/report/{question_id} → retrieves the report for a question if available.

This module integrates the AI analyzer with FastAPI,
handles validation, persistence, and structured responses.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Optional, Any, Dict

from analyzer import analyze_topic
from db.session import SessionLocal, init_db
from db.models.question import Question, Answer
from db.models.ai_analysis import (
    StanceAnalysis,
    OptionComparison,
    IdeaGeneration,
    PriorityRanking,
    FeedbackAnalysis,
)

# ---------------------------------------------------------------------
# Router setup
# ---------------------------------------------------------------------
router = APIRouter(prefix="/analyze", tags=["analysis"])


# ---------------------------------------------------------------------
# Database session dependency
# ---------------------------------------------------------------------
def get_db():
    """Provides a SQLAlchemy session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------
# Response schema
# ---------------------------------------------------------------------
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
# Helper — Run the analysis pipeline
# ---------------------------------------------------------------------
def _run_ai_analysis(db: Session, question: Question) -> Dict[str, Any]:
    """Internal helper that executes AI analysis and persists results."""

    question_type = question.question_type.type
    topic = question.content

    # Fetch all associated answers (as opinions)
    answers = db.query(Answer).filter(Answer.question_id == question.id).all()
    opinions = [a.content for a in answers]

    if not opinions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No opinions/answers found for this question."
        )

    try:
        # Run the appropriate AI pipeline
        result = analyze_topic(
            question_type=question_type,
            topic=topic,
            opinions=opinions,
            session=db,
            question_id=question.id,
        )

        # Link the analysis record back to the question
        question.report_id = result["id"]
        db.commit()

        # Separate common fields and extras
        generic_keys = {
            "id", "question_type", "topic", "summary",
            "recommendation", "ai_thought", "created_at", "updated_at"
        }
        extra = {k: v for k, v in result.items() if k not in generic_keys}

        return {
            "id": result["id"],
            "question_type": result["question_type"],
            "topic": result["topic"],
            "summary": result.get("summary"),
            "recommendation": result.get("recommendation"),
            "ai_thought": result.get("ai_thought"),
            "created_at": result.get("created_at"),
            "updated_at": result.get("updated_at"),
            "extra": extra or None,
        }

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


# ---------------------------------------------------------------------
# POST /analyze/{question_id} — Run analysis if not exists
# ---------------------------------------------------------------------
@router.post("/{question_id}", response_model=AnalyzeResponse, status_code=status.HTTP_201_CREATED)
def run_analysis(question_id: int, db: Session = Depends(get_db)):
    """Run AI analysis for an existing question (if not already generated)."""
    init_db()

    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    if not question.question_type or not question.question_type.type:
        raise HTTPException(status_code=400, detail="Question type not defined.")

    if question.report_id:
        raise HTTPException(
            status_code=409,
            detail=f"Report already exists for question {question_id}. Use PUT to update."
        )

    return _run_ai_analysis(db, question)


# ---------------------------------------------------------------------
# PUT /analyze/{question_id} — Force re-analysis (overwrite)
# ---------------------------------------------------------------------
@router.put("/{question_id}", response_model=AnalyzeResponse)
def update_analysis(question_id: int, db: Session = Depends(get_db)):
    """
    Re-run the AI analysis for an existing question.

    This will overwrite the current report with a new one.
    """
    init_db()

    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    if not question.question_type or not question.question_type.type:
        raise HTTPException(status_code=400, detail="Question type not defined.")

    # Optionally delete old report record before re-running
    question.report_id = None
    db.commit()

    return _run_ai_analysis(db, question)


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
    """Retrieve the AI analysis report for a specific question."""
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    if not question.question_type or not question.question_type.type:
        raise HTTPException(status_code=400, detail="Question type not defined.")

    model_class = MODEL_MAP.get(question.question_type.type)
    if not model_class:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported analysis type '{question.question_type.type}' for this question."
        )

    if not question.report_id:
        return {
            "question_id": question.id,
            "type": question.question_type.type,
            "status": "pending",
            "message": "Analysis report not yet generated for this question."
        }

    report = db.query(model_class).filter(model_class.id == question.report_id).first()
    if not report:
        return {
            "question_id": question.id,
            "type": question.question_type.type,
            "status": "missing",
            "message": f"Report ID {question.report_id} not found."
        }

    data = report.__dict__.copy()
    data.pop("_sa_instance_state", None)
    data["question_id"] = question.id
    data["type"] = question.question_type.type
    data["status"] = "ready"

    return data
