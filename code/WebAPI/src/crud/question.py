from sqlalchemy.orm import Session
from src import models, schemas
from fastapi import HTTPException


# -------------------------
# CREATE QUESTION
# -------------------------
def create_question(db: Session, question: schemas.QuestionCreate):
    # Controlla team_lead
    team_lead = db.query(models.TeamLead).filter(models.TeamLead.id == question.team_lead_id).first()
    if not team_lead:
        raise HTTPException(status_code=404, detail="TeamLead not found")

    # Controlla question_type
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
    return db_question


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
