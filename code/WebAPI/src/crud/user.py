from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.db import models


def get_user(db: Session, user_id: int, lead_id: int) -> models.User:
    """
    Retrieve a user by ID, ensuring that the user belongs to one of the teams
    managed by the logged-in team lead.
    """
    user = (
        db.query(models.User)
        .join(models.UserTeam)
        .join(models.Team)
        .filter(models.User.id == user_id, models.Team.team_lead_id == lead_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user"
        )
    return user


def list_users(db: Session, lead_id: int):
    """
    List all users belonging to teams managed by the logged-in team lead.
    """
    return (
        db.query(models.User)
        .join(models.UserTeam)
        .join(models.Team)
        .filter(models.Team.team_lead_id == lead_id)
        .all()
    )


def create_user(db: Session, user_data, lead_id: int):
    """
    Create a new user and assign them to a team owned by the current team lead.
    """

    team = (
        db.query(models.Team)
        .filter(models.Team.id == user_data.team_id, models.Team.team_lead_id == lead_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to add users to this team"
        )

    existing_user = db.query(models.User).filter_by(email=user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user_data.email}' already exists"
        )


    user = models.User(
        name=user_data.name,
        lastname=user_data.lastname,
        email=user_data.email,
    )

    team.users.append(user)


    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user_id: int, user_data, lead_id: int):
    """
    Update a user's basic info only if they belong to one of the lead's teams.
    """
    user = get_user(db, user_id, lead_id)

    if user_data.name is not None:
        user.name = user_data.name
    if user_data.lastname is not None:
        user.lastname = user_data.lastname
    if user_data.email is not None:
        user.email = user_data.email

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int, lead_id: int):
    """
    Delete a user only if they belong to a team owned by the current team lead.
    """

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    authorized = any(team.team_lead_id == lead_id for team in user.teams)
    if not authorized:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}

def list_users_by_team(db: Session, team_id: int, lead_id: int):
    """
    List all users that belong to a specific team owned by the current team lead.
    """
    team = (
        db.query(models.Team)
        .filter(models.Team.id == team_id, models.Team.team_lead_id == lead_id)
        .first()
    )

    if not team:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this team or team does not exist"
        )

    return team.users

