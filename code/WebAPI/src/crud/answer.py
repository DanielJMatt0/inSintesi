from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.db import models


def create_answer(db: Session, token_value: str, content: str):
    """
    Create an answer using a valid token.
    Steps:
    - Check if token exists and is valid
    - Retrieve associated question
    - Create and link answer to that question
    - Optionally mark token as used
    """
    token = db.query(models.Token).filter(models.Token.token_value == token_value).first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )

    if token.expires_at:
        if token.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired"
            )

    if token.used:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has already been used"
        )

    answer = models.Answer(
        content=content,
        question_id=token.question_id
    )

    db.add(answer)

    if token.used is not None:
        token.used = True
    db.commit()
    db.refresh(answer)

    return answer


def get_answers_by_question(db: Session, question_id: int):
    """Retrieve all answers for a specific question."""
    return db.query(models.Answer).filter(models.Answer.question_id == question_id).all()


def get_answer(db: Session, answer_id: int):
    """Retrieve a single answer by ID."""
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")
    return answer


def delete_answer(db: Session, answer_id: int):
    """Delete an answer (if needed for cleanup)."""
    answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not answer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")

    db.delete(answer)
    db.commit()
    return {"message": "Answer deleted successfully"}
