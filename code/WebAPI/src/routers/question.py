from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.session import get_db
from src import schemas, crud


router = APIRouter()

@router.post("/", response_model=schemas.QuestionCreateResponse)
def create_question_endpoint(question_data: schemas.QuestionCreate, db: Session = Depends(get_db)):
    question, tokens = crud.question.create_question(db, question_data)
    return {"question": question, "tokens": tokens}

@router.get("/")
def get_all_questions(db: Session = Depends(get_db)):
    return crud.question.get_questions(db)

@router.get("/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = crud.question.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    success = crud.question.delete_question(db, question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found")
    return {"message": "Question deleted successfully"}