from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets

from src import models, schemas


def create_question(db: Session, question_data: schemas.QuestionCreate):
    # Creazione diretta dell’istanza SQLAlchemy dal modello Pydantic
    question_dict = question_data.dict(exclude={"token_type", "teams_ids", "users_ids"})
    question = models.Question(**question_dict)

    db.add(question)
    db.flush()

    if question_data.teams_ids:
        teams = db.query(models.Team).filter(models.Team.id.in_(question_data.teams_ids)).all()
        question.teams.extend(teams)

    tokens = []
    if question_data.token_type == "universal":
        token_value = secrets.token_urlsafe(16)
        db.add(models.Token(
            token_value=token_value,
            question_id=question.id,
            expires_at=datetime.utcnow() + timedelta(days=7),
            used=False
        ))
        tokens.append(token_value)

    elif question_data.token_type == "individual":
        user_ids_set = set(question_data.users_ids or [])
        if question_data.teams_ids:
            team_users = (
                db.query(models.User.id)
                .join(models.user_team)
                .filter(models.user_team.c.team_id.in_(question_data.teams_ids))
                .all()
            )
            team_user_ids = {u[0] for u in team_users}
            user_ids_set.update(team_user_ids)

        for user_id in user_ids_set:
            token_value = secrets.token_urlsafe(16)
            token = models.Token(
                token_value=token_value,
                question_id=question.id,
                user_id=user_id,
                expires_at=datetime.utcnow() + timedelta(days=7),
                used=False
            )
            db.add(token)
            tokens.append(token_value)

    db.commit()
    db.refresh(question)

    return question, tokens



def get_questions(db: Session):
    return db.query(models.Question).all()

def get_question_by_id(db: Session, question_id: int):
    question = (
        db.query(models.Question)
        .filter(models.Question.id == question_id)
        .first()
    )
    return question

def delete_question(db: Session, question_id: int):
    question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not question:
        return None

    db.delete(question)
    db.commit()
    return True
