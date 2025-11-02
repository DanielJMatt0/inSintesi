from http.client import HTTPException

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from src import schemas
from src.db import models

from fastapi import HTTPException, BackgroundTasks

from src.utils.email import send_token_email
from src.utils.question_type import get_question_type_by_content


def create_question(
    db: Session,
    question_data: schemas.QuestionCreate,
    lead_id: int,
    background_tasks: BackgroundTasks,
):
    """
    Create a new question, automatically assign its type based on content,
    generate tokens, and optionally send emails.
    """

    # 1. Prepare base question data (exclude token-related fields)
    question_dict = question_data.dict(
        exclude={"token_type", "teams_ids", "users_ids", "expires_at"}
    )
    question_dict["team_lead_id"] = lead_id

    # 2. Automatically determine the question type from content (returns numeric ID)
    question_type_id = get_question_type_by_content(db, question_data.content)
    question_dict["question_type_id"] = question_type_id

    # 3. Create and add the question
    question = models.Question(**question_dict)
    db.add(question)
    db.flush()  # flush to get the question ID before commit

    # 4. Link teams if provided
    if question_data.teams_ids:
        teams = (
            db.query(models.Team)
            .filter(models.Team.id.in_(question_data.teams_ids))
            .all()
        )

        for t in teams:
            if t.team_lead_id != lead_id:
                raise HTTPException(
                    status_code=403,
                    detail=f"Not authorized to assign team {t.id}",
                )

        question.teams.extend(teams)

    # 5. Token management
    token_expires_at = question_data.expires_at
    tokens = []

    # Universal token (one token for everyone)
    if question_data.token_type == "universal":
        token_value = secrets.token_urlsafe(16)
        db.add(
            models.Token(
                token_value=token_value,
                question_id=question.id,
                expires_at=token_expires_at,
                used=None,
            )
        )
        tokens.append(token_value)

    # Individual tokens (one per user)
    elif question_data.token_type == "individual":
        user_ids_set = set(question_data.users_ids or [])

        # Include users from assigned teams
        if question_data.teams_ids:
            team_users = (
                db.query(models.User.id)
                .join(models.UserTeam, models.User.id == models.UserTeam.user_id)
                .filter(models.UserTeam.team_id.in_(question_data.teams_ids))
                .all()
            )
            team_user_ids = {u[0] for u in team_users}
            user_ids_set.update(team_user_ids)

        # Retrieve all users to generate tokens for
        users = (
            db.query(models.User)
            .filter(models.User.id.in_(user_ids_set))
            .all()
        )

        for user in users:
            token_value = secrets.token_urlsafe(16)
            db.add(
                models.Token(
                    token_value=token_value,
                    question_id=question.id,
                    user_id=user.id,
                    expires_at=token_expires_at,
                    used=False,
                )
            )
            tokens.append(token_value)

            # Send token email asynchronously
            background_tasks.add_task(
                send_token_email, user.email, token_value, question.content
            )

    # 6. Commit and refresh
    db.commit()
    db.refresh(question)

    return question, tokens


def get_questions_by_lead(db: Session, lead_id: int):
    """Return only questions created by the given team lead."""
    return db.query(models.Question).filter(models.Question.team_lead_id == lead_id).all()


def get_question_by_id(db: Session, question_id: int, lead_id: int):
    """Return a question only if it belongs to the current team lead."""
    question = (
        db.query(models.Question)
        .filter(models.Question.id == question_id, models.Question.team_lead_id == lead_id)
        .first()
    )

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found or not authorized"
        )
    return question

def delete_question(db: Session, question_id: int, lead_id: int):
    """Delete only if the question belongs to the given lead."""
    question = (
        db.query(models.Question)
        .filter(models.Question.id == question_id, models.Question.team_lead_id == lead_id)
        .first()
    )
    if not question:
        return None

    db.delete(question)
    db.commit()
    return True


def get_answer_count_by_question(db: Session, question_id: int, lead_id: int):
    """Return the number of answers for a given question, if owned by the team lead."""
    from src.db import models

    question = (
        db.query(models.Question)
        .filter(models.Question.id == question_id, models.Question.team_lead_id == lead_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found or not authorized"
        )

    answers_count = (
        db.query(models.Answer)
        .filter(models.Answer.question_id == question_id)
        .count()
    )

    tokens = (
        db.query(models.Token)
        .filter(models.Token.question_id == question_id)
        .all()
    )

    token_data = [
        {"token_value": t.token_value, "expires_at": t.expires_at}
        for t in tokens
    ]

    return {
        "question_id": question.id,
        "answers_count": answers_count,
        "tokens": token_data,
    }
