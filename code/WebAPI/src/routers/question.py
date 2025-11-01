from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src import models, schemas, crud

router = APIRouter()

# -------------------------
# CREATE QUESTION
# -------------------------
@router.post("/", response_model=dict)
def create_question(question: schemas.QuestionCreate, token_type: str = "universal", users_ids: list[int] = None, db: Session = Depends(get_db)):
    return crud.create_question(db=db, question=question, token_type=token_type, users_ids=users_ids)

# -------------------------
# GET ALL QUESTIONS
# -------------------------
@router.get("/", response_model=List[schemas.Question])
def get_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_questions(db=db, skip=skip, limit=limit)

# -------------------------
# GET QUESTION BY ID
# -------------------------
@router.get("/{question_id}", response_model=schemas.Question)
def get_question(question_id: int, db: Session = Depends(get_db)):
    return crud.get_question(db=db, question_id=question_id)

# -------------------------
# DELETE QUESTION
# -------------------------
@router.delete("/{question_id}", response_model=dict)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    return crud.delete_question(db=db, question_id=question_id)
