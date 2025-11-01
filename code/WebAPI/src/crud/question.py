from sqlalchemy.orm import Session
from src import models, schemas
from fastapi import HTTPException
from datetime import datetime, timedelta
import secrets


# -------------------------
# CREATE QUESTION (with token)
# -------------------------
def create_question(db: Session, question: schemas.QuestionCreate, token_type: str = "universal",
                    users_ids: list[int] = None):
    """
    token_type: "universal" or "individual"
    users_ids: list of user_id if token_type=="individual"
    """
    team_lead = db.query(models.TeamLead).filter(models.TeamLead.id == question.team_lead_id).first()
    if not team_lead:
        raise HTTPException(status_code=404, detail="TeamLead not found")

    qtype = db.query(models.QuestionType).filter(models.QuestionType.id == question.question_type_id).first()
    if not qtype:
        raise HTTPException(status_code=404, detail="QuestionType not found")

    db_question = models.Question(
        content=question.content,
        team_lead_id=question.team_lead_id,
        question_type_id=question.question_type_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    # --- GENERATE TOKEN ---
    tokens = []

    if token_type == "universal":
        token_value = secrets.token_urlsafe(16)
        token = models.Token(
            token_value=token_value,
            question_id=db_question.id,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.add(token)
        tokens.append(token)

    elif token_type == "individual":
        if not users_ids:
            raise HTTPException(status_code=400, detail="users_ids required for individual tokens")
        for uid in users_ids:
            user = db.query(models.User).filter(models.User.id == uid).first()
            if not user:
                raise HTTPException(status_code=404, detail=f"User {uid} not found")
            token_value = secrets.token_urlsafe(16)
            token = models.Token(
                token_value=token_value,
                question_id=db_question.id,
                user_id=uid,
                expires_at=datetime.utcnow() + timedelta(days=7)
            )
            db.add(token)
            tokens.append(token)
    else:
        raise HTTPException(status_code=400, detail="Invalid token_type. Must be 'universal' or 'individual'")

    db.commit()

    return {"question": db_question, "tokens": tokens}


# -------------------------
# GET ALL QUESTIONS
# -------------------------
def get_questions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Question).offset(skip).limit(limit).all()


# -------------------------
# GET QUESTION BY ID
# -------------------------
def get_question(db: Session, question_id: int):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


# -------------------------
# DELETE QUESTION
# -------------------------
def delete_question(db: Session, question_id: int):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"detail": f"Question {question_id} deleted"}
