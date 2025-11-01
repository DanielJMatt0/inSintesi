from datetime import datetime
from http.client import HTTPException

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from src.db import models
from src.db.session import get_db
from src import crud, schemas


router = APIRouter()


@router.post("/{token_value}", response_model=schemas.AnswerResponse)
def create_answer_endpoint(
    token_value: str,
    content: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """
    Create an answer linked to a question via a token.
    Token must be valid and unused.
    """
    answer = crud.answer.create_answer(db, token_value, content)
    return answer


@router.get("/question/{token_value}", response_model=schemas.QuestionResponse)
def get_question_from_token(token_value: str, db: Session = Depends(get_db)):
    """
    Retrieve the question associated with a given token.
    Useful for showing the question to the user before submitting an answer.
    """

    token = db.query(models.Token).filter(models.Token.token_value == token_value).first()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token"
        )


    if token.expires_at:
        if token.expires_at < datetime.now(datetime.timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token has expired"
            )

    question = db.query(models.Question).filter(models.Question.id == token.question_id).first()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found for this token"
        )

    return question


@router.get("/{answer_id}", response_model=schemas.AnswerResponse)
def get_answer_endpoint(answer_id: int, db: Session = Depends(get_db)):
    """Get a single answer."""
    return crud.answer.get_answer(db, answer_id)


@router.delete("/{answer_id}")
def delete_answer_endpoint(answer_id: int, db: Session = Depends(get_db)):
    """Delete an answer."""
    return crud.answer.delete_answer(db, answer_id)
