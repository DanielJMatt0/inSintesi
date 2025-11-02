from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.db import models


def get_team(db: Session, team_id: int, lead_id: int = None) -> models.Team:
    """
    Retrieve a single team by ID.
    If `lead_id` is provided, ensures that the team belongs to the current team lead.
    """
    query = db.query(models.Team).filter(models.Team.id == team_id)
    if lead_id is not None:
        query = query.filter(models.Team.team_lead_id == lead_id)

    team = query.first()

    if not team:
        if lead_id is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this team"
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")

    return team


def list_teams(db: Session, lead_id: int):
    """List all teams belonging to the current team lead."""
    return db.query(models.Team).filter(models.Team.team_lead_id == lead_id).all()


def create_team(db: Session, team_data, lead_id: int):
    """Create a new team for the logged-in team lead."""
    team = models.Team(name=team_data.name,team_lead_id=lead_id)

    # Add members if provided
    if team_data.users_ids:
        users = db.query(models.User).filter(models.User.id.in_(team_data.users_ids)).all()
        team.users.extend(users)

    db.add(team)
    db.commit()
    db.refresh(team)
    return team


def update_team(db: Session, team_id: int, team_data, lead_id: int):
    """Update an existing team if it belongs to the current team lead."""
    team = get_team(db, team_id, lead_id)

    if team_data.name is not None:
        team.name = team_data.name

    # Replace all users if provided
    if team_data.users_ids is not None:
        users = db.query(models.User).filter(models.User.id.in_(team_data.users_ids)).all()
        team.users = users

    db.commit()
    db.refresh(team)

    orphan_users = (
        db.query(models.User)
        .outerjoin(models.UserTeam)
        .filter(models.UserTeam.team_id == None)
        .all()
    )

    for user in orphan_users:
        db.delete(user)

    db.commit()
    db.refresh(team)

    return team


def delete_team(db: Session, team_id: int, lead_id: int):
    """Delete a team only if the logged-in team lead owns it."""
    team = get_team(db, team_id, lead_id)
    db.delete(team)
    db.commit()
