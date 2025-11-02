from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from src.crud.question import get_question_type_by_question_id
from src.db.session import get_db
from src.auth.authentication import get_current_team_lead
from src import schemas, crud

router = APIRouter()

@router.post("/", response_model=schemas.QuestionCreateResponse)
def create_question_endpoint(
    question_data: schemas.QuestionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_lead=Depends(get_current_team_lead),
):
    question, tokens = crud.question.create_question(db, question_data, current_lead.id, background_tasks)
    return {"question": question, "tokens": tokens}


@router.get("/")
def get_all_questions(db: Session = Depends(get_db), current_lead=Depends(get_current_team_lead)):
    return crud.question.get_questions_by_lead(db, current_lead.id)


@router.get("/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db), current_lead=Depends(get_current_team_lead)):
    question = crud.question.get_question_by_id(db, question_id, current_lead.id)
    return question


@router.delete("/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db), current_lead=Depends(get_current_team_lead)):
    success = crud.question.delete_question(db, question_id, current_lead.id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found or not authorized")
    return {"message": "Question deleted successfully"}

@router.get("/answer-counter/{question_id}")
def get_answer_count(
    question_id: int,
    db: Session = Depends(get_db),
    current_lead=Depends(get_current_team_lead),
):
    """
    Return the number of answers saved for a question,
    including its tokens and expiration dates.
    """
    result = crud.question.get_answer_count_by_question(db, question_id, current_lead.id)
    return result

@router.get("/type/{question_id}", response_model=schemas.QuestionTypeOut)
def read_question_type(question_id: int, db: Session = Depends(get_db)):

    question_type = get_question_type_by_question_id(db, question_id)
    if not question_type:
        raise HTTPException(status_code=404, detail="Question or QuestionType not found")
    return question_type